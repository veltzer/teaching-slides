---
tags:
  - networking:http
  - networking:tcp-ip
  - networking:troubleshooting
  - architecture:load-balancing
level: beginner
category: networking
audience:
  - audiences:network-engineers
  - audiences:sysadmins
  - audiences:devops

---

# Monitoring Application Health

---

## What This Chapter Covers

- Why `BIG-IP` monitors nodes and pool members at all
- Monitor types: address, service, content and performance checks
- Built in monitors and custom monitors derived from them
- Send and receive strings for `HTTP` monitors
- Interval and timeout settings
- Assigning monitors to nodes, pools and pool members
- Combining monitors with an availability requirement
- Reading monitor status and troubleshooting a member marked down

---

## Why Monitor

- A load balancer that sends traffic to a dead server is worse than no load balancer
- Without a monitor, `BIG-IP` assumes every member is available
- A monitor probes each node or member on a schedule
- Failed probes mark the object down; load balancing skips it
- Successful probes mark it up again, without operator action
- Monitoring turns a pool of servers into a self healing service

---

## What Up and Down Mean

- **Up**: the object passed its monitors and receives new connections
- **Down**: the object failed its monitors; no new connections are sent to it
- Existing connections to a member that goes down are not cut by default
- `Action On Service Down` on the pool decides what happens to them
- A pool with every member down makes its virtual server unavailable
- Clients then get a reset, or whatever fallback you configured

---

## Action On Service Down

| Setting | Effect on existing connections |
| --- | --- |
| `None` (default) | Left alone; they finish or time out |
| `Reject` | Reset immediately, client must reconnect |
| `Drop` | Silently removed from the connection table |
| `Reselect` | Moved to another member (for stateless traffic) |

- `Reject` is a good choice for most `HTTP` applications
- `Reselect` only makes sense when the protocol tolerates a new server mid flow

---

## Monitor Types

![monitor_layers](svg/courses/networking/f5-bigip-fundamentals/03_monitoring_application_health/monitor_layers.svg)

---

## The Four Kinds of Check

| Check | Question it answers | Example monitors | Cost |
| --- | --- | --- | --- |
| Address | Does the `IP` respond? | `icmp`, `gateway_icmp` | Very low |
| Service | Is the port open? | `tcp`, `udp`, `tcp_half_open` | Low |
| Content | Does the application answer correctly? | `http`, `https`, `ftp`, `smtp` | Medium |
| Performance | How loaded is the server? | `snmp_dca`, `wmi` | Medium |

---

## Why Deeper Checks Win

- Each layer proves more than the one below it
- A server can answer `ping` while its web server is stopped
- Prefer content checks for anything that serves users

---

## Where Monitors Run

- Monitors are executed by `bigd` on the Linux host side, not by `TMM`
- Probes are sourced from the self `IP` on the server `VLAN`
- Servers must accept probes from the self `IP` addresses (watch firewalls)
- In an `HA` pair, each device monitors independently
- Status changes are written to `/var/log/ltm`

---

## Built In Address and Service Monitors

| Monitor | Probe | Default interval | Default timeout |
| --- | --- | --- | --- |
| `gateway_icmp` | `ICMP` echo to the address | 5s | 16s |
| `icmp` | `ICMP` echo | 5s | 16s |
| `tcp` | Open `TCP` connection, optional send/receive | 5s | 16s |
| `tcp_half_open` | `SYN`, expect `SYN-ACK`, then reset | 5s | 16s |

---

## Built In Content Monitors

| Monitor | Probe | Default interval | Default timeout |
| --- | --- | --- | --- |
| `http` | `GET /`, any reply counts | 5s | 16s |
| `https` | `GET /` over `TLS`, any reply counts | 5s | 16s |

---

## Custom Monitors

- Built in monitors cannot be modified
- To change anything, create a custom monitor that uses one as its parent
- Local Traffic > Monitors > Create
- Choose a type (`HTTP`, `HTTPS`, `TCP`...) and a parent monitor
- Settings not changed are inherited from the parent
- Name monitors after the application, not the protocol: `mon_shop_http`

```bash
tmsh create ltm monitor http mon_shop_http \
    defaults-from http \
    send "GET /health HTTP/1.1\r\nHost: shop.example.com\r\nConnection: close\r\n\r\n" \
    recv "200 OK" \
    interval 5 timeout 16
```

---

## Send Strings

- The send string is the request the monitor writes to the server
- Default `http` send is `GET /\r\n`, an `HTTP/0.9` style request
- Many servers and virtual hosts reject that: use a full `HTTP/1.1` request
- `HTTP/1.1` requires a `Host` header
- Add `Connection: close` so the server ends the probe connection cleanly
- Escape line breaks as `\r\n` and end the request with an empty line

```http
GET /health HTTP/1.1\r\nHost: shop.example.com\r\nConnection: close\r\n\r\n
```

---

## Receive Strings

- The receive string is matched against the response (headers and body)
- It is a regular expression, searched anywhere in the first part of the reply
- Without a receive string, any response marks the member up, even a `500`
- Match something only a healthy application returns

| Receive string | Matches | Risk |
| --- | --- | --- |
| (empty) | Any reply | Error pages count as healthy |
| `200 OK` | Status line | A static page can still say `200` |
| `"status":"up"` | Body of a health endpoint | Needs an application endpoint |

---

## Receive Disable String

- `recv-disable` matches a second string that means "up, but do not send new work"
- The member goes to **disabled**: persistent and active connections continue
- Lets the application drain itself before maintenance
- Example: the health page returns `MAINTENANCE` during a deploy

```bash
tmsh modify ltm monitor http mon_shop_http \
    recv "status: up" recv-disable "status: maintenance"
```

---

## Interval and Timeout

![interval_timeout](svg/courses/networking/f5-bigip-fundamentals/03_monitoring_application_health/interval_timeout.svg)

---

## Choosing Interval and Timeout

- **Interval**: how often a probe is sent (default 5 seconds)
- **Timeout**: how long without a good reply before the member is marked down (default 16 seconds)
- Rule of thumb: timeout = 3 × interval + 1
- Three missed probes in a row before marking down; one lost packet is not an outage
- Shorter values detect failures faster but load the servers and `bigd` more
- `Up Interval` and `Time Until Up` slow down how quickly a recovering member returns

---

## Probe Timing Settings

| Setting | Default | Effect |
| --- | --- | --- |
| `interval` | 5 | Seconds between probes while the member is down or up |
| `timeout` | 16 | Seconds without a good reply before marking down |
| `up-interval` | 0 (disabled) | Separate, slower probe rate while the member is up |

---

## Recovery Settings

| Setting | Default | Effect |
| --- | --- | --- |
| `time-until-up` | 0 | Seconds of passing probes before marking up |
| `manual-resume` | disabled | Stay down until an operator enables the member |

- `manual-resume` is useful for applications that need a warm up check by a person

---

## Monitor Assignment

![monitor_assignment](svg/courses/networking/f5-bigip-fundamentals/03_monitoring_application_health/monitor_assignment.svg)

---

## Assigning Monitors

- **Node**: usually an address check (`icmp`); default node monitor is set under Nodes > Default Monitor
- **Pool**: the default monitor for every member of the pool
- **Pool member**: overrides the pool monitor for that single member
- A member is available only if its node and its own monitors all pass
- A node that fails its monitor takes down every member that uses it, in every pool

```bash
tmsh modify ltm default-node-monitor rule icmp
tmsh modify ltm pool shop_pool monitor mon_shop_http
tmsh modify ltm pool shop_pool members modify { 10.1.20.12:443 { monitor https } }
```

---

## Combining Monitors

- A pool or member can have several monitors at once
- Typical combination: `tcp` on the port plus `http` on the health page
- Each monitor reports independently; the availability requirement combines them
- More monitors mean more probe traffic: combine only what adds information

```bash
tmsh modify ltm pool shop_pool monitor "mon_shop_http and tcp"
tmsh modify ltm pool shop_pool monitor "min 2 of { icmp mon_shop_http mon_shop_login }"
```

---

## Availability Requirement

![availability_requirement](svg/courses/networking/f5-bigip-fundamentals/03_monitoring_application_health/availability_requirement.svg)

---

## All or At Least N

- **All** (default): every monitor must pass; `tmsh` uses `and`
- **At Least N**: a minimum number must pass; `tmsh` uses `min N of { ... }`
- Use **All** when each monitor checks something the application cannot live without
- Use **At Least N** when monitors are alternatives and some flakiness is expected
- The same idea exists on pools: `min-active-members` for priority groups

---

## Monitor Status Icons

| Icon | Status | Meaning |
| --- | --- | --- |
| Green circle | Available | Monitors pass, receiving traffic |
| Red diamond | Offline | Monitors fail, no new traffic |
| Blue square | Unknown | No monitor assigned, assumed up |
| Yellow triangle | Unavailable | Connection limit reached |
| Black shape | Disabled | Administratively disabled by an operator |
| Gray shape | Disabled by parent | The parent object is disabled |

- Unknown is not healthy: it only means nobody is checking

---

## Enabled, Disabled and Forced Offline

| State | New connections | Persistent connections | Active connections |
| --- | --- | --- | --- |
| Enabled | Yes | Yes | Yes |
| Disabled | No | Yes | Yes |
| Forced Offline | No | No | Yes |

- These are operator decisions, independent of monitor results
- Disable a member to drain it gracefully before maintenance
- Force offline when even returning users must leave the server

---

## Reading Monitor Status

```bash
tmsh show ltm pool shop_pool members field-fmt
tmsh show ltm pool shop_pool detail
tmsh show ltm node 10.1.20.12
```

```output
ltm pool shop_pool:Members:10.1.20.12:80 {
    status.availability-state offline
    status.enabled-state enabled
    status.status-reason Pool member has been marked down by a monitor
    monitor-status down
}
```

---

## Monitor Logs

- Every status change of a member is logged to `/var/log/ltm`
- The log names the monitor, the member and the reason

```bash
grep "Pool /Common/shop_pool member" /var/log/ltm
```

```output
Pool /Common/shop_pool member /Common/10.1.20.12:80 monitor status down.
  [ /Common/mon_shop_http: down; last error: Response Code: 503 (Service Unavailable) ]
  [ was up for 2hrs:14mins:3sec ]
```

---

## Troubleshooting a Member Marked Down

1. Read the status reason and the log entry: which monitor failed and why
1. Check the node monitor first: is the address itself down?
1. Reproduce the probe from the `BIG-IP` bash prompt, from the self `IP`
1. Compare the actual response with the receive string
1. Check server side firewalls and access lists for the self `IP`
1. Check routing: can the server reply back to the self `IP`?
1. Fix the server or the monitor, then watch the member come back up

---

## Reproducing an HTTP Probe

```bash
curl -v --interface 10.1.20.245 \
    -H "Host: shop.example.com" -H "Connection: close" \
    http://10.1.20.12/health
```

- `--interface` sources the request from the self `IP`, like `bigd` does
- Look at the status line and body: does the receive string appear?
- `tcpdump -ni internal host 10.1.20.12 and port 80` shows the real probes
- Common causes: missing `Host` header, wrong path, receive string typo, redirect to `HTTPS`

---

## Common Monitor Request Mistakes

| Mistake | Symptom | Fix |
| --- | --- | --- |
| No receive string | Error pages keep the member up | Match a healthy response |
| `HTTP/1.1` without `Host` | Server answers `400`, member down | Add the `Host` header |
| Missing `\r\n\r\n` | Probe hangs until timeout | End the request with an empty line |

---

## Common Monitor Design Mistakes

| Mistake | Symptom | Fix |
| --- | --- | --- |
| Timeout shorter than interval | Flapping members | Use timeout = 3 × interval + 1 |
| Only `icmp` on a web pool | Dead web server still gets traffic | Add a content monitor |

---

## Lab: Monitoring the Shop Pool

1. Create `mon_shop_http` with a full `HTTP/1.1` send string and a receive string
1. Assign it to `shop_pool` and confirm all three members are green
1. Set the default node monitor to `icmp`
1. Stop the web server on `10.1.20.12` and time how long until it is marked down
1. Read the log entry and the status reason
1. Change the health page so the receive string no longer matches; observe the result
1. Try an availability requirement of at least 2 of 3 monitors

---

## Key Takeaways

- Monitors are what make a pool self healing
- Prefer content checks with an explicit receive string
- Use full `HTTP/1.1` send strings with a `Host` header
- Keep timeout at three intervals plus one
- A node monitor failure takes down every member on that node
- Troubleshoot by reproducing the probe from the self `IP`
