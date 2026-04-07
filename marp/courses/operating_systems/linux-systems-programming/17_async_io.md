# Asynchronous I/O in Linux

---

## What is Asynchronous I/O?

1. **Non-blocking operations** - Initiate I/O and continue working
1. **Completion notification** - Get notified when operation completes
1. **No waiting** - Thread doesn't block on I/O operations
1. **Overlap computation** - CPU work while I/O in progress
1. **High concurrency** - Handle thousands of operations

---

## Synchronous vs Asynchronous

![synchronous_vs_asynchronous](/svg/courses/operating_systems/linux-systems-programming/17_async_io/synchronous_vs_asynchronous.svg)

---

## Benefits of Async I/O

1. **Better resource utilization** - CPU works while I/O pending
1. **Higher throughput** - Multiple operations in flight
1. **Lower latency** - No blocking delays
1. **Scalability** - Handle more concurrent clients
1. **Responsive applications** - UI doesn't freeze

---

## Linux Async I/O APIs

1. **POSIX AIO** - `aio_*` functions
1. **Linux Native AIO** - `io_submit/io_getevents`
1. **io_uring** - Modern unified interface
1. **epoll + non-blocking** - Event-driven simulation
1. **Signal-driven I/O** - SIGIO notifications

---

## POSIX AIO Overview

```c
#include <aio.h>

struct aiocb cb;
cb.aio_fildes = fd;
cb.aio_buf = buffer;
cb.aio_nbytes = sizeof(buffer);
cb.aio_offset = 0;
cb.aio_sigevent.sigev_notify = SIGEV_NONE;

// Initiate async read
if (aio_read(&cb) == -1) {
    perror("aio_read");
}
```

1. **Control block** - `struct aiocb` describes operation
1. **Standard API** - POSIX portable
1. **Multiple backends** - Implementation varies

---

## POSIX AIO: Checking Completion

```c
// Poll for completion
while (1) {
    int status = aio_error(&cb);
    if (status == 0) {
        // Operation completed successfully
        ssize_t bytes = aio_return(&cb);
        printf("Read %zd bytes\n", bytes);
        break;
    } else if (status == EINPROGRESS) {
        // Still in progress, do other work
        usleep(1000);
    } else {
        // Error occurred
        perror("aio_error");
        break;
    }
}
```

---

## POSIX AIO: Blocking Wait

```c
// Block until completion
const struct aiocb *list[] = {&cb};
int ret = aio_suspend(list, 1, NULL);
if (ret == 0) {
    ssize_t bytes = aio_return(&cb);
    printf("Operation completed: %zd bytes\n", bytes);
} else {
    perror("aio_suspend");
}
```

1. **aio_suspend()** - Block until one operation completes
1. **Multiple operations** - Wait for any in a list
1. **Timeout support** - Optional timeout parameter

---

## POSIX AIO: Signal Notification

```c
// Setup signal handler
signal(SIGUSR1, aio_completion_handler);

// Configure for signal notification
cb.aio_sigevent.sigev_notify = SIGEV_SIGNAL;
cb.aio_sigevent.sigev_signo = SIGUSR1;
cb.aio_sigevent.sigev_value.sival_ptr = &cb;

void aio_completion_handler(int sig) {
    // Handle completion in signal context
    // Be careful - limited functions allowed here
}
```

1. **Signal delivery** - Async notification
1. **Signal safety** - Limited functions in handler
1. **Context information** - Pass data via `sigev_value`

---

## POSIX AIO: Thread Notification

```c
void *completion_thread(void *arg) {
    struct aiocb *cb = (struct aiocb *)arg;
    ssize_t bytes = aio_return(cb);
    printf("Async operation completed: %zd bytes\n", bytes);
    return NULL;
}

// Configure for thread notification
cb.aio_sigevent.sigev_notify = SIGEV_THREAD;
cb.aio_sigevent.sigev_notify_function = completion_thread;
cb.aio_sigevent.sigev_notify_attributes = NULL;
cb.aio_sigevent.sigev_value.sival_ptr = &cb;
```

---

## POSIX AIO: Multiple Operations

```c
#define NUM_OPS 10
struct aiocb cbs[NUM_OPS];
const struct aiocb *list[NUM_OPS];

// Initialize multiple operations
for (int i = 0; i < NUM_OPS; i++) {
    cbs[i].aio_fildes = fd;
    cbs[i].aio_buf = buffers[i];
    cbs[i].aio_nbytes = BUFFER_SIZE;
    cbs[i].aio_offset = i * BUFFER_SIZE;
    list[i] = &cbs[i];

    aio_read(&cbs[i]);
}

// Wait for all to complete
aio_suspend(list, NUM_OPS, NULL);
```

---

## POSIX AIO: Write Operations

```c
struct aiocb write_cb;
write_cb.aio_fildes = fd;
write_cb.aio_buf = data;
write_cb.aio_nbytes = strlen(data);
write_cb.aio_offset = 0;

// Async write
if (aio_write(&write_cb) == -1) {
    perror("aio_write");
}

// Wait for write completion
aio_suspend((const struct aiocb*[]){&write_cb}, 1, NULL);
ssize_t written = aio_return(&write_cb);
```

---

## POSIX AIO: Synchronization

```c
// Force all pending writes to storage
aio_fsync(O_SYNC, &write_cb);

// Cancel pending operation
if (aio_cancel(fd, &cb) == AIO_CANCELED) {
    printf("Operation canceled\n");
}

// List all operations for a file descriptor
struct aiocb *list[] = {&cb1, &cb2, &cb3};
aio_suspend(list, 3, NULL);
```

1. **aio_fsync()** - Async sync to storage
1. **aio_cancel()** - Cancel pending operations
1. **Batch operations** - Handle multiple requests

---

## Linux Native AIO

```c
#include <linux/aio_abi.h>
#include <sys/syscall.h>

// Create AIO context
aio_context_t ctx = 0;
long ret = syscall(SYS_io_setup, 128, &ctx);

// Prepare I/O control block
struct iocb cb;
io_prep_pread(&cb, fd, buffer, size, offset);

// Submit operation
struct iocb *list[] = {&cb};
ret = syscall(SYS_io_submit, ctx, 1, list);
```

1. **Direct syscalls** - No glibc wrapper
1. **High performance** - Kernel implementation
1. **Batch submission** - Multiple operations at once

---

## Native AIO: Event Retrieval

```c
// Wait for completion events
struct io_event events[10];
struct timespec timeout = {1, 0}; // 1 second

long num_events = syscall(SYS_io_getevents, ctx, 1, 10,
                         events, &timeout);

for (int i = 0; i < num_events; i++) {
    struct iocb *cb = (struct iocb*)events[i].obj;
    long result = events[i].res;

    if (result > 0) {
        printf("Operation completed: %ld bytes\n", result);
    } else {
        printf("Operation failed: %s\n", strerror(-result));
    }
}
```

---

## Native AIO: Cleanup

```c
// Cancel all pending operations
ret = syscall(SYS_io_cancel, ctx, &cb, &event);

// Destroy AIO context
ret = syscall(SYS_io_destroy, ctx);
if (ret != 0) {
    perror("io_destroy");
}
```

1. **Resource management** - Clean up contexts
1. **Cancellation** - Stop pending operations
1. **Error handling** - Check return values

---

## io_uring: Modern Async I/O

```c
#include <liburing.h>

struct io_uring ring;
io_uring_queue_init(32, &ring, 0);

// Get submission queue entry
struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
io_uring_prep_read(sqe, fd, buffer, sizeof(buffer), 0);

// Submit the operation
io_uring_submit(&ring);
```

1. **Unified interface** - All I/O operations
1. **High performance** - Shared memory rings
1. **Modern design** - Lessons from previous APIs

---

## io_uring: Completion Handling

```c
// Wait for completion
struct io_uring_cqe *cqe;
int ret = io_uring_wait_cqe(&ring, &cqe);
if (ret < 0) {
    perror("io_uring_wait_cqe");
}

// Process result
if (cqe->res < 0) {
    printf("I/O error: %s\n", strerror(-cqe->res));
} else {
    printf("Read %d bytes\n", cqe->res);
}

// Mark completion as seen
io_uring_cqe_seen(&ring, cqe);
```

---

## io_uring: Ring Structure

![iouring_ring_structure](/svg/courses/operating_systems/linux-systems-programming/17_async_io/iouring_ring_structure.svg)

---

## io_uring: Multiple Operations

```c
// Submit multiple operations
for (int i = 0; i < 10; i++) {
    struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
    io_uring_prep_read(sqe, fd, buffers[i], BUFFER_SIZE,
                       i * BUFFER_SIZE);
    sqe->user_data = i; // Associate data with request
}

io_uring_submit(&ring);

// Process completions
for (int i = 0; i < 10; i++) {
    struct io_uring_cqe *cqe;
    io_uring_wait_cqe(&ring, &cqe);

    printf("Operation %llu completed\n", cqe->user_data);
    io_uring_cqe_seen(&ring, &cqe);
}
```

---

## io_uring: Advanced Features

```c
// Chain operations - read then write
struct io_uring_sqe *sqe1 = io_uring_get_sqe(&ring);
io_uring_prep_read(sqe1, fd_in, buffer, size, 0);
sqe1->flags |= IOSQE_IO_LINK;

struct io_uring_sqe *sqe2 = io_uring_get_sqe(&ring);
io_uring_prep_write(sqe2, fd_out, buffer, size, 0);

// Fixed file descriptors for performance
int fds[] = {fd1, fd2, fd3};
io_uring_register_files(&ring, fds, 3);
```

1. **Operation chaining** - Link dependent operations
1. **Fixed resources** - Pre-register files/buffers
1. **Zero-copy** - Direct kernel access

---

## Async I/O with epoll

```c
// Make socket non-blocking
int flags = fcntl(sockfd, F_GETFL, 0);
fcntl(sockfd, F_SETFL, flags | O_NONBLOCK);

// Add to epoll
int epfd = epoll_create1(0);
struct epoll_event event;
event.events = EPOLLIN | EPOLLET; // Edge-triggered
event.data.fd = sockfd;
epoll_ctl(epfd, EPOLL_CTL_ADD, sockfd, &event);

// Event loop
while (1) {
    int nfds = epoll_wait(epfd, events, MAX_EVENTS, -1);
    for (int i = 0; i < nfds; i++) {
        handle_io_event(&events[i]);
    }
}
```

---

## Signal-Driven I/O

```c
// Setup signal handler
signal(SIGIO, sigio_handler);

// Enable signal-driven I/O
fcntl(fd, F_SETOWN, getpid());
int flags = fcntl(fd, F_GETFL);
fcntl(fd, F_SETFL, flags | O_ASYNC);

void sigio_handler(int sig) {
    // I/O is ready
    char buffer[1024];
    ssize_t bytes = read(fd, buffer, sizeof(buffer));
    if (bytes > 0) {
        process_data(buffer, bytes);
    }
}
```

1. **SIGIO signal** - Delivered when I/O ready
1. **Limited portability** - Not widely supported
1. **Signal overhead** - Context switching costs

---

## Performance Comparison

![performance_comparison](/svg/courses/operating_systems/linux-systems-programming/17_async_io/performance_comparison.svg)

---

## Async I/O Patterns

1. **Reactor pattern** - Event-driven dispatch
1. **Proactor pattern** - Completion-based dispatch
1. **Half-sync/Half-async** - Hybrid approach
1. **Leader-follower** - Thread pool coordination
1. **Pipeline processing** - Staged operations

---

## Reactor Pattern

```c
// Reactor event loop
while (running) {
    int events = epoll_wait(epfd, event_list, MAX_EVENTS, timeout);

    for (int i = 0; i < events; i++) {
        if (event_list[i].events & EPOLLIN) {
            handle_read(event_list[i].data.fd);
        }
        if (event_list[i].events & EPOLLOUT) {
            handle_write(event_list[i].data.fd);
        }
    }
}
```

1. **Event demultiplexing** - Single thread handles events
1. **Non-blocking I/O** - Operations don't block
1. **State machines** - Track connection states

---

## Proactor Pattern

```c
// Proactor with io_uring
void completion_handler(struct io_uring_cqe *cqe) {
    Operation *op = (Operation*)cqe->user_data;

    if (cqe->res > 0) {
        op->bytes_completed = cqe->res;
        op->completion_callback(op);
    } else {
        handle_error(op, cqe->res);
    }
}

// Main event loop
while (running) {
    struct io_uring_cqe *cqe;
    io_uring_wait_cqe(&ring, &cqe);
    completion_handler(cqe);
    io_uring_cqe_seen(&ring, cqe);
}
```

---

## Error Handling in Async I/O

```c
// Check for errors in POSIX AIO
int error = aio_error(&cb);
if (error != 0) {
    if (error == EINPROGRESS) {
        // Still in progress
    } else {
        printf("AIO error: %s\n", strerror(error));
    }
}

// io_uring error handling
if (cqe->res < 0) {
    printf("io_uring error: %s\n", strerror(-cqe->res));
} else if (cqe->res == 0) {
    // EOF or empty read
}
```

1. **Error codes** - Negative values indicate errors
1. **Partial operations** - Handle incomplete I/O
1. **Resource cleanup** - Free on error

---

## Memory Management

```c
// Aligned buffers for Direct I/O
void *buffer;
posix_memalign(&buffer, 4096, BUFFER_SIZE);

// Register buffers with io_uring
struct iovec iovecs[NUM_BUFFERS];
for (int i = 0; i < NUM_BUFFERS; i++) {
    iovecs[i].iov_base = aligned_buffers[i];
    iovecs[i].iov_len = BUFFER_SIZE;
}
io_uring_register_buffers(&ring, iovecs, NUM_BUFFERS);

// Use fixed buffer in operation
io_uring_prep_read_fixed(sqe, fd, NULL, size, offset, 0);
```

---

## Batch Operations

```c
// Batch multiple operations for efficiency
#define BATCH_SIZE 32
struct io_uring_sqe *sqes[BATCH_SIZE];

// Prepare batch
for (int i = 0; i < BATCH_SIZE; i++) {
    sqes[i] = io_uring_get_sqe(&ring);
    io_uring_prep_read(sqes[i], fd, buffers[i], size, offset);
}

// Submit entire batch
io_uring_submit(&ring);

// Process completions in batch
struct io_uring_cqe *cqes[BATCH_SIZE];
int completed = io_uring_peek_batch_cqe(&ring, cqes, BATCH_SIZE);
```

---

## Async Network I/O

```c
// Async accept with io_uring
struct sockaddr_in client_addr;
socklen_t addr_len = sizeof(client_addr);

struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
io_uring_prep_accept(sqe, server_fd,
                     (struct sockaddr*)&client_addr,
                     &addr_len, 0);
sqe->user_data = ACCEPT_TOKEN;

// Async send/receive
io_uring_prep_send(sqe, client_fd, buffer, len, 0);
io_uring_prep_recv(sqe, client_fd, buffer, len, 0);
```

---

## File I/O Optimizations

```c
// Direct I/O to bypass page cache
int fd = open("file.dat", O_RDWR | O_DIRECT);

// Vectored I/O operations
struct iovec iov[3];
iov[0].iov_base = buffer1;
iov[0].iov_len = size1;
// ... setup other vectors

struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
io_uring_prep_readv(sqe, fd, iov, 3, offset);

// Async file sync
io_uring_prep_fsync(sqe, fd, IORING_FSYNC_DATASYNC);
```

---

## Monitoring and Profiling

```c
// Track operation latencies
struct timespec start, end;
clock_gettime(CLOCK_MONOTONIC, &start);

// Submit operation
io_uring_submit(&ring);

// Wait for completion
io_uring_wait_cqe(&ring, &cqe);
clock_gettime(CLOCK_MONOTONIC, &end);

long latency_ns = (end.tv_sec - start.tv_sec) * 1000000000L +
                  (end.tv_nsec - start.tv_nsec);
printf("Operation latency: %ld ns\n", latency_ns);
```

---

## Common Pitfalls

1. **Buffer lifetime** - Keep buffers valid until completion
1. **File descriptor validity** - Don't close before completion
1. **Error handling** - Always check return values
1. **Resource limits** - Watch memory and fd limits
1. **Completion ordering** - Operations may complete out of order

---

## Threading Considerations

```c
// Thread-safe completion handling
pthread_mutex_t completion_mutex = PTHREAD_MUTEX_INITIALIZER;

void handle_completion(struct io_uring_cqe *cqe) {
    pthread_mutex_lock(&completion_mutex);

    // Process completion safely
    Operation *op = (Operation*)cqe->user_data;
    op->completed = true;
    op->result = cqe->res;

    pthread_mutex_unlock(&completion_mutex);

    // Wake up waiting threads
    pthread_cond_signal(&op->completion_cond);
}
```

---

## Load Balancing

```c
// Distribute work across multiple io_uring instances
struct io_uring rings[NUM_THREADS];
atomic_int ring_index = 0;

int get_next_ring() {
    return atomic_fetch_add(&ring_index, 1) % NUM_THREADS;
}

// Submit to least loaded ring
int target_ring = get_next_ring();
struct io_uring_sqe *sqe = io_uring_get_sqe(&rings[target_ring]);
io_uring_prep_read(sqe, fd, buffer, size, offset);
io_uring_submit(&rings[target_ring]);
```

---

## Testing Async I/O

```c
// Simulate slow I/O for testing
void simulate_slow_io() {
    // Create large file for testing
    int fd = open("test_file", O_CREAT | O_RDWR, 0644);
    fallocate(fd, 0, 0, 1024 * 1024 * 1024); // 1GB file

    // Test with multiple concurrent operations
    for (int i = 0; i < 100; i++) {
        submit_async_read(fd, i * 4096, 4096);
    }

    // Measure completion times
    measure_completion_latency();
}
```

---

## Integration with Event Loops

```c
// Integrate io_uring with epoll
int ring_fd = io_uring_ring_fd(&ring);

struct epoll_event ev;
ev.events = EPOLLIN;
ev.data.fd = ring_fd;
epoll_ctl(epfd, EPOLL_CTL_ADD, ring_fd, &ev);

// In main event loop
if (events[i].data.fd == ring_fd) {
    // Handle io_uring completions
    handle_uring_completions(&ring);
}
```

---

## Performance Tuning

1. **Queue depth** - Balance between latency and throughput
1. **Batch submissions** - Reduce syscall overhead
1. **Fixed resources** - Pre-register files and buffers
1. **CPU affinity** - Pin threads to cores
1. **Memory alignment** - Use properly aligned buffers

---

## Real-World Applications

1. **Database systems** - High-performance storage engines
1. **Web servers** - Handle thousands of connections
1. **File servers** - Efficient file transfer protocols
1. **Streaming systems** - Low-latency data processing
1. **CDN services** - Content delivery optimization

---

## Best Practices

1. **Start simple** - Begin with basic patterns
1. **Error handling** - Always check for errors
1. **Resource management** - Clean up properly
1. **Testing** - Verify under load conditions
1. **Monitoring** - Track performance metrics
1. **Documentation** - Document async flow clearly

---

## Future of Async I/O

1. **io_uring evolution** - New features and optimizations
1. **Hardware acceleration** - Storage and network offload
1. **Language support** - Better async/await primitives
1. **Ecosystem growth** - More libraries and frameworks
1. **Standards development** - Cross-platform APIs
