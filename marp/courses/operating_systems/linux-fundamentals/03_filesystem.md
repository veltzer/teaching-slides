# UNIX File System
## Understanding Structure and Navigation

---

## Basic File System Structure

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="240" y="5" width="120" height="30" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="25" text-anchor="middle" font-size="12" font-weight="bold">/ (root)</text>
  <line x1="230" y1="35" x2="100" y2="55" stroke="#333" stroke-width="1"/>
  <line x1="270" y1="35" x2="220" y2="55" stroke="#333" stroke-width="1"/>
  <line x1="300" y1="35" x2="300" y2="55" stroke="#333" stroke-width="1"/>
  <line x1="330" y1="35" x2="380" y2="55" stroke="#333" stroke-width="1"/>
  <line x1="370" y1="35" x2="500" y2="55" stroke="#333" stroke-width="1"/>
  <rect x="50" y="55" width="90" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="95" y="72" text-anchor="middle" font-size="10">/bin</text>
  <rect x="175" y="55" width="90" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="72" text-anchor="middle" font-size="10">/etc</text>
  <rect x="275" y="55" width="90" height="25" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="320" y="72" text-anchor="middle" font-size="10">/home</text>
  <rect x="375" y="55" width="90" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="420" y="72" text-anchor="middle" font-size="10">/usr</text>
  <rect x="475" y="55" width="90" height="25" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="520" y="72" text-anchor="middle" font-size="10">/var</text>
  <line x1="320" y1="80" x2="270" y2="100" stroke="#333" stroke-width="1"/>
  <line x1="320" y1="80" x2="370" y2="100" stroke="#333" stroke-width="1"/>
  <rect x="220" y="100" width="100" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="270" y="115" text-anchor="middle" font-size="9">/home/alice</text>
  <rect x="330" y="100" width="100" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="380" y="115" text-anchor="middle" font-size="9">/home/bob</text>
  <rect x="50" y="140" width="510" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="157" text-anchor="middle" font-size="10" font-weight="bold">Filesystem Hierarchy Standard (FHS)</text>
  <text x="300" y="175" text-anchor="middle" font-size="10">/bin:cmds  /etc:config  /home:users  /usr:programs  /var:logs,data</text>
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
  <rect x="50" y="10" width="240" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="170" y="30" text-anchor="middle" font-size="11" font-weight="bold">Absolute Path</text>
  <text x="170" y="48" text-anchor="middle" font-family="monospace" font-size="10">/home/user/docs/file.txt</text>
  <rect x="310" y="10" width="240" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="430" y="30" text-anchor="middle" font-size="11" font-weight="bold">Relative Path</text>
  <text x="430" y="48" text-anchor="middle" font-family="monospace" font-size="10">./docs/file.txt</text>
  <rect x="50" y="75" width="500" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="92" text-anchor="middle" font-size="10" font-weight="bold">Special Path Symbols</text>
  <text x="300" y="110" text-anchor="middle" font-family="monospace" font-size="10">/  (root)    .  (current)    ..  (parent)    ~  (home)    -  (previous)</text>
  <rect x="50" y="135" width="500" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="152" text-anchor="middle" font-size="10" font-weight="bold">Path Resolution Example (cwd = /home/user)</text>
  <text x="300" y="172" text-anchor="middle" font-family="monospace" font-size="10">cd ../bob/docs  -->  /home/bob/docs</text>
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
  <rect x="50" y="10" width="500" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="25" text-anchor="middle" font-size="11" font-weight="bold">Home Directory Structure</text>
  <text x="300" y="42" text-anchor="middle" font-family="monospace" font-size="10">/home/username  or  ~  or  $HOME</text>
  <rect x="50" y="65" width="150" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="125" y="80" text-anchor="middle" font-size="10" font-weight="bold">~/Documents</text>
  <text x="125" y="96" text-anchor="middle" font-size="9" fill="#666">personal files</text>
  <rect x="220" y="65" width="150" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="295" y="80" text-anchor="middle" font-size="10" font-weight="bold">~/.bashrc</text>
  <text x="295" y="96" text-anchor="middle" font-size="9" fill="#666">shell config (hidden)</text>
  <rect x="390" y="65" width="160" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="470" y="80" text-anchor="middle" font-size="10" font-weight="bold">~/.ssh/</text>
  <text x="470" y="96" text-anchor="middle" font-size="9" fill="#666">SSH keys (mode 700)</text>
  <rect x="50" y="120" width="500" height="65" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="137" text-anchor="middle" font-size="10" font-weight="bold">Dot Files (Hidden) - shown with ls -a</text>
  <text x="300" y="155" text-anchor="middle" font-size="10">.profile  .bash_history  .config/  .local/</text>
  <text x="300" y="173" text-anchor="middle" font-size="10" fill="#666">root's home: /root (not /home/root)</text>
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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="11" font-weight="bold">Directory Stack (pushd / popd)</text>
  <rect x="50" y="30" width="120" height="140" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="50" text-anchor="middle" font-size="10" font-weight="bold">Stack</text>
  <rect x="60" y="58" width="100" height="22" fill="#fff3e0" stroke="#333" stroke-width="1" rx="2"/>
  <text x="110" y="73" text-anchor="middle" font-size="9">/home/user</text>
  <rect x="60" y="84" width="100" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="2"/>
  <text x="110" y="99" text-anchor="middle" font-size="9">/var/log</text>
  <rect x="60" y="110" width="100" height="22" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="2"/>
  <text x="110" y="125" text-anchor="middle" font-size="9">/etc</text>
  <text x="110" y="155" text-anchor="middle" font-size="9" fill="#666">dirs -v</text>
  <rect x="200" y="40" width="180" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="290" y="58" text-anchor="middle" font-size="10" font-weight="bold">pushd /var/log</text>
  <text x="290" y="78" text-anchor="middle" font-size="10">saves current dir, cd to new</text>
  <rect x="200" y="110" width="180" height="55" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="290" y="128" text-anchor="middle" font-size="10" font-weight="bold">popd</text>
  <text x="290" y="148" text-anchor="middle" font-size="10">return to previous dir</text>
  <rect x="410" y="40" width="140" height="125" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="480" y="58" text-anchor="middle" font-size="10" font-weight="bold">Quick Nav</text>
  <text x="480" y="78" text-anchor="middle" font-size="10">cd -    : toggle</text>
  <text x="480" y="98" text-anchor="middle" font-size="10">cd ~    : home</text>
  <text x="480" y="118" text-anchor="middle" font-size="10">cd ..   : parent</text>
  <text x="480" y="138" text-anchor="middle" font-size="10">cd      : home</text>
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
  <rect x="50" y="10" width="160" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="130" y="30" text-anchor="middle" font-size="10" font-weight="bold">dirname</text>
  <text x="130" y="50" text-anchor="middle" font-family="monospace" font-size="9">/home/user/docs</text>
  <rect x="220" y="10" width="160" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="10" font-weight="bold">basename</text>
  <text x="300" y="50" text-anchor="middle" font-family="monospace" font-size="9">file.txt</text>
  <rect x="390" y="10" width="160" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="30" text-anchor="middle" font-size="10" font-weight="bold">realpath</text>
  <text x="470" y="50" text-anchor="middle" font-family="monospace" font-size="9">resolves symlinks</text>
  <rect x="50" y="80" width="500" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="95" text-anchor="middle" font-size="10" font-weight="bold">Input: /home/user/docs/file.txt</text>
  <text x="300" y="112" text-anchor="middle" font-family="monospace" font-size="10">dirname -> /home/user/docs  |  basename -> file.txt</text>
  <rect x="100" y="135" width="400" height="50" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="152" text-anchor="middle" font-size="10" font-weight="bold">Path variable manipulation in bash:</text>
  <text x="300" y="172" text-anchor="middle" font-family="monospace" font-size="10">${path%/*} (dirname)  |  ${path##*/} (basename)</text>
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
