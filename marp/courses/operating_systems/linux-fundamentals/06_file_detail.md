# Files in Detail
## Understanding UNIX File Types and Inodes
---
## Seven File Types in UNIX

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Seven UNIX File Types</text>
  <rect x="10" y="35" width="75" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="4"/>
  <text x="47" y="55" text-anchor="middle" font-size="10" font-weight="bold">- regular</text>
  <text x="47" y="70" text-anchor="middle" font-size="9">file</text>
  <rect x="95" y="35" width="75" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="4"/>
  <text x="132" y="55" text-anchor="middle" font-size="10" font-weight="bold">d directory</text>
  <text x="132" y="70" text-anchor="middle" font-size="9">folder</text>
  <rect x="180" y="35" width="75" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="4"/>
  <text x="217" y="55" text-anchor="middle" font-size="10" font-weight="bold">l symlink</text>
  <text x="217" y="70" text-anchor="middle" font-size="9">pointer</text>
  <rect x="265" y="35" width="75" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="4"/>
  <text x="302" y="55" text-anchor="middle" font-size="10" font-weight="bold">c char dev</text>
  <text x="302" y="70" text-anchor="middle" font-size="9">serial</text>
  <rect x="350" y="35" width="75" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="4"/>
  <text x="387" y="55" text-anchor="middle" font-size="10" font-weight="bold">b block dev</text>
  <text x="387" y="70" text-anchor="middle" font-size="9">disk</text>
  <rect x="435" y="35" width="75" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="4"/>
  <text x="472" y="55" text-anchor="middle" font-size="10" font-weight="bold">s socket</text>
  <text x="472" y="70" text-anchor="middle" font-size="9">IPC</text>
  <rect x="520" y="35" width="75" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="4"/>
  <text x="557" y="55" text-anchor="middle" font-size="10" font-weight="bold">p pipe</text>
  <text x="557" y="70" text-anchor="middle" font-size="9">FIFO</text>
  <text x="300" y="110" text-anchor="middle" font-size="11" fill="#333">Identified by first character in ls -l output</text>
  <rect x="80" y="125" width="440" height="55" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5" opacity="0.5"/>
  <text x="300" y="147" text-anchor="middle" font-size="10" font-family="monospace">-rw-r--r--  drwxr-xr-x  lrwxrwxrwx  crw-rw-rw-</text>
  <text x="300" y="168" text-anchor="middle" font-size="10" font-family="monospace">brw-rw-rw-  srwxrwxrwx  prw-r--r--</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Directory as a File</text>
  <defs>
    <marker id="arrowdir" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="180" y="35" width="240" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="60" text-anchor="middle" font-size="12" font-weight="bold">Directory (inode)</text>
  <line x1="230" y1="75" x2="100" y2="105" stroke="#333" stroke-width="1.5" marker-end="url(#arrowdir)"/>
  <line x1="300" y1="75" x2="300" y2="105" stroke="#333" stroke-width="1.5" marker-end="url(#arrowdir)"/>
  <line x1="370" y1="75" x2="500" y2="105" stroke="#333" stroke-width="1.5" marker-end="url(#arrowdir)"/>
  <rect x="30" y="105" width="140" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="4"/>
  <text x="100" y="120" text-anchor="middle" font-size="10" font-weight="bold">. (self)</text>
  <text x="100" y="133" text-anchor="middle" font-size="9">inode of this dir</text>
  <rect x="230" y="105" width="140" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="4"/>
  <text x="300" y="120" text-anchor="middle" font-size="10" font-weight="bold">.. (parent)</text>
  <text x="300" y="133" text-anchor="middle" font-size="9">inode of parent dir</text>
  <rect x="430" y="105" width="140" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="4"/>
  <text x="500" y="120" text-anchor="middle" font-size="10" font-weight="bold">entries</text>
  <text x="500" y="133" text-anchor="middle" font-size="9">name-to-inode map</text>
  <rect x="80" y="160" width="440" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="4" opacity="0.7"/>
  <text x="300" y="180" text-anchor="middle" font-size="10">A directory is a special file mapping filenames to inode numbers</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Symbolic Link Structure</text>
  <defs>
    <marker id="arrowsym" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="55" width="150" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="75" text-anchor="middle" font-size="11" font-weight="bold">link.txt</text>
  <text x="105" y="92" text-anchor="middle" font-size="10">(symlink inode)</text>
  <line x1="180" y1="80" x2="230" y2="80" stroke="#333" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#arrowsym)"/>
  <text x="205" y="72" text-anchor="middle" font-size="9">points to</text>
  <rect x="230" y="55" width="150" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="305" y="75" text-anchor="middle" font-size="11" font-weight="bold">target.txt</text>
  <text x="305" y="92" text-anchor="middle" font-size="10">(path string)</text>
  <line x1="380" y1="80" x2="430" y2="80" stroke="#333" stroke-width="2" marker-end="url(#arrowsym)"/>
  <text x="405" y="72" text-anchor="middle" font-size="9">resolves</text>
  <rect x="430" y="55" width="150" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="75" text-anchor="middle" font-size="11" font-weight="bold">data blocks</text>
  <text x="505" y="92" text-anchor="middle" font-size="10">(actual content)</text>
  <rect x="30" y="130" width="250" height="50" fill="#ffebee" stroke="#333" stroke-width="1" rx="4" opacity="0.7"/>
  <text x="155" y="150" text-anchor="middle" font-size="10" font-weight="bold">If target is deleted:</text>
  <text x="155" y="167" text-anchor="middle" font-size="10">symlink becomes broken (dangling)</text>
  <rect x="320" y="130" width="260" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="4" opacity="0.7"/>
  <text x="450" y="150" text-anchor="middle" font-size="10" font-weight="bold">Can cross filesystems</text>
  <text x="450" y="167" text-anchor="middle" font-size="10">Stores path, not inode number</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Inode Structure</text>
  <defs>
    <marker id="arrowinode" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="35" width="200" height="150" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="130" y="55" text-anchor="middle" font-size="11" font-weight="bold">Inode #12345</text>
  <line x1="40" y1="62" x2="220" y2="62" stroke="#333" stroke-width="1"/>
  <text x="45" y="78" font-size="10">Type: regular file</text>
  <text x="45" y="93" font-size="10">Perms: rwxr-xr--</text>
  <text x="45" y="108" font-size="10">Owner: uid=1000</text>
  <text x="45" y="123" font-size="10">Size: 4096 bytes</text>
  <text x="45" y="138" font-size="10">Links: 2</text>
  <text x="45" y="153" font-size="10">Timestamps: amc</text>
  <text x="45" y="170" font-size="10" font-weight="bold">Block ptrs ---></text>
  <line x1="230" y1="165" x2="280" y2="80" stroke="#333" stroke-width="1.5" marker-end="url(#arrowinode)"/>
  <line x1="230" y1="165" x2="280" y2="120" stroke="#333" stroke-width="1.5" marker-end="url(#arrowinode)"/>
  <line x1="230" y1="165" x2="280" y2="160" stroke="#333" stroke-width="1.5" marker-end="url(#arrowinode)"/>
  <rect x="280" y="60" width="130" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="345" y="80" text-anchor="middle" font-size="10">Data Block 0</text>
  <rect x="280" y="100" width="130" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="345" y="120" text-anchor="middle" font-size="10">Data Block 1</text>
  <rect x="280" y="140" width="130" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="345" y="160" text-anchor="middle" font-size="10">Data Block 2</text>
  <rect x="440" y="55" width="140" height="130" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5" opacity="0.7"/>
  <text x="510" y="78" text-anchor="middle" font-size="10" font-weight="bold">Note:</text>
  <text x="510" y="96" text-anchor="middle" font-size="10">Filename is NOT</text>
  <text x="510" y="112" text-anchor="middle" font-size="10">stored in inode.</text>
  <text x="510" y="132" text-anchor="middle" font-size="10">It lives in the</text>
  <text x="510" y="148" text-anchor="middle" font-size="10">parent directory</text>
  <text x="510" y="164" text-anchor="middle" font-size="10">entry.</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Hard Links vs Symbolic Links</text>
  <defs>
    <marker id="arrowlinks" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <!-- Hard link side -->
  <text x="150" y="42" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">Hard Link</text>
  <rect x="30" y="50" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="80" y="70" text-anchor="middle" font-size="10">file.txt</text>
  <rect x="160" y="50" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="210" y="70" text-anchor="middle" font-size="10">hardlink.txt</text>
  <line x1="80" y1="80" x2="145" y2="110" stroke="#333" stroke-width="1.5" marker-end="url(#arrowlinks)"/>
  <line x1="210" y1="80" x2="145" y2="110" stroke="#333" stroke-width="1.5" marker-end="url(#arrowlinks)"/>
  <rect x="95" y="110" width="100" height="30" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="4"/>
  <text x="145" y="130" text-anchor="middle" font-size="10" font-weight="bold">Inode #12345</text>
  <line x1="145" y1="140" x2="145" y2="160" stroke="#333" stroke-width="1.5" marker-end="url(#arrowlinks)"/>
  <rect x="95" y="160" width="100" height="25" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="145" y="177" text-anchor="middle" font-size="10">Data Blocks</text>
  <!-- Symbolic link side -->
  <text x="450" y="42" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">Symbolic Link</text>
  <rect x="340" y="50" width="100" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="390" y="70" text-anchor="middle" font-size="10">symlink.txt</text>
  <line x1="440" y1="65" x2="470" y2="65" stroke="#333" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arrowlinks)"/>
  <rect x="470" y="50" width="100" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="520" y="70" text-anchor="middle" font-size="10">target.txt</text>
  <line x1="520" y1="80" x2="520" y2="110" stroke="#333" stroke-width="1.5" marker-end="url(#arrowlinks)"/>
  <rect x="470" y="110" width="100" height="30" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="4"/>
  <text x="520" y="130" text-anchor="middle" font-size="10" font-weight="bold">Inode #67890</text>
  <line x1="520" y1="140" x2="520" y2="160" stroke="#333" stroke-width="1.5" marker-end="url(#arrowlinks)"/>
  <rect x="470" y="160" width="100" height="25" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="520" y="177" text-anchor="middle" font-size="10">Data Blocks</text>
  <line x1="300" y1="35" x2="300" y2="190" stroke="#999" stroke-width="1" stroke-dasharray="3,3"/>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="22" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">Filesystem Layout on Disk</text>
  <rect x="20" y="40" width="80" height="60" fill="#ffebee" stroke="#333" stroke-width="2" rx="3"/>
  <text x="60" y="65" text-anchor="middle" font-size="10" font-weight="bold">Boot</text>
  <text x="60" y="80" text-anchor="middle" font-size="9">Block</text>
  <rect x="110" y="40" width="100" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="3"/>
  <text x="160" y="65" text-anchor="middle" font-size="10" font-weight="bold">Superblock</text>
  <text x="160" y="80" text-anchor="middle" font-size="9">FS metadata</text>
  <rect x="220" y="40" width="130" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="3"/>
  <text x="285" y="65" text-anchor="middle" font-size="10" font-weight="bold">Inode Table</text>
  <text x="285" y="80" text-anchor="middle" font-size="9">file metadata</text>
  <rect x="360" y="40" width="220" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="3"/>
  <text x="470" y="65" text-anchor="middle" font-size="10" font-weight="bold">Data Blocks</text>
  <text x="470" y="80" text-anchor="middle" font-size="9">actual file content</text>
  <rect x="110" y="120" width="100" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3" opacity="0.7"/>
  <text x="160" y="138" text-anchor="middle" font-size="9">block size, count</text>
  <text x="160" y="153" text-anchor="middle" font-size="9">free blocks/inodes</text>
  <rect x="220" y="120" width="130" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3" opacity="0.7"/>
  <text x="285" y="138" text-anchor="middle" font-size="9">perms, owner, size</text>
  <text x="285" y="153" text-anchor="middle" font-size="9">timestamps, ptrs</text>
  <rect x="360" y="120" width="220" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3" opacity="0.7"/>
  <text x="470" y="138" text-anchor="middle" font-size="9">file bytes stored in</text>
  <text x="470" y="153" text-anchor="middle" font-size="9">fixed-size blocks (4K typical)</text>
  <line x1="160" y1="100" x2="160" y2="120" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="285" y1="100" x2="285" y2="120" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
  <line x1="470" y1="100" x2="470" y2="120" stroke="#333" stroke-width="1" stroke-dasharray="3,3"/>
</svg>

Key components:
- Superblock: File system metadata
- Inode table: File metadata
- Data blocks: Actual file content
