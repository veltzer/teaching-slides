# Signal Handling in Linux

---

## Chapter Overview

1. **Why Signals?**
1. **Signal Basics**
1. **Asynchronous Delivery Problems**
1. **Signal Safety**
1. **Signal Implementation**
1. **Synchronous Signal Handling**
1. **Advanced Signal Techniques**

---

## What are Signals?

## Definition:
- **Software interrupts** to processes
- **Asynchronous notifications** of events
- **IPC mechanism** between processes
- **Default actions** or custom handlers
- **Cannot be ignored** (mostly)

Like hardware interrupts but for processes!

---

## Why Signals?

## Use Cases:

1. **Process control** - Stop, continue, terminate
1. **Error notification** - Segfault, illegal instruction
1. **User interaction** - Ctrl+C, Ctrl+Z
1. **Timers** - Alarms, intervals
1. **IPC** - Process communication
1. **Resource limits** - CPU, file size
1. **Child events** - Exit, stop

---

## Signal Types

![signal_types](svg/courses/operating_systems/linux-systems-programming/07_signals/signal_types.svg)

---

## Standard Signals List

```c
// Common signals (first 31)
#define SIGHUP    1   // Hangup (terminal disconnected)
#define SIGINT    2   // Interrupt (Ctrl+C)
#define SIGQUIT   3   // Quit (Ctrl+\)
#define SIGILL    4   // Illegal instruction
#define SIGTRAP   5   // Trace/breakpoint trap
#define SIGABRT   6   // Abort (abort())
#define SIGBUS    7   // Bus error
#define SIGFPE    8   // Floating point exception
#define SIGKILL   9   // Kill (cannot catch)
#define SIGUSR1   10  // User-defined 1
#define SIGSEGV   11  // Segmentation fault
#define SIGUSR2   12  // User-defined 2
#define SIGPIPE   13  // Broken pipe
#define SIGALRM   14  // Alarm clock
#define SIGTERM   15  // Termination
#define SIGCHLD   17  // Child status changed
#define SIGCONT   18  // Continue
#define SIGSTOP   19  // Stop (cannot catch)
#define SIGTSTP   20  // Terminal stop (Ctrl+Z)
```

---

## Signal Default Actions

| Action | Description | Signals |
|--------|-------------|---------|
| **Term** | Terminate process | SIGTERM, SIGINT, SIGHUP |
| **Core** | Terminate + core dump | SIGSEGV, SIGQUIT, SIGILL |
| **Ign** | Ignore signal | SIGCHLD, SIGURG |
| **Stop** | Stop process | SIGSTOP, SIGTSTP |
| **Cont** | Continue if stopped | SIGCONT |

```bash
# Check signal defaults
man 7 signal
```

---

## Basic Signal Handling

```c
#include <signal.h>

// Signal handler function
void handler(int signum) {
    printf("Caught signal %d\n", signum);
    // DANGER: printf is not signal-safe!
}

int main() {
    // Install handler
    signal(SIGINT, handler);

    // Special handlers
    signal(SIGUSR1, SIG_IGN);  // Ignore
    signal(SIGUSR2, SIG_DFL);  // Default action

    // Wait for signals
    while (1) {
        pause();  // Sleep until signal
    }
}
```

---

## Problems with signal()

## Issues:

1. **Unreliable** on old systems
1. **Race conditions**
1. **Different semantics** across UNIX variants
1. **Handler reset** on some systems
1. **No signal masking** during handler

## Solution: Use sigaction()!

---

## sigaction() - Reliable Signals

```c
#include <signal.h>

void handler(int sig, siginfo_t *info, void *ucontext) {
    // Extended handler with more info
    write(STDOUT_FILENO, "Signal!\n", 8);  // Signal-safe
}

int main() {
    struct sigaction sa;

    // Setup handler
    sa.sa_sigaction = handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_SIGINFO | SA_RESTART;

    // Install handler
    if (sigaction(SIGINT, &sa, NULL) == -1) {
        perror("sigaction");
    }

    while (1) pause();
}
```

---

## sigaction Structure

```c
struct sigaction {
    void (*sa_handler)(int);           // Simple handler
    void (*sa_sigaction)(int, siginfo_t *, void *); // Extended
    sigset_t sa_mask;                  // Signals to block
    int sa_flags;                      // Flags
    void (*sa_restorer)(void);         // Obsolete
};

// Flags:
SA_RESTART    // Restart interrupted system calls
SA_SIGINFO    // Use sa_sigaction with extra info
SA_NODEFER    // Don't block signal during handler
SA_RESETHAND  // Reset to SIG_DFL after handling
SA_NOCLDSTOP  // Don't signal for child stop
SA_NOCLDWAIT  // Don't create zombies
```

---

## Signal Sets and Masking

```c
#include <signal.h>

// Signal set operations
sigset_t set, oldset;

sigemptyset(&set);           // Clear all
sigfillset(&set);            // Set all
sigaddset(&set, SIGINT);     // Add signal
sigdelset(&set, SIGINT);     // Remove signal
sigismember(&set, SIGINT);   // Test membership

// Block/unblock signals
sigprocmask(SIG_BLOCK, &set, &oldset);    // Block
sigprocmask(SIG_UNBLOCK, &set, NULL);     // Unblock
sigprocmask(SIG_SETMASK, &set, NULL);     // Replace

// Check pending signals
sigset_t pending;
sigpending(&pending);
```

---

## The Async Problem

![the_async_problem](svg/courses/operating_systems/linux-systems-programming/07_signals/the_async_problem.svg)

---

## Signal-Safe Functions

## Async-Signal-Safe Functions:

```c
// SAFE in signal handlers:
write()     read()      open()      close()
dup()       dup2()      pipe()      socket()
select()    poll()      kill()      pause()
alarm()     sleep()     time()      getpid()
getppid()   getuid()    getgid()    _exit()
signal()    sigaction() sigprocmask()

// NOT SAFE:
printf()    malloc()    free()      pthread_*
fopen()     fread()     fwrite()    exit()
system()    strtok()    rand()      localtime()

// Rule: Only use functions guaranteed reentrant!
```

---

## Solving Async Problems

## Strategy 1: Self-Pipe Trick

```c
int pipefd[2];

void signal_handler(int sig) {
    char a = 1;
    // Just write one byte to pipe
    write(pipefd[1], &a, 1);
}

int main() {
    pipe(pipefd);
    signal(SIGUSR1, signal_handler);

    fd_set readfds;
    FD_ZERO(&readfds);
    FD_SET(pipefd[0], &readfds);

    // Wait for signal via pipe
    select(pipefd[0] + 1, &readfds, NULL, NULL, NULL);

    // Handle signal in main context
    if (FD_ISSET(pipefd[0], &readfds)) {
        handle_signal_safely();
    }
}
```

---

## Solving Async Problems (cont.)

## Strategy 2: Signal Masking

```c
void critical_section() {
    sigset_t newmask, oldmask;

    // Block all signals
    sigfillset(&newmask);
    sigprocmask(SIG_BLOCK, &newmask, &oldmask);

    // Critical code - no signals here
    modify_global_data();
    update_structures();

    // Restore signal mask
    sigprocmask(SIG_SETMASK, &oldmask, NULL);
}
```

---

## Solving Async Problems (cont.)

## Strategy 3: signalfd()

```c
#include <sys/signalfd.h>

int main() {
    sigset_t mask;
    int sfd;

    // Block signals normally
    sigemptyset(&mask);
    sigaddset(&mask, SIGINT);
    sigaddset(&mask, SIGTERM);
    sigprocmask(SIG_BLOCK, &mask, NULL);

    // Create signalfd
    sfd = signalfd(-1, &mask, SFD_CLOEXEC);

    // Read signals synchronously
    struct signalfd_siginfo fdsi;
    while (read(sfd, &fdsi, sizeof(fdsi)) == sizeof(fdsi)) {
        printf("Got signal %d from PID %d\n",
               fdsi.ssi_signo, fdsi.ssi_pid);
    }
}
```

---

## Signal Delivery and Queuing

![signal_delivery_and_queuing](svg/courses/operating_systems/linux-systems-programming/07_signals/signal_delivery_and_queuing.svg)

---

## How Signals are Implemented

## Kernel Implementation:

1. **Signal generation**
    - Set bit in target's pending mask
    - Wake up target if sleeping

1. **Signal delivery**
    - Check on return to user space
    - Save context on stack
    - Jump to handler

1. **Return from handler**
    - Restore saved context
    - Resume interrupted code

---

## Signal Delivery Mechanism

```c
// Kernel pseudo-code for signal delivery
void return_to_userspace() {
    if (has_pending_signals()) {
        sig = get_next_signal();

        // Save current context on user stack
        save_context(stack);

        // Setup signal frame
        setup_signal_frame(sig, handler);

        // Modify return address to handler
        set_user_pc(handler_address);
    }
}

// After handler returns:
// 1. sigreturn() system call
// 2. Restore saved context
// 3. Continue original execution
```

---

## Signal Interruption

```c
// System calls can be interrupted
ssize_t n = read(fd, buf, size);
if (n == -1) {
    if (errno == EINTR) {
        // Interrupted by signal
        // Retry or handle appropriately
    }
}

// SA_RESTART flag auto-restarts:
struct sigaction sa;
sa.sa_flags = SA_RESTART;
sigaction(SIGINT, &sa, NULL);

// Now read() will automatically restart
```

---

## SIGCHLD Handling

```c
// Proper SIGCHLD handler to reap children
void sigchld_handler(int sig) {
    int saved_errno = errno;  // Save errno
    int status;
    pid_t pid;

    // Reap all available children
    while ((pid = waitpid(-1, &status, WNOHANG)) > 0) {
        // Log child exit (use write, not printf!)
        char msg[] = "Child exited\n";
        write(STDOUT_FILENO, msg, sizeof(msg)-1);
    }

    errno = saved_errno;  // Restore errno
}

int main() {
    struct sigaction sa;
    sa.sa_handler = sigchld_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;
    sigaction(SIGCHLD, &sa, NULL);
}
```

---

## Jumping Out of Signal Context

```c
#include <setjmp.h>

jmp_buf env;

void signal_handler(int sig) {
    // Jump back to main context
    longjmp(env, 1);
}

int main() {
    signal(SIGINT, signal_handler);

    if (setjmp(env) == 0) {
        // Normal execution
        while (1) {
            do_work();
        }
    } else {
        // Jumped here from signal
        printf("Interrupted!\n");
        cleanup();
    }
}

// Warning: Use siglongjmp/sigsetjmp for signals!
```

---

## Sending Signals

```c
#include <signal.h>

// Send to process
kill(pid, SIGTERM);

// Send to self
raise(SIGTERM);
// or
kill(getpid(), SIGTERM);

// Send to process group
kill(-pgid, SIGTERM);

// Send to all processes (except init)
kill(-1, SIGTERM);  // Requires privilege

// Send with data (real-time)
union sigval value;
value.sival_int = 42;
sigqueue(pid, SIGRTMIN, value);

// Check if process exists
if (kill(pid, 0) == -1) {
    if (errno == ESRCH) {
        // Process doesn't exist
    }
}
```

---

## Signal Info Structure

```c
// Extended signal information
typedef struct {
    int si_signo;     // Signal number
    int si_errno;     // Error number
    int si_code;      // Signal code
    pid_t si_pid;     // Sending process ID
    uid_t si_uid;     // Real user ID of sending process
    int si_status;    // Exit value or signal
    clock_t si_utime; // User time consumed
    clock_t si_stime; // System time consumed
    sigval_t si_value;// Signal value
    int si_int;       // Integer value
    void *si_ptr;     // Pointer value
    void *si_addr;    // Memory location (SIGSEGV)
    int si_band;      // Band event
    int si_fd;        // File descriptor
} siginfo_t;

// Access in SA_SIGINFO handler
void handler(int sig, siginfo_t *info, void *context) {
    printf("Signal %d from PID %d\n", sig, info->si_pid);
}
```

---

## Alarm and Timers

```c
#include <unistd.h>
#include <signal.h>

// Simple alarm
alarm(5);  // SIGALRM in 5 seconds

// Cancel alarm
alarm(0);

// Interval timer
#include <sys/time.h>

struct itimerval timer;
timer.it_value.tv_sec = 5;     // Initial
timer.it_value.tv_usec = 0;
timer.it_interval.tv_sec = 1;  // Repeat
timer.it_interval.tv_usec = 0;

setitimer(ITIMER_REAL, &timer, NULL);  // SIGALRM

// Timer types:
// ITIMER_REAL - Wall clock time (SIGALRM)
// ITIMER_VIRTUAL - Process time (SIGVTALRM)
// ITIMER_PROF - Process + system time (SIGPROF)
```

---

## pause() and sigsuspend()

```c
// Wait for any signal
pause();  // Returns -1 with errno = EINTR

// Atomic mask change and wait
sigset_t mask, oldmask;

// Block SIGINT while waiting
sigemptyset(&mask);
sigaddset(&mask, SIGINT);
sigprocmask(SIG_BLOCK, &mask, &oldmask);

// Atomically unblock and wait
sigsuspend(&oldmask);  // Race-free!

// Better than:
sigprocmask(SIG_SETMASK, &oldmask, NULL);
pause();  // RACE: Signal can arrive here!
```

---

## Signal Stack

```c
#include <signal.h>

// Alternate signal stack for handling stack overflow
char altstack[SIGSTKSZ];

stack_t ss;
ss.ss_sp = altstack;
ss.ss_size = SIGSTKSZ;
ss.ss_flags = 0;

// Set alternate stack
if (sigaltstack(&ss, NULL) == -1) {
    perror("sigaltstack");
}

// Use alternate stack for SIGSEGV
struct sigaction sa;
sa.sa_flags = SA_ONSTACK;  // Use alternate stack
sa.sa_handler = segv_handler;
sigaction(SIGSEGV, &sa, NULL);
```

---

## Real-Time Signal Priority

```c
// Real-time signals have priority
// Lower signal numbers = higher priority

void send_rt_signals(pid_t target) {
    union sigval val;

    // Send multiple RT signals
    val.sival_int = 1;
    sigqueue(target, SIGRTMIN + 5, val);

    val.sival_int = 2;
    sigqueue(target, SIGRTMIN + 2, val);

    val.sival_int = 3;
    sigqueue(target, SIGRTMIN + 8, val);

    // Delivery order: SIGRTMIN+2, +5, +8
    // (lower number = higher priority)
}

// Handler for RT signals
void rt_handler(int sig, siginfo_t *info, void *ctx) {
    printf("RT signal %d, value %d\n",
           sig, info->si_value.sival_int);
}
```

---

## Signal Handling in Threads

```c
#include <pthread.h>
#include <signal.h>

// Signals are process-wide
// But each thread has its own signal mask

void *thread_func(void *arg) {
    sigset_t set;

    // Block SIGINT in this thread
    sigemptyset(&set);
    sigaddset(&set, SIGINT);
    pthread_sigmask(SIG_BLOCK, &set, NULL);

    // Thread work...
}

// Dedicated signal handling thread
void *signal_thread(void *arg) {
    sigset_t set;
    int sig;

    // Wait for signals
    sigemptyset(&set);
    sigaddset(&set, SIGINT);
    sigaddset(&set, SIGTERM);

    while (1) {
        sigwait(&set, &sig);  // Synchronous wait
        printf("Got signal %d\n", sig);
    }
}
```

---

## Common Signal Patterns

## Pattern 1: Graceful Shutdown

```c
volatile sig_atomic_t shutdown_flag = 0;

void term_handler(int sig) {
    shutdown_flag = 1;
}

int main() {
    signal(SIGTERM, term_handler);
    signal(SIGINT, term_handler);

    while (!shutdown_flag) {
        do_work();
    }

    cleanup();
    printf("Graceful shutdown complete\n");
}
```

---

## Common Signal Patterns (cont.)

## Pattern 2: Configuration Reload

```c
volatile sig_atomic_t reload_config = 0;

void hup_handler(int sig) {
    reload_config = 1;
}

int main() {
    signal(SIGHUP, hup_handler);
    load_config();

    while (1) {
        if (reload_config) {
            reload_config = 0;
            printf("Reloading configuration\n");
            load_config();
        }
        do_work();
    }
}
```

---

## Signal Debugging

```bash
# Send signals
kill -TERM 1234
kill -USR1 1234
killall -HUP nginx

# List signals
kill -l

# Monitor signals
strace -e signal ./program

# Check signal mask
cat /proc/$$/status | grep Sig

# Signal information
cat /proc/$$/status | grep -E "Sig|Shd"
# SigQ:   2/15337  (queued/limit)
# SigPnd: 0000000000000000
# ShdPnd: 0000000000000000
# SigBlk: 0000000000000000
# SigIgn: 0000000000000000
# SigCgt: 0000000000000002
```

---

## Signal Race Conditions

```c
// RACE CONDITION: Child might die before handler installed
pid_t pid = fork();
if (pid > 0) {
    // Parent
    signal(SIGCHLD, sigchld_handler);  // RACE!
    // Child might exit here
}

// SOLUTION: Install handler first
signal(SIGCHLD, sigchld_handler);
pid_t pid = fork();

// Or block signal during critical section
sigset_t set, oldset;
sigemptyset(&set);
sigaddset(&set, SIGCHLD);
sigprocmask(SIG_BLOCK, &set, &oldset);

pid = fork();
if (pid > 0) {
    // Setup complete
    sigprocmask(SIG_SETMASK, &oldset, NULL);
}
```

---

## Signal Safety Rules

## Best Practices:

1. **Keep handlers simple**
    - Set flags only
    - Minimal code

1. **Use signal-safe functions only**
    - write() not printf()
    - No malloc/free

1. **Save and restore errno**

1. **Use volatile sig_atomic_t** for flags

1. **Block signals** during critical sections

1. **Prefer synchronous** handling (signalfd, sigwait)

---

## Modern Signal Handling

```c
// Modern approach: epoll with signalfd
int setup_signal_handling() {
    sigset_t mask;
    int sfd, epfd;

    // Block signals
    sigemptyset(&mask);
    sigaddset(&mask, SIGINT);
    sigaddset(&mask, SIGTERM);
    sigprocmask(SIG_BLOCK, &mask, NULL);

    // Create signalfd
    sfd = signalfd(-1, &mask, SFD_CLOEXEC);

    // Add to epoll
    epfd = epoll_create1(EPOLL_CLOEXEC);

    struct epoll_event ev;
    ev.events = EPOLLIN;
    ev.data.fd = sfd;
    epoll_ctl(epfd, EPOLL_CTL_ADD, sfd, &ev);

    return epfd;
}
```

---

## Signal Handling in Real-Time Linux

## RT Considerations:

```c
// Real-time systems need predictable signal handling

// 1. Use real-time signals for priority
sigqueue(pid, SIGRTMIN + priority, value);

// 2. Dedicated signal handling thread
cpu_set_t cpuset;
CPU_ZERO(&cpuset);
CPU_SET(3, &cpuset);  // Dedicated CPU
pthread_setaffinity_np(signal_thread,
                      sizeof(cpuset), &cpuset);

// 3. Minimize handler latency
struct sigaction sa;
sa.sa_flags = SA_NODEFER;  // Don't block signal
```

---

## Common Signal Bugs

## 1. Non-reentrant Functions
```c
// BAD: printf in handler
void handler(int sig) {
    printf("Signal %d\n", sig);  // NOT SAFE!
}
```

## 2. Race Conditions
```c
// BAD: Check-then-act
if (!flag) {  // Signal can arrive here!
    flag = 1;
}
```

## 3. Forgetting errno
```c
// BAD: errno corrupted
void handler(int sig) {
    write(1, "sig", 3);  // Changes errno!
}
```

---

## Signal Use Cases

## Common Applications:

1. **Daemon reload** - SIGHUP for config
1. **Graceful shutdown** - SIGTERM/SIGINT
1. **Process monitoring** - SIGCHLD
1. **Debugging** - SIGUSR1/2 for state dump
1. **Resource limits** - SIGXCPU, SIGXFSZ
1. **Job control** - SIGTSTP, SIGCONT
1. **Profiling** - SIGPROF
1. **Cleanup** - SIGPIPE, SIGSEGV recovery

---

## Performance Considerations

```c
// Signal delivery overhead
// Approximate costs:

// Signal delivery: ~2-5 microseconds
// Context switch: ~1-2 microseconds
// Handler execution: varies

// Minimize signal frequency
// Use signalfd/epoll for high-frequency signals

// Batch signal handling
volatile sig_atomic_t signal_count = 0;

void handler(int sig) {
    signal_count++;  // Just count
}

// Process in main loop
while (1) {
    if (signal_count) {
        int count = signal_count;
        signal_count = 0;
        process_signals(count);
    }
    do_work();
}
```

---

## Signal Handling Best Practices

1. **Use sigaction()** not signal()

1. **Keep handlers minimal**

1. **Use synchronous handling** when possible

1. **Document signal usage**

1. **Test signal handling** thoroughly

1. **Handle EINTR** in system calls

1. **Avoid signal races** with proper masking

---

## Summary

## Key Takeaways:

- **Signals** are asynchronous notifications
- **Safety** is critical in handlers
- **Race conditions** are common pitfalls
- **Synchronous** handling preferred
- **Real-time signals** offer queuing
- **Modern approaches** use signalfd/epoll
- **Testing** signal code is essential

Master signals = Robust applications!
