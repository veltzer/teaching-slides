---
tags:
  - networking:http
  - networking:tcp-ip
  - networking:performance
  - architecture:caching
  - architecture:load-balancing
level: beginner
category: networking
audience:
  - audiences:network-engineers
  - audiences:sysadmins
  - audiences:devops

---

# Modifying Traffic Behavior with Profiles

---

## What This Chapter Covers

- What profiles are and how they attach to a virtual server
- Profile types, parent profiles and inheritance
- `TCP` Express and the `TCP` profiles
- `HTTP` and `HTTP/2` profile options
- `OneConnect` connection reuse
- `HTTP` compression offload
- Web acceleration and `HTTP` caching
- Stream profiles for payload rewriting
- The `F5` acceleration technologies as a whole

---

## What Is a Profile

- A profile is a named set of settings for one kind of traffic
- A virtual server references profiles; it does not hold the settings itself
- The same profile can be shared by many virtual servers
- Change the profile once, every virtual server that uses it changes
- Profiles tell `TMM` how to parse, optimize and modify the traffic
- No profile, no feature: no `HTTP` profile means no `HTTP` awareness

---

## Profiles Decide What the Virtual Server Understands

| Profiles on the virtual server | What `BIG-IP` can see and do |
| --- | --- |
| `fastL4` only | Packets and ports; forwards fast, no payload view |
| `tcp` | Full `TCP` proxy: two connections, independent tuning |
| `tcp` + `http` | Requests, headers, cookies, per-request decisions |
| `tcp` + `clientssl` + `http` | Same, after decrypting `HTTPS` |
| `tcp` + `http` + `oneconnect` | Per-request load balancing over reused server connections |

---

## Profile Types

| Category | Examples |
| --- | --- |
| Protocol | `tcp`, `udp`, `fastL4`, `sctp` |
| Services | `http`, `http2`, `ftp`, `dns`, `sip` |
| `SSL` | `clientssl`, `serverssl` |
| Persistence | `cookie`, `source_addr`, `ssl`, `universal` |
| Other | `oneconnect`, `stream`, `httpcompression`, `webacceleration` |
| Analytics and logging | `analytics`, `request-log` |

- GUI: Local Traffic > Profiles, one tab per category

---

## System Default Profiles

- `BIG-IP` ships a parent profile for every type: `tcp`, `http`, `clientssl`...
- Plus pre-tuned children: `tcp-wan-optimized`, `optimized-caching`...
- Default profiles are the roots of the inheritance tree
- Never edit a system default profile in production
    - It changes every virtual server that uses it or inherits from it
    - It makes the device behave differently from documentation and support
- Create a custom profile instead

---

## Parent Profiles and Inheritance

![profile_inheritance](svg/courses/networking/f5-bigip-fundamentals/04_modifying_traffic_behavior_with_profiles/profile_inheritance.svg)

---

## How Inheritance Works

- A custom profile names a parent (`defaults-from` in `tmsh`)
- Every setting is either inherited or overridden
- GUI: tick the "Custom" box next to a setting to override it
- Inherited settings follow the parent when the parent changes
- Overridden settings stay fixed whatever the parent does
- Chains are allowed: a child can be the parent of another custom profile

```bash
tmsh create ltm profile tcp tcp_mobile_custom \
    defaults-from tcp-mobile-optimized idle-timeout 600
tmsh list ltm profile tcp tcp_mobile_custom
```

---

## Seeing Inherited Values

- `tmsh list` shows only the overridden settings
- Add `all-properties` to see the effective value of every setting

```bash
tmsh list ltm profile tcp tcp_mobile_custom
tmsh list ltm profile tcp tcp_mobile_custom all-properties
tmsh list ltm profile tcp tcp_mobile_custom idle-timeout nagle
```

```config
ltm profile tcp tcp_mobile_custom {
    app-service none
    defaults-from tcp-mobile-optimized
    idle-timeout 600
}
```

---

## Profile Naming Conventions

- Prefix with the type: `tcp_`, `http_`, `oc_`, `comp_`, `wa_`
- Include the purpose: `http_xff`, `tcp_wan_portal`
- Keep custom profiles in `/Common` unless you use partitions
- Name says what changed, so the next engineer does not need `all-properties`
- A profile in use cannot be deleted; remove it from virtual servers first

---

## Client Side and Server Side Profiles

![profile_placement](svg/courses/networking/f5-bigip-fundamentals/04_modifying_traffic_behavior_with_profiles/profile_placement.svg)

---

## Profile Context

| Context | Applies to | Typical profiles |
| --- | --- | --- |
| `clientside` | Connection from client to `BIG-IP` | `tcp-wan-optimized`, `clientssl`, `http2` |
| `serverside` | Connection from `BIG-IP` to pool member | `tcp-lan-optimized`, `serverssl` |
| `all` | Both sides | `tcp`, `http`, `oneconnect` |

- A `TCP` profile can be set separately per side
- `SSL` profiles are inherently one sided
- GUI: Protocol (Client) and Protocol (Server) on the virtual server

---

## Assigning Profiles to a Virtual Server

- GUI: Local Traffic > Virtual Servers > `vs_http` > Configuration (Advanced)
- `tmsh`: `profiles add`, `profiles delete`, `profiles replace-all-with`

```bash
tmsh modify ltm virtual vs_http profiles add { \
    tcp-wan-optimized { context clientside } \
    tcp-lan-optimized { context serverside } }
tmsh modify ltm virtual vs_http profiles add { http_xff }
tmsh list ltm virtual vs_http profiles
```

- `replace-all-with` removes every profile not listed: use with care

---

## Profile Dependencies

| Profile | Requires on the virtual server |
| --- | --- |
| `http` | `tcp` (or `fastL4` for `fasthttp`) |
| `http2` | `http` and, for browsers, `clientssl` |
| `clientssl` / `serverssl` | `tcp` |
| `oneconnect` | `http` for per-request reuse |
| `httpcompression` | `http` |
| `webacceleration` | `http` |
| Cookie persistence | `http` |

- The configuration is rejected when a dependency is missing

---

## Changing a Profile in Use

- Edits to a profile apply to new connections immediately
- Existing connections keep the settings they started with
- Swapping a profile on a virtual server can reset its connections
- Test changes on a copy: clone the virtual server or the profile
- Save the configuration when the change is good: `tmsh save sys config`

---

## Lab: Build Custom Profiles

1. Create `tcp_wan_lab` from `tcp-wan-optimized`
1. Create `http_lab` from `http`
1. Assign `tcp_wan_lab` client side and `tcp-lan-optimized` server side to `vs_http`
1. Add `http_lab` to `vs_http`
1. Run `tmsh list ltm virtual vs_http profiles` and confirm the contexts
1. Browse to `http://10.1.10.100/` from the client and confirm it still works

---

## TCP Express

- `TCP` Express is the `F5` `TCP` stack inside `TMM`
- Not the `Linux` stack: tuned for proxying millions of connections
- Implements the modern `TCP` standards and extensions
    - Selective ACK, window scaling, timestamps, `ECN`
    - Several congestion control algorithms
- Because of the full proxy, each side gets its own stack instance
- The `TCP` profile is how you tune `TCP` Express per virtual server

---

## Why Tuning Each Side Matters

![tcp_wan_lan](svg/courses/networking/f5-bigip-fundamentals/04_modifying_traffic_behavior_with_profiles/tcp_wan_lan.svg)

---

## Built-in TCP Profiles

| Profile | Tuned for |
| --- | --- |
| `tcp` | General purpose parent, conservative defaults |
| `tcp-lan-optimized` | Low latency, high bandwidth data center links |
| `tcp-wan-optimized` | Higher latency internet links |
| `tcp-mobile-optimized` | Lossy, high latency cellular clients |
| `f5-tcp-progressive` | `F5` recommended general purpose starting point |
| `f5-tcp-lan`, `f5-tcp-wan`, `f5-tcp-mobile` | Newer tuned variants of the above |

---

## Key TCP Profile Settings

| Setting | Default in `tcp` | Effect |
| --- | --- | --- |
| Idle Timeout | 300 seconds | Closes quiet connections |
| Nagle's Algorithm | Disabled | Coalesces small segments |
| Delayed ACK | Enabled | Fewer ACK packets |
| Proxy Buffer High / Low | 49152 / 32768 | Buffer between client and server sides |
| Send Buffer / Receive Window | 65535 bytes | Data in flight per connection |
| Selective ACK | Enabled | Faster loss recovery |

- Check exact values on your version with `all-properties`

---

## Congestion Control

- Decides how fast to send and how to react to loss
- Available algorithms include `high-speed`, `cubic`, `woodside`, `bbr`, `new-reno`
- `cubic` and `high-speed`: good on high bandwidth paths
- `woodside`: built for lossy, mobile connections
- `bbr`: models bandwidth and round trip time instead of reacting to loss
- Change one side at a time and measure

```bash
tmsh modify ltm profile tcp tcp_wan_lab congestion-control bbr
```

---

## Idle Timeout

- Every connection has an idle timer in the connection table
- Default 300 seconds: idle connections are reset and removed
- Too short: long polls, database and `SSH` sessions break
- Too long: the connection table fills with dead entries
- Match it to the application, and to firewalls on the path

```bash
tmsh create ltm profile tcp tcp_long_idle \
    defaults-from tcp idle-timeout 3600
tmsh show sys connection cs-server-addr 10.1.10.100
```

---

## The `fastL4` Profile

- Not a full proxy: `BIG-IP` forwards packets of one `TCP` flow
- Used by Performance (Layer 4) virtual servers
- Can be offloaded to the hardware `ePVA` on appliances
- No `HTTP`, no `SSL` termination, no payload inspection
- Ideal for high volume traffic that only needs load balancing
- Trade-off: speed and scale versus visibility and control

---

## TCP Profile Versus `fastL4`

| Aspect | `tcp` (Standard virtual server) | `fastL4` (Performance L4) |
| --- | --- | --- |
| Connections | Two, one per side | One, passed through |
| Payload access | Yes | No |
| `HTTP`, `SSL`, compression | Yes | No |
| Hardware acceleration | Limited | `ePVA` on supported platforms |
| Per-side `TCP` tuning | Yes | No |
| Best for | Applications | Bulk `L4` traffic |

---

## Lab: Measure TCP Behavior

1. Download a 10 MB file through `vs_http` with `curl -o /dev/null -w '%{time_total}'`
1. Switch the client side profile to `tcp-mobile-optimized` and repeat
1. Compare the timings and the statistics

```bash
tmsh show ltm virtual vs_http
tmsh show ltm profile tcp tcp_wan_lab
tmsh reset-stats ltm virtual vs_http
```

---

## The HTTP Profile

- Makes the virtual server `HTTP` aware
- `TMM` parses each request and response, header by header
- Enables per-request features: cookie persistence, policies, iRules events
- Enables header insertion and removal, redirect rewriting, chunking control
- Parent profile: `http`; most applications need a custom child

---

## HTTP Proxy Modes

| Mode | Use |
| --- | --- |
| Reverse | Default: `BIG-IP` in front of your servers |
| Explicit | Forward proxy: clients are configured to use `BIG-IP` |
| Transparent | Inspects `HTTP` passing through without being the destination |

- This course uses Reverse mode throughout
- Explicit mode needs a `DNS` resolver object on `BIG-IP`

---

## Inserting X-Forwarded-For

![http_xff](svg/courses/networking/f5-bigip-fundamentals/04_modifying_traffic_behavior_with_profiles/http_xff.svg)

---

## X-Forwarded-For in Practice

- With `SNAT` the server sees the `BIG-IP` self `IP`, not the client
- `Insert X-Forwarded-For`: adds the original client address as a header
- The web server must log the header, not the socket address

```bash
tmsh create ltm profile http http_xff \
    defaults-from http insert-xforwarded-for enabled
```

```http
GET / HTTP/1.1
Host: app.example.com
X-Forwarded-For: 203.0.113.7
```

---

## Header Insert and Header Erase

- Header Insert: add one static header to every request
- Header Erase: remove one named header from every request
- Useful for simple tags the servers expect

```bash
tmsh modify ltm profile http http_lab \
    header-insert "X-Lab: bigip1" header-erase "X-Debug"
```

- For more than one header or conditional logic, use a local traffic policy (later chapter)

---

## Fallback Host and Error Codes

- Fallback Host: redirect target when no pool member is available
- Fallback on Error Codes: also redirect when the server answers with listed codes
- Gives users a friendly page instead of a reset connection

```bash
tmsh modify ltm profile http http_lab \
    fallback-host "https://sorry.example.com/" \
    fallback-status-codes add { 500 502 503 }
```

---

## Redirect Rewrite

- Servers behind `SSL` offload often redirect to `http://`
- Redirect Rewrite fixes the `Location` header on the way out

| Value | Rewrites |
| --- | --- |
| None | Nothing (default) |
| All | Every redirect, to the virtual server protocol |
| Matching | Only redirects to the requested host |
| Nodes | Only redirects to a pool member address |

---

## Chunking

- `HTTP/1.1` can send bodies in chunks without a `Content-Length`
- Any feature that changes the body length must re-chunk
- Request and response chunking settings control the behavior

| Setting | Behavior |
| --- | --- |
| `Preserve` / `Sustain` | Keep chunking as the sender used it |
| `Selective` | Re-chunk only when the body was modified |
| `Rechunk` | Always re-chunk |
| `Unchunk` | Remove chunking, buffer and send a length |

---

## HTTP Profile Enforcement Settings

| Setting | Default | Purpose |
| --- | --- | --- |
| Maximum Header Size | 32768 bytes | Rejects oversized headers |
| Maximum Header Count | 64 | Rejects header floods |
| Unknown Methods | Allow | Allow, reject or pass through |
| Pipelining | Allow | Multiple requests before responses |
| Server Agent Name | `BigIP` | Name used in `BIG-IP` generated responses |

- Tighten these on internet facing virtual servers

---

## HTTP Strict Transport Security

- `HSTS` tells browsers to use `HTTPS` only for this host
- The `HTTP` profile can insert the `Strict-Transport-Security` header
- Settings: mode, maximum age, include subdomains, preload
- Enable only once the whole site works on `HTTPS`

```bash
tmsh modify ltm profile http http_lab \
    hsts { mode enabled maximum-age 31536000 include-subdomains enabled }
```

---

## Lab: Custom HTTP Profile

1. Create `http_xff` with `insert-xforwarded-for enabled`
1. Replace `http_lab` on `vs_http` with `http_xff`
1. On a web server, tail the access log and confirm the client address
1. Add a Fallback Host and disable every pool member
1. Request the site and confirm the redirect
1. Re-enable the pool members

---

## The HTTP/2 Profile

- `HTTP/2` multiplexes many streams over one `TCP` connection
- Binary framing and compressed headers (`HPACK`)
- Browsers use `HTTP/2` only over `TLS`, negotiated with `ALPN`
- `BIG-IP` can speak `HTTP/2` to clients and `HTTP/1.1` to servers
- Servers need no change to benefit

---

## HTTP/2 Gateway Mode

![http2_gateway](svg/courses/networking/f5-bigip-fundamentals/04_modifying_traffic_behavior_with_profiles/http2_gateway.svg)

---

## HTTP/2 Profile Options

| Setting | Default | Meaning |
| --- | --- | --- |
| Concurrent Streams Per Connection | 10 | Parallel requests per client connection |
| Connection Idle Timeout | 300 seconds | Closes idle `HTTP/2` connections |
| Header Table Size | 4096 bytes | `HPACK` dynamic table |
| Frame Size | 2048 bytes | Largest data frame `BIG-IP` sends |
| Receive Window | 32 KB | Per-stream flow control |
| Activation Modes | `ALPN` | How `HTTP/2` is negotiated |

---

## Enabling HTTP/2

- Requires `http` and `clientssl` on the same virtual server
- The client `SSL` profile must offer `h2` through `ALPN` (automatic with an `http2` profile)

```bash
tmsh create ltm profile http2 h2_lab \
    defaults-from http2 concurrent-streams-per-connection 50
tmsh modify ltm virtual vs_https profiles add { h2_lab { context clientside } }
curl -k --http2 -sI https://10.1.10.101/ | head -1
```

```output
HTTP/2 200
```

---

## HTTP/2 to the Servers

- Newer versions can also speak `HTTP/2` on the server side
- Add the `http2` profile with `serverside` context and a server `SSL` profile
- Worth it only when the servers handle `HTTP/2` well
- Gateway mode remains the most common deployment

| Client side | Server side | Name |
| --- | --- | --- |
| `HTTP/2` | `HTTP/1.1` | Gateway mode |
| `HTTP/2` | `HTTP/2` | Full proxy `HTTP/2` |
| `HTTP/1.1` | `HTTP/1.1` | Plain `HTTP` profile |

---

## `OneConnect`

- Without it: one server connection per client connection
- With it: idle server connections are kept and reused for new requests
- Fewer `TCP` handshakes and fewer open sockets on the servers
- With an `HTTP` profile, every request is load balanced separately
- One of the cheapest and most effective optimizations on `BIG-IP`

---

## `OneConnect` Connection Reuse

![connection_reuse](svg/courses/networking/f5-bigip-fundamentals/04_modifying_traffic_behavior_with_profiles/connection_reuse.svg)

---

## `OneConnect` Settings

| Setting | Default | Meaning |
| --- | --- | --- |
| Source Mask | `0.0.0.0` | Which clients may share a server connection |
| Maximum Size | 10000 | Idle connections kept in the reuse pool |
| Maximum Age | 86400 seconds | Retire a server connection after this long |
| Maximum Reuse | 1000 | Retire after this many requests |
| Idle Timeout Override | Disabled | Separate idle timeout for pooled connections |
| Limit Type | None | How reuse interacts with connection limits |

---

## The Source Mask

| Mask | Who shares a server connection |
| --- | --- |
| `0.0.0.0` | Any client with any other client |
| `255.255.255.0` | Clients from the same `/24` |
| `255.255.255.255` | Only requests from the same client address |

- With `SNAT`, the mask is applied to the translated address
- Servers that tie state to the connection (for example `NTLM` authentication) need care

---

## `OneConnect` Without an HTTP Profile

- Without `HTTP` awareness, `BIG-IP` cannot see request boundaries
- Load balancing then happens per connection, not per request
- Persistence also binds per connection
- Rule of thumb: `oneconnect` goes together with `http`

```bash
tmsh create ltm profile one-connect oc_lab defaults-from oneconnect
tmsh modify ltm virtual vs_http profiles add { oc_lab }
tmsh show ltm profile one-connect oc_lab
```

---

## Lab: Watch `OneConnect` Work

1. Run 100 requests from the client with `ab -n 100 -c 5 http://10.1.10.100/`
1. Run `tmsh show ltm pool web_pool members` and note the connection totals
1. Add `oc_lab` to `vs_http` and reset the statistics
1. Repeat the test
1. Compare: requests per member stay similar, server side connections drop sharply

---

## HTTP Compression Offload

- Compressing text saves bandwidth and speeds up slow clients
- Doing it on every server wastes server CPU
- `BIG-IP` compresses responses on behalf of all pool members
- Servers send plain responses, `BIG-IP` sends `gzip` to the client
- On some platforms compression runs in hardware

---

## Compression Decision Flow

![compression_flow](svg/courses/networking/f5-bigip-fundamentals/04_modifying_traffic_behavior_with_profiles/compression_flow.svg)

---

## Compression Profile Settings

| Setting | Default | Meaning |
| --- | --- | --- |
| Minimum Content Length | 1024 bytes | Small responses are not worth it |
| Content Type Include | `text/`, `application/xml` and similar | What to compress |
| Content Type Exclude | (empty) | Never compress these |
| Keep Accept Encoding | Disabled | Strip the header so servers send plain |
| Vary Header | Enabled | Insert `Vary: Accept-Encoding` |
| `gzip` Compression Level | 1 | Higher is smaller and slower |

---

## What Not to Compress

- Images, video, audio: already compressed (`jpeg`, `png`, `mp4`)
- Archives: `zip`, `gz`
- Responses that are already encoded by the server
- Very small responses below the minimum length
- `HTTP/1.0` clients by default
- Compressing compressed data costs CPU and gains nothing

---

## Configuring Compression

```bash
tmsh create ltm profile http-compression comp_lab \
    defaults-from httpcompression \
    content-type-include add { application/json } \
    min-size 2048
tmsh modify ltm virtual vs_http profiles add { comp_lab }
curl -s -H 'Accept-Encoding: gzip' -o /dev/null \
    -w '%{size_download}\n' http://10.1.10.100/app.js
tmsh show ltm profile http-compression comp_lab
```

- Compare the downloaded size with and without the header

---

## Compression and CPU

- Compression is CPU intensive on `BIG-IP` too
- CPU Saver: reduces compression when `TMM` CPU is high
- Keep the compression level low; level 1 gets most of the gain
- `wan-optimized-compression` parent profile: tuned for slow links
- Watch `tmsh show sys cpu` before and after enabling it

---

## Web Acceleration and Caching

- The web acceleration profile adds a RAM cache to the virtual server
- Static objects are served from `BIG-IP` memory
- Pool members see only cache misses and expired objects
- Cuts server load and response time for repeated content
- Requires an `HTTP` profile

---

## Cache Hit and Miss

![cache_hit_miss](svg/courses/networking/f5-bigip-fundamentals/04_modifying_traffic_behavior_with_profiles/cache_hit_miss.svg)

---

## What Gets Cached

- Only `GET` requests
- Only cacheable status codes: 200, 203, 300, 301, 410
- Responses that `Cache-Control` and `Expires` headers allow
- Objects between the minimum and maximum object size
- `URI` lists override: include, exclude and pin
- Responses with `Set-Cookie` or authentication are not cached by default

---

## Web Acceleration Settings

| Setting | Default | Meaning |
| --- | --- | --- |
| Cache Size | 100 MB | Memory per profile, per `TMM` |
| Maximum Entries | 10000 | Objects in the cache |
| Maximum Age | 3600 seconds | Upper bound on object lifetime |
| Minimum Object Size | 500 bytes | Below this, not cached |
| Maximum Object Size | 50000 bytes | Above this, not cached |
| Insert Age Header | Enabled | Tells clients how old the object is |

---

## Configuring Caching

```bash
tmsh create ltm profile web-acceleration wa_lab \
    defaults-from optimized-caching \
    cache-size 200 cache-max-age 600 \
    cache-uri-exclude add { "/api/*" }
tmsh modify ltm virtual vs_http profiles add { wa_lab }
tmsh show ltm profile ramcache wa_lab
tmsh delete ltm profile ramcache wa_lab
```

- `show ... ramcache` lists cached objects
- `delete ... ramcache` empties the cache, the profile stays

---

## Caching Pitfalls

- Caching personal pages leaks one user's data to another
- Use exclude lists for `/api/`, `/account/`, anything per user
- Content changes stay invisible until objects expire
- Plan a cache flush step into every deployment
- Test with `curl -I` and watch the `Age` header grow

---

## Stream Profiles

- Search and replace on the payload, in both directions
- Simple form: one source string, one target string
- Expression form: `@search@replace@` pairs, several at once
- Typical uses
    - Fix hard coded `http://` links behind `SSL` offload
    - Rename internal host names in pages
    - Mask data such as account numbers

---

## Stream Rewrite

![stream_rewrite](svg/courses/networking/f5-bigip-fundamentals/04_modifying_traffic_behavior_with_profiles/stream_rewrite.svg)

---

## Configuring a Stream Profile

```bash
tmsh create ltm profile stream st_links \
    source "http://app.lab" target "https://app.example.com"
tmsh create ltm profile stream st_multi \
    target "@http://app.lab@https://app.example.com@@internal-db@db@"
tmsh modify ltm virtual vs_https profiles add { st_links }
```

- With an `HTTP` profile, `BIG-IP` fixes `Content-Length` and chunking
- The server must not compress: strip `Accept-Encoding` toward it

---

## Stream Profile Caveats

- Rewrites every matching byte, including in requests
- Cannot see inside compressed bodies
- Costs CPU on every response
- Broad matches cause surprising results: keep strings specific
- For conditional rewriting (only some content types), use an iRule with `STREAM::` commands

---

## F5 Acceleration Technologies

| Technology | What it accelerates |
| --- | --- |
| `TCP` Express | Transport on both sides of the proxy |
| `OneConnect` | Server connection setup |
| `HTTP` compression | Bandwidth to clients |
| Web acceleration (RAM cache) | Repeated static content |
| `SSL` offload with hardware crypto | Encryption cost on the servers |
| `fastL4` and `ePVA` | Raw packet forwarding |
| `HTTP/2` gateway | Browser page loads over high latency links |

---

## Combining Profiles

- A typical web virtual server stacks several profiles

```config
ltm virtual vs_https {
    destination 10.1.10.101:https
    pool web_pool
    profiles {
        f5-tcp-progressive { context clientside }
        tcp-lan-optimized { context serverside }
        clientssl_lab { context clientside }
        http_xff { }
        h2_lab { context clientside }
        oc_lab { }
        comp_lab { }
        wa_lab { }
    }
    source-address-translation { type automap }
}
```

---

## Order of Processing

- Profiles act on the traffic in a fixed order inside `TMM`
- Request direction: `TCP` > client `SSL` > `HTTP/2` > `HTTP` > cache lookup > load balancing
- Response direction: server `SSL` > `HTTP` > stream > compression > client `SSL` > `TCP`
- A cache hit never reaches load balancing or the pool
- Compression happens after any rewriting of the body

---

## Troubleshooting Profiles

| Symptom | Check |
| --- | --- |
| Virtual server rejects a profile | Missing dependency (`http`, `tcp`, `clientssl`) |
| Client addresses missing in server logs | `insert-xforwarded-for` and server log format |
| Connections drop after a few minutes | `TCP` idle timeout |
| Stale content | Web acceleration cache, `Age` header |
| Rewrite does not happen | Compression from the server, wrong source string |
| Uneven load with `OneConnect` | Source mask and persistence |

---

## Statistics Per Profile

```bash
tmsh show ltm profile tcp tcp_wan_lab
tmsh show ltm profile http http_xff
tmsh show ltm profile http2 h2_lab
tmsh show ltm profile one-connect oc_lab
tmsh show ltm profile http-compression comp_lab
tmsh show ltm profile web-acceleration wa_lab
```

- GUI: Statistics > Module Statistics > Local Traffic > Profiles Summary
- Reset counters before a test: `tmsh reset-stats ltm profile <type> <name>`

---

## Lab: Full Profile Stack

1. Build `vs_https` with client `SSL`, `http_xff`, `h2_lab`, `oc_lab`, `comp_lab`, `wa_lab`
1. Request the site with `curl --http2 -H 'Accept-Encoding: gzip' -k -v`
    - Confirm `HTTP/2`, `Content-Encoding: gzip` and an `Age` header on repeats
1. Check the server log for `X-Forwarded-For`
1. Review every profile's statistics
1. Save the configuration

---

## Key Takeaways

- Profiles carry the settings; virtual servers only reference them
- Always create custom children, never edit the system parents
- Tune the client side and server side `TCP` independently
- The `HTTP` profile unlocks every request level feature
- `OneConnect`, compression and caching move work off the servers
- Stream profiles rewrite payload, but cost CPU and need uncompressed data
- Verify every change with `tmsh show` statistics
