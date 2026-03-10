# Forensic Data Carving

## Course: Linux Forensics - Day 3
- Data carving recovers files from raw disk data
- Works without filesystem metadata
- Essential when filesystems are damaged or evidence is deleted
- This module covers carving tools, techniques, and system info files

---

## What is Data Carving?

```text
Raw Disk Image:
+-------+-------+-------+-------+-------+-------+-------+
| Boot  | Used  | Free  | Used  | Free  | Free  | Used  |
| Sector| Block | Block | Block | Block | Block | Block |
+-------+-------+-------+-------+-------+-------+-------+
                    |                |       |
            +-------+       +-------+   +---+
            | JPEG          | PDF       | ZIP
            | header        | header    | header
            | found!        | found!    | found!
            +-------+       +-------+   +---+
```

- Scans raw data for file signatures (headers/footers)
- Ignores filesystem structure entirely
- Can recover files from formatted or corrupted drives

---

## Carving Process Overview

1. **Identify** target media and create forensic image
2. **Select** carving tool and configure file types
3. **Scan** the image for file headers and footers
4. **Extract** identified files
5. **Validate** recovered files (open, check integrity)
6. **Document** findings and recovery statistics

```bash
# Typical workflow
sudo dd if=/dev/sdb of=/evidence/disk.dd bs=4M status=progress
sha256sum /evidence/disk.dd > /evidence/disk.dd.sha256
foremost -t all -i /evidence/disk.dd -o /evidence/carved/
cat /evidence/carved/audit.txt
```

---

## `foremost` - File Carving Tool

```bash
# Install foremost
sudo apt install foremost

# Basic usage - carve all known types
foremost -i disk_image.dd -o /evidence/carved/

# Carve specific file types
foremost -t jpg,png,pdf,doc,zip -i disk_image.dd \
  -o /evidence/carved/

# Supported types:
# jpg, gif, png, bmp     - Images
# pdf, doc, docx, xls    - Documents
# zip, rar, tar          - Archives
# avi, mpg, mov, mp4     - Video
# wav, mp3               - Audio
# htm, cpp, java         - Source code
# exe, dll               - Windows executables
# ole, all               - OLE/all types
```

---

## `foremost` Configuration

```bash
# Configuration file
cat /etc/foremost.conf

# Format: extension  case_sensitive  max_size  header  footer
# Example entries:
# jpg  y  200000  \xff\xd8\xff  \xff\xd9
# png  y  500000  \x89\x50\x4e\x47  \x49\x45\x4e\x44

# Custom configuration for specific needs
cat > /tmp/custom_foremost.conf << 'EOF'
# Carve only PDFs and JPEGs, with custom max sizes
pdf  y  20000000  %PDF  %%EOF
jpg  y  5000000   \xff\xd8\xff  \xff\xd9
EOF

foremost -c /tmp/custom_foremost.conf \
  -i disk_image.dd -o /evidence/carved/
```

---

## `foremost` Output Analysis

```bash
# Audit file shows carving results
cat /evidence/carved/audit.txt
# Foremost version 1.5.7
# Audit File
# 
# Foremost started at Mon Jan 15 10:30:00 2025
# Invocation: foremost -i disk_image.dd -o /evidence/carved/
# 
# Output directory: /evidence/carved/
# Configuration file: /etc/foremost.conf
# 
# File: disk_image.dd
# Length: 500 GB (536870912000 bytes)
# 
# Num      Name (bs=512)    Size    File Offset     Comment
# 0:  00012345.jpg         234 KB  6320640         
# 1:  00012567.jpg         156 KB  6434304         
# 2:  00089012.pdf         1.2 MB  45574144        
#
# 345 FILES EXTRACTED

ls -la /evidence/carved/jpg/
ls -la /evidence/carved/pdf/
```

---

## `scalpel` - Fast File Carving

```bash
# Install scalpel
sudo apt install scalpel

# Configure scalpel (edit the config to enable desired types)
sudo cp /etc/scalpel/scalpel.conf /tmp/scalpel.conf
# Uncomment desired file types in the config

# Run scalpel
scalpel -c /tmp/scalpel.conf -o /evidence/scalpel_output/ \
  disk_image.dd

# Scalpel advantages over foremost:
# - Faster on large images
# - More efficient memory usage
# - Support for regular expressions in headers/footers
# - Better handling of fragmented files
```

---

## `bulk_extractor` - Advanced Extraction

```bash
# bulk_extractor extracts features without parsing filesystem
sudo apt install bulk-extractor

# Run on disk image
bulk_extractor -o /evidence/bulk_output/ disk_image.dd

# Extracts:
# - Email addresses
# - URLs and domain names
# - Credit card numbers
# - Phone numbers
# - GPS coordinates from images
# - Windows registry entries
# - Network packets (pcap)
# - Base64 and Base16 encoded data

# View results
ls /evidence/bulk_output/
# email.txt, url.txt, ccn.txt, telephone.txt,
# domain.txt, gps.txt, packets.pcap, etc.
```

---

## `bulk_extractor` Output Analysis

```bash
# Email addresses found
cat /evidence/bulk_output/email.txt
# Offset  Email
# 1234567 user@example.com
# 2345678 admin@target.org

# URLs found
cat /evidence/bulk_output/url.txt
# Offset  URL
# 3456789 http://malicious-site.com/payload

# Feature files are tab-delimited
# Can be imported into spreadsheets or databases

# Generate histogram reports
bulk_extractor -o /evidence/bulk_output/ -R disk_image.dd
cat /evidence/bulk_output/url_histogram.txt
# n=25  http://www.google.com
# n=15  http://internal-server.local
# n=3   http://suspicious-domain.com/beacon
```

---

## Carving from Memory Dumps

```bash
# File carving also works on RAM dumps
# Memory may contain recently opened files

# Carve files from memory dump
foremost -t all -i memory_dump.raw -o /evidence/mem_carved/

# Look for specific data types in memory
strings memory_dump.raw | grep -iE "password|secret|key"

# Carve network packets from memory
bulk_extractor -o /evidence/mem_features/ memory_dump.raw
ls /evidence/mem_features/packets.pcap

# Open carved packets in Wireshark
wireshark /evidence/mem_features/packets.pcap
```

---

## System Information Files

```bash
# Hostname and domain
cat /etc/hostname
cat /etc/hosts
cat /etc/resolv.conf

# Operating system identification
cat /etc/os-release
# NAME="Ubuntu"
# VERSION="22.04.3 LTS (Jammy Jellyfish)"
# ID=ubuntu
# VERSION_ID="22.04"

cat /etc/lsb-release    # Ubuntu/Debian
cat /etc/redhat-release  # RHEL/CentOS

# Kernel version
uname -a
cat /proc/version
```

---

## System Configuration Files

```bash
# Sysctl (kernel parameters)
cat /etc/sysctl.conf
sysctl -a 2>/dev/null | head -20
# Key forensic indicators:
# net.ipv4.ip_forward = 1  (routing enabled - suspicious?)
# kernel.randomize_va_space = 0  (ASLR disabled - suspicious!)

# PAM configuration (authentication modules)
ls /etc/pam.d/
cat /etc/pam.d/common-auth
cat /etc/pam.d/sshd

# nsswitch (name service resolution order)
cat /etc/nsswitch.conf

# Security limits
cat /etc/security/limits.conf
```

---

## User Information Files

```bash
# User account information
cat /etc/passwd     # All accounts
cat /etc/shadow     # Password hashes (root only)
cat /etc/group      # Group memberships
cat /etc/gshadow    # Group passwords

# Login defaults
cat /etc/login.defs
# PASS_MAX_DAYS  99999
# PASS_MIN_DAYS  0
# PASS_WARN_AGE  7
# UID_MIN        1000
# UID_MAX        60000

# User skeleton (default files for new users)
ls -la /etc/skel/

# Adduser configuration
cat /etc/adduser.conf
```

---

## Cron and Scheduled Task Files

```bash
# System crontab
cat /etc/crontab
# SHELL=/bin/sh
# PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin
# 17 * * * * root cd / && run-parts --report /etc/cron.hourly

# Cron directories
for dir in /etc/cron.d /etc/cron.daily /etc/cron.hourly \
           /etc/cron.weekly /etc/cron.monthly; do
  echo "=== $dir ==="
  ls -la "$dir/"
done

# Per-user crontabs
for f in /var/spool/cron/crontabs/*; do
  echo "=== $(basename $f) ==="
  cat "$f"
done

# At jobs
ls -la /var/spool/at/
for f in /var/spool/at/*; do cat "$f"; done
```

---

## Network Configuration Files

```bash
# Network interfaces
cat /etc/network/interfaces  # Debian-style
ls /etc/NetworkManager/system-connections/  # NetworkManager
ls /etc/netplan/  # Ubuntu netplan

# Firewall rules
cat /etc/iptables/rules.v4
cat /etc/nftables.conf

# Hosts file (static DNS)
cat /etc/hosts
# 127.0.0.1 localhost
# 10.0.0.50 malware-c2.evil.com  # <-- suspicious entry!

# SSH configuration
cat /etc/ssh/sshd_config

# Proxy settings
cat /etc/environment | grep -i proxy
cat /etc/apt/apt.conf.d/*proxy* 2>/dev/null
```

---

## Service and Daemon Configuration

```bash
# Systemd service files (check for malicious services)
find /etc/systemd/system/ -name "*.service" -exec cat {} \;

# inetd/xinetd (legacy network services)
cat /etc/inetd.conf 2>/dev/null
ls /etc/xinetd.d/ 2>/dev/null

# init.d scripts
ls -la /etc/init.d/

# rc.local (legacy startup script)
cat /etc/rc.local

# Systemd generators
ls /etc/systemd/system-generators/

# Persistence check: look for unusual services
systemctl list-unit-files --type=service | grep enabled
# Compare against known-good baseline
```

---

## File Integrity Databases

```bash
# AIDE (Advanced Intrusion Detection Environment)
sudo apt install aide

# Initialize AIDE database (baseline)
sudo aideinit
# Creates /var/lib/aide/aide.db.new

# Check for changes
sudo aide --check
# Output shows:
# Added: /tmp/suspicious_file
# Changed: /usr/bin/ls  <-- binary modified!
# Removed: /etc/cron.d/legitimate-job

# Tripwire (alternative to AIDE)
sudo apt install tripwire
sudo tripwire --init
sudo tripwire --check

# rpm verification (RHEL/CentOS)
rpm -Va  # Verify all packages
```

---

## Carving Specific Data Types

```bash
# Carve email files (mbox format)
grep -c "^From " disk_image.dd  # Count emails

# Extract all strings from unallocated space
blkls disk_image.dd | strings > unalloc_strings.txt

# Search for credit card numbers
grep -oP '\b[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b' \
  unalloc_strings.txt

# Search for email addresses
grep -oP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' \
  unalloc_strings.txt

# Search for URLs
grep -oP 'https?://[^\s"<>]+' unalloc_strings.txt

# Search for IP addresses
grep -oP '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b' unalloc_strings.txt
```

---

## Automated System Survey Script

```bash
#!/bin/bash
# Comprehensive system information collection
OUTPUT="/evidence/system_survey_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTPUT"

echo "Collecting system info..."
uname -a > "$OUTPUT/uname.txt"
cat /etc/os-release > "$OUTPUT/os-release.txt"
cat /etc/hostname > "$OUTPUT/hostname.txt"
date > "$OUTPUT/collection_time.txt"

echo "Collecting user info..."
cat /etc/passwd > "$OUTPUT/passwd.txt"
cat /etc/group > "$OUTPUT/group.txt"
last > "$OUTPUT/last_logins.txt"
lastlog > "$OUTPUT/lastlog.txt"

echo "Collecting network info..."
ip addr > "$OUTPUT/ip_addr.txt"
ip route > "$OUTPUT/ip_route.txt"
ss -tunapl > "$OUTPUT/connections.txt"
cat /etc/hosts > "$OUTPUT/hosts.txt"
cat /etc/resolv.conf > "$OUTPUT/resolv.txt"

echo "Collecting service info..."
systemctl list-units --all > "$OUTPUT/services.txt"
systemctl list-timers > "$OUTPUT/timers.txt"
crontab -l > "$OUTPUT/crontab_root.txt" 2>/dev/null

echo "Survey complete: $OUTPUT"
```

---

## Exercise: Data Carving Lab

### Tasks:
1. Create a test image with various file types
2. Delete some files and carve them back
3. Use `foremost` to recover JPEG and PDF files
4. Use `bulk_extractor` to find email addresses and URLs
5. Analyze carving results and validate recovered files

```bash
# Create test image
dd if=/dev/zero of=/tmp/test.dd bs=1M count=100
mkfs.ext4 /tmp/test.dd
sudo mount -o loop /tmp/test.dd /mnt/test
# Add files, then delete some, unmount
sudo umount /mnt/test

# Carve deleted files
foremost -t all -i /tmp/test.dd -o /tmp/carved/
cat /tmp/carved/audit.txt
```

---

## Summary: Forensic Data Carving

- Data carving recovers files using signatures, not filesystem metadata
- `foremost` is the classic carving tool with broad file type support
- `scalpel` offers faster performance for large images
- `bulk_extractor` extracts structured data (emails, URLs, cards)
- Carving configuration can be customized for specific investigations
- System information files reveal OS state and configuration
- User information files show accounts, privileges, and history
- Scheduled tasks (`cron`, timers, `at`) may indicate persistence
- Network configuration files reveal connectivity and firewall rules
- File integrity tools (AIDE, Tripwire) detect unauthorized changes
- Always validate carved files before including in evidence

---

## Custom Carving with `scalpel`

```bash
# Create custom scalpel configuration
cat > /tmp/custom_scalpel.conf << 'EOF'
# Custom file types for investigation

# SSH private keys
ssh_key  y  10000  -----BEGIN\x20OPENSSH\x20PRIVATE  -----END\x20OPENSSH\x20PRIVATE\x20KEY-----

# PGP keys
pgp_key  y  50000  -----BEGIN\x20PGP  -----END\x20PGP

# Python scripts
py       y  500000  #!/usr/bin/python  \x00\x00\x00\x00

# Shell scripts
sh       y  200000  #!/bin/bash  \x00\x00\x00\x00
sh2      y  200000  #!/bin/sh    \x00\x00\x00\x00

# SQLite databases
sqlite   y  50000000  SQLite\x20format\x203

# Tar archives
tar      y  100000000  ustar
EOF

scalpel -c /tmp/custom_scalpel.conf -o /evidence/custom_carved/ \
  disk_image.dd
```

---

## Validating Carved Files

```bash
# Not all carved files are valid - validate them

# Check file type
for f in /evidence/carved/jpg/*; do
  actual=$(file -b "$f")
  if ! echo "$actual" | grep -qi "jpeg\|jpg"; then
    echo "INVALID: $f ($actual)"
  fi
done

# Try to render images
for f in /evidence/carved/jpg/*; do
  identify "$f" 2>/dev/null || echo "BROKEN: $f"
done

# Validate PDFs
for f in /evidence/carved/pdf/*; do
  pdfinfo "$f" 2>/dev/null || echo "BROKEN: $f"
done

# Check file sizes (too small = likely false positive)
find /evidence/carved -size -100c -type f -exec echo "TINY: {}" \;

# Generate thumbnails for visual review
for f in /evidence/carved/jpg/*.jpg; do
  convert "$f" -thumbnail 200x200 \
    "/evidence/carved/thumbnails/$(basename $f)" 2>/dev/null
done
```

---

## Carving from Unallocated Space

```bash
# The Sleuth Kit's blkls extracts unallocated blocks

# Extract unallocated space
blkls -o 2048 /forensics/images/disk.dd > \
  /evidence/unallocated.raw

# Size of unallocated space
ls -lh /evidence/unallocated.raw

# Carve files from unallocated space only
foremost -t all -i /evidence/unallocated.raw \
  -o /evidence/unalloc_carved/

# Search unallocated space for patterns
strings /evidence/unallocated.raw | grep -i "password" | \
  sort -u > /evidence/unalloc_passwords.txt

# Extract slack space separately
blkls -s -o 2048 /forensics/images/disk.dd > \
  /evidence/slack.raw

# Carve from slack space
foremost -t all -i /evidence/slack.raw \
  -o /evidence/slack_carved/
```

---

## Recovering Specific File Types

```bash
# Targeted recovery for common evidence types

# Recover all images (photos may contain evidence)
foremost -t jpg,png,gif,bmp,tif \
  -i disk_image.dd -o /evidence/images/

# Recover documents
foremost -t doc,docx,pdf,xls,xlsx,ppt,pptx \
  -i disk_image.dd -o /evidence/documents/

# Recover archives (may contain packed evidence)
foremost -t zip,rar,tar,gz \
  -i disk_image.dd -o /evidence/archives/

# Recover executables (potential malware)
foremost -t exe,elf \
  -i disk_image.dd -o /evidence/executables/

# After carving, analyze each category
echo "=== Images ===" && ls /evidence/images/ | wc -l
echo "=== Documents ===" && ls /evidence/documents/ | wc -l
echo "=== Archives ===" && ls /evidence/archives/ | wc -l
echo "=== Executables ===" && ls /evidence/executables/ | wc -l
```

---

## Photorec Advanced Usage

```bash
# Photorec with command-line options
photorec /cmd disk_image.dd partition_type,none \
  fileopt,jpg,enable \
  fileopt,pdf,enable \
  search

# Photorec file type support:
# Over 440 file types recognized including:
# - Office documents (doc, xls, ppt, odt)
# - Images (jpg, png, gif, tif, bmp, raw)
# - Video (avi, mp4, mkv, mov)
# - Audio (mp3, wav, flac, ogg)
# - Archives (zip, rar, 7z, tar)
# - Databases (sqlite, mdb)
# - Executables (exe, elf, mach-o)
# - Email (pst, mbox, eml)

# Photorec vs foremost:
# Photorec: more file types, smarter parsing
# foremost: faster, simpler, customizable config
```

---

## Data Carving Challenges

```bash
# Challenge 1: File fragmentation
# Files stored in non-contiguous blocks
# Header-footer carving may produce corrupt files
# Solution: Fragment recovery tools, bifragment carver

# Challenge 2: Encrypted/compressed data
# Cannot carve from encrypted volumes without key
# Compressed data has high entropy, hard to distinguish
# Solution: Check for encryption, try known passwords

# Challenge 3: False positives
# Random data may match file signatures
# Solution: Validate carved files, check file structure

# Challenge 4: Overwritten data
# Partially overwritten files produce corrupt output
# Solution: Accept partial recovery, document limitations

# Challenge 5: SSD TRIM
# Deleted data may be zeroed by TRIM command
# Solution: Image quickly after seizure, check TRIM status
cat /sys/block/sda/queue/discard_max_bytes
# 0 = TRIM not supported/enabled
```

---

## Carving from Network Captures

```bash
# PCAP files contain transferred files

# Extract files from HTTP traffic with tcpflow
sudo apt install tcpflow
tcpflow -r /evidence/capture.pcap -o /evidence/http_flows/

# Extract with NetworkMiner (if available)
# Or use Wireshark: File -> Export Objects -> HTTP

# Carve files from raw PCAP
foremost -t all -i /evidence/capture.pcap \
  -o /evidence/pcap_carved/

# Extract specific file types from network traffic
tshark -r /evidence/capture.pcap \
  --export-objects "http,/evidence/http_objects/"

# Extract SMTP attachments
tshark -r /evidence/capture.pcap \
  --export-objects "smb,/evidence/smb_objects/" 2>/dev/null

# Look for encoded data transfers
strings /evidence/capture.pcap | \
  grep -oP '[A-Za-z0-9+/]{100,}={0,2}' | \
  while read b64; do
    echo "$b64" | base64 -d 2>/dev/null | file -
  done
```

---

## Carving Deleted Emails

```bash
# Email recovery from disk images

# Search for email headers in raw image
grep -boa "^From: \|^To: \|^Subject: \|^Date: " \
  /forensics/images/disk.dd | head -20

# Carve mbox-format emails
grep -Pboa "^From [^\n]+ \d{4}\n" /forensics/images/disk.dd | \
  head -10

# Search unallocated space for email content
blkls -o 2048 /forensics/images/disk.dd | \
  strings | grep -B2 -A5 "^Subject:" | head -50

# Thunderbird profile recovery
find /forensics/mounted -path "*.thunderbird*" -name "*.msf" \
  2>/dev/null
find /forensics/mounted -path "*.thunderbird*" -name "INBOX" \
  2>/dev/null

# Parse recovered mbox files
formail -s head -20 < /evidence/recovered_inbox
```

---

## Carving Encrypted and Compressed Data

```bash
# Encrypted data appears as high-entropy random bytes
# Cannot be carved by signature alone

# Detect encrypted files by entropy
for f in /evidence/carved/*; do
  entropy=$(ent "$f" 2>/dev/null | head -1 | awk '{print $NF}')
  if (( $(echo "$entropy > 7.9" | bc -l) )); then
    echo "HIGH ENTROPY (possibly encrypted): $f ($entropy)"
  fi
done

# Compressed files CAN be carved by signature
# gzip: 1f 8b
# bzip2: 42 5a 68
# xz: fd 37 7a 58 5a
# zstd: 28 b5 2f fd

# Try to decompress carved files
for f in /evidence/carved/unknown/*; do
  gzip -t "$f" 2>/dev/null && echo "GZIP: $f"
  bzip2 -t "$f" 2>/dev/null && echo "BZIP2: $f"
  xz -t "$f" 2>/dev/null && echo "XZ: $f"
  zstd -t "$f" 2>/dev/null && echo "ZSTD: $f"
done
```

---

## Documenting Carving Results

```bash
# Professional documentation of carving results

cat > /evidence/carving_report.txt << 'EOF'
FORENSIC DATA CARVING REPORT
==============================
Date: $(date -u)
Examiner: [Name]
Source: disk_image.dd (SHA-256: abc123...)
Tool: foremost 1.5.7

Configuration: Default (/etc/foremost.conf)
Target: All file types

RESULTS SUMMARY:
Type      | Count | Size Range      | Valid
----------|-------|-----------------|------
JPEG      | 245   | 10KB - 5.2MB    | 230
PNG       | 34    | 5KB - 2.1MB     | 31
PDF       | 18    | 50KB - 15MB     | 15
ZIP       | 12    | 1KB - 500MB     | 10
DOC       | 8     | 100KB - 2MB     | 7
ELF       | 3     | 50KB - 1.5MB    | 3

VALIDATION: Each carved file was tested for validity.
Files failing validation were retained for manual review.

NOTABLE FILES:
- carved/jpg/00012345.jpg: Photo with GPS coordinates
- carved/pdf/00089012.pdf: Financial document
- carved/zip/00123456.zip: Password-protected archive
EOF
```
