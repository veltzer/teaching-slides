# Multi Processing
---
## Running Commands in the Background

```bash
# & runs a command in the background
sleep 10 &
echo "PID of background job: $!"

# The shell immediately gives you the prompt back
# The background job runs concurrently

# List background jobs
jobs
# [1]+  Running  sleep 10 &

# Bring to foreground
fg %1

# Send to background (after Ctrl+Z)
bg %1
```
---
## `$!` - Last Background PID

```bash
# $! holds the PID of the most recent background command
command1 &
pid1=$!

command2 &
pid2=$!

echo "Started: $pid1 and $pid2"
```
---
## `wait` - Waiting for Background Jobs

```bash
# Wait for a specific process
sleep 5 &
pid=$!
echo "Waiting for $pid..."
wait $pid
echo "Process $pid finished with code $?"

# Wait for ALL background jobs
job1 &
job2 &
job3 &
wait    # waits for all three
echo "All jobs finished"
```
---
## Collecting Return Codes

```bash
#!/bin/bash

# Run multiple jobs and collect return codes
pids=()

./task1.sh &
pids+=($!)

./task2.sh &
pids+=($!)

./task3.sh &
pids+=($!)

# Wait for each and check result
failed=0
for pid in "${pids[@]}"; do
    if ! wait "$pid"; then
        echo "Process $pid failed" >&2
        failed=$((failed + 1))
    fi
done

echo "$failed job(s) failed"
exit $((failed > 0 ? 1 : 0))
```
---
## Parallel Execution with Return Codes

```bash
#!/bin/bash
set -uo pipefail

# Run tasks in parallel, fail if any fail
declare -A task_pids

for host in web1 web2 web3 db1 db2; do
    ssh "$host" "sudo systemctl restart myapp" &
    task_pids[$host]=$!
done

errors=0
for host in "${!task_pids[@]}"; do
    pid=${task_pids[$host]}
    if wait "$pid"; then
        echo "OK: $host"
    else
        echo "FAILED: $host (exit code: $?)" >&2
        errors=$((errors + 1))
    fi
done

[[ $errors -gt 0 ]] && exit 1
```
---
## Subshells

```bash
# Parentheses create a subshell
(cd /tmp && ls)
pwd    # still in original directory

# Subshells inherit:
# - All variables (shell and environment)
# - Functions
# - File descriptors
# - Current directory
# - umask, traps

# Subshells do NOT propagate changes back:
x=1
(x=2; echo "inside: $x")    # inside: 2
echo "outside: $x"           # outside: 1
```
---
## Process Substitution for Parallel Execution

```bash
# Run commands in parallel and diff their output
diff <(ssh web1 cat /etc/config) <(ssh web2 cat /etc/config)

# Parallel download and processing
paste <(curl -s "$url1") <(curl -s "$url2") > combined.txt

# Tee into multiple processes
cat data.txt | tee >(gzip > data.gz) >(wc -l > count.txt) > /dev/null
```
---
## Job Control

```bash
# Ctrl+Z suspends the current foreground job
# bg resumes it in the background
# fg brings a background job to the foreground

# List all jobs
jobs -l    # with PIDs

# Kill a job
kill %1        # by job number
kill $pid      # by PID
kill -9 $pid   # force kill (SIGKILL)

# Wait for specific job
wait %1
```
---
## `xargs -P` for Parallel Execution

```bash
# Process files in parallel (4 at a time)
find . -name "*.jpg" -print0 | xargs -0 -P 4 -I {} convert {} -resize 800x600 {}.resized

# Parallel HTTP requests
cat urls.txt | xargs -P 10 -I {} curl -s -o /dev/null -w "%{url_effective}: %{http_code}\n" {}

# Parallel compression
find /logs -name "*.log" -print0 | xargs -0 -P $(nproc) gzip
```
---
## GNU `parallel`

```bash
# More powerful than xargs -P
# Install: apt install parallel

# Basic parallel execution
parallel echo ::: A B C D
# A B C D (in parallel)

# Process files
parallel gzip ::: *.log

# With progress bar
parallel --bar gzip ::: *.log

# Remote execution
parallel -S web1,web2,web3 uptime
```
---
## Signals

```bash
# Common signals:
# SIGHUP  (1)  - Terminal closed
# SIGINT  (2)  - Ctrl+C
# SIGQUIT (3)  - Ctrl+\
# SIGKILL (9)  - Force kill (cannot be caught)
# SIGTERM (15) - Polite termination request
# SIGSTOP (19) - Pause (cannot be caught)
# SIGCONT (18) - Resume

# Send signals
kill -TERM $pid     # polite shutdown
kill -INT $pid      # like Ctrl+C
kill -9 $pid        # force kill (last resort)

# Trap signals
trap 'echo "Caught SIGINT"' INT
trap 'cleanup; exit 0' TERM
```
---
## Day 2 Summary
- Scripts need a shebang, `chmod +x`, and error handling
- Use `set -euo pipefail` as the standard starting point
- `[[` is preferred over `[` in `bash` scripts
- Loops: `while`, `for` (word list and C-style), `until`
- Pipes connect commands and run them concurrently
- Beware: pipe stages run in subshells
- `read` is the primary tool for reading input
- Scripts can redirect their own I/O with `exec`
- Background jobs: `&`, `$!`, `wait`, `jobs`
