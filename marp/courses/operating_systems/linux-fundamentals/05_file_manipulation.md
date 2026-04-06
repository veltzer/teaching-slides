# File and Disk Manipulation
## Essential Commands and Power Tools

---

## Basic File Operations

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="70" width="90" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="140" y="70" width="90" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="260" y="70" width="90" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="380" y="70" width="90" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="500" y="70" width="80" height="50" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="65" y="92" text-anchor="middle" font-size="11" font-weight="bold">cp / mv</text>
  <text x="65" y="107" text-anchor="middle" font-size="10">copy / move</text>
  <text x="185" y="92" text-anchor="middle" font-size="11" font-weight="bold">rm</text>
  <text x="185" y="107" text-anchor="middle" font-size="10">remove</text>
  <text x="305" y="92" text-anchor="middle" font-size="11" font-weight="bold">mkdir</text>
  <text x="305" y="107" text-anchor="middle" font-size="10">create dir</text>
  <text x="425" y="92" text-anchor="middle" font-size="11" font-weight="bold">touch</text>
  <text x="425" y="107" text-anchor="middle" font-size="10">create file</text>
  <text x="540" y="92" text-anchor="middle" font-size="11" font-weight="bold">ln</text>
  <text x="540" y="107" text-anchor="middle" font-size="10">link</text>
  <text x="300" y="35" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Core File Operations</text>
  <rect x="20" y="145" width="560" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3" opacity="0.5"/>
  <text x="300" y="167" text-anchor="middle" font-size="11" fill="#333">All operate on the filesystem tree: files, directories, and links</text>
</svg>

---

## Listing Files: ls

```bash
# Basic listing
ls

# Long format
ls -l

# Show hidden files
ls -la

# Human-readable sizes
ls -lh

# Sort by time
ls -lt

# Sort by size
ls -lS

# Recursive listing
ls -R
```

Output example:

```console
-rw-r--r-- 1 user group 4.0K Nov 19 10:00 file.txt
drwxr-xr-x 2 user group 4.0K Nov 19 09:45 directory
```

---

## Viewing File Contents

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="25" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">File Viewing Tools</text>
  <rect x="30" y="45" width="100" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="67" text-anchor="middle" font-size="11" font-weight="bold">cat</text>
  <text x="80" y="82" text-anchor="middle" font-size="10">entire file</text>
  <rect x="155" y="45" width="100" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="205" y="67" text-anchor="middle" font-size="11" font-weight="bold">less/more</text>
  <text x="205" y="82" text-anchor="middle" font-size="10">paged view</text>
  <rect x="280" y="45" width="100" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="330" y="67" text-anchor="middle" font-size="11" font-weight="bold">head</text>
  <text x="330" y="82" text-anchor="middle" font-size="10">first N lines</text>
  <rect x="405" y="45" width="100" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="455" y="67" text-anchor="middle" font-size="11" font-weight="bold">tail</text>
  <text x="455" y="82" text-anchor="middle" font-size="10">last N lines</text>
  <rect x="30" y="120" width="475" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="5" opacity="0.7"/>
  <text x="267" y="137" text-anchor="middle" font-size="11" font-weight="bold">tail -f logfile.txt</text>
  <text x="267" y="152" text-anchor="middle" font-size="10">Follow mode: watch file updates in real time</text>
  <line x1="455" y1="100" x2="455" y2="120" stroke="#333" stroke-width="1.5" stroke-dasharray="4,3"/>
</svg>

Examples:

```bash
# View entire file
cat file.txt

# Page through file
less file.txt

# First 10 lines
head file.txt

# Last 10 lines
tail file.txt

# Follow file updates
tail -f log.txt
```

---

## File Creation and Modification

```bash
# Create empty file
touch newfile.txt

# Create directory
mkdir new_directory

# Create nested directories
mkdir -p path/to/new/directory

# Copy files
cp source.txt destination.txt

# Copy directories
cp -r source_dir destination_dir

# Move/rename files
mv old.txt new.txt

# Move directories
mv old_dir new_dir
```

---

## Disk Usage Commands

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="25" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Disk Usage: df vs du</text>
  <rect x="40" y="45" width="220" height="130" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="150" y="70" text-anchor="middle" font-size="12" font-weight="bold">df -h (filesystem)</text>
  <rect x="60" y="82" width="180" height="20" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="96" text-anchor="middle" font-size="10">/dev/sda1  50G  30G  20G  60%</text>
  <rect x="60" y="108" width="180" height="20" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="122" text-anchor="middle" font-size="10">/dev/sdb1 100G  80G  20G  80%</text>
  <rect x="60" y="134" width="180" height="20" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="150" y="148" text-anchor="middle" font-size="10">tmpfs       4G   1G   3G  25%</text>
  <rect x="340" y="45" width="220" height="130" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="450" y="70" text-anchor="middle" font-size="12" font-weight="bold">du -sh (directory)</text>
  <rect x="360" y="82" width="180" height="20" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="450" y="96" text-anchor="middle" font-size="10">2.1G  /home/user/docs</text>
  <rect x="360" y="108" width="180" height="20" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="450" y="122" text-anchor="middle" font-size="10">500M  /home/user/src</text>
  <rect x="360" y="134" width="180" height="20" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="450" y="148" text-anchor="middle" font-size="10">50M   /home/user/tmp</text>
</svg>

Examples:

```bash
# Check filesystem usage
df -h

# Directory size
du -sh directory

# Top 10 largest directories
du -h | sort -rh | head -n 10
```

---

## Text Processing Tools

## tr (translate)

```bash
# Convert to uppercase
echo "hello" | tr 'a-z' 'A-Z'

# Delete characters
echo "hello 123" | tr -d '0-9'

# Squeeze repeats
echo "hello    world" | tr -s ' '
```

## cut

```bash
# Extract fields from CSV
cut -d',' -f1,3 file.csv

# Extract characters
cut -c1-5 file.txt
```

---

## Sorting and Uniqueness

### sort

```bash
# Basic sort
sort file.txt

# Numeric sort
sort -n numbers.txt

# Reverse sort
sort -r file.txt

# Sort by field
sort -k2 data.txt
```

### uniq

```bash
# Show unique lines
sort file.txt | uniq

# Count occurrences
sort file.txt | uniq -c

# Show duplicates only
sort file.txt | uniq -d
```

---

## Finding Files

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="25" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">find Command: Search the File Tree</text>
  <defs>
    <marker id="arrowfind" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="220" y="40" width="160" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="63" text-anchor="middle" font-size="11" font-weight="bold">find /path</text>
  <line x1="260" y1="75" x2="120" y2="105" stroke="#333" stroke-width="1.5" marker-end="url(#arrowfind)"/>
  <line x1="300" y1="75" x2="300" y2="105" stroke="#333" stroke-width="1.5" marker-end="url(#arrowfind)"/>
  <line x1="340" y1="75" x2="480" y2="105" stroke="#333" stroke-width="1.5" marker-end="url(#arrowfind)"/>
  <rect x="40" y="105" width="150" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="115" y="127" text-anchor="middle" font-size="10">-name "*.log"</text>
  <rect x="220" y="105" width="160" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="127" text-anchor="middle" font-size="10">-type f -size +1M</text>
  <rect x="410" y="105" width="150" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="485" y="127" text-anchor="middle" font-size="10">-mtime -7</text>
  <line x1="115" y1="140" x2="220" y2="165" stroke="#333" stroke-width="1.5" marker-end="url(#arrowfind)"/>
  <line x1="300" y1="140" x2="300" y2="160" stroke="#333" stroke-width="1.5" marker-end="url(#arrowfind)"/>
  <line x1="485" y1="140" x2="380" y2="165" stroke="#333" stroke-width="1.5" marker-end="url(#arrowfind)"/>
  <rect x="200" y="160" width="200" height="30" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="180" text-anchor="middle" font-size="11" font-weight="bold">-exec command {} \;</text>
</svg>

Examples:

```bash
# Find by name
find . -name "*.txt"

# Find by type
find . -type d

# Find by size
find . -size +1M

# Find and execute
find . -name "*.log" -exec rm {} \;
```

---

## Text Search with grep

```bash
# Basic search
grep "pattern" file.txt

# Recursive search
grep -r "pattern" directory/

# Case insensitive
grep -i "pattern" file.txt

# Show line numbers
grep -n "pattern" file.txt

# Show context
grep -C 2 "pattern" file.txt

# Extended regex
grep -E "pattern1|pattern2" file.txt
```

---

## Advanced Text Processing

### sed (Stream Editor)

```bash
# Replace text
sed 's/old/new/' file.txt

# Global replacement
sed 's/old/new/g' file.txt

# Delete lines
sed '/pattern/d' file.txt

# Multiple commands
sed -e 's/old/new/' -e 's/foo/bar/' file.txt
```

### awk

```bash
# Print specific fields
awk '{print $1, $3}' file.txt

# Filter rows
awk '$3 > 100' data.txt

# Sum column
awk '{sum += $1} END {print sum}' numbers.txt
```

---

## Power Tools in Action

Complex example combining multiple tools:

```bash
# Find large log files, extract errors, sort by frequency
find /var/log -type f -name "*.log" \
  -size +1M \
  -exec grep -i "error" {} \; \
  | sort \
  | uniq -c \
  | sort -rn \
  | head -n 10
```

---

## Practical Examples

1. File Analysis

```bash
# Count words in all text files
find . -name "*.txt" -exec wc -w {} \;

# Find duplicate files
find . -type f -exec md5sum {} \; \
  | sort | uniq -d -w32
```

1. Log Processing

```bash
# Extract IP addresses from log
grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" \
  access.log | sort | uniq -c
```

---

## Power Tools Exercise

Create a script to analyze system logs:

```bash
#!/bin/bash

# Find all log files
find /var/log -type f -name "*.log" | \
while read logfile; do
    echo "=== $logfile ==="

    # Count errors and warnings
    echo "Errors:"
    grep -i "error" "$logfile" | wc -l

    echo "Warnings:"
    grep -i "warn" "$logfile" | wc -l

    # Show top IP addresses
    echo "Top IP addresses:"
    grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" \
      "$logfile" | \
      sort | uniq -c | sort -rn | head -5
done
```
