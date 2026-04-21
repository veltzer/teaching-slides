---
tags:
  - infrastructure:linux
  - security:forensics
  - security:security
level: advanced
category: security
audience:
  - audiences:security-professionals

---

# Linux OS Artifacts

## Course: Linux Forensics - Day 2 (continued)
- `Linux` systems generate extensive forensic artifacts
- User activity, system events, and application data leave traces
- Knowing where to find artifacts is key to successful investigation
- This module covers user activity files, `/proc`, logs, and more

---

## User Activity Artifacts Overview

```tree
User Activity Artifacts
├── Shell history files
├── Recently used files
├── Desktop environment data
├── Browser history/cache
├── SSH known_hosts
├── Application configs
├── Trash/recycle bin
├── Thumbnails cache
├── Clipboard history
└── Login/logout records
```

---

## Bash History Deep Dive

```bash
# Default location
cat /home/user/.bash_history

# History with timestamps (if configured)
# Check for HISTTIMEFORMAT
grep HISTTIMEFORMAT /home/user/.bashrc
# HISTTIMEFORMAT="%F %T "

# When timestamps are enabled, .bash_history contains:
# #1705312200
# ls -la
# #1705312215
# cat /etc/passwd

# Convert timestamp
date -d @1705312200
# Mon Jan 15 10:30:00 UTC 2025

# Search history for suspicious commands
grep -iE "wget|curl|nc |ncat|python.*http|base64|chmod.*777" \
  /home/*/.bash_history /root/.bash_history 2>/dev/null
```

---

## Other Shell History Files

```bash
# Zsh history (with timestamps by default)
cat /home/user/.zsh_history
# : 1705312200:0;ls -la
# : 1705312215:0;cat /etc/passwd

# Fish shell history
cat /home/user/.local/share/fish/fish_history
# - cmd: ls -la
#   when: 1705312200

# Python interactive history
cat /home/user/.python_history

# MySQL/MariaDB command history
cat /home/user/.mysql_history

# PostgreSQL command history
cat /home/user/.psql_history

# Less command search history
cat /home/user/.lesshst
```

---

## Recently Used Files

```bash
# GNOME recently used files (XML format)
cat /home/user/.local/share/recently-used.xbel

# Parse recently used files
grep -oP 'href="file://\K[^"]+' \
  /home/user/.local/share/recently-used.xbel

# KDE recent documents
ls /home/user/.local/share/RecentDocuments/

# GTK recent file manager bookmarks
cat /home/user/.config/gtk-3.0/bookmarks

# Nautilus (GNOME Files) saved searches
ls /home/user/.local/share/nautilus/saved-searches/

# Thumbnails (indicate files that were viewed)
ls /home/user/.cache/thumbnails/normal/
ls /home/user/.cache/thumbnails/large/
```

---

## Trash / Recycle Bin

```bash
# GNOME/FreeDesktop trash location
ls -la /home/user/.local/share/Trash/
# files/     - deleted file contents
# info/      - metadata about deleted files

# Trash info file format
cat /home/user/.local/share/Trash/info/document.txt.trashinfo
# [Trash Info]
# Path=/home/user/Documents/document.txt
# DeletionDate=2025-01-15T10:30:00

# List all trashed files with original paths
for f in /home/user/.local/share/Trash/info/*.trashinfo; do
  echo "=== $(basename $f) ==="
  cat "$f"
done

# Root trash (if using GUI as root)
ls /root/.local/share/Trash/
```

---

## Browser Artifacts: Firefox

```bash
# Firefox profile directory
ls /home/user/.mozilla/firefox/
# profiles.ini - lists all profiles
# xxxxxxxx.default-release/ - profile directory

PROFILE="/home/user/.mozilla/firefox/*.default-release"

# Key forensic files:
ls $PROFILE/places.sqlite      # History and bookmarks
ls $PROFILE/cookies.sqlite     # Cookies
ls $PROFILE/formhistory.sqlite # Form data
ls $PROFILE/logins.json        # Saved passwords
ls $PROFILE/key4.db            # Master key database
ls $PROFILE/downloads.json     # Download history
ls $PROFILE/sessionstore.jsonlz4  # Session data
ls $PROFILE/cert9.db           # Certificates

# Query browsing history
sqlite3 $PROFILE/places.sqlite \
  "SELECT datetime(last_visit_date/1000000, 'unixepoch'),
   url, title FROM moz_places
   ORDER BY last_visit_date DESC LIMIT 20;"
```

---

## Browser Artifacts: Chrome/Chromium

```bash
# Chrome profile directory
CHROME="/home/user/.config/google-chrome/Default"

# Key forensic files:
ls $CHROME/History          # Browsing history (SQLite)
ls $CHROME/Cookies          # Cookies (SQLite)
ls $CHROME/Login\ Data      # Saved passwords (SQLite)
ls $CHROME/Web\ Data        # Autofill data (SQLite)
ls $CHROME/Bookmarks        # Bookmarks (JSON)
ls $CHROME/Preferences      # Settings (JSON)
ls $CHROME/Extensions/      # Installed extensions

# Query Chrome history
sqlite3 "$CHROME/History" \
  "SELECT datetime(last_visit_time/1000000-11644473600,
   'unixepoch'), url, title
   FROM urls ORDER BY last_visit_time DESC LIMIT 20;"
```

---

## SSH Artifacts

```bash
# SSH known_hosts - servers the user has connected to
cat /home/user/.ssh/known_hosts
# May be hashed (HashKnownHosts yes)
# |1|base64salt|base64hash hostname ssh-rsa AAAA...

# If not hashed, shows hostnames/IPs directly
# 192.168.1.100 ssh-rsa AAAA...

# SSH authorized_keys - who can log in as this user
cat /home/user/.ssh/authorized_keys

# SSH private keys (may unlock other systems)
ls -la /home/user/.ssh/id_*

# SSH client config (custom connections)
cat /home/user/.ssh/config
# Host myserver
#   HostName 10.0.0.50
#   User admin
#   IdentityFile ~/.ssh/special_key
```

---

## The `/proc` Filesystem for Live Forensics

```bash
# /proc is a virtual filesystem - only exists in RAM
# Essential for live forensic investigation

# System-wide information
cat /proc/version        # Kernel version string
cat /proc/uptime         # System uptime in seconds
cat /proc/loadavg        # System load averages
cat /proc/stat           # CPU statistics
cat /proc/meminfo        # Detailed memory info
cat /proc/swaps          # Swap usage
cat /proc/filesystems    # Supported filesystem types
cat /proc/modules        # Loaded kernel modules
cat /proc/net/tcp        # Active TCP connections
cat /proc/net/udp        # Active UDP connections
cat /proc/net/arp        # ARP cache
```

---

## Per-Process Information in `/proc`

```bash
# Each process has a directory /proc/[PID]/
ls /proc/1234/

# Critical files:
cat /proc/1234/cmdline | tr '\0' ' '    # Command line
cat /proc/1234/environ | tr '\0' '\n'   # Environment vars
cat /proc/1234/status                    # Process status
cat /proc/1234/maps                      # Memory mappings
cat /proc/1234/cwd                       # Current working dir
readlink /proc/1234/exe                  # Executable path
ls -la /proc/1234/fd/                    # Open file descriptors

# Network connections for specific process
ls -la /proc/1234/net/tcp
cat /proc/1234/net/tcp

# Recover deleted executable
cp /proc/1234/exe /evidence/recovered_binary
# Works even if the file was deleted from disk!
```

---

## Enumerating Processes via `/proc`

```bash
# List all processes with their executables
for pid in /proc/[0-9]*/; do
  pid_num=$(basename "$pid")
  exe=$(readlink "$pid/exe" 2>/dev/null)
  cmdline=$(cat "$pid/cmdline" 2>/dev/null | tr '\0' ' ')
  if [ -n "$exe" ]; then
    echo "PID: $pid_num | EXE: $exe | CMD: $cmdline"
  fi
done

# Find processes with deleted executables (suspicious!)
ls -la /proc/*/exe 2>/dev/null | grep "(deleted)"
# lrwxrwxrwx 1 root root 0 ... /proc/5678/exe -> /tmp/malware (deleted)

# This means the binary was deleted while still running
# Common malware technique to avoid detection
```

---

## Network Connections via `/proc`

```bash
# Parse /proc/net/tcp for active connections
cat /proc/net/tcp
#   sl  local_address rem_address   st ...
#    0: 0100007F:1F90 00000000:0000 0A ...

# Decode: addresses are in hex, little-endian
# 0100007F = 127.0.0.1
# 1F90 = 8080 (port)
# st: 0A = LISTEN

# Better: use ss or netstat
ss -tunapl

# Connection states:
# 0A = LISTEN
# 01 = ESTABLISHED
# 06 = TIME_WAIT
# 08 = CLOSE_WAIT

# Find process behind a connection
ss -tunapl | grep ":4443"
# ESTAB  0  0  10.0.0.5:4443  10.0.0.1:8080  users:(("suspicious",pid=5678,fd=3))
```

---

## `journalctl` Forensic Analysis

```bash
# All logs from the journal
journalctl --no-pager

# Logs from specific time window
journalctl --since "2025-01-15 00:00:00" \
           --until "2025-01-15 23:59:59"

# Authentication events
journalctl -u systemd-logind
journalctl _COMM=sshd
journalctl _COMM=sudo

# Failed login attempts
journalctl _COMM=sshd | grep -i "failed\|invalid"

# Kernel messages (hardware events, module loads)
journalctl -k

# JSON output for parsing
journalctl -o json-pretty | head -50
```

---

## Traditional Log Files: `auth.log`

```bash
# Authentication log - critical for forensics
sudo cat /var/log/auth.log

# Successful SSH logins
grep "Accepted" /var/log/auth.log
# Jan 15 10:30:00 server sshd[1234]: Accepted publickey
#   for john from 192.168.1.50 port 52341 ssh2

# Failed SSH attempts
grep "Failed" /var/log/auth.log
# Jan 15 10:30:05 server sshd[1235]: Failed password
#   for root from 10.0.0.99 port 52342 ssh2

# sudo usage
grep "sudo" /var/log/auth.log
# Jan 15 10:31:00 server sudo: john : TTY=pts/0 ;
#   PWD=/home/john ; USER=root ; COMMAND=/bin/bash

# User account changes
grep -E "useradd|userdel|usermod|groupadd" /var/log/auth.log
```

---

## Traditional Log Files: `syslog`

```bash
# General system messages
sudo cat /var/log/syslog | tail -50

# Filter by service
grep "cron" /var/log/syslog
grep "kernel" /var/log/syslog
grep "systemd" /var/log/syslog

# Look for errors and warnings
grep -iE "error|warning|critical|alert|emergency" /var/log/syslog

# Cron job execution
grep "CRON" /var/log/syslog
# Jan 15 */5 * * * root /tmp/.hidden/beacon.sh

# Service starts and stops
grep "Started\|Stopped\|Starting\|Stopping" /var/log/syslog

# Searching across rotated logs
zgrep "pattern" /var/log/syslog.*.gz
```

---

## Kernel Log Analysis

```bash
# Kernel ring buffer (current boot)
dmesg
dmesg -T  # With human-readable timestamps

# Kernel log file
cat /var/log/kern.log

# USB device connections (evidence of device attachment)
dmesg | grep -i "usb"
# [12345.678] usb 2-1: new high-speed USB device number 3
# [12345.789] usb 2-1: Product: USB Flash Drive
# [12345.790] usb 2-1: SerialNumber: ABC123456

# Disk events
dmesg | grep -iE "sd[a-z]|nvme"

# Network interface events
dmesg | grep -iE "eth|wlan|enp|wlp|link"

# Module loading
dmesg | grep "module"
```

---

## Web Server Logs

```bash
# Apache access log
cat /var/log/apache2/access.log
# 192.168.1.50 - - [15/Jan/2025:10:30:00 +0000]
#   "GET /index.html HTTP/1.1" 200 1234

# Apache error log
cat /var/log/apache2/error.log

# Nginx access log
cat /var/log/nginx/access.log

# Nginx error log
cat /var/log/nginx/error.log

# Look for attack indicators in web logs
grep -iE "union.*select|\.\.\/|<script|cmd=|exec\(|eval\(" \
  /var/log/apache2/access.log

# Find all unique IP addresses
awk '{print $1}' /var/log/apache2/access.log | sort -u
```

---

## Application-Specific Logs

```bash
# MySQL/MariaDB
cat /var/log/mysql/error.log
# If general log enabled:
cat /var/log/mysql/mysql.log

# PostgreSQL
cat /var/log/postgresql/postgresql-*-main.log

# Docker
journalctl -u docker.service
cat /var/log/docker.log

# Mail server
cat /var/log/mail.log
cat /var/log/mail.err

# CUPS (printing)
cat /var/log/cups/access_log
cat /var/log/cups/error_log
```

---

## Cracking `/etc/shadow` and `/etc/passwd`

- `/etc/shadow` contains password hashes
- Only readable by root

```bash
# Shadow file format:
# username:hash:lastchange:min:max:warn:inactive:expire:reserved
sudo cat /etc/shadow
# root:$6$salt$hash...:19000:0:99999:7:::
# john:$y$j9T$salt$hash...:19010:0:99999:7:::

# Hash format: $id$salt$hash
# $1$  = MD5
# $5$  = SHA-256
# $6$  = SHA-512
# $y$  = yescrypt (modern default)
# $2b$ = bcrypt

# Extract hash for cracking
sudo cat /etc/shadow | grep -v ':\*:\|:!:' | \
  awk -F: '{print $1":"$2}'
```

---

## Password Hash Identification

```bash
# Identify hash type from /etc/shadow
# $6$rounds=5000$saltsalt$hashhashhash...
#  |   |              |        |
#  |   |              |        +-- Hash value
#  |   |              +-- Salt
#  |   +-- Optional rounds parameter
#  +-- Hash algorithm ID

# Common hash IDs:
# $1$  -> MD5 (weak, deprecated)
# $5$  -> SHA-256 (better)
# $6$  -> SHA-512 (strong)
# $y$  -> yescrypt (newest, default on modern systems)
# $2b$ -> bcrypt (common on BSD)

# Check system's default hashing method
grep -E "^ENCRYPT_METHOD" /etc/login.defs
grep "pam_unix" /etc/pam.d/common-password
```

---

## Unshadowing Password Files

```bash
# John the Ripper needs combined passwd+shadow format

# Combine passwd and shadow files
sudo unshadow /etc/passwd /etc/shadow > /evidence/unshadowed.txt

# Or manually from a forensic image:
unshadow /mnt/evidence/etc/passwd /mnt/evidence/etc/shadow \
  > /evidence/unshadowed.txt

# Now crack with John the Ripper
john /evidence/unshadowed.txt

# Using a specific wordlist
john --wordlist=/usr/share/wordlists/rockyou.txt \
  /evidence/unshadowed.txt

# Show cracked passwords
john --show /evidence/unshadowed.txt
```

---

## Password Cracking with Hashcat

```bash
# Extract just the hash for hashcat
# For SHA-512 ($6$):
echo '$6$saltsalt$hashvalue...' > /evidence/hash.txt

# Hashcat hash modes for Linux:
# 500  = MD5 Unix ($1$)
# 7400 = SHA-256 Unix ($5$)
# 1800 = SHA-512 Unix ($6$)
# 3200 = bcrypt ($2b$)

# Dictionary attack
hashcat -m 1800 -a 0 /evidence/hash.txt \
  /usr/share/wordlists/rockyou.txt

# Dictionary + rules
hashcat -m 1800 -a 0 /evidence/hash.txt \
  /usr/share/wordlists/rockyou.txt -r rules/best64.rule

# Brute force (short passwords)
hashcat -m 1800 -a 3 /evidence/hash.txt ?a?a?a?a?a?a
```

---

## Files in `/dev`

```bash
# /dev contains device files and pseudo-devices
# Forensically interesting entries:

# Disk devices
ls -la /dev/sd* /dev/nvme* 2>/dev/null

# RAM access (if available)
ls -la /dev/mem /dev/kmem 2>/dev/null

# Loop devices (may indicate mounted images)
ls -la /dev/loop*
losetup -l

# Check for unusual device files
# Device files should not exist in directories like /tmp
find /tmp /var/tmp /home -type b -o -type c 2>/dev/null
# Block or character device files in user dirs = suspicious

# Device mapper (LVM, encrypted volumes)
ls -la /dev/mapper/
```

---

## SUID and SGID File Analysis

```bash
# Find all SUID files
find / -perm -4000 -type f 2>/dev/null | sort

# Expected SUID binaries (not exhaustive):
# /usr/bin/passwd, /usr/bin/sudo, /usr/bin/su
# /usr/bin/mount, /usr/bin/umount, /usr/bin/chfn
# /usr/bin/newgrp, /usr/bin/gpasswd, /usr/bin/chsh
# /usr/bin/pkexec, /usr/bin/ping

# Find SUID files NOT owned by root (unusual)
find / -perm -4000 ! -user root -type f 2>/dev/null

# Find SUID files in unusual locations
find /tmp /home /var/tmp /opt -perm -4000 -type f 2>/dev/null

# Find SUID files modified recently
find / -perm -4000 -mtime -30 -type f 2>/dev/null

# Compare against baseline
find / -perm -4000 -type f 2>/dev/null | sort > current_suid.txt
diff baseline_suid.txt current_suid.txt
```

---

## SGID Files and Directories

```bash
# Find all SGID files
find / -perm -2000 -type f 2>/dev/null | sort

# SGID directories (new files inherit group)
find / -perm -2000 -type d 2>/dev/null

# World-writable SGID directories (potential privilege escalation)
find / -perm -2002 -type d 2>/dev/null

# Check for capabilities (alternative to SUID)
getcap -r / 2>/dev/null
# /usr/bin/ping cap_net_raw=ep
# Unusual capabilities = potential privilege escalation
```

---

## Data and File Structure

```bash
# File magic numbers (signatures)
file /bin/ls
# /bin/ls: ELF 64-bit LSB pie executable, x86-64...

file document.pdf
# document.pdf: PDF document, version 1.7

# View file header bytes
xxd /bin/ls | head -3
# 00000000: 7f45 4c46 0201 0100 0000 0000 0000 0000  .ELF............

# Common magic numbers:
# 7f 45 4c 46 = ELF binary
# 25 50 44 46 = %PDF
# 50 4b 03 04 = PK (ZIP, DOCX, XLSX)
# ff d8 ff    = JPEG
# 89 50 4e 47 = PNG
# 1f 8b       = gzip
```

---

## Hex Editors for Forensics

```bash
# xxd - quick hex dump (comes with vim)
xxd file.bin | head -20
xxd -s 0x100 -l 64 file.bin  # Start at offset 0x100, 64 bytes

# hexdump - flexible formatting
hexdump -C file.bin | head -20

# od - octal dump with various formats
od -A x -t x1z -v file.bin | head -20

# bvi - binary vi (interactive hex editor)
bvi file.bin

# hexedit - another interactive hex editor
hexedit file.bin

# ghex - GUI hex editor (if desktop available)
# Bless - another GUI hex editor
```

---

## File Structure: ELF Binaries

```bash
# ELF (Executable and Linkable Format) analysis
readelf -h /bin/ls
# ELF Header:
#   Magic:   7f 45 4c 46 02 01 01 00 ...
#   Class:                 ELF64
#   Type:                  DYN (Position-Independent Executable)
#   Machine:               Advanced Micro Devices X86-64

# View sections
readelf -S /bin/ls

# View program headers
readelf -l /bin/ls

# Extract strings from binary
strings /bin/ls | head -20
strings -n 10 suspicious_binary  # Strings >= 10 chars

# Check for symbols
nm suspicious_binary 2>/dev/null
```

---

## File Structure: PDF Files

```bash
# PDF file structure
# Header: %PDF-1.7
# Body: objects (text, images, fonts)
# Cross-reference table
# Trailer

# Extract text from PDF
pdftotext document.pdf -

# View PDF metadata
pdfinfo document.pdf
exiftool document.pdf

# Look for embedded JavaScript (malicious PDFs)
strings document.pdf | grep -iE "javascript|/JS|eval|exec"

# Extract embedded files
binwalk document.pdf
# Or use pdf-parser
python3 pdf-parser.py -s javascript document.pdf
```

---

## Embedded Metadata (EXIF)

```bash
# Install exiftool
sudo apt install libimage-exiftool-perl

# View image metadata
exiftool photo.jpg
# Camera make/model, GPS coordinates, timestamps
# Software used, author information

# Key forensic metadata fields:
exiftool -DateTimeOriginal photo.jpg    # When photo was taken
exiftool -GPSLatitude -GPSLongitude photo.jpg  # GPS location
exiftool -Make -Model photo.jpg         # Camera info
exiftool -Software photo.jpg            # Editing software

# View metadata of documents
exiftool document.docx
# Author, creation date, modification date, software version

# Remove metadata (anti-forensics awareness)
exiftool -all= photo.jpg  # Strips all metadata
```

---

## File Clusters and Slack Space

![file_clusters_and_slack_space](svg/courses/security/linux-forensics/04_linux_os_artifacts/file_clusters_and_slack_space.svg)

---

## File Clusters and Slack Space: Example

- Slack space = unused portion of allocated cluster
- May contain remnants of previously deleted files
- Important source of forensic evidence
```bash
# View cluster/block size
sudo tune2fs -l /dev/sda2 | grep "Block size"
# Block size: 4096
```

---

## Finding Hidden Data in Slack Space

```bash
# Using Sleuth Kit to analyze slack space
# blkstat shows block allocation
blkstat image.dd 1000  # Check block 1000

# Extract file slack using Sleuth Kit
blkls -s image.dd > slack_data.raw

# Search slack space for strings
strings slack_data.raw | grep -iE "password|secret|key"

# Using foremost to carve data from unallocated space
foremost -i image.dd -o /evidence/carved/

# Using scalpel (faster alternative to foremost)
scalpel image.dd -o /evidence/carved/
```

---

## File Carving Basics

- File carving recovers files based on headers/footers
- Works on unallocated space and raw images
- Does not depend on filesystem metadata

```bash
# Install file carving tools
sudo apt install foremost scalpel

# Foremost - automatic file carving
foremost -t all -i disk_image.dd -o /evidence/carved/
# -t all = all file types
# -t jpg,png,pdf = specific types only

# View results
cat /evidence/carved/audit.txt
ls -la /evidence/carved/jpg/
ls -la /evidence/carved/pdf/
ls -la /evidence/carved/zip/
```

---

## Exercise: OS Artifacts Collection

### Tasks:
1. Collect all shell histories from the system
1. Analyze authentication logs for suspicious activity
1. Check for unusual SUID/SGID files
1. Examine browser artifacts for a user
1. Parse recent USB device connections from kernel logs

```bash
#!/bin/bash
# Artifact collection script
EVIDENCE="/evidence/artifacts"
mkdir -p "$EVIDENCE"

# Shell histories
cp /home/*/.bash_history "$EVIDENCE/" 2>/dev/null
cp /root/.bash_history "$EVIDENCE/root_bash_history" 2>/dev/null

# Auth log summary
grep -E "Accepted|Failed|sudo" /var/log/auth.log > \
  "$EVIDENCE/auth_summary.txt" 2>/dev/null

# SUID files
find / -perm -4000 -type f 2>/dev/null > "$EVIDENCE/suid_files.txt"

echo "Collection complete: $EVIDENCE"
```

---

## Summary: Linux OS Artifacts

- Shell history files are among the most valuable artifacts
- Browser data contains history, cookies, passwords, and downloads
- SSH artifacts reveal remote connections and trusted servers
- `/proc` provides live system state (volatile - capture early)
- `journalctl` and traditional logs record system events
- `/etc/shadow` contains password hashes for analysis
- SUID/SGID files may indicate privilege escalation
- File metadata (EXIF, document properties) reveals authorship
- Slack space and unallocated areas may contain deleted data
- File carving recovers files without filesystem metadata

---

## Systemd Journal Forensics Deep Dive

```bash
# Journal provides structured logging with rich metadata

# List all boots recorded in journal
journalctl --list-boots
#  0 abc123... Mon 2025-01-15 08:00 - Mon 2025-01-15 18:00
# -1 def456... Sun 2025-01-14 08:00 - Sun 2025-01-14 22:00

# Entries from specific boot
journalctl -b -1  # Previous boot

# Filter by priority
journalctl -p 0..3  # Emergency through Error only

# Show fields available for filtering
journalctl -F _COMM  # All unique COMM values
journalctl -F _UID   # All unique UIDs

# Advanced filtering
journalctl _COMM=sshd + _COMM=sudo  # OR logic
journalctl _UID=0 _COMM=bash        # AND logic

# Count events by type
journalctl --since today -o json | \
  python3 -c "import sys,json,collections; \
  c=collections.Counter(json.loads(l).get('_COMM','?') \
  for l in sys.stdin); print(*c.most_common(10), sep='\n')"
```

---

## Application Cache and Data

```bash
# Application caches contain forensic artifacts

# Thumbnails (prove files were viewed)
ls /home/user/.cache/thumbnails/
# normal/    - 128x128 thumbnails
# large/     - 256x256 thumbnails
# fail/      - files that couldn't be thumbnailed
# Thumbnails persist after original files are deleted!

# GNOME Tracker database (file indexing)
ls /home/user/.cache/tracker/
sqlite3 /home/user/.cache/tracker/meta.db \
  "SELECT url FROM nie:InformationElement LIMIT 20;"

# Zeitgeist activity log
ls /home/user/.local/share/zeitgeist/
sqlite3 /home/user/.local/share/zeitgeist/activity.sqlite \
  "SELECT timestamp, subj_uri FROM event_view ORDER BY timestamp DESC LIMIT 20;"

# GVFS metadata
ls /home/user/.local/share/gvfs-metadata/
```

---

## Clipboard History

```bash
# GPaste (GNOME clipboard manager)
ls /home/user/.local/share/gpaste/
cat /home/user/.local/share/gpaste/history.xml

# KDE Klipper
ls /home/user/.local/share/klipper/
cat /home/user/.local/share/klipper/history2.lst

# xclip/xsel (current clipboard only, volatile)
xclip -selection clipboard -o
xsel --clipboard --output

# CopyQ clipboard manager
ls /home/user/.config/copyq/
sqlite3 /home/user/.config/copyq/copyq.db "SELECT * FROM items;"

# Clipboard may contain:
# - Copied passwords
# - Copied commands
# - Copied file paths
# - Copied text from sensitive documents
```

---

## Printer and Scanner Artifacts

```bash
# CUPS print history
ls /var/log/cups/
cat /var/log/cups/access_log
cat /var/log/cups/error_log
cat /var/log/cups/page_log
# Page log format:
# printer user jobid date copies options

# Print queue
lpstat -a
lpq

# Completed jobs may be cached
ls /var/spool/cups/
# d00001-001  <- job data files
# c00001      <- control files

# Spool files may contain the printed document
file /var/spool/cups/d*

# Print to file/PDF history
find /home -name "*.pdf" -newer /tmp/start_date \
  -path "*Print*" 2>/dev/null
```

---

## Package Manager Artifacts

```bash
# APT/dpkg history reveals software installations

# APT history
cat /var/log/apt/history.log
# Start-Date: 2025-01-15 10:30:00
# Commandline: apt install nmap
# Install: nmap:amd64 (7.93-0ubuntu1)
# End-Date: 2025-01-15 10:30:15

# dpkg log
cat /var/log/dpkg.log
# 2025-01-15 10:30:05 install nmap:amd64 <none> 7.93-0ubuntu1

# APT sources (where packages come from)
cat /etc/apt/sources.list
ls /etc/apt/sources.list.d/

# Snap installations
snap list --all
cat /var/log/syslog | grep snapd

# pip packages (Python)
pip3 list
ls /home/user/.local/lib/python3*/site-packages/

# Manually installed software
ls /opt/
ls /usr/local/bin/
```

---

## Keyring and Credential Storage

```bash
# GNOME Keyring stores passwords and secrets
ls /home/user/.local/share/keyrings/
# login.keyring  - default keyring (encrypted)
# user.keystore  - additional keyring

# Decode keyring (requires user's login password)
# Tools: gnome-keyring-dump, keyring-viewer

# KDE Wallet
ls /home/user/.local/share/kwalletd/
# kdewallet.kwl

# Secret Service API entries
secret-tool search --all true 2>/dev/null

# SSH agent keys (in memory)
ssh-add -l

# GPG keyring
gpg --list-keys
ls /home/user/.gnupg/

# Password manager databases
find /home -name "*.kdbx" 2>/dev/null   # KeePass
find /home -name "*.psafe3" 2>/dev/null  # PasswordSafe
find /home -name "logins.json" 2>/dev/null  # Firefox
```

---

## Audit Trail with `auditd`

```bash
# auditd provides comprehensive audit logging

# View audit rules
sudo auditctl -l

# Common forensic audit rules:
# Monitor file access
sudo auditctl -w /etc/passwd -p rwa -k passwd_watch
sudo auditctl -w /etc/shadow -p rwa -k shadow_watch

# Monitor command execution
sudo auditctl -a always,exit -F arch=b64 -S execve -k cmd_exec

# Monitor network connections
sudo auditctl -a always,exit -F arch=b64 -S connect -k net_connect

# Search audit log
sudo ausearch -k passwd_watch
sudo ausearch -k cmd_exec -ts today
sudo ausearch -m USER_LOGIN -ts today

# Generate reports
sudo aureport --auth       # Authentication events
sudo aureport --login      # Login events
sudo aureport --file       # File access events
sudo aureport --executable # Command executions
```

---

## Tmp Files and Forensic Evidence

```bash
# Temporary files often contain forensic gold

# /tmp - cleared on reboot (usually)
ls -laR /tmp/

# /var/tmp - preserved across reboots
ls -laR /var/tmp/

# /dev/shm - shared memory tmpfs
ls -laR /dev/shm/
# Attackers use /dev/shm because it's world-writable
# and often overlooked

# User temp files
ls -la /home/user/.cache/
ls -la /run/user/*/

# vim swap files (may contain unsaved edits)
find / -name ".*.swp" -o -name ".*.swo" 2>/dev/null

# Editor backup files
find / -name "*~" -o -name "*.bak" -o -name "*.orig" 2>/dev/null | head -20

# Core dumps
find / -name "core" -o -name "core.*" 2>/dev/null
```

---

## Desktop Environment Artifacts

```bash
# GNOME session data
ls /home/user/.cache/gnome-session/

# GNOME shell extensions
ls /home/user/.local/share/gnome-shell/extensions/

# Recent documents (GNOME)
cat /home/user/.local/share/recently-used.xbel | \
  grep -oP 'href="file://\K[^"]+' | head -20

# Desktop files and launchers
ls /home/user/Desktop/
ls /home/user/.local/share/applications/

# Screenshot directory
ls /home/user/Pictures/Screenshots/ 2>/dev/null

# Screen recordings
find /home/user -name "*.webm" -o -name "*.mkv" | head -10

# Notification history
ls /home/user/.local/share/gnome-shell/notifications
```

---

## Git and Version Control Artifacts

```bash
# Git repositories may contain sensitive information

# Find all git repos
find /home -name ".git" -type d 2>/dev/null

# Git history in a repo
cd /home/user/project
git log --oneline -20
git log --all --oneline  # Include all branches

# Search git history for sensitive data
git log --all -p | grep -iE "password|secret|api.key|token"

# View deleted/modified files across history
git log --diff-filter=D --summary  # Deleted files
git log --diff-filter=M --summary  # Modified files

# Git stash (hidden work in progress)
git stash list
git stash show -p stash@{0}

# Git reflog (records all HEAD changes)
git reflog

# Other VCS
find /home -name ".svn" -type d 2>/dev/null
find /home -name ".hg" -type d 2>/dev/null
```

---

## Wi-Fi and Bluetooth Artifacts

```bash
# NetworkManager stores Wi-Fi connection history
ls /etc/NetworkManager/system-connections/
cat /etc/NetworkManager/system-connections/*.nmconnection
# [wifi]
# ssid=CorporateWiFi
# [wifi-security]
# key-mgmt=wpa-psk
# psk=WiFiPassword123  <- plaintext password!

# wpa_supplicant configuration
cat /etc/wpa_supplicant/wpa_supplicant.conf
# network={
#   ssid="HomeNetwork"
#   psk="password123"
# }

# Bluetooth paired devices
ls /var/lib/bluetooth/
# Contains paired device addresses and keys
find /var/lib/bluetooth -name "info" -exec cat {} \;

# Wireless interface history
journalctl | grep -iE "wlan|wifi|wireless|wpa"
```

---

## System Snapshots and Backups

```bash
# Timeshift snapshots (common on Linux Mint/Ubuntu)
ls /timeshift/snapshots/
# 2025-01-01_00-00-01/  <- snapshot from Jan 1

# Compare current state with snapshot
diff -r /timeshift/snapshots/2025-01-01_00-00-01/localhost/etc \
  /etc/ 2>/dev/null | head -30

# Btrfs snapshots
sudo btrfs subvolume list /
sudo btrfs subvolume show /snapshots/latest

# Snapper (SUSE, can be installed on others)
snapper list
snapper diff 1..2  # Compare snapshots

# rsync backups
find / -name "rsync" -path "*backup*" 2>/dev/null

# Duplicity/Deja-Dup backups
ls /home/user/.local/share/deja-dup/

# Forensic value: snapshots show state BEFORE compromise
# Compare pre-compromise snapshot with current state
```

---

## Systemd User Sessions

```bash
# Systemd tracks user sessions via logind

# List sessions
loginctl list-sessions
# SESSION  UID  USER  SEAT  TTY
# 1        1001 john  seat0 tty1
# 2        1001 john        pts/0

# Session details
loginctl show-session 2
# Id=2
# User=1001
# Name=john
# Timestamp=Mon 2025-01-15 10:30:00 UTC
# Remote=yes
# RemoteHost=192.168.1.50
# Service=sshd
# Leader=5678

# Session logs
journalctl _SYSTEMD_SESSION=2

# User lingering (sessions persist after logout)
loginctl show-user john | grep Linger
ls /var/lib/systemd/linger/
# Files here = users with lingering enabled
```

---

## Application Sandboxing Artifacts

```bash
# Flatpak application data
ls /var/lib/flatpak/app/
ls /home/user/.var/app/
# Each Flatpak app has isolated storage here

# Snap application data
ls /snap/
ls /home/user/snap/
# Snap applications store data in ~/snap/<app>/

# AppImage applications (no standard storage)
find /home -name "*.AppImage" 2>/dev/null

# Firejail sandboxing
ls /home/user/.config/firejail/
cat /etc/firejail/*.profile | head -20

# Application-specific sandboxes
# Chromium/Chrome runs with its own sandbox
# Check chrome://sandbox in browser data

# Forensic consideration:
# Sandboxed app data may be in different locations
# than expected. Check both standard and sandbox paths
```

---

## Machine Learning Model Artifacts

```bash
# ML/AI tools increasingly found on forensic targets

# Jupyter notebook history
find /home -name "*.ipynb" 2>/dev/null
# Contains code cells, outputs, and metadata

# Python virtual environments
find /home -name "activate" -path "*/bin/*" 2>/dev/null

# Model files
find /home -name "*.h5" -o -name "*.pkl" \
  -o -name "*.pt" -o -name "*.onnx" 2>/dev/null

# Docker images for ML
docker images | grep -iE "tensorflow|pytorch|jupyter"

# GPU usage history (may indicate crypto mining)
nvidia-smi --query-gpu=gpu_name --format=csv 2>/dev/null
cat /var/log/syslog | grep -i "nvidia\|cuda\|gpu"

# Forensic relevance:
# - Training data may contain sensitive information
# - Models may reveal intellectual property
# - GPU usage may indicate unauthorized crypto mining
```
