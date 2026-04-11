---
tags:
  - infrastructure:linux
  - infrastructure:unix
  - concepts:filesystem
level: beginner
category: operating-systems
audience:
  - audiences:developers
  - audiences:sysadmins

---
# Files in Detail
## Understanding UNIX File Types and Inodes

---

## Seven File Types in UNIX

![seven_file_types_in_unix](svg/courses/operating_systems/linux-fundamentals/06_file_detail/seven_file_types_in_unix.svg)

---

## Seven File Types in UNIX

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

## File Attributes Anatomy

![file_attributes](svg/courses/operating_systems/linux-fundamentals/06_file_detail/file_attributes.svg)

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

![directories_d](svg/courses/operating_systems/linux-fundamentals/06_file_detail/directories_d.svg)

---

## Directories (d)

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

![symbolic_links_l](svg/courses/operating_systems/linux-fundamentals/06_file_detail/symbolic_links_l.svg)

---

## Symbolic Links (l)

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

![the_inode_concept](svg/courses/operating_systems/linux-fundamentals/06_file_detail/the_inode_concept.svg)

---

## The INODE Concept

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

```console
# ls -i
12345 file.txt
12345 hardlink.txt  # Same inode number
67890 different.txt # Different inode
```

---

## Hard Links vs Symbolic Links

![hard_links_vs_symbolic_links](svg/courses/operating_systems/linux-fundamentals/06_file_detail/hard_links_vs_symbolic_links.svg)

---

## Hard Links vs Symbolic Links

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

![file_system_layout](svg/courses/operating_systems/linux-fundamentals/06_file_detail/file_system_layout.svg)

---

## File System Layout

Key components:
- Superblock: File system metadata
- Inode table: File metadata
- Data blocks: Actual file content
