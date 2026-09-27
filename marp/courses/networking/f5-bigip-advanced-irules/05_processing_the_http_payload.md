---
tags:
  - networking:http
  - networking:web
  - networking:security
  - practices:scripting
level: advanced
category: networking
audience:
  - audiences:security-engineers
  - audiences:network-engineers
  - audiences:devops
  - audiences:sysadmins

---

# Processing the HTTP Payload

---

## What This Chapter Covers

- Reviewing `HTTP` headers and the commands that read them
- Accessing and manipulating headers with `HTTP::header`
- Other `HTTP` commands: host, method, status, respond, redirect
- Parsing and normalizing the `URI`
- Parsing cookies with `HTTP::cookie`
- Collecting and inspecting the body
- Selectively compressing `HTTP` data

---

## Anatomy of a Request

```http
POST /app/login?next=%2Fhome HTTP/1.1
Host: www.example.com
User-Agent: curl/8.5.0
Content-Type: application/x-www-form-urlencoded
Content-Length: 24
Cookie: session=abc123; theme=dark

user=bob&pass=hunter2
```

- Request line: method, `URI`, version
- Headers until the first empty line
- Body follows, sized by `Content-Length` or chunked

---

## Anatomy of a Response

```http
HTTP/1.1 200 OK
Server: Apache/2.4.58
X-Powered-By: PHP/8.2
Set-Cookie: session=abc123; Path=/
Content-Type: text/html
Content-Length: 512

<html>...</html>
```

- Status line: version, status code, reason phrase
- `Server` and `X-Powered-By` leak implementation details
- `Set-Cookie` attributes decide how the browser protects the cookie

---

## Headers a Security Team Cares About

| Header | Direction | Why it matters |
|--------|-----------|----------------|
| `Host` | request | virtual hosting, routing decisions |
| `X-Forwarded-For` | request | real client address behind the proxy |
| `Content-Type` | both | parser selection, upload filtering |
| `Cookie` / `Set-Cookie` | both | sessions, persistence, theft |
| `Location` | response | redirects, open redirect abuse |
| `Server` / `X-Powered-By` | response | fingerprinting |

---

## Where iRule Commands Read Each Piece

![http_anatomy](svg/courses/networking/f5-bigip-advanced-irules/05_processing_the_http_payload/http_anatomy.svg)

---

## Introducing the HTTP Header Commands

- All `HTTP::` commands need an `HTTP` profile on the virtual server
- Without it the `HTTP_REQUEST` event never fires
- Request commands run in `HTTP_REQUEST` and `HTTP_REQUEST_DATA`
- Response commands run in `HTTP_RESPONSE` and `HTTP_RESPONSE_DATA`
- Calling a request command in a response event is a runtime error
- `SSL` must be terminated on the `BIG-IP` for `HTTPS` payloads to be visible

---

## Request Events Versus Response Events

| Event | Fires when | Typical use |
|-------|------------|-------------|
| `HTTP_REQUEST` | request headers parsed | routing, blocking, rewriting |
| `HTTP_REQUEST_DATA` | collected request body ready | body inspection |
| `HTTP_RESPONSE` | response headers from the server | header hardening |
| `HTTP_RESPONSE_DATA` | collected response body ready | body rewrite |

---

## Reading Headers

```tcl
when HTTP_REQUEST {
    if { [HTTP::header exists "X-Forwarded-For"] } {
        set xff [HTTP::header value "X-Forwarded-For"]
        log local0. "client via proxy: $xff"
    }
    set ua [HTTP::header "User-Agent"]
    set n [HTTP::header count]
    log local0. "[HTTP::header names] ($n headers)"
}
```

- `HTTP::header value NAME` and `HTTP::header NAME` are equivalent
- A missing header returns an empty string, check `exists` first

---

## Header Names Are Case Insensitive

- `HTTP::header "host"` and `HTTP::header "Host"` return the same value
- Matching follows the `HTTP` specification, not `Tcl` string rules
- Values are case sensitive and returned verbatim
- Do not `string tolower` the name, do it on the value when you compare
- Leading and trailing whitespace of a value is trimmed

---

## Multiple Headers With the Same Name

```tcl
when HTTP_REQUEST {
    # returns the value of the first matching header
    set first [HTTP::header value "X-Forwarded-For"]
    # returns all values as a Tcl list
    set all [HTTP::header values "X-Forwarded-For"]
    log local0. "first=$first all=$all"
}
```

- `X-Forwarded-For` frequently appears more than once
- The last hop appended by a trusted proxy is the reliable one
- `HTTP::header values` gives every occurrence in order

---

## Inserting and Replacing Headers

```tcl
when HTTP_REQUEST {
    # insert adds a header even if one already exists
    HTTP::header insert "X-Forwarded-For" [IP::client_addr]
    # replace overwrites, or inserts when missing
    HTTP::header replace "X-Forwarded-Proto" "https"
    # add a request id for correlation across tiers
    HTTP::header insert "X-Request-Id" [TMM::cmp_unit][clock clicks]
}
```

- `insert` never removes an existing header, watch for duplicates
- `replace` is what you usually want for a single-valued header

---

## Removing Headers on the Way Out

```tcl
when HTTP_RESPONSE {
    HTTP::header remove "Server"
    HTTP::header remove "X-Powered-By"
    HTTP::header remove "X-AspNet-Version"
    if { [HTTP::header exists "Via"] } {
        HTTP::header remove "Via"
    }
}
```

- Removing a missing header is harmless
- `HTTP::header sanitize` keeps only a list of allowed headers
- Do not remove `Content-Length` or `Transfer-Encoding` by accident

---

## Sanitizing to an Allow List

```tcl
when HTTP_RESPONSE {
    # keep only these headers, drop every other one
    HTTP::header sanitize "Content-Type" "Content-Length" \
        "Cache-Control" "Set-Cookie" "Location"
}
```

- Allow list is safer than a deny list against unknown headers
- Keep the headers the browser needs to render and cache
- Test with `curl -i` against every application path before deploying

---

## Host, Method and Version

```tcl
when HTTP_REQUEST {
    set host [string tolower [HTTP::host]]
    switch [HTTP::method] {
        "GET" - "HEAD" - "POST" { }
        default { reject }
    }
    if { [HTTP::version] eq "1.0" } {
        HTTP::header replace "Connection" "close"
    }
}
```

- `HTTP::host` is the `Host` header without the port if standard
- `HTTP::method` returns the verb exactly as sent, so compare uppercase

---

## Status and Keepalive

```tcl
when HTTP_RESPONSE {
    if { [HTTP::status] >= 500 } {
        log local0. "server error [HTTP::status] from [LB::server]"
    }
    if { [HTTP::is_keepalive] } {
        HTTP::header replace "Keep-Alive" "timeout=5, max=100"
    }
}
```

- `HTTP::status` is only valid in response events
- `HTTP::is_keepalive` tells whether the connection stays open afterwards
- Both are read only, the pool member decides the status

---

## HTTP::redirect

```tcl
when HTTP_REQUEST {
    if { [HTTP::host] eq "old.example.com" } {
        HTTP::redirect "https://www.example.com[HTTP::uri]"
    }
}
```

- Builds a `302 Found` with a `Location` header and no body
- The request never reaches the pool
- Use `HTTP::respond 301` when you need a permanent redirect
- Always include the original `URI` unless you mean to drop it

---

## HTTP::respond

```tcl
when HTTP_REQUEST {
    if { [HTTP::uri] starts_with "/admin" } {
        HTTP::respond 403 content "Forbidden" \
            "Content-Type" "text/plain" \
            "Connection" "close"
    }
}
```

- Sends a complete response from the `BIG-IP` itself
- Status, optional `content`, then header name and value pairs
- Only one `respond` or `redirect` per request, then stop the rule
- `return` right after it keeps later code from running

---

## Reading and Setting the URI

```tcl
when HTTP_REQUEST {
    set uri [HTTP::uri]
    if { $uri starts_with "/v1/" } {
        # rewrite the path the server sees
        HTTP::uri "/api[string range $uri 3 end]"
    }
    log local0. "path=[HTTP::path] query=[HTTP::query]"
}
```

- `HTTP::uri` with an argument rewrites the request line
- `HTTP::path` is the part before `?`, `HTTP::query` the part after
- Rewriting happens before load balancing, the pool sees the new value

---

## The URI Decomposed

![uri_decomposition](svg/courses/networking/f5-bigip-advanced-irules/05_processing_the_http_payload/uri_decomposition.svg)

---

## The URI Commands

| Command | Input | Returns |
|---------|-------|---------|
| `URI::path` | full `URI` | directory part with slashes |
| `URI::basename` | full `URI` | last path segment |
| `URI::query` | `URI` and name | value of one query parameter |
| `URI::decode` | string | percent decoded form |
| `URI::encode` | string | percent encoded form |

- `URI::` commands take a string, `HTTP::path` reads the current request
- `URI::path [HTTP::uri]` and `HTTP::path` differ: one keeps only directories

---

## Working With Query Parameters

```tcl
when HTTP_REQUEST {
    set user [URI::query [HTTP::uri] "user"]
    set fmt [URI::query [HTTP::uri] "fmt"]
    if { $user eq "" } {
        HTTP::respond 400 content "missing user" "Connection" "close"
        return
    }
    log local0. "user=$user fmt=$fmt"
}
```

- Missing parameters return an empty string
- Values come back still percent encoded
- Decode before comparing, encode before rebuilding a `URI`

---

## Decoding Before Deciding

```tcl
when HTTP_REQUEST {
    set path [string tolower [URI::decode [HTTP::path]]]
    if { $path contains "../" } {
        reject
        return
    }
}
```

- Attackers encode `../` as `%2e%2e%2f` to slip past naive matches
- Double encoding turns `%2e` into `%252e`, so decode until stable
- Lower case the decoded value, `Windows` backends ignore case
- Decide on the normalized form, not on what was sent

---

## Decoding Until Stable

```tcl
when HTTP_REQUEST {
    set raw [HTTP::uri]
    set dec [URI::decode $raw]
    set rounds 0
    while { $dec ne $raw && $rounds < 3 } {
        set raw $dec
        set dec [URI::decode $raw]
        incr rounds
    }
    if { $rounds == 3 } { reject }
}
```

- Bound the loop, a hostile `URI` can decode forever
- More than two rounds is itself suspicious, reject it

---

## Forward One Form Consistently

- Two choices: forward the original `URI` or the normalized one
- Forwarding the original keeps the application's own decoding intact
- Forwarding the normalized one removes ambiguity for every backend
- Never mix: decide on normalized and forward original only when both agree
- Document the choice in the iRule header comment

---

## Reading Cookies

```tcl
when HTTP_REQUEST {
    if { [HTTP::cookie exists "session"] } {
        set sid [HTTP::cookie value "session"]
        log local0. "session $sid from [IP::client_addr]"
    }
    foreach name [HTTP::cookie names] {
        log local0. "cookie: $name"
    }
}
```

- `HTTP::cookie names` returns every cookie name in the request
- `HTTP::cookie value NAME` and `HTTP::cookie NAME` are equivalent

---

## Inserting and Removing Cookies

```tcl
when HTTP_REQUEST {
    # cookie the server will see, scoped to the api path
    HTTP::cookie insert name "region" value "eu" path "/api"
    # strip a cookie the server must never trust
    HTTP::cookie remove "debug"
}
```

- Insert on the request side adds to the `Cookie` header
- Insert on the response side adds a `Set-Cookie` header
- Removing a cookie the client sent does not remove it from the browser

---

## Cookie Handling in Each Direction

![cookie_lanes](svg/courses/networking/f5-bigip-advanced-irules/05_processing_the_http_payload/cookie_lanes.svg)

---

## Setting Cookie Attributes

```tcl
when HTTP_RESPONSE {
    foreach name [HTTP::cookie names] {
        HTTP::cookie attribute $name insert "Secure"
        HTTP::cookie attribute $name insert "HttpOnly"
    }
    HTTP::cookie attribute "session" insert "Max-Age" "1800"
}
```

- `HTTP::cookie secure NAME enable` is the shortcut for the first line
- `HTTP::cookie httponly NAME enable` is the shortcut for the second
- Attributes only exist on `Set-Cookie`, so response events only

---

## Encrypting Cookies

```tcl
when HTTP_RESPONSE {
    HTTP::cookie encrypt "session" "my_passphrase"
}
when HTTP_REQUEST {
    HTTP::cookie decrypt "session" "my_passphrase"
}
```

- The client stores ciphertext, the server never notices
- Tampering produces garbage that the application rejects
- The passphrase belongs in a data group, not in the rule text
- The `HTTP` profile has the same feature without any `Tcl`

---

## Cookies and Persistence

- Cookie persistence inserts `BIGipServer<pool>` automatically
- iRules run before the persistence profile evaluates the request
- Removing or rewriting that cookie breaks server stickiness
- Encrypt it with the profile setting, not with an iRule
- `persist cookie insert` in an iRule overrides the profile per request

---

## Collecting the Body

```tcl
when HTTP_REQUEST {
    if { [HTTP::method] eq "POST" } {
        set len [HTTP::header "Content-Length"]
        if { $len > 0 && $len < 65536 } {
            HTTP::collect $len
        }
    }
}
```

- Headers arrive first, the body is not available in `HTTP_REQUEST`
- `HTTP::collect N` buffers up to `N` bytes in `TMM`
- Without `N` the whole body is collected, chunked or not

---

## The Collect Flow

![collect_flow](svg/courses/networking/f5-bigip-advanced-irules/05_processing_the_http_payload/collect_flow.svg)

---

## Inspecting the Collected Body

```tcl
when HTTP_REQUEST_DATA {
    set body [HTTP::payload]
    set user [URI::query "?$body" "user"]
    if { [string length $user] > 64 } {
        HTTP::respond 400 content "bad user" "Connection" "close"
        return
    }
    HTTP::release
}
```

- `HTTP_REQUEST_DATA` fires once the collected bytes are in
- `HTTP::payload length` reports what was actually collected
- `HTTP::release` sends the request on, forgetting it stalls the connection

---

## Content-Length Versus Chunked

- `Content-Length` bodies have a known size, collect exactly that
- Chunked bodies have no size up front, `HTTP::collect` gathers as it goes
- Bound the collect size in both cases to protect `TMM` memory
- Collect only the first kilobytes for a parameter check
- A `1 MB` collect on a busy virtual server is a self inflicted attack

---

## Rewriting a Response Body

```tcl
when HTTP_RESPONSE {
    if { [HTTP::header "Content-Type"] starts_with "text/html" } {
        HTTP::collect
    }
}
when HTTP_RESPONSE_DATA {
    set find "http://internal.example.com"
    set repl "https://www.example.com"
    set off [string first $find [HTTP::payload]]
    if { $off >= 0 } {
        HTTP::payload replace $off [string length $find] $repl
    }
    HTTP::release
}
```

---

## Body Rewrite Pitfalls

- Replacing changes the length, so `Content-Length` no longer matches
- `HTTP::payload replace` updates `Content-Length` when the body was fully collected
- For partial collects remove `Content-Length` and let chunking take over
- Compressed responses must be decompressed first or not rewritten at all
- A `Stream` profile does simple find and replace with far less cost

---

## Selectively Compressing

```tcl
when HTTP_REQUEST {
    if { [HTTP::uri] starts_with "/account" } {
        COMPRESS::disable
    }
}
when HTTP_RESPONSE {
    if { [HTTP::header "Content-Type"] starts_with "image/" } {
        COMPRESS::disable
    }
}
```

- Requires an `HTTP` compression profile on the virtual server
- `COMPRESS::enable` and `COMPRESS::disable` decide per response

---

## When to Disable Compression

- Content already compressed: images, video, archives, `PDF`
- Tiny responses where the header overhead exceeds the savings
- Pages that mix a secret with attacker controlled input
    - `BREACH` style attacks recover the secret from the compressed size
    - Disable compression on login, token and account pages
- `COMPRESS::method` reports which algorithm was negotiated

---

## Key Takeaways

- Every `HTTP::` command needs the `HTTP` profile and the right event
- `HTTP::header` reads, inserts, replaces, removes and sanitizes
- `HTTP::respond` and `HTTP::redirect` end the request at the edge
- Decode and normalize the `URI` before making any decision
- Cookie attributes and encryption belong in `HTTP_RESPONSE`
- Bound every `HTTP::collect` and always `HTTP::release`
