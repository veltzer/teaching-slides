# Redirection
---
## File Descriptors
<svg xmlns="http://www.w3.org/2000/svg" width="660" height="200" font-family="sans-serif">
  <!-- title row -->
  <rect x="10" y="10" width="640" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="20" y="30" font-size="13" font-weight="bold" fill="#222">Every process has three standard file descriptors:</text>
  <!-- header row -->
  <rect x="10" y="50" width="80" height="28" fill="#bbdefb" stroke="#333" stroke-width="1.5"/>
  <rect x="90" y="50" width="90" height="28" fill="#bbdefb" stroke="#333" stroke-width="1.5"/>
  <rect x="180" y="50" width="120" height="28" fill="#bbdefb" stroke="#333" stroke-width="1.5"/>
  <rect x="300" y="50" width="350" height="28" fill="#bbdefb" stroke="#333" stroke-width="1.5"/>
  <text x="20" y="69" font-size="13" font-weight="bold" fill="#222">FD</text>
  <text x="100" y="69" font-size="13" font-weight="bold" fill="#222">Name</text>
  <text x="190" y="69" font-size="13" font-weight="bold" fill="#222">Default</text>
  <text x="310" y="69" font-size="13" font-weight="bold" fill="#222">C equivalent</text>
  <!-- row 0 -->
  <rect x="10" y="78" width="80" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="90" y="78" width="90" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="180" y="78" width="120" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="300" y="78" width="350" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="20" y="97" font-size="13" fill="#222">0</text>
  <text x="100" y="97" font-size="13" fill="#222">stdin</text>
  <text x="190" y="97" font-size="13" fill="#222">keyboard</text>
  <text x="310" y="97" font-size="13" fill="#222">stdin / scanf</text>
  <!-- row 1 -->
  <rect x="10" y="106" width="80" height="28" fill="#f0f4f8" stroke="#333" stroke-width="1"/>
  <rect x="90" y="106" width="90" height="28" fill="#f0f4f8" stroke="#333" stroke-width="1"/>
  <rect x="180" y="106" width="120" height="28" fill="#f0f4f8" stroke="#333" stroke-width="1"/>
  <rect x="300" y="106" width="350" height="28" fill="#f0f4f8" stroke="#333" stroke-width="1"/>
  <text x="20" y="125" font-size="13" fill="#222">1</text>
  <text x="100" y="125" font-size="13" fill="#222">stdout</text>
  <text x="190" y="125" font-size="13" fill="#222">terminal</text>
  <text x="310" y="125" font-size="13" fill="#222">stdout / printf</text>
  <!-- row 2 -->
  <rect x="10" y="134" width="80" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="90" y="134" width="90" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="180" y="134" width="120" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <rect x="300" y="134" width="350" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="20" y="153" font-size="13" fill="#222">2</text>
  <text x="100" y="153" font-size="13" fill="#222">stderr</text>
  <text x="190" y="153" font-size="13" fill="#222">terminal</text>
  <text x="310" y="153" font-size="13" fill="#222">stderr / fprintf</text>
  <!-- footer -->
  <text x="20" y="190" font-size="13" fill="#555">The shell can redirect any of these.</text>
</svg>
---
## stdout Redirection

```bash
# Redirect stdout to a file (create or overwrite)
echo "hello" > output.txt

# Append to a file
echo "world" >> output.txt

# Explicitly: 1> means "redirect fd 1"
echo "hello" 1> output.txt    # same as >
```
---
## stderr Redirection

```bash
# Redirect stderr to a file
ls /nonexistent 2> errors.txt

# Append stderr
ls /nonexistent 2>> errors.txt

# stdout and stderr to DIFFERENT files
command > stdout.txt 2> stderr.txt

# Example: save errors, show output
find / -name "*.conf" 2> /dev/null
# Errors (permission denied) are silenced
# Matching files are printed to terminal
```
---
## Redirecting Both stdout and stderr

```bash
# Method 1: redirect each separately
command > output.txt 2> errors.txt

# Method 2: redirect stderr to same place as stdout
command > all_output.txt 2>&1

# Method 3: shorthand (bash 4.0+)
command &> all_output.txt

# Method 4: append both
command >> all_output.txt 2>&1
command &>> all_output.txt    # bash 4.0+
```
---
## Order Matters!

```bash
# RIGHT: redirect stdout, then stderr to stdout's location
command > file.txt 2>&1
# Both stdout and stderr go to file.txt

# WRONG: redirect stderr to stdout (terminal), then stdout to file
command 2>&1 > file.txt
# stdout goes to file.txt
# stderr still goes to terminal!

# Think of it as: 2>&1 means "stderr goes where stdout
# is pointing RIGHT NOW"
```
---
## Visualizing Redirect Order
```misc
CORRECT: command > file.txt 2>&1

  Step 1: stdout --> file.txt
  Step 2: stderr --> (where stdout points) --> file.txt
  Result: both go to file.txt

INCORRECT: command 2>&1 > file.txt

  Step 1: stderr --> (where stdout points) --> terminal
  Step 2: stdout --> file.txt
  Result: stdout=file.txt, stderr=terminal
```
---
## stdin Redirection

```bash
# Read input from a file instead of keyboard
sort < unsorted.txt

# Combine with stdout redirection
sort < unsorted.txt > sorted.txt

# Here-string: provide a string as stdin
grep "hello" <<< "hello world"

# Multiple words
bc <<< "2 + 3"    # prints 5
```
---
## Here Documents

```bash
# Provide multi-line input to a command
cat << EOF
Hello, $USER
Today is $(date)
Welcome to bash scripting
EOF

# To prevent variable expansion, quote the delimiter
cat << 'EOF'
This is literal: $USER $(date)
No expansion happens here
EOF

# Indent with <<- (strips leading TABS only)
    cat <<- EOF
    This is indented with tabs
    They will be stripped
    EOF
```
---
## `/dev/null` - The Black Hole

```bash
# Discard stdout
command > /dev/null

# Discard stderr
command 2> /dev/null

# Discard everything
command > /dev/null 2>&1
command &> /dev/null

# Check if a command succeeds without seeing output
if grep -q "pattern" file.txt 2>/dev/null; then
    echo "found"
fi
```
---
## `/dev/zero`, `/dev/urandom`, `/dev/stdin`

```bash
# /dev/zero produces infinite zero bytes
dd if=/dev/zero of=zeros.bin bs=1M count=10

# /dev/urandom produces random bytes
dd if=/dev/urandom of=random.bin bs=1M count=10

# /dev/stdin, /dev/stdout, /dev/stderr
# are symlinks to the process's file descriptors
# Useful when a program expects a filename:
echo "data" | cat /dev/stdin
```
---
## Redirecting to Multiple Places: `tee`

```bash
# tee copies stdin to stdout AND to file(s)
echo "hello" | tee output.txt
# "hello" appears on terminal AND in output.txt

# Append mode
echo "world" | tee -a output.txt

# Multiple files
echo "data" | tee file1.txt file2.txt file3.txt

# Common pattern: see output and save it
make 2>&1 | tee build.log
```
---
## Process Substitution

```bash
# <(command) creates a virtual file from command's output
diff <(ls /dir1) <(ls /dir2)

# >(command) creates a virtual file that feeds into command
echo "data" | tee >(gzip > data.gz) >(wc -l > count.txt)

# Compare two sorted files without creating temp files
diff <(sort file1.txt) <(sort file2.txt)

# This is bash-specific, not POSIX
# It uses /dev/fd/ internally
echo <(true)    # prints something like /dev/fd/63
```
---
## Opening Custom File Descriptors

```bash
# Open fd 3 for writing
exec 3> custom_output.txt
echo "line 1" >&3
echo "line 2" >&3
exec 3>&-    # close fd 3

# Open fd 4 for reading
exec 4< input.txt
read line1 <&4
read line2 <&4
exec 4<&-    # close fd 4

# Open fd 5 for read/write
exec 5<> bidirectional.txt
```
---
## Swapping stdout and stderr

```bash
# Sometimes you want to swap them
# (e.g., to pipe stderr through a filter)

# Swap stdout and stderr using fd 3 as temporary:
command 3>&1 1>&2 2>&3 3>&-

# Step by step:
# 3>&1  : fd 3 = copy of stdout
# 1>&2  : stdout = stderr (terminal)
# 2>&3  : stderr = fd 3 (original stdout)
# 3>&-  : close fd 3

# Now stdout goes where stderr went and vice versa
```
---
## Redirection Tricks

```bash
# Truncate a file (make it empty)
> file.txt

# Read a file line by line
while IFS= read -r line; do
    echo "Line: $line"
done < file.txt

# Redirect a block of commands
{
    echo "header"
    date
    echo "footer"
} > report.txt

# Append to a file that needs sudo
echo "data" | sudo tee -a /etc/some_config > /dev/null
# Note: sudo echo "data" >> /etc/file DOES NOT WORK
# because >> is handled by the current (non-root) shell
```
---
## The `noclobber` Option

```bash
# Prevent accidental overwriting
set -o noclobber

echo "data" > existing_file.txt
# bash: existing_file.txt: cannot overwrite existing file

# Force overwrite despite noclobber
echo "data" >| existing_file.txt

# Turn off noclobber
set +o noclobber
```
