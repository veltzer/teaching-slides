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
# Processes in Linux

---
## Process Lifecycle

![process_lifecycle](svg/courses/operating_systems/linux-systems-programming/04_processes/process_lifecycle.svg)

---

## Fork and Exec Pattern

![fork_exec_flow](svg/courses/operating_systems/linux-systems-programming/04_processes/fork_exec_flow.svg)

---

## Chapter Overview

1. **Process Tree and Init**
1. **Systemd and Containers**
1. **Process Creation**
1. **Process States and Waiting**
1. **Zombies and Orphans**
1. **Fork/Exec Pattern**
1. **Advanced Process Management**

---

## What is a Process?

## Definition:
- **Running instance** of a program
- Own **address space** and resources
- **PID** (Process ID) identifier
- **Scheduled** by kernel
- **Context** includes registers, memory, files

Every command you run creates a process!

---

## Process Components

![process_components](svg/courses/operating_systems/linux-systems-programming/04_processes/process_components.svg)

---

## The Process Tree

```console
systemd(1)─┬─systemd-journal(559)
          ├─systemd-udevd(580)
          ├─systemd-network(612)
          ├─systemd-resolve(614)
          ├─sshd(892)───sshd(1205)───bash(1207)───vim(2103)
          ├─nginx(920)─┬─nginx(921)
          │            └─nginx(922)
          ├─cron(900)
          └─dockerd(1050)───docker-containe(1100)───app(1150)
```

**Every process has exactly one parent** (except init)

---

## Viewing Process Tree

```bash
# Text tree view
pstree
pstree -p  # Show PIDs
pstree -u  # Show user changes

# Process list
ps aux
ps -ef
ps -ejH  # Tree format

# Real-time view
top
htop  # Better interface

# Detailed info
cat /proc/$$/status
cat /proc/$$/stat
```

---

## /sbin/init - The First Process

## PID 1 Special Properties:

1. **Started by kernel** at boot
1. **Parent of all** processes
1. **Cannot die** - kernel panic if killed
1. **Adopts orphans** automatically
1. **Reaps zombies** without parent
1. **Immune to signals** it doesn't handle
1. **Controls runlevels/targets**

---

## Init System Evolution

![init_system_evolution](svg/courses/operating_systems/linux-systems-programming/04_processes/init_system_evolution.svg)

---

## Systemd Overview

## Modern Init System:

- **Parallel startup** - Fast boot
- **Dependency management** - Correct order
- **On-demand activation** - Socket/D-Bus
- **Cgroups integration** - Resource control
- **Journald logging** - Structured logs
- **Timer units** - Replace cron
- **Target units** - Replace runlevels

---

## Systemd Architecture

![systemd_architecture](svg/courses/operating_systems/linux-systems-programming/04_processes/systemd_architecture.svg)

---

## Systemd Unit Files

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application Service
Documentation=man:myapp(8)
After=network.target postgresql.service
Requires=postgresql.service
Wants=redis.service

[Service]
Type=notify
User=appuser
Group=appgroup
WorkingDirectory=/opt/myapp
Environment="NODE_ENV=production"
ExecStartPre=/opt/myapp/bin/check-config
ExecStart=/opt/myapp/bin/start
ExecReload=/bin/kill -HUP $MAINPID
ExecStop=/opt/myapp/bin/stop
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

## Systemd Service Types

```ini
[Service]
# Type=simple (default)
# - Process doesn't fork
# - systemd considers it started immediately

# Type=forking
# - Traditional daemons that fork
# - Parent process exits

# Type=oneshot
# - Process exits, service remains active

# Type=notify
# - Service sends notification when ready
# - sd_notify(0, "READY=1")

# Type=dbus
# - Service acquires D-Bus name

# Type=idle
# - Delayed until all jobs dispatched
```

---

## Managing Services with Systemd

```bash
# Service control
systemctl start myapp.service
systemctl stop myapp.service
systemctl restart myapp.service
systemctl reload myapp.service

# Enable at boot
systemctl enable myapp.service
systemctl disable myapp.service

# Status and logs
systemctl status myapp.service
journalctl -u myapp.service
journalctl -f -u myapp.service  # Follow

# List units
systemctl list-units
systemctl list-unit-files

# Reload systemd
systemctl daemon-reload
```

---

## Container Initialization Problem

## The PID 1 Problem in Containers:

```dockerfile
# BAD: Application as PID 1
FROM ubuntu
CMD ["python", "app.py"]
# Problems:
# - Doesn't reap zombies
# - Doesn't handle signals properly
# - No graceful shutdown

# GOOD: Proper init
FROM ubuntu
RUN apt-get install -y tini
ENTRYPOINT ["tini", "--"]
CMD ["python", "app.py"]
```

---

## Container Init Solutions

## Options:

1. **tini** - Minimal init (1MB)
1. **dumb-init** - Python-based
1. **s6-overlay** - Full supervision
1. **systemd** - Full init (heavy)
1. **--init flag** - Docker built-in

```bash
# Docker with init
docker run --init myimage

# Kubernetes
# Add initContainers or use distroless
```

---

## Default User in Docker

```dockerfile
# Security: Don't run as root
FROM ubuntu

# Create user
RUN useradd -m -u 1000 appuser

# Switch to user
USER appuser

# Or at runtime
docker run --user 1000:1000 myimage

# Check user
docker exec container whoami
```

---

## Creating Processes - fork()

```c
#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>

int main() {
    printf("Parent PID: %d\n", getpid());

    pid_t pid = fork();

    if (pid < 0) {
        // Fork failed
        perror("fork");
        return 1;
    } else if (pid == 0) {
        // Child process
        printf("Child PID: %d, Parent: %d\n",
               getpid(), getppid());
        sleep(2);
        return 42;  // Exit code
    } else {
        // Parent process
        printf("Created child with PID: %d\n", pid);
        int status;
        waitpid(pid, &status, 0);
        printf("Child exited with: %d\n",
               WEXITSTATUS(status));
    }
    return 0;
}
```

---

## How fork() Works

![how_fork_works](svg/courses/operating_systems/linux-systems-programming/04_processes/how_fork_works.svg)

---

## Copy-on-Write (COW)

## Memory Efficiency:

```c
int global = 100;
char huge_array[1000000];  // 1MB

pid_t pid = fork();

if (pid == 0) {
    // Child
    printf("%d\n", global);      // Read: shared page
    huge_array[0] = 'X';         // Write: page copied
    global = 200;                // Write: page copied
}

// Only modified pages are copied!
// Unmodified pages remain shared
```

---

## What Gets Inherited

## Inherited from Parent:
- Memory (text, data, heap, stack)
- Open file descriptors
- Signal handlers
- Nice value
- Current working directory
- Root directory
- umask
- Resource limits
- Environment variables

## Unique in Child:
- Process ID (PID)
- Parent PID (PPID)
- File locks
- Pending signals
- Timers

---

## Waiting for Children

```c
#include <sys/wait.h>

// wait() - Wait for any child
int status;
pid_t pid = wait(&status);

// waitpid() - Wait for specific child
pid_t result = waitpid(child_pid, &status, 0);

// Options for waitpid
WNOHANG     // Return immediately if no child exited
WUNTRACED   // Return if child stopped
WCONTINUED  // Return if stopped child continued

// Non-blocking wait
while ((pid = waitpid(-1, &status, WNOHANG)) > 0) {
    printf("Child %d exited\n", pid);
}
```

---

## Analyzing Exit Status

```c
int status;
pid_t pid = waitpid(child_pid, &status, 0);

if (pid > 0) {
    if (WIFEXITED(status)) {
        // Normal termination
        int exit_code = WEXITSTATUS(status);
        printf("Child exited with code %d\n", exit_code);
    }
    else if (WIFSIGNALED(status)) {
        // Killed by signal
        int sig = WTERMSIG(status);
        printf("Child killed by signal %d\n", sig);
        if (WCOREDUMP(status)) {
            printf("Core dumped\n");
        }
    }
    else if (WIFSTOPPED(status)) {
        // Stopped (not terminated)
        int sig = WSTOPSIG(status);
        printf("Child stopped by signal %d\n", sig);
    }
}
```

---

## Process State Transitions

![process_state_transitions](svg/courses/operating_systems/linux-systems-programming/04_processes/process_state_transitions.svg)

---

## Linux Process States in /proc

```bash
# From /proc/[pid]/stat
R - Running or runnable (on run queue)
S - Interruptible sleep (waiting for event)
D - Uninterruptible sleep (usually IO)
T - Stopped by job control signal
t - Stopped by debugger (traced)
Z - Zombie (terminated but not reaped)
X - Dead (should never be seen)
I - Idle kernel thread

# Check process state
ps aux | grep process_name
cat /proc/$$/stat | awk '{print $3}'

# State with details
cat /proc/$$/status | grep State
```

---

## Zombies - The Undead Processes

## What is a Zombie?

```c
// Creating a zombie
if (fork() == 0) {
    // Child exits immediately
    exit(0);
}
// Parent doesn't call wait()
sleep(60);  // Child is zombie for 60 seconds

// Zombie characteristics:
// - Process terminated
// - Parent hasn't called wait()
// - Holds exit status in process table
// - No memory/CPU used
// - Can't be killed (already dead!)
// - Shows as <defunct> in ps
```

---

## Preventing Zombies

## Method 1: Signal Handler

```c
void sigchld_handler(int sig) {
    int saved_errno = errno;
    // Reap all available zombie children
    while (waitpid(-1, NULL, WNOHANG) > 0);
    errno = saved_errno;
}

int main() {
    struct sigaction sa;
    sa.sa_handler = sigchld_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;
    sigaction(SIGCHLD, &sa, NULL);

    // Now safe to create children
    for (int i = 0; i < 10; i++) {
        if (fork() == 0) {
            sleep(i);
            exit(0);
        }
    }

    // Parent continues work
    while (1) {
        // Do work...
        sleep(1);
    }
}
```

---

## Preventing Zombies (cont.)

## Method 2: Double Fork

```c
void create_daemon() {
    pid_t pid = fork();

    if (pid == 0) {
        // First child
        pid_t pid2 = fork();

        if (pid2 == 0) {
            // Grandchild - will be adopted by init
            setsid();  // New session
            // Do daemon work...
            while (1) {
                sleep(10);
            }
        }
        // First child exits immediately
        exit(0);
    }

    // Parent waits for first child only
    wait(NULL);  // Quick reap
    // Grandchild is now orphaned and adopted by init
}
```

---

## Orphan Processes and Adoption

```c
// Creating an orphan
if (fork() == 0) {
    // Child
    printf("Original parent: %d\n", getppid());
    sleep(5);  // Wait for parent to die
    printf("New parent: %d\n", getppid());  // Will be 1
    // Continue running as orphan...
}
// Parent exits immediately
exit(0);

// Orphan characteristics:
// - Parent died before child
// - Adopted by init (PID 1) or subreaper
// - Init will wait() for it
// - No zombie problem
```

---

## Fork Performance

## vfork() - Optimized Fork:

```c
// vfork() shares parent's memory
pid_t pid = vfork();

if (pid == 0) {
    // Child runs in parent's address space!
    // ONLY call exec() or _exit()
    execl("/bin/ls", "ls", NULL);
    _exit(1);  // Not exit()!
}
// Parent blocked until child execs or exits

// Benefits:
// - No COW overhead
// - Faster for fork+exec pattern
// Dangers:
// - Shared memory corruption
// - Must be very careful
```

---

## exec() Family - Program Replacement

```c
// Six variants of exec
int execl(const char *path, const char *arg, ...);
int execlp(const char *file, const char *arg, ...);
int execle(const char *path, const char *arg, ..., char *envp[]);
int execv(const char *path, char *const argv[]);
int execvp(const char *file, char *const argv[]);
int execve(const char *filename, char *const argv[], char *const envp[]);

// Examples:
execl("/bin/ls", "ls", "-l", "/tmp", NULL);

char *args[] = {"ls", "-l", "/tmp", NULL};
execv("/bin/ls", args);

// Search PATH
execlp("python3", "python3", "script.py", NULL);

// Custom environment
char *env[] = {"PATH=/bin", "USER=test", NULL};
execle("/bin/sh", "sh", "-c", "env", NULL, env);
```

---

## Fork-Exec Pattern

```c
void run_command(const char *cmd) {
    pid_t pid = fork();

    if (pid == 0) {
        // Child: redirect and exec

        // Redirect stdout to file
        int fd = open("output.txt",
                     O_WRONLY | O_CREAT | O_TRUNC, 0644);
        dup2(fd, STDOUT_FILENO);
        close(fd);

        // Close unused file descriptors
        for (int i = 3; i < 1024; i++) {
            close(i);
        }

        // Execute command
        execl("/bin/sh", "sh", "-c", cmd, NULL);
        perror("execl");
        _exit(127);
    }

    // Parent waits
    int status;
    waitpid(pid, &status, 0);
}
```

---

## system() and popen()

```c
// system() - Simple but limited
int ret = system("ls -l | grep '.txt'");
if (ret == -1) {
    perror("system");
}

// How system() works:
// 1. fork()
// 2. execl("/bin/sh", "sh", "-c", command, NULL)
// 3. wait()

// popen() - Read command output
FILE *fp = popen("ps aux", "r");
char line[256];
while (fgets(line, sizeof(line), fp)) {
    printf("Output: %s", line);
}
int status = pclose(fp);

// Security warning: Shell injection!
char cmd[256];
sprintf(cmd, "grep %s file.txt", user_input);  // DANGEROUS!
system(cmd);
```

---

## Shell Implementation Basics

```c
// Simple shell loop
void simple_shell() {
    char line[1024];
    while (1) {
        printf("$ ");
        if (!fgets(line, sizeof(line), stdin)) {
            break;
        }
        // Remove newline
        line[strcspn(line, "\n")] = 0;
        // Parse command
        char *args[64];
        int i = 0;
        char *token = strtok(line, " ");
        while (token && i < 63) {
            args[i++] = token;
            token = strtok(NULL, " ");
        }
        args[i] = NULL;
        if (args[0] == NULL) continue;
        // Built-in commands
        if (strcmp(args[0], "exit") == 0) {
            break;
        }
        if (strcmp(args[0], "cd") == 0) {
            chdir(args[1] ? args[1] : getenv("HOME"));
            continue;
        }
        // External command
        if (fork() == 0) {
            execvp(args[0], args);
            perror(args[0]);
            exit(127);
        }
        wait(NULL);
    }
}
```
