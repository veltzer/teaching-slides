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
# I/O Multiplexing in Linux

---

## What is I/O Multiplexing?

1. **Single thread** - Monitor multiple file descriptors
1. **Event notification** - Get notified when I/O is ready
1. **Non-blocking I/O** - Avoid blocking on any single operation
1. **Scalability** - Handle thousands of connections
1. **Efficiency** - Better resource utilization than threading

---

## The Problem to Solve

![the_problem_to_solve](svg/courses/operating_systems/linux-systems-programming/18_multiplexing/the_problem_to_solve.svg)

---

## Multiplexing Solution

![multiplexing_solution](svg/courses/operating_systems/linux-systems-programming/18_multiplexing/multiplexing_solution.svg)

---

## Linux Multiplexing APIs

1. **select()** - POSIX standard, portable
1. **poll()** - Better interface, no FD limit
1. **epoll()** - Linux-specific, high performance
1. **io_uring** - Modern unified interface
1. **kqueue** - FreeBSD equivalent (for comparison)

---

## select() System Call

```c
#include <sys/select.h>

fd_set readfds, writefds, exceptfds;
struct timeval timeout;

FD_ZERO(&readfds);
FD_SET(fd1, &readfds);
FD_SET(fd2, &readfds);

timeout.tv_sec = 1;
timeout.tv_usec = 0;

int ready = select(maxfd + 1, &readfds, &writefds,
                   &exceptfds, &timeout);
```

1. **Three sets** - Read, write, exception events
1. **Timeout support** - Block with timeout
1. **Return value** - Number of ready descriptors

---

## select() Event Processing

```c
if (ready > 0) {
    if (FD_ISSET(fd1, &readfds)) {
        // fd1 is ready for reading
        ssize_t bytes = read(fd1, buffer, sizeof(buffer));
        if (bytes > 0) {
            process_data(buffer, bytes);
        } else if (bytes == 0) {
            // EOF - connection closed
            close(fd1);
        }
    }

    if (FD_ISSET(fd2, &readfds)) {
        // fd2 is ready for reading
        handle_fd2();
    }
}
```

---

## select() Limitations

1. **FD_SETSIZE limit** - Typically 1024 file descriptors
1. **O(n) complexity** - Scans all descriptors
1. **FD set modification** - Must rebuild sets each call
1. **No event data** - Only knows FD is ready
1. **Portability issues** - Different behavior across systems

---

## select() Server Example

```c
int server_fd = socket(AF_INET, SOCK_STREAM, 0);
bind(server_fd, &addr, sizeof(addr));
listen(server_fd, 10);

fd_set master_set, read_set;
FD_ZERO(&master_set);
FD_SET(server_fd, &master_set);
int max_fd = server_fd;

while (1) {
    read_set = master_set;
    int activity = select(max_fd + 1, &read_set, NULL, NULL, NULL);

    for (int fd = 0; fd <= max_fd; fd++) {
        if (FD_ISSET(fd, &read_set)) {
            if (fd == server_fd) {
                handle_new_connection();
            } else {
                handle_client_data(fd);
            }
        }
    }
}
```

---

## poll() System Call

```c
#include <poll.h>

struct pollfd fds[MAX_FDS];
int nfds = 0;

// Setup file descriptors
fds[0].fd = server_fd;
fds[0].events = POLLIN;
fds[1].fd = client_fd;
fds[1].events = POLLIN | POLLOUT;

int ready = poll(fds, nfds, timeout_ms);
```

1. **Array-based** - No arbitrary FD limit
1. **Event flags** - More descriptive than select
1. **Simpler interface** - No bit manipulation
1. **Per-FD events** - Different events per descriptor

---

## poll() Event Flags

```c
// Input events (events field)
POLLIN      // Data available for reading
POLLOUT     // Ready for writing
POLLPRI     // Urgent data (out-of-band)

// Output events (revents field)
POLLERR     // Error condition
POLLHUP     // Hang up occurred
POLLNVAL    // Invalid file descriptor

// Usage example
if (fds[i].revents & POLLIN) {
    // Ready for reading
}
if (fds[i].revents & (POLLERR | POLLHUP)) {
    // Error or hangup
    close_connection(fds[i].fd);
}
```

---

## poll() Server Example

```c
struct pollfd fds[MAX_CONNECTIONS];
int nfds = 1;

fds[0].fd = server_fd;
fds[0].events = POLLIN;

while (1) {
    int ready = poll(fds, nfds, -1); // Block indefinitely

    for (int i = 0; i < nfds; i++) {
        if (fds[i].revents & POLLIN) {
            if (fds[i].fd == server_fd) {
                // New connection
                int client_fd = accept(server_fd, NULL, NULL);
                fds[nfds].fd = client_fd;
                fds[nfds].events = POLLIN;
                nfds++;
            } else {
                // Client data
                handle_client(fds[i].fd);
            }
        }
    }
}
```

---

## poll() vs select()

![poll_vs_select](svg/courses/operating_systems/linux-systems-programming/18_multiplexing/poll_vs_select.svg)

---

## epoll() Overview

```c
#include <sys/epoll.h>

// Create epoll instance
int epfd = epoll_create1(0);

// Add file descriptor to epoll
struct epoll_event event;
event.events = EPOLLIN;
event.data.fd = fd;
epoll_ctl(epfd, EPOLL_CTL_ADD, fd, &event);

// Wait for events
struct epoll_event events[MAX_EVENTS];
int nfds = epoll_wait(epfd, events, MAX_EVENTS, timeout);
```

1. **Linux-specific** - High performance implementation
1. **O(1) complexity** - Only returns ready descriptors
1. **Edge/Level triggered** - Flexible notification modes
1. **Scalable** - Handles millions of connections

---

## epoll() Control Operations

```c
// Add file descriptor
epoll_ctl(epfd, EPOLL_CTL_ADD, fd, &event);

// Modify existing descriptor
event.events = EPOLLIN | EPOLLOUT;
epoll_ctl(epfd, EPOLL_CTL_MOD, fd, &event);

// Remove file descriptor
epoll_ctl(epfd, EPOLL_CTL_DEL, fd, NULL);

// Event flags
EPOLLIN     // Ready for reading
EPOLLOUT    // Ready for writing
EPOLLET     // Edge-triggered mode
EPOLLONESHOT // One-shot mode
EPOLLRDHUP  // Peer closed connection
```

---

## Level vs Edge Triggered

![level_vs_edge_triggered](svg/courses/operating_systems/linux-systems-programming/18_multiplexing/level_vs_edge_triggered.svg)

---

## epoll() Edge-Triggered Example

```c
// Setup edge-triggered mode
event.events = EPOLLIN | EPOLLET;
event.data.fd = fd;
epoll_ctl(epfd, EPOLL_CTL_ADD, fd, &event);

// Must read all available data
void handle_edge_triggered(int fd) {
    char buffer[4096];
    ssize_t bytes;

    while ((bytes = read(fd, buffer, sizeof(buffer))) > 0) {
        process_data(buffer, bytes);
    }

    if (bytes == -1 && errno != EAGAIN) {
        perror("read");
    }
}
```

1. **Complete consumption** - Must read all available data
1. **Non-blocking I/O** - Required for edge-triggered
1. **Higher performance** - Fewer system calls

---

## epoll() Server Example

```c
int epfd = epoll_create1(0);
struct epoll_event event, events[MAX_EVENTS];

// Add server socket
event.events = EPOLLIN;
event.data.fd = server_fd;
epoll_ctl(epfd, EPOLL_CTL_ADD, server_fd, &event);

while (1) {
    int nfds = epoll_wait(epfd, events, MAX_EVENTS, -1);

    for (int i = 0; i < nfds; i++) {
        if (events[i].data.fd == server_fd) {
            // Accept new connection
            int client_fd = accept(server_fd, NULL, NULL);
            set_nonblocking(client_fd);

            event.events = EPOLLIN | EPOLLET;
            event.data.fd = client_fd;
            epoll_ctl(epfd, EPOLL_CTL_ADD, client_fd, &event);
        } else {
            handle_client(events[i].data.fd, events[i].events);
        }
    }
}
```

---

## epoll() with User Data

```c
struct connection {
    int fd;
    char *buffer;
    size_t buffer_size;
    size_t bytes_read;
    enum state { READING, WRITING } state;
};

// Associate custom data with events
struct connection *conn = malloc(sizeof(struct connection));
conn->fd = client_fd;
conn->state = READING;

event.events = EPOLLIN;
event.data.ptr = conn;  // Store pointer to connection
epoll_ctl(epfd, EPOLL_CTL_ADD, client_fd, &event);

// In event loop
struct connection *conn = events[i].data.ptr;
handle_connection_event(conn, events[i].events);
```

---

## Making Sockets Non-blocking

```c
int set_nonblocking(int fd) {
    int flags = fcntl(fd, F_GETFL, 0);
    if (flags == -1) {
        perror("fcntl F_GETFL");
        return -1;
    }

    if (fcntl(fd, F_SETFL, flags | O_NONBLOCK) == -1) {
        perror("fcntl F_SETFL");
        return -1;
    }

    return 0;
}

// Alternative method
int enable = 1;
ioctl(fd, FIONBIO, &enable);
```

---

## Handling EAGAIN/EWOULDBLOCK

```c
ssize_t safe_read(int fd, void *buffer, size_t size) {
    ssize_t bytes;

    do {
        bytes = read(fd, buffer, size);
    } while (bytes == -1 && errno == EINTR);

    if (bytes == -1) {
        if (errno == EAGAIN || errno == EWOULDBLOCK) {
            // No data available right now
            return 0;
        } else {
            // Real error
            perror("read");
            return -1;
        }
    }

    return bytes;
}
```

---

## Partial Read/Write Handling

```c
typedef struct {
    char *buffer;
    size_t size;
    size_t offset;
} io_buffer_t;

int handle_partial_write(int fd, io_buffer_t *buf) {
    ssize_t written = write(fd, buf->buffer + buf->offset,
                           buf->size - buf->offset);

    if (written > 0) {
        buf->offset += written;
        if (buf->offset == buf->size) {
            // Complete write
            return 1;
        } else {
            // Partial write, continue later
            return 0;
        }
    } else if (written == -1 && errno == EAGAIN) {
        // Would block
        return 0;
    }

    return -1; // Error
}
```

---

## Connection State Machine

![connection_state_machine](svg/courses/operating_systems/linux-systems-programming/18_multiplexing/connection_state_machine.svg)

---

## Event-Driven State Machine

```c
enum conn_state {
    CONN_READING,
    CONN_WRITING,
    CONN_CLOSING
};

void handle_connection(struct connection *conn, uint32_t events) {
    if (events & (EPOLLERR | EPOLLHUP)) {
        close_connection(conn);
        return;
    }

    switch (conn->state) {
        case CONN_READING:
            if (events & EPOLLIN) {
                if (read_data(conn) == 0) {
                    conn->state = CONN_WRITING;
                    modify_epoll_events(conn, EPOLLOUT);
                }
            }
            break;

        case CONN_WRITING:
            if (events & EPOLLOUT) {
                if (write_data(conn) == 0) {
                    conn->state = CONN_READING;
                    modify_epoll_events(conn, EPOLLIN);
                }
            }
            break;
    }
}
```

---

## Performance Comparison

![performance_comparison](svg/courses/operating_systems/linux-systems-programming/18_multiplexing/performance_comparison.svg)

---

## Memory Usage Patterns

```c
// Connection pool to reduce malloc overhead
#define CONN_POOL_SIZE 1000
struct connection conn_pool[CONN_POOL_SIZE];
struct connection *free_connections[CONN_POOL_SIZE];
int free_count = CONN_POOL_SIZE;

struct connection *alloc_connection() {
    if (free_count > 0) {
        return free_connections[--free_count];
    }
    return NULL; // Pool exhausted
}

void free_connection(struct connection *conn) {
    // Reset connection state
    memset(conn, 0, sizeof(*conn));
    free_connections[free_count++] = conn;
}
```

---

## Buffer Management

```c
// Per-connection buffer management
#define BUFFER_SIZE 8192

struct connection {
    int fd;
    char read_buffer[BUFFER_SIZE];
    char write_buffer[BUFFER_SIZE];
    size_t read_pos;
    size_t write_pos;
    size_t write_len;
};

// Circular buffer for high-throughput scenarios
typedef struct {
    char *data;
    size_t size;
    size_t head;
    size_t tail;
    size_t count;
} circular_buffer_t;
```

---

## Timer Integration

```c
// Using timerfd with epoll
int create_timer(int seconds) {
    int timerfd = timerfd_create(CLOCK_MONOTONIC, TFD_CLOEXEC);

    struct itimerspec timer;
    timer.it_value.tv_sec = seconds;
    timer.it_value.tv_nsec = 0;
    timer.it_interval.tv_sec = seconds;
    timer.it_interval.tv_nsec = 0;

    timerfd_settime(timerfd, 0, &timer, NULL);

    // Add to epoll
    struct epoll_event event;
    event.events = EPOLLIN;
    event.data.fd = timerfd;
    epoll_ctl(epfd, EPOLL_CTL_ADD, timerfd, &event);

    return timerfd;
}
```

---

## Signal Integration

```c
// Using signalfd with epoll
int setup_signal_handling() {
    sigset_t mask;
    sigemptyset(&mask);
    sigaddset(&mask, SIGTERM);
    sigaddset(&mask, SIGINT);

    // Block signals for all threads
    pthread_sigmask(SIG_BLOCK, &mask, NULL);

    // Create signalfd
    int sfd = signalfd(-1, &mask, SFD_CLOEXEC);

    struct epoll_event event;
    event.events = EPOLLIN;
    event.data.fd = sfd;
    epoll_ctl(epfd, EPOLL_CTL_ADD, sfd, &event);

    return sfd;
}
```

---

## Multi-threading with epoll

```c
// One epoll per thread
void *worker_thread(void *arg) {
    int thread_id = *(int*)arg;
    int epfd = epoll_create1(0);

    while (running) {
        int nfds = epoll_wait(epfd, events, MAX_EVENTS, 1000);

        for (int i = 0; i < nfds; i++) {
            handle_event(&events[i], thread_id);
        }
    }

    close(epfd);
    return NULL;
}

// Load balancing: distribute connections across threads
int next_thread = 0;
int target_thread = (next_thread++) % num_threads;
move_connection_to_thread(conn, target_thread);
```

---

## Connection Distribution

```c
// Accept connections and distribute to workers
void *acceptor_thread(void *arg) {
    while (running) {
        int client_fd = accept(server_fd, NULL, NULL);
        if (client_fd > 0) {
            set_nonblocking(client_fd);

            // Round-robin distribution
            int worker_id = client_fd % num_workers;
            add_to_worker_epoll(worker_id, client_fd);
        }
    }
    return NULL;
}

// Use eventfd for inter-thread communication
int notify_worker(int worker_id, int client_fd) {
    uint64_t value = client_fd;
    return write(worker_eventfds[worker_id], &value, sizeof(value));
}
```

---

## Error Handling Patterns

```c
void handle_epoll_error(int fd, uint32_t events) {
    if (events & EPOLLERR) {
        int error;
        socklen_t len = sizeof(error);
        getsockopt(fd, SOL_SOCKET, SO_ERROR, &error, &len);
        printf("Socket error on fd %d: %s\n", fd, strerror(error));
    }

    if (events & EPOLLHUP) {
        printf("Hang up on fd %d\n", fd);
    }

    if (events & EPOLLRDHUP) {
        printf("Peer closed connection on fd %d\n", fd);
    }

    // Clean up connection
    epoll_ctl(epfd, EPOLL_CTL_DEL, fd, NULL);
    close(fd);
}
```

---

## Graceful Shutdown

```c
volatile int shutdown_requested = 0;

void handle_shutdown_signal(int sig) {
    shutdown_requested = 1;
}

// Main event loop with graceful shutdown
while (!shutdown_requested) {
    int nfds = epoll_wait(epfd, events, MAX_EVENTS, 1000);

    if (shutdown_requested) {
        // Close all active connections
        close_all_connections();
        break;
    }

    for (int i = 0; i < nfds; i++) {
        handle_event(&events[i]);
    }
}

// Cleanup
close(epfd);
close(server_fd);
```

---

## Protocol Handling

```c
// HTTP request parsing state machine
enum http_state {
    HTTP_REQUEST_LINE,
    HTTP_HEADERS,
    HTTP_BODY,
    HTTP_COMPLETE
};

int parse_http_request(struct connection *conn) {
    switch (conn->http_state) {
        case HTTP_REQUEST_LINE:
            if (parse_request_line(conn)) {
                conn->http_state = HTTP_HEADERS;
            }
            break;

        case HTTP_HEADERS:
            if (parse_headers(conn)) {
                conn->http_state = HTTP_BODY;
            }
            break;

        case HTTP_BODY:
            if (parse_body(conn)) {
                conn->http_state = HTTP_COMPLETE;
                return 1; // Request complete
            }
            break;
    }
    return 0; // Need more data
}
```

---

## Performance Optimization Tips

1. **Use edge-triggered mode** - Fewer epoll_wait calls
1. **Batch operations** - Process multiple events together
1. **Connection pooling** - Reuse connection objects
1. **Buffer management** - Pre-allocate buffers
1. **Avoid memory allocation** - Use stack or pools
1. **CPU affinity** - Pin threads to cores

---

## Monitoring and Debugging

```c
// Connection statistics
struct server_stats {
    atomic_long total_connections;
    atomic_long active_connections;
    atomic_long bytes_read;
    atomic_long bytes_written;
    atomic_long errors;
};

void update_stats(struct connection *conn, int bytes_processed) {
    atomic_fetch_add(&stats.bytes_read, bytes_processed);
}

// Debug connection state
void dump_connection_info(struct connection *conn) {
    printf("Connection fd=%d state=%d read_pos=%zu write_pos=%zu\n",
           conn->fd, conn->state, conn->read_pos, conn->write_pos);
}
```

---

## Testing Multiplexed Servers

```c
// Stress testing with multiple clients
void stress_test(const char *server_addr, int port, int num_clients) {
    for (int i = 0; i < num_clients; i++) {
        int fd = socket(AF_INET, SOCK_STREAM, 0);

        struct sockaddr_in addr;
        addr.sin_family = AF_INET;
        addr.sin_port = htons(port);
        inet_pton(AF_INET, server_addr, &addr.sin_addr);

        if (connect(fd, (struct sockaddr*)&addr, sizeof(addr)) == 0) {
            // Send test data
            send(fd, "Hello Server\n", 13, 0);
        }

        close(fd);
    }
}
```

---

## Common Pitfalls

1. **Forgetting non-blocking** - Must set O_NONBLOCK
1. **Incomplete reads** - Edge-triggered requires full consumption
1. **File descriptor leaks** - Always close on error
1. **Buffer overruns** - Check bounds on all operations
1. **Signal interference** - Use signalfd or block signals
1. **Thundering herd** - Multiple processes on same socket

---

## Real-World Applications

1. **Web servers** - nginx, Apache (event MPM)
1. **Database systems** - PostgreSQL, Redis
1. **Message brokers** - RabbitMQ, Apache Kafka
1. **Reverse proxies** - HAProxy, Envoy
1. **Game servers** - Real-time multiplayer games

---

## Alternative Approaches

1. **Thread pools** - Fixed number of worker threads
1. **Coroutines** - Cooperative multitasking
1. **Actor model** - Message-passing concurrency
1. **Async/await** - Language-level async support
1. **Event-driven frameworks** - libuv, libevent

---

## Best Practices

1. **Start simple** - Use level-triggered mode initially
1. **Profile performance** - Measure before optimizing
1. **Handle all error cases** - Check return values
1. **Test under load** - Verify scalability claims
1. **Document state machines** - Clear protocol handling
1. **Monitor resource usage** - Watch memory and CPU

---

## Future Considerations

1. **io_uring adoption** - Modern alternative to epoll
1. **eBPF integration** - Kernel-space packet processing
1. **Hardware acceleration** - Smart NICs and DPUs
1. **Container awareness** - Resource limits and scheduling
1. **Security hardening** - Rate limiting and DoS protection
