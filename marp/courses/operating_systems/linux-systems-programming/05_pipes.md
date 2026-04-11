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
# Pipes in Linux

---

## Chapter Overview

1. **What are Pipes**
1. **The pipe() System Call**
1. **File Descriptor Management**
1. **Named Pipes (FIFOs)**
1. **Pipe Internals**
1. **Common Patterns**
1. **Best Practices**

---

## What is a Pipe?

## Definition:
- **Unidirectional** data channel
- **Byte stream** interface
- **In-memory** buffer
- **First In, First Out** (FIFO)
- **Inter-Process Communication** (IPC)

```bash
# Shell pipe example
ls | grep txt | wc -l
```

---

## Pipe Characteristics

## Properties:

1. **Unidirectional** - Data flows one way
1. **Byte-oriented** - No message boundaries
1. **Buffered** - Usually 64KB on Linux
1. **Blocking** - Read/write can block
1. **Anonymous** - No name in filesystem
1. **Related processes** - Parent/child

---

## Pipe Anatomy

![pipe_anatomy](svg/courses/operating_systems/linux-systems-programming/05_pipes/pipe_anatomy.svg)

---

## The pipe() System Call

```c
#include <unistd.h>

int main() {
    int pipefd[2];

    // Create pipe
    if (pipe(pipefd) == -1) {
        perror("pipe");
        exit(1);
    }

    // pipefd[0] - read end
    // pipefd[1] - write end

    write(pipefd[1], "Hello", 5);

    char buffer[10];
    read(pipefd[0], buffer, 5);
}
```

---

## Parent-Child Communication

```c
int main() {
    int pipefd[2];
    pipe(pipefd);

    pid_t pid = fork();

    if (pid == 0) {
        // Child: reader
        close(pipefd[1]);  // Close write end

        char buffer[100];
        read(pipefd[0], buffer, sizeof(buffer));
        printf("Child received: %s\n", buffer);
        close(pipefd[0]);
    } else {
        // Parent: writer
        close(pipefd[0]);  // Close read end

        write(pipefd[1], "Hello child!", 12);
        close(pipefd[1]);
        wait(NULL);
    }
}
```

---

## File Descriptor Table After Fork

![file_descriptor_table_after_fork](svg/courses/operating_systems/linux-systems-programming/05_pipes/file_descriptor_table_after_fork.svg)

---

## Why Close Unused Ends?

```c
// BAD: Not closing unused ends
if (pid == 0) {
    // Child reads but doesn't close write end
    char buf[100];
    read(pipefd[0], buf, 100);  // May hang!
}

// GOOD: Close unused ends
if (pid == 0) {
    close(pipefd[1]);  // Close write end
    char buf[100];
    int n = read(pipefd[0], buf, 100);
    // Gets EOF when parent closes write end
}
```

**EOF only when ALL write ends closed!**

---

## EOF Condition

```c
// Writer
write(pipefd[1], "data", 4);
close(pipefd[1]);  // Send EOF

// Reader
while (1) {
    char buffer[100];
    ssize_t n = read(pipefd[0], buffer, sizeof(buffer));

    if (n > 0) {
        // Got data
        process_data(buffer, n);
    } else if (n == 0) {
        // EOF - all writers closed
        break;
    } else {
        // Error
        perror("read");
        break;
    }
}
```

---

## SIGPIPE Signal

```c
// What happens when reader closes first?

// Reader
close(pipefd[0]);  // Close read end

// Writer
ssize_t n = write(pipefd[1], "data", 4);
// Gets SIGPIPE signal!
// Default action: terminate process

// Handle or ignore SIGPIPE
signal(SIGPIPE, SIG_IGN);
ssize_t n = write(pipefd[1], "data", 4);
if (n == -1 && errno == EPIPE) {
    // Reader closed
}
```

---

## Bidirectional Communication

```c
// Need TWO pipes for bidirectional
int pipe_to_child[2];
int pipe_to_parent[2];

pipe(pipe_to_child);
pipe(pipe_to_parent);

if (fork() == 0) {
    // Child
    close(pipe_to_child[1]);  // Close write
    close(pipe_to_parent[0]);  // Close read

    // Read from parent
    read(pipe_to_child[0], buffer, size);

    // Write to parent
    write(pipe_to_parent[1], response, size);
} else {
    // Parent - opposite
    close(pipe_to_child[0]);
    close(pipe_to_parent[1]);

    write(pipe_to_child[1], command, size);
    read(pipe_to_parent[0], response, size);
}
```

---

## Using dup2() for Redirection

```c
// Redirect stdout to pipe
int pipefd[2];
pipe(pipefd);

if (fork() == 0) {
    // Child: make stdout go to pipe
    close(pipefd[0]);  // Close read

    // Duplicate write end to stdout
    dup2(pipefd[1], STDOUT_FILENO);
    close(pipefd[1]);  // Close original

    // Now stdout goes to pipe
    printf("This goes to pipe\n");
    execl("/bin/ls", "ls", NULL);
}
```

---

## Implementing Shell Pipes

```c
// ls | grep txt
int pipefd[2];
pipe(pipefd);

if (fork() == 0) {
    // First child: ls
    dup2(pipefd[1], STDOUT_FILENO);
    close(pipefd[0]);
    close(pipefd[1]);
    execl("/bin/ls", "ls", NULL);
}

if (fork() == 0) {
    // Second child: grep
    dup2(pipefd[0], STDIN_FILENO);
    close(pipefd[0]);
    close(pipefd[1]);
    execl("/bin/grep", "grep", "txt", NULL);
}

// Parent closes both ends
close(pipefd[0]);
close(pipefd[1]);
wait(NULL); wait(NULL);
```

---

## Multiple Pipes Chain

```c
// cmd1 | cmd2 | cmd3
void pipeline(char *cmds[], int n) {
    int pipefds[2];
    int prev_pipe = STDIN_FILENO;

    for (int i = 0; i < n; i++) {
        pipe(pipefds);

        if (fork() == 0) {
            // Redirect input from previous
            dup2(prev_pipe, STDIN_FILENO);

            // Redirect output to next (not last)
            if (i < n-1) {
                dup2(pipefds[1], STDOUT_FILENO);
            }

            close(pipefds[0]);
            close(pipefds[1]);
            exec_command(cmds[i]);
        }

        close(prev_pipe);
        close(pipefds[1]);
        prev_pipe = pipefds[0];
    }
}
```

---

## popen() - High Level Pipe

```c
#include <stdio.h>

// Easier than pipe+fork+exec
FILE *fp = popen("ls -l", "r");
if (fp == NULL) {
    perror("popen");
    exit(1);
}

char line[256];
while (fgets(line, sizeof(line), fp)) {
    printf("Output: %s", line);
}

int status = pclose(fp);
if (WIFEXITED(status)) {
    printf("Command exited with %d\n",
           WEXITSTATUS(status));
}
```

---

## popen() Modes

```c
// Read mode - read command output
FILE *fp = popen("ls", "r");
char buffer[100];
fread(buffer, 1, 100, fp);
pclose(fp);

// Write mode - send input to command
FILE *fp = popen("grep pattern", "w");
fprintf(fp, "line with pattern\n");
fprintf(fp, "line without\n");
pclose(fp);

// Note: Can't do both read AND write
// Use two pipes for bidirectional
```

---

## Pipe Buffer and Atomicity

```c
// PIPE_BUF = 4096 on Linux
// Writes <= PIPE_BUF are atomic

// Atomic write (won't interleave)
char msg[4096];
write(pipefd[1], msg, sizeof(msg));

// Non-atomic (may interleave)
char big_msg[8192];
write(pipefd[1], big_msg, sizeof(big_msg));

// Check system limit
#include <limits.h>
printf("PIPE_BUF = %d\n", PIPE_BUF);

// Get actual pipe size
int size = fcntl(pipefd[0], F_GETPIPE_SZ);
```

---

## Pipe Size and Tuning

```c
// Default pipe size: 64KB on Linux

// Get pipe size
int size = fcntl(pipefd[0], F_GETPIPE_SZ);
printf("Pipe size: %d\n", size);

// Set pipe size (CAP_SYS_RESOURCE needed for > limit)
int new_size = 1048576;  // 1MB
fcntl(pipefd[1], F_SETPIPE_SZ, new_size);

// System limits
// /proc/sys/fs/pipe-max-size
// /proc/sys/fs/pipe-user-pages-hard
// /proc/sys/fs/pipe-user-pages-soft
```

---

## Non-blocking Pipes

```c
#include <fcntl.h>

// Make pipe non-blocking
int flags = fcntl(pipefd[0], F_GETFL);
fcntl(pipefd[0], F_SETFL, flags | O_NONBLOCK);

// Non-blocking read
ssize_t n = read(pipefd[0], buffer, size);
if (n == -1) {
    if (errno == EAGAIN || errno == EWOULDBLOCK) {
        // No data available
    } else {
        // Real error
        perror("read");
    }
}

// Useful for polling multiple sources
```

---

## Named Pipes (FIFOs)

```c
#include <sys/stat.h>

// Create named pipe
if (mkfifo("/tmp/myfifo", 0666) == -1) {
    perror("mkfifo");
}

// Writer process
int fd = open("/tmp/myfifo", O_WRONLY);
write(fd, "Hello", 5);
close(fd);

// Reader process (different program)
int fd = open("/tmp/myfifo", O_RDONLY);
char buffer[100];
read(fd, buffer, sizeof(buffer));
close(fd);

// Remove when done
unlink("/tmp/myfifo");
```

---

## FIFO Characteristics

## Named Pipes:

1. **Exist in filesystem** - Have a path
1. **Survive process** - Persistent
1. **Unrelated processes** - Can communicate
1. **Same as pipes** - Otherwise identical
1. **Special file** - No disk storage

```bash
# Create from shell
mkfifo /tmp/myfifo

# Shows as pipe
ls -l /tmp/myfifo
prw-rw-r-- 1 user user 0 Jan 1 12:00 /tmp/myfifo
#^-- 'p' for pipe
```

---

## FIFO Blocking Behavior

```c
// FIFOs block on open() until both ends connected

// This blocks until a reader opens
int fd = open("/tmp/myfifo", O_WRONLY);

// This blocks until a writer opens
int fd = open("/tmp/myfifo", O_RDONLY);

// Non-blocking open
int fd = open("/tmp/myfifo", O_RDONLY | O_NONBLOCK);
if (fd == -1 && errno == ENXIO) {
    // No writer yet
}

// Often used for synchronization
```

---

## FIFO Use Cases

## Common Applications:

1. **Client-Server** on same machine
1. **Command line** data passing
   ```bash
   mkfifo pipe
   gzip < pipe &
   tar cf - . > pipe
   ```

1. **Video streaming**
   ```bash
   mkfifo video.pipe
   ffmpeg -i input.mp4 -f mpegts video.pipe &
   vlc video.pipe
   ```

1. **Process synchronization**

---

## Pipe vs FIFO Comparison

| Feature | Pipe | FIFO |
|---------|------|------|
| **Creation** | pipe() | mkfifo() |
| **Name** | Anonymous | Named path |
| **Persistence** | Process lifetime | Until deleted |
| **Processes** | Related | Any |
| **Shell** | &#124; operator | mkfifo command |
| **Use case** | Parent-child | Client-server |

---

## Pipe Limitations

## Issues:

1. **Unidirectional** - Need two for duplex
1. **Related processes** - Or use FIFO
1. **Byte stream** - No message boundaries
1. **Limited buffer** - Can block
1. **Local only** - Same machine
1. **No broadcast** - One reader gets data

## Alternatives:
- **Sockets** - Network, bidirectional
- **Message queues** - Boundaries
- **Shared memory** - Faster

---

## Select/Poll with Pipes

```c
// Monitor multiple pipes
fd_set readfds;
FD_ZERO(&readfds);
FD_SET(pipe1[0], &readfds);
FD_SET(pipe2[0], &readfds);

int maxfd = MAX(pipe1[0], pipe2[0]) + 1;

struct timeval timeout = {.tv_sec = 5};
int ready = select(maxfd, &readfds, NULL, NULL, &timeout);

if (ready > 0) {
    if (FD_ISSET(pipe1[0], &readfds)) {
        // Data on pipe1
        read(pipe1[0], buffer, size);
    }
    if (FD_ISSET(pipe2[0], &readfds)) {
        // Data on pipe2
        read(pipe2[0], buffer, size);
    }
}
```

---

## Splicing Data (Zero-Copy)

```c
#define _GNU_SOURCE
#include <fcntl.h>

// Zero-copy transfer between pipes
int pipeA[2], pipeB[2];
pipe(pipeA);
pipe(pipeB);

// Move data from pipeA to pipeB without copying
ssize_t n = splice(
    pipeA[0], NULL,  // Source
    pipeB[1], NULL,  // Destination
    4096,            // Size
    SPLICE_F_MOVE    // Flags
);

// Also: tee() for duplicating pipe data
tee(pipeA[0], pipeB[1], 4096, 0);
```

---

## inetd Pattern with Pipes

```c
// Server redirects stdin/stdout to socket
// Programs work over network without modification

void handle_client(int client_socket) {
    if (fork() == 0) {
        // Redirect stdin/stdout to socket
        dup2(client_socket, STDIN_FILENO);
        dup2(client_socket, STDOUT_FILENO);
        close(client_socket);

        // Execute program - uses stdin/stdout
        execl("/usr/games/fortune", "fortune", NULL);
    }
    close(client_socket);
}

// Client sees fortune output over network!
```

---

## Debugging Pipes

```bash
# See pipe usage
lsof | grep PIPE

# Monitor pipe data
strace -e read,write -s 100 ./program

# Check pipe buffer
cat /proc/sys/fs/pipe-max-size

# See FIFOs
find /tmp -type p

# Test FIFO
echo "test" > /tmp/myfifo &
cat /tmp/myfifo
```

---

## Common Pipe Bugs

## 1. Deadlock
```c
// BAD: Circular wait
// Parent writes, waits for child
// Child reads all, then writes back
// Deadlock if pipe buffer fills!
```

## 2. Not Closing FDs
```c
// BAD: EOF never arrives
// Forgot close(pipefd[1]) in reader
```

## 3. SIGPIPE Crash
```c
// BAD: Default SIGPIPE kills process
write(pipefd[1], data, size);  // Boom!
```

---

## Best Practices

1. **Always close unused ends**
   ```c
   close(pipefd[write_end]);  // In reader
   close(pipefd[read_end]);   // In writer
   ```

1. **Handle SIGPIPE**
   ```c
   signal(SIGPIPE, SIG_IGN);
   ```

1. **Check return values**
   ```c
   if (read(fd, buf, size) == -1) {
       perror("read");
   }
   ```

1. **Use higher-level APIs when appropriate**
    - popen() for simple cases

1. **Consider alternatives**
    - Sockets for bidirectional
    - Shared memory for performance

---

## Performance Tips

1. **Adjust pipe size** for throughput
   ```c
   fcntl(fd, F_SETPIPE_SZ, 1048576);
   ```

1. **Use splice()** for zero-copy

1. **Batch writes** to reduce syscalls

1. **Non-blocking** for responsiveness

1. **Consider shared memory** for large data

1. **Profile** with perf/strace

---

## Security Considerations

```c
// FIFOs have filesystem permissions
mkfifo("/tmp/myfifo", 0600);  // Owner only

// Check for symbolic links
struct stat st;
lstat("/tmp/myfifo", &st);
if (!S_ISFIFO(st.st_mode)) {
    // Not a FIFO!
}

// Use mkstemp() for unique names
char template[] = "/tmp/fifoXXXXXX";
mkstemp(template);
unlink(template);
mkfifo(template, 0600);
```

---

## Real-World Example: Logger

```c
// Central logging via FIFO
#define LOG_FIFO "/var/run/app.fifo"

// Logger daemon
void logger_daemon() {
    mkfifo(LOG_FIFO, 0622);
    int fd = open(LOG_FIFO, O_RDONLY);

    char buffer[1024];
    while (1) {
        ssize_t n = read(fd, buffer, sizeof(buffer)-1);
        if (n > 0) {
            buffer[n] = '\0';
            syslog(LOG_INFO, "%s", buffer);
        }
    }
}

// Client apps
void log_message(const char *msg) {
    int fd = open(LOG_FIFO, O_WRONLY | O_NONBLOCK);
    if (fd != -1) {
        write(fd, msg, strlen(msg));
        close(fd);
    }
}
```

---

## Advanced: Pipe Pairs

```c
// Full-duplex communication
int sv[2];
if (socketpair(AF_UNIX, SOCK_STREAM, 0, sv) == -1) {
    perror("socketpair");
}

if (fork() == 0) {
    // Child
    close(sv[0]);
    // Read and write on sv[1]
    write(sv[1], "Hello", 5);
    read(sv[1], buffer, size);
} else {
    // Parent
    close(sv[1]);
    // Read and write on sv[0]
    read(sv[0], buffer, size);
    write(sv[0], "Reply", 5);
}
```

---

## Summary

## Key Takeaways:

- **Pipes** enable IPC between related processes
- **pipe()** creates anonymous pipe
- **Always close** unused ends
- **SIGPIPE** needs handling
- **FIFOs** work for unrelated processes
- **Buffering** affects behavior
- **Many patterns** built on pipes

Master pipes = Build powerful IPC!
