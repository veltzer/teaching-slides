# Process Management
## Understanding and Controlling UNIX Processes

---

## The ps Command

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_08_process_management)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_08_process_management)"/>
  <defs>
    <marker id="arrowd0_08_process_management" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

```txt
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0 225868  9416 ?        Ss   Oct19   0:23 /sbin/init
```

Key fields:

```txt
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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_08_process_management)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_08_process_management)"/>
  <defs>
    <marker id="arrowd1_08_process_management" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="40" width="300" height="70" fill="#f0f0f0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="80" text-anchor="middle" font-size="14">Diagram</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_08_process_management)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_08_process_management)"/>
  <defs>
    <marker id="arrowd3_08_process_management" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Interactive commands:

```txt
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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_08_process_management)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_08_process_management)"/>
  <defs>
    <marker id="arrowd4_08_process_management" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="40" width="300" height="70" fill="#f0f0f0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="80" text-anchor="middle" font-size="14">Diagram</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_08_process_management)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_08_process_management)"/>
  <defs>
    <marker id="arrowd6_08_process_management" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_08_process_management)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_08_process_management)"/>
  <defs>
    <marker id="arrowd7_08_process_management" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Common commands:

```bash
# CPU usage
pidstat -p PID 1

# Memory usage
ps -o pid,rss,command -p PID

# Process tree
pstree -p PID
```
