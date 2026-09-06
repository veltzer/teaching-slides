---
tags:
  - languages:bash
  - practices:scripting
  - infrastructure:linux
  - practices:automation
level: intermediate
category: language
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---

# Pipes

---

## What is a Pipe?
- Connects stdout of one command to stdin of another
- Data flows left to right
- Each command runs in its own process
- All commands in a pipeline run **simultaneously**

```bash
# Simple pipe
ls -la | grep ".txt"

# Data flow:
# ls -la --> stdout --> pipe --> stdin --> grep ".txt"
```

---

## Pipe Syntax

```bash
# Single pipe
command1 | command2

# Multiple pipes (pipeline)
command1 | command2 | command3 | command4

# Real example: find the 10 largest files
du -sh /var/log/* 2>/dev/null | sort -rh | head -10
```

---

## How Pipes Work Internally

![how_pipes_work_internally](svg/courses/languages/bash/bash-scripting/13_pipes/how_pipes_work_internally.svg)

---

## Pipes Run Concurrently

```bash
# Both commands start at the same time!
# They do NOT run sequentially

# Proof:
{ echo "producer started"; sleep 2; echo "data"; } |
{ echo "consumer started"; cat; }

# Output:
# consumer started
# producer started
# data

# The consumer doesn't wait for the producer to finish
```

---

## Pipe Buffer and Blocking

```bash
# The pipe has a limited buffer (typically 64KB on Linux)
# Check your system:
cat /proc/sys/fs/pipe-max-size

# If the buffer is full:
# - The writer BLOCKS until the reader reads some data

# If the buffer is empty:
# - The reader BLOCKS until the writer writes data

# This is how flow control works automatically
```

---

## Common Pipeline Patterns

```bash
# Filter
cat access.log | grep "404"

# Better (avoid useless use of cat):
grep "404" access.log

# Transform
ps aux | awk '{print $2, $11}'

# Sort and unique
cut -d: -f7 /etc/passwd | sort | uniq -c | sort -rn

# Count
grep -c "error" logfile.txt
# Or:
grep "error" logfile.txt | wc -l
```

---

## Pipeline Building Blocks

```bash
# Filtering:     grep, awk, sed
# Sorting:       sort, uniq
# Counting:      wc
# Cutting:       cut, awk
# Transforming:  tr, sed, awk
# Paging:        head, tail, less
# Formatting:    column, printf

# Example: user activity report
last | awk '{print $1}' | sort | uniq -c | sort -rn | head -5
```

---

## The "Useless Use of `cat`" Anti-Pattern

```bash
# WRONG (wasteful extra process):
cat file.txt | grep "pattern"
cat file.txt | wc -l
cat file.txt | sort

# RIGHT (the command reads the file directly):
grep "pattern" file.txt
wc -l < file.txt
sort file.txt

# When cat IS useful:
cat file1.txt file2.txt | sort    # concatenating files
cat -n file.txt                    # adding line numbers
```

---

## Pipes and Return Codes

```bash
# Default: $? is the return code of the LAST command
false | true
echo $?    # 0 (true succeeded)

# With pipefail: $? is the rightmost failure
set -o pipefail
false | true
echo $?    # 1 (false failed)

# PIPESTATUS array: all return codes
false | true | false
echo "${PIPESTATUS[@]}"    # 1 0 1
```

---

## Pipes and Subshells: The Trap

```bash
# PROBLEM: each pipe command runs in a subshell
count=0
echo -e "a\nb\nc" | while read line; do
    count=$((count + 1))
done
echo "count=$count"    # 0! (subshell changes lost)

# SOLUTION 1: process substitution
count=0
while read line; do
    count=$((count + 1))
done < <(echo -e "a\nb\nc")
echo "count=$count"    # 3

# SOLUTION 2: lastpipe (bash 4.2+)
shopt -s lastpipe
count=0
echo -e "a\nb\nc" | while read line; do
    count=$((count + 1))
done
echo "count=$count"    # 3
```

---

## Named Pipes (FIFOs)

```bash
# Create a named pipe
mkfifo /tmp/mypipe

# Terminal 1: read from the pipe (blocks until data arrives)
cat /tmp/mypipe

# Terminal 2: write to the pipe
echo "Hello from terminal 2" > /tmp/mypipe

# Named pipes are files in the filesystem
ls -la /tmp/mypipe
# prw-r--r-- 1 user user 0 ... /tmp/mypipe

# Cleanup
rm /tmp/mypipe
```

---

## Pipe to `xargs`

```bash
# xargs converts stdin lines into command arguments
echo "file1 file2 file3" | xargs rm

# One argument per line
find . -name "*.log" | xargs rm

# Handle spaces in filenames
find . -name "*.log" -print0 | xargs -0 rm

# Run one command per input line
cat urls.txt | xargs -n 1 curl -O

# Run in parallel
cat hosts.txt | xargs -n 1 -P 4 ping -c 1
```

---

## Pipeline Performance

```bash
# Pipes are efficient: data streams without temp files
# But each | creates a new process

# For simple operations, avoid unnecessary pipes:

# Slow (4 processes):
cat file | grep pattern | head -1 | cut -d: -f1

# Faster (1 process):
awk -F: '/pattern/ {print $1; exit}' file

# Know when pipes are worth it:
# - Clear, readable code
# - Each stage does one thing well
# - The Unix philosophy
```
