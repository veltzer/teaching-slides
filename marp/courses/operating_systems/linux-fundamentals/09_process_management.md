# Process Management
## Understanding and Controlling UNIX Processes

---

## The ps Command

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Process Tree: init to User Processes</text>
  <defs>
    <marker id="arrowps" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="220" y="35" width="160" height="30" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="55" text-anchor="middle" font-size="11" font-weight="bold">init/systemd (PID 1)</text>
  <line x1="260" y1="65" x2="130" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#arrowps)"/>
  <line x1="300" y1="65" x2="300" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#arrowps)"/>
  <line x1="340" y1="65" x2="470" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#arrowps)"/>
  <rect x="50" y="85" width="160" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="130" y="104" text-anchor="middle" font-size="10">sshd (service)</text>
  <rect x="220" y="85" width="160" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="300" y="104" text-anchor="middle" font-size="10">cron (scheduler)</text>
  <rect x="390" y="85" width="160" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="470" y="104" text-anchor="middle" font-size="10">nginx (web server)</text>
  <line x1="100" y1="113" x2="70" y2="133" stroke="#333" stroke-width="1" marker-end="url(#arrowps)"/>
  <line x1="160" y1="113" x2="190" y2="133" stroke="#333" stroke-width="1" marker-end="url(#arrowps)"/>
  <rect x="20" y="133" width="100" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="70" y="150" text-anchor="middle" font-size="9">bash (shell)</text>
  <rect x="140" y="133" width="100" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="190" y="150" text-anchor="middle" font-size="9">bash (shell)</text>
  <line x1="70" y1="158" x2="70" y2="173" stroke="#333" stroke-width="1" marker-end="url(#arrowps)"/>
  <rect x="20" y="173" width="100" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="70" y="188" text-anchor="middle" font-size="9">vim (user cmd)</text>
  <rect x="300" y="148" width="260" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="4" opacity="0.7"/>
  <text x="430" y="163" text-anchor="middle" font-size="10" font-weight="bold">ps shows:</text>
  <text x="430" y="178" text-anchor="middle" font-size="10">PID, PPID, USER, STAT, CMD</text>
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
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Finding Process IDs</text>
  <defs>
    <marker id="arrowpid" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="220" y="35" width="160" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="11" font-weight="bold">Find PID of "nginx"</text>
  <line x1="250" y1="70" x2="100" y2="95" stroke="#333" stroke-width="1.5" marker-end="url(#arrowpid)"/>
  <line x1="300" y1="70" x2="300" y2="95" stroke="#333" stroke-width="1.5" marker-end="url(#arrowpid)"/>
  <line x1="350" y1="70" x2="500" y2="95" stroke="#333" stroke-width="1.5" marker-end="url(#arrowpid)"/>
  <rect x="20" y="95" width="160" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="113" text-anchor="middle" font-size="10" font-weight="bold">ps aux | grep</text>
  <text x="100" y="130" text-anchor="middle" font-size="9">classic, verbose output</text>
  <rect x="220" y="95" width="160" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="113" text-anchor="middle" font-size="10" font-weight="bold">pgrep nginx</text>
  <text x="300" y="130" text-anchor="middle" font-size="9">returns PIDs only</text>
  <rect x="420" y="95" width="160" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="113" text-anchor="middle" font-size="10" font-weight="bold">pidof nginx</text>
  <text x="500" y="130" text-anchor="middle" font-size="9">exact name match</text>
  <rect x="100" y="160" width="400" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="4" opacity="0.6"/>
  <text x="300" y="180" text-anchor="middle" font-size="10">Once you have the PID, use it with kill, top -p, strace, etc.</text>
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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Sending Signals to Processes</text>
  <defs>
    <marker id="arrowsig" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="40" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="65" text-anchor="middle" font-size="11" font-weight="bold">kill PID</text>
  <line x1="150" y1="60" x2="200" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowsig)"/>
  <rect x="200" y="35" width="200" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="55" text-anchor="middle" font-size="10" font-weight="bold">Signal Delivery</text>
  <text x="300" y="72" text-anchor="middle" font-size="10">kernel delivers to process</text>
  <line x1="400" y1="60" x2="440" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowsig)"/>
  <rect x="440" y="40" width="130" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="65" text-anchor="middle" font-size="11" font-weight="bold">Process</text>
  <rect x="30" y="100" width="120" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="90" y="120" text-anchor="middle" font-size="10">SIGTERM (15)</text>
  <text x="90" y="143" text-anchor="middle" font-size="9" fill="#666">graceful stop</text>
  <rect x="170" y="100" width="120" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="230" y="120" text-anchor="middle" font-size="10">SIGKILL (9)</text>
  <text x="230" y="143" text-anchor="middle" font-size="9" fill="#666">force kill</text>
  <rect x="310" y="100" width="120" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="370" y="120" text-anchor="middle" font-size="10">SIGSTOP (19)</text>
  <text x="370" y="143" text-anchor="middle" font-size="9" fill="#666">pause process</text>
  <rect x="450" y="100" width="120" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="510" y="120" text-anchor="middle" font-size="10">SIGCONT (18)</text>
  <text x="510" y="143" text-anchor="middle" font-size="9" fill="#666">resume</text>
  <rect x="30" y="160" width="540" height="28" fill="#ffebee" stroke="#333" stroke-width="1" rx="4" opacity="0.5"/>
  <text x="300" y="179" text-anchor="middle" font-size="10">SIGKILL and SIGSTOP cannot be caught or ignored by the process</text>
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
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">top: Real-Time Process Monitor</text>
  <rect x="30" y="35" width="540" height="145" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="40" y="45" width="520" height="18" fill="#fff3e0" stroke="none" rx="2"/>
  <text x="50" y="58" font-size="9" font-family="monospace">top - 14:28:00 up 10 days, load average: 0.15, 0.22, 0.25</text>
  <rect x="40" y="67" width="520" height="18" fill="#e8f5e9" stroke="none" rx="2"/>
  <text x="50" y="80" font-size="9" font-family="monospace">Tasks: 213 total, 1 running, 212 sleeping, 0 zombie</text>
  <rect x="40" y="89" width="520" height="18" fill="#fff3e0" stroke="none" rx="2"/>
  <text x="50" y="102" font-size="9" font-family="monospace">%Cpu: 2.1 us, 1.0 sy, 96.8 id    Mem: 15881M total, 7993M free</text>
  <line x1="40" y1="112" x2="560" y2="112" stroke="#333" stroke-width="1"/>
  <text x="50" y="126" font-size="9" font-family="monospace" font-weight="bold">  PID USER  %CPU %MEM  COMMAND</text>
  <text x="50" y="142" font-size="9" font-family="monospace"> 1234 root   5.2  2.1  nginx</text>
  <text x="50" y="158" font-size="9" font-family="monospace"> 5678 john   3.1  1.5  python3</text>
  <text x="50" y="174" font-size="9" font-family="monospace"> 9012 mysql  1.8  8.3  mysqld</text>
  <text x="430" y="142" font-size="9" fill="#333">h=help</text>
  <text x="430" y="158" font-size="9" fill="#333">k=kill</text>
  <text x="430" y="174" font-size="9" fill="#333">q=quit</text>
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
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Zombie Process Lifecycle</text>
  <defs>
    <marker id="arrowzomb" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="40" width="110" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="65" text-anchor="middle" font-size="10" font-weight="bold">fork()</text>
  <line x1="140" y1="60" x2="170" y2="60" stroke="#333" stroke-width="1.5" marker-end="url(#arrowzomb)"/>
  <rect x="170" y="40" width="110" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="225" y="55" text-anchor="middle" font-size="10" font-weight="bold">Running</text>
  <text x="225" y="70" text-anchor="middle" font-size="9">(child process)</text>
  <line x1="280" y1="60" x2="310" y2="60" stroke="#333" stroke-width="1.5" marker-end="url(#arrowzomb)"/>
  <rect x="310" y="40" width="110" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="365" y="55" text-anchor="middle" font-size="10" font-weight="bold">Exit</text>
  <text x="365" y="70" text-anchor="middle" font-size="9">(child exits)</text>
  <line x1="420" y1="60" x2="450" y2="60" stroke="#333" stroke-width="1.5" marker-end="url(#arrowzomb)"/>
  <rect x="450" y="40" width="130" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="55" text-anchor="middle" font-size="10" font-weight="bold">Zombie (Z)</text>
  <text x="515" y="70" text-anchor="middle" font-size="9">waiting for wait()</text>
  <line x1="515" y1="80" x2="515" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowzomb)"/>
  <rect x="410" y="100" width="170" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="117" text-anchor="middle" font-size="10" font-weight="bold">Parent calls wait()</text>
  <text x="495" y="128" text-anchor="middle" font-size="9">zombie is reaped</text>
  <rect x="30" y="100" width="350" height="80" fill="#ffebee" stroke="#333" stroke-width="1" rx="5" opacity="0.5"/>
  <text x="205" y="120" text-anchor="middle" font-size="10" font-weight="bold">If parent never calls wait():</text>
  <text x="205" y="138" text-anchor="middle" font-size="10">Zombie stays in process table (STAT = Z)</text>
  <text x="205" y="156" text-anchor="middle" font-size="10">Fix: kill parent, init adopts and reaps</text>
  <text x="205" y="170" text-anchor="middle" font-size="9" font-family="monospace">ps aux | grep Z   # find zombies</text>
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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Shell Job Control</text>
  <defs>
    <marker id="arrowjob" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="220" y="35" width="160" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="58" text-anchor="middle" font-size="11" font-weight="bold">Foreground</text>
  <rect x="220" y="130" width="160" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="153" text-anchor="middle" font-size="11" font-weight="bold">Background</text>
  <rect x="470" y="80" width="110" height="35" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="102" text-anchor="middle" font-size="11" font-weight="bold">Stopped</text>
  <!-- fg to bg -->
  <line x1="280" y1="70" x2="280" y2="128" stroke="#333" stroke-width="1.5" marker-end="url(#arrowjob)"/>
  <text x="240" y="105" font-size="10" fill="#333">Ctrl-Z</text>
  <!-- bg to fg -->
  <line x1="320" y1="128" x2="320" y2="72" stroke="#333" stroke-width="1.5" marker-end="url(#arrowjob)"/>
  <text x="335" y="105" font-size="10" fill="#333">fg %n</text>
  <!-- stopped -->
  <line x1="380" y1="60" x2="470" y2="87" stroke="#333" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowjob)"/>
  <text x="445" y="62" font-size="9" fill="#666">Ctrl-Z</text>
  <line x1="470" y1="107" x2="380" y2="143" stroke="#333" stroke-width="1.5" marker-end="url(#arrowjob)"/>
  <text x="445" y="137" font-size="9" fill="#333">bg %n</text>
  <rect x="30" y="80" width="160" height="55" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="4"/>
  <text x="110" y="97" text-anchor="middle" font-size="10" font-weight="bold">Start in background:</text>
  <text x="110" y="113" text-anchor="middle" font-size="10" font-family="monospace">command &amp;</text>
  <text x="110" y="128" text-anchor="middle" font-size="10" font-family="monospace">jobs  # list all</text>
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
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Process Priority (nice values)</text>
  <rect x="30" y="40" width="540" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="40" y="62" font-size="10" font-weight="bold">-20</text>
  <text x="275" y="62" text-anchor="middle" font-size="10" font-weight="bold">0</text>
  <text x="555" y="62" text-anchor="end" font-size="10" font-weight="bold">+19</text>
  <rect x="30" y="80" width="540" height="15" fill="#fff" stroke="#333" stroke-width="1" rx="3"/>
  <rect x="30" y="80" width="180" height="15" fill="#ffebee" stroke="none" rx="3"/>
  <rect x="210" y="80" width="180" height="15" fill="#fff3e0" stroke="none"/>
  <rect x="390" y="80" width="180" height="15" fill="#e8f5e9" stroke="none" rx="3"/>
  <text x="120" y="91" text-anchor="middle" font-size="8" fill="#333">Higher priority</text>
  <text x="480" y="91" text-anchor="middle" font-size="8" fill="#333">Lower priority</text>
  <text x="120" y="115" text-anchor="middle" font-size="10" fill="#c00">root only</text>
  <text x="300" y="115" text-anchor="middle" font-size="10">default</text>
  <text x="480" y="115" text-anchor="middle" font-size="10" fill="#090">any user</text>
  <rect x="30" y="135" width="260" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="4"/>
  <text x="160" y="153" text-anchor="middle" font-size="10" font-family="monospace">nice -n 10 command</text>
  <text x="160" y="170" text-anchor="middle" font-size="9">start with lower priority</text>
  <rect x="310" y="135" width="260" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="4"/>
  <text x="440" y="153" text-anchor="middle" font-size="10" font-family="monospace">renice -n 5 -p PID</text>
  <text x="440" y="170" text-anchor="middle" font-size="9">change running process priority</text>
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
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Process Troubleshooting Toolkit</text>
  <rect x="30" y="40" width="170" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="115" y="60" text-anchor="middle" font-size="11" font-weight="bold">CPU issues</text>
  <text x="115" y="78" text-anchor="middle" font-size="10" font-family="monospace">pidstat -p PID 1</text>
  <rect x="215" y="40" width="170" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="60" text-anchor="middle" font-size="11" font-weight="bold">Memory issues</text>
  <text x="300" y="78" text-anchor="middle" font-size="10" font-family="monospace">ps -o rss,cmd PID</text>
  <rect x="400" y="40" width="170" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="485" y="60" text-anchor="middle" font-size="11" font-weight="bold">Process tree</text>
  <text x="485" y="78" text-anchor="middle" font-size="10" font-family="monospace">pstree -p PID</text>
  <rect x="30" y="115" width="170" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="115" y="135" text-anchor="middle" font-size="11" font-weight="bold">Open files</text>
  <text x="115" y="153" text-anchor="middle" font-size="10" font-family="monospace">lsof -p PID</text>
  <rect x="215" y="115" width="170" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="135" text-anchor="middle" font-size="11" font-weight="bold">System calls</text>
  <text x="300" y="153" text-anchor="middle" font-size="10" font-family="monospace">strace -p PID</text>
  <rect x="400" y="115" width="170" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="485" y="135" text-anchor="middle" font-size="11" font-weight="bold">I/O activity</text>
  <text x="485" y="153" text-anchor="middle" font-size="10" font-family="monospace">iotop -p PID</text>
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
