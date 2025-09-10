# Linux I/O Architecture
## Understanding Input/Output in Linux Systems
---
## What is Linux I/O?
1. **Input/Output (I/O)** - Communication between CPU and external devices
1. Linux treats everything as a file
1. Unified interface for:
    - Regular files
    - Devices (block and character)
    - Sockets
    - Pipes
---
## File Descriptors
1. Integer handles to open files/resources
1. Standard descriptors:
    - `0` - stdin (standard input)
    - `1` - stdout (standard output)
    - `2` - stderr (standard error)
```c
int fd = open("/path/to/file", O_RDONLY);
read(fd, buffer, size);
close(fd);
```
---
## I/O System Calls
### Core Operations
1. `open()` - Open file/device
1. `read()` - Read data
1. `write()` - Write data
1. `close()` - Close descriptor
1. `lseek()` - Change file position
1. `ioctl()` - Device-specific control
---
## Virtual File System (VFS)
<svg viewBox="0 0 600 400" xmlns="http://www.w3.org/2000/svg">
  <!-- User Space -->
  <rect x="50" y="30" width="500" height="60" fill="#e8f4fd" stroke="#2196F3"/>
  <text x="300" y="65" text-anchor="middle" font-size="16" font-weight="bold">User Applications</text>
  <!-- System Call Interface -->
  <rect x="50" y="110" width="500" height="40" fill="#fff3e0" stroke="#ff9800"/>
  <text x="300" y="135" text-anchor="middle" font-size="14">System Call Interface</text>
  <!-- VFS Layer -->
  <rect x="50" y="170" width="500" height="60" fill="#f3e5f5" stroke="#9c27b0"/>
  <text x="300" y="205" text-anchor="middle" font-size="16" font-weight="bold">Virtual File System (VFS)</text>
  <!-- File Systems -->
  <rect x="70" y="250" width="100" height="50" fill="#e8f5e9" stroke="#4caf50"/>
  <text x="120" y="280" text-anchor="middle" font-size="12">ext4</text>
  <rect x="190" y="250" width="100" height="50" fill="#e8f5e9" stroke="#4caf50"/>
  <text x="240" y="280" text-anchor="middle" font-size="12">XFS</text>
  <rect x="310" y="250" width="100" height="50" fill="#e8f5e9" stroke="#4caf50"/>
  <text x="360" y="280" text-anchor="middle" font-size="12">Btrfs</text>
  <rect x="430" y="250" width="100" height="50" fill="#e8f5e9" stroke="#4caf50"/>
  <text x="480" y="280" text-anchor="middle" font-size="12">Device Files</text>
  <!-- Hardware -->
  <rect x="50" y="320" width="500" height="50" fill="#ffebee" stroke="#f44336"/>
  <text x="300" y="350" text-anchor="middle" font-size="14">Hardware Devices (Disks, Network, etc.)</text>
  <!-- Arrows -->
  <path d="M 300 90 L 300 110" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 300 150 L 300 170" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 300 230 L 300 250" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 300 300 L 300 320" stroke="black" stroke-width="2" marker-end="url(#arrowhead)"/>
  <!-- Arrow marker -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="black"/>
    </marker>
  </defs>
</svg>
---
## Buffered vs Unbuffered I/O
### Unbuffered (System Calls)
1. Direct kernel interaction
1. Immediate but expensive
1. `read()`, `write()`
### Buffered (stdio)
1. User-space buffering
1. Reduces system calls
1. `fread()`, `fwrite()`, `fprintf()`
```c
FILE *fp = fopen("file.txt", "r");
fread(buffer, 1, 1024, fp);
```
---
## I/O Models
<svg viewBox="0 0 700 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Blocking I/O -->
  <g transform="translate(50, 50)">
    <rect x="0" y="0" width="120" height="40" fill="#ffcdd2" stroke="#d32f2f"/>
    <text x="60" y="25" text-anchor="middle" font-size="14">Blocking I/O</text>
    <rect x="10" y="60" width="100" height="20" fill="#ef5350"/>
    <text x="60" y="75" text-anchor="middle" font-size="11" fill="white">Wait for data</text>
    <rect x="10" y="90" width="100" height="20" fill="#4caf50"/>
    <text x="60" y="105" text-anchor="middle" font-size="11" fill="white">Process data</text>
  </g>
  <!-- Non-blocking I/O -->
  <g transform="translate(200, 50)">
    <rect x="0" y="0" width="120" height="40" fill="#c8e6c9" stroke="#388e3c"/>
    <text x="60" y="25" text-anchor="middle" font-size="14">Non-blocking</text>
    <rect x="10" y="60" width="30" height="20" fill="#81c784"/>
    <rect x="45" y="60" width="30" height="20" fill="#81c784"/>
    <rect x="80" y="60" width="30" height="20" fill="#81c784"/>
    <text x="60" y="75" text-anchor="middle" font-size="11">Poll</text>
    <rect x="10" y="90" width="100" height="20" fill="#4caf50"/>
    <text x="60" y="105" text-anchor="middle" font-size="11" fill="white">Process data</text>
  </g>
  <!-- Async I/O -->
  <g transform="translate(350, 50)">
    <rect x="0" y="0" width="120" height="40" fill="#e1bee7" stroke="#7b1fa2"/>
    <text x="60" y="25" text-anchor="middle" font-size="14">Async I/O</text>
    <rect x="10" y="60" width="100" height="20" fill="#ba68c8"/>
    <text x="60" y="75" text-anchor="middle" font-size="11" fill="white">Submit request</text>
    <rect x="10" y="90" width="100" height="20" fill="#9c27b0"/>
    <text x="60" y="105" text-anchor="middle" font-size="11" fill="white">Do other work</text>
    <rect x="10" y="120" width="100" height="20" fill="#4caf50"/>
    <text x="60" y="135" text-anchor="middle" font-size="11" fill="white">Handle completion</text>
  </g>
  <!-- I/O Multiplexing -->
  <g transform="translate(500, 50)">
    <rect x="0" y="0" width="140" height="40" fill="#fff9c4" stroke="#f57c00"/>
    <text x="70" y="25" text-anchor="middle" font-size="14">I/O Multiplexing</text>
    <rect x="10" y="60" width="120" height="20" fill="#ffb74d"/>
    <text x="70" y="75" text-anchor="middle" font-size="11">select/poll/epoll</text>
    <rect x="10" y="90" width="120" height="20" fill="#ff9800"/>
    <text x="70" y="105" text-anchor="middle" font-size="11" fill="white">Monitor multiple FDs</text>
    <rect x="10" y="120" width="120" height="20" fill="#4caf50"/>
    <text x="70" y="135" text-anchor="middle" font-size="11" fill="white">Process ready FDs</text>
  </g>
</svg>
---

## Page Cache & Buffer Cache
### Page Cache
1. Caches file data in memory
1. Automatic and transparent
1. Improves read performance
### Buffer Cache
1. Caches filesystem metadata
1. Block device buffering
### Benefits
1. Reduces disk I/O
1. Speeds up repeated access
1. Write coalescing
---

## Advanced I/O Techniques
### Direct I/O
1. Bypass page cache with `O_DIRECT`
1. Database systems use case
### Memory-mapped I/O
1. Map files directly to memory
1. `mmap()` system call
### io_uring (Linux 5.1+)
1. High-performance async I/O
1. Ring buffers for submission/completion
1. Reduces syscall overhead
---

## Performance Tips
1. **Use appropriate buffer sizes** - Match filesystem block size
1. **Choose right I/O model** - Blocking vs async based on workload
1. **Leverage page cache** - Let kernel optimize for you
1. **Monitor with tools**:
    - `iostat` - I/O statistics
    - `iotop` - Per-process I/O
    - `strace` - Trace system calls
### Key Takeaway
Understanding Linux I/O layers helps optimize application performance!
