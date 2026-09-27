---
tags:
  - networking:http
  - practices:scripting
  - architecture:load-balancing
level: advanced
category: networking
audience:
  - audiences:security-engineers
  - audiences:network-engineers
  - audiences:devops
  - audiences:sysadmins

---

# Getting Started With iRules

---

## What This Chapter Covers

- What an iRule is and how it customizes application delivery
- What iRules can do that profiles and policies cannot
- Assigning iRules to a virtual server and ordering them
- The `DevCentral` ecosystem
- Creating and deploying iRules from the `GUI` and from `tmsh`
- Your first iRule: redirecting `HTTP` to `HTTPS`

---

## What Is an iRule?

- A small `Tcl` script attached to a virtual server
- Event driven: code runs when `TMM` reaches a point in the connection
- Runs inside the data plane, on every matching connection
- Can read, rewrite, route, reject and log traffic
- Uses `BIG-IP` specific commands on top of standard `Tcl`

```tcl
when HTTP_REQUEST {
    if { [HTTP::uri] starts_with "/admin" } {
        reject
    }
}
```

---

## Customizing Application Delivery

- Profiles give you fixed knobs: compression on, `HTTP/2` on, timeouts
- Local traffic policies give you rules: if condition then action
- iRules give you a programming language on the traffic path
- Typical uses: redirects, header rewriting, content routing, logging
- Security uses: block methods, strip headers, virtual patching

---

## Profiles, Policies and iRules

![profile_policy_irule](svg/courses/networking/f5-bigip-advanced-irules/02_getting_started_with_irules/profile_policy_irule.svg)

---

## What Only an iRule Can Do

- Arbitrary logic: loops, arithmetic, string parsing
- Read and modify the request or response body
- Keep state across requests with the `table` command
- Correlate events: remember something at `HTTP_REQUEST`, use it at `HTTP_RESPONSE`
- Talk to other systems: `HSL`, `DNS`, sideband connections
- Choose a pool member by any computed value

---

## When to Prefer a Profile or Policy

- Policies compile to native code: faster than `Tcl`
- No scripting skills needed; editable in the `GUI`
- Fully supported by `F5`; iRule logic is your own responsibility
- Rule of thumb: if a policy can express it, use the policy
- Reach for an iRule when the policy runs out of expressiveness

---

## Triggering an iRule

- iRules are assigned to a virtual server as a list
- Traffic on that virtual server fires events in order
- Each iRule with a handler for the event runs its code
- Events only exist if the matching profile is on the virtual server
- One iRule can be shared by many virtual servers

---

## Ordering Multiple iRules

- Every event handler has a `priority`, default `500`
- Lower priority runs first
- Same priority: the order of the list on the virtual server
- `event disable` and `return` affect only the current iRule
- Keep ordering explicit when rules depend on each other

```tcl
when HTTP_REQUEST priority 100 {
    set uri [string tolower [HTTP::uri]]
}
when HTTP_REQUEST priority 900 {
    log local0. "normalized uri: $uri"
}
```

---

## The iRule Lifecycle

![irule_lifecycle](svg/courses/networking/f5-bigip-advanced-irules/02_getting_started_with_irules/irule_lifecycle.svg)

---

## The DevCentral Ecosystem

- `devcentral.f5.com`: the `F5` developer community
- iRules wiki: reference page per event and per command
- `CodeShare`: hundreds of working iRules to adapt
- Q&A forum: most problems have already been asked
- Search the wiki before writing a command from memory

---

## Creating an iRule in the Configuration Utility

1. Local Traffic, iRules, iRule List, Create
1. Give the rule a name and paste the `Tcl` code
1. Click Finished: the rule is parsed and syntax checked
1. Local Traffic, Virtual Servers, pick the server, Resources tab
1. Manage iRules, move the rule to Enabled, order it, Finished

- A syntax error blocks the save and shows the line number
- Runtime errors only appear in the log once traffic arrives

---

## Creating an iRule From tmsh

```bash
tmsh create ltm rule http_to_https {
    when HTTP_REQUEST {
        HTTP::redirect "https://[HTTP::host][HTTP::uri]"
    }
}
tmsh modify ltm virtual vs_web rules { http_to_https }
tmsh list ltm rule http_to_https
tmsh list ltm virtual vs_web rules
tmsh save sys config
```

- The same validation runs on `create` and `modify`
- Use `tmsh load sys config merge file` for many rules at once

---

## Your First iRule: HTTP to HTTPS

- Virtual server on port `80` with an `HTTP` profile
- Redirect everything to the same host and path on `HTTPS`
- `HTTP::redirect` sends a `302` and closes the request
- `[HTTP::host]` and `[HTTP::uri]` are command substitutions

```tcl
when HTTP_REQUEST {
    HTTP::redirect "https://[HTTP::host][HTTP::uri]"
}
```

---

## The Redirect Flow

![redirect_flow](svg/courses/networking/f5-bigip-advanced-irules/02_getting_started_with_irules/redirect_flow.svg)

---

## Testing the First iRule

```bash
curl -i http://www.example.com/login?next=/home
```

```output
HTTP/1.0 302 Found
Location: https://www.example.com/login?next=/home
Server: BigIP
Connection: Keep-Alive
Content-Length: 0
```

- Add a `log local0.` line and watch `tail -f /var/log/ltm`
- Remove the log line before going to production
