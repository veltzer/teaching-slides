# UNIX File System
## Understanding Structure and Navigation

---

## Basic File System Structure

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_02_filesystem)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_02_filesystem)"/>
  <defs>
    <marker id="arrowd0_02_filesystem" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_02_filesystem)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_02_filesystem)"/>
  <defs>
    <marker id="arrowd1_02_filesystem" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_02_filesystem)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_02_filesystem)"/>
  <defs>
    <marker id="arrowd2_02_filesystem" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_02_filesystem)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd3_02_filesystem)"/>
  <defs>
    <marker id="arrowd3_02_filesystem" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_02_filesystem)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_02_filesystem)"/>
  <defs>
    <marker id="arrowd4_02_filesystem" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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
