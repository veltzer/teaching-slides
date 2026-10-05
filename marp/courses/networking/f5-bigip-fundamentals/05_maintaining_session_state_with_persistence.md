---
tags:
  - networking:http
  - architecture:load-balancing
  - networking:troubleshooting
  - security:tls
level: beginner
category: networking
audience:
  - audiences:network-engineers
  - audiences:sysadmins
  - audiences:devops

---

# Maintaining Session State with Persistence

---

## What This Chapter Covers

- Why stateful applications need a client to stay on one server
- Source address affinity persistence and its limits
- Cookie persistence: insert, rewrite, passive and hash modes
- Other methods: destination address, `SSL` session, universal
- How persistence interacts with `OneConnect`
- Fallback persistence and the match across options
- Viewing and clearing persistence records

---

## Load Balancing Versus Session State

- Load balancing picks a server for every new connection
- Many applications keep state in the memory of one server
    - Login sessions, shopping carts, multi step forms
- The next connection may land on a different server
- That server has never seen the client: the session is lost
- Persistence overrides load balancing to keep the client on the same member

---

## Session State Lost Without Persistence

![session_lost](svg/courses/networking/f5-bigip-fundamentals/05_maintaining_session_state_with_persistence/session_lost.svg)

---

## Do You Really Need Persistence?

- Stateless applications do not need it: let load balancing work
- Shared session stores (`Redis`, database) remove the need
- Persistence skews the load: popular clients stay where they are
- A persisted member that fails loses its sessions anyway
- Ask the application team before adding it
- When the application needs it, nothing else will do

---

## How Persistence Works on BIG-IP

1. The first request is load balanced as usual
1. `BIG-IP` creates a persistence record: key to pool member
1. Later requests are matched by key against the records
1. A match sends the request to the recorded member, skipping load balancing
1. Records expire after the profile timeout without traffic

- The key depends on the method: source address, cookie, `SSL` session ID, any value
- Persistence is a profile, assigned on the virtual server's Resources tab

---

## Persistence Methods Keyed on Addresses

| Method | Key | Record stored on | Typical use |
| --- | --- | --- | --- |
| Source address affinity | Client `IP` (masked) | `BIG-IP` | Non `HTTP` `TCP`/`UDP` services |
| Destination address | Destination `IP` | `BIG-IP` | Cache and proxy farms |

---

## Persistence Methods Keyed on Session Data

| Method | Key | Record stored on | Typical use |
| --- | --- | --- | --- |
| Cookie | `HTTP` cookie | Client browser (insert) | Web applications |
| `SSL` session | `SSL` session ID | `BIG-IP` | Encrypted pass through |
| Universal | Any value an iRule extracts | `BIG-IP` | `JSESSIONID`, custom tokens |
| Hash | Hash of a value | Nothing (computed) | Stateless consistent mapping |

---

## Built In Persistence Profiles

```bash
tmsh list ltm persistence one-line | awk '{print $3, $4}'
```

```output
cookie cookie
dest-addr dest_addr
hash hash
source-addr source_addr
ssl ssl
universal universal
```

- Every method has a parent profile named after it
- Create a child profile to change settings; never edit the parent

---

## Source Address Affinity

- Key: the client source `IP` address, optionally masked
- Works for any protocol: no `HTTP` profile required
- Default timeout: 180 seconds of inactivity
- Mask `255.255.255.0` puts a whole `/24` on one member

```bash
tmsh create ltm persistence source-addr src_persist_24 \
    defaults-from source_addr mask 255.255.255.0 timeout 600
tmsh modify ltm virtual vs_app persist replace-all-with { src_persist_24 }
```

---

## The Mega Proxy Problem

![mega_proxy](svg/courses/networking/f5-bigip-fundamentals/05_maintaining_session_state_with_persistence/mega_proxy.svg)

---

## Limits of Source Address Affinity

- Many users behind one `NAT` or proxy share one source address
- All of them persist to the same member: uneven load
- Mobile clients change `IP` address mid session and lose persistence
- Records live in `BIG-IP` memory: millions of clients cost memory
- Prefer cookie persistence for `HTTP` traffic
- Keep source address affinity as the fallback method

---

## Cookie Persistence

- Uses an `HTTP` cookie as the persistence key
- Requires an `HTTP` profile on the virtual server
- Four modes: insert, rewrite, passive and hash
- Insert is the default and by far the most common
- Default cookie name: `BIGipServer` followed by the pool name
- Works through `NAT`s and proxies, since each browser has its own cookie

---

## Cookie Modes

| Mode | Who creates the cookie | `BIG-IP` stores records | Notes |
| --- | --- | --- | --- |
| Insert | `BIG-IP` adds `Set-Cookie` | No | Default, zero server changes |
| Rewrite | Server sends a blank cookie, `BIG-IP` fills it | No | Legacy, rarely used |
| Passive | Server sets a cookie with member encoded | No | Server must know the encoding |
| Hash | Server sets its own session cookie | No | `BIG-IP` hashes the value to a member |

---

## Cookie Insert Flow

![cookie_insert_flow](svg/courses/networking/f5-bigip-fundamentals/05_maintaining_session_state_with_persistence/cookie_insert_flow.svg)

---

## What Is Inside the Cookie

```http
HTTP/1.1 200 OK
Set-Cookie: BIGipServerweb_pool=185860362.20480.0000; path=/; Httponly
```

- The value encodes the pool member address and port
- `185860362` is `10.1.20.11` as a little endian integer
- `20480` is port `80` with its bytes swapped
- Anyone can decode it: it leaks internal addressing
- Enable cookie encryption in the profile to hide it

---

## Configuring Cookie Insert

```bash
tmsh create ltm persistence cookie cookie_web \
    defaults-from cookie method insert \
    cookie-name APPSRV expiration 0 \
    cookie-encryption required cookie-encryption-passphrase S3cret
tmsh modify ltm virtual vs_web persist replace-all-with { cookie_web }
```

- `expiration 0` makes a session cookie, deleted when the browser closes
- A custom cookie name avoids advertising `BIG-IP`
- Encryption required: unencrypted cookies from clients are ignored

---

## Cookie Persistence Options

| Option | Default | Effect |
| --- | --- | --- |
| `cookie-name` | `BIGipServer<pool>` | Name of the inserted cookie |
| `expiration` | `0` (session) | Lifetime of the cookie in the browser |
| `always-send` | `disabled` | Send `Set-Cookie` on every response |
| `httponly` | `enabled` | Hide the cookie from scripts |
| `secure` | `enabled` | Send only over `HTTPS` |
| `cookie-encryption` | `disabled` | `disabled`, `preferred` or `required` |

---

## Other Persistence Methods

- Destination address affinity
    - Key is the destination `IP`: keeps one site on one cache server
    - Used with transparent cache and proxy pools
- `SSL` session persistence
    - Key is the `SSL` session ID, for traffic `BIG-IP` does not decrypt
    - Fragile: clients renegotiate and `TLS 1.3` drops session ID resumption
- Universal persistence
    - An iRule supplies the key, for example `JSESSIONID`
- Hash persistence: maps a value to a member with no stored record

---

## Universal Persistence Example

```tcl
when HTTP_REQUEST {
    set sid [HTTP::cookie value "JSESSIONID"]
    if { $sid ne "" } { persist uie $sid 1800 }
}
when HTTP_RESPONSE {
    set sid [HTTP::cookie value "JSESSIONID"]
    if { $sid ne "" } { persist add uie $sid 1800 }
}
```

- The application's own session ID becomes the persistence key
- Attach the iRule to a universal profile on the virtual server
- iRules are covered in depth in the Advanced iRules course

---

## Persistence and `OneConnect`

![oneconnect_persistence](svg/courses/networking/f5-bigip-fundamentals/05_maintaining_session_state_with_persistence/oneconnect_persistence.svg)

---

## Why `OneConnect` Matters for Persistence

- Without `OneConnect`, the server side connection is fixed after the first request
- Later requests on the same client connection go to the same member
- A proxy that multiplexes many users on one connection breaks persistence
- With `OneConnect`, each request is detached and decided again
- Each request is matched against its own cookie
- Rule: cookie or universal persistence on `HTTP` should run with `OneConnect`

---

## Fallback Persistence

![fallback_persistence](svg/courses/networking/f5-bigip-fundamentals/05_maintaining_session_state_with_persistence/fallback_persistence.svg)

---

## Configuring Fallback Persistence

- Set on the virtual server, next to the default persistence profile
- Used when the default method finds no key in the request
- Typical pair: cookie insert as default, source address as fallback
- Covers clients that refuse cookies and non browser `API` clients

```bash
tmsh modify ltm virtual vs_web \
    persist replace-all-with { cookie_web { default yes } } \
    fallback-persistence src_persist_24
```

---

## Match Across Options

| Option | Records shared across | Use when |
| --- | --- | --- |
| `match-across-services` | Virtual servers on the same address, different ports | `HTTP` and `HTTPS` of one site share sessions |
| `match-across-virtuals` | All virtual servers on the system | Several sites use the same servers |
| `match-across-pools` | Pools, not just the virtual server's default pool | iRules or policies switch pools |

- Only for record based methods such as source address affinity
- The same member must exist in the pool the request ends up in

---

## Match Across Services Example

- `vs_web_http` on `10.1.10.100:80` and `vs_web_https` on `10.1.10.100:443`
- Client logs in over `HTTPS`, browses product pages over `HTTP`
- One persistence profile with `match-across-services enabled` on both
- The record created on port `443` is honored on port `80`

```bash
tmsh modify ltm persistence source-addr src_persist_24 \
    match-across-services enabled
```

---

## Viewing Persistence Records

- `GUI`: Statistics > Module Statistics > Local Traffic > Persistence Records
- The `GUI` page must be enabled once with a `db` key
- Cookie insert creates no records: the state lives in the browser

```bash
tmsh modify sys db ui.statistics.modulestatistics.localtraffic.persistencerecords \
    value true
tmsh show ltm persistence persist-records
```

```output
Sys::Persistent Connections
source-address  10.1.10.50  10.1.10.100:80  10.1.20.12:80  (tmm: 0)
```

---

## Clearing Persistence Records

```bash
tmsh delete ltm persistence persist-records
tmsh delete ltm persistence persist-records client-addr 10.1.10.50
tmsh delete ltm persistence persist-records virtual vs_web
```

- Clear records after maintenance so clients rebalance
- Disabling a pool member keeps persisted clients flowing to it
- Forcing a member offline stops even persisted traffic
- Cookie clients are only moved by deleting the cookie or a member going down

---

## Troubleshooting Persistence

- Check the `Set-Cookie` header with `curl -v` against the virtual server
- Confirm the `HTTP` profile and the persistence profile are both attached
- No records with source affinity: check the timeout and the virtual server
- Users bounce between members: look for a missing `OneConnect` profile
- One member overloaded: look for a mega proxy and change the method

```bash
curl -sv -o /dev/null http://10.1.10.100/ 2>&1 | grep -i set-cookie
curl -s -b 'BIGipServerweb_pool=185860362.20480.0000' http://10.1.10.100/
```

---

## Lab: Adding Persistence

1. Browse `vs_web` repeatedly and note how requests rotate between servers
1. Create `src_persist_24` with a `/24` mask and attach it to `vs_web`
1. View the persistence record and watch the requests stay on one member
1. Replace it with `cookie_web` in insert mode as the default method
1. Set `src_persist_24` as fallback persistence
1. Inspect the cookie with `curl -v` and decode the member address
1. Clear the records and confirm the client is load balanced again

---

## Key Takeaways

- Persistence trades even load for session continuity
- Source address affinity works for any protocol but suffers behind `NAT`
- Cookie insert is the default choice for `HTTP` and stores nothing on `BIG-IP`
- Run `HTTP` persistence with `OneConnect` for per request decisions
- Pair a default method with a fallback method
- Use match across options when sessions span services, virtual servers or pools
