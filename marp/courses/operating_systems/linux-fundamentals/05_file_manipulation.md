---
tags:
  - infrastructure:linux
  - infrastructure:unix
  - practices:command-line
level: beginner
category: operating-systems
audience:
  - audiences:developers
  - audiences:sysadmins

---

# File and Disk Manipulation
## Essential Commands and Power Tools

---

## Basic File Operations

![basic_file_operations](svg/courses/operating_systems/linux-fundamentals/05_file_manipulation/basic_file_operations.svg)

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
![viewing_file_contents](svg/courses/operating_systems/linux-fundamentals/05_file_manipulation/viewing_file_contents.svg)

---

## Viewing File Contents: Example

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
![disk_usage_commands](svg/courses/operating_systems/linux-fundamentals/05_file_manipulation/disk_usage_commands.svg)

---

## Disk Usage Commands: Example

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

## File Operations Overview

![file_operations_overview](svg/courses/operating_systems/linux-fundamentals/05_file_manipulation/file_operations_overview.svg)

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
![finding_files](svg/courses/operating_systems/linux-fundamentals/05_file_manipulation/finding_files.svg)

---

## Finding Files: Example

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
