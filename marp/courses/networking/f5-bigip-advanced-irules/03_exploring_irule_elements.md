---
tags:
  - networking:http
  - architecture:load-balancing
  - practices:scripting
level: advanced
category: networking
audience:
  - audiences:security-engineers
  - audiences:network-engineers
  - audiences:devops
  - audiences:sysadmins

---

# Exploring iRule Elements

---

## What This Chapter Covers

- `Tcl` syntax as used inside iRules
- Events, event context and the connection lifecycle
- Query, action and utility commands
- Logging with the `log` command
- Variables: local, `static::` and global
- Operators, conditionals, loops
- Best practices for production iRules

---

## The Shape of an iRule

- An iRule is a list of `when EVENT { ... }` blocks
- Each block runs when that event fires on the connection
- The body is plain `Tcl` plus the iRule command set
- One iRule can handle many events
- Blocks for events that never fire simply never run

```tcl
when HTTP_REQUEST {
    log local0. "request for [HTTP::uri]"
}
when HTTP_RESPONSE {
    log local0. "status [HTTP::status]"
}
```

---

## Tcl in One Slide

- Everything is a command: the first word names it, the rest are arguments
- `[cmd args]` runs a command and substitutes its result
- `$name` substitutes a variable's value
- `{ ... }` groups without substitution, `" ... "` groups with substitution
- `#` starts a comment, only at the start of a command
- A trailing backslash continues the command on the next line

---

## Substitution in Practice

```tcl
when HTTP_REQUEST {
    set host [HTTP::host]
    set path [HTTP::path]
    log local0. "host=$host path=$path"
    log local0. {no substitution: $host}
    HTTP::header insert X-Backend-Host \
        "$host-internal"
}
```

- Line four logs the values, line five logs the literal text
- The backslash splits a long command across two lines

---

## Braces and the if Command

- `if` and `while` take their condition inside braces
- Braces delay substitution until the command evaluates it
- Using quotes instead breaks quoting and wastes cycles
- The body is also a braced block, run only when needed

```tcl
when HTTP_REQUEST {
    if { [HTTP::method] eq "TRACE" } {
        reject
    }
}
```

---

## Events: Where Code Runs

- An event is a point in the life of a connection
- The iRule engine calls your block at exactly that point
- Client side events describe the client connection
- Server side events describe the pool member connection
- Which commands are legal depends on the event

---

## Client Side Events

| Event | Fires when |
| --- | --- |
| `CLIENT_ACCEPTED` | client `TCP` handshake completes |
| `CLIENTSSL_HANDSHAKE` | client `TLS` handshake completes |
| `HTTP_REQUEST` | request headers fully parsed |
| `HTTP_REQUEST_DATA` | collected request body is available |
| `CLIENT_CLOSED` | client connection closes |

---

## Server Side Events

| Event | Fires when |
| --- | --- |
| `LB_SELECTED` | a pool member has been chosen |
| `LB_FAILED` | no pool member could be selected |
| `SERVER_CONNECTED` | server `TCP` handshake completes |
| `HTTP_RESPONSE` | response headers fully parsed |
| `HTTP_RESPONSE_DATA` | collected response body is available |
| `SERVER_CLOSED` | server connection closes |

---

## Event Timeline of an HTTP Connection

![event_timeline](svg/courses/networking/f5-bigip-advanced-irules/03_exploring_irule_elements/event_timeline.svg)

---

## The TCP Connection Lifecycle

1. `CLIENT_ACCEPTED`: client side connection exists, no server side yet
1. `LB_SELECTED`: the load balancer picked a member
1. `SERVER_CONNECTED`: server side connection exists
1. Data flows in both directions
1. `CLIENT_CLOSED` and `SERVER_CLOSED` as each side ends
1. Server side setup is lazy: it waits for the first data that needs it

---

## The HTTP Connection Lifecycle

- One `TCP` connection can carry many `HTTP` requests
- With keep-alive `HTTP_REQUEST` fires once per request
- `HTTP_RESPONSE` fires once per response on the same connection
- `CLIENT_ACCEPTED` fires only once, before the first request
- Per-request state therefore belongs in `HTTP_REQUEST`, not in `CLIENT_ACCEPTED`

---

## Event Context Matters

- `HTTP::status` is only valid in response events
- `HTTP::uri` is valid in `HTTP_REQUEST` and later events
- `LB::server` is empty before `LB_SELECTED`
- `SSL::cipher` is valid only after `CLIENTSSL_HANDSHAKE`
- Calling a command in the wrong event raises a runtime error and aborts the connection

```tcl
when HTTP_REQUEST {
    # runtime error: no response exists yet
    log local0. [HTTP::status]
}
```

---

## RULE_INIT

- Fires when the iRule is loaded or saved, not per connection
- Runs once per `TMM` instance
- The place to initialize `static::` variables
- No connection context: no `HTTP::` or `IP::` commands

```tcl
when RULE_INIT {
    set static::maint_page "<html>Back soon</html>"
    set static::debug 0
}
```

---

## Event Priority

- Several iRules on one virtual server all handle the same event
- Execution order within an event follows `priority`, then list order
- Default priority is 500, lower numbers run first
- `priority` may be set for the whole iRule or per event

```tcl
priority 100
when HTTP_REQUEST {
    log local0. "runs before default-priority rules"
}
```

---

## Multiple iRules on One Virtual Server

![irule_priority](svg/courses/networking/f5-bigip-advanced-irules/03_exploring_irule_elements/irule_priority.svg)

---

## Stopping Early

- `return` leaves the current event block of the current iRule only
- `event disable` stops this event firing again on this connection
- `event HTTP_REQUEST disable` names the event to silence
- Neither stops other iRules that also handle the event

```tcl
when HTTP_REQUEST {
    if { [HTTP::uri] starts_with "/health" } {
        HTTP::respond 200 content "ok"
        return
    }
    event disable
}
```

---

## Three Kinds of Commands

![command_taxonomy](svg/courses/networking/f5-bigip-advanced-irules/03_exploring_irule_elements/command_taxonomy.svg)

---

## Query Commands

- Return information about the connection or message
- Have no side effect on the traffic
- Cheap to call, but every call still costs cycles
- Store the result in a variable when used more than once

```tcl
when HTTP_REQUEST {
    set uri [HTTP::uri]
    set client [IP::client_addr]
    set port [TCP::client_port]
    set proto [HTTP::version]
}
```

---

## Action Commands

- Change what happens to the connection
- `pool` selects a pool, `node` selects a specific address
- `HTTP::respond` answers directly from `BIG-IP`
- `HTTP::redirect` sends a `302` with a `Location` header
- `reject` resets the connection, `drop` silently discards it

```tcl
when HTTP_REQUEST {
    if { [HTTP::uri] starts_with "/api" } {
        pool pool_api
    } else {
        pool pool_web
    }
}
```

---

## Utility Commands

- `log` writes to `syslog-ng`
- `table` stores shared session state across connections
- `class` looks up data groups
- `HSL::send` ships logs to an external collector
- `ISTATS` increments custom statistics counters

---

## Command Namespaces

| Namespace | Scope |
| --- | --- |
| `HTTP::` | headers, `URI`, cookies, payload |
| `TCP::` | ports, options, payload |
| `IP::` | addresses, `TOS`, `TTL` |
| `SSL::` | cipher, certificates, session |
| `LB::` | pool and member selection |
| `URI::` | parsing and decoding of a `URI` string |

---

## Logging With the log Command

- `log <facility>.<level> "message"`
- `local0.` is the conventional facility for iRules
- Messages land in `/var/log/ltm` via `syslog-ng`
- Level defaults to `info` when omitted after the dot
- The message is prefixed with the iRule name and the event

```tcl
when HTTP_REQUEST {
    log local0. "[IP::client_addr] [HTTP::method] [HTTP::uri]"
}
```

---

## Logging Details

- `log local0.warn "..."` picks the level explicitly
- `log -noname local0. "..."` drops the `Rule /Common/x` prefix
- Logging is synchronous in the data plane: it slows every connection
- Never log per request on a busy virtual server without a guard
- High speed logging is covered in the efficiency chapter

```tcl
when HTTP_REQUEST {
    if { $static::debug } {
        log local0. "debug: [HTTP::uri]"
    }
}
```

---

## Local Variables

- Created with `set`, read with `$name`
- Scope is the connection, across all events and all iRules on it
- A value set in `HTTP_REQUEST` is visible in `HTTP_RESPONSE`
- Destroyed when the connection closes
- No declaration; a variable exists once assigned

```tcl
when HTTP_REQUEST {
    set start [clock clicks -milliseconds]
}
when HTTP_RESPONSE {
    set took [expr {[clock clicks -milliseconds] - $start}]
    log local0. "[HTTP::status] took ${took}ms"
}
```

---

## Checking and Removing Variables

- Reading an unset variable is a runtime error
- `info exists name` tests without reading
- `unset name` removes it; `unset -nocomplain` tolerates absence
- With keep-alive, a variable from a previous request may linger

```tcl
when HTTP_REQUEST {
    if { [info exists start] } {
        unset start
    }
    set start [clock clicks -milliseconds]
}
```

---

## Variable Scopes

![variable_scopes](svg/courses/networking/f5-bigip-advanced-irules/03_exploring_irule_elements/variable_scopes.svg)

---

## Static Variables

- Named `static::name`, shared across all connections of the iRule
- Set them in `RULE_INIT`, read them everywhere else
- Ideal for constants: pool names, page bodies, feature flags
- Writing them outside `RULE_INIT` demotes the virtual server from `CMP`

```tcl
when RULE_INIT {
    set static::blocked_agents [list "sqlmap" "nikto"]
}
when HTTP_REQUEST {
    set ua [string tolower [HTTP::header User-Agent]]
    foreach a $static::blocked_agents {
        if { $ua contains $a } { reject }
    }
}
```

---

## Global Variables and CMP

- `::name` is a `Tcl` global, shared by every connection and iRule
- `CMP` (clustered multiprocessing) runs a virtual server on all `TMM` instances
- Globals cannot be shared across `TMM` instances safely
- `BIG-IP` therefore demotes the virtual server to a single `TMM`
- Result: a fraction of the platform's throughput
- Use `static::` for read-only data and `table` for shared mutable state

---

## Everything Is a String

- `Tcl` has one data type: the string
- Numbers are strings that `expr` knows how to parse
- Lists are strings with whitespace separated elements
- Commands convert on demand, which costs cycles
- `"10" eq "10.0"` is false, `10 == 10.0` is true

---

## Arithmetic With expr

- `expr` evaluates a mathematical expression
- Always brace the expression: `[expr {$a + 1}]`
- Unbraced expressions are parsed twice and are an injection risk
- `incr name` adds one, `incr name 5` adds five

```tcl
when HTTP_REQUEST {
    set len [HTTP::header Content-Length]
    if { $len ne "" && [expr {$len / 1024}] > 512 } {
        HTTP::respond 413 content "too large"
    }
}
```

---

## Comparison Operators

| Operator | Meaning |
| --- | --- |
| `==` `!=` | numeric comparison |
| `eq` `ne` | string comparison |
| `<` `<=` `>` `>=` | numeric ordering |
| `&&` `\|\|` `!` | logical and, or, not |

- Comparing `HTTP` strings with `==` forces a numeric parse attempt
- Use `eq` and `ne` for anything that is not a number

---

## iRule String Operators

- `contains`, `starts_with`, `ends_with`, `equals`
- `matches_glob` for wildcard patterns
- `matches_regex` for regular expressions, at a real cost
- `not` negates any of them inside an expression
- All are case sensitive; lowercase the input first when needed

```tcl
when HTTP_REQUEST {
    if { [string tolower [HTTP::path]] ends_with ".php" } {
        reject
    }
}
```

---

## Conditionals With if

- `if { cond } { body } elseif { cond } { body } else { body }`
- Conditions are evaluated in order; the first true branch wins
- Long chains cost more the further down the match is
- Keep the most common case first

```tcl
when HTTP_REQUEST {
    if { [HTTP::host] eq "api.example.com" } {
        pool pool_api
    } elseif { [HTTP::host] eq "static.example.com" } {
        pool pool_static
    } else {
        pool pool_web
    }
}
```

---

## Conditionals With switch

- `switch` compares one value against many patterns
- Exact matching by default, `-glob` for wildcards
- `default` catches everything else
- A `-` body falls through to the next pattern's body

```tcl
when HTTP_REQUEST {
    switch -glob [HTTP::path] {
        "/images/*" -
        "/css/*" { pool pool_static }
        "/api/*" { pool pool_api }
        default { pool pool_web }
    }
}
```

---

## Choosing the Control Structure

![control_flow_choices](svg/courses/networking/f5-bigip-advanced-irules/03_exploring_irule_elements/control_flow_choices.svg)

---

## Loops

- `while { cond } { body }` and `for {init} {cond} {step} { body }`
- `foreach item $list { body }` walks a list
- `break` leaves the loop, `continue` skips to the next iteration
- Every iteration runs in the data plane and delays the connection

```tcl
when HTTP_REQUEST {
    foreach name [HTTP::header names] {
        if { [string tolower $name] starts_with "x-internal-" } {
            HTTP::header remove $name
        }
    }
}
```

---

## Loops Are Dangerous

- An unbounded loop stalls a `TMM` and every connection on it
- Never loop on data an attacker controls without a cap
- Prefer a `switch`, a data group or a `string` command to a loop
- If you must loop, loop over a short fixed list

```tcl
when HTTP_REQUEST {
    set n 0
    foreach c [HTTP::cookie names] {
        if { [incr n] > 50 } { reject }
    }
}
```

---

## A Maintenance Page Responder

```tcl
when RULE_INIT {
    set static::maint "<html><body>Back soon</body></html>"
}
when HTTP_REQUEST {
    if { [active_members [LB::server pool]] < 1 } {
        HTTP::respond 503 content $static::maint \
            "Content-Type" "text/html" \
            "Retry-After" "120"
    }
}
```

- The page is built once in `RULE_INIT`
- `active_members` checks pool health without selecting a member

---

## Client Address Based Pool Selection

```tcl
when CLIENT_ACCEPTED {
    if { [IP::addr [IP::client_addr] equals 10.0.0.0/8] } {
        pool pool_internal
    } else {
        pool pool_public
    }
}
```

- `IP::addr` compares addresses and prefixes correctly
- `CLIENT_ACCEPTED` is the earliest event with the client address
- Deciding early avoids parsing `HTTP` when it is not needed

---

## Naming, Comments and Structure

- Name iRules by purpose: `redirect_http_to_https`, `block_bad_agents`
- A header comment states what, why, owner and date
- One event block per event; group related logic together
- Comment the intent, not the syntax
- Keep each iRule to one responsibility

```tcl
# block_bad_agents: reject known scanner user agents
# owner: security-infra, 2026-09
when HTTP_REQUEST {
    # ...
}
```

---

## Return Early, Fail Closed

- Handle the rejecting or short-circuit case first, then `return`
- Deep nesting hides the common path
- When a check cannot be completed, reject rather than pass
- A `catch` that swallows an error and continues is an open door

```tcl
when HTTP_REQUEST {
    if { [HTTP::method] eq "TRACE" } {
        reject
        return
    }
    if { [catch { set d [URI::decode [HTTP::uri]] }] } {
        reject
        return
    }
}
```

---

## Stay Out of the Hot Path

- A profile or local traffic policy is compiled, an iRule is interpreted
- `HTTP` to `HTTPS` redirect, header insertion, simple routing: use a policy
- Reserve iRules for logic that profiles and policies cannot express
- Every iRule on a busy virtual server is paid for on every event
- Prefer the earliest event that already has the data you need

---

## Key Takeaways

- iRules are `Tcl` event blocks; braces, brackets and quotes matter
- Events give context; commands are only valid in the right one
- Local variables live for the connection, `static::` for the iRule, globals are avoided
- `eq` and `ne` for strings, `==` and `!=` for numbers
- `switch -glob` beats long `if` chains; loops need a cap
- Return early, fail closed, and let profiles do the simple work
