---
tags:
  - infrastructure:linux
  - languages:c
  - concepts:systems-programming
level: advanced
category: operating-systems
audience:
  - audiences:developers
  - audiences:devops

---
# Zero Copy I/O in Linux

---

## What is Zero Copy?

1. **Eliminate data copying** - Data moves without CPU involvement
1. **Reduce system calls** - Fewer kernel transitions
1. **Direct memory transfer** - Between file descriptors
1. **Higher throughput** - Less CPU overhead
1. **Lower latency** - Reduced processing time

---

## The Copy Problem

![the_copy_problem](svg/courses/operating_systems/linux-systems-programming/19_zero_copy/the_copy_problem.svg)

---

## Traditional File Transfer

```c
// Inefficient file transfer
int transfer_file_traditional(int in_fd, int out_fd) {
    char buffer[8192];
    ssize_t bytes_read, bytes_written;

    while ((bytes_read = read(in_fd, buffer, sizeof(buffer))) > 0) {
        bytes_written = write(out_fd, buffer, bytes_read);
        if (bytes_written != bytes_read) {
            return -1;
        }
    }

    return bytes_read == 0 ? 0 : -1;
}
```

1. **Multiple copies** - Disk → Kernel → User → Socket
1. **Context switches** - User/kernel transitions
1. **CPU overhead** - Processing time for copying

---

## sendfile() System Call

```c
#include <sys/sendfile.h>

// Zero-copy file transfer
ssize_t sendfile(int out_fd, int in_fd, off_t *offset, size_t count);

// Example usage
int transfer_file_sendfile(int in_fd, int out_fd) {
    struct stat st;
    fstat(in_fd, &st);

    ssize_t sent = sendfile(out_fd, in_fd, NULL, st.st_size);
    if (sent == st.st_size) {
        return 0;  // Success
    }

    return -1;  // Error or partial transfer
}
```

1. **Direct transfer** - File to socket without user space
1. **Single system call** - Fewer kernel transitions
1. **No user buffers** - Data never enters user space

---

## sendfile() Zero Copy Flow

![sendfile_zero_copy_flow](svg/courses/operating_systems/linux-systems-programming/19_zero_copy/sendfile_zero_copy_flow.svg)

---

## sendfile() Limitations

```c
// sendfile() only works with:
// - Regular files as input (in_fd)
// - Sockets as output (out_fd)

// Won't work for:
int pipe_fds[2];
pipe(pipe_fds);
sendfile(pipe_fds[1], file_fd, NULL, size); // Error

// Socket to socket also fails
sendfile(socket2_fd, socket1_fd, NULL, size); // Error
```

1. **Input restriction** - Only regular files
1. **Output restriction** - Only sockets
1. **No transformation** - Cannot modify data in transit

---

## splice() System Call

```c
#include <fcntl.h>

ssize_t splice(int fd_in, loff_t *off_in,
               int fd_out, loff_t *off_out,
               size_t len, unsigned int flags);

// Example: file to pipe
int pipe_fds[2];
pipe(pipe_fds);

ssize_t bytes = splice(file_fd, NULL,           // Source: file
                      pipe_fds[1], NULL,        // Dest: pipe write end
                      8192,                     // Length
                      SPLICE_F_MOVE);           // Flags
```

1. **More flexible** - Works with pipes, files, sockets
1. **Page-level operations** - Moves memory pages
1. **Atomic operations** - All-or-nothing transfers

---

## splice() Flags

```c
// splice() flags
SPLICE_F_MOVE     // Move pages instead of copying
SPLICE_F_NONBLOCK // Non-blocking operation
SPLICE_F_MORE     // More data is coming
SPLICE_F_GIFT     // Give away pages to destination

// Example with multiple flags
ssize_t bytes = splice(in_fd, NULL, out_fd, NULL, size,
                      SPLICE_F_MOVE | SPLICE_F_NONBLOCK);

if (bytes == -1 && errno == EAGAIN) {
    // Would block, try again later
}
```

---

## Pipe-based Zero Copy

```c
// Use pipes as intermediate buffers
int create_transfer_pipe(int file_fd, int socket_fd, size_t size) {
    int pipe_fds[2];
    if (pipe(pipe_fds) == -1) {
        return -1;
    }

    // File → Pipe
    ssize_t to_pipe = splice(file_fd, NULL, pipe_fds[1], NULL,
                            size, SPLICE_F_MOVE);

    if (to_pipe > 0) {
        // Pipe → Socket
        ssize_t to_socket = splice(pipe_fds[0], NULL, socket_fd, NULL,
                                  to_pipe, SPLICE_F_MOVE);

        close(pipe_fds[0]);
        close(pipe_fds[1]);
        return to_socket;
    }

    close(pipe_fds[0]);
    close(pipe_fds[1]);
    return -1;
}
```

---

## tee() System Call

```c
#include <fcntl.h>

ssize_t tee(int fd_in, int fd_out, size_t len, unsigned int flags);

// Duplicate data in pipe without consuming
int duplicate_pipe_data(int pipe_read, int pipe_write, size_t len) {
    return tee(pipe_read, pipe_write, len, SPLICE_F_NONBLOCK);
}

// Example: log all data passing through
ssize_t bytes = tee(input_pipe, log_pipe, 8192, 0);
if (bytes > 0) {
    // Data is now in both pipes
    write_to_log(log_pipe, bytes);
    process_data(input_pipe, bytes);
}
```

1. **Data duplication** - Copy between two pipes
1. **Non-consuming** - Original data remains in source
1. **Monitoring** - Useful for debugging/logging

---

## vmsplice() System Call

```c
#include <fcntl.h>

ssize_t vmsplice(int fd, const struct iovec *iov,
                 unsigned long nr_segs, unsigned int flags);

// Move user-space memory into pipe
struct iovec iov;
iov.iov_base = user_buffer;
iov.iov_len = buffer_size;

ssize_t bytes = vmsplice(pipe_write_fd, &iov, 1, SPLICE_F_GIFT);

// SPLICE_F_GIFT transfers ownership of pages to kernel
// User space should not access buffer after this
```

1. **User to kernel** - Move user pages to pipe
1. **Memory ownership** - Can transfer page ownership
1. **Efficiency** - Avoids copying from user space

---

## Zero Copy Architecture

![zero_copy_architecture](svg/courses/operating_systems/linux-systems-programming/19_zero_copy/zero_copy_architecture.svg)

---

## Complete Zero Copy Server

```c
struct zero_copy_server {
    int server_fd;
    int epoll_fd;
    int pipe_fds[2];
};

int handle_client_request(int client_fd, int file_fd) {
    struct stat st;
    if (fstat(file_fd, &st) == -1) {
        return -1;
    }

    // Try sendfile first (most efficient)
    ssize_t sent = sendfile(client_fd, file_fd, NULL, st.st_size);
    if (sent == st.st_size) {
        return 0;
    }

    // Fallback to splice if sendfile fails
    return transfer_with_splice(client_fd, file_fd, st.st_size);
}
```

---

## Zero Copy Server: Splice Transfer

```c
int transfer_with_splice(int socket_fd, int file_fd, size_t size) {
    int pipe_fds[2];
    if (pipe(pipe_fds) == -1) {
        return -1;
    }

    ssize_t total_sent = 0;
    while (total_sent < size) {
        ssize_t to_pipe = splice(file_fd, NULL, pipe_fds[1], NULL,
                                size - total_sent, SPLICE_F_MOVE);
        if (to_pipe <= 0) break;

        ssize_t to_socket = splice(pipe_fds[0], NULL, socket_fd, NULL,
                                  to_pipe, SPLICE_F_MOVE);
        if (to_socket <= 0) break;

        total_sent += to_socket;
    }

    close(pipe_fds[0]);
    close(pipe_fds[1]);
    return total_sent == size ? 0 : -1;
}
```

---

## Memory Mapped I/O

```c
#include <sys/mman.h>

// Map file into memory
void *mmap_transfer(int in_fd, int out_fd, size_t size) {
    void *mapped = mmap(NULL, size, PROT_READ, MAP_SHARED, in_fd, 0);
    if (mapped == MAP_FAILED) {
        return NULL;
    }

    // Write mapped memory to output
    ssize_t written = write(out_fd, mapped, size);

    munmap(mapped, size);
    return written == size ? mapped : NULL;
}

// Advanced: copy between mappings
int mmap_copy(int src_fd, int dst_fd, size_t size) {
    void *src = mmap(NULL, size, PROT_READ, MAP_SHARED, src_fd, 0);
    void *dst = mmap(NULL, size, PROT_WRITE, MAP_SHARED, dst_fd, 0);

    if (src != MAP_FAILED && dst != MAP_FAILED) {
        memcpy(dst, src, size); // Still a copy, but efficient
    }

    munmap(src, size);
    munmap(dst, size);
    return 0;
}
```

---

## Direct I/O and Zero Copy

```c
// Combine O_DIRECT with zero copy
int open_direct_io(const char *filename) {
    int fd = open(filename, O_RDONLY | O_DIRECT);
    if (fd == -1) {
        return -1;
    }

    // Ensure proper alignment for Direct I/O
    posix_fadvise(fd, 0, 0, POSIX_FADV_SEQUENTIAL);

    return fd;
}

// Aligned buffer for Direct I/O + vmsplice
void *create_aligned_buffer(size_t size) {
    void *buffer;
    int ret = posix_memalign(&buffer, 4096, size);
    return ret == 0 ? buffer : NULL;
}
```

---

## Network Zero Copy Optimization

```c
// Enable TCP_CORK for better zero copy performance
int enable_tcp_cork(int socket_fd) {
    int flag = 1;
    return setsockopt(socket_fd, IPPROTO_TCP, TCP_CORK, &flag, sizeof(flag));
}

// Disable Nagle's algorithm
int disable_nagle(int socket_fd) {
    int flag = 1;
    return setsockopt(socket_fd, IPPROTO_TCP, TCP_NODELAY, &flag, sizeof(flag));
}

// Use MSG_MORE for efficient sending
ssize_t send_with_more(int socket_fd, const void *data, size_t len) {
    return send(socket_fd, data, len, MSG_MORE);
}
```

---

## Scatter-Gather I/O

```c
#include <sys/uio.h>

// Vectored I/O operations
ssize_t readv(int fd, const struct iovec *iov, int iovcnt);
ssize_t writev(int fd, const struct iovec *iov, int iovcnt);

// Example: gather multiple buffers for writing
int scatter_gather_example(int fd) {
    char header[] = "HTTP/1.1 200 OK\r\n\r\n";
    char body[] = "Hello World";

    struct iovec iov[2];
    iov[0].iov_base = header;
    iov[0].iov_len = strlen(header);
    iov[1].iov_base = body;
    iov[1].iov_len = strlen(body);

    return writev(fd, iov, 2);
}
```

---

## Zero Copy with io_uring

```c
#include <liburing.h>

// Zero copy with io_uring
int uring_zero_copy(struct io_uring *ring, int in_fd, int out_fd) {
    // Prepare splice operation
    struct io_uring_sqe *sqe = io_uring_get_sqe(ring);

    // Use splice through io_uring
    io_uring_prep_splice(sqe, in_fd, -1, out_fd, -1, 8192,
                         SPLICE_F_MOVE);

    io_uring_submit(ring);

    struct io_uring_cqe *cqe;
    io_uring_wait_cqe(ring, &cqe);

    int result = cqe->res;
    io_uring_cqe_seen(ring, cqe);

    return result;
}
```

---

## Performance Measurement

```c
// Benchmark zero copy vs traditional copy
struct benchmark_result {
    double traditional_time;
    double zero_copy_time;
    size_t bytes_transferred;
    double speedup;
};

struct benchmark_result benchmark_transfer(const char *filename,
                                         int socket_fd) {
    struct benchmark_result result = {0};
    int fd = open(filename, O_RDONLY);
    struct stat st;
    fstat(fd, &st);
    result.bytes_transferred = st.st_size;

    // Traditional copy benchmark
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    traditional_copy(fd, socket_fd);
    clock_gettime(CLOCK_MONOTONIC, &end);
    result.traditional_time = timespec_diff(&start, &end);

    // Zero copy benchmark
    lseek(fd, 0, SEEK_SET);
    clock_gettime(CLOCK_MONOTONIC, &start);
    sendfile_copy(fd, socket_fd, st.st_size);
    clock_gettime(CLOCK_MONOTONIC, &end);
    result.zero_copy_time = timespec_diff(&start, &end);

    result.speedup = result.traditional_time / result.zero_copy_time;

    close(fd);
    return result;
}
```

---

## Error Handling in Zero Copy

```c
// Robust zero copy with fallback
ssize_t robust_zero_copy_transfer(int in_fd, int out_fd, size_t size) {
    ssize_t transferred = 0;

    // Try sendfile first
    transferred = sendfile(out_fd, in_fd, NULL, size);
    if (transferred == size) {
        return transferred;
    }

    if (transferred == -1) {
        if (errno == EINVAL || errno == ENOSYS) {
            // sendfile not supported, try splice
            return splice_transfer(in_fd, out_fd, size);
        }
        return -1;
    }

    // Partial transfer - continue with remaining data
    size_t remaining = size - transferred;
    ssize_t additional = splice_transfer(in_fd, out_fd, remaining);

    return additional > 0 ? transferred + additional : transferred;
}
```

---

## Buffer Management

```c
// Ring buffer for zero copy operations
struct zero_copy_ring {
    void *buffer;
    size_t size;
    size_t head;
    size_t tail;
    int pipe_read;
    int pipe_write;
};

struct zero_copy_ring *create_zero_copy_ring(size_t size) {
    struct zero_copy_ring *ring = malloc(sizeof(*ring));

    // Create pipe for zero copy transfers
    if (pipe(ring->pipe_fds) == -1) {
        free(ring);
        return NULL;
    }

    // Set pipe to maximum capacity
    fcntl(ring->pipe_write, F_SETPIPE_SZ, size);

    ring->buffer = NULL; // No user buffer needed
    ring->size = size;
    ring->head = ring->tail = 0;

    return ring;
}
```

---

## Large File Handling

```c
// Handle files larger than pipe buffer capacity
int transfer_large_file(int in_fd, int out_fd) {
    struct stat st;
    fstat(in_fd, &st);

    const size_t chunk_size = 64 * 1024; // 64KB chunks
    off_t offset = 0;

    while (offset < st.st_size) {
        size_t to_transfer = min(chunk_size, st.st_size - offset);

        ssize_t sent = sendfile(out_fd, in_fd, &offset, to_transfer);
        if (sent <= 0) {
            return -1;
        }

        offset += sent;
    }

    return 0;
}

// Non-blocking large file transfer
int transfer_large_file_async(int in_fd, int out_fd, int epoll_fd) {
    // Set socket to non-blocking
    set_nonblocking(out_fd);

    // Register for EPOLLOUT events
    struct epoll_event ev;
    ev.events = EPOLLOUT;
    ev.data.fd = out_fd;
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, out_fd, &ev);

    // Continue transfer when socket is ready
    return 0;
}
```

---

## Platform-Specific Optimizations

```c
// Linux-specific optimizations
#ifdef __linux__

// Use splice for maximum efficiency
#define ZERO_COPY_METHOD splice_transfer

// Enable TCP_CORK for batching
int optimize_tcp_socket(int fd) {
    int cork = 1;
    setsockopt(fd, IPPROTO_TCP, TCP_CORK, &cork, sizeof(cork));

    // Disable when done sending
    cork = 0;
    setsockopt(fd, IPPROTO_TCP, TCP_CORK, &cork, sizeof(cork));

    return 0;
}

#else

// FreeBSD: use sendfile with different signature
#define ZERO_COPY_METHOD bsd_sendfile_transfer

int bsd_sendfile_transfer(int in_fd, int out_fd, size_t size) {
    off_t sent = 0;
    return sendfile(in_fd, out_fd, 0, size, NULL, &sent, 0);
}

#endif
```

---

## Memory Page Alignment

```c
// Ensure optimal page alignment for zero copy
void *allocate_aligned_buffer(size_t size) {
    size_t page_size = getpagesize();
    size_t aligned_size = (size + page_size - 1) & ~(page_size - 1);

    void *buffer = aligned_alloc(page_size, aligned_size);
    if (buffer) {
        // Lock pages in memory for performance
        mlock(buffer, aligned_size);
    }

    return buffer;
}

// Check if buffer is page-aligned
int is_page_aligned(void *ptr) {
    uintptr_t addr = (uintptr_t)ptr;
    return (addr & (getpagesize() - 1)) == 0;
}
```

---

## Monitoring Zero Copy Performance

```c
// Performance counters for zero copy operations
struct zero_copy_stats {
    atomic_long sendfile_calls;
    atomic_long sendfile_bytes;
    atomic_long splice_calls;
    atomic_long splice_bytes;
    atomic_long fallback_calls;
    atomic_long errors;
};

void update_zero_copy_stats(enum transfer_method method,
                           ssize_t bytes, int success) {
    switch (method) {
        case SENDFILE:
            atomic_fetch_add(&stats.sendfile_calls, 1);
            if (success && bytes > 0) {
                atomic_fetch_add(&stats.sendfile_bytes, bytes);
            }
            break;

        case SPLICE:
            atomic_fetch_add(&stats.splice_calls, 1);
            if (success && bytes > 0) {
                atomic_fetch_add(&stats.splice_bytes, bytes);
            }
            break;
    }

    if (!success) {
        atomic_fetch_add(&stats.errors, 1);
    }
}
```

---

## Integration with Web Servers

```c
// HTTP static file server with zero copy
int serve_static_file(int client_fd, const char *filepath) {
    int file_fd = open(filepath, O_RDONLY);
    if (file_fd == -1) {
        return send_404_response(client_fd);
    }

    struct stat st;
    fstat(file_fd, &st);

    // Send HTTP headers first
    char headers[512];
    snprintf(headers, sizeof(headers),
             "HTTP/1.1 200 OK\r\n"
             "Content-Length: %ld\r\n"
             "Content-Type: application/octet-stream\r\n"
             "\r\n", st.st_size);

    write(client_fd, headers, strlen(headers));

    // Zero copy file transfer
    ssize_t sent = sendfile(client_fd, file_fd, NULL, st.st_size);

    close(file_fd);
    return sent == st.st_size ? 0 : -1;
}
```

---

## Database Applications

```c
// Zero copy for database log shipping
int replicate_wal_segment(int master_fd, int replica_fd) {
    // WAL (Write-Ahead Log) segment transfer
    struct stat st;
    fstat(master_fd, &st);

    // Send WAL header
    struct wal_header header;
    header.size = st.st_size;
    header.checksum = calculate_checksum(master_fd);
    write(replica_fd, &header, sizeof(header));

    // Zero copy WAL data
    return sendfile(replica_fd, master_fd, NULL, st.st_size);
}
```

---

## Content Delivery Networks

```c
// CDN edge server zero copy
struct cache_entry {
    int fd;
    size_t size;
    time_t last_modified;
    char etag[64];
};

int serve_cached_content(int client_fd, struct cache_entry *entry) {
    // Send HTTP headers with caching info
    char headers[1024];
    snprintf(headers, sizeof(headers),
             "HTTP/1.1 200 OK\r\n"
             "Content-Length: %zu\r\n"
             "ETag: %s\r\n"
             "Cache-Control: public, max-age=3600\r\n"
             "\r\n", entry->size, entry->etag);

    write(client_fd, headers, strlen(headers));

    // Zero copy cached content
    return sendfile(client_fd, entry->fd, NULL, entry->size);
}
```

---

## Security Considerations

```c
// Secure zero copy with validation
int secure_file_transfer(int client_fd, const char *requested_path) {
    char safe_path[PATH_MAX];

    // Validate and sanitize path
    if (!is_safe_path(requested_path, safe_path)) {
        return send_403_response(client_fd);
    }

    // Check permissions
    if (access(safe_path, R_OK) != 0) {
        return send_403_response(client_fd);
    }

    // Rate limiting
    if (!check_rate_limit(client_fd)) {
        return send_429_response(client_fd);
    }

    // Proceed with zero copy transfer
    return transfer_file_zero_copy(client_fd, safe_path);
}
```

---

## Debugging Zero Copy

```c
// Debug zero copy operations
void debug_zero_copy_transfer(int in_fd, int out_fd, size_t size) {
    struct stat in_stat, out_stat;
    fstat(in_fd, &in_stat);
    fstat(out_fd, &out_stat);

    printf("Zero copy debug:\n");
    printf("  Input fd: %d, size: %ld, type: %s\n",
           in_fd, in_stat.st_size, get_file_type(&in_stat));
    printf("  Output fd: %d, type: %s\n",
           out_fd, get_socket_type(out_fd));
    printf("  Transfer size: %zu\n", size);

    // Check if zero copy is possible
    if (S_ISREG(in_stat.st_mode) && is_socket(out_fd)) {
        printf("  sendfile() possible: YES\n");
    } else {
        printf("  sendfile() possible: NO, will use splice()\n");
    }
}
```

---

## Testing Zero Copy

```c
// Unit tests for zero copy functionality
int test_zero_copy_methods() {
    int test_fd = create_test_file(1024 * 1024); // 1MB test file
    int socket_fds[2];
    socketpair(AF_UNIX, SOCK_STREAM, 0, socket_fds);

    // Test sendfile
    assert(sendfile(socket_fds[0], test_fd, NULL, 1024) == 1024);

    // Test splice
    int pipe_fds[2];
    pipe(pipe_fds);
    assert(splice(test_fd, NULL, pipe_fds[1], NULL, 1024, 0) == 1024);
    assert(splice(pipe_fds[0], NULL, socket_fds[0], NULL, 1024, 0) == 1024);

    // Cleanup
    close(test_fd);
    close(socket_fds[0]);
    close(socket_fds[1]);
    close(pipe_fds[0]);
    close(pipe_fds[1]);

    return 0;
}
```

---

## Best Practices

1. **Try sendfile() first** - Most efficient for file-to-socket
1. **Use splice() for flexibility** - Works with pipes and sockets
1. **Handle partial transfers** - Check return values carefully
1. **Combine with non-blocking I/O** - For scalable servers
1. **Measure performance gains** - Verify benefits in your use case
1. **Have fallback methods** - Not all systems support zero copy

---

## Common Pitfalls

1. **Assuming full transfer** - Check for partial operations
1. **Ignoring error conditions** - Handle EINTR, EAGAIN properly
1. **File descriptor types** - Verify compatibility before calling
1. **Memory alignment** - Important for Direct I/O
1. **Resource cleanup** - Close pipes and file descriptors
1. **Platform differences** - Different signatures across OSes

---

## Future Developments

1. **io_uring integration** - Modern async zero copy
1. **Hardware acceleration** - NIC-level zero copy
1. **Storage optimizations** - NVMe direct access
1. **Container optimization** - Efficient data sharing
1. **Network protocols** - QUIC and HTTP/3 optimizations

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
1. Reduces CPU usage by ~5-8% on 10/25/100 GbE links
1. Latency may increase slightly due to notification overhead

---

## io_uring: Zero-Copy Send (Linux 6.0+)

1. `IORING_OP_SEND_ZC` — zero-copy network send via `io_uring`
1. Similar to `MSG_ZEROCOPY` but with `io_uring`'s completion model
1. Avoids copy from user buffer to kernel socket buffer

```c
struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
io_uring_prep_send_zc(sqe, sock_fd, buf, len, 0, 0);
io_uring_submit(&ring);
/* Completion notifies when buf can be reused */
```

1. Also `IORING_OP_SENDMSG_ZC` for `sendmsg`-style zero-copy
1. Notification via CQE flags (`IORING_CQE_F_NOTIF`)

---

## copy_file_range(): In-Kernel File Copy

1. Copies data between two file descriptors **entirely in kernel space**
1. No user-space buffer involvement
1. On COW filesystems (Btrfs, XFS): may create reflinks (no data copy at all)

```c
#include <unistd.h>
loff_t off_in = 0, off_out = 0;
copy_file_range(fd_in, &off_in, fd_out, &off_out, len, 0);
```

Available since Linux 4.5.

---

## Shared Memory: Zero-Copy Between Processes

The most fundamental form of zero-copy IPC: multiple processes map the same physical memory.

```c
/* Process A: create and write */
int shm_fd = shm_open("/my_shm", O_CREAT | O_RDWR, 0666);
ftruncate(shm_fd, SHM_SIZE);
void *ptr = mmap(NULL, SHM_SIZE, PROT_READ | PROT_WRITE,
                 MAP_SHARED, shm_fd, 0);
memcpy(ptr, data, len);

/* Process B: open and read — same physical pages, no copy */
int shm_fd = shm_open("/my_shm", O_RDONLY, 0);
void *ptr = mmap(NULL, SHM_SIZE, PROT_READ, MAP_SHARED, shm_fd, 0);
```

---

## memfd_create(): Anonymous Shared Memory

1. Creates anonymous file descriptors backed by memory
1. Can be passed to other processes via Unix domain socket `SCM_RIGHTS`
1. Ideal for zero-copy IPC without filesystem visibility

```c
int memfd = memfd_create("shared_buf", MFD_CLOEXEC);
ftruncate(memfd, BUF_SIZE);
void *buf = mmap(NULL, BUF_SIZE, PROT_READ | PROT_WRITE,
                 MAP_SHARED, memfd, 0);
/* Send fd to another process via SCM_RIGHTS */
send_fd_over_unix_socket(unix_sock, memfd);
```

With `MFD_ALLOW_SEALING` the creator can enforce immutability on the buffer.

---

## XDP: eXpress Data Path

1. Programmable hook at the **lowest point** in the Linux network stack
1. eBPF programs run before `sk_buff` allocation
1. Can drop, redirect, or modify packets before any kernel processing

```c
SEC("xdp")
int xdp_prog(struct xdp_md *ctx) {
    void *data     = (void *)(long)ctx->data;
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
1. Four shared rings: Fill, Completion, RX, TX
1. Keeps kernel network stack available (unlike DPDK)
1. NIC must support XDP zero-copy driver mode

---

## DPDK: Data Plane Development Kit

1. User-space networking framework that bypasses the kernel entirely
1. NIC memory-mapped directly to user-space via huge pages + IOMMU
1. Polling model instead of interrupts
1. Dedicates CPU cores to polling; no kernel stack features
1. Requires Poll Mode Drivers (PMDs) for supported NICs

---

## DMA-BUF: Zero-Copy Between Devices

1. Kernel framework for sharing buffers between hardware devices
1. Originally for GPU; now used broadly (cameras, video encoders, displays)
1. Exported via file descriptors, shareable between processes
1. Example pipeline: Camera DMA → shared buffer → GPU process → display controller, all without copying
1. Used by V4L2 (video), DRM/KMS (display), and GPU drivers

---

## RDMA: Remote Direct Memory Access

1. Network transfer that bypasses both kernels and the remote CPU
1. Source NIC reads from source memory, writes directly to destination memory
1. True zero-copy across the network

Key technologies:

1. **InfiniBand** — dedicated RDMA fabric
1. **RoCE** — RDMA over Converged Ethernet
1. **iWARP** — RDMA over TCP/IP

Programming: `libibverbs` — register memory regions, create queue pairs, post send/receive work requests, completion via completion queues.

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
