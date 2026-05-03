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

# Data and File Structure

## Course: Linux Forensics - Day 2 (continued)
- Understanding file formats at the binary level
- Hex editors reveal hidden data within files
- File structure knowledge enables manual data recovery
- This module covers hex analysis, file internals, and metadata

---

## Why Understand File Structure?

- Files may be disguised with wrong extensions
- Malware hides inside legitimate-looking files
- Embedded objects can contain evidence
- Corrupted files may be partially recoverable
- Steganography hides data within files

```bash
# A file renamed to .jpg is still identifiable
cp /bin/ls /tmp/image.jpg
file /tmp/image.jpg
# /tmp/image.jpg: ELF 64-bit LSB pie executable, x86-64...
# file command checks magic bytes, not extension
```

---

## Magic Numbers Reference

![magic_numbers_reference](svg/courses/security/linux-forensics/05_data_and_file_structure/magic_numbers_reference.svg)

---

## Using `xxd` for Hex Analysis

```bash
# Basic hex dump
xxd suspicious_file | head -20

# Hex dump with specific offset and length
xxd -s 0 -l 64 suspicious_file

# Reverse hex dump (hex to binary)
echo "48 65 6c 6c 6f" | xxd -r -p > output.bin

# Search for hex pattern in file
xxd suspicious_file | grep "504b"  # Look for PK (ZIP)

# Compare two files in hex
diff <(xxd file1) <(xxd file2)

# Patch a binary using xxd
xxd suspicious_file > hex_dump.txt
# Edit hex_dump.txt
xxd -r hex_dump.txt > patched_file
```

---

## Using `hexdump`

```bash
# Canonical format (hex + ASCII)
hexdump -C file.bin | head -20

# Custom format: offset, hex bytes, ASCII
hexdump -e '"%08.8_ax: " 16/1 "%02x " "  |"' \
        -e '16/1 "%_p" "|\n"' file.bin

# Show only unique lines (suppress duplicates)
hexdump -C file.bin | uniq

# Skip to offset
hexdump -C -s 512 file.bin | head -10

# Limit output length
hexdump -C -n 256 file.bin
```

---

## Binary Editors: `bvi`

```bash
# bvi = binary vi - uses vi keybindings for hex editing
sudo apt install bvi
bvi suspicious_file

# Navigation (same as vi):
# h,j,k,l = move cursor
# /pattern = search forward
# ?pattern = search backward
# :set hex  = switch to hex display
# :set ascii = switch to ASCII display

# Search for string in hex
# /\x50\x4b\x03\x04   <- search for ZIP signature

# Goto specific address
# :0x1000   <- jump to offset 0x1000

# Save and quit
# :wq
```

---

## File Carving with `binwalk`

```bash
# Install binwalk
sudo apt install binwalk

# Scan file for embedded files and signatures
binwalk firmware.bin
# DECIMAL       HEXADECIMAL     DESCRIPTION
# 0             0x0             ELF, 64-bit LSB executable
# 147456        0x24000         gzip compressed data
# 524288        0x80000         JFFS2 filesystem

# Extract embedded files
binwalk -e firmware.bin

# Extract with specific signature
binwalk -D 'png image:png' disk_image.dd

# Recursive extraction
binwalk -Me firmware.bin

# Entropy analysis (detect encrypted/compressed sections)
binwalk -E firmware.bin
```

---

## Entropy Analysis

```bash
# High entropy = encrypted or compressed data
# Low entropy = plain text or empty space

# Using binwalk for entropy graph
binwalk -E suspicious_file

# Using ent for detailed entropy statistics
sudo apt install ent
ent suspicious_file
# Entropy = 7.998 bits per byte  <- nearly random (encrypted?)
# Entropy = 4.523 bits per byte  <- likely text
# Entropy = 0.001 bits per byte  <- nearly empty

# Quick entropy estimate with Python
python3 -c "
import math, collections, sys
data = open(sys.argv[1], 'rb').read()
freq = collections.Counter(data)
entropy = -sum((c/len(data)) * math.log2(c/len(data))
               for c in freq.values())
print(f'Entropy: {entropy:.4f} bits/byte')
" suspicious_file
```

---

## File System Metadata vs File Content

![file_system_metadata_vs_file_content](svg/courses/security/linux-forensics/05_data_and_file_structure/file_system_metadata_vs_file_content.svg)

---

## File System Metadata vs File Content: Details

- Deleting a file removes the directory entry and marks inode as free
- Data blocks are NOT overwritten immediately
- This is why deleted files can often be recovered

---

## Inode Structure in `ext4`

![inode_structure](svg/courses/security/linux-forensics/05_data_and_file_structure/inode_structure.svg)

---

## Inode Structure in `ext4`: Example

```bash
# View inode information
stat /etc/passwd
# File: /etc/passwd
# Size: 2345      Blocks: 8     IO Block: 4096  regular file
# Device: 802h/2050d  Inode: 131073  Links: 1
# Access: (0644/-rw-r--r--)  Uid: (0/root)  Gid: (0/root)
# Access: 2025-01-15 10:30:00.123456789 +0000
# Modify: 2025-01-10 08:00:00.987654321 +0000
# Change: 2025-01-10 08:00:00.987654321 +0000
#  Birth: 2024-06-01 12:00:00.000000000 +0000

# View detailed inode with debugfs
sudo debugfs -R "stat <131073>" /dev/sda2
# Shows block allocation, extent tree, etc.

# Count of total inodes vs used
df -i /
```

---

## Timestamps in Forensic Context

### MAC(B) Times
- **M**odify: content last changed
- **A**ccess: content last read
- **C**hange: metadata last changed (permissions, ownership)
- **B**irth: file creation time (`ext4` only)

```bash
# Detailed timestamps with nanosecond precision
stat -c "%n: mtime=%y atime=%x ctime=%z birth=%w" /etc/passwd

# Find files modified in time range
find / -newermt "2025-01-15 00:00" ! -newermt "2025-01-15 23:59" \
  -type f 2>/dev/null

# Find files accessed in last 24 hours
find / -atime -1 -type f 2>/dev/null

# Timestamp manipulation detection
# If mtime < ctime, timestamps may have been altered
# touch can set mtime and atime but NOT ctime
```

---

## Steganography Detection

```bash
# Steganography hides data within other files (images, audio)

# Check image for hidden data using steghide
sudo apt install steghide
steghide info image.jpg
# "image.jpg":
#   format: jpeg
#   capacity: 5.2 KB
#   embedded file "secret.txt"

# Extract hidden data
steghide extract -sf image.jpg
# Enter passphrase:

# Using stegdetect for automated detection
stegdetect image.jpg

# Using zsteg for PNG/BMP steganography
sudo gem install zsteg
zsteg image.png

# Compare file size to expected size for content
# An image much larger than expected may contain hidden data
```

---

## Document Metadata Analysis

```bash
# Microsoft Office documents (DOCX, XLSX, PPTX)
# These are ZIP archives containing XML

# Extract and examine
unzip -l document.docx
# Archive:  document.docx
#   Length      Date    Time    Name
#   ---------  ---------- -----   ----
#   1234       2025-01-15 10:30   [Content_Types].xml
#   567        2025-01-15 10:30   docProps/core.xml
#   890        2025-01-15 10:30   docProps/app.xml

# View document properties
unzip -p document.docx docProps/core.xml
# <dc:creator>John Doe</dc:creator>
# <dcterms:created>2025-01-15T10:30:00Z</dcterms:created>
# <cp:lastModifiedBy>Jane Smith</cp:lastModifiedBy>
```

---

## Deleted File Recovery Theory

```misc
Before Deletion:
Directory Entry -> Inode 12345 -> Data Blocks [100, 101, 102]
  "secret.txt"    (allocated)     (allocated)

After Deletion:
Directory Entry    Inode 12345 -> Data Blocks [100, 101, 102]
  (removed)        (marked free)  (marked free but data intact)

After Overwrite:
Directory Entry    Inode 12345 -> Data Blocks [100, 101, 102]
  (removed)        (reused)       (partially overwritten)
```

- Time between deletion and overwrite = recovery window
- On HDDs: data may persist for a long time
- On SSDs with TRIM: data may be wiped almost immediately

---

## File Recovery with `extundelete`

```bash
# Install extundelete
sudo apt install extundelete

# Recover all deleted files from partition
sudo extundelete /dev/sdb1 --restore-all

# Recover specific file
sudo extundelete /dev/sdb1 --restore-file home/user/secret.txt

# Recover files deleted after specific time
sudo extundelete /dev/sdb1 --restore-all \
  --after $(date -d "2025-01-15" +%s)

# Recover from image file
extundelete disk_image.dd --restore-all

# Note: works only on ext3/ext4 filesystems
# For other filesystems, use photorec or foremost
```

---

## File Recovery with `photorec`

```bash
# photorec - part of testdisk suite
sudo apt install testdisk

# Run photorec on a disk image
photorec disk_image.dd

# Interactive menu:
# 1. Select disk/image
# 2. Select partition type
# 3. Select filesystem type
# 4. Choose recovery destination
# 5. Start recovery

# photorec recovers based on file signatures
# Supports 400+ file types
# Ignores filesystem - works on raw data
# Output: recup_dir.1/, recup_dir.2/, etc.
```

---

## Analyzing Compressed and Archive Files

```bash
# Identify archive type
file archive.unknown
# archive.unknown: gzip compressed data

# List contents without extracting
tar -tzf archive.tar.gz
unzip -l archive.zip
7z l archive.7z

# Extract with preserved metadata
tar -xzf archive.tar.gz --preserve-permissions
unzip archive.zip

# Password-protected ZIP
unzip -P password archive.zip
# Or crack with fcrackzip
fcrackzip -b -c a -l 1-6 archive.zip

# Examine archive metadata
zipinfo archive.zip
zipdetails archive.zip  # Very detailed
```

---

## Exercise: File Structure Analysis

### Tasks:
1. Identify file types by magic numbers (not extensions)
1. Extract metadata from image and document files
1. Search a hex dump for specific patterns
1. Perform file carving on a sample disk image
1. Analyze entropy of suspicious files

```bash
#!/bin/bash
# File analysis script
TARGET_DIR="/evidence/files"

for f in "$TARGET_DIR"/*; do
  echo "=== $(basename $f) ==="
  echo "Type: $(file -b $f)"
  echo "Size: $(stat -c %s $f) bytes"
  echo "Magic: $(xxd -l 8 -p $f)"
  echo "Entropy: $(ent $f 2>/dev/null | head -1)"
  echo "Metadata:"
  exiftool -s "$f" 2>/dev/null | head -5
  echo ""
done
```

---

## Summary: Data and File Structure

- Magic numbers identify true file types regardless of extension
- Hex editors (`xxd`, `hexdump`, `bvi`) reveal raw file contents
- File structures (headers, footers, internal format) enable carving
- `binwalk` finds embedded files within other files
- Entropy analysis distinguishes encrypted, compressed, and plain data
- Inodes store metadata separately from file content
- Deleted files are recoverable until data blocks are overwritten
- MACB timestamps are crucial for forensic timelines
- Document metadata reveals authorship and modification history
- Steganography detection tools find hidden data in media files
- Archive files may contain evidence and require password cracking

---

## Advanced File Carving Techniques

```bash
# Header-footer carving
# Most common approach - find header, read until footer

# JPEG: Header FF D8 FF, Footer FF D9
# Search for all JPEGs manually
grep -Pbao '\xff\xd8\xff' disk_image.dd | head -10
# Shows byte offsets of all JPEG headers

# Extract JPEG at known offset
dd if=disk_image.dd bs=1 skip=1234567 count=50000 \
  of=extracted.jpg

# Validate extracted file
file extracted.jpg
identify extracted.jpg  # ImageMagick

# Fragment recovery
# When files span non-contiguous blocks, carving is harder
# Tools like bifragment carver handle 2-fragment files
```

---

## File System Journaling and Recovery

```bash
# ext4 journal contains recent filesystem operations
# Can reveal recently deleted or modified files

# Dump the journal
sudo debugfs -R "logdump -a" /dev/sda2 > /evidence/journal.txt

# View journal contents
sudo debugfs -R "logdump" /dev/sda2 | head -50

# Journal entries show:
# - Inode allocations/deallocations
# - Block allocations/deallocations
# - Directory entry modifications

# XFS journal
sudo xfs_logprint /dev/sda2

# Journal location
sudo debugfs -R "features" /dev/sda2
# has_journal
sudo dumpe2fs /dev/sda2 | grep "Journal"
# Journal inode: 8
# Journal size: 128M
```

---

## Alternate Data Streams and Extended Attributes

```bash
# Linux extended attributes can hide data
# Similar concept to NTFS Alternate Data Streams

# Set extended attribute (for awareness)
setfattr -n user.hidden_data -v "secret message" /tmp/innocent_file

# List extended attributes
getfattr -d /tmp/innocent_file
# user.hidden_data="secret message"

# Search for files with extended attributes
getfattr -R -d /home/ 2>/dev/null | grep -B1 "user\."

# Forensic scan for all extended attributes
find /forensics/mounted -exec getfattr -d {} \; 2>/dev/null | \
  grep -v "^$" > /evidence/xattrs.txt

# Security attributes
getfattr -n security.selinux /path/to/file 2>/dev/null
getfattr -n security.capability /path/to/file 2>/dev/null
```

---

## Sparse Files and Forensic Impact

```bash
# Sparse files don't allocate blocks for zero-filled regions
# This affects imaging and analysis

# Detect sparse files
ls -ls /path/to/file
# First number (blocks) much smaller than file size

# Example:
# 0 -rw-r--r-- 1 user user 1073741824 file.dat
# File claims 1GB but uses 0 blocks

# Check if an image is sparse
stat disk_image.dd
# Size: 536870912000  Blocks: 1048576  <- much fewer blocks

# Convert sparse to non-sparse (for forensic imaging)
cp --sparse=never source.dd destination.dd

# Forensic impact:
# - dd creates non-sparse images by default
# - Some tools create sparse images to save space
# - Sparse images may cause issues with some analysis tools
```

---

## Unicode and Encoding in Filenames

```bash
# Attackers use Unicode tricks to hide files

# Right-to-left override character
# Can make "harmless.txt" appear as "txt.sselmrah"
# Check for Unicode control characters
find / -regex '.*[^[:print:]].*' 2>/dev/null | head -10

# Homoglyph attacks (characters that look alike)
# Latin 'a' vs Cyrillic 'а'
# Check for non-ASCII filenames
find / -regex '.*[^\x00-\x7F].*' -type f 2>/dev/null | head -10

# Zero-width characters in filenames
python3 -c "
import os
for root, dirs, files in os.walk('/home'):
    for name in files:
        if any(ord(c) > 127 or ord(c) < 32 for c in name):
            print(f'Suspicious: {os.path.join(root, name)}'
                  f' ({[hex(ord(c)) for c in name]})')
" 2>/dev/null
```

---

## Image Format Forensics

```bash
# JPEG forensic analysis
# JFIF/EXIF header structure
xxd -l 64 photo.jpg
# ff d8 ff e0 = JFIF marker
# ff d8 ff e1 = EXIF marker

# Extract all EXIF data
exiftool -a -u -g1 photo.jpg

# JPEG quantization tables (camera identification)
exiftool -HtmlDump photo.jpg > photo_analysis.html

# PNG forensic analysis
# PNG chunks: IHDR, PLTE, IDAT, IEND
python3 -c "
import struct
with open('image.png', 'rb') as f:
    f.read(8)  # PNG signature
    while True:
        length_bytes = f.read(4)
        if len(length_bytes) < 4: break
        length = struct.unpack('>I', length_bytes)[0]
        chunk_type = f.read(4).decode('ascii')
        print(f'Chunk: {chunk_type}, Length: {length}')
        f.read(length + 4)  # data + CRC
"

# Check for appended data after IEND
# Data after the PNG IEND chunk is suspicious
```

---

## Email Forensics

```bash
# Parse email files

# Mbox format (common in Linux mail)
cat /var/mail/user
# From user@example.com Mon Jan 15 10:30:00 2025
# Subject: Important meeting
# ...

# Maildir format
ls /home/user/Maildir/{cur,new,tmp}/

# Parse email headers (find sender IP)
grep -E "^Received:|^From:|^To:|^Subject:|^Date:" \
  /var/mail/user | head -30

# Thunderbird email
ls /home/user/.thunderbird/*.default/
sqlite3 /home/user/.thunderbird/*.default/global-messages-db.sqlite \
  "SELECT subject, sender FROM messagesText_content LIMIT 20;"

# Extract attachments from mbox
munpack /var/mail/user  # From mpack package
```

---

## Database Forensics on Linux

```bash
# SQLite databases (most common on Linux)
# Firefox, Chrome, GNOME apps, many applications

# Identify SQLite files
file database.db
# database.db: SQLite 3.x database

# Open and examine
sqlite3 database.db
# .tables          - list all tables
# .schema          - show all table schemas
# .dump            - dump entire database

# Recover deleted SQLite records
# SQLite marks records as deleted but doesn't overwrite
sqlite3 database.db "PRAGMA freelist_count;"
# Non-zero = deleted data may be recoverable

# Use undark to recover deleted SQLite data
undark -i database.db > recovered_records.txt

# Search for SQLite databases on mounted image
find /forensics/mounted -name "*.sqlite" -o -name "*.db" \
  -o -name "*.sqlite3" 2>/dev/null
```

---

## Linux Executable Formats

```bash
# ELF (Executable and Linkable Format) - standard Linux binary
file /usr/bin/ls
# ELF 64-bit LSB pie executable, x86-64

# Shell scripts (text-based executables)
file /usr/bin/some_script
# POSIX shell script, ASCII text executable

# Python bytecode
file script.pyc
# Python 3.10 byte-compiled

# Java class files
file Main.class
# compiled Java class data, version 61.0

# .NET assemblies (via Mono or .NET Core)
file app.dll
# PE32 executable (DLL) (console) Mono/.Net assembly

# Understanding executable format helps:
# - Identify program capabilities
# - Determine static vs dynamic linking
# - Find embedded resources and strings
# - Detect packing or obfuscation
```

---

## Log File Formats

```bash
# Syslog format (RFC 3164/5424)
# <priority>timestamp hostname app[pid]: message
# Jan 15 10:30:00 server sshd[1234]: Accepted publickey...

# Apache Combined Log Format
# IP - user [date] "request" status size "referer" "agent"
# 192.168.1.50 - - [15/Jan/2025:10:30:00 +0000] "GET / HTTP/1.1" ...

# JSON structured logs (modern applications)
# {"timestamp":"2025-01-15T10:30:00Z","level":"error","msg":"..."}

# Binary log formats:
# wtmp/btmp - fixed-size records
utmpdump /var/log/wtmp
# systemd journal - binary with indexing
journalctl -o json-pretty

# CSV logs
# timestamp,source_ip,dest_ip,port,protocol,action
# Easily imported to spreadsheets and databases
```

---

## Analyzing Configuration File Changes

```bash
# Package-managed config files have expected defaults

# View default config vs current
dpkg --status openssh-server
# Conffiles:
#  /etc/ssh/sshd_config 12345abcdef...

# Check if config was modified from package default
dpkg -V openssh-server
# ??5?????? c /etc/ssh/sshd_config  <- modified

# View package default config
dpkg --fsys-tarfile /var/cache/apt/archives/openssh-server_*.deb | \
  tar -xf - ./etc/ssh/sshd_config -O > /tmp/default_sshd_config

# Compare current with default
diff /tmp/default_sshd_config /etc/ssh/sshd_config
# Shows exactly what was changed from defaults

# This technique works for any package-managed config file
# Changes from default = intentional modification
# Useful for detecting unauthorized configuration changes
```

---

## Filesystem Metadata Structures

```bash
# ext4 superblock contains filesystem-level metadata
sudo dumpe2fs -h /dev/sda2
# Filesystem created:       Wed Jun 01 12:00:00 2024
# Last mount time:          Mon Jan 15 08:15:00 2025
# Last write time:          Mon Jan 15 08:15:00 2025
# Mount count:              42
# Maximum mount count:      -1
# Last checked:             Wed Jun 01 12:00:00 2024
# First inode:              11
# Inode size:               256
# Default mount options:    user_xattr acl

# Group descriptors show block allocation
sudo dumpe2fs /dev/sda2 | grep -A5 "Group 0:"
# Group 0: (Blocks 0-32767)
#   Block bitmap at 1024 (+1024)
#   Inode bitmap at 1040 (+1040)
#   Inode table at 1056-1567 (+1056)
#   24576 free blocks, 8000 free inodes

# Forensic value:
# - Filesystem creation date = OS installation date
# - Mount count tracks system usage
# - Error flags indicate unclean shutdowns
```

---

## Analyzing Symbolic and Hard Links

```bash
# Symbolic links point to file paths
# Hard links share the same inode

# Find symbolic links
find /forensics/mounted -type l -ls 2>/dev/null | head -20
# Look for symlinks pointing to unusual targets

# Find broken symbolic links (target deleted)
find /forensics/mounted -xtype l 2>/dev/null | head -10

# Find hard links (same inode, multiple names)
find /forensics/mounted -type f -links +1 -ls 2>/dev/null | head -20

# Hard links used for hiding files:
# An attacker can create a hard link to a file in /etc
# The linked copy in /tmp looks like a normal file
# Deleting one copy doesn't affect the other

# Check for hard links across directories
find /forensics/mounted -type f -links +1 -printf '%i %n %p\n' | \
  sort -n | head -20
# Same inode number = same file content
```

---

## Analyzing Systemd Coredump from Image

```bash
# Check for core dumps on forensic image
ls /forensics/mounted/var/lib/systemd/coredump/

# Core dump journal entries
journalctl --directory=/forensics/mounted/var/log/journal/ | \
  grep -i "coredump\|core dump\|segfault"

# Decompress stored core dumps
for f in /forensics/mounted/var/lib/systemd/coredump/*.zst; do
  zstd -d "$f" -o "/evidence/coredumps/$(basename ${f%.zst})"
done

# Analyze core dump
file /evidence/coredumps/core.suspicious.6789.*
gdb /forensics/mounted/tmp/.hidden/tool \
  /evidence/coredumps/core.suspicious.6789.*

# Core dump metadata
# journal entry includes:
# - Process name and PID
# - Signal that caused crash
# - Executable path
# - Timestamp
# - Core dump file location
```

---

## Superblock Structure

![superblock_structure](svg/courses/security/linux-forensics/05_data_and_file_structure/superblock_structure.svg)

---

## Journaling Filesystems

![journaling_filesystems](svg/courses/security/linux-forensics/05_data_and_file_structure/journaling_filesystems.svg)
