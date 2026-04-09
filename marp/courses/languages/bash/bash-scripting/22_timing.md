# Timing

---
## The `time` Built-in

```bash
# time measures how long a command takes
time sleep 2
# real    0m2.003s    (wall clock time)
# user    0m0.001s    (CPU time in user mode)
# sys     0m0.001s    (CPU time in kernel mode)

# time a pipeline
time find / -name "*.log" 2>/dev/null | wc -l

# time a block of commands
time {
    sort bigfile.txt > sorted.txt
    uniq sorted.txt > unique.txt
}
```

---
## Understanding `time` Output

```misc
real = Wall clock time (what a stopwatch measures)
user = CPU time in user space (your code)
sys  = CPU time in kernel space (system calls)

Relationships:
- real >= user + sys  (usually, due to I/O waits)
- For CPU-bound: real ≈ user + sys
- For I/O-bound: real >> user + sys
- For parallel: real < user + sys (multi-core)
```

---
## The `/usr/bin/time` Command

```bash
# The external time command has more options
/usr/bin/time -v ls > /dev/null
# Command being timed: "ls"
# ...
# Maximum resident set size (kbytes): 3456
# Major (requiring I/O) page faults: 0
# Voluntary context switches: 2
# ...

# Useful format string
/usr/bin/time -f "Time: %e seconds, Memory: %M KB" ls > /dev/null
# Time: 0.00 seconds, Memory: 3456 KB
```

---
## High-Precision Timing

```bash
# date +%s gives seconds since epoch
start=$(date +%s)
sleep 2
end=$(date +%s)
echo "Elapsed: $((end - start)) seconds"

# date +%s%N gives nanoseconds (Linux only)
start=$(date +%s%N)
some_command
end=$(date +%s%N)
elapsed=$(( (end - start) / 1000000 ))
echo "Elapsed: ${elapsed}ms"

# EPOCHREALTIME (bash 5.0+)
start=$EPOCHREALTIME
some_command
end=$EPOCHREALTIME
echo "Elapsed: $(bc <<< "$end - $start") seconds"
```

---
## Timing Functions

```bash
# Reusable timing wrapper
timer() {
    local start end elapsed_ms
    start=$(date +%s%N)
    "$@"
    local rc=$?
    end=$(date +%s%N)
    elapsed_ms=$(( (end - start) / 1000000 ))
    printf "[TIMER] %s: %dms (exit %d)\n" "$*" "$elapsed_ms" "$rc" >&2
    return $rc
}

# Usage:
timer sleep 1
# [TIMER] sleep 1: 1003ms (exit 0)

timer find /usr -name "*.so" -type f > /dev/null
# [TIMER] find /usr -name *.so -type f: 245ms (exit 0)
```

---
## Benchmarking

```bash
#!/bin/bash

# Run a command N times and calculate average
benchmark() {
    local n=$1
    shift
    local total=0
    local i

    for ((i = 0; i < n; i++)); do
        local start end elapsed
        start=$(date +%s%N)
        "$@" > /dev/null 2>&1
        end=$(date +%s%N)
        elapsed=$(( (end - start) / 1000000 ))
        total=$((total + elapsed))
    done

    local avg=$((total / n))
    echo "Average over $n runs: ${avg}ms"
}

benchmark 10 ls -la /usr/bin
```

---
## `SECONDS` Variable

```bash
# SECONDS counts seconds since shell started
# or since it was assigned

SECONDS=0

# Do some work
sleep 3
echo "Took $SECONDS seconds so far"

# Reset
SECONDS=0
sleep 1
echo "This phase: $SECONDS seconds"

# Useful for script runtime
#!/bin/bash
SECONDS=0
# ... entire script ...
echo "Script completed in $SECONDS seconds"
```

---
## Timeout for Commands

```bash
# timeout kills a command after N seconds
timeout 5 long_running_command

# With signal specification
timeout --signal=KILL 10 command

# Check if it timed out
timeout 2 sleep 10
if [ $? -eq 124 ]; then
    echo "Command timed out"
fi

# In pure bash (no timeout command):
( sleep 5; kill $$ 2>/dev/null ) &
timer_pid=$!
long_command
kill $timer_pid 2>/dev/null
```

---
## Profiling Scripts

```bash
#!/bin/bash
# Add timing to every line with PS4 and xtrace

PS4='+ $(date +%s%N) '
set -x

echo "step 1"
sleep 1
echo "step 2"
sleep 2
echo "step 3"

# Output shows nanosecond timestamps for each line
# You can pipe through a script to compute deltas
```
