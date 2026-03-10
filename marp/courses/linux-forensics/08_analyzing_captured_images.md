# Analyzing Captured Images

## Course: Linux Forensics - Day 4
- Once evidence is captured, analysis begins
- Forensic images are examined without modifying original evidence
- This module covers image analysis tools, inode analysis,
  timeline building, and system log examination

---

## Analysis Environment Setup

```bash
# Create analysis workspace
mkdir -p /forensics/{images,mounted,output,tools}

# Mount evidence image read-only
sudo mount -o ro,noexec,noatime,loop \
  /forensics/images/disk.dd /forensics/mounted/

# For images with multiple partitions
sudo losetup -fP /forensics/images/disk.dd
# Creates /dev/loop0, /dev/loop0p1, /dev/loop0p2
sudo mount -o ro,noexec /dev/loop0p2 /forensics/mounted/

# Mount E01 images
sudo ewfmount /forensics/images/disk.E01 /forensics/ewf/
sudo mount -o ro,loop,offset=$((2048*512)) \
  /forensics/ewf/ewf1 /forensics/mounted/
```

---

## The Sleuth Kit (TSK) Overview

```bash
# Install The Sleuth Kit
sudo apt install sleuthkit

# TSK tools hierarchy:
# Volume Layer:  mmls, mmstat, mmcat
# Filesystem:    fsstat, fls, ffind, fcat
# File/Inode:    istat, icat, ifind
# Data/Block:    blkstat, blkls, blkcat, blkcalc
# Hash:          hfind, sorter
# Timeline:      mactime, fls -m
# Image:         img_stat, img_cat

# Get image information
img_stat /forensics/images/disk.dd

# List partitions
mmls /forensics/images/disk.dd
# Offset    Length    Description
# 0000002048  0001024000  Linux (0x83)
# 0001026048  0000032768  Linux Swap (0x82)
```

---

## Volume Analysis with `mmls`

```bash
# Display partition layout
mmls /forensics/images/disk.dd
# Units are in 512-byte sectors
#      Slot    Start       End         Length      Description
# 000: Meta    0000000000  0000000000  0000000001  Primary Table (#0)
# 001: -----   0000000000  0000002047  0000002048  Unallocated
# 002: 000:00  0000002048  0104857599  0104855552  Linux (0x83)
# 003: 000:01  0104857600  0109051903  0004194304  Linux Swap

# Calculate byte offset for partition
# Partition 002 starts at sector 2048
# Byte offset = 2048 * 512 = 1048576

# Access specific partition directly
# Use -o offset (in sectors) for TSK tools
fls -o 2048 /forensics/images/disk.dd
```

---

## Filesystem Analysis with `fsstat`

```bash
# Display filesystem details
fsstat -o 2048 /forensics/images/disk.dd

# Output includes:
# FILE SYSTEM INFORMATION
# File System Type: Ext4
# Volume Name:
# Volume ID: abcdef1234567890
#
# METADATA INFORMATION
# First Inode: 1
# Last Inode: 6553600
# Root Directory: 2
#
# CONTENT INFORMATION
# Block Size: 4096
# Block Count: 13106944
# Free Blocks: 8234567
#
# BLOCK GROUP INFORMATION
# Number of Block Groups: 400
# Inodes per group: 16384
# Blocks per group: 32768
```

---

## Directory Listing with `fls`

```bash
# List root directory
fls -o 2048 /forensics/images/disk.dd
# d/d  2:      .
# d/d  11:     lost+found
# d/d  131073: etc
# d/d  262145: home
# d/d  393217: var
# r/r  12:     vmlinuz

# List with full paths recursively
fls -o 2048 -r /forensics/images/disk.dd | head -20

# List specific directory (by inode)
fls -o 2048 /forensics/images/disk.dd 131073  # /etc

# Show deleted files (prefix -)
fls -o 2048 -d /forensics/images/disk.dd
# -/r * 45678: secret_document.txt
# -/r * 45679: malware.elf
# The * indicates the file is deleted

# List with MAC times
fls -o 2048 -l /forensics/images/disk.dd
```

---

## Inode Analysis with `istat`

```bash
# Display detailed inode information
istat -o 2048 /forensics/images/disk.dd 131073

# Output:
# inode: 131073
# Allocated
# Group: 8
# Generation Id: 1234567890
# uid / gid: 0 / 0
# mode: drwxr-xr-x
# Flags: Extents,
# size: 4096
# num of links: 82
#
# Inode Times:
# Accessed:     2025-01-15 10:30:00 (UTC)
# File Modified: 2025-01-10 08:00:00 (UTC)
# Inode Modified: 2025-01-10 08:00:00 (UTC)
# File Created:  2024-06-01 12:00:00 (UTC)
#
# Direct Blocks:
# 1234567
```

---

## Inode Analysis: Understanding Results

```bash
# Key inode fields for forensics:

# Allocation status
# - "Allocated" = active file
# - "Not Allocated" = deleted file (potentially recoverable)

# Timestamps (MACB):
# - Accessed (A): last content read
# - File Modified (M): last content change
# - Inode Modified (C): last metadata change (permissions, etc.)
# - File Created (B): birth time (ext4 only)

# Size vs Blocks:
# - Size: logical file size
# - Blocks: allocated disk blocks
# - If size < blocks * block_size: slack space exists

# Link count:
# - 0 for deleted files
# - >1 for files with hard links
```

---

## File Content Extraction with `icat`

```bash
# Extract file content by inode number
icat -o 2048 /forensics/images/disk.dd 45678 > recovered_file.txt

# Extract deleted file content
icat -o 2048 /forensics/images/disk.dd 45679 > recovered_malware.elf

# Pipe to other tools for analysis
icat -o 2048 /forensics/images/disk.dd 45678 | strings | head -20
icat -o 2048 /forensics/images/disk.dd 45678 | file -
icat -o 2048 /forensics/images/disk.dd 45678 | sha256sum

# Find inode by filename
ifind -o 2048 -n "/etc/passwd" /forensics/images/disk.dd
# Output: 131074

# Extract that file
icat -o 2048 /forensics/images/disk.dd 131074 > etc_passwd.txt
```

---

## Block-Level Analysis

```bash
# Check block allocation status
blkstat -o 2048 /forensics/images/disk.dd 1234567
# Block: 1234567
# Allocated

# Extract specific block content
blkcat -o 2048 /forensics/images/disk.dd 1234567 | xxd | head -20

# Extract all unallocated blocks (free space)
blkls -o 2048 /forensics/images/disk.dd > unallocated.raw

# Extract slack space
blkls -o 2048 -s /forensics/images/disk.dd > slack_space.raw

# Search unallocated space for strings
strings unallocated.raw | grep -iE "password|secret|key" > \
  /forensics/output/unalloc_strings.txt

# Find which file uses a specific block
ifind -o 2048 -d 1234567 /forensics/images/disk.dd
# Output: 45678 (inode number)
```

---

## Building Forensic Timelines

```bash
# Step 1: Generate bodyfile from filesystem
fls -o 2048 -r -m "/" /forensics/images/disk.dd > bodyfile.txt

# Bodyfile format:
# MD5|name|inode|mode_as_string|UID|GID|size|atime|mtime|ctime|crtime
# 0|/etc/passwd|131074|r/rrw-r--r--|0|0|2345|1705312200|1705225600|...

# Step 2: Generate timeline from bodyfile
mactime -b bodyfile.txt -d > timeline.csv

# Step 3: Filter timeline by date range
mactime -b bodyfile.txt -d 2025-01-15..2025-01-16 > \
  /forensics/output/timeline_jan15.csv

# CSV columns:
# Date, Size, Type, Mode, UID, GID, Meta, File Name
```

---

## Timeline Analysis Techniques

```bash
# View timeline sorted by time
mactime -b bodyfile.txt 2025-01-15 | head -30

# Filter for specific activity types
# m = modified, a = accessed, c = changed, b = born
grep ",m" /forensics/output/timeline.csv | head -20

# Find activity around specific event
mactime -b bodyfile.txt -d 2025-01-15T10:00:00..2025-01-15T11:00:00

# Combine with log timelines
# Add log events to timeline
cat /forensics/mounted/var/log/auth.log | \
  awk '{print $1,$2,$3,"|AUTH|",$0}' >> combined_timeline.txt

# Sort combined timeline
sort -t'|' -k1 combined_timeline.txt > sorted_timeline.txt

# Look for timeline gaps (potential evidence destruction)
# Look for timestamp clusters (intensive activity periods)
```

---

## Timeline Visualization

```text
Jan 15, 2025 - Activity Timeline
|
10:00 -- SSH login from 10.0.0.99 (auth.log)
10:01 -- /tmp/.hidden/ directory created (filesystem)
10:02 -- /tmp/.hidden/toolkit.tar.gz created
10:03 -- /tmp/.hidden/toolkit.tar.gz accessed (extracted)
10:03 -- /tmp/.hidden/recon.sh created
10:04 -- /tmp/.hidden/recon.sh executed (process accounting)
10:05 -- /etc/cron.d/update created (persistence)
10:10 -- /var/www/html/shell.php created (webshell)
10:15 -- SSH logout (auth.log)
  ...
10:30 -- /var/www/html/shell.php accessed (web log)
10:31 -- /etc/passwd accessed (web log, possible LFI)
|
```

---

## System Log Analysis from Image

```bash
# Read logs from mounted evidence
cat /forensics/mounted/var/log/auth.log | head -50

# Parse syslog for specific timeframe
grep "Jan 15" /forensics/mounted/var/log/syslog | head -50

# Check for log tampering
# 1. Gaps in log timestamps
awk '{print $1,$2,$3}' /forensics/mounted/var/log/syslog | \
  sort | uniq | head -30

# 2. Log files with unexpected modification times
stat /forensics/mounted/var/log/*

# 3. Truncated log files
wc -l /forensics/mounted/var/log/syslog
wc -l /forensics/mounted/var/log/auth.log

# Read binary logs
utmpdump /forensics/mounted/var/log/wtmp
utmpdump /forensics/mounted/var/log/btmp
```

---

## Analyzing `wtmp` and `btmp`

```bash
# wtmp contains login/logout records
# btmp contains failed login attempts

# Read wtmp
last -f /forensics/mounted/var/log/wtmp
# username  pts/0  192.168.1.50  Mon Jan 15 10:30 - 10:45 (00:15)
# username  pts/0  192.168.1.50  Mon Jan 15 09:00 - 09:30 (00:30)

# Read btmp (failed logins)
lastb -f /forensics/mounted/var/log/btmp
# root      ssh:notty  10.0.0.99  Mon Jan 15 10:28 - 10:28 (00:00)
# admin     ssh:notty  10.0.0.99  Mon Jan 15 10:28 - 10:28 (00:00)

# Dump raw wtmp data
utmpdump /forensics/mounted/var/log/wtmp
# [7] [01234] [ts/0] [john    ] [pts/0       ] [192.168.1.50    ]
#   [192.168.1.50] [2025-01-15T10:30:00,000000+0000]
```

---

## Journal Analysis from Image

```bash
# systemd journal files are in binary format
ls /forensics/mounted/var/log/journal/*/

# Read journal from mounted image
journalctl --directory=/forensics/mounted/var/log/journal/

# Filter by time
journalctl --directory=/forensics/mounted/var/log/journal/ \
  --since "2025-01-15" --until "2025-01-16"

# Filter by service
journalctl --directory=/forensics/mounted/var/log/journal/ \
  -u sshd

# Export as JSON for parsing
journalctl --directory=/forensics/mounted/var/log/journal/ \
  -o json-pretty > /forensics/output/journal.json

# Export as text
journalctl --directory=/forensics/mounted/var/log/journal/ \
  --no-pager > /forensics/output/journal.txt
```

---

## Log Correlation

```bash
# Correlate authentication with file changes

# Step 1: Extract SSH logins with timestamps
grep "Accepted" /forensics/mounted/var/log/auth.log | \
  awk '{print $1,$2,$3,$9,$11}' > /forensics/output/ssh_logins.txt

# Step 2: Find files modified around login times
# For each login time, find files changed within +/- 30 minutes
while read month day time user ip; do
  echo "=== Login: $user from $ip at $month $day $time ==="
  login_epoch=$(date -d "$month $day $time" +%s 2>/dev/null)
  if [ -n "$login_epoch" ]; then
    find /forensics/mounted -newer /tmp/before -not -newer /tmp/after \
      -type f 2>/dev/null | head -10
  fi
done < /forensics/output/ssh_logins.txt

# Step 3: Cross-reference with sudo activity
grep "sudo" /forensics/mounted/var/log/auth.log
```

---

## Recovering Deleted Files from Image

```bash
# List all deleted files
fls -o 2048 -r -d /forensics/images/disk.dd | head -30
# -/r * 45678: home/user/deleted_document.pdf
# -/d * 45680: tmp/.hidden

# Recover specific deleted file
icat -o 2048 /forensics/images/disk.dd 45678 > \
  /forensics/output/recovered_document.pdf

# Verify recovered file
file /forensics/output/recovered_document.pdf
sha256sum /forensics/output/recovered_document.pdf

# Batch recover all deleted files
mkdir -p /forensics/output/recovered/
fls -o 2048 -r -d /forensics/images/disk.dd | while read line; do
  inode=$(echo "$line" | awk -F: '{print $1}' | tr -d ' *-/rd')
  name=$(echo "$line" | awk -F: '{print $2}' | tr -d ' ')
  if [ -n "$inode" ] && [ "$inode" -gt 0 ] 2>/dev/null; then
    icat -o 2048 /forensics/images/disk.dd "$inode" > \
      "/forensics/output/recovered/${inode}_${name##*/}" 2>/dev/null
  fi
done
```

---

## Keyword Search in Image

```bash
# Search raw image for keywords
strings /forensics/images/disk.dd | \
  grep -in "password\|secret\|confidential" | head -20

# Search with offset tracking
grep -boa "password" /forensics/images/disk.dd | head -10
# 123456789:password
# Offset 123456789 bytes into the image

# Convert byte offset to block number
# Block number = byte_offset / block_size
python3 -c "print(123456789 // 4096)"
# 30150

# Find which file contains that block
ifind -o 2048 -d 30150 /forensics/images/disk.dd
# Returns inode number

# Using Sleuth Kit's sigfind for pattern matching
sigfind -o 2048 25504446 /forensics/images/disk.dd
# Searches for %PDF signature
```

---

## Analyzing User Artifacts from Image

```bash
# Extract bash histories
for user_dir in /forensics/mounted/home/*/; do
  username=$(basename "$user_dir")
  echo "=== $username ==="
  cat "$user_dir/.bash_history" 2>/dev/null
done

# Extract SSH data
for user_dir in /forensics/mounted/home/*/; do
  username=$(basename "$user_dir")
  echo "=== $username SSH ==="
  cat "$user_dir/.ssh/known_hosts" 2>/dev/null
  cat "$user_dir/.ssh/authorized_keys" 2>/dev/null
done

# Browser history
sqlite3 /forensics/mounted/home/user/.mozilla/firefox/*.default*/places.sqlite \
  "SELECT datetime(last_visit_date/1000000,'unixepoch'), url
   FROM moz_places ORDER BY last_visit_date DESC LIMIT 30;"
```

---

## Hash Analysis of Image Contents

```bash
# Generate hashes of all files in image
find /forensics/mounted -type f -exec sha256sum {} \; > \
  /forensics/output/all_file_hashes.txt

# Compare against NSRL (known software)
# Files NOT in NSRL may be custom/suspicious
while read hash filepath; do
  if ! grep -qi "$hash" /forensics/tools/NSRLFile.txt; then
    echo "UNKNOWN: $hash $filepath"
  fi
done < /forensics/output/all_file_hashes.txt > \
  /forensics/output/unknown_files.txt

# Compare against known malware hashes
while read hash filepath; do
  if grep -qi "$hash" /forensics/tools/malware_hashes.txt; then
    echo "MALWARE MATCH: $hash $filepath"
  fi
done < /forensics/output/all_file_hashes.txt
```

---

## Autopsy Integration

```bash
# Autopsy is a GUI frontend for The Sleuth Kit
# Provides visual timeline, keyword search, and reporting

# Install Autopsy
sudo apt install autopsy

# Start Autopsy web interface
autopsy
# Open browser to http://localhost:9999/autopsy

# Autopsy features:
# - Case management
# - Image import (dd, E01, AFF)
# - File system analysis
# - Timeline view
# - Keyword searching
# - Hash filtering (NSRL)
# - Web artifact analysis
# - Email parsing
# - Registry analysis (Windows images)
# - Report generation
```

---

## Exercise: Image Analysis Lab

### Tasks:
1. Mount a forensic image read-only
1. Use `fls` to list directory contents and deleted files
1. Use `istat` to analyze inodes of interest
1. Build a timeline using `fls` and `mactime`
1. Recover a deleted file and verify its integrity

```bash
# Analysis workflow
IMG="/forensics/images/disk.dd"
OFFSET=2048

# List partitions
mmls "$IMG"

# List root directory
fls -o $OFFSET "$IMG"

# Find deleted files
fls -o $OFFSET -r -d "$IMG" | head -20

# Build timeline
fls -o $OFFSET -r -m "/" "$IMG" > bodyfile.txt
mactime -b bodyfile.txt -d 2025-01-15 > timeline.csv
head -30 timeline.csv
```

---

## Summary: Analyzing Captured Images

- The Sleuth Kit provides comprehensive command-line forensic analysis
- `mmls` reveals partition layout; `fsstat` shows filesystem details
- `fls` lists files and directories, including deleted entries
- `istat` provides detailed inode information with timestamps
- `icat` extracts file content by inode number
- Block-level tools analyze raw disk data and unallocated space
- Timelines combine filesystem timestamps into chronological view
- `mactime` generates CSV timelines from body files
- System logs from images reveal authentication and system events
- Correlating multiple evidence sources strengthens findings
- Autopsy provides a GUI interface for visual analysis

---

## Advanced Timeline Analysis

```bash
# Super Timeline with Plaso
# Plaso combines hundreds of artifact parsers

# Install Plaso
pip3 install plaso-tools

# Create super timeline
log2timeline.py /evidence/timeline.plaso /forensics/images/disk.dd

# Output timeline as CSV
psort.py -o l2tcsv -w /evidence/timeline.csv \
  /evidence/timeline.plaso

# Filter by date range
psort.py -o l2tcsv -w /evidence/filtered_timeline.csv \
  /evidence/timeline.plaso \
  "date > '2025-01-15 00:00:00' AND date < '2025-01-16 00:00:00'"

# Filter by source
psort.py -o l2tcsv -w /evidence/auth_timeline.csv \
  /evidence/timeline.plaso \
  "source_short == 'LOG' AND source == 'syslog'"
```

---

## Searching for IOCs in Images

```bash
# IOC = Indicator of Compromise

# Search for known malicious filenames
find /forensics/mounted -name "*.php" -exec grep -l "eval\|exec\|system\|passthru" {} \;

# Search for known malicious hashes
# Create IOC hash list
cat > /evidence/ioc_hashes.txt << 'EOF'
abc123def456789...  malware_variant_1
def789abc012345...  webshell_common
EOF

# Compare against all files on image
find /forensics/mounted -type f -exec sha256sum {} \; 2>/dev/null | \
  while read hash filepath; do
    if grep -q "$hash" /evidence/ioc_hashes.txt; then
      echo "IOC MATCH: $filepath ($hash)"
    fi
  done

# Search for known C2 domains
strings /forensics/images/disk.dd | \
  grep -f /evidence/ioc_domains.txt > /evidence/domain_hits.txt

# YARA rule scanning
yara -r /evidence/rules/malware.yar /forensics/mounted/
```

---

## YARA Rules for Forensic Scanning

```bash
# Install YARA
sudo apt install yara

# Example YARA rule for PHP webshell
cat > /evidence/rules/webshell.yar << 'EOF'
rule PHP_Webshell {
    meta:
        description = "Detects PHP web shells"
        author = "Forensic Analyst"
    strings:
        $eval = "eval(" ascii
        $system = "system(" ascii
        $exec = "exec(" ascii
        $passthru = "passthru(" ascii
        $shell_exec = "shell_exec(" ascii
        $base64 = "base64_decode(" ascii
        $php = "<?php" ascii
    condition:
        $php and any of ($eval, $system, $exec, $passthru,
                         $shell_exec, $base64)
}
EOF

# Scan mounted evidence
yara -r /evidence/rules/webshell.yar /forensics/mounted/var/www/
# webshell /forensics/mounted/var/www/html/uploads/cmd.php
```

---

## Analyzing Deleted User Accounts

```bash
# Users may be created and deleted during compromise

# Check /etc/passwd for recently deleted users
# Compare with backup or package default
diff /forensics/mounted/etc/passwd /forensics/baseline/etc/passwd

# Check /var/log/auth.log for user account operations
grep -E "useradd|userdel|usermod|groupadd|groupdel" \
  /forensics/mounted/var/log/auth.log

# Look for orphaned home directories
for dir in /forensics/mounted/home/*/; do
  username=$(basename "$dir")
  if ! grep -q "^$username:" /forensics/mounted/etc/passwd; then
    echo "ORPHANED HOME DIR: $dir (user $username deleted)"
    ls -la "$dir"
  fi
done

# Check for orphaned crontabs
for f in /forensics/mounted/var/spool/cron/crontabs/*; do
  username=$(basename "$f")
  if ! grep -q "^$username:" /forensics/mounted/etc/passwd; then
    echo "ORPHANED CRONTAB: $f"
    cat "$f"
  fi
done
```

---

## Analyzing Modified System Binaries

```bash
# Verify system binaries against package database

# Method 1: dpkg verification (Debian/Ubuntu)
# On forensic workstation, mount image and compare
dpkg -V --root=/forensics/mounted/ 2>/dev/null | head -30
# ??5?????? /usr/bin/ls  <- MD5 mismatch!

# Method 2: rpm verification (RHEL/CentOS)
rpm --root=/forensics/mounted/ -Va 2>/dev/null | head -30

# Method 3: Manual hash comparison
# Get expected hash from package
apt download coreutils
dpkg -c coreutils_*.deb | grep "/bin/ls"
dpkg --fsys-tarfile coreutils_*.deb | tar -xf - ./usr/bin/ls
sha256sum ./usr/bin/ls
sha256sum /forensics/mounted/usr/bin/ls
# Compare hashes

# Method 4: Compare file sizes
find /forensics/mounted/usr/bin -type f -exec stat -c '%s %n' {} \; | \
  sort -k2 > /evidence/bin_sizes.txt
```

---

## Analyzing Web Application Data

```bash
# Web roots may contain evidence of compromise

# Find web roots
find /forensics/mounted -name "index.html" -o -name "index.php" | \
  head -10

# Search for web shells
find /forensics/mounted/var/www -name "*.php" -exec \
  grep -l "eval\|exec\|system\|passthru\|base64_decode\|$_GET\[.cmd\]" {} \;

# Recently modified web files
find /forensics/mounted/var/www -mtime -7 -type f -ls

# Upload directories (common attack target)
find /forensics/mounted/var/www -name "uploads" -type d -exec ls -la {} \;

# Database connection strings (credentials)
grep -rn "mysql_connect\|mysqli\|PDO\|pg_connect" \
  /forensics/mounted/var/www/ | head -10

# Configuration files with passwords
find /forensics/mounted/var/www -name "*.conf" -o -name "*.config" \
  -o -name "*.ini" -o -name "*.env" | xargs grep -l "password" 2>/dev/null
```

---

## Analyzing Network Configuration Changes

```bash
# Compare network config against expected state

# DNS resolution
cat /forensics/mounted/etc/resolv.conf
# nameserver 8.8.8.8  <- Expected?
# nameserver 10.0.0.99  <- Attacker's DNS?

# Hosts file manipulation
cat /forensics/mounted/etc/hosts
# Look for entries redirecting legitimate domains
# 10.0.0.99 update.microsoft.com  <- DNS hijacking!

# iptables rules
cat /forensics/mounted/etc/iptables/rules.v4 2>/dev/null
# Look for:
# - Rules allowing traffic from suspicious IPs
# - Port forwarding rules
# - Rules that drop logging

# SSH config changes
diff /forensics/baseline/etc/ssh/sshd_config \
  /forensics/mounted/etc/ssh/sshd_config
# Look for:
# - PermitRootLogin yes
# - PasswordAuthentication yes
# - Port changed from 22
```

---

## Slack Space Analysis

```bash
# Extract and analyze slack space using TSK

# Identify file with slack space
istat -o 2048 /forensics/images/disk.dd 131074
# Size: 100, Allocated: 4096
# Slack = 4096 - 100 = 3996 bytes

# Extract file slack for all files
blkls -s -o 2048 /forensics/images/disk.dd > \
  /evidence/all_slack.raw

# Search slack space for strings
strings /evidence/all_slack.raw | \
  grep -iE "password|secret|credit.card" > \
  /evidence/slack_hits.txt

# View slack of specific file
# Get last block of file from istat output
# Then extract just the slack portion
blkcat -o 2048 /forensics/images/disk.dd 12345 | \
  tail -c +101 > /evidence/file_slack.raw
# Skip first 100 bytes (file content), rest is slack
```

---

## Automating Image Analysis

```bash
#!/bin/bash
# Automated image analysis script
IMG="$1"
OFFSET="$2"
OUT="/evidence/analysis_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"

echo "[*] Starting automated analysis of $IMG"

echo "[*] Partition layout..."
mmls "$IMG" > "$OUT/partitions.txt"

echo "[*] Filesystem info..."
fsstat -o "$OFFSET" "$IMG" > "$OUT/fsstat.txt"

echo "[*] Directory listing..."
fls -o "$OFFSET" -r "$IMG" > "$OUT/full_listing.txt"

echo "[*] Deleted files..."
fls -o "$OFFSET" -r -d "$IMG" > "$OUT/deleted_files.txt"

echo "[*] Building timeline..."
fls -o "$OFFSET" -r -m "/" "$IMG" > "$OUT/bodyfile.txt"
mactime -b "$OUT/bodyfile.txt" -d > "$OUT/timeline.csv"

echo "[*] Extracting strings from unallocated..."
blkls -o "$OFFSET" "$IMG" | strings > "$OUT/unalloc_strings.txt"

echo "[*] Analysis complete: $OUT"
sha256sum "$OUT"/* > "$OUT/analysis_hashes.sha256"
```

---

## Analyzing Linux Swap from Image

```bash
# Identify swap partition in image
mmls /forensics/images/disk.dd
# Look for "Linux Swap" partition type

# Extract swap partition
mmcat /forensics/images/disk.dd 3 > /evidence/swap_partition.dd

# Verify it's swap
file /evidence/swap_partition.dd
# Linux/i386 swap file (new style)

# Search swap for strings
strings /evidence/swap_partition.dd | \
  grep -iE "password|secret|private" | head -20

# Carve files from swap
foremost -t all -i /evidence/swap_partition.dd \
  -o /evidence/swap_carved/

# Search for specific patterns
grep -boa "BEGIN.*PRIVATE KEY" /evidence/swap_partition.dd
grep -boa "mysql://\|postgres://\|redis://" /evidence/swap_partition.dd

# Extract browser data from swap
strings /evidence/swap_partition.dd | \
  grep -oP 'https?://[^\s"<>]+' | sort -u > /evidence/swap_urls.txt
```

---

## Analyzing Docker Images from Forensic Image

```bash
# Docker stores data in /var/lib/docker/

# Find Docker storage on mounted evidence
ls /forensics/mounted/var/lib/docker/
# containers/  images/  overlay2/  volumes/

# List containers
ls /forensics/mounted/var/lib/docker/containers/
# Each directory is a container ID

# Container configuration
cat /forensics/mounted/var/lib/docker/containers/*/config.v2.json | \
  python3 -m json.tool | head -30

# Container logs
cat /forensics/mounted/var/lib/docker/containers/*/*.log

# Docker images
ls /forensics/mounted/var/lib/docker/overlay2/

# Docker volumes (persistent data)
ls /forensics/mounted/var/lib/docker/volumes/

# Docker daemon configuration
cat /forensics/mounted/etc/docker/daemon.json

# Check for suspicious containers
# Look for: --privileged, --net=host, volume mounts to /
```

---

## Filesystem Comparison Analysis

```bash
# Compare evidence filesystem against known-good baseline

# Method 1: File list comparison
fls -o 2048 -r /forensics/images/evidence.dd | sort > evidence_files.txt
fls -o 2048 -r /forensics/images/baseline.dd | sort > baseline_files.txt
diff evidence_files.txt baseline_files.txt > file_diff.txt

# Method 2: Hash comparison
find /forensics/mounted_evidence -type f -exec sha256sum {} \; | \
  sort -k2 > evidence_hashes.txt
find /forensics/mounted_baseline -type f -exec sha256sum {} \; | \
  sort -k2 > baseline_hashes.txt
diff evidence_hashes.txt baseline_hashes.txt > hash_diff.txt

# Method 3: Using rsync for comparison
rsync -rvnc /forensics/mounted_baseline/ /forensics/mounted_evidence/ \
  > differences.txt

# Focus areas for comparison:
# - /usr/bin, /usr/sbin (modified binaries)
# - /etc (changed configurations)
# - /lib, /lib64 (modified libraries)
# - System service files
```

---

## Analyzing Encrypted Volumes from Image

```bash
# Detect LUKS encrypted partitions
mmls /forensics/images/disk.dd
# Identify partition offsets

# Check for LUKS header
dd if=/forensics/images/disk.dd bs=512 skip=2048 count=1 | \
  xxd | head -3
# 4c55 4b53 = LUKS magic bytes

# Extract encrypted partition
mmcat /forensics/images/disk.dd 2 > /evidence/encrypted_part.dd

# Attempt to open with known password/key
sudo cryptsetup luksOpen /evidence/encrypted_part.dd evidence_crypt
# Enter passphrase:

# If opened, mount and analyze
sudo mount -o ro /dev/mapper/evidence_crypt /forensics/decrypted/
# Analyze normally

# List LUKS metadata
sudo cryptsetup luksDump /evidence/encrypted_part.dd
# Shows key slots, cipher, hash algorithm

# If password unknown, document that partition exists
# Note: cracking LUKS is generally infeasible
```

---

## Reporting Analysis Results

```bash
# Generate structured analysis report

cat > /evidence/analysis_report.md << 'REPORT'
# Forensic Analysis Report
## Evidence: disk_image.dd

### Partition Layout
$(mmls /forensics/images/disk.dd)

### Filesystem Information
- Type: ext4
- Volume: $(fsstat -o 2048 /forensics/images/disk.dd | grep "Volume Name")
- Created: $(fsstat -o 2048 /forensics/images/disk.dd | grep "Filesystem created")

### Key Findings

#### Finding 1: Deleted Malware
- File: /tmp/.hidden/toolkit.tar.gz (inode 45678)
- Status: Deleted
- Content: Extracted and identified as penetration testing toolkit
- Hash: $(icat -o 2048 /forensics/images/disk.dd 45678 | sha256sum)

#### Finding 2: Web Shell
- File: /var/www/html/cmd.php (inode 56789)
- Status: Active
- Content: PHP web shell enabling remote command execution

### Timeline Summary
See attached timeline.csv for complete chronological analysis
REPORT

echo "Analysis report generated"
```

---

## Multi-Partition Analysis Workflow

```bash
# When image has multiple partitions, analyze each

IMG="/forensics/images/disk.dd"

# Get all partition offsets
mmls "$IMG" | grep "^0" | while read slot start length desc; do
  echo "=== Analyzing: $desc (offset: $start) ==="

  # Try to identify filesystem
  fsstat -o "$start" "$IMG" 2>/dev/null | head -5

  # List root directory
  echo "--- Root contents ---"
  fls -o "$start" "$IMG" 2>/dev/null | head -10

  # Check for deleted files
  echo "--- Deleted files ---"
  fls -o "$start" -d "$IMG" 2>/dev/null | head -10

  echo ""
done

# Don't forget:
# - EFI System Partition (FAT32, may have boot logs)
# - Swap partition (contains paged memory)
# - LVM physical volumes (need special handling)
# - Unallocated space between partitions
```
