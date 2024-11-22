# Files in Detail
## Understanding UNIX File Types and Inodes
---
## Seven File Types in UNIX

![0](../../../out/mermaid/marp/courses/linux-fundamentals/05_file_detail.md/0.png)

First character in ls -l output indicates type:

```bash
-rw-r--r--  # Regular file
drwxr-xr-x  # Directory
lrwxrwxrwx  # Symbolic link
crw-rw-rw-  # Character device
brw-rw-rw-  # Block device
srwxrwxrwx  # Socket
prw-r--r--  # Named pipe
```
---
## Regular Files (-)

```bash
# Create regular file
touch regular.txt
echo "content" > regular.txt

# View file type
file regular.txt

# Check permissions
ls -l regular.txt
```

Common types:
- Text files
- Binary files
- Data files
- Scripts
- Executables

---
## Directories (d)

![1](../../../out/mermaid/marp/courses/linux-fundamentals/05_file_detail.md/1.png)

```bash
# Create directory
mkdir newdir

# List directory contents
ls -la newdir

# Show directory type
file newdir

# Directory permissions
ls -ld newdir
```
---
## Device Files (c, b)

Character Devices (c):
- Serial ports
- Terminals
- Mouse/keyboard

Block Devices (b):
- Hard drives
- SSDs
- USB drives

```bash
# View device files
ls -l /dev/

# Common devices
ls -l /dev/sda    # Hard drive
ls -l /dev/tty    # Terminal
ls -l /dev/null   # Null device
```
---
## Symbolic Links (l)

![2](../../../out/mermaid/marp/courses/linux-fundamentals/05_file_detail.md/2.png)

```bash
# Create symbolic link
ln -s target.txt link.txt

# View link
ls -l link.txt

# Read link target
readlink link.txt

# Find broken links
find . -type l -! -exec test -e {} \; -print
```
---
## Sockets (s) and Named Pipes (p)

Sockets:
```bash
# View system sockets
ls -l /var/run/*.sock

# Create socket (in C)
socket(AF_UNIX, SOCK_STREAM, 0);
```

Named Pipes:
```bash
# Create named pipe
mkfifo mypipe

# Use pipe
echo "data" > mypipe &
cat < mypipe
```

---
## The INODE Concept

![3](../../../out/mermaid/marp/courses/linux-fundamentals/05_file_detail.md/3.png)

Inode contains:
- File type
- Permissions
- Link count
- Owner and group
- Size
- Timestamps
- Data block pointers

---
## Working with Inodes

```bash
# View inode numbers
ls -i

# Find files with same inode
find . -inum 12345

# Get file status (inode info)
stat file.txt

# File system inode usage
df -i
```

Example output:

```txt
# ls -i
12345 file.txt
12345 hardlink.txt  # Same inode number
67890 different.txt # Different inode
```
---
## Hard Links vs Symbolic Links

![4](../../../out/mermaid/marp/courses/linux-fundamentals/05_file_detail.md/4.png)

Creating Links:
```bash
# Create hard link
ln target.txt hardlink.txt

# Create symbolic link
ln -s target.txt symlink.txt

# Compare inodes
ls -li target.txt hardlink.txt symlink.txt
```

---
## Link Count and Storage

```bash
# Create test file
echo "test" > original.txt

# Create hard links
ln original.txt link1.txt
ln original.txt link2.txt

# Check link count
ls -l original.txt  # Shows count of 3

# Remove original
rm original.txt     # File still exists
cat link1.txt      # Still accessible
```
---
## File Timestamps

Three main timestamps:
```bash
# View all timestamps
stat file.txt

# Access time (-atime)
ls -lu file.txt

# Modification time (-mtime)
ls -l file.txt

# Change time (-ctime)
ls -lc file.txt
```

Updating timestamps:
```bash
# Update access/modification times
touch file.txt

# Update access time only
touch -a file.txt

# Update modification time only
touch -m file.txt
```
---
## Practical Examples

1. Finding files by inode:

```bash
# Create test files
echo "content" > original.txt
ln original.txt hard1.txt
ln original.txt hard2.txt

# Find all hard links
find . -inum $(ls -i original.txt | cut -d' ' -f1)
```

1. Link management:

```bash
# Create directory structure
mkdir -p dir1/dir2
touch dir1/dir2/target.txt

# Create relative symbolic link
cd dir1
ln -s dir2/target.txt link.txt

# Create absolute symbolic link
ln -s /absolute/path/target.txt abslink.txt
```
---
## File System Layout

![5](../../../out/mermaid/marp/courses/linux-fundamentals/05_file_detail.md/5.png)

Key components:
- Superblock: File system metadata
- Inode table: File metadata
- Data blocks: Actual file content
