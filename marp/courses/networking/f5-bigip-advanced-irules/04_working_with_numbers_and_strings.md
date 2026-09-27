---
tags:
  - networking:http
  - practices:scripting
  - practices:performance
level: advanced
category: networking
audience:
  - audiences:security-engineers
  - audiences:network-engineers
  - audiences:devops
  - audiences:sysadmins

---

# Working with Numbers and Strings

---

## What This Chapter Covers

- Number forms and the "everything is a string" rule
- Arithmetic and comparison with `expr`
- Whitespace, special symbols and quoting
- The `string` and `scan` commands
- Combining strings and iRule parsing commands
- Glob versus regular expressions and their cost
- Working with lists

---

## Everything Is a String

- `Tcl` has one data type: the string
- A "number" is a string that `expr` can parse
- `set port 80` stores the two characters `8` and `0`
- Conversion happens when a command needs a number
- `HTTP::header Content-Length` returns a string too

```tcl
set len [HTTP::header "Content-Length"]
# "1048576" - still a string
set big [expr { $len > 1048576 }]
# now parsed as an integer, result is 1 or 0
```

---

## Number Forms and Notation

- Decimal: `42`, `-7`
- Hexadecimal with a `0x` prefix: `0xff` is `255`
- Floats: `3.14`, `1e6`, `2.5e-3`
- Leading zeros are dangerous: `010` may be read as octal
- `expr { "08" + 1 }` fails: `8` is not an octal digit

```tcl
set a 0xff
log local0. [expr { $a + 1 }]    ;# 256
set day "08"
log local0. [expr { [string trimleft $day 0] + 1 }]  ;# 9
```

---

## Arithmetic with expr

- `expr` evaluates an arithmetic or logical expression
- Always wrap the expression in braces
- Integer division truncates, one float operand gives a float
- `incr` adds to a variable in place and is cheaper

```tcl
set n [expr { $a + 1 }]
set avg [expr { $total / $count }]      ;# integer result
set avg [expr { double($total) / $count }]
incr requests
incr requests -1
```

---

## Why Always Brace expr

- Unbraced `expr $x + 1` substitutes first, then parses
- A `$x` that contains spaces or `[` becomes code
- Braced expressions are compiled once and run faster
- Client controlled values reach `expr` all the time

```tcl
# DANGEROUS: value substituted before evaluation
set n [expr [HTTP::header "X-Count"] + 1]

# SAFE: parsed as one expression, then evaluated
set n [expr { [HTTP::header "X-Count"] + 1 }]
```

---

## Comparison Returns 1 or 0

- `==`, `!=`, `<`, `<=`, `>`, `>=` compare numbers
- `eq` and `ne` compare as strings
- `&&`, `||` and `!` combine conditions
- The result is `1` or `0`, which `if` accepts directly

```tcl
if { [HTTP::header "Content-Length"] > 1048576 } {
    HTTP::respond 413 content "Too large"
    return
}
if { [HTTP::method] eq "POST" && [HTTP::uri] starts_with "/api" } {
    pool api_pool
}
```

---

## Whitespace Separates Words

- A command is a list of words separated by whitespace
- Newline or `;` ends a command
- A trailing `\` continues the command on the next line
- Extra spaces inside braces and quotes are kept as data

```tcl
set msg "hello world"          ;# two words after set
log local0. $msg ; log local0. "done"
HTTP::respond 200 content "ok" \
    "Content-Type" "text/plain"
```

---

## Special Symbols

| Symbol | Meaning |
|--------|---------|
| `$` | variable substitution |
| `[ ]` | command substitution |
| `{ }` | group without substitution |
| `" "` | group with substitution |
| `#` | comment, only at the start of a command |
| `\` | escape the next character or continue a line |

---

## Quoting Rules

![quoting_rules](svg/courses/networking/f5-bigip-advanced-irules/04_working_with_numbers_and_strings/quoting_rules.svg)

---

## Grouping with Braces

- Braces group text literally, nothing is substituted
- Used for `if` conditions, loop bodies and `expr`
- Braces nest, so `{a {b c}}` is one word
- Substitution happens later, when the body runs

```tcl
set host {[HTTP::host]}   ;# the literal text, not the host
if { [HTTP::uri] starts_with "/admin" } {
    log local0. "admin: [IP::client_addr]"
}
```

---

## Grouping with Double Quotes

- Quotes group text and substitute `$var` and `[cmd]`
- Needed to build messages, redirects and header values
- Escape a literal quote or bracket with `\`
- A `"` inside a header value must be escaped or the word ends early

```tcl
set target "https://[HTTP::host][HTTP::uri]"
log local0. "client [IP::client_addr] asked for $target"
HTTP::header insert "X-Note" "said \"hi\" at [clock seconds]"
```

---

## Common Quoting Bugs

- `if $x == 1` with a `$x` of `a b` becomes three words
- Unbraced `expr` with a `URI` containing `$` tries to substitute
- A `#` in the middle of a line is not a comment
- A stray `}` inside quotes still closes the brace

```tcl
# BROKEN: URI "/a b" makes the if see extra words
if [HTTP::uri] equals "/a b" { pool p }
# FIXED
if { [HTTP::uri] equals "/a b" } { pool p }
```

---

## The string Command

- One command with many subcommands
- Case: `tolower`, `toupper`
- Shape: `length`, `trim`, `trimleft`, `trimright`, `range`
- Search: `first`, `last`, `match`, `equal`
- Rewrite: `map`, `repeat`

```tcl
set host [string tolower [HTTP::host]]
set len [string length [HTTP::uri]]
set clean [string trim [HTTP::header "X-Id"]]
set ext [string range [HTTP::path] end-3 end]
```

---

## string first, last, map, is

- `string first needle haystack` returns an index or `-1`
- `string last` searches from the end
- `string map` replaces many substrings in one pass
- `string is integer -strict` validates before `expr`

```tcl
set idx [string first "?" [HTTP::uri]]
set uri [string map { "//" "/" ".." "" } [HTTP::uri]]
if { ![string is integer -strict [HTTP::header "X-Id"]] } {
    HTTP::respond 400 content "bad id"
    return
}
```

---

## Parsing with scan

- `scan` reads formatted input into variables
- `%d` integers, `%s` words, `%x` hex, `%c` a character
- Returns the number of conversions that succeeded
- Ideal for `IP` addresses and version strings

```tcl
scan [IP::client_addr] "%d.%d.%d.%d" a b c d
if { $a == 10 } { log local0. "private net" }

scan [HTTP::version] "%d.%d" major minor
if { $major < 1 || ($major == 1 && $minor < 1) } { reject }
```

---

## Combining Strings

- Juxtaposition: `"$a$b"` or `"$host:$port"`
- `append var s1 s2` extends in place
- `concat` joins with single spaces and trims
- `join list sep` joins list elements with a separator

```tcl
set url "https://[HTTP::host][HTTP::uri]"
set msg "client "
append msg [IP::client_addr] " uri " [HTTP::uri]
set line [concat $a $b]           ;# "a b"
set path [join [list "api" "v2" "users"] "/"]
```

---

## Why append Beats Repeated set

- `set s "$s more"` copies the whole string every time
- `append` grows the existing value in place
- Inside a loop the difference is quadratic versus linear
- The same holds for `lappend` on lists

```tcl
# slow: one full copy per iteration
foreach h [HTTP::header names] { set out "$out $h" }

# fast: grows in place
foreach h [HTTP::header names] { append out " " $h }
```

---

## iRule String Parsing Commands

- `findstr string search offset terminator`
- `getfield string separator index`
- `substr string offset length_or_terminator`
- `TMM` native, cheaper than a regular expression
- Return an empty string when nothing matches

```tcl
set uri "/app/v2/users?id=42&lang=en"
findstr $uri "id=" 3 "&"          ;# 42
getfield $uri "/" 3               ;# v2
substr $uri 0 "?"                 ;# /app/v2/users
```

---

## Parsing a URI

![uri_parsing](svg/courses/networking/f5-bigip-advanced-irules/04_working_with_numbers_and_strings/uri_parsing.svg)

---

## findstr in Detail

- Finds `search` inside `string`
- `offset` skips that many characters past the match
- `terminator` is a string or a length that ends the result
- Without a terminator it returns the rest of the string

```tcl
set auth [HTTP::header "Authorization"]
# "Bearer eyJhbGciOi..."
set token [findstr $auth "Bearer " 7]
# session id from a cookie header, ends at ";"
set sid [findstr [HTTP::header "Cookie"] "sid=" 4 ";"]
```

---

## getfield and substr in Detail

- `getfield` splits on a separator and returns field `n` (1 based)
- Leading separators produce an empty first field
- `substr` cuts from an offset up to a length or terminator
- Both are simpler than `split` plus `lindex` for one field

```tcl
set path [HTTP::path]            ;# /app/v2/users
getfield $path "/" 2             ;# app
getfield $path "/" 3             ;# v2
substr $path 5                   ;# v2/users
substr $path 5 "/"               ;# v2
```

---

## Parsing Commands Compared

| Command | Selects by | Best for |
|---------|-----------|----------|
| `findstr` | search string plus terminator | a value after a key |
| `getfield` | separator and field number | one field of a delimited path |
| `substr` | offset and length or terminator | a fixed position slice |
| `string range` | start and end index | when you know both indexes |

---

## Glob Patterns

- `*` any run of characters, `?` one character, `[abc]` a set
- `string match`, `matches_glob` and `switch -glob` use glob
- Cheap: a single pass, no backtracking
- Covers most `URI` and host routing needs

```tcl
switch -glob [string tolower [HTTP::uri]] {
    "/images/*" { pool static_pool }
    "*.php"     { pool php_pool }
    "/api/v[12]/*" { pool api_pool }
    default     { pool default_pool }
}
```

---

## Regular Expressions

- `regexp` tests and captures, `regsub` rewrites
- `matches_regex` inside conditions
- Anchor with `^` and `$` to avoid scanning the whole string
- Justified when the shape is irregular or you need captures

```tcl
if { [regexp {^/user/(\d+)/profile$} [HTTP::path] -> uid] } {
    HTTP::header insert "X-User-Id" $uid
}
set new [regsub -all {/+} [HTTP::uri] "/"]
```

---

## The Cost of Matching

![matching_cost](svg/courses/networking/f5-bigip-advanced-irules/04_working_with_numbers_and_strings/matching_cost.svg)

---

## Choosing a Matching Method

- `equals`, `starts_with`, `ends_with`, `contains`: cheapest
- `switch` with exact strings: one jump, many cases
- Glob: wildcards without backtracking
- Regex: last resort, always anchored, never in a loop
- Measure with `timing on` before and after a rewrite

---

## Working with Lists

- `split` turns a string into a list, `join` reverses it
- `lindex`, `llength`, `lrange` read a list
- `lappend`, `lsearch`, `lsort` build and query it
- `foreach` walks the elements

```tcl
set parts [split [HTTP::uri] "/"]
set first [lindex $parts 1]       ;# element 0 is empty
set depth [llength $parts]
foreach seg $parts {
    if { $seg equals ".." } { reject }
}
```

---

## Lists from Headers

- `HTTP::header names` returns a list of header names
- `HTTP::header values X-Forwarded-For` returns all values
- A single `X-Forwarded-For` value is a comma separated list
- Split it, trim each element, then trust only the last hop

```tcl
set xff [HTTP::header "X-Forwarded-For"]
set hops [split $xff ","]
set client [string trim [lindex $hops 0]]
set last [string trim [lindex $hops end]]
if { [lsearch -exact [HTTP::header names] "X-Debug"] >= 0 } {
    HTTP::header remove "X-Debug"
}
```

---

## Key Takeaways

- Every value is a string until `expr` or `scan` reads it
- Brace every `expr` and every `if` condition
- Prefer `string`, `findstr`, `getfield` and `substr` over regex
- Use `append` and `lappend` to grow values
- Reach for `switch -glob` before `regexp`
