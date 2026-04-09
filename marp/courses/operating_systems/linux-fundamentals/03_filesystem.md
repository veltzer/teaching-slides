# UNIX File System
## Understanding Structure and Navigation

---

## Basic File System Structure

![basic_file_system_structure](svg/courses/operating_systems/linux-fundamentals/03_filesystem/basic_file_system_structure.svg)

---

## Basic File System Structure

Key Directories:
- `/bin`: Essential commands
- `/etc`: System configuration
- `/home`: User directories
- `/usr`: User programs
- `/var`: Variable data

---

## Important System Directories

| Directory | Purpose |
|-----------|---------|
| `/bin`    | Essential commands |
| `/sbin`   | System binaries |
| `/etc`    | Configuration files |
| `/dev`    | Device files |
| `/proc`   | Process information |
| `/tmp`    | Temporary files |
| `/var`    | Variable data |
| `/root`   | Root user's home |

---

## Understanding Paths

![understanding_paths](svg/courses/operating_systems/linux-fundamentals/03_filesystem/understanding_paths.svg)

---

## Understanding Paths

Examples:
```bash
# Absolute path
cd /home/user/documents
# Relative path
cd ./documents
cd ../user2/documents
# Special paths
cd ~        # Home directory
cd -        # Previous directory
```

---

## Path Navigation Examples

```bash
# Current location
pwd
/home/user1

# Move to subdirectory
cd documents

# Move up one level
cd ..

# Absolute path navigation
cd /usr/local/bin

# Return home
cd ~

# Go to previous directory
cd -
```

---

## Home Directories

![home_directories](svg/courses/operating_systems/linux-fundamentals/03_filesystem/home_directories.svg)

---

## Home Directories

Access methods:
```bash
# Using tilde
cd ~
cd ~/Documents
# Using $HOME
cd $HOME
cd $HOME/Documents
# Using absolute path
cd /home/username
```

---

## Moving Around Commands

## Basic Navigation

```bash
# Print working directory
pwd

# Change directory
cd /path/to/directory

# List directory contents
ls
ls -la
```

## Directory Stack

```bash
# Push directory to stack
pushd /path/to/dir

# Pop directory from stack
popd

# Show directory stack
dirs -v
```

---

## Directory Stack Management

![directory_stack_management](svg/courses/operating_systems/linux-fundamentals/03_filesystem/directory_stack_management.svg)

---

## Practical Directory Navigation

```bash
# Start in home directory
cd ~

# Create and navigate test directory structure
mkdir -p projects/{docs,src,tests}
pushd projects/docs

# Create some files
touch readme.txt
pushd ../src

# View stack
dirs -v

# Return to previous directory
popd

# View current location
pwd
```

---

## Path Manipulation Tips

```bash
# Get directory name
dirname /path/to/file

# Get base name
basename /path/to/file

# Normalize path
realpath ./relative/path

# Expand home directory
echo ~
echo $HOME
```

---

## Common Path Operations

![common_path_operations](svg/courses/operating_systems/linux-fundamentals/03_filesystem/common_path_operations.svg)

---

## Common Path Operations

Examples:
```bash
# Extract components
path="/home/user/docs/file.txt"
echo $(dirname "$path")  # /home/user/docs
echo $(basename "$path") # file.txt
```

---

## Practice Exercises

1. Directory Navigation

```bash
# Create test directory structure
mkdir -p ~/test/{a,b,c}/{1,2,3}

# Navigate and list
cd ~/test/a/1
pwd
ls ../../b

# Use pushd/popd
pushd ~/test/c/3
pushd ~/test/b/2
dirs -v
popd
pwd
```

1. Path Manipulation

```bash
# Create test files
touch ~/test/a/1/file.txt
echo $(dirname ~/test/a/1/file.txt)
echo $(basename ~/test/a/1/file.txt)
```

---

## Advanced Topics

## Symbolic Links

```bash
# Create symbolic link
ln -s target_file link_name

# Follow symbolic link
readlink link_name
```

## Hard Links

```bash
# Create hard link
ln target_file link_name

# Find same inodes
find . -samefile target_file
```
