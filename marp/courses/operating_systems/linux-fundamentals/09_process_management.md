# Process Management
## Understanding and Controlling UNIX Processes

---

## Process States

![process_states](svg/courses/operating_systems/linux-fundamentals/09_process_management/process_states.svg)

---

## The ps Command

![the_ps_command](svg/courses/operating_systems/linux-fundamentals/09_process_management/the_ps_command.svg)

---

## The ps Command

Basic usage:
```bash
# Simple process list
ps
# Full format
ps -f
# All processes (BSD style)
ps aux
# All processes (UNIX style)
ps -ef
# Process tree
ps -ejH
```

---

## PS Output Fields

Example output:

```console
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0 225868  9416 ?        Ss   Oct19   0:23 /sbin/init
```

Key fields:

```misc
USER  - Process owner
PID   - Process ID
%CPU  - CPU usage
%MEM  - Memory usage
VSZ   - Virtual memory size
RSS   - Resident set size
TTY   - Terminal
STAT  - Process state
TIME  - CPU time used
```

---

## Finding Process IDs

![finding_process_ids](svg/courses/operating_systems/linux-fundamentals/09_process_management/finding_process_ids.svg)

---

## Finding Process IDs

Different methods:
```bash
# Using ps and grep
ps aux | grep nginx
# Using pgrep
pgrep nginx
# Using pidof
pidof nginx
# Find parent process
ps -o ppid= -p PID
```

---

## Sending Signals (kill)

![sending_signals_kill](svg/courses/operating_systems/linux-fundamentals/09_process_management/sending_signals_kill.svg)

---

## Sending Signals (kill)

Common signals:
```bash
# Terminate gracefully (SIGTERM)
kill PID
# Force kill (SIGKILL)
kill -9 PID
# Stop process (SIGSTOP)
kill -STOP PID
# Continue process (SIGCONT)
kill -CONT PID
```

---

## Common Signal Numbers

| Signal    | Number | Purpose               |
|-----------|--------|----------------------|
| SIGHUP    | 1      | Hangup              |
| SIGINT    | 2      | Interrupt (Ctrl+C)  |
| SIGQUIT   | 3      | Quit                |
| SIGKILL   | 9      | Force Kill          |
| SIGTERM   | 15     | Terminate           |
| SIGSTOP   | 19     | Stop                |
| SIGCONT   | 18     | Continue            |
| SIGUSR1   | 10     | User defined        |
| SIGUSR2   | 12     | User defined        |

---

## Monitoring with top

![monitoring_with_top](svg/courses/operating_systems/linux-fundamentals/09_process_management/monitoring_with_top.svg)

---

## Monitoring with top

Interactive commands:
```misc
h - help
k - kill process
r - renice process
f - select fields
q - quit
```

---

## Top Display

```bash
top - 14:28:00 up 10 days,  5:27,  1 user,  load average: 0.15, 0.22, 0.25
Tasks: 213 total,   1 running, 212 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.1 us,  1.0 sy,  0.0 ni, 96.8 id,  0.0 wa,  0.0 hi,  0.1 si
MiB Mem :  15881.4 total,   7993.5 free,   4182.0 used,   3705.9 buff/cache
MiB Swap:   2048.0 total,   2048.0 free,      0.0 used.  11699.4 avail Mem
```

Key sections:
- System uptime and load
- Task summary
- CPU states
- Memory usage
- Swap usage

---

## Dealing with Zombies

![dealing_with_zombies](svg/courses/operating_systems/linux-fundamentals/09_process_management/dealing_with_zombies.svg)

---

## Dealing with Zombies

Identifying zombies:
```bash
# Show zombie processes
ps aux | grep 'Z'
# Find zombie parent
ps -o ppid= -p ZOMBIE_PID
# Kill parent to clean up
kill -9 PARENT_PID
```

---

## The Shell and Jobs

![the_shell_and_jobs](svg/courses/operating_systems/linux-fundamentals/09_process_management/the_shell_and_jobs.svg)

---

## The Shell and Jobs

Job control:
```bash
# Start background job
command &
# List jobs
jobs
# Bring to foreground
fg %1
# Send to background
bg %1
```

---

## Process Priorities (nice)

![process_priorities_nice](svg/courses/operating_systems/linux-fundamentals/09_process_management/process_priorities_nice.svg)

---

## Process Priorities (nice)

Managing priorities:
```bash
# Start with priority
nice -n 10 command
# Change priority
renice -n 10 -p PID
# Show priorities
ps -o pid,nice,command
```

---

## Process Resource Limits

```bash
# View limits
ulimit -a

# Set file size limit
ulimit -f 1000

# Set process limit
ulimit -u 100

# Set memory limit
ulimit -m 1000000
```

Example limits:
- Maximum file size
- Maximum process count
- Stack size
- CPU time
- Virtual memory

---

## Practical Process Management

1. Find and monitor specific process:

```bash
# Find PID
pid=$(pgrep nginx)

# Watch process
watch -n 1 "ps -p $pid -o pid,ppid,%cpu,%mem,cmd"
```

1. Resource management:

```bash
# CPU intensive process
nice -n 19 tar -czf backup.tar.gz /data

# Memory monitoring
watch -n 1 'free -m'
```

---

## Process Troubleshooting

![process_troubleshooting](svg/courses/operating_systems/linux-fundamentals/09_process_management/process_troubleshooting.svg)

---

## Process Troubleshooting

Common commands:
```bash
# CPU usage
pidstat -p PID 1
# Memory usage
ps -o pid,rss,command -p PID
# Process tree
pstree -p PID
```
