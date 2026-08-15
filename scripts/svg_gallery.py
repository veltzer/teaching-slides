#!/usr/bin/env python

"""
Browse SVGs in a browser, mark ones for redesign, and attach a note
explaining why.

  mark_svgs.py            # all SVGs
  mark_svgs.py --sample N # random sample of N

Each cell has a click area (toggle the mark) and a text input below
(reason for redesign). Notes auto-save as you type. Marked entries are
written to /tmp/redesign_queue.jsonl as one JSON record per line:
  {"path": "svg/...", "note": "..."}

Notes survive across sessions (loaded on startup) and re-render in the
sidebar. Server stops on Ctrl-C.
"""

import argparse
import http.server
import json
import pathlib
import random
import socketserver
import subprocess
import sys
import threading
import urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "svg"
QUEUE = pathlib.Path("/tmp/redesign_queue.jsonl")
PORT = 8765

# In-memory store: path -> {"marked": bool, "note": str}
# Loaded from QUEUE on startup, persisted on every change.
STATE: dict[str, dict] = {}
STATE_LOCK = threading.Lock()


def load_state() -> None:
    if not QUEUE.exists():
        return
    for line in QUEUE.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        path = rec.get("path")
        if not path:
            continue
        STATE[path] = {"marked": True, "note": rec.get("note", "")}


def save_state() -> None:
    lines = []
    for path, info in STATE.items():
        if info.get("marked"):
            lines.append(json.dumps({"path": path, "note": info.get("note", "")}))
    QUEUE.write_text("\n".join(lines) + ("\n" if lines else ""))


def queue_list() -> list[dict]:
    out = []
    for path, info in STATE.items():
        if info.get("marked"):
            out.append({"path": path, "note": info.get("note", "")})
    return out


def render_html(paths: list[pathlib.Path]) -> str:
    cells = []
    for p in paths:
        rel = str(p.relative_to(ROOT))
        info = STATE.get(rel, {})
        marked = " marked" if info.get("marked") else ""
        note = info.get("note", "")
        # HTML-escape the relative path and note for safe attribute insertion.
        rel_attr = rel.replace('"', "&quot;")
        note_attr = note.replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")
        src = "/svg/" + str(p.relative_to(SVG_DIR))
        cells.append(
            f'<div class="cell{marked}" data-path="{rel_attr}">'
            f'<div class="img-wrap"><img src="{src}" loading="lazy"></div>'
            f'<div class="cap">{rel_attr}</div>'
            f'<input class="note" type="text" placeholder="why redesign? (typing auto-marks)" '
            f'value="{note_attr}">'
            f'</div>'
        )
    return f"""<!doctype html><html><head><meta charset="utf-8">
<title>Mark SVGs ({len(paths)})</title>
<style>
body{{margin:0;font-family:system-ui,sans-serif;background:#222;color:#eee;
display:grid;grid-template-columns:1fr 360px;min-height:100vh}}
main{{padding:16px}}
.grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}}
.cell{{background:#fff;border-radius:6px;overflow:hidden;
border:4px solid transparent;transition:border-color .1s;
display:flex;flex-direction:column}}
.cell .img-wrap{{cursor:pointer}}
.cell .img-wrap:hover{{outline:2px solid #888;outline-offset:-2px}}
.cell.marked{{border-color:#e74c3c}}
.cell img{{width:100%;height:auto;display:block}}
.cell .cap{{padding:6px 10px;background:#333;color:#ddd;font-size:11px;
font-family:monospace;word-break:break-all}}
.cell .note{{border:0;border-top:1px solid #555;background:#1a1a1a;
color:#eee;font-family:inherit;font-size:13px;padding:8px 10px;outline:none}}
.cell .note:focus{{background:#222;border-top-color:#e74c3c}}
aside{{background:#111;padding:16px;position:sticky;top:0;height:100vh;
overflow-y:auto;border-left:1px solid #333}}
aside h2{{margin:0 0 12px;font-size:14px;text-transform:uppercase;
letter-spacing:.5px;color:#888}}
.q-item{{margin-bottom:12px;padding:8px;background:#1a1a1a;border-radius:4px}}
.q-item .q-path{{font-family:monospace;font-size:11px;color:#ddd;
word-break:break-all;margin-bottom:4px}}
.q-item .q-note{{font-size:12px;color:#aaa;font-style:italic}}
.q-item .q-note:empty:before{{content:"(no note)";color:#555}}
button{{background:#444;color:#eee;border:0;padding:8px 12px;
border-radius:4px;cursor:pointer;font-size:12px;margin-bottom:12px}}
button:hover{{background:#555}}
.count{{color:#e74c3c;font-weight:bold}}
</style></head><body>
<main><div class="grid">{''.join(cells)}</div></main>
<aside>
<h2>Redesign queue (<span class="count" id="count">0</span>)</h2>
<button onclick="clearQueue()">Clear queue</button>
<button onclick="finish()" style="background:#e74c3c">Done — fix these</button>
<div id="queue"></div>
</aside>
<script>
function escapeHTML(s) {{
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}
async function refreshQueue() {{
  const r = await fetch("/queue");
  const items = await r.json();
  document.getElementById("count").textContent = items.length;
  const html = items.map(i =>
    `<div class="q-item"><div class="q-path">${{escapeHTML(i.path)}}</div>` +
    `<div class="q-note">${{escapeHTML(i.note)}}</div></div>`
  ).join("");
  document.getElementById("queue").innerHTML = html;
  const paths = new Set(items.map(i => i.path));
  document.querySelectorAll(".cell").forEach(c => {{
    c.classList.toggle("marked", paths.has(c.dataset.path));
  }});
}}
async function toggle(path) {{
  await fetch("/toggle", {{method:"POST",
    headers:{{"content-type":"application/x-www-form-urlencoded"}},
    body:"path=" + encodeURIComponent(path)}});
  refreshQueue();
}}
async function setNote(path, note) {{
  await fetch("/note", {{method:"POST",
    headers:{{"content-type":"application/x-www-form-urlencoded"}},
    body:"path=" + encodeURIComponent(path) + "&note=" + encodeURIComponent(note)}});
  refreshQueue();
}}
async function clearQueue() {{
  if (!confirm("Clear all marks and notes?")) return;
  await fetch("/clear", {{method:"POST"}});
  document.querySelectorAll(".cell .note").forEach(n => n.value = "");
  refreshQueue();
}}
async function finish() {{
  const r = await fetch("/queue");
  const items = await r.json();
  if (!items.length) {{ alert("Queue is empty — mark some slides first."); return; }}
  if (!confirm("Stop the server and ask Claude to redesign " + items.length + " slide(s)?")) return;
  await fetch("/done", {{method:"POST"}});
  document.body.innerHTML =
    '<div style="padding:40px;font-size:18px;line-height:1.6">' +
    '<p>Server stopped. Queue saved to <code>/tmp/redesign_queue.jsonl</code>.</p>' +
    '<p>Now tell Claude: <b>"fix the queue"</b> (or similar) and it will redesign each marked slide using your notes.</p>' +
    '</div>';
}}
document.querySelectorAll(".cell").forEach(c => {{
  c.querySelector(".img-wrap").addEventListener("click",
    () => toggle(c.dataset.path));
  const note = c.querySelector(".note");
  let timer;
  note.addEventListener("input", () => {{
    clearTimeout(timer);
    timer = setTimeout(() => setNote(c.dataset.path, note.value), 350);
  }});
}});
refreshQueue();
</script></body></html>"""


def make_handler(html: str, server_holder: list):
    class H(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self._send(200, "text/html; charset=utf-8", html.encode())
                return
            if self.path == "/queue":
                with STATE_LOCK:
                    body = json.dumps(queue_list()).encode()
                self._send(200, "application/json", body)
                return
            if self.path.startswith("/svg/"):
                rel = urllib.parse.unquote(self.path[len("/svg/"):])
                target = (SVG_DIR / rel).resolve()
                try:
                    target.relative_to(SVG_DIR.resolve())
                except ValueError:
                    self._send(403, "text/plain", b"forbidden")
                    return
                if not target.is_file():
                    self._send(404, "text/plain", b"not found")
                    return
                self._send(200, "image/svg+xml", target.read_bytes())
                return
            self._send(404, "text/plain", b"not found")

        def do_POST(self):
            length = int(self.headers.get("content-length", 0))
            body = self.rfile.read(length).decode()
            params = urllib.parse.parse_qs(body, keep_blank_values=True)
            if self.path == "/toggle":
                path = params.get("path", [""])[0]
                if path:
                    with STATE_LOCK:
                        info = STATE.setdefault(path, {"marked": False, "note": ""})
                        info["marked"] = not info.get("marked", False)
                        save_state()
                self._send(200, "text/plain", b"ok")
                return
            if self.path == "/note":
                path = params.get("path", [""])[0]
                note = params.get("note", [""])[0]
                if path:
                    with STATE_LOCK:
                        info = STATE.setdefault(path, {"marked": False, "note": ""})
                        info["note"] = note
                        # Typing a note auto-marks the slide.
                        if note.strip():
                            info["marked"] = True
                        save_state()
                self._send(200, "text/plain", b"ok")
                return
            if self.path == "/clear":
                with STATE_LOCK:
                    STATE.clear()
                    save_state()
                self._send(200, "text/plain", b"ok")
                return
            if self.path == "/done":
                with STATE_LOCK:
                    items = queue_list()
                self._send(200, "text/plain", b"ok")
                # Print a clear summary so the terminal shows what to fix.
                print("\n=== Redesign queue submitted ===", file=sys.stderr)
                print(f"{len(items)} slide(s) queued in {QUEUE}", file=sys.stderr)
                for it in items:
                    note = it.get("note", "").strip() or "(no note)"
                    print(f"  - {it['path']}\n      {note}", file=sys.stderr)
                print("\nTell Claude: 'fix the queue'", file=sys.stderr)
                # Schedule shutdown so this response completes first.
                if server_holder:
                    threading.Thread(target=server_holder[0].shutdown,
                                     daemon=True).start()
                return
            self._send(404, "text/plain", b"not found")

        def _send(self, status: int, ctype: str, body: bytes) -> None:
            self.send_response(status)
            self.send_header("content-type", ctype)
            self.send_header("content-length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args, **kwargs):
            pass
    return H


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sample", type=int, default=None)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--port", type=int, default=PORT)
    p.add_argument("paths", nargs="*",
                   help="explicit SVG paths to show; overrides --sample")
    args = p.parse_args()

    if args.paths:
        paths = [pathlib.Path(p).resolve() for p in args.paths
                 if pathlib.Path(p).is_file() and pathlib.Path(p).suffix == ".svg"]
        paths.sort()
    else:
        paths = sorted(SVG_DIR.rglob("*.svg"))
        if args.sample:
            if args.seed is not None:
                random.seed(args.seed)
            paths = random.sample(paths, min(args.sample, len(paths)))
            paths.sort()

    load_state()
    html = render_html(paths)
    server_holder: list = []
    handler = make_handler(html, server_holder)

    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", args.port), handler) as srv:
        server_holder.append(srv)
        url = f"http://127.0.0.1:{args.port}/"
        print(f"serving {len(paths)} slides at {url}", file=sys.stderr)
        print(f"queue file: {QUEUE}  (Ctrl-C to stop)", file=sys.stderr)
        def _open_browser():
            subprocess.Popen(
                ["google-chrome", "--incognito", "--new-window",
                 "--user-data-dir=/tmp/chrome-incognito-svg-gallery", url],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
        threading.Timer(0.3, _open_browser).start()
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped", file=sys.stderr)


if __name__ == "__main__":
    main()
