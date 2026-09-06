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

# Real Time Signals

---

## The Problem with Standard Signals

1. Standard signals (like `SIGINT`, `SIGTERM`) were designed for simple notifications.
1. They lack features needed for complex, real-time applications.
1. Let's review the main limitations.

---

## Limitation 1: Lack of Reliability

1. Standard signals are not queued.
1. If multiple instances of the same signal are sent to a process before it can handle them, the signals are merged.
1. The process only receives the signal once. This is unreliable for event counting.

---

## Standard Signal Merging

![standard_signal_merging](svg/courses/operating_systems/linux-systems-programming/08_real_time_signals/standard_signal_merging.svg)

---

## Limitation 2: No Prioritization

1. Standard signals do not have a defined delivery order.
1. If multiple different signals are pending, the kernel can deliver them in any order.
1. This is problematic when the order of events matters.

---

## Limitation 3: No Associated Data

1. A standard signal is just a number.
1. There is no standard way to send a payload or context along with the signal.
1. This makes it difficult to convey information beyond the event type itself.

---

## The Solution: Real-Time Signals

1. To address these limitations, POSIX introduced real-time signals.
1. They are designed to be a reliable, queued, and data-carrying signaling mechanism.
1. They are a range of signals from `SIGRTMIN` to `SIGRTMAX`.

---

## Feature 1: Queuing

1. Real-time signals are queued.
1. If multiple instances of the same real-time signal are sent, they are delivered multiple times.
1. No signals are lost (up to a system limit).

---

## Real-Time Signal Queuing

![real_time_signal_queuing](svg/courses/operating_systems/linux-systems-programming/08_real_time_signals/real_time_signal_queuing.svg)

---

## Feature 2: Prioritization

1. Real-time signals are delivered in a guaranteed order.
1. Signals with lower numbers have higher priority.
    - `SIGRTMIN` has higher priority than `SIGRTMIN+1`.
1. For signals of the same number, they are delivered in the order they were sent (FIFO).

---

## Feature 3: Associated Data

1. A real-time signal can carry a small payload.
1. This payload can be an integer or a pointer.
1. The data is delivered to the signal handler as part of the `siginfo_t` structure.

---

## Signal Ranges

1. Standard signals have fixed numbers (1-31).
1. Real-time signals occupy a range.
    - Use `SIGRTMIN` and `SIGRTMAX` to determine the range on a given system.
    - You can check their values with `kill -l`.

---

## Getting the RT Signal Range

You can find the numeric values for `SIGRTMIN` and `SIGRTMAX` on your system programmatically.

```c
#include <stdio.h>
#include <signal.h>

int main(void) {
    printf("SIGRTMIN = %d\n", SIGRTMIN);
    printf("SIGRTMAX = %d\n", SIGRTMAX);
    return 0;
}
```

---

## Sending Real-Time Signals

1. The standard `kill(2)` can send a real-time signal, but without data.
1. To send a real-time signal with data, you must use `sigqueue(2)`.

---

## The `sigqueue(2)` System Call

```c
#include <signal.h>

int sigqueue(pid_t pid, int sig, const union sigval value);
```

1. `pid`: The process ID to send the signal to.
1. `sig`: The signal number (must be a real-time signal).
1. `value`: The data payload to send.

---

## The `sigval` Union

The `value` parameter is of type `union sigval`.

```c
union sigval {
    int   sival_int;
    void *sival_ptr;
};
```

1. You can send either an integer (`sival_int`) or a pointer (`sival_ptr`).
1. Remember: if you send a pointer, the memory it points to must be valid in the receiving process's address space.

---

## `sigqueue(2)` Example: Sending an Integer

```c
#include <signal.h>
#include <unistd.h>

void send_rt_signal(pid_t target_pid) {
    union sigval val;
    val.sival_int = 12345; // Our data payload

    if (sigqueue(target_pid, SIGRTMIN, val) == -1) {
        perror("sigqueue");
    }
}
```

---

## Handling Real-Time Signals

1. To handle real-time signals and access their data, you must use the `sigaction(2)` system call.
1. You must set the `SA_SIGINFO` flag in `sa_flags`.
1. This tells the kernel to use the three-argument version of the signal handler.

---

## The `SA_SIGINFO` Handler

When `SA_SIGINFO` is used, the handler has this prototype:

```c
void handler(int sig, siginfo_t *info, void *ucontext);
```

1. `sig`: The signal number.
1. `info`: A pointer to a `siginfo_t` structure containing detailed information about the signal.
1. `ucontext`: A pointer to a `ucontext_t` structure (rarely used).

---

## The `siginfo_t` Structure

This structure contains a wealth of information. For `sigqueue(2)`, we care about:

```c
typedef struct {
    int      si_signo;  // Signal number
    int      si_errno;  // An errno value
    int      si_code;   // Signal code
    pid_t    si_pid;    // Sending process ID
    uid_t    si_uid;    // Real user ID of sending process
    union sigval si_value; // The value passed to sigqueue()
} siginfo_t;
```

---

## Setting up the Handler

```c
#include <signal.h>
#include <stdio.h>
#include <unistd.h>

void rt_handler(int sig, siginfo_t *info, void *ucontext) {
    printf("Caught signal %d\n", sig);
    printf("Payload (integer): %d\n", info->si_value.sival_int);
    printf("Sent by PID: %d\n", info->si_pid);
}
```

---

## Registering the Handler with `sigaction`

```c
void setup_handler(void) {
    struct sigaction sa;

    // Use the sa_sigaction field, not sa_handler
    sa.sa_sigaction = rt_handler;

    // Set the SA_SIGINFO flag
    sa.sa_flags = SA_SIGINFO;

    // It's good practice to initialize the signal mask
    sigemptyset(&sa.sa_mask);

    if (sigaction(SIGRTMIN, &sa, NULL) == -1) {
        perror("sigaction");
    }
}
```

---

## Queue Limits

1. There is a limit to how many real-time signals can be queued for a process.
1. This limit is defined by `RLIMIT_SIGPENDING`.
1. If the queue is full, `sigqueue(2)` will fail with `errno` set to `EAGAIN`.

---

## Checking `RLIMIT_SIGPENDING`

You can check the limit using `getrlimit(2)`.

```c
#include <stdio.h>
#include <sys/resource.h>

int main(void) {
    struct rlimit rl;
    if (getrlimit(RLIMIT_SIGPENDING, &rl) == 0) {
        printf("Signal queue limit: %ld\n", rl.rlim_cur);
    }
    return 0;
}
```

---

## Use Cases for Real-Time Signals

1. **Asynchronous I/O (AIO):** The kernel uses real-time signals (`SIGRTMIN+1`) by default to notify a process that an AIO operation has completed.
1. **POSIX Timers:** `timer_create(2)` can be configured to deliver a signal upon timer expiration.
1. **Lightweight IPC:** Can be used for simple, prioritized event notification between processes.

---

## Standard vs. Real-Time Signals: A Summary

| Feature | Standard Signals | Real-Time Signals |
| :--- | :--- | :--- |
| **Reliability** | Unreliable (merged) | Reliable (queued) |
| **Ordering** | No guaranteed order | Prioritized & FIFO |
| **Data** | No | Yes (int or pointer) |
| **Range** | 1 to 31 | `SIGRTMIN` to `SIGRTMAX` |
| **Sending** | `kill(2)` | `sigqueue(2)` |
| **Handling** | `signal(2)`, `sigaction(2)` | `sigaction(2)` with `SA_SIGINFO` |

---

## Example: A Simple Queueing System

1. A server process sets up a handler for `SIGRTMIN`.
1. Multiple client processes send `SIGRTMIN` signals to the server using `sigqueue(2)`.
1. Each client sends its PID as the integer payload.
1. The server's handler processes the requests in the order they were received.

---

## Example: Server Code Snippet

```c
void handler(int sig, siginfo_t *info, void *ucontext) {
    // In a real app, add this request to a work queue
    printf("Received request from client PID %d\n",
           info->si_value.sival_int);
}

void main() {
    struct sigaction sa;
    sa.sa_sigaction = handler;
    sa.sa_flags = SA_SIGINFO;
    sigemptyset(&sa.sa_mask);
    sigaction(SIGRTMIN, &sa, NULL);

    printf("Server PID %d waiting for signals...\n", getpid());
    while(1) {
        pause(); // Wait for a signal
    }
}
```

---

## Example: Client Code Snippet

```c
void main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <server_pid>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    pid_t server_pid = atoi(argv[1]);

    union sigval value;
    value.sival_int = getpid(); // Send our own PID

    printf("Client %d sending signal to server %d\n", getpid(), server_pid);
    sigqueue(server_pid, SIGRTMIN, value);
}
```

---

## Considerations and Pitfalls

1. **Pointer Payloads:** Sending pointers is tricky. The pointed-to memory must be accessible to the receiver (e.g., shared memory).
1. **Queue Overflow:** Always check the return value of `sigqueue(2)` for `EAGAIN`. Implement a backoff or retry mechanism if the queue is full.
1. **Portability:** The number of available real-time signals can vary between `UNIX`-like systems. Use `SIGRTMIN` and `SIGRTMAX` and don't hardcode signal numbers.

---

## Real-Time Signals and Threads

1. In a multi-threaded process, a real-time signal is delivered to the process, not a specific thread.
1. The kernel will choose one of the threads that does not have the signal blocked to run the handler.
1. To direct signals to a specific thread, use `pthread_sigmask(3)` to block the signal in all other threads.

---

## Using `sigwaitinfo(2)`

1. Instead of using an asynchronous handler, a thread can wait for a signal synchronously.
1. `sigwaitinfo(2)` suspends execution until a signal in its specified set is delivered.
1. It returns the signal number and can also provide the `siginfo_t` structure.

---

## `sigwaitinfo(2)` Example

```c
#include <signal.h>
#include <stdio.h>

int main(void) {
    sigset_t set;
    siginfo_t info;

    sigemptyset(&set);
    sigaddset(&set, SIGRTMIN);

    // Block the signal so the handler isn't called
    pthread_sigmask(SIG_BLOCK, &set, NULL);

    printf("Waiting for SIGRTMIN...\n");
    int sig = sigwaitinfo(&set, &info);

    printf("Got signal %d with value %d from PID %d\n",
           sig, info.si_value.sival_int, info.si_pid);
    return 0;
}
```

---

## Why use `sigwaitinfo(2)`?

1. **Simplifies Control Flow:** It avoids the complexities of asynchronous signal handlers (reentrancy, signal-safe functions).
1. **Dedicated Signal Thread:** A common design pattern is to have one thread dedicated to handling all signals for the application using `sigwaitinfo(2)` in a loop.
1. This thread can then dispatch tasks to other worker threads based on the signals received.

---

## Summary of Real-Time Signals

1. They solve the key problems of standard signals: reliability, ordering, and data transfer.
1. They are **queued**, not merged.
1. They are **prioritized** by number, and **FIFO** for the same number.
1. They can carry an **integer or pointer** payload.
1. Use `sigqueue(2)` to send and `sigaction(2)` with `SA_SIGINFO` to handle.
1. They are a powerful tool for building robust real-time and event-driven applications in `Linux`.

---

## Chapter Summary

1. We identified the limitations of standard signals for complex applications.
1. We introduced real-time signals as the POSIX solution.
1. We explored their key features: queuing, prioritization, and data payloads.
1. We learned the APIs for sending (`sigqueue`) and handling (`sigaction` with `SA_SIGINFO`).
1. We discussed practical use cases and advanced techniques like `sigwaitinfo`.
