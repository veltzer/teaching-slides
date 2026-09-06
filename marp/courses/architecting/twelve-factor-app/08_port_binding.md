---
tags:
  - concepts:architecture
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:developers

---

# Factor VII: Port Binding

---

## Port Binding At A Glance

![port_binding](svg/courses/architecting/twelve-factor-app/08_port_binding/port_binding.svg)

---

## The Rule

- Export services via port binding
- The app is self-contained — it embeds its own server
- No reliance on external application servers (Apache, IIS, etc.)

---

## Self-Contained Apps

- The app starts itself, opens a port, and accepts connections
- No installation into a web server's container
- A single command launches the app
- The app is a standalone executable, not a plugin

---

## Embedded Server vs External Server

- Old way: write a `.war` file and deploy into Tomcat
- New way: the app embeds Tomcat (or Jetty, or Netty) and runs as a process
- The boundary moves from "app runs inside server" to "app contains server"
- The deployment unit becomes the app, not the app + server pair

---

## Examples

- Spring Boot: embeds Tomcat by default
- Node.js: any HTTP server is embedded by definition
- Go: `net/http` is part of the binary
- Python: gunicorn/uvicorn are libraries the app launches itself
- Rust: actix, axum, etc. — embedded

---

## Why It Matters

- One artifact, one runtime — easier to ship and operate
- No version-skew between app and external server
- The app is portable — runs the same anywhere a port is available
- Containers became practical because of this shift

---

## Port Configuration

- The port is a config value (factor III)
- Read from `$PORT` environment variable
- The platform tells the app what port to bind to
- Heroku and similar platforms set this automatically

---

## A Minimal Pattern

```python
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

port = int(os.environ.get("PORT", "8080"))
server = HTTPServer(("0.0.0.0", port), MyHandler)
server.serve_forever()
```

- Bind to `0.0.0.0`, not `localhost`
- Read the port from env
- Start serving — that's it

---

## Anti-Patterns

- Apps that require a specific Apache config
- Apps that use a hardcoded port
- Apps that require URL rewriting at the proxy level to even start
- Apps that depend on the operating system's init system

---

## Beyond HTTP

- The factor applies to any protocol over a port
- gRPC services, message broker connections, custom TCP services
- The app exports a service via a network port; clients connect

---

## Routing in Front

- A reverse proxy (nginx, Cloud Load Balancer) usually sits in front
- It routes by hostname/path to the right app's port
- The app doesn't need to know about routing
- This is composition; not a violation of factor VII

---

## Summary

- The app embeds its server and binds to a port
- Port comes from env config
- One artifact, one process
- Containers naturally fit; PaaS platforms expect it
