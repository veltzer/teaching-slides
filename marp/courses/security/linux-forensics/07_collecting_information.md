# Collecting Information

## Course: Linux Forensics - Day 3 (continued)
- Systematic evidence collection is the foundation of forensic investigation
- Every artifact must be documented and preserved
- This module covers program execution evidence, hidden files, network artifacts,
  server logs, mounted filesystems, and kernel modules

---

## Order of Volatility

```diagram
Most Volatile (collect first)
+----------------------------------+
| 1. CPU registers, cache          |
| 2. RAM contents                  |
| 3. Network connections           |
| 4. Running processes             |
| 5. Kernel modules                |
| 6. Temporary files               |
| 7. Disk data                     |
| 8. Remote logs                   |
| 9. Physical configuration        |
| 10. Archival media               |
+----------------------------------+
Least Volatile (collect last)
```

- Collect volatile data first - it disappears on power loss
- RFC 3227 defines the order of volatility

---

## Program Execution Evidence

```bash
# Recently executed programs leave traces in multiple locations

# 1. Shell history
cat /home/user/.bash_history

# 2. /var/log/auth.log (programs run via sudo)
grep sudo /var/log/auth.log

# 3. Process accounting (if enabled)
lastcomm  # Shows recently executed commands
sa        # Summary of commands

# 4. auditd logs (if configured)
ausearch -k execve
aureport --executable

# 5. systemd journal
journalctl _COMM=specific_program

# 6. /proc (running processes only)
ls /proc/*/exe 2>/dev/null
```

---

## Process Accounting

```bash
# Enable process accounting
sudo apt install acct
sudo /etc/init.d/acct start

# View accounting data
lastcomm
# username  command  terminal  time
# root      ls       pts/0     Mon Jan 15 10:30
# john      wget     pts/1     Mon Jan 15 10:31
# root      bash     pts/0     Mon Jan 15 10:32

# Summary by user
sa -u

# Summary by command
sa -c

# Accounting log file
ls -la /var/log/account/pacct

# Dump raw accounting data
dump-acct /var/log/account/pacct
```

---

## Audit System (`auditd`)

```bash
# auditd provides comprehensive system call auditing
sudo apt install auditd

# Check audit status
sudo auditctl -s

# View audit rules
sudo auditctl -l

# Add rule to monitor file execution
sudo auditctl -a always,exit -F arch=b64 -S execve -k program_exec

# Add rule to monitor file access
sudo auditctl -w /etc/passwd -p rwa -k passwd_access

# Search audit logs
sudo ausearch -k program_exec
sudo ausearch -k passwd_access
sudo ausearch -i -ts today

# Generate reports
sudo aureport
sudo aureport --executable --summary
sudo aureport --login --summary
```

---

## Finding Hidden Files

```bash
# Files starting with dot (.) are hidden in Linux
find /home -name ".*" -type f 2>/dev/null | head -30

# Files in hidden directories
find /home -path "*/.*/*" -type f 2>/dev/null | head -30

# Files with unusual names (spaces, unicode)
find / -name "* *" -type f 2>/dev/null
find / -regex '.*[^a-zA-Z0-9._/-].*' -type f 2>/dev/null | head -20

# Files hidden by extended attributes (immutable)
lsattr -R / 2>/dev/null | grep -E "^....i"

# Files in unexpected locations
find /dev -type f 2>/dev/null  # Regular files in /dev
find /proc -type f -writable 2>/dev/null
find /sys -type f -size +0 2>/dev/null | head -20
```

---

## Finding Suspicious Files

```bash
# World-writable files
find / -perm -o+w -type f ! -path "/proc/*" ! -path "/sys/*" \
  2>/dev/null

# Files owned by nobody/nogroup
find / -nouser -o -nogroup 2>/dev/null | head -20

# Executable files in temp directories
find /tmp /var/tmp /dev/shm -type f -executable 2>/dev/null

# Recently modified files in system directories
find /usr/bin /usr/sbin /usr/lib -mtime -7 -type f 2>/dev/null

# Large files that might be data exfiltration staging
find /tmp /var/tmp /home -size +100M -type f 2>/dev/null

# Files with execution bit in non-standard locations
find /var/www /tmp /home -type f -perm -111 2>/dev/null
```

---

## Rootkit Detection

```bash
# Install rootkit detection tools
sudo apt install chkrootkit rkhunter

# chkrootkit scan
sudo chkrootkit

# rkhunter scan
sudo rkhunter --check

# Manual checks for common rootkit indicators:

# 1. Compare kernel module list
lsmod > current_modules.txt
# Compare against baseline

# 2. Check for /etc/ld.so.preload (library injection)
cat /etc/ld.so.preload
# Should be empty or not exist

# 3. Check for LD_PRELOAD in environment
env | grep LD_PRELOAD
grep LD_PRELOAD /etc/environment /etc/profile /etc/bash.bashrc

# 4. Verify system binaries
dpkg --verify 2>/dev/null | grep "^..5"
```

---

## Network Information Collection

```bash
# Active network connections
ss -tunapl
# -t TCP, -u UDP, -n numeric, -a all, -p processes, -l listening

# All connections with process info
ss -tunapl | column -t

# Routing table
ip route show
route -n  # Legacy

# ARP cache (recently communicated hosts)
ip neigh show
arp -a  # Legacy

# DNS cache (if systemd-resolved is used)
resolvectl statistics
resolvectl query example.com

# Open ports
ss -tlnp  # TCP listening
ss -ulnp  # UDP listening
```

---

## Network Interface Details

```bash
# All interfaces and addresses
ip addr show

# Interface statistics (traffic counters)
ip -s link show

# Promiscuous mode detection (sniffing)
ip link show | grep PROMISC
# If PROMISC flag is set, interface may be capturing packets

# Wireless information
iwconfig 2>/dev/null
iw dev

# VPN connections
ip link show type tun
ip link show type wireguard

# Network namespaces (container networking)
ip netns list
```

---

## Firewall Analysis

```bash
# iptables rules
sudo iptables -L -n -v --line-numbers
sudo iptables -t nat -L -n -v
sudo iptables -t mangle -L -n -v

# nftables rules
sudo nft list ruleset

# UFW (Ubuntu Firewall)
sudo ufw status verbose

# Firewalld (RHEL/CentOS)
sudo firewall-cmd --list-all

# Save firewall state for evidence
sudo iptables-save > /evidence/iptables_rules.txt
sudo nft list ruleset > /evidence/nft_rules.txt

# Look for suspicious rules
# - Rules allowing traffic from specific external IPs
# - Rules redirecting traffic
# - Rules in unexpected chains
```

---

## Active Network Capture

```bash
# Capture live traffic (if authorized)
sudo tcpdump -i eth0 -w /evidence/capture.pcap -c 10000

# Capture specific traffic
sudo tcpdump -i eth0 port 443 -w /evidence/https.pcap
sudo tcpdump -i eth0 host 10.0.0.99 -w /evidence/suspect.pcap

# Capture with rotation
sudo tcpdump -i eth0 -w /evidence/cap_%Y%m%d_%H%M%S.pcap \
  -G 3600 -W 24  # Rotate hourly, keep 24 files

# Quick analysis of pcap file
tcpdump -r /evidence/capture.pcap -n | head -20

# Extract statistics
capinfos /evidence/capture.pcap

# List all IP conversations
tcpdump -r /evidence/capture.pcap -n | \
  awk '{print $3, $5}' | sort | uniq -c | sort -rn | head -20
```

---

## Server Log Analysis

```bash
# Web server access logs
# Combined Log Format:
# IP - user [date] "request" status size "referer" "user-agent"

# Top requesting IPs
awk '{print $1}' /var/log/apache2/access.log | \
  sort | uniq -c | sort -rn | head -10

# Most requested URLs
awk '{print $7}' /var/log/apache2/access.log | \
  sort | uniq -c | sort -rn | head -10

# HTTP status code distribution
awk '{print $9}' /var/log/apache2/access.log | \
  sort | uniq -c | sort -rn

# Requests per hour (activity timeline)
awk -F'[:[]' '{print $2":"$3}' /var/log/apache2/access.log | \
  sort | uniq -c
```

---

## Web Attack Detection in Logs

```bash
# SQL injection attempts
grep -iE "union.*select|'.*or.*'|drop.*table|insert.*into" \
  /var/log/apache2/access.log

# Directory traversal
grep -E "\.\./\.\.|%2e%2e" /var/log/apache2/access.log

# Shell command injection
grep -iE "cmd=|exec\(|system\(|passthru|eval\(" \
  /var/log/apache2/access.log

# XSS attempts
grep -iE "<script|javascript:|onerror=|onload=" \
  /var/log/apache2/access.log

# Scanner/bot detection
grep -iE "nikto|sqlmap|nmap|masscan|dirbuster" \
  /var/log/apache2/access.log

# Large POST requests (potential file upload)
awk '$10 > 1000000 {print}' /var/log/apache2/access.log
```

---

## Mail Server Logs

```bash
# Postfix mail log
grep "postfix" /var/log/mail.log

# Sent emails
grep "status=sent" /var/log/mail.log

# Received emails
grep "from=" /var/log/mail.log

# Rejected/bounced emails
grep -E "reject|bounce" /var/log/mail.log

# Extract sender and recipient pairs
grep "from=<" /var/log/mail.log | \
  grep -oP 'from=<\K[^>]+' | sort | uniq -c | sort -rn

# Timeline of email activity
awk '{print $1, $2, $3}' /var/log/mail.log | \
  cut -d: -f1,2 | sort | uniq -c
```

---

## Database Server Logs

```bash
# MySQL/MariaDB
cat /var/log/mysql/error.log
# Check for general query log (if enabled)
cat /var/log/mysql/mysql.log

# Find MySQL configuration
cat /etc/mysql/mysql.conf.d/mysqld.cnf | grep -E "log|general"

# PostgreSQL
cat /var/log/postgresql/postgresql-*-main.log
# Check for log settings
grep "log" /etc/postgresql/*/main/postgresql.conf

# MongoDB
cat /var/log/mongodb/mongod.log

# Redis
cat /var/log/redis/redis-server.log
```

---

## Mounted Filesystems Analysis

```bash
# Currently mounted filesystems
mount
cat /proc/mounts
findmnt --tree

# Filesystem usage
df -h
df -i  # Inode usage

# Check for unusual mounts
mount | grep -v -E "^(sysfs|proc|devtmpfs|tmpfs|cgroup)"

# Look for:
# - Network mounts (NFS, CIFS/SMB)
mount | grep -E "nfs|cifs|smb"

# - Encrypted volumes
mount | grep -E "crypt|luks|ecryptfs"

# - Loop devices (mounted images)
mount | grep loop
losetup -l

# Fstab (persistent mounts)
cat /etc/fstab
```

---

## Encrypted Volume Detection

```bash
# Check for LUKS encrypted volumes
sudo cryptsetup luksDump /dev/sda3

# List open encrypted volumes
ls /dev/mapper/
dmsetup ls

# eCryptfs (home directory encryption)
ls /home/.ecryptfs/
cat /home/.ecryptfs/user/.Private/.ecryptfs/auto-mount

# VeraCrypt volumes (if VeraCrypt is installed)
veracrypt -l

# Check for encrypted swap
cat /etc/crypttab

# Identify encrypted partitions
blkid | grep -i "crypto\|luks"
```

---

## Kernel Module Analysis

```bash
# List all loaded modules
lsmod
# Module                  Size  Used by
# nf_tables             303104  0
# bluetooth             720896  1 btusb

# Detailed module information
modinfo nf_tables
# filename:    /lib/modules/.../nf_tables.ko
# license:     GPL
# author:      ...
# description: Netfilter nf_tables core

# Module dependencies
modprobe --show-depends suspicious_module

# Check module signature verification
cat /proc/sys/kernel/module_sig_enforce
# 1 = only signed modules allowed

# Recent module activity in logs
dmesg | grep -i "module"
journalctl -k | grep -i "module\|insmod\|modprobe"
```

---

## Detecting Malicious Kernel Modules

```bash
# Compare loaded modules against known-good list
lsmod | awk '{print $1}' | sort > /evidence/loaded_modules.txt

# Check for modules not associated with any package
for mod in $(lsmod | awk 'NR>1 {print $1}'); do
  modpath=$(modinfo -F filename "$mod" 2>/dev/null)
  if [ -n "$modpath" ] && [ "$modpath" != "(builtin)" ]; then
    pkg=$(dpkg -S "$modpath" 2>/dev/null)
    if [ -z "$pkg" ]; then
      echo "UNPACKAGED MODULE: $mod ($modpath)"
    fi
  fi
done

# Check module file hashes
for mod in $(find /lib/modules/$(uname -r) -name "*.ko*"); do
  sha256sum "$mod"
done > /evidence/module_hashes.txt
```

---

## Persistence Mechanisms Checklist

```bash
# Comprehensive check for persistence mechanisms
echo "=== Cron Jobs ==="
crontab -l 2>/dev/null
ls /etc/cron.d/ /etc/cron.daily/ /etc/cron.hourly/

echo "=== Systemd Services ==="
systemctl list-unit-files --state=enabled --type=service

echo "=== Systemd Timers ==="
systemctl list-timers

echo "=== Init Scripts ==="
ls /etc/init.d/
cat /etc/rc.local 2>/dev/null

echo "=== Shell Startup Files ==="
for f in /etc/profile /etc/profile.d/*.sh /etc/bash.bashrc; do
  echo "--- $f ---"
  cat "$f" 2>/dev/null
done

echo "=== SSH Authorized Keys ==="
find /home /root -name "authorized_keys" -exec cat {} \;

echo "=== LD_PRELOAD ==="
cat /etc/ld.so.preload 2>/dev/null
```

---

## Docker and Container Forensics

```bash
# Check for Docker
docker version 2>/dev/null
docker ps -a  # All containers (running and stopped)
docker images  # Available images

# Container logs
docker logs container_name

# Inspect container configuration
docker inspect container_name

# Container filesystem
docker diff container_name  # Changed files
docker export container_name > container_fs.tar

# Container networking
docker network ls
docker network inspect bridge

# Docker daemon logs
journalctl -u docker.service

# Podman containers (rootless alternative)
podman ps -a 2>/dev/null
```

---

## Collecting Evidence Script

```bash
#!/bin/bash
# Comprehensive evidence collection script
EVIDENCE="/evidence/collection_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$EVIDENCE"/{system,network,users,logs,processes}

# System info
cp /etc/os-release "$EVIDENCE/system/"
uname -a > "$EVIDENCE/system/uname.txt"
uptime > "$EVIDENCE/system/uptime.txt"

# Network state
ss -tunapl > "$EVIDENCE/network/connections.txt"
ip addr > "$EVIDENCE/network/interfaces.txt"
ip route > "$EVIDENCE/network/routes.txt"
ip neigh > "$EVIDENCE/network/arp.txt"

# User data
cp /etc/passwd /etc/group "$EVIDENCE/users/"
last > "$EVIDENCE/users/last.txt"
w > "$EVIDENCE/users/who.txt"

# Running processes
ps auxf > "$EVIDENCE/processes/ps.txt"
lsmod > "$EVIDENCE/processes/modules.txt"

# Calculate hash of everything collected
find "$EVIDENCE" -type f -exec sha256sum {} \; > \
  "$EVIDENCE/collection_hashes.sha256"

echo "Collection complete: $EVIDENCE"
```

---

## Exercise: Information Collection

### Tasks:
1. Run a comprehensive system survey
1. Identify all network connections and associated processes
1. Check for persistence mechanisms
1. Collect program execution evidence
1. Document all findings with timestamps

```bash
# Quick triage commands
echo "=== Date/Time ===" && date
echo "=== Hostname ===" && hostname
echo "=== Uptime ===" && uptime
echo "=== Who ===" && w
echo "=== Connections ===" && ss -tunapl
echo "=== Processes ===" && ps auxf | head -30
echo "=== SUID Files ===" && find / -perm -4000 -type f 2>/dev/null
echo "=== Cron ===" && crontab -l 2>/dev/null
echo "=== Recent Files ===" && find / -mtime -1 -type f 2>/dev/null | \
  head -20
```

---

## Summary: Collecting Information

- Follow order of volatility: volatile data first
- Program execution evidence exists in history, logs, and accounting
- Hidden files may use dot prefix, unusual names, or attributes
- Network analysis reveals active connections and communications
- Server logs contain attack evidence and user activity
- Mounted filesystems may include network shares or encrypted volumes
- Kernel modules should be verified against known-good lists
- Persistence mechanisms include cron, systemd, init scripts, SSH keys
- Container environments add additional forensic complexity
- Document every step with timestamps and hash verification

---

## Systemd Unit File Forensics

```bash
# Detailed examination of suspicious systemd services

# Find all non-package service files
for f in /etc/systemd/system/*.service; do
  [ -f "$f" ] || continue
  if ! dpkg -S "$f" >/dev/null 2>&1; then
    echo "=== CUSTOM SERVICE: $f ==="
    cat "$f"
    echo ""
  fi
done

# Examine service properties
systemctl show suspicious.service | grep -E \
  "ExecStart|User|Group|WorkingDirectory|Environment"

# Check for override files
systemctl cat suspicious.service
# Shows merged configuration including overrides

# Service dependency chain
systemctl list-dependencies suspicious.service

# Service resource usage
systemctl status suspicious.service
# Shows CPU, memory, tasks
```

---

## Collecting USB Evidence

```bash
# USB forensic evidence collection

# Current USB devices
lsusb
lsusb -t  # Tree format

# Detailed USB device info
for bus in /sys/bus/usb/devices/*/; do
  if [ -f "$bus/idVendor" ]; then
    vendor=$(cat "$bus/idVendor" 2>/dev/null)
    product=$(cat "$bus/idProduct" 2>/dev/null)
    serial=$(cat "$bus/serial" 2>/dev/null)
    manufacturer=$(cat "$bus/manufacturer" 2>/dev/null)
    prod_name=$(cat "$bus/product" 2>/dev/null)
    echo "Device: $manufacturer $prod_name ($vendor:$product) SN:$serial"
  fi
done

# USB event timeline from journal
journalctl _KERNEL_SUBSYSTEM=usb --since "7 days ago" \
  -o short-precise
```

---

## Network Forensic Data Collection

```bash
# Comprehensive network state capture

# DNS cache
resolvectl statistics 2>/dev/null
# Or check nscd cache
nscd -g 2>/dev/null

# Listening services
ss -tlnp | awk 'NR>1 {print $4, $6}'
# 0.0.0.0:22  users:(("sshd",pid=234,fd=3))
# 0.0.0.0:80  users:(("apache2",pid=567,fd=4))
# 127.0.0.1:3306  users:(("mysqld",pid=890,fd=23))

# Established connections with process info
ss -tnp state established

# Socket statistics summary
ss -s

# Wireless network history
ls /etc/NetworkManager/system-connections/
# Files here contain SSID, passwords (plaintext!)
cat /etc/NetworkManager/system-connections/*.nmconnection

# VPN configurations
ls /etc/openvpn/ /etc/wireguard/ 2>/dev/null
```

---

## Mounted Filesystems Deep Dive

```bash
# Detailed mount information
findmnt --tree --output TARGET,SOURCE,FSTYPE,OPTIONS,SIZE,USED

# Detect unusual bind mounts
findmnt --types bind
# Bind mounts can overlay directories, hiding contents

# Check for overlayfs (Docker/container layers)
findmnt --types overlay
mount | grep overlay

# Detect FUSE filesystems (user-space filesystems)
mount | grep fuse
# sshfs, encfs, gocryptfs may be in use

# NFS/CIFS mounts (network shares)
mount | grep -E "nfs|cifs|smb"
cat /etc/fstab | grep -E "nfs|cifs|smb"

# Auto-mount configuration
cat /etc/auto.master 2>/dev/null
ls /etc/auto.* 2>/dev/null

# Check for stale mounts
timeout 5 df -h 2>&1 | grep "Stale"
```

---

## Collecting Cgroup Information

```bash
# Cgroups control resource allocation
# Used by systemd, Docker, and other container runtimes

# View cgroup hierarchy
systemd-cgls

# Resource usage by cgroup
systemd-cgtop

# Per-process cgroup
cat /proc/1234/cgroup
# 0::/system.slice/ssh.service

# Docker container cgroups
ls /sys/fs/cgroup/system.slice/docker-*.scope/

# Memory limits and usage
cat /sys/fs/cgroup/system.slice/docker-*/memory.max
cat /sys/fs/cgroup/system.slice/docker-*/memory.current

# CPU limits
cat /sys/fs/cgroup/system.slice/docker-*/cpu.max

# Forensic value:
# - Identify containerized processes
# - Track resource consumption patterns
# - Detect resource-intensive malware (crypto miners)
```

---

## Evidence Collection: File Integrity

```bash
# Before collecting evidence, establish integrity

# Generate SHA-256 hashes during collection
collect_with_hash() {
  local src="$1" dst="$2"
  cp -p "$src" "$dst"
  sha256sum "$dst" >> /evidence/collection_hashes.sha256
  echo "Collected: $src -> $dst"
}

# Collect with metadata preservation
collect_with_hash /etc/passwd /evidence/files/passwd
collect_with_hash /etc/shadow /evidence/files/shadow
collect_with_hash /var/log/auth.log /evidence/files/auth.log

# Timestamp the collection
echo "Collection completed: $(date -u)" >> \
  /evidence/collection_log.txt

# Verify all collected files
sha256sum -c /evidence/collection_hashes.sha256
# /evidence/files/passwd: OK
# /evidence/files/shadow: OK
# /evidence/files/auth.log: OK
```

---

## Live Triage Script

```bash
#!/bin/bash
# Rapid live triage for incident response
# Run this FIRST before detailed analysis

TS=$(date -u +%Y%m%dT%H%M%SZ)
OUT="/evidence/triage_${TS}"
mkdir -p "$OUT"

echo "=== TRIAGE START: $TS ===" | tee "$OUT/triage.log"

# Volatile data (highest priority)
date -u > "$OUT/date.txt"
uptime > "$OUT/uptime.txt"
w > "$OUT/who.txt"
ps auxf > "$OUT/processes.txt"
ss -tunapl > "$OUT/network.txt"
ip addr > "$OUT/interfaces.txt"
ip route > "$OUT/routes.txt"
ip neigh > "$OUT/arp.txt"
lsmod > "$OUT/modules.txt"
free -m > "$OUT/memory.txt"
lsof -i > "$OUT/network_files.txt" 2>/dev/null
cat /proc/mounts > "$OUT/mounts.txt"

# Semi-volatile data
last > "$OUT/logins.txt"
lastb > "$OUT/failed_logins.txt" 2>/dev/null
cat /etc/passwd > "$OUT/passwd.txt"
cat /etc/group > "$OUT/group.txt"
crontab -l > "$OUT/crontab_root.txt" 2>/dev/null
systemctl list-units --all > "$OUT/services.txt"
find / -perm -4000 -type f > "$OUT/suid.txt" 2>/dev/null

# Hash triage output
sha256sum "$OUT"/* > "$OUT/triage_hashes.sha256"
echo "=== TRIAGE COMPLETE ===" | tee -a "$OUT/triage.log"
```

---

## Collecting Volatile Network Data

```bash
# Network state changes rapidly - capture early

# ARP table (recently communicated hosts)
ip neigh show > /evidence/volatile/arp_table.txt
# 192.168.1.1 dev eth0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
# 10.0.0.99 dev eth0 lladdr 11:22:33:44:55:66 STALE

# Connection tracking (NAT/firewall state)
sudo conntrack -L > /evidence/volatile/conntrack.txt 2>/dev/null

# Raw socket information
cat /proc/net/raw > /evidence/volatile/raw_sockets.txt
cat /proc/net/packet > /evidence/volatile/packet_sockets.txt
# Raw/packet sockets = potential sniffing

# Routing cache
ip route show cache > /evidence/volatile/route_cache.txt

# TCP connection details with timer info
ss -tnopi > /evidence/volatile/tcp_details.txt

# UDP endpoints
ss -unap > /evidence/volatile/udp.txt

# Unix domain sockets (inter-process communication)
ss -xlp > /evidence/volatile/unix_sockets.txt
```

---

## Collecting Application State

```bash
# Application-specific volatile state

# Web server connections
sudo apache2ctl fullstatus 2>/dev/null > \
  /evidence/volatile/apache_status.txt
curl -s http://localhost/nginx_status 2>/dev/null > \
  /evidence/volatile/nginx_status.txt

# Database connections
sudo mysql -e "SHOW PROCESSLIST\G" 2>/dev/null > \
  /evidence/volatile/mysql_processes.txt
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;" \
  2>/dev/null > /evidence/volatile/pg_processes.txt

# Redis info (in-memory database)
redis-cli INFO 2>/dev/null > /evidence/volatile/redis_info.txt
redis-cli CLIENT LIST 2>/dev/null > /evidence/volatile/redis_clients.txt

# Docker container state
docker ps -a --format "table {{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" \
  > /evidence/volatile/docker_state.txt 2>/dev/null
docker stats --no-stream > /evidence/volatile/docker_stats.txt 2>/dev/null
```

---

## Collecting System Performance Data

```bash
# Performance data can reveal anomalous behavior

# CPU usage by process
top -bn1 > /evidence/volatile/top_output.txt

# Memory usage details
free -m > /evidence/volatile/memory.txt
cat /proc/meminfo > /evidence/volatile/meminfo.txt

# Disk I/O statistics
iostat -x > /evidence/volatile/iostat.txt 2>/dev/null

# Process resource usage
ps -eo pid,ppid,user,%cpu,%mem,vsz,rss,stat,start,time,comm \
  --sort=-%cpu > /evidence/volatile/process_resources.txt

# System load average history
cat /proc/loadavg > /evidence/volatile/loadavg.txt

# Unusual resource usage may indicate:
# - Cryptocurrency mining (high CPU)
# - Data exfiltration (high network I/O)
# - Disk wiping (high disk I/O)
# - Memory-resident malware (high memory)
```

---

## Evidence Collection: Physical Security

```misc
PHYSICAL EVIDENCE COLLECTION
==============================
Before touching any device:

1. PHOTOGRAPH everything
   - Front, back, sides of device
   - Cable connections
   - Screen contents (if powered on)
   - Labels, serial numbers, asset tags
   - Surrounding environment

2. DOCUMENT device state
   - Power on/off?
   - Screen locked/unlocked?
   - LEDs and indicators
   - Sounds (fans, drives)
   - Temperature (warm = recently used)

3. PRESERVE power state
   - If ON: consider live acquisition first
   - If OFF: do NOT power on
   - Pull power plug (desktop) vs proper shutdown (server)
   - Laptop: remove battery after imaging

4. SEAL and LABEL
   - Anti-static bags for drives
   - Tamper-evident seals
   - Evidence tags with case number
   - Sign and date all seals
```
