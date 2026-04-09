---
tags:
- concepts:io
- concepts:linux-kernel
- concepts:filesystems
level: advanced
category: operating-systems
audience:
- audiences:developers

---
# Linux I/O Architecture
## Understanding Input/Output in Linux Systems
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## What is Linux I/O?

![title](svg/lectures/operating_systems/linux-io/title.svg)

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
![virtual_file_system_vfs](svg/lectures/operating_systems/linux-io/virtual_file_system_vfs.svg)

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
![i_o_models](svg/lectures/operating_systems/linux-io/i_o_models.svg)

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
