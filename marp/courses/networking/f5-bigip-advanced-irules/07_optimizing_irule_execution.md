---
tags:
  - networking:http
  - practices:performance
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

# Optimizing iRule Execution

---

## What This Chapter Covers

- Why efficiency matters in the data plane
- Measuring iRule runtime with timing statistics
- Modularizing iRules and using procedures
- Optimizing logging and high speed logging (`HSL`)
- Data groups, `switch`, and cheap string handling
- Choosing the earliest event that has the data

---

## Every iRule Runs in the Data Plane

- iRules execute inside `TMM`, not on the Linux host
- They run on every request, on every `TMM` instance
- Microseconds per request times millions of requests
- A slow iRule raises latency for every client of the `VS`
- It also burns `CPU` that other virtual servers needed
- Worst case: `CMP` demotion, the `VS` drops to a single `TMM`

---

## Where the Cost Is Paid

![irule_cost_path](svg/courses/networking/f5-bigip-advanced-irules/07_optimizing_irule_execution/irule_cost_path.svg)

---

## The Arithmetic of a Slow iRule

| Per request | At 5,000 req/s | At 50,000 req/s |
|-------------|----------------|-----------------|
| 5 us        | 2.5% of a core | 25% of a core   |
| 50 us       | 25% of a core  | 2.5 cores       |
| 500 us      | 2.5 cores      | 25 cores        |

- A regex that costs 500 microseconds looks harmless in the lab
- In production it is the difference between idle and saturated

---

## Turning On Timing Statistics

- `timing on` collects execution and cycle counters
- Can be set per iRule or per event
- Counters live in memory; read them with `tmsh`

```tcl
timing on
when HTTP_REQUEST {
    if { [HTTP::uri] starts_with "/admin" } {
        HTTP::respond 403 content "forbidden"
        return
    }
}
```

---

## Reading the Counters

```bash
tmsh show ltm rule my_rule
tmsh reset-stats ltm rule my_rule
```

```output
Ltm::Rule Event: my_rule:HTTP_REQUEST
  Priority               500
  Executions
    Total                184213
    Failures             0
    Aborts               0
  CPU Cycles on Executing
    Average              4120
    Maximum              89330
    Minimum              2980
```

---

## From Cycles to Microseconds

- Cycles are `CPU` clock ticks, not time
- Divide by the clock rate to get seconds
- Find the rate in `/proc/cpuinfo` on the host

```bash
grep MHz /proc/cpuinfo | head -1
```

```output
cpu MHz : 2500.000
```

- `4120` cycles at `2.5 GHz` is about `1.6` microseconds
- `89330` cycles is about `36` microseconds: find out why

---

## Interpreting Timing Statistics

![timing_statistics](svg/courses/networking/f5-bigip-advanced-irules/07_optimizing_irule_execution/timing_statistics.svg)

---

## Timing in Production

- Timing itself costs a little on every execution
- Enable it during tuning, disable it when done
- Or keep it on for a few key rules and accept the overhead
- Compare `Average` against `Maximum`: a big gap means a slow branch
- `Failures` and `Aborts` should be zero; they are runtime errors

---

## Custom Counters with ISTATS

- `ISTATS` are user defined statistics kept inside `TMM`
- Cheap to increment, visible from `tmsh`
- Count what matters: blocks, redirects, cache hits

```tcl
when HTTP_REQUEST {
    if { [HTTP::uri] contains "../" } {
        ISTATS::incr "ltm.virtual [virtual name] c blocked" 1
        reject
    }
}
```

```bash
tmsh show ltm virtual vs_web
istats dump
```

---

## Small Rules Beat One Giant Rule

- Several single purpose iRules on the `VS`, not one monolith
- Each rule has one job: redirect, block, log, rewrite
- A rule can be shared by many virtual servers
- Disable one behavior by detaching one rule
- Ordering is explicit through `priority`

---

## Naming and Structure Conventions

- Prefix by purpose: `sec_`, `redir_`, `log_`, `lib_`
- Version and author in a comment header
- One event handler per event per rule
- Keep data in data groups, not in the code
- Keep the rule short enough to read on one screen

```tcl
# sec_block_admin v1.2 - blocks /admin from outside
# owner: security infrastructure team
when HTTP_REQUEST {
    if { [class match [IP::client_addr] equals internal_nets] } {
        return
    }
}
```

---

## Defining a Procedure

- A `proc` is a reusable function defined inside an iRule
- Takes arguments, returns a value
- Lives in the rule that defines it; callers reference that rule

```tcl
proc is_internal { addr } {
    return [class match $addr equals internal_nets]
}
```

---

## Calling a Procedure

- `call rulename::procname args` invokes it from any event
- The library rule need not be attached to the `VS`
- No shared variables unless they are passed as arguments

```tcl
when HTTP_REQUEST {
    if { [call lib_net::is_internal [IP::client_addr]] } {
        return
    }
    HTTP::respond 403 content "forbidden"
}
```

---

## Library iRules

- A rule that contains only procs is a library
- One place to fix a bug that many rules share
- Name them `lib_*` so nobody attaches them by mistake
- A `call` costs a little more than inline code
- Use a proc when logic is shared or long; copy a one liner

---

## Logging Is Not Free

- Every `log` call builds a string and hands it to `syslog-ng`
- `syslog-ng` runs on the host and writes to disk
- Logging on every request can cost more than the rule itself
- `/var/log/ltm` fills, rotates, and slows the box
- Log decisions, not traffic

---

## Guarding Logs with a Debug Flag

- A `static::` variable set once in `RULE_INIT`
- Flip it to `1` while troubleshooting, back to `0` after
- The `if` costs almost nothing; the string building is skipped

```tcl
when RULE_INIT {
    set static::debug 0
}
when HTTP_REQUEST {
    if { $static::debug } {
        log local0. "req [IP::client_addr] [HTTP::uri]"
    }
}
```

---

## Two Ways Out for a Log Line

![logging_paths](svg/courses/networking/f5-bigip-advanced-irules/07_optimizing_irule_execution/logging_paths.svg)

---

## High Speed Logging

- `HSL` sends log messages straight from `TMM` to a remote collector
- No host `syslog-ng`, no local disk, no `/var/log/ltm`
- Transport is `UDP` or `TCP` to a pool of collectors
- Message format is yours: prefix with a syslog priority
- Built for per request logging at line rate

---

## Opening and Sending with HSL

- Open the handle once per connection in `CLIENT_ACCEPTED`
- Reuse it for every request on that connection

```tcl
when CLIENT_ACCEPTED {
    set hsl [HSL::open -proto UDP -pool syslog_pool]
}
when HTTP_REQUEST {
    HSL::send $hsl "<134> [IP::client_addr] [HTTP::method] [HTTP::uri]"
}
```

---

## A Request Logging iRule

```tcl
when CLIENT_ACCEPTED {
    set hsl [HSL::open -proto UDP -pool syslog_pool]
}
when HTTP_REQUEST {
    set start [clock clicks -milliseconds]
    set line "[IP::client_addr] [HTTP::method] [HTTP::host][HTTP::uri]"
}
when HTTP_RESPONSE {
    set ms [expr {[clock clicks -milliseconds] - $start}]
    HSL::send $hsl "<134>web $line [HTTP::status] ${ms}ms"
}
```

- `HSL::open` per request would open a new handle each time
- The `CLIENT_ACCEPTED` handle is amortized over keepalive requests

---

## Data Groups Instead of Long Chains

- A data group is a named lookup table stored outside the rule
- Three types: `address`, `string` and `integer`
- `class match` tests, `class lookup` returns the value
- Change the data without touching the code

```bash
tmsh create ltm data-group internal blocked_paths type string \
    records { /admin { } /setup { } /backup { } }
```

```tcl
if { [class match [HTTP::path] starts_with blocked_paths] } {
    HTTP::respond 403 content "forbidden"
    return
}
```

---

## Lookup Versus Chain

![data_group_vs_chain](svg/courses/networking/f5-bigip-advanced-irules/07_optimizing_irule_execution/datagroup_vs_chain.svg)

---

## Prefer switch and glob Over Regex

- `switch -glob` is a byte comparison, `regexp` compiles a machine
- Most `URI` decisions are prefix, suffix or contains tests
- Save `regexp` for patterns that genuinely need it

```tcl
switch -glob [string tolower [HTTP::path]] {
    "/api/*" { pool api_pool }
    "*.jpg" - "*.png" - "*.css" { pool static_pool }
    default { pool web_pool }
}
```

---

## Avoid Copies and Repeated Work

- Every `set` copies a string into a new variable
- Every `string tolower` walks the whole string
- Call a command once, keep the result, or use it inline once
- Do not `HTTP::collect` a body you never inspect

```tcl
# slow: three copies, three lowercase passes
set u [HTTP::uri]
if { [string tolower $u] starts_with "/a" } { ... }
if { [string tolower $u] starts_with "/b" } { ... }
if { [string tolower $u] starts_with "/c" } { ... }
```

---

## Choose the Earliest Event

- Reject a bad client `IP` in `CLIENT_ACCEPTED`, not `HTTP_REQUEST`
- The `HTTP` parser has not run yet; the connection is dropped cheaply
- Do the header checks before any payload check
- Return as soon as the decision is made

```tcl
when CLIENT_ACCEPTED {
    if { [class match [IP::client_addr] equals blocked_nets] } {
        reject
    }
}
```

---

## Before: A Slow iRule

```tcl
when HTTP_REQUEST {
    set uri [string tolower [HTTP::uri]]
    set ip [IP::client_addr]
    log local0. "request from $ip for $uri"
    if { [regexp {^/admin.*} $uri] } {
        HTTP::respond 403 content "forbidden"
    } elseif { [regexp {^/setup.*} $uri] } {
        HTTP::respond 403 content "forbidden"
    } elseif { [regexp {^/backup.*} $uri] } {
        HTTP::respond 403 content "forbidden"
    }
}
```

---

## After: The Same Rule, Fast

```tcl
when HTTP_REQUEST {
    if { [class match [string tolower [HTTP::path]] \
            starts_with blocked_paths] } {
        ISTATS::incr "ltm.virtual [virtual name] c blocked" 1
        HTTP::respond 403 content "forbidden"
        return
    }
}
```

- No log on every request, no variables, one lowercase pass
- One data group lookup instead of three regex compiles
- A counter instead of a log line

---

## Efficiency Tips and Their Gain

| Tip                                      | Gain            |
|------------------------------------------|-----------------|
| Reject in `CLIENT_ACCEPTED`              | Skips `HTTP` parsing |
| `class match` instead of `if` chains     | Constant time lookup |
| `switch -glob` instead of `regexp`       | No regex compile     |
| Guard `log` with a debug flag            | No string building   |
| `HSL` instead of `log`                   | No host disk `I/O`   |
| `return` after the decision              | Skips the rest       |
