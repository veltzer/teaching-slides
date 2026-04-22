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
# Advanced I/O

---

## Overview of Advanced I/O

1. **File locking** - Coordinate access between processes
1. **Record locking** - Lock specific file regions
1. **Memory-mapped I/O** - Map files into memory
1. **Asynchronous I/O** - Non-blocking I/O operations
1. **I/O vectors** - Scatter-gather operations
1. **Network server design** - High-performance patterns

---

## File Locking Fundamentals

![file_locking_fundamentals](svg/courses/operating_systems/linux-systems-programming/21_advanced_io/file_locking_fundamentals.svg)

---

## Advisory vs Mandatory Locking

```c
// Advisory locking (default in Linux)
int fd = open("shared_file.txt", O_WRONLY);
struct flock lock;
lock.l_type = F_WRLCK;      // Write lock
lock.l_whence = SEEK_SET;   // From beginning
lock.l_start = 0;           // Offset
lock.l_len = 0;             // Entire file

// This only works if all processes cooperate
if (fcntl(fd, F_SETLKW, &lock) == -1) {
    perror("fcntl lock");
}
```

1. **Advisory** - Processes must cooperate
1. **Mandatory** - Kernel enforces locks (rarely used)
1. **Default behavior** - Linux uses advisory locking
1. **Cooperation required** - All processes must check locks

---

## fcntl() File Locking

```c
#include <fcntl.h>

// Lock structure
struct flock {
    short l_type;    // F_RDLCK, F_WRLCK, F_UNLCK
    short l_whence;  // SEEK_SET, SEEK_CUR, SEEK_END
    off_t l_start;   // Offset for lock
    off_t l_len;     // Length (0 = to EOF)
    pid_t l_pid;     // PID holding lock (returned by F_GETLK)
};

// Set lock (blocking)
int set_lock(int fd, int type, off_t start, off_t len) {
    struct flock lock;
    lock.l_type = type;
    lock.l_whence = SEEK_SET;
    lock.l_start = start;
    lock.l_len = len;

    return fcntl(fd, F_SETLKW, &lock);
}

// Try to set lock (non-blocking)
int try_lock(int fd, int type, off_t start, off_t len) {
    struct flock lock;
    lock.l_type = type;
    lock.l_whence = SEEK_SET;
    lock.l_start = start;
    lock.l_len = len;

    return fcntl(fd, F_SETLK, &lock);
}
```

---

## Record Locking: Lock Helper

```c
struct record {
    int id;
    char name[32];
    int value;
};

int lock_record(int fd, int record_id, int lock_type) {
    struct flock lock;
    lock.l_type = lock_type;
    lock.l_whence = SEEK_SET;
    lock.l_start = record_id * sizeof(struct record);
    lock.l_len = sizeof(struct record);

    if (fcntl(fd, F_SETLKW, &lock) == -1) {
        if (errno == EAGAIN || errno == EACCES) {
            printf("Record %d is locked by another process\n", record_id);
        }
        return -1;
    }

    return 0;
}
```

---

## Record Locking: Read with Lock

```c
int read_record_locked(int fd, int record_id, struct record *rec) {
    if (lock_record(fd, record_id, F_RDLCK) == -1) {
        return -1;
    }

    lseek(fd, record_id * sizeof(struct record), SEEK_SET);

    ssize_t bytes = read(fd, rec, sizeof(struct record));

    lock_record(fd, record_id, F_UNLCK);

    return bytes == sizeof(struct record) ? 0 : -1;
}
```

---

## Lock Testing and Detection

```c
// Test if a region is locked
int test_lock(int fd, int type, off_t start, off_t len) {
    struct flock lock;
    lock.l_type = type;
    lock.l_whence = SEEK_SET;
    lock.l_start = start;
    lock.l_len = len;

    if (fcntl(fd, F_GETLK, &lock) == -1) {
        return -1;
    }

    if (lock.l_type == F_UNLCK) {
        return 0; // Not locked
    } else {
        printf("Locked by process %d with %s lock\n",
               lock.l_pid,
               lock.l_type == F_RDLCK ? "read" : "write");
        return 1; // Locked
    }
}

// Deadlock detection helper
void handle_deadlock(int signum) {
    printf("Potential deadlock detected (signal %d)\n", signum);
    // Implement deadlock recovery strategy
}
```

---

## flock() System Call

```c
#include <sys/file.h>

// Simpler file locking interface
int flock_example(const char *filename) {
    int fd = open(filename, O_WRONLY | O_CREAT, 0644);
    if (fd == -1) {
        return -1;
    }

    // Exclusive lock (blocks until available)
    if (flock(fd, LOCK_EX) == -1) {
        perror("flock");
        close(fd);
        return -1;
    }

    // Critical section - file is exclusively locked
    write(fd, "Locked content\n", 15);
    sleep(5); // Simulate work

    // Unlock (automatic on close)
    flock(fd, LOCK_UN);
    close(fd);

    return 0;
}

// Non-blocking flock
int try_flock(int fd) {
    if (flock(fd, LOCK_EX | LOCK_NB) == -1) {
        if (errno == EWOULDBLOCK) {
            printf("File is already locked\n");
        }
        return -1;
    }
    return 0;
}
```

---

## Lock Types Comparison

![lock_types_comparison](svg/courses/operating_systems/linux-systems-programming/21_advanced_io/lock_types_comparison.svg)

---

## Memory-Mapped I/O: map_file

```c
#include <sys/mman.h>

void *map_file(const char *filename, size_t *size) {
    int fd = open(filename, O_RDWR);
    if (fd == -1) {
        return MAP_FAILED;
    }

    struct stat st;
    fstat(fd, &st);
    *size = st.st_size;

    void *mapped = mmap(NULL, st.st_size, PROT_READ | PROT_WRITE,
                       MAP_SHARED, fd, 0);

    close(fd);
    return mapped;
}
```

---

## Memory-Mapped I/O: Process Mapped File

```c
int process_mapped_file(const char *filename) {
    size_t size;
    char *data = map_file(filename, &size);

    if (data == MAP_FAILED) {
        return -1;
    }

    for (size_t i = 0; i < size; i++) {
        if (data[i] == '\n') {
            data[i] = ' ';
        }
    }

    munmap(data, size);
    return 0;
}
```

---

## mmap() Flags and Protection

```c
// Protection flags
PROT_READ    // Page can be read
PROT_WRITE   // Page can be written
PROT_EXEC    // Page can be executed
PROT_NONE    // Page cannot be accessed

// Mapping flags
MAP_SHARED   // Share mapping with other processes
MAP_PRIVATE  // Create copy-on-write mapping
MAP_FIXED    // Map at exact address specified
MAP_ANONYMOUS // Map not backed by file

// Example: Create shared memory segment
void *create_shared_memory(size_t size) {
    void *addr = mmap(NULL, size, PROT_READ | PROT_WRITE,
                      MAP_SHARED | MAP_ANONYMOUS, -1, 0);

    if (addr == MAP_FAILED) {
        return NULL;
    }

    return addr;
}

// Example: Map executable code
void *map_executable(const char *filename) {
    int fd = open(filename, O_RDONLY);
    struct stat st;
    fstat(fd, &st);

    void *code = mmap(NULL, st.st_size, PROT_READ | PROT_EXEC,
                      MAP_PRIVATE, fd, 0);

    close(fd);
    return code;
}
```

---

## Memory Mapping Optimization

```c
// Advise kernel about memory access patterns
int optimize_memory_mapping(void *addr, size_t size, int pattern) {
    switch (pattern) {
        case ACCESS_NORMAL:
            return madvise(addr, size, MADV_NORMAL);
        case ACCESS_RANDOM:
            return madvise(addr, size, MADV_RANDOM);
        case ACCESS_SEQUENTIAL:
            return madvise(addr, size, MADV_SEQUENTIAL);
        case ACCESS_WILLNEED:
            return madvise(addr, size, MADV_WILLNEED);
        case ACCESS_DONTNEED:
            return madvise(addr, size, MADV_DONTNEED);
    }
    return -1;
}

// Synchronize mapped memory
int sync_mapped_memory(void *addr, size_t size, int flags) {
    // MS_SYNC: synchronous write
    // MS_ASYNC: asynchronous write
    // MS_INVALIDATE: invalidate cache
    return msync(addr, size, flags);
}

// Lock memory pages to prevent swapping
int lock_memory_pages(void *addr, size_t size) {
    if (mlock(addr, size) == -1) {
        perror("mlock");
        return -1;
    }
    return 0;
}
```

---

## Vectored I/O Operations

```c
#include <sys/uio.h>

// Scatter-gather I/O with iovec
struct iovec {
    void *iov_base;  // Starting address
    size_t iov_len;  // Number of bytes
};

// Read into multiple buffers
ssize_t scatter_read(int fd, struct iovec *iov, int count) {
    return readv(fd, iov, count);
}

// Write from multiple buffers
ssize_t gather_write(int fd, struct iovec *iov, int count) {
    return writev(fd, iov, count);
}

// Example: HTTP response with header and body
int send_http_response(int sockfd, const char *header, const char *body) {
    struct iovec iov[2];

    iov[0].iov_base = (void *)header;
    iov[0].iov_len = strlen(header);
    iov[1].iov_base = (void *)body;
    iov[1].iov_len = strlen(body);

    ssize_t written = writev(sockfd, iov, 2);
    return written == (iov[0].iov_len + iov[1].iov_len) ? 0 : -1;
}
```

---

## Advanced Vectored I/O: Setup

```c
int process_file_vectored(const char *filename) {
    int fd = open(filename, O_RDONLY);
    if (fd == -1) {
        return -1;
    }

    const int num_buffers = 4;
    const size_t buffer_size = 4096;
    struct iovec iov[num_buffers];

    for (int i = 0; i < num_buffers; i++) {
        iov[i].iov_base = malloc(buffer_size);
        iov[i].iov_len = buffer_size;
    }
```

---

## Advanced Vectored I/O: Process and Cleanup

```c
    ssize_t total_read = 0;
    ssize_t bytes;

    while ((bytes = readv(fd, iov, num_buffers)) > 0) {
        total_read += bytes;

        ssize_t remaining = bytes;
        for (int i = 0; i < num_buffers && remaining > 0; i++) {
            size_t to_process = remaining < iov[i].iov_len ?
                               remaining : iov[i].iov_len;

            process_buffer(iov[i].iov_base, to_process);
            remaining -= to_process;
        }
    }

    for (int i = 0; i < num_buffers; i++) {
        free(iov[i].iov_base);
    }

    close(fd);
    return total_read;
}
```

---

## Asynchronous I/O: State Machine

```c
enum async_state {
    ASYNC_IDLE,
    ASYNC_READING,
    ASYNC_WRITING,
    ASYNC_COMPLETE,
    ASYNC_ERROR
};

struct async_operation {
    int fd;
    void *buffer;
    size_t size;
    off_t offset;
    enum async_state state;
    void (*completion_callback)(struct async_operation *);
};
```

---

## Asynchronous I/O: Start Read

```c
int async_read_start(struct async_operation *op) {
    int flags = fcntl(op->fd, F_GETFL);
    fcntl(op->fd, F_SETFL, flags | O_NONBLOCK);

    op->state = ASYNC_READING;

    ssize_t bytes = pread(op->fd, op->buffer, op->size, op->offset);

    if (bytes == op->size) {
        op->state = ASYNC_COMPLETE;
        if (op->completion_callback) {
            op->completion_callback(op);
        }
        return 0;
    } else if (bytes == -1 && errno == EAGAIN) {
        return 1;
    } else {
        op->state = ASYNC_ERROR;
        return -1;
    }
}
```

---

## Network Server Design Patterns

![network_server_design_patterns](svg/courses/operating_systems/linux-systems-programming/21_advanced_io/network_server_design_patterns.svg)

---

## Thread-per-Connection: Handler

```c
void *handle_client(void *arg) {
    int client_fd = *(int *)arg;
    free(arg);

    char buffer[1024];
    ssize_t bytes;

    while ((bytes = read(client_fd, buffer, sizeof(buffer))) > 0) {
        write(client_fd, buffer, bytes);
    }

    close(client_fd);
    return NULL;
}
```

---

## Thread-per-Connection: Server Loop

```c
int threaded_server(int port) {
    int server_fd = create_server_socket(port);

    while (1) {
        struct sockaddr_in client_addr;
        socklen_t addr_len = sizeof(client_addr);

        int client_fd = accept(server_fd, (struct sockaddr*)&client_addr,
                              &addr_len);
        if (client_fd == -1) {
            continue;
        }

        pthread_t thread;
        int *client_fd_ptr = malloc(sizeof(int));
        *client_fd_ptr = client_fd;

        pthread_create(&thread, NULL, handle_client, client_fd_ptr);
        pthread_detach(thread);
    }

    return 0;
}
```

---

## Thread Pool: Structure

```c
struct work_item {
    int client_fd;
    struct work_item *next;
};

struct thread_pool {
    pthread_t *threads;
    int num_threads;
    struct work_item *work_queue;
    pthread_mutex_t queue_mutex;
    pthread_cond_t work_available;
    int shutdown;
};
```

---

## Thread Pool: Worker Thread

```c
void *worker_thread(void *arg) {
    struct thread_pool *pool = (struct thread_pool *)arg;

    while (!pool->shutdown) {
        pthread_mutex_lock(&pool->queue_mutex);

        while (pool->work_queue == NULL && !pool->shutdown) {
            pthread_cond_wait(&pool->work_available, &pool->queue_mutex);
        }

        if (pool->shutdown) {
            pthread_mutex_unlock(&pool->queue_mutex);
            break;
        }

        struct work_item *item = pool->work_queue;
        pool->work_queue = item->next;

        pthread_mutex_unlock(&pool->queue_mutex);

        handle_client_request(item->client_fd);
        close(item->client_fd);
        free(item);
    }

    return NULL;
}
```

---

## Thread Pool: Add Work

```c
int add_work(struct thread_pool *pool, int client_fd) {
    struct work_item *item = malloc(sizeof(struct work_item));
    item->client_fd = client_fd;
    item->next = NULL;

    pthread_mutex_lock(&pool->queue_mutex);

    if (pool->work_queue == NULL) {
        pool->work_queue = item;
    } else {
        struct work_item *last = pool->work_queue;
        while (last->next != NULL) {
            last = last->next;
        }
        last->next = item;
    }

    pthread_cond_signal(&pool->work_available);
    pthread_mutex_unlock(&pool->queue_mutex);

    return 0;
}
```

---

## Event-Driven Server: Setup

```c
struct client_connection {
    int fd;
    char *read_buffer;
    char *write_buffer;
    size_t read_pos;
    size_t write_pos;
    size_t write_len;
};

int event_driven_server(int port) {
    int server_fd = create_server_socket(port);
    int epoll_fd = epoll_create1(0);

    struct epoll_event ev;
    ev.events = EPOLLIN;
    ev.data.fd = server_fd;
    epoll_ctl(epoll_fd, EPOLL_CTL_ADD, server_fd, &ev);

    struct epoll_event events[MAX_EVENTS];

    while (1) {
        int nfds = epoll_wait(epoll_fd, events, MAX_EVENTS, -1);

        for (int i = 0; i < nfds; i++) {
            if (events[i].data.fd == server_fd) {
                handle_new_connection(server_fd, epoll_fd);
            } else {
                handle_client_event(events[i].data.fd, events[i].events);
            }
        }
    }

    return 0;
}
```

---

## Event-Driven Server: Client Event Handler

```c
void handle_client_event(int client_fd, uint32_t events) {
    if (events & EPOLLIN) {
        char buffer[4096];
        ssize_t bytes = read(client_fd, buffer, sizeof(buffer));

        if (bytes > 0) {
            write(client_fd, buffer, bytes);
        } else if (bytes == 0) {
            close(client_fd);
        }
    }

    if (events & (EPOLLERR | EPOLLHUP)) {
        close(client_fd);
    }
}
```

---

## High-Performance Server: Worker Thread

```c
struct server_thread {
    int epoll_fd;
    int thread_id;
    pthread_t thread;
    struct client_connection *connections[MAX_CONNECTIONS];
};

void *server_worker_thread(void *arg) {
    struct server_thread *worker = (struct server_thread *)arg;
    struct epoll_event events[MAX_EVENTS];

    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(worker->thread_id, &cpuset);
    pthread_setaffinity_np(worker->thread, sizeof(cpuset), &cpuset);

    while (1) {
        int nfds = epoll_wait(worker->epoll_fd, events, MAX_EVENTS, -1);

        for (int i = 0; i < nfds; i++) {
            struct client_connection *conn =
                (struct client_connection *)events[i].data.ptr;

            if (events[i].events & EPOLLIN) {
                handle_read(conn);
            }
            if (events[i].events & EPOLLOUT) {
                handle_write(conn);
            }
            if (events[i].events & (EPOLLERR | EPOLLHUP)) {
                cleanup_connection(conn);
            }
        }
    }

    return NULL;
}
```

---

## High-Performance Server: Load Balancing

```c
int distribute_connection(int client_fd) {
    static int next_thread = 0;
    int target_thread = next_thread++ % num_worker_threads;

    struct client_connection *conn = create_connection(client_fd);
    add_to_worker_epoll(target_thread, conn);

    return 0;
}
```

---

## Connection State Management: Types

```c
enum connection_state {
    CONN_READING_HEADER,
    CONN_READING_BODY,
    CONN_PROCESSING,
    CONN_WRITING_RESPONSE,
    CONN_CLOSING
};

struct http_connection {
    int fd;
    enum connection_state state;
    char *buffer;
    size_t buffer_size;
    size_t bytes_received;
    size_t content_length;
    struct http_request request;
    struct http_response response;
};
```

---

## Connection State Management: Handler

```c
int handle_http_connection(struct http_connection *conn, uint32_t events) {
    switch (conn->state) {
        case CONN_READING_HEADER:
            if (events & EPOLLIN) {
                if (read_http_header(conn) == 0) {
                    conn->state = CONN_READING_BODY;
                }
            }
            break;

        case CONN_READING_BODY:
            if (events & EPOLLIN) {
                if (read_http_body(conn) == 0) {
                    conn->state = CONN_PROCESSING;
                    process_http_request(conn);
                    conn->state = CONN_WRITING_RESPONSE;
                    modify_epoll_events(conn->fd, EPOLLOUT);
                }
            }
            break;

        case CONN_WRITING_RESPONSE:
            if (events & EPOLLOUT) {
                if (write_http_response(conn) == 0) {
                    conn->state = CONN_CLOSING;
                    return 1;
                }
            }
            break;
    }

    return 0;
}
```

---

## Zero-Copy in Network Servers: sendfile

```c
int serve_static_file_zerocopy(int client_fd, const char *filepath) {
    int file_fd = open(filepath, O_RDONLY);
    if (file_fd == -1) {
        return -1;
    }

    struct stat st;
    fstat(file_fd, &st);

    char headers[512];
    int header_len = snprintf(headers, sizeof(headers),
                             "HTTP/1.1 200 OK\r\n"
                             "Content-Length: %ld\r\n"
                             "Content-Type: application/octet-stream\r\n"
                             "\r\n", st.st_size);

    write(client_fd, headers, header_len);

    off_t offset = 0;
    ssize_t sent = 0;

    while (offset < st.st_size) {
        sent = sendfile(client_fd, file_fd, &offset, st.st_size - offset);
        if (sent <= 0) {
            break;
        }
    }

    close(file_fd);
    return offset == st.st_size ? 0 : -1;
}
```

---

## Zero-Copy in Network Servers: splice

```c
int proxy_with_splice(int client_fd, int upstream_fd) {
    int pipe_fds[2];
    pipe(pipe_fds);

    ssize_t to_pipe = splice(upstream_fd, NULL, pipe_fds[1], NULL,
                            4096, SPLICE_F_MOVE | SPLICE_F_NONBLOCK);

    if (to_pipe > 0) {
        ssize_t to_client = splice(pipe_fds[0], NULL, client_fd, NULL,
                                  to_pipe, SPLICE_F_MOVE | SPLICE_F_NONBLOCK);

        close(pipe_fds[0]);
        close(pipe_fds[1]);
        return to_client;
    }

    close(pipe_fds[0]);
    close(pipe_fds[1]);
    return to_pipe;
}
```

---

## Buffer Management: Ring Buffer Structure

```c
struct ring_buffer {
    char *data;
    size_t size;
    size_t head;
    size_t tail;
    size_t count;
};

struct ring_buffer *create_ring_buffer(size_t size) {
    struct ring_buffer *rb = malloc(sizeof(*rb));
    rb->data = malloc(size);
    rb->size = size;
    rb->head = rb->tail = rb->count = 0;
    return rb;
}
```

---

## Buffer Management: Read/Write

```c
size_t ring_buffer_write(struct ring_buffer *rb, const void *data, size_t len) {
    size_t available = rb->size - rb->count;
    size_t to_write = len < available ? len : available;

    for (size_t i = 0; i < to_write; i++) {
        rb->data[rb->head] = ((const char*)data)[i];
        rb->head = (rb->head + 1) % rb->size;
    }

    rb->count += to_write;
    return to_write;
}

size_t ring_buffer_read(struct ring_buffer *rb, void *data, size_t len) {
    size_t to_read = len < rb->count ? len : rb->count;

    for (size_t i = 0; i < to_read; i++) {
        ((char*)data)[i] = rb->data[rb->tail];
        rb->tail = (rb->tail + 1) % rb->size;
    }

    rb->count -= to_read;
    return to_read;
}
```

---

## Connection Pooling: Get Connection

```c
struct connection_pool {
    struct database_connection *connections;
    int pool_size;
    int active_count;
    pthread_mutex_t pool_mutex;
    pthread_cond_t connection_available;
};

struct database_connection *get_connection(struct connection_pool *pool) {
    pthread_mutex_lock(&pool->pool_mutex);

    while (pool->active_count >= pool->pool_size) {
        pthread_cond_wait(&pool->connection_available, &pool->pool_mutex);
    }

    for (int i = 0; i < pool->pool_size; i++) {
        if (!pool->connections[i].in_use) {
            pool->connections[i].in_use = 1;
            pool->active_count++;
            pthread_mutex_unlock(&pool->pool_mutex);
            return &pool->connections[i];
        }
    }

    pthread_mutex_unlock(&pool->pool_mutex);
    return NULL;
}
```

---

## Connection Pooling: Return Connection

```c
void return_connection(struct connection_pool *pool,
                      struct database_connection *conn) {
    pthread_mutex_lock(&pool->pool_mutex);

    conn->in_use = 0;
    pool->active_count--;

    pthread_cond_signal(&pool->connection_available);
    pthread_mutex_unlock(&pool->pool_mutex);
}
```

---

## Performance Monitoring: Metrics Struct

```c
struct server_metrics {
    atomic_long total_connections;
    atomic_long active_connections;
    atomic_long requests_processed;
    atomic_long bytes_read;
    atomic_long bytes_written;
    atomic_long errors;

    struct timespec start_time;
    double avg_request_time;
    double peak_request_time;
};

void update_metrics(struct server_metrics *metrics,
                   double request_time, size_t bytes_in, size_t bytes_out) {
    atomic_fetch_add(&metrics->requests_processed, 1);
    atomic_fetch_add(&metrics->bytes_read, bytes_in);
    atomic_fetch_add(&metrics->bytes_written, bytes_out);

    if (request_time > metrics->peak_request_time) {
        metrics->peak_request_time = request_time;
    }

    metrics->avg_request_time =
        (metrics->avg_request_time * 0.9) + (request_time * 0.1);
}
```

---

## Performance Monitoring: Print Stats

```c
void print_server_stats(struct server_metrics *metrics) {
    printf("Server Statistics:\n");
    printf("  Active connections: %ld\n",
           atomic_load(&metrics->active_connections));
    printf("  Total requests: %ld\n",
           atomic_load(&metrics->requests_processed));
    printf("  Average request time: %.3f ms\n",
           metrics->avg_request_time * 1000);
    printf("  Peak request time: %.3f ms\n",
           metrics->peak_request_time * 1000);
}
```

---

## Error Handling: Error Dispatcher

```c
int handle_server_error(int error_type, void *context) {
    switch (error_type) {
        case SERVER_ERROR_MEMORY:
            cleanup_idle_connections();
            garbage_collect();
            break;

        case SERVER_ERROR_FD_LIMIT:
            close_oldest_connections(10);
            break;

        case SERVER_ERROR_NETWORK:
            reset_network_connections();
            break;

        case SERVER_ERROR_DISK_FULL:
            enable_emergency_mode();
            send_alerts();
            break;

        default:
            log_error("Unknown server error: %d", error_type);
            break;
    }

    return 0;
}
```

---

## Error Handling: Circuit Breaker Struct

```c
struct circuit_breaker {
    int failure_count;
    int failure_threshold;
    time_t last_failure;
    int timeout_seconds;
    enum { CLOSED, OPEN, HALF_OPEN } state;
};
```

---

## Error Handling: Circuit Breaker Open/Half-Open

```c
int circuit_breaker_call(struct circuit_breaker *cb,
                        int (*operation)(void *), void *arg) {
    time_t now = time(NULL);

    switch (cb->state) {
        case OPEN:
            if (now - cb->last_failure > cb->timeout_seconds) {
                cb->state = HALF_OPEN;
            } else {
                return -1;
            }
            break;

        case HALF_OPEN:
            if (operation(arg) == 0) {
                cb->failure_count = 0;
                cb->state = CLOSED;
                return 0;
            } else {
                cb->state = OPEN;
                cb->last_failure = now;
                return -1;
            }
```

---

## Error Handling: Circuit Breaker Closed

```c
        case CLOSED:
            if (operation(arg) == 0) {
                return 0;
            } else {
                cb->failure_count++;
                if (cb->failure_count >= cb->failure_threshold) {
                    cb->state = OPEN;
                    cb->last_failure = now;
                }
                return -1;
            }
    }

    return -1;
}
```

---

## Load Testing: Worker

```c
struct load_test_config {
    char *server_host;
    int server_port;
    int num_connections;
    int requests_per_connection;
    int concurrent_connections;
};

void *load_test_worker(void *arg) {
    struct load_test_config *config = (struct load_test_config *)arg;

    for (int i = 0; i < config->requests_per_connection; i++) {
        int fd = connect_to_server(config->server_host, config->server_port);
        if (fd == -1) {
            continue;
        }

        char request[] = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n";
        write(fd, request, sizeof(request) - 1);

        char response[4096];
        read(fd, response, sizeof(response));

        close(fd);
    }

    return NULL;
}
```

---

## Load Testing: Run Test

```c
int run_load_test(struct load_test_config *config) {
    pthread_t *threads = malloc(config->concurrent_connections *
                               sizeof(pthread_t));

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < config->concurrent_connections; i++) {
        pthread_create(&threads[i], NULL, load_test_worker, config);
    }

    for (int i = 0; i < config->concurrent_connections; i++) {
        pthread_join(threads[i], NULL);
    }

    clock_gettime(CLOCK_MONOTONIC, &end);

    double elapsed = (end.tv_sec - start.tv_sec) +
                    (end.tv_nsec - start.tv_nsec) / 1e9;

    int total_requests = config->concurrent_connections *
                        config->requests_per_connection;

    printf("Load test results:\n");
    printf("  Total requests: %d\n", total_requests);
    printf("  Time elapsed: %.2f seconds\n", elapsed);
    printf("  Requests per second: %.2f\n", total_requests / elapsed);

    free(threads);
    return 0;
}
```

---

## Best Practices Summary

1. **Choose appropriate architecture** - Match server design to requirements
1. **Use non-blocking I/O** - For scalable network servers
1. **Implement proper error handling** - Graceful degradation
1. **Monitor performance** - Track key metrics
1. **Use memory efficiently** - Pool allocations, avoid leaks
1. **Test under load** - Verify performance characteristics

---

## Common Pitfalls

1. **Blocking operations** - In event-driven servers
1. **Resource leaks** - File descriptors, memory
1. **Race conditions** - In multi-threaded servers
1. **Buffer overflows** - Always check bounds
1. **Deadlocks** - In complex locking schemes
1. **Poor error recovery** - Servers should be robust

---

## Future Considerations

1. **io_uring adoption** - Modern async I/O interface
1. **eBPF integration** - Kernel-space packet processing
1. **QUIC protocol** - UDP-based transport
1. **HTTP/3 support** - Next-generation web protocols
1. **Container optimization** - Resource-aware applications
1. **Hardware acceleration** - Smart NICs and DPUs
