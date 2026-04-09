---
tags:
- concepts:io
- concepts:performance
- concepts:linux-kernel
level: advanced
category: operating-systems
audience:
- audiences:developers
---
# Zero-Copy in Linux
## Eliminating Unnecessary Data Copies for Maximum Performance
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

![title](svg/lectures/operating_systems/zero-copy-linux/title.svg)

## What is Zero-Copy?

1. A technique where the CPU does **not** copy data between memory regions
1. Traditional I/O involves multiple copies:
    - Device to kernel buffer
    - Kernel buffer to user buffer
    - User buffer back to kernel buffer (on send)
1. Zero-copy eliminates redundant copies
1. The goal: move data from source to destination with minimal CPU involvement

---

## Why Zero-Copy Matters

1. Memory bandwidth is a bottleneck in modern systems
1. Each copy wastes:
    - CPU cycles
    - Memory bandwidth
    - Cache pollution
    - Power
1. Network servers spending 60-80% of CPU on data copying is common
1. Zero-copy can yield 2-5x throughput improvements for I/O-heavy workloads

---

## Traditional I/O Path: The Problem

Reading a file and sending it over a network socket:

```c
char buf[BUF_SIZE];
read(fd, buf, BUF_SIZE);   /* 2 copies: disk→kernel, kernel→user */
write(sock, buf, BUF_SIZE); /* 2 copies: user→kernel, kernel→NIC */
```

Total: **4 copies**, **4 context switches**

![traditional_i_o_path_the_problem](svg/lectures/operating_systems/zero-copy-linux/traditional_i_o_path_the_problem.svg)

---

## DMA: The Foundation of Zero-Copy

1. **Direct Memory Access** (DMA) transfers data between devices and memory without CPU
1. The CPU sets up the transfer, the DMA engine does the work
1. Most modern hardware supports scatter-gather DMA
1. Scatter-gather DMA can read/write to non-contiguous memory regions
1. This is what makes kernel-level zero-copy possible

---

## Overview of Zero-Copy APIs and Subsystems

Organized from foundational to specialized:

1. **Memory mapping** - `mmap()`, `MAP_SHARED`
1. **File-to-socket transfer** - `sendfile()`
1. **Pipe-based splicing** - `splice()`, `tee()`, `vmsplice()`
1. **Networking** - `MSG_ZEROCOPY`, DPDK, XDP, AF_XDP
1. **Async I/O** - `io_uring` with fixed buffers
1. **Inter-thread communication** - shared memory, ring buffers, `memfd`
1. **GPU and device** - DMA-BUF, RDMA

---

## mmap(): Memory-Mapped Files

1. Maps a file directly into the process address space
1. The kernel page cache **is** the buffer - no copy to user space
1. Reading from the mapped region triggers page faults handled by the kernel
1. Writes go directly to page cache, flushed by kernel later

```c
void *addr = mmap(NULL, file_size,
                  PROT_READ, MAP_SHARED, fd, 0);
/* Access file data directly - no read() copy */
process_data(addr, file_size);
munmap(addr, file_size);
```

---

## mmap(): Advantages and Pitfalls

### Advantages
1. No copy from kernel buffer to user buffer
1. Multiple processes can share the same physical pages
1. Lazy loading via page faults (only load what you access)
1. Kernel manages page cache eviction automatically

### Pitfalls
1. Page faults can be expensive if access is random
1. No easy error handling (SIGBUS on I/O errors)
1. TLB pressure with many mappings
1. `MAP_POPULATE` or `madvise(MADV_SEQUENTIAL)` can help

---

## mmap() + write(): One Less Copy

```c
void *addr = mmap(NULL, file_size,
                  PROT_READ, MAP_SHARED, fd, 0);
write(sock, addr, file_size);
/* Only 3 copies instead of 4:
   disk→page_cache (DMA), page_cache→socket_buf, socket_buf→NIC (DMA) */
```

1. Eliminates the kernel-to-user copy
1. Still has a CPU copy from page cache to socket buffer
1. Better approaches exist for file-to-socket transfers

---

## sendfile(): File-to-Socket Transfer

1. Transfers data directly from one file descriptor to another **in kernel space**
1. User-space buffer is never involved
1. Introduced in Linux 2.2

```c
#include <sys/sendfile.h>

off_t offset = 0;
sendfile(sock_fd, file_fd, &offset, file_size);
```

1. With scatter-gather DMA: only **2 DMA copies**, zero CPU copies
1. Without scatter-gather DMA: one CPU copy (page cache to socket buffer)

---

## sendfile(): How It Works

![sendfile_how_it_works](svg/lectures/operating_systems/zero-copy-linux/sendfile_how_it_works.svg)

*With scatter-gather DMA, only buffer descriptors (pointers + lengths) are passed to the socket buffer.

---

## sendfile(): Limitations

1. Destination must be a socket (until Linux 2.6.33)
1. Since Linux 2.6.33: destination can be any file descriptor
1. Cannot modify data in transit (no transformation pipeline)
1. Cannot transfer between two sockets
1. For more flexibility, use `splice()`

---

## splice(): Pipe-Based Zero-Copy

1. Moves data between a file descriptor and a pipe without user-space copy
1. Uses the pipe as an in-kernel buffer
1. The pipe buffer holds **references** to pages, not copies

```c
#include <fcntl.h>

int pipefd[2];
pipe(pipefd);

/* Move data from file to pipe (zero-copy) */
splice(file_fd, &off, pipefd[1], NULL, len, SPLICE_F_MOVE);

/* Move data from pipe to socket (zero-copy) */
splice(pipefd[0], NULL, sock_fd, NULL, len, SPLICE_F_MOVE);
```

---

## splice(): Key Flags

1. `SPLICE_F_MOVE` - attempt to move pages instead of copying
1. `SPLICE_F_NONBLOCK` - non-blocking operation
1. `SPLICE_F_MORE` - more data coming (enables TCP corking)

### Advantages over sendfile()
1. Can transfer between **any** fd and a pipe
1. Composable: chain multiple splice operations
1. Works with sockets, files, devices, other pipes
1. Enables transformation pipelines via pipe intermediaries

---

## tee(): Duplicate Pipe Data Without Copying

1. Duplicates data in a pipe to another pipe **without consuming it**
1. True zero-copy: no data movement at all, only reference counting

```c
/* Duplicate pipe data for logging while forwarding */
int pipe_a[2], pipe_b[2];
pipe(pipe_a);
pipe(pipe_b);

/* Source → pipe_a */
splice(source_fd, NULL, pipe_a[1], NULL, len, 0);

/* Duplicate pipe_a → pipe_b (zero-copy) */
tee(pipe_a[0], pipe_b[1], len, 0);

/* pipe_a → destination, pipe_b → log */
splice(pipe_a[0], NULL, dest_fd, NULL, len, 0);
splice(pipe_b[0], NULL, log_fd, NULL, len, 0);
```

---

## vmsplice(): User Pages into a Pipe

1. Maps user-space memory into a pipe **without copying**
1. The pipe buffer references the user pages directly

```c
struct iovec iov = {
    .iov_base = user_buffer,
    .iov_len = len
};

/* Splice user memory into pipe (zero-copy) */
vmsplice(pipefd[1], &iov, 1, SPLICE_F_GIFT);

/* Then splice from pipe to socket */
splice(pipefd[0], NULL, sock_fd, NULL, len, 0);
```

1. `SPLICE_F_GIFT` - caller promises not to modify the pages
1. Useful for sending user-generated data to a socket without copy

---

## The splice() Family: Summary

| Syscall   | From          | To            | Zero-Copy Mechanism         |
|-----------|---------------|---------------|-----------------------------|
| `splice`  | fd ↔ pipe     | pipe ↔ fd     | Page reference transfer     |
| `tee`     | pipe          | pipe          | Page reference duplication  |
| `vmsplice`| user memory   | pipe          | User page pinning           |

All three work by manipulating **page references** in the pipe buffer rather than copying data.

---

## MSG_ZEROCOPY: Socket Send Without Copy

1. Added in Linux 4.14
1. Avoids copying user data into kernel socket buffer
1. Kernel pins user pages and DMA reads directly from them

```c
/* Enable zero-copy on socket */
int val = 1;
setsockopt(sock, SOL_SOCKET, SO_ZEROCOPY, &val, sizeof(val));

/* Send with zero-copy flag */
send(sock, buf, len, MSG_ZEROCOPY);

/* Must wait for completion notification before reusing buf */
struct msghdr msg = {};
recvmsg(sock, &msg, MSG_ERRQUEUE);
```

---

## MSG_ZEROCOPY: When to Use

1. Only beneficial for **large sends** (>10 KB typically)
1. Overhead: completion notification, page pinning
1. For small messages, the copy is cheaper than the bookkeeping
1. Supported protocols: TCP, UDP, raw sockets

### Performance Characteristics
1. Reduces CPU usage by ~5-8% for large transfers
1. Greatest benefit on 10 GbE / 25 GbE / 100 GbE links
1. Latency may increase slightly due to notification overhead

---

## DPDK: Data Plane Development Kit

1. User-space networking framework, bypasses the kernel entirely
1. NIC memory-mapped directly to user-space via `mmap()` + huge pages
1. Polling model instead of interrupts

### How It Achieves Zero-Copy
1. DMA writes packets directly to user-space memory (via IOMMU)
1. No kernel buffers, no `sk_buff` allocation, no context switches
1. Application reads/writes packet buffers directly

### Trade-offs
1. Dedicates CPU cores to polling
1. Kernel network stack features (firewall, routing) not available
1. Requires specific NIC drivers (PMD - Poll Mode Drivers)

---

## XDP: eXpress Data Path

1. Programmable hook at the **lowest point** in the Linux network stack
1. eBPF programs run before `sk_buff` allocation
1. Can drop, redirect, or modify packets before any kernel processing

### Zero-Copy Aspect
1. Operates on raw packet data in DMA-mapped memory
1. No `sk_buff` allocation, no socket buffer copies
1. Can redirect packets between interfaces without going through the stack

```c
SEC("xdp")
int xdp_prog(struct xdp_md *ctx) {
    void *data = (void *)(long)ctx->data;
    void *data_end = (void *)(long)ctx->data_end;
    /* Process packet directly in DMA buffer */
    return XDP_PASS; /* or XDP_DROP, XDP_TX, XDP_REDIRECT */
}
```

---

## AF_XDP: Zero-Copy Socket Interface

1. Combines XDP with a user-space socket interface
1. Packets delivered to user-space via shared memory ring buffers
1. **True zero-copy mode**: NIC DMA writes directly to user-space memory (UMEM)

```c
/* Setup UMEM (shared packet memory) */
struct xsk_umem *umem;
xsk_umem__create(&umem, buffer, size, &fill_ring, &comp_ring, NULL);

/* Create AF_XDP socket */
struct xsk_socket *xsk;
xsk_socket__create(&xsk, ifname, queue_id, umem, &rx, &tx, NULL);
```

1. Four shared rings: Fill, Completion, RX, TX
1. Keeps kernel network stack available (unlike DPDK)
1. NIC must support XDP zero-copy driver mode

---

## AF_XDP Architecture

![afxdp_architecture](svg/lectures/operating_systems/zero-copy-linux/afxdp_architecture.svg)

---

## io_uring: Zero-Copy with Fixed Buffers

1. `io_uring` supports zero-copy through pre-registered (fixed) buffers
1. Buffers pinned in memory, DMA-accessible, no per-I/O mapping

```c
struct iovec iov = { .iov_base = buf, .iov_len = size };

/* Pin buffers in kernel */
io_uring_register_buffers(&ring, &iov, 1);

/* Read directly into fixed buffer (no extra copy) */
io_uring_prep_read_fixed(sqe, fd, buf, size, 0, 0);
```

---

## io_uring: Zero-Copy Send (Linux 6.0+)

1. `IORING_OP_SEND_ZC` - zero-copy network send via `io_uring`
1. Similar to `MSG_ZEROCOPY` but with `io_uring` completion model
1. Avoids copy from user buffer to kernel socket buffer

```c
struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
io_uring_prep_send_zc(sqe, sock_fd, buf, len, 0, 0);
io_uring_submit(&ring);

/* Completion notifies when buf can be reused */
```

1. Also supports `IORING_OP_SENDMSG_ZC` for `sendmsg`-style zero-copy
1. Notification via CQE flags (`IORING_CQE_F_NOTIF`)

---

## Shared Memory: Zero-Copy Between Processes

1. The most fundamental form of zero-copy IPC
1. Multiple processes map the same physical memory

### POSIX Shared Memory
```c
/* Process A: create and write */
int shm_fd = shm_open("/my_shm", O_CREAT | O_RDWR, 0666);
ftruncate(shm_fd, SHM_SIZE);
void *ptr = mmap(NULL, SHM_SIZE, PROT_READ | PROT_WRITE,
                 MAP_SHARED, shm_fd, 0);
memcpy(ptr, data, len);

/* Process B: open and read - no copy, same physical pages */
int shm_fd = shm_open("/my_shm", O_RDONLY, 0);
void *ptr = mmap(NULL, SHM_SIZE, PROT_READ,
                 MAP_SHARED, shm_fd, 0);
process(ptr, len);
```

---

## memfd_create(): Anonymous Shared Memory

1. Creates anonymous file descriptors backed by memory
1. Can be passed to other processes via Unix domain socket `SCM_RIGHTS`
1. Ideal for zero-copy IPC without filesystem visibility

```c
/* Create anonymous memory file */
int memfd = memfd_create("shared_buf", MFD_CLOEXEC);
ftruncate(memfd, BUF_SIZE);

/* Map it */
void *buf = mmap(NULL, BUF_SIZE, PROT_READ | PROT_WRITE,
                 MAP_SHARED, memfd, 0);

/* Send fd to another process via SCM_RIGHTS */
send_fd_over_unix_socket(unix_sock, memfd);
```

1. Combined with `memfd_create()` + `MFD_ALLOW_SEALING`: can enforce immutability

---

## Cross-Process Ring Buffers

1. Build lock-free SPSC (single-producer, single-consumer) queues in shared memory
1. Zero-copy: producer and consumer access the same memory
1. Used by many high-performance frameworks

```c
/* Shared ring buffer structure in shared memory */
struct ring_buffer {
    _Atomic uint64_t head;  /* written by producer */
    _Atomic uint64_t tail;  /* written by consumer */
    char data[RING_SIZE];   /* shared data region */
};

/* Producer writes directly, consumer reads directly */
/* No copies, no syscalls, only memory barriers */
```

1. Examples: LMAX Disruptor pattern, DPDK rte_ring, io_uring itself

---

## copy_file_range(): In-Kernel File Copy

1. Copies data between two file descriptors **entirely in kernel space**
1. No user-space buffer involvement
1. Can leverage filesystem-level optimizations (reflinks on Btrfs/XFS)

```c
#include <unistd.h>

loff_t off_in = 0, off_out = 0;
copy_file_range(fd_in, &off_in, fd_out, &off_out, len, 0);
```

1. On COW filesystems (Btrfs, XFS): may create reflinks (no data copy at all)
1. On other filesystems: kernel-space copy (still saves 2 user-kernel transitions)

---

## process_vm_readv / process_vm_writev

1. Transfer data between address spaces of two processes
1. Single system call, single copy (directly between process memories)
1. Half the copies compared to shared memory + `read()`/`write()` over pipes

```c
/* Read from remote process directly */
struct iovec local_iov = { .iov_base = local_buf, .iov_len = len };
struct iovec remote_iov = { .iov_base = remote_addr, .iov_len = len };

process_vm_readv(target_pid, &local_iov, 1, &remote_iov, 1, 0);
```

1. Not truly zero-copy (one copy remains) but avoids kernel intermediate buffers
1. Requires `ptrace` permissions or `CAP_SYS_PTRACE`

---

## DMA-BUF: Zero-Copy Between Devices

1. Kernel framework for sharing buffers between hardware devices
1. Originally for GPU but now used broadly (cameras, video encoders, displays)

### Use Case: Camera → GPU → Display
1. Camera DMA writes frame to buffer
1. Same buffer passed to GPU for processing (no copy)
1. GPU output buffer passed to display controller (no copy)

1. Exported via file descriptors, can be shared between processes
1. User-space access via `mmap()` of the DMA-BUF fd
1. Used by V4L2 (video), DRM/KMS (display), and GPU drivers

---

## RDMA: Remote Direct Memory Access

1. Network transfer that bypasses both the kernel **and** remote CPU
1. Source NIC reads from source memory, writes directly to destination memory
1. True zero-copy across the network

### Key Technologies
1. **InfiniBand** - dedicated RDMA fabric
1. **RoCE** (RDMA over Converged Ethernet) - RDMA on standard Ethernet
1. **iWARP** - RDMA over TCP/IP

### Programming Interface
1. **libibverbs** - low-level RDMA verbs API
1. Register memory regions, create queue pairs, post send/receive work requests
1. Completion via completion queues (similar concept to `io_uring`)

---

## Summary: API Comparison

| API / Subsystem        | Scope                  | True Zero-Copy? | Min Kernel |
|------------------------|------------------------|-----------------|------------|
| `mmap()`               | File ↔ memory          | Yes             | All        |
| `sendfile()`           | File → socket          | Yes*            | 2.2        |
| `splice()`/`tee()`     | fd ↔ pipe ↔ fd         | Yes             | 2.6.17     |
| `vmsplice()`           | User mem → pipe        | Yes             | 2.6.17     |
| `MSG_ZEROCOPY`         | Socket send            | Yes             | 4.14       |
| `io_uring` fixed bufs  | Any I/O                | Yes             | 5.1        |
| `io_uring` send_zc     | Socket send            | Yes             | 6.0        |
| `copy_file_range()`    | File → file            | Depends on FS   | 4.5        |
| `process_vm_readv()`   | Process → process      | No (1 copy)     | 3.2        |
| Shared memory          | Process ↔ process      | Yes             | All        |
| `memfd_create()`       | Process ↔ process      | Yes             | 3.17       |
| XDP / AF_XDP           | Network packets        | Yes             | 4.18       |
| DPDK                   | Network packets        | Yes             | N/A        |
| DMA-BUF                | Device ↔ device        | Yes             | 3.3        |
| RDMA                   | Machine ↔ machine      | Yes             | 2.6.11     |

*With scatter-gather DMA support on the NIC.

---

## Decision Guide: Which API to Use?

1. **Serving files over network** → `sendfile()` (simple) or `splice()` (flexible)
1. **Transforming data in a pipeline** → `splice()` + `tee()`
1. **High-throughput network send** → `MSG_ZEROCOPY` or `io_uring send_zc`
1. **Line-rate packet processing** → AF_XDP (with kernel) or DPDK (bypass kernel)
1. **IPC between processes** → shared memory / `memfd_create()` + ring buffer
1. **File-to-file copy** → `copy_file_range()`
1. **GPU / multimedia pipeline** → DMA-BUF
1. **Cross-machine transfer** → RDMA
1. **General async I/O with minimal copies** → `io_uring` with fixed buffers

---

## Kernel Internals: How Zero-Copy Works

1. The kernel avoids copying by manipulating **page references**
1. Key kernel structures:
    - `struct page` - represents a physical memory page
    - `struct bio` - block I/O request, holds page references
    - `struct sk_buff` - network buffer, can reference external pages
    - `struct pipe_buffer` - holds page references in pipes
1. `get_page()` / `put_page()` manage reference counts
1. Data stays in place; only metadata (pointers, lengths) is copied

---

## Common Pattern: Page Reference Passing

```misc
sendfile(sock_fd, file_fd, ...):

1. DMA reads file data into page cache pages
2. Socket buffer gets references to those same pages
3. NIC DMA reads directly from page cache pages
4. Pages are released when NIC is done (via completion)
```

1. The data in the page cache is never copied
1. Only page references and buffer descriptors move between subsystems
1. This is the fundamental mechanism behind most Linux zero-copy APIs

---

## Pitfalls and Considerations

1. **Buffer lifetime management** - user must not reuse buffers before completion
1. **Page pinning costs** - pinning many pages can pressure memory management
1. **Small transfer overhead** - zero-copy setup cost can exceed copy cost for small buffers
1. **Hardware requirements** - scatter-gather DMA, IOMMU for some features
1. **Alignment requirements** - some APIs require page-aligned buffers
1. **Error handling** - more complex than simple `read()`/`write()`

---

## When NOT to Use Zero-Copy

1. **Small messages** (<4 KB) - copy is cheaper than bookkeeping
1. **Data that needs transformation** - if you must modify data, you need a copy anyway
1. **Simple applications** - added complexity may not be worth it
1. **Latency-sensitive small I/O** - page pinning and notifications add latency
1. Profile first: measure whether data copying is actually your bottleneck

---

## Conclusion

1. Zero-copy is a spectrum, not a single technique
1. Linux provides a rich set of APIs for different use cases
1. The foundation is DMA + kernel page reference management
1. Choose the right API based on your data flow pattern
1. Always benchmark: zero-copy overhead can exceed copy cost for small transfers
1. The trend: `io_uring` is unifying many zero-copy patterns under one interface
