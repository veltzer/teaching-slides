---
tags:
  - networking:http
  - networking:security
  - security:web-security
  - practices:scripting
level: advanced
category: networking
audience:
  - audiences:security-engineers
  - audiences:network-engineers
  - audiences:devops
  - audiences:sysadmins

---

# Securing Web Applications with iRules

---

## What This Chapter Covers

- Where iRules fit in web application defense
- Virtual patching at the edge
- Mitigating `HTTP` version, method and path traversal attacks
- Defending against `CSRF`
- Securing cookies, adding and removing headers
- Building and testing a complete defense iRule

---

## Defense in Depth

![defense_in_depth](svg/courses/networking/f5-bigip-advanced-irules/08_securing_web_applications_with_irules/defense_in_depth.svg)

---

## Where iRules Fit Next to a WAF

- The network firewall filters by address and port
- `LTM` iRules and local traffic policies act on `HTTP` fields
- `ASM` or Advanced `WAF` policies know attack signatures and learning
- The application validates its own business logic
- An iRule is the fastest way to close a specific gap at the edge

---

## What an iRule Is Good For

- A targeted fix that the `WAF` policy cannot express
- A block that must be live in an hour, not after a policy cycle
- Header and cookie hygiene for every application behind the `VS`
- Logging and counting exactly the thing you care about
- Not a replacement for a `WAF`: no signatures, no learning, no evasion handling

---

## Virtual Patching at the Edge

- A `CVE` is published against a library your application uses
- The application team needs weeks to upgrade and retest
- The exploit has a request signature you can describe
- An iRule blocks that signature today, at the `VS`
- The application is shielded while the real fix is built

---

## The Virtual Patch Timeline

![virtual_patch_timeline](svg/courses/networking/f5-bigip-advanced-irules/08_securing_web_applications_with_irules/virtual_patch_timeline.svg)

---

## Virtual Patching Workflow

1. Identify the request signature of the exploit
1. Write the block as a single purpose iRule
1. Test it with the real exploit request in the lab
1. Deploy in log only mode and watch for false positives
1. Switch to enforce
1. Remove the rule when the application is patched

---

## Log Only Mode

- The same rule, one flag decides between log and block
- Run it in production for a day before enforcing

```tcl
when RULE_INIT {
    set static::enforce 0
}
when HTTP_REQUEST {
    if { [HTTP::uri] contains {${jndi:} } {
        log local0. "vpatch [IP::client_addr] [HTTP::uri]"
        if { $static::enforce } {
            HTTP::respond 403 content "forbidden"
        }
    }
}
```

---

## HTTP Version Attacks

- `HTTP/0.9` and `HTTP/1.0` requests bypass `Host` based routing
- Old versions are a fingerprint for scanners and hand crafted tools
- `HTTP::version` returns the version string of the request
- Reject anything below `1.1` when policy allows it
- Respond `505` to tell a legitimate client why

---

## Enforcing the HTTP Version

```tcl
when HTTP_REQUEST {
    if { [HTTP::version] ne "1.1" } {
        HTTP::respond 505 content "HTTP/1.1 required"
        return
    }
    if { [HTTP::host] eq "" } {
        HTTP::respond 400 content "Host header required"
        return
    }
}
```

- `HTTP/1.1` requires a `Host` header; enforce that too

---

## Request Smuggling Awareness

- A request with both `Content-Length` and `Transfer-Encoding` is ambiguous
- Front end and back end may disagree on where the body ends
- The disagreement lets an attacker smuggle a second request
- `BIG-IP` normalizes most cases; drop the ambiguous ones anyway

```tcl
when HTTP_REQUEST {
    if { [HTTP::header exists "Content-Length"] &&
         [HTTP::header exists "Transfer-Encoding"] } {
        reject
    }
}
```

---

## Path Traversal Attacks

- The attacker walks out of the web root with `../`
- Encodings hide it: `%2e%2e%2f`, `%2e%2e/`, `..%5c`
- Double encoding hides it again: `%252e%252e%252f`
- Backslashes work on `Windows` back ends
- Decode first, then normalize, then decide

---

## Path Traversal Payloads

```http
GET /images/../../etc/passwd HTTP/1.1
GET /images/%2e%2e/%2e%2e/etc/passwd HTTP/1.1
GET /images/%252e%252e/etc/passwd HTTP/1.1
GET /images/..%5c..%5cwindows/win.ini HTTP/1.1
```

- Each of these is the same attack in a different coat
- One decoding pass catches the first three; check backslashes separately

---

## Blocking Path Traversal

```tcl
when HTTP_REQUEST {
    set path [string tolower [URI::decode [URI::decode [HTTP::path]]]]
    set path [string map {"\\" "/"} $path]
    if { $path contains "../" ||
         [class match $path starts_with forbidden_paths] } {
        log local0. "traversal [IP::client_addr] [HTTP::uri]"
        HTTP::respond 403 content "forbidden"
        return
    }
}
```

- `forbidden_paths` is a data group: `/etc/`, `/proc/`, `/windows/`

---

## Cross Site Request Forgery

- The victim is logged in; the attacker's page makes the browser send a request
- The browser attaches the session cookie automatically
- The application cannot tell the forged request from a real one
- State changing methods are the target: `POST`, `PUT`, `DELETE`, `PATCH`
- Modern browsers send `Origin` on those requests

---

## Origin Check in an iRule

```tcl
when HTTP_REQUEST {
    switch [HTTP::method] {
        "POST" - "PUT" - "DELETE" - "PATCH" {
            set origin [string tolower [HTTP::header "Origin"]]
            if { $origin eq "" } {
                set origin [string tolower [URI::host [HTTP::header "Referer"]]]
            }
            if { ![class match $origin equals allowed_origins] } {
                HTTP::respond 403 content "cross site request rejected"
                return
            }
        }
    }
}
```

---

## Limits of CSRF Defense at the Edge

- `Origin` may be missing on old clients: decide to allow or block
- `Referer` is stripped by privacy settings and some proxies
- `SameSite` cookies are the partner control, set in `HTTP_RESPONSE`
- Per form tokens belong in the application, not in an iRule
- The iRule buys time and blocks the naive attack

---

## HTTP Method Vulnerabilities

- `TRACE` and `TRACK` echo the request, including cookies
- `PUT` and `DELETE` on a misconfigured `WebDAV` server write files
- `OPTIONS` reveals what the server accepts
- `X-HTTP-Method-Override` turns a `POST` into a `DELETE`
- Allow what the application uses; deny everything else

---

## A Method Allow List

```tcl
when HTTP_REQUEST {
    switch [HTTP::method] {
        "GET" - "POST" - "HEAD" { }
        "OPTIONS" {
            HTTP::respond 204 "Allow" "GET, POST, HEAD, OPTIONS"
            return
        }
        default {
            HTTP::respond 405 content "method not allowed"
            return
        }
    }
    HTTP::header remove "X-HTTP-Method-Override"
}
```

---

## Cookie Attributes

| Attribute  | Protects against                       |
|------------|----------------------------------------|
| `Secure`   | Sending the cookie over plain `HTTP`   |
| `HttpOnly` | Reading the cookie from `JavaScript`   |
| `SameSite` | Sending the cookie on cross site requests |

- The application should set them; the iRule guarantees it
- Set them in `HTTP_RESPONSE`, on every `Set-Cookie`

---

## Securing Cookies in HTTP_RESPONSE

```tcl
when HTTP_RESPONSE {
    foreach name [HTTP::cookie names] {
        HTTP::cookie secure $name enable
        HTTP::cookie httponly $name enable
        HTTP::cookie attribute $name insert SameSite Strict
    }
}
```

- Only on an `HTTPS` virtual server: `Secure` cookies never return over `HTTP`
- `SameSite=Lax` is the compromise when the site is linked from outside

---

## The Persistence Cookie

- `BIG-IP` cookie persistence exposes the pool member address
- The cookie profile can encrypt it: `Cookie Encryption` with a passphrase
- Or set `Secure` and `HttpOnly` in the persistence profile itself
- Check the `Set-Cookie` header with `curl -i` after every change

```bash
curl -ik https://vs.example.com/ | grep -i set-cookie
```

---

## Security Headers

| Header                         | Purpose                         |
|--------------------------------|---------------------------------|
| `Strict-Transport-Security`    | Force `HTTPS` on the browser    |
| `X-Content-Type-Options`       | Stop `MIME` sniffing            |
| `X-Frame-Options`              | Stop clickjacking               |
| `Content-Security-Policy`      | Limit script and resource origins |
| `Referrer-Policy`              | Limit what `Referer` leaks      |
| `Permissions-Policy`           | Limit browser features          |

---

## Adding Security Headers

```tcl
when HTTP_RESPONSE {
    if { ![HTTP::header exists "Strict-Transport-Security"] } {
        HTTP::header insert "Strict-Transport-Security" \
            "max-age=31536000; includeSubDomains"
    }
    if { ![HTTP::header exists "X-Content-Type-Options"] } {
        HTTP::header insert "X-Content-Type-Options" "nosniff"
    }
    if { ![HTTP::header exists "X-Frame-Options"] } {
        HTTP::header insert "X-Frame-Options" "DENY"
    }
}
```

- The `exists` guard lets the application override the edge default

---

## Header Rules of Thumb

- `HSTS` only on an `HTTPS` virtual server, never on port `80`
- Start `Content-Security-Policy` in report only mode
- `X-Frame-Options: DENY` breaks legitimate frames; know your application
- `HTTP::header insert` adds; `HTTP::header replace` overwrites
- Test with the browser developer tools after every change

---

## Headers That Leak

- `Server: Apache/2.4.29 (Ubuntu)` tells the attacker which exploits to try
- `X-Powered-By: PHP/7.2.3` does the same for the runtime
- `X-AspNet-Version` and `X-AspNetMvc-Version` version the framework
- `Via` reveals internal proxies
- Internal headers such as `X-Backend` name pool members

---

## Removing Undesirable Headers

```tcl
when HTTP_RESPONSE {
    HTTP::header remove "X-Powered-By"
    HTTP::header remove "X-AspNet-Version"
    HTTP::header remove "X-AspNetMvc-Version"
    HTTP::header remove "Via"
    HTTP::header remove "X-Backend"
    HTTP::header replace "Server" "web"
}
```

- Replace `Server` with a bland value rather than removing it
- Some clients misbehave when `Server` is absent

---

## Stripping Spoofed Request Headers

- Clients can send `X-Forwarded-For` themselves to fake their address
- Remove it on the way in, then let the `HTTP` profile insert the real one

```tcl
when HTTP_REQUEST {
    HTTP::header remove "X-Forwarded-For"
    HTTP::header remove "X-Real-IP"
    HTTP::header insert "X-Forwarded-For" [IP::client_addr]
}
```

---

## The Response Hardening Pipeline

![response_hardening](svg/courses/networking/f5-bigip-advanced-irules/08_securing_web_applications_with_irules/response_hardening.svg)

---

## Composing the Complete Defense iRule

- Request side: method allow list, version check, traversal check, `CSRF` check
- Response side: header removal, header insertion, cookie hardening
- A `static::` debug flag and `HSL` logging of every block
- An `ISTATS` counter per block reason
- Cheapest checks first, `return` after every response

---

## The Request Pipeline

![defense_request_pipeline](svg/courses/networking/f5-bigip-advanced-irules/08_securing_web_applications_with_irules/defense_request_pipeline.svg)

---

## Defense iRule: Setup and Helpers

```tcl
# sec_web_defense v1.0 - edge hardening for vs_web
when RULE_INIT {
    set static::enforce 1
}
proc block { hsl reason code } {
    HSL::send $hsl "<132>block $reason [IP::client_addr] \
        [HTTP::method] [HTTP::uri]"
    ISTATS::incr "ltm.virtual [virtual name] c block_$reason" 1
    if { $static::enforce } {
        HTTP::respond $code content "forbidden"
    }
}
when CLIENT_ACCEPTED {
    set hsl [HSL::open -proto UDP -pool syslog_pool]
}
```

---

## Defense iRule: Method and Version

```tcl
when HTTP_REQUEST {
    switch [HTTP::method] {
        "GET" - "POST" - "HEAD" { }
        default {
            call sec_web_defense::block $hsl method 405
            return
        }
    }
    if { [HTTP::version] ne "1.1" } {
        call sec_web_defense::block $hsl version 505
        return
    }
    HTTP::header remove "X-HTTP-Method-Override"
    HTTP::header remove "X-Forwarded-For"
```

---

## Defense iRule: Traversal and CSRF

```tcl
    set path [string tolower [URI::decode [URI::decode [HTTP::path]]]]
    set path [string map {"\\" "/"} $path]
    if { $path contains "../" ||
         [class match $path starts_with forbidden_paths] } {
        call sec_web_defense::block $hsl traversal 403
        return
    }
    if { [HTTP::method] eq "POST" } {
        set origin [string tolower [HTTP::header "Origin"]]
        if { ![class match $origin equals allowed_origins] } {
            call sec_web_defense::block $hsl csrf 403
            return
        }
    }
}
```

---

## Defense iRule: Response Side

```tcl
when HTTP_RESPONSE {
    HTTP::header remove "X-Powered-By"
    HTTP::header remove "X-AspNet-Version"
    HTTP::header remove "Via"
    HTTP::header replace "Server" "web"
    if { ![HTTP::header exists "Strict-Transport-Security"] } {
        HTTP::header insert "Strict-Transport-Security" "max-age=31536000"
    }
    HTTP::header insert "X-Content-Type-Options" "nosniff"
    HTTP::header insert "X-Frame-Options" "DENY"
    foreach name [HTTP::cookie names] {
        HTTP::cookie secure $name enable
        HTTP::cookie httponly $name enable
    }
}
```

---

## Testing Each Attack

```bash
# path traversal, keep the dots as sent
curl -i --path-as-is "https://vs.example.com/../../etc/passwd"
# forbidden method
curl -i -X TRACE https://vs.example.com/
# old protocol version
curl -i --http1.0 https://vs.example.com/
# cross site POST
curl -i -X POST -H "Origin: https://evil.example" \
    https://vs.example.com/account/delete
```

- Each must return the expected status: `403`, `405`, `505`, `403`

---

## Checking the Evidence

```bash
tail -f /var/log/ltm
tmsh show ltm virtual vs_web
istats dump | grep block_
```

```output
ltm.virtual /Common/vs_web c block_traversal 12
ltm.virtual /Common/vs_web c block_method 3
ltm.virtual /Common/vs_web c block_version 1
ltm.virtual /Common/vs_web c block_csrf 7
```

- The remote collector receives the `HSL` lines with client and reason

---

## Rolling It Out

1. Attach with `static::enforce 0` and watch the counters for a day
1. Investigate every block reason that hits legitimate traffic
1. Adjust the data groups, not the code
1. Set `static::enforce 1` and save the configuration
1. Keep timing on for the first week and read the cycles
1. Add the rule to your iRule library with its test script

---

## Key Takeaways

- iRules are the fastest control at the edge, next to a `WAF`, not instead of it
- Decode and normalize before deciding; check the cheap things first
- Harden every response: strip, add, secure the cookies
- Log every block with a reason and count it
- Ship in log only mode, then enforce, then retire when the application is fixed
