---
tags:
  - languages:bash
  - practices:scripting
  - infrastructure:linux
  - practices:automation
level: intermediate
category: language
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops
---
# Handling Errors

---

## Bash Error Handling Strategies

![Bash Error Handling Strategies](svg/courses/languages/bash/bash-scripting/07_handling_errors/error_handling_strategies.svg)

---
## Why Error Handling Matters

```bash
# Without error handling, scripts silently continue
cd /nonexistent/directory
rm -rf *    # This runs in the WRONG directory!

# This is the #1 cause of scripting disasters
# Always handle errors explicitly
```

---
## The `&&` Approach

```bash
# Chain commands with &&
cd /target/directory && rm -rf temp/

# If cd fails, rm never runs
# Simple and effective for short chains

# Longer chains get hard to read
mkdir -p /tmp/build && \
    cd /tmp/build && \
    cmake .. && \
    make && \
    make install
```

---
## The `||` Approach

```bash
# Handle the error case
cd /target/directory || exit 1

# With a message
cd /target/directory || { echo "cd failed" >&2; exit 1; }

# Common pattern: provide a default
config_file="${1:-/etc/myapp.conf}"
source "$config_file" || {
    echo "Cannot read config: $config_file" >&2
    exit 1
}
```

---
## `set -e` (errexit)

```bash
#!/bin/bash
set -e

# Now the script exits on ANY command failure
echo "Step 1"
false           # script exits here with code 1
echo "Step 2"   # never reached
```

---
## `set -e` Gotchas

```bash
set -e

# These do NOT trigger errexit:
false || true        # || suppresses it
false && true        # && suppresses it
if false; then       # conditionals suppress it
    echo "no"
fi

# This DOES trigger errexit:
false                # bare command with non-zero exit

# Subshell failures:
x=$(false)           # triggers errexit in bash 4.4+
```

---
## `set -e` in Practice

```bash
#!/bin/bash
set -e

# Problem: you can't check return codes anymore
set -e
some_command
rc=$?              # never reached if some_command fails!

# Solution: use || true to suppress for one command
some_command || true
# Or capture it explicitly:
if some_command; then
    echo "succeeded"
else
    echo "failed, but script continues"
fi
```

---
## `set -u` (nounset)

```bash
#!/bin/bash
set -u

# Exit on use of undefined variables
echo "$undefined_var"
# bash: undefined_var: unbound variable

# This catches typos:
filename="data.txt"
echo "$filname"     # TYPO! Script exits with error

# Use defaults to work around it:
echo "${optional_var:-default}"   # OK with set -u
```

---
## `set -o pipefail`

```bash
#!/bin/bash
set -o pipefail

# Without pipefail:
false | true
echo $?    # 0 (error from false is hidden)

# With pipefail:
false | true
echo $?    # 1 (error from false is caught)

# Real-world example:
curl -s "$url" | jq '.data'
# Without pipefail: if curl fails, jq gets empty input
# and you might not notice the error
```

---
## The Strict Mode

```bash
#!/bin/bash
set -euo pipefail

# This is the recommended starting point for all scripts
# -e : exit on error
# -u : exit on undefined variable
# -o pipefail : catch errors in pipes

# Some people also add:
IFS=$'\n\t'
# Removes space from IFS to make word splitting safer
```

---
## Trapping Errors

```bash
#!/bin/bash
set -euo pipefail

# Run a function when an error occurs
trap 'echo "Error on line $LINENO" >&2' ERR

echo "Step 1"
false           # triggers the trap, then exits
echo "Step 2"   # never reached
```

---
## Cleanup with `trap`

```bash
#!/bin/bash

# Create a temporary file
tmpfile=$(mktemp)

# Ensure cleanup on exit (normal or error)
trap 'rm -f "$tmpfile"' EXIT

# Also handle specific signals
trap 'echo "Interrupted!" >&2; exit 130' INT TERM

# Use the temp file safely
echo "data" > "$tmpfile"
process "$tmpfile"
# tmpfile is automatically removed when script exits
```

---
## Comprehensive Error Handling Pattern

```bash
#!/bin/bash
set -euo pipefail

readonly SCRIPT_NAME="$(basename "$0")"
readonly LOG_FILE="/tmp/${SCRIPT_NAME}.log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"; }
die() { echo "${SCRIPT_NAME}: ERROR: $*" >&2; exit 1; }

cleanup() {
    local exit_code=$?
    rm -f "$tmpfile"
    [ $exit_code -ne 0 ] && log "Failed with code $exit_code"
    exit $exit_code
}
trap cleanup EXIT

tmpfile=$(mktemp) || die "Cannot create temp file"

log "Starting..."
# ... rest of script ...
```

---
## Retry Pattern

```bash
#!/bin/bash

retry() {
    local max_attempts=$1
    shift
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if "$@"; then
            return 0
        fi
        echo "Attempt $attempt/$max_attempts failed" >&2
        attempt=$((attempt + 1))
        sleep $((attempt * 2))
    done
    return 1
}

# Usage:
retry 3 curl -s -o /dev/null "https://example.com"
```

---
## Error Handling: Common Mistakes

```bash
# MISTAKE 1: Not quoting variables
file="my file.txt"
rm $file         # removes "my" and "file.txt" separately!
rm "$file"       # correct

# MISTAKE 2: Ignoring cd failures
cd "$dir"
rm -rf *         # if cd failed, this runs in wrong directory!
cd "$dir" || exit 1

# MISTAKE 3: Not checking command substitution
result=$(failing_command)     # with set -e, exits
result=$(failing_command) || true  # captures empty string
```
