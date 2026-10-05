---
tags:
  - networking:http
  - architecture:load-balancing
  - security:tls
  - practices:sysadmin
level: beginner
category: networking
audience:
  - audiences:network-engineers
  - audiences:sysadmins
  - audiences:devops

---

# Customizing Application Delivery with Local Traffic Policies

---

## What This Chapter Covers

- What local traffic policies are and what problems they solve
- Where policies fit next to profiles and iRules
- Draft and published policies
- Rules: conditions, actions and rule ordering
- Matching strategies: first match, best match, all match
- Common use cases: `HTTP` to `HTTPS` redirection, `URI` based pool selection, header insertion
- Viewing, testing and troubleshooting policies

---

## Why Customize Traffic at All

- A virtual server with a pool sends every request to the same place
- Real applications need decisions per request
    - `/api` goes to the application servers, `/static` to the file servers
    - Plain `HTTP` must be redirected to `HTTPS`
    - The servers need to know the original client and protocol
- `BIG-IP` sees the full request on the client side, so it can decide
- The question is how to express the decision

---

## Three Ways to Express Behavior

![policy_spectrum](svg/courses/networking/f5-bigip-fundamentals/08_customizing_application_delivery_with_local_traffic_policies/policy_spectrum.svg)

---

## What a Local Traffic Policy Is

- A named, ordered list of rules attached to a virtual server
- Each rule: a set of conditions and a set of actions
- If the conditions match, the actions run
- Built in the `GUI` under Local Traffic > Policies, or with `tmsh create ltm policy`
- Runs inside `TMM` at native speed, no script interpreter
- Available in every `LTM` license, no extra module needed

---

## Policies, Profiles and iRules Compared

| Aspect | Profile | Local traffic policy | iRule |
| --- | --- | --- | --- |
| Model | Settings | Condition and action rules | `Tcl` code |
| Per request decisions | No | Yes | Yes |
| Skills needed | Admin | Admin | Developer |
| Performance | Fastest | Fast, compiled | Slower, interpreted |
| Validation | Built in | Built in | Runtime errors possible |
| Flexibility | Low | Medium | Unlimited |

---

## When to Choose a Policy

- The decision is "if this request looks like X, do Y"
- X is a host, path, header, cookie, method, client address or `TLS` property
- Y is pick a pool, redirect, reject, add or remove a header, toggle compression
- You want any administrator to read and change it safely
- Choose an iRule when you need variables across events, loops, payload rewriting or calculations
- Rule of thumb: start with a policy, move to an iRule only when the policy cannot express it

---

## Policies Depend on Profiles

- A policy can only inspect what a profile has parsed
- `HTTP` conditions need an `HTTP` profile on the virtual server
- `TLS` conditions (`SNI`, cipher) need a client `SSL` profile
- The policy declares this with `requires`, for example `requires { http }`
- The policy also declares which features it `controls`, for example `forwarding`
- Attaching a policy whose requirements are missing fails with a validation error

---

## Requires and Controls

| Setting | Common values | Meaning |
| --- | --- | --- |
| `requires` | `http` | Policy reads `HTTP` data |
| `requires` | `tcp` | Policy reads addresses and ports only |
| `requires` | `client-ssl` | Policy reads `TLS` handshake data |
| `controls` | `forwarding` | Policy may choose pool, node or reject |
| `controls` | `compression`, `caching` | Policy may toggle these features |
| `controls` | `persistence`, `server-ssl` | Policy may change persistence or server `SSL` |

- Recent versions fill these in automatically from the rules you write

---

## Draft and Published Policies

![draft_publish_lifecycle](svg/courses/networking/f5-bigip-fundamentals/08_customizing_application_delivery_with_local_traffic_policies/draft_publish_lifecycle.svg)

---

## Working With Drafts

- New policies start as drafts in the `Drafts` folder of the partition
- A draft can be edited freely but cannot be attached to a virtual server
- Publishing replaces the published version atomically
- Every virtual server using the policy gets the new version immediately
- To change a published policy, create a draft from it, edit, publish again
- Drafts let you prepare a change in working hours and publish in the window

```bash
tmsh create ltm policy Drafts/uri_routing strategy first-match
tmsh publish ltm policy Drafts/uri_routing
tmsh modify ltm policy uri_routing create-draft
```

---

## Anatomy of a Rule

- Name, unique inside the policy
- Ordinal: the position of the rule in the evaluation order
- Conditions: zero or more tests, all must be true (logical `AND`)
- Actions: one or more things to do when the conditions match
- A rule with no conditions always matches: use it as the default rule
- For an `OR`, list several values in one condition or write two rules

---

## Conditions

| Operand | Example selector | Typical test |
| --- | --- | --- |
| `http-host` | `host` | equals `shop.example.com` |
| `http-uri` | `path`, `extension`, `query-string` | starts with `/api/` |
| `http-header` | `name User-Agent` | contains `Mobile` |
| `http-cookie` | `name session` | exists |
| `http-method` | `method` | equals `POST` |
| `tcp` | `address`, `port` | client address in `10.0.0.0/8` |

---

## Condition Options

- Comparison: `equals`, `starts-with`, `ends-with`, `contains`, plus `not` to negate
- Case: `case-insensitive` (default for most `HTTP` operands) or `case-sensitive`
- Several values in one condition are an `OR`: `values { /api/ /v2/ }`
- Event: when the condition is evaluated, `request` (default) or `response`
- `TLS` conditions such as `ssl-extension server-name` are evaluated at the client hello
- Prefer `starts-with` on the path to `contains` on the full `URI`: more precise and cheaper

---

## Actions

| Action | tmsh form | Effect |
| --- | --- | --- |
| Forward | `forward select pool api_pool` | Choose a pool, node or virtual server |
| Reject | `forward reset` | Reset the connection |
| Redirect | `http-reply redirect location ...` | Send a `302` to the client |
| Header | `http-header insert name ... value ...` | Insert, replace or remove a header |
| `URI` | `http-uri replace path ...` | Rewrite the path before forwarding |
| Compression | `compress disable` | Toggle compression for this request |
| Log | `log write facility local0 message ...` | Write a line to the `LTM` log |

---

## Dynamic Values in Actions

- Action values can be `Tcl` expressions, prefixed with `tcl:`
- Read request data with iRule commands, no full iRule needed
- Typical use: build a redirect from the original host and `URI`
- Keep expressions short: anything longer belongs in an iRule

```tcl
tcl:https://[HTTP::host][HTTP::uri]
tcl:[IP::client_addr]
```

---

## Matching Strategies

![rule_matching_strategies](svg/courses/networking/f5-bigip-fundamentals/08_customizing_application_delivery_with_local_traffic_policies/rule_matching_strategies.svg)

---

## Choosing a Strategy

| Strategy | Rules executed | Use when |
| --- | --- | --- |
| `first-match` | The first matching rule, by ordinal | Routing decisions with a clear priority |
| `all-match` | Every matching rule, in order | Independent actions, such as several header changes |
| `best-match` | The most specific matching rule | Many overlapping rules, order should not matter |

- `first-match` is the most common and the easiest to reason about
- With `all-match`, two rules that both forward: the last one wins
- The strategy is a property of the whole policy, not of a rule

---

## Rule Ordering

- Rules are evaluated in ordinal order, lowest first
- Put the most specific rules first and the catch all rule last
- In the `GUI`, drag rules in the policy rules list to reorder
- In `tmsh`, set the `ordinal` of each rule
- A catch all rule placed first with `first-match` hides every rule after it
- Review ordering every time a rule is added

---

## Building a Policy in tmsh

```bash
tmsh create ltm policy Drafts/uri_routing \
    strategy first-match requires add { http } controls add { forwarding } \
    rules add {
        api {
            ordinal 1
            conditions add { 0 { http-uri path starts-with values { /api/ } } }
            actions add { 0 { forward select pool api_pool } }
        }
        static {
            ordinal 2
            conditions add { 0 { http-uri path starts-with values { /static/ } } }
            actions add { 0 { forward select pool static_pool } }
        }
    }
tmsh publish ltm policy Drafts/uri_routing
```

---

## Attaching the Policy

- A virtual server can have several policies
- Each policy must control different features, for example one for forwarding, one for compression
- Policies are evaluated before the iRules attached to the same virtual server
- The virtual server default pool still applies when no forwarding rule matches

```bash
tmsh modify ltm virtual vs_web policies add { uri_routing }
tmsh list ltm virtual vs_web policies
```

---

## URI Based Pool Selection

![uri_pool_selection](svg/courses/networking/f5-bigip-fundamentals/08_customizing_application_delivery_with_local_traffic_policies/uri_pool_selection.svg)

---

## HTTP to HTTPS Redirection

- An `HTTP` virtual server on port 80 with no pool, only a redirect rule
- One rule, no conditions, one `http-reply` action
- Alternative: the built in `_sys_https_redirect` iRule does the same

```bash
tmsh create ltm policy Drafts/https_redirect \
    strategy first-match requires add { http } controls add { forwarding } \
    rules add { redirect {
        actions add { 0 { http-reply redirect \
            location "tcl:https://[HTTP::host][HTTP::uri]" } }
    } }
tmsh publish ltm policy Drafts/https_redirect
tmsh create ltm virtual vs_web_80 destination 10.1.10.100:80 \
    profiles add { http } policies add { https_redirect }
```

---

## Inserting Headers

- After `SSL` offload and `SNAT`, the server sees neither the client address nor the protocol
- Insert headers so the application can log and build correct links
- Use `all-match` or a single rule with several actions

```bash
tmsh create ltm policy Drafts/add_headers \
    strategy all-match requires add { http } \
    rules add { client_info {
        actions add {
            0 { http-header insert name X-Forwarded-For value "tcl:[IP::client_addr]" }
            1 { http-header insert name X-Forwarded-Proto value https }
        }
    } }
```

---

## Other Common Use Cases

- Block an administrative path from outside: `http-uri path starts-with /admin` and client address not internal, then `forward reset`
- Send mobile clients to a separate pool by `User-Agent`
- Host based routing: one virtual server, one pool per `http-host`
- Disable compression for already compressed content types
- Route by `SNI` server name to different pools on one `HTTPS` virtual server
- Maintenance page: redirect everything while the pool is drained

---

## Verifying and Troubleshooting

- Check that the virtual server has the needed profiles: `requires` errors show at attach time
- Test each rule with `curl` and watch which pool member answers
- Add a temporary `log` action to see which rule matched
- Look at policy statistics for rule match counts

```bash
curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' http://10.1.10.100/
curl -s http://10.1.10.100/api/health
tmsh show ltm policy uri_routing
tail -f /var/log/ltm
```

---

## Common Mistakes

- Editing the policy but forgetting to publish the draft
- Catch all rule at ordinal 1 with `first-match`
- Path condition without the leading slash or with the wrong case option
- Two policies on one virtual server that both control `forwarding`
- Expecting a policy to see the `HTTP` request on a virtual server without an `HTTP` profile
- Building a long `tcl:` expression instead of writing a proper iRule

---

## Lab: Local Traffic Policies

1. Create pools `api_pool` (`10.1.20.11:8080`) and `static_pool` (`10.1.20.12:80`)
1. Build the draft policy `uri_routing` with `first-match` and two rules
1. Publish it and attach it to `vs_web`; verify with `curl` which member answers each path
1. Create `vs_web_80` with the `https_redirect` policy and test the `302`
1. Add an `all-match` header policy and confirm the headers in the server access log
1. Create a draft of `uri_routing`, add a rule for `/admin`, publish and retest

---

## Key Takeaways

- Local traffic policies express "if request matches, do action" without code
- They need profiles for what they inspect and declare it with `requires`
- Edit in drafts, publish to apply atomically to every virtual server
- Pick the matching strategy deliberately and order rules from specific to general
- Use policies first, iRules when the logic outgrows conditions and actions
