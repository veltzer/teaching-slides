# The Return Code
---
## What is a Return Code?
- Every command that runs produces a return code (exit status)
- It is an integer from 0 to 255
- 0 means **success**
- Any non-zero value means **failure**
- This is the opposite of most programming languages!
---
## Checking the Return Code
```bash
# The special variable $? holds the last return code
ls /tmp
echo $?    # 0 (success)

ls /nonexistent_directory
echo $?    # 2 (failure - no such directory)

# IMPORTANT: $? is overwritten by every command
ls /nonexistent_directory
echo $?    # 2
echo $?    # 0 (the previous echo succeeded!)
```
---
## Common Return Codes
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse of built-in command |
| 126 | Command found but not executable |
| 127 | Command not found |
| 128+N | Killed by signal N |
| 130 | Killed by Ctrl+C (SIGINT = 2, 128+2) |
| 137 | Killed by SIGKILL (128+9) |
| 143 | Killed by SIGTERM (128+15) |
---
## `true` and `false` Commands
```bash
# true always returns 0
true
echo $?    # 0

# false always returns 1
false
echo $?    # 1

# These are actual commands (also built-ins)
type true
# true is a shell builtin

# Useful for infinite loops
while true; do
    echo "forever"
    sleep 1
done
```
---
## Return Codes and `&&` / `||`
```bash
# && (AND): run second only if first succeeds
mkdir /tmp/mydir && echo "Directory created"

# || (OR): run second only if first fails
mkdir /tmp/mydir || echo "Failed to create directory"

# Combine them for if-then-else pattern:
test -f /etc/passwd && echo "exists" || echo "missing"

# WARNING: this pattern is not a true if-else
# If the && command fails, the || also runs!
true && false || echo "this runs unexpectedly"
```
---
## Return Codes in Conditional Context
```bash
# The if statement checks the return code
if grep -q "root" /etc/passwd; then
    echo "root user exists"
fi

# The return code of the LAST command in a pipeline
echo "hello" | grep -q "hello"
echo $?    # 0

echo "hello" | grep -q "world"
echo $?    # 1

# Negation with !
if ! grep -q "nonexistent" /etc/passwd; then
    echo "not found (this is expected)"
fi
```
---
## The `test` Command and `[`
```bash
# test is a command that evaluates expressions
test 5 -gt 3
echo $?    # 0 (true)

test 5 -lt 3
echo $?    # 1 (false)

# [ is an alias for test (literally)
[ 5 -gt 3 ]
echo $?    # 0

# IMPORTANT: spaces are required!
[5 -gt 3]     # WRONG: tries to run command "[5"
[ 5 -gt 3 ]   # RIGHT
```
---
## Return Codes from Scripts
```bash
#!/bin/bash
# A script's return code is the code of its last command

echo "doing stuff"
ls /nonexistent   # returns 2
# Script exits with 2

# Use exit to set an explicit return code
#!/bin/bash
echo "checking..."
if [ ! -f "$1" ]; then
    echo "File not found: $1" >&2
    exit 1
fi
echo "File exists"
exit 0
```
---
## Capturing Return Codes
```bash
# Save it immediately if you need it later
some_command
rc=$?

# Now you can use it multiple times
if [ $rc -ne 0 ]; then
    echo "Command failed with code $rc"
    exit $rc
fi

# Common pattern: check and act
if ! output=$(some_command 2>&1); then
    echo "Failed: $output"
    exit 1
fi
```
---
## `PIPESTATUS` Array
```bash
# $? only gives the return code of the LAST command in a pipe
false | true
echo $?    # 0 (from true, not from false!)

# PIPESTATUS gives you ALL return codes
false | true | false
echo "${PIPESTATUS[0]}"  # 1 (from first false)
echo "${PIPESTATUS[1]}"  # 0 (from true)
echo "${PIPESTATUS[2]}"  # 1 (from second false)

# WARNING: PIPESTATUS is reset by the next command
false | true
echo "${PIPESTATUS[@]}"  # shows PIPESTATUS of echo, not the pipe!

# Save it immediately:
false | true
saved=("${PIPESTATUS[@]}")
```
---
## `set -o pipefail`
```bash
# By default, pipeline return code = last command's code
false | true
echo $?    # 0 (we lost the error!)

# With pipefail, pipeline fails if ANY command fails
set -o pipefail
false | true
echo $?    # 1 (the failure is caught)

# The return code is from the RIGHTMOST failed command
true | false | true | false
echo $?    # 1 (from the last false)
```
