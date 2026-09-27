---
tags:
  - networking:http
  - networking:troubleshooting
  - practices:scripting
level: advanced
category: networking
audience:
  - audiences:security-engineers
  - audiences:network-engineers
  - audiences:devops
  - audiences:sysadmins

---

# Developing and Troubleshooting iRules

---

## What This Chapter Covers

- Reading `/var/log/ltm` and `Tcl` runtime errors
- Catching errors with `catch`
- Testing in stages: log first, act later
- `Fiddler` as an intercepting proxy
- `curl` and `tcpdump` on the `BIG-IP`
- Common failure modes and how to spot them

---

## The Troubleshooting Loop

![troubleshooting_loop](svg/courses/networking/f5-bigip-advanced-irules/06_developing_and_troubleshooting_irules/troubleshooting_loop.svg)

---

## Reading /var/log/ltm

- Every `log local0.` line and every runtime error lands here
- `tail -f /var/log/ltm` while you send test traffic
- Runtime errors name the rule, the event and the line number
- The rule keeps running for other connections after an error

```bash
tail -f /var/log/ltm
```

```output
err tmm[12345]: 01220001:3: TCL error: /Common/my_rule
  <HTTP_REQUEST> - can't read "uid": no such variable
  while executing "log local0. "user $uid"" (line 4)
```

---

## Common Runtime Error Messages

| Message | Cause |
|---------|-------|
| `can't read "x": no such variable` | set in another event or branch |
| `invalid command name` | typo or a `Tcl` command not in iRules |
| `command is not valid in current event context` | `HTTP::` used in `CLIENT_ACCEPTED` |
| `Multiple redirect/respond invocations not allowed` | two responses in one request |
| `Operation not supported` | payload command before `HTTP::collect` |

---

## Catching Errors with catch

- `catch` runs a script and returns `1` on error instead of aborting
- The error message goes into the named variable
- Wrap risky code: parsing, `class` lookups, payload access
- Decide what to do on failure, usually fail closed

```tcl
when HTTP_REQUEST {
    if { [catch { set id [getfield [HTTP::path] "/" 3] } err] } {
        log local0. "parse error: $err"
        reject
        return
    }
}
```

---

## Testing in Stages

- Stage one: log every value you intend to branch on
- Stage two: add the decision but only log what it would do
- Stage three: enable the action
- Keep a `debug` switch so logging can be turned off in place

```tcl
when RULE_INIT { set static::debug 1 }
when HTTP_REQUEST {
    if { $static::debug } {
        log local0. "[IP::client_addr] [HTTP::method] [HTTP::uri]"
    }
}
```

---

## Deploy to a Test Virtual Server First

- Clone the production virtual server with a test address
- Attach the new iRule only there
- Drive traffic with `curl` from a known client address
- Promote to production once the log shows the expected decisions
- Keep the old iRule attached until the new one is proven

---

## Where Each Tool Sees Traffic

![tool_vantage_points](svg/courses/networking/f5-bigip-advanced-irules/06_developing_and_troubleshooting_irules/tool_vantage_points.svg)

---

## Using Fiddler

- Intercepting proxy on the workstation, sees every browser request
- Inspect request and response headers side by side
- Compose a request by hand and replay it
- Breakpoints pause a request so you can edit it before it leaves
- Enable `HTTPS` decryption to see inside `TLS` sessions

---

## Fiddler Workflow for an iRule

1. Load the page through the browser once
1. Select the request and check the headers the iRule reads
1. Drag it into the composer, change a header or the `URI`
1. Execute and compare the response headers with the expected ones
1. Set a breakpoint to test the rule against a malformed request

---

## Testing with curl

- `-v` shows request and response headers
- `-H` adds a header, `-X` sets the method, `-d` sends a body
- `--resolve` targets a virtual server without changing `DNS`
- `-k` skips certificate checks in the lab, `-b` sends a cookie

```bash
curl -v -H "X-Debug: 1" -X POST -d 'a=1' \
    --resolve www.example.com:443:10.1.10.50 \
    -k -b "sid=abc123" https://www.example.com/api/v2/users
curl -v --http1.0 http://10.1.10.50/
```

---

## Capturing with tcpdump

- Runs on the `BIG-IP` itself, sees both sides of the proxy
- Interface `0.0` captures every `VLAN`
- The `:nnn` suffix adds `TMM` and flow metadata to each packet
- `-s0` keeps whole packets, `-w` writes a file for `Wireshark`

```bash
tcpdump -nni 0.0:nnn -s0 host 10.1.1.5 and port 80 \
    -w /var/tmp/cap.pcap
tcpdump -nni client_vlan host 10.1.1.5 and port 443
tcpdump -nni server_vlan port 80
```

---

## Client Side Versus Server Side Capture

- Capture on the client `VLAN` to see what the client really sent
- Capture on the server `VLAN` to see what the iRule changed
- Compare the two to confirm a header insert or a rewrite
- `ssldump` with the private key decodes the `TLS` side
- Open the `pcap` in `Wireshark`, filter on `http.request`

---

## Failure Modes and Fixes

![failure_modes](svg/courses/networking/f5-bigip-advanced-irules/06_developing_and_troubleshooting_irules/failure_modes.svg)

---

## More Failure Modes

- Reading a header that is absent returns an empty string, not an error
- A global variable demotes the virtual server from `CMP`
- An iRule on every request when only one path needs it wastes `TMM` time
- A missing `return` after `HTTP::respond` runs the rest of the event
- Two iRules both redirecting produce the double invocation error

```tcl
when HTTP_REQUEST {
    if { [HTTP::uri] equals "/health" } {
        HTTP::respond 200 content "ok"
        return
    }
    pool web_pool
}
```

---

## Key Takeaways

- `/var/log/ltm` names the rule, the event and the line
- `catch` turns an abort into a decision
- Log first, act later, and test on a separate virtual server
- `Fiddler` and `curl` shape the input, `tcpdump` shows both sides
- Most failures are quoting, wrong event or double response
