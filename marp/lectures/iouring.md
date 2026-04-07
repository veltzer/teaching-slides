# io_uring: High-Performance I/O Interface for Linux

---

## What is `io_uring`?

1. Modern asynchronous I/O interface for Linux
1. Introduced in Linux kernel 5.1 (2019)
1. Designed to overcome limitations of previous I/O APIs
1. Provides zero-copy, lock-free operation

---

## Why `io_uring` Was Created

1. Traditional I/O APIs had significant limitations
    - `read()`/`write()`: Blocking and synchronous
    - `epoll`: Only for network I/O, not files
    - `aio`: Complex and limited functionality
1. Need for unified, high-performance I/O interface
1. Support for both network and file I/O

---

## Core Design Principles

1. Shared memory rings between kernel and userspace
1. Submission Queue (SQ) and Completion Queue (CQ)
1. Minimal system call overhead
1. Batch operations support

![core_design_principles](/svg/lectures/iouring/core_design_principles.svg)

---

## Ring Buffer Architecture

1. Two ring buffers for communication
    - Submission Queue (SQ): User submits I/O requests
    - Completion Queue (CQ): Kernel returns results
1. Lock-free single producer, single consumer design
1. Memory mapped into user space

---

## Submission Queue Entry (SQE)

```c
struct io_uring_sqe {
    __u8    opcode;     /* Operation type */
    __u8    flags;      /* Request flags */
    __u16   ioprio;     /* I/O priority */
    __s32   fd;         /* File descriptor */
    __u64   off;        /* Offset */
    __u64   addr;       /* Buffer address */
    __u32   len;        /* Buffer length */
    /* ... more fields ... */
};
```

---

## Completion Queue Entry (CQE)

```c
struct io_uring_cqe {
    __u64   user_data;  /* Data from submission */
    __s32   res;        /* Result of operation */
    __u32   flags;      /* Completion flags */
};
```

---

## Basic `io_uring` Workflow

1. Setup ring with `io_uring_setup()`
1. Map rings to user memory with `mmap()`
1. Fill Submission Queue Entries (SQEs)
1. Submit operations with `io_uring_enter()`
1. Reap completions from Completion Queue (CQ)

---

## Setting Up `io_uring`

```c
#include <liburing.h>

struct io_uring ring;
int ret;

/* Initialize ring with 64 entries */
ret = io_uring_queue_init(64, &ring, 0);
if (ret < 0) {
    perror("io_uring_queue_init");
    return -1;
}
```

---

## Submitting a Read Operation

```c
struct io_uring_sqe *sqe;
char buffer[4096];

/* Get submission queue entry */
sqe = io_uring_get_sqe(&ring);

/* Prepare read operation */
io_uring_prep_read(sqe, fd, buffer,
                   sizeof(buffer), 0);

/* Submit the operation */
io_uring_submit(&ring);
```

---

## Reaping Completions

```c
struct io_uring_cqe *cqe;
int ret;

/* Wait for completion */
ret = io_uring_wait_cqe(&ring, &cqe);
if (ret < 0) {
    perror("io_uring_wait_cqe");
    return -1;
}

/* Process result */
if (cqe->res < 0) {
    fprintf(stderr, "Read failed: %s\n",
            strerror(-cqe->res));
}

/* Mark CQE as seen */
io_uring_cqe_seen(&ring, cqe);
```

---

## Supported Operations

1. File I/O: `read`, `write`, `readv`, `writev`
1. Network: `send`, `recv`, `accept`, `connect`
1. Synchronization: `fsync`, `fdatasync`
1. Polling: `poll_add`, `poll_remove`
1. Timeouts: `timeout`, `link_timeout`
1. Many more operations available

---

## Advanced Features: Linked Operations

1. Chain multiple operations together
1. Next operation depends on previous success
1. Use `IOSQE_IO_LINK` flag

```c
/* First operation - read */
sqe = io_uring_get_sqe(&ring);
io_uring_prep_read(sqe, fd, buf1, len1, 0);
sqe->flags |= IOSQE_IO_LINK;

/* Second operation - write (runs if read succeeds) */
sqe = io_uring_get_sqe(&ring);
io_uring_prep_write(sqe, fd2, buf2, len2, 0);
```

---

## Advanced Features: Fixed Files

1. Pre-register file descriptors
1. Avoid per-operation file table lookups
1. Improved performance for frequently used files

```c
int fds[] = {fd1, fd2, fd3};

/* Register file descriptors */
io_uring_register_files(&ring, fds, 3);

/* Use fixed file in operation */
io_uring_prep_read(sqe, 0, buf, len, 0);
sqe->flags |= IOSQE_FIXED_FILE;
```

---

## Advanced Features: Fixed Buffers

1. Pre-register memory buffers
1. Pin pages in memory
1. Eliminate page table lookups

```c
struct iovec iov = {
    .iov_base = buffer,
    .iov_len = buffer_size
};

/* Register buffer */
io_uring_register_buffers(&ring, &iov, 1);

/* Use fixed buffer */
io_uring_prep_read_fixed(sqe, fd, 0,
                         len, 0, 0);
```

---

## Polling Mode (`SQPOLL`)

1. Kernel thread polls submission queue
1. Eliminates `io_uring_enter()` system calls
1. Lower latency for high-frequency operations

```c
struct io_uring_params params = {
    .flags = IORING_SETUP_SQPOLL,
    .sq_thread_idle = 2000  /* milliseconds */
};

io_uring_queue_init_params(64, &ring, &params);
```

---

## `io_uring` vs Traditional I/O

![iouring_vs_traditional_i_o](/mermaid/lectures/iouring/iouring_vs_traditional_i_o.mmd)

---

## Performance Benefits

1. Reduced system call overhead
1. Batch submission and completion
1. Zero-copy operations with fixed buffers
1. Lock-free ring buffer design
1. CPU cache-friendly operation

---

## Real-World Performance Numbers

1. Up to 2x improvement in IOPS
1. Reduced CPU usage by 30-50%
1. Lower latency for small I/O operations
1. Better scaling with multiple cores

![real_world_performance_numbers](/svg/lectures/iouring/real_world_performance_numbers.svg)

---

## Error Handling

```c
struct io_uring_cqe *cqe;

io_uring_wait_cqe(&ring, &cqe);

if (cqe->res < 0) {
    switch (-cqe->res) {
        case EAGAIN:
            /* Resource temporarily unavailable */
            break;
        case EINVAL:
            /* Invalid argument */
            break;
        default:
            /* Other error */
            break;
    }
}
```

---

## Memory Ordering Considerations

1. Ring buffers use memory barriers
1. Proper ordering between producer and consumer
1. `smp_mb()` ensures visibility across CPUs
1. Critical for correctness in multi-core systems

---

## Use Case: Web Server

```c
/* Accept loop with io_uring */
void accept_loop(struct io_uring *ring) {
    struct io_uring_sqe *sqe;

    sqe = io_uring_get_sqe(ring);
    io_uring_prep_accept(sqe, listen_fd,
                         NULL, NULL, 0);
    sqe->user_data = ACCEPT_EVENT;

    io_uring_submit(ring);
}
```

---

## Use Case: Database Engine

1. Asynchronous file I/O for data pages
1. Parallel reads from multiple files
1. Write-ahead logging with `fsync`
1. Reduced latency for queries

---

## Use Case: Video Streaming

1. High-throughput file reading
1. Zero-copy with `splice` operations
1. Network sending with fixed buffers
1. Minimal CPU overhead

---

## Debugging `io_uring` Applications

1. Use `strace` to trace system calls
1. Enable kernel tracing with `trace-cmd`
1. Monitor with `/proc/[pid]/fdinfo/[fd]`
1. Check `dmesg` for kernel messages

```bash
# Trace io_uring system calls
strace -e io_uring_setup,io_uring_enter ./app
```

---

## Common Pitfalls

1. Not checking for kernel support
1. Incorrect memory barrier usage
1. Ring overflow without proper handling
1. Memory leaks with fixed buffers
1. Not marking CQEs as seen

---

## Kernel Version Requirements

1. Basic support: Linux 5.1+
1. Full feature set: Linux 5.6+
1. Latest optimizations: Linux 5.11+
1. Check features with:

```c
struct io_uring_params params = {0};
io_uring_queue_init_params(32, &ring, &params);
/* Check params.features */
```

---

## Library Support

1. **liburing**: Official C library
1. **Rust**: tokio-uring, rio
1. **Go**: golang.org/x/sys/unix
1. **Python**: python-liburing
1. **Node.js**: experimental support

---

## Security Considerations

1. Requires `CAP_SYS_ADMIN` for some features
1. Memory pinning limits (`RLIMIT_MEMLOCK`)
1. Potential for resource exhaustion
1. Proper validation of user data

---

## Best Practices

1. Use liburing for portability
1. Start with simple operations
1. Profile before optimizing
1. Handle ring overflow gracefully
1. Clean up resources properly

---

## Benchmarking `io_uring`

```c
/* Simple benchmark */
struct timespec start, end;
clock_gettime(CLOCK_MONOTONIC, &start);

/* Submit 1000 operations */
for (int i = 0; i < 1000; i++) {
    submit_operation(&ring);
}

/* Wait for all completions */
wait_all_completions(&ring);

clock_gettime(CLOCK_MONOTONIC, &end);
/* Calculate elapsed time */
```

---

## Comparison with `epoll`

![comparison_with_epoll](/mermaid/lectures/iouring/comparison_with_epoll.mmd)

---

## Comparison with POSIX `aio`

1. **io_uring**: Modern, actively developed
    - Full feature set
    - Better performance
    - Simpler API
1. **POSIX aio**: Legacy, limited
    - Complex signal-based API
    - Poor kernel implementation
    - Limited operations

---

## Future Developments

1. Continued performance optimizations
1. New operation types
1. Better integration with kernel subsystems
1. Enhanced debugging tools
1. Wider language support

---

## Migration Strategy

1. Identify I/O bottlenecks in application
1. Start with simple read/write operations
1. Gradually adopt advanced features
1. Measure performance improvements
1. Consider fallback for older kernels

---

## Example: Echo Server

```c
void echo_server(struct io_uring *ring) {
    struct io_uring_sqe *sqe;
    struct io_uring_cqe *cqe;

    /* Submit read */
    sqe = io_uring_get_sqe(ring);
    io_uring_prep_recv(sqe, client_fd,
                       buf, BUF_SIZE, 0);
    io_uring_submit(ring);

    /* Wait and echo back */
    io_uring_wait_cqe(ring, &cqe);
    if (cqe->res > 0) {
        /* Echo data back */
        send(client_fd, buf, cqe->res, 0);
    }
}
```

---

## Performance Tuning Tips

1. Use appropriate ring size
1. Enable `SQPOLL` for low latency
1. Register frequently used files
1. Use fixed buffers for hot paths
1. Batch operations when possible

---

## Monitoring and Metrics

1. Track submission rate
1. Monitor completion latency
1. Check ring utilization
1. Measure system call frequency
1. Profile CPU usage

---

## Conclusion

1. `io_uring` revolutionizes Linux I/O
1. Significant performance improvements
1. Unified interface for all I/O types
1. Active development and growing adoption
1. Future of high-performance Linux applications
