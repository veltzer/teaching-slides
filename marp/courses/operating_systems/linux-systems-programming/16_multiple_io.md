# Multiple I/O APIs in Linux System Programming

---

## Overview

1. **Blocking I/O** - Traditional synchronous operations
1. **Non-blocking I/O** - Immediate return with status
1. **I/O Multiplexing** - Monitor multiple file descriptors
1. **Asynchronous I/O** - True async with callbacks
1. **Modern async patterns** - `io_uring` and beyond

---

## Blocking I/O

```c
int fd = open("file.txt", O_RDONLY);
char buffer[1024];
ssize_t bytes = read(fd, buffer, sizeof(buffer));
// Program blocks until data is available
```

1. **Simple model** - One operation at a time
1. **Predictable** - Easy to reason about
1. **Limited scalability** - One thread per connection

---

## Non-blocking I/O

```c
int fd = open("file.txt", O_RDONLY | O_NONBLOCK);
char buffer[1024];
ssize_t bytes = read(fd, buffer, sizeof(buffer));
if (bytes == -1 && errno == EAGAIN) {
    // Would block, try again later
}
```

1. **Immediate return** - Never blocks the caller
1. **Polling required** - Must check repeatedly
1. **CPU intensive** - Busy waiting

---

## I/O Multiplexing: `select()`

```c
fd_set readfds;
FD_ZERO(&readfds);
FD_SET(fd1, &readfds);
FD_SET(fd2, &readfds);

int ready = select(maxfd + 1, &readfds, NULL, NULL, &timeout);
if (FD_ISSET(fd1, &readfds)) {
    // fd1 is ready for reading
}
```

1. **Monitor multiple FDs** - Single thread handles many
1. **Limited to 1024 FDs** - Implementation constraint
1. **O(n) complexity** - Scans all file descriptors

---

## I/O Multiplexing: `poll()`

```c
struct pollfd fds[2];
fds[0].fd = fd1;
fds[0].events = POLLIN;
fds[1].fd = fd2;
fds[1].events = POLLIN;

int ready = poll(fds, 2, timeout);
for (int i = 0; i < 2; i++) {
    if (fds[i].revents & POLLIN) {
        // fds[i].fd is ready
    }
}
```

1. **No FD limit** - Can handle thousands
1. **Better interface** - Array-based approach
1. **Still O(n)** - Linear scan of descriptors

---

## I/O Multiplexing: `epoll()`

```c
int epfd = epoll_create1(0);
struct epoll_event event;
event.events = EPOLLIN;
event.data.fd = fd1;
epoll_ctl(epfd, EPOLL_CTL_ADD, fd1, &event);

struct epoll_event events[10];
int ready = epoll_wait(epfd, events, 10, timeout);
```

1. **Linux-specific** - High performance
1. **O(1) complexity** - Only ready FDs returned
1. **Edge/Level triggered** - Flexible notification modes

---

## Edge vs Level Triggered

![edge_vs_level_triggered](/svg/courses/operating_systems/linux-systems-programming/16_multiple_io/edge_vs_level_triggered.svg)

1. **Level** - Notify while condition is true
1. **Edge** - Notify when condition changes
1. **Performance** - Edge triggered is more efficient

---

## Asynchronous I/O: `aio_*`

```c
struct aiocb cb;
cb.aio_fildes = fd;
cb.aio_buf = buffer;
cb.aio_nbytes = sizeof(buffer);
cb.aio_offset = 0;

aio_read(&cb);
// Continue other work
while (aio_error(&cb) == EINPROGRESS) {
    // Still in progress
}
ssize_t bytes = aio_return(&cb);
```

1. **True async** - No blocking at all
1. **Complex API** - More setup required
1. **Limited adoption** - Performance issues historically

---

## Modern Async: `io_uring`

```c
struct io_uring ring;
io_uring_queue_init(32, &ring, 0);

struct io_uring_sqe *sqe = io_uring_get_sqe(&ring);
io_uring_prep_read(sqe, fd, buffer, sizeof(buffer), 0);
io_uring_submit(&ring);

struct io_uring_cqe *cqe;
io_uring_wait_cqe(&ring, &cqe);
```

1. **High performance** - Shared memory rings
1. **Flexible** - Supports many operations
1. **Modern design** - Linux 5.1+

---

## I/O Model Comparison

![i_o_model_comparison](/svg/courses/operating_systems/linux-systems-programming/16_multiple_io/i_o_model_comparison.svg)

---

## Server Architecture Patterns

1. **Thread per connection** - Blocking I/O model
1. **Thread pool** - Limited number of worker threads
1. **Event loop** - Single thread with multiplexing
1. **Actor model** - Message passing between actors
1. **Async/await** - Cooperative multitasking

---

## Event Loop Pattern

```c
while (running) {
    int ready = epoll_wait(epfd, events, MAX_EVENTS, timeout);
    for (int i = 0; i < ready; i++) {
        if (events[i].events & EPOLLIN) {
            handle_read(events[i].data.fd);
        }
        if (events[i].events & EPOLLOUT) {
            handle_write(events[i].data.fd);
        }
    }
}
```

1. **Single thread** - No synchronization needed
1. **Non-blocking handlers** - Quick processing only
1. **State machines** - Track connection state

---

## C10K Problem

1. **Challenge** - 10,000 concurrent connections
1. **Thread limits** - Memory and context switching
1. **File descriptor limits** - `ulimit` constraints
1. **Solutions** - Event-driven architectures
1. **Modern** - C10M (10 million) is now the target

---

## Choosing the Right API

![choosing_the_right_api](/svg/courses/operating_systems/linux-systems-programming/16_multiple_io/choosing_the_right_api.svg)

---

## Performance Considerations

1. **Memory usage** - Per-connection overhead
1. **Context switching** - Thread model costs
1. **System call overhead** - Minimize kernel transitions
1. **Cache locality** - Data structure layout
1. **Lock contention** - Shared resource access

---

## Error Handling Patterns

```c
// Check for EINTR (interrupted system call)
do {
    ready = epoll_wait(epfd, events, MAX_EVENTS, timeout);
} while (ready == -1 && errno == EINTR);

// Handle partial reads/writes
while (total_sent < message_len) {
    ssize_t sent = send(fd, buffer + total_sent,
                       message_len - total_sent, 0);
    if (sent == -1) break;
    total_sent += sent;
}
```

1. **Interrupted calls** - Handle `EINTR` properly
1. **Partial operations** - Read/write may be incomplete
1. **Resource exhaustion** - Handle `EAGAIN`/`EWOULDBLOCK`

---

## Best Practices

1. **Buffer management** - Avoid unnecessary copies
1. **Connection pooling** - Reuse connections
1. **Graceful degradation** - Handle overload situations
1. **Monitoring** - Track performance metrics
1. **Testing** - Load testing under realistic conditions
