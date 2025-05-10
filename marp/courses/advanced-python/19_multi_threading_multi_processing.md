# Multi-Threading and Multi-Processing

---

## Introduction to Concurrent Programming

- Concurrent programming: multiple computations executing during overlapping time periods
- Parallelism: multiple computations executing simultaneously
- Enables better resource utilization
- Critical for modern software performance
- Leverages multi-core/multi-processor architectures

---

## Concurrency vs. Parallelism

- Concurrency: dealing with multiple things at once
- Parallelism: doing multiple things at once
- Concurrency is about structure
- Parallelism is about execution

<svg viewBox="0 0 500 200">
  <rect x="50" y="40" width="180" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="50" y="80" width="180" height="30" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="50" y="120" width="180" height="30" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <text x="140" y="60" text-anchor="middle" font-family="sans-serif">Task A</text>
  <text x="140" y="100" text-anchor="middle" font-family="sans-serif">Task B</text>
  <text x="140" y="140" text-anchor="middle" font-family="sans-serif">Task C</text>
  <text x="140" y="180" text-anchor="middle" font-family="sans-serif">Concurrent (Single Core)</text>
  <rect x="270" y="40" width="180" height="110" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="270" y="40" width="60" height="110" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="330" y="40" width="60" height="110" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="390" y="40" width="60" height="110" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <text x="300" y="100" text-anchor="middle" font-family="sans-serif" font-size="12">Task A</text>
  <text x="360" y="100" text-anchor="middle" font-family="sans-serif" font-size="12">Task B</text>
  <text x="420" y="100" text-anchor="middle" font-family="sans-serif" font-size="12">Task C</text>
  <text x="360" y="180" text-anchor="middle" font-family="sans-serif">Parallel (Multi-Core)</text>
</svg>

---

## Processes vs. Threads

- Process:
    1. Independent execution unit
    1. Has its own memory space
    1. Heavyweight, more resource intensive
- Thread:
    1. Lightweight execution unit within a process
    1. Shares process memory space
    1. Lighter weight, less resource intensive

---

## Process Characteristics

- Has its own virtual address space
- Contains one or more threads
- Isolated from other processes
- Communication requires IPC mechanisms
- Protected by the operating system
- Includes code, data, heap, stack segments

---

## Thread Characteristics

- Shares process resources
- Has its own:
    1. Program counter
    1. Registers
    1. Stack
    1. Thread-local storage
- Cheaper to create than processes
- Easier to communicate within threads

<svg viewBox="0 0 500 250">
  <rect x="50" y="30" width="400" height="200" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <text x="250" y="50" text-anchor="middle" font-family="sans-serif">Process</text>
  <rect x="70" y="60" width="110" height="150" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="190" y="60" width="110" height="150" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="310" y="60" width="110" height="150" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="125" y="80" text-anchor="middle" font-family="sans-serif" font-size="14">Thread 1</text>
  <text x="245" y="80" text-anchor="middle" font-family="sans-serif" font-size="14">Thread 2</text>
  <text x="365" y="80" text-anchor="middle" font-family="sans-serif" font-size="14">Thread 3</text>
  <rect x="80" y="90" width="90" height="30" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <rect x="200" y="90" width="90" height="30" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <rect x="320" y="90" width="90" height="30" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <text x="125" y="110" text-anchor="middle" font-family="sans-serif" font-size="10">Stack</text>
  <text x="245" y="110" text-anchor="middle" font-family="sans-serif" font-size="10">Stack</text>
  <text x="365" y="110" text-anchor="middle" font-family="sans-serif" font-size="10">Stack</text>
  <rect x="80" y="130" width="90" height="30" fill="#fff0e0" stroke="#000" stroke-width="2"/>
  <rect x="200" y="130" width="90" height="30" fill="#fff0e0" stroke="#000" stroke-width="2"/>
  <rect x="320" y="130" width="90" height="30" fill="#fff0e0" stroke="#000" stroke-width="2"/>
  <text x="125" y="150" text-anchor="middle" font-family="sans-serif" font-size="10">Registers</text>
  <text x="245" y="150" text-anchor="middle" font-family="sans-serif" font-size="10">Registers</text>
  <text x="365" y="150" text-anchor="middle" font-family="sans-serif" font-size="10">Registers</text>
  <rect x="80" y="170" width="90" height="30" fill="#f0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="200" y="170" width="90" height="30" fill="#f0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="320" y="170" width="90" height="30" fill="#f0e0ff" stroke="#000" stroke-width="2"/>
  <text x="125" y="190" text-anchor="middle" font-family="sans-serif" font-size="10">Thread-Local</text>
  <text x="245" y="190" text-anchor="middle" font-family="sans-serif" font-size="10">Thread-Local</text>
  <text x="365" y="190" text-anchor="middle" font-family="sans-serif" font-size="10">Thread-Local</text>
  <rect x="70" y="220" width="350" height="20" fill="#e0ffff" stroke="#000" stroke-width="2"/>
  <text x="245" y="235" text-anchor="middle" font-family="sans-serif" font-size="14">Shared Resources (Code, Data, Files)</text>
</svg>

---

## Multi-Threading Benefits

- Improved responsiveness
- Resource sharing
- Economy (cheaper than multiple processes)
- Scalability on multi-core systems
- Better performance for certain tasks
- Enhanced throughput

---

## Multi-Threading Challenges

- Increased complexity
- Synchronization issues
- Race conditions
- Deadlocks and livelocks
- Debugging difficulty
- Non-deterministic behavior
- Cache coherency overhead

---

## Thread APIs Overview

- POSIX Threads (pthreads)
- C++11 std::thread
- Java Thread class
- .NET ThreadPool
- Python threading module
- Go goroutines

---

## POSIX Threads (pthreads)

- Standard C library for thread management
- `pthread_create()` - create new thread
- `pthread_join()` - wait for thread completion
- `pthread_exit()` - terminate calling thread
- `pthread_cancel()` - request thread cancellation
- `pthread_self()` - get thread ID

```c
#include <pthread.h>

void *thread_function(void *arg) {
    // Thread code here
    return NULL;
}

int main() {
    pthread_t thread;
    pthread_create(&thread, NULL, thread_function, NULL);
    pthread_join(thread, NULL);
    return 0;
}
```

---

## C++11 Threads

- Part of C++11 standard library
- `std::thread` class for thread management
- `std::this_thread` namespace for operations on current thread
- Automatic joining with `std::jthread` (C++20)

```cpp
#include <thread>
#include <iostream>

void thread_function() {
    // Thread code here
}

int main() {
    std::thread t(thread_function);
    t.join(); // Wait for thread completion
    return 0;
}
```

---

## Thread States and Lifecycle

- New: thread created but not started
- Runnable: ready for execution
- Running: currently executing
- Blocked/Waiting: temporarily inactive
- Terminated: completed execution

<svg viewBox="0 0 500 200">
  <rect x="50" y="80" width="80" height="40" rx="10" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="180" y="80" width="80" height="40" rx="10" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <rect x="310" y="80" width="80" height="40" rx="10" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="310" y="150" width="80" height="40" rx="10" fill="#fff0e0" stroke="#000" stroke-width="2"/>
  <rect x="180" y="150" width="80" height="40" rx="10" fill="#f0e0ff" stroke="#000" stroke-width="2"/>
  <text x="90" y="105" text-anchor="middle" font-family="sans-serif" font-size="12">New</text>
  <text x="220" y="105" text-anchor="middle" font-family="sans-serif" font-size="12">Runnable</text>
  <text x="350" y="105" text-anchor="middle" font-family="sans-serif" font-size="12">Running</text>
  <text x="350" y="175" text-anchor="middle" font-family="sans-serif" font-size="12">Blocked</text>
  <text x="220" y="175" text-anchor="middle" font-family="sans-serif" font-size="12">Terminated</text>
  <path d="M130,100 L180,100" stroke="#000" stroke-width="2" marker-end="url(#lifecycle-arrow)"/>
  <path d="M260,100 L310,100" stroke="#000" stroke-width="2" marker-end="url(#lifecycle-arrow)"/>
  <path d="M350,120 L350,150" stroke="#000" stroke-width="2" marker-end="url(#lifecycle-arrow)"/>
  <path d="M310,170 L260,170" stroke="#000" stroke-width="2" marker-end="url(#lifecycle-arrow)"/>
  <path d="M350,150 C350,130 290,100 260,100" stroke="#000" stroke-width="2" marker-end="url(#lifecycle-arrow)"/>
  <path d="M310,100 C290,80 260,50 240,50 C220,50 190,80 180,100" stroke="#000" stroke-width="2" marker-end="url(#lifecycle-arrow)"/>
  <defs>
    <marker id="lifecycle-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Thread Creation Parameters

- Entry point function
- Function arguments
- Thread attributes:
    1. Stack size
    1. Priority
    1. Scheduling policy
    1. Detach state

---

## Thread Termination

- Return from thread function
- Explicit termination call (`pthread_exit()`, etc.)
- Thread cancellation by another thread
- Process termination
- Handling terminated threads:
    1. Join (wait for completion)
    1. Detach (resources automatically reclaimed)

---

## Race Conditions

- Occurs when multiple threads access shared data concurrently
- Result depends on the relative timing of events
- Can lead to inconsistent/corrupt data
- Hard to reproduce and debug
- Example: counter incrementation by multiple threads

---

## Critical Sections

- Segment of code that accesses shared resources
- Only one thread should execute a critical section at a time
- Must be protected by synchronization mechanisms
- Properties:
    1. Mutual exclusion
    1. Progress
    1. Bounded waiting

<svg viewBox="0 0 500 180">
  <rect x="50" y="40" width="400" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="50" y="70" width="400" height="40" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="50" y="110" width="400" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <text x="250" y="60" text-anchor="middle" font-family="sans-serif">Non-Critical Section</text>
  <text x="250" y="95" text-anchor="middle" font-family="sans-serif">Critical Section</text>
  <text x="250" y="130" text-anchor="middle" font-family="sans-serif">Non-Critical Section</text>
  <path d="M40,70 L460,70" stroke="#000" stroke-width="2" stroke-dasharray="5,5"/>
  <path d="M40,110 L460,110" stroke="#000" stroke-width="2" stroke-dasharray="5,5"/>
  <text x="480" y="75" text-anchor="middle" font-family="sans-serif" font-size="10">lock()</text>
  <text x="480" y="105" text-anchor="middle" font-family="sans-serif" font-size="10">unlock()</text>
</svg>

---

## Synchronization Mechanisms

- Mutexes (mutual exclusion)
- Semaphores
- Condition variables
- Barriers
- Readers-writer locks
- Atomic operations
- Spinlocks

---

## Mutexes

- Basic synchronization primitive
- Protects critical sections
- Only one thread can hold a mutex at a time
- Operations:
    1. lock - acquire the mutex (wait if already locked)
    1. unlock - release the mutex
    1. trylock - non-blocking attempt to acquire

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void *thread_function(void *arg) {
    pthread_mutex_lock(&mutex);
    // Critical section here
    pthread_mutex_unlock(&mutex);
    return NULL;
}
```

---

## Semaphores

- Synchronization primitive with a counter
- Can allow multiple threads to access a resource
- Binary semaphore: permits only 0 or 1 (similar to mutex)
- Counting semaphore: permits arbitrary number
- Operations:
    1. wait (P) - decrement counter (wait if zero)
    1. post (V) - increment counter

```c
#include <semaphore.h>
sem_t semaphore;

void *thread_function(void *arg) {
    sem_wait(&semaphore);  // Wait
    // Critical section here
    sem_post(&semaphore);  // Signal
    return NULL;
}

int main() {
    sem_init(&semaphore, 0, 1);  // Initialize with value 1
    // Thread creation code...
    sem_destroy(&semaphore);
    return 0;
}
```

---

## Condition Variables

- Allow threads to wait for a condition to become true
- Used with a mutex to protect shared state
- Operations:
    1. wait - release mutex and wait for signal
    1. signal - wake up one waiting thread
    1. broadcast - wake up all waiting threads

<svg viewBox="0 0 500 200">
  <rect x="50" y="30" width="140" height="140" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <text x="120" y="50" text-anchor="middle" font-family="sans-serif">Thread 1</text>
  <rect x="310" y="30" width="140" height="140" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="380" y="50" text-anchor="middle" font-family="sans-serif">Thread 2</text>
  <rect x="70" y="60" width="100" height="100" fill="#fff" stroke="#000" stroke-width="1" stroke-dasharray="5,5"/>
  <rect x="330" y="60" width="100" height="100" fill="#fff" stroke="#000" stroke-width="1" stroke-dasharray="5,5"/>
  <text x="120" y="80" text-anchor="middle" font-family="sans-serif" font-size="10">lock(mutex)</text>
  <text x="120" y="100" text-anchor="middle" font-family="sans-serif" font-size="10">while(!condition)</text>
  <text x="120" y="120" text-anchor="middle" font-family="sans-serif" font-size="10">  wait(cond,mutex)</text>
  <text x="120" y="140" text-anchor="middle" font-family="sans-serif" font-size="10">// critical section</text>
  <text x="120" y="160" text-anchor="middle" font-family="sans-serif" font-size="10">unlock(mutex)</text>

  <text x="380" y="80" text-anchor="middle" font-family="sans-serif" font-size="10">lock(mutex)</text>
  <text x="380" y="100" text-anchor="middle" font-family="sans-serif" font-size="10">// modify condition</text>
  <text x="380" y="120" text-anchor="middle" font-family="sans-serif" font-size="10">condition = true</text>
  <text x="380" y="140" text-anchor="middle" font-family="sans-serif" font-size="10">signal(cond)</text>
  <text x="380" y="160" text-anchor="middle" font-family="sans-serif" font-size="10">unlock(mutex)</text>

  <path d="M380,145 C300,170 200,170 120,125" stroke="#000" stroke-width="2" marker-end="url(#cvar-arrow)"/>
  <defs>
    <marker id="cvar-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Barriers

- Synchronization point for a group of threads
- Threads wait at barrier until all threads arrive
- Used for algorithms with distinct phases
- All threads must reach the barrier before any can proceed

```c
#include <pthread.h>

pthread_barrier_t barrier;

void *thread_function(void *arg) {
    // Phase 1 work
    pthread_barrier_wait(&barrier);  // Wait for all threads
    // Phase 2 work
    return NULL;
}

int main() {
    pthread_barrier_init(&barrier, NULL, NUM_THREADS);
    // Thread creation code...
    pthread_barrier_destroy(&barrier);
    return 0;
}
```

---

## Deadlocks

- Situation where two or more threads are blocked forever
- Each waiting for resources held by others
- Occurs when four conditions are met:
    1. Mutual exclusion
    1. Hold and wait
    1. No preemption
    1. Circular wait

<svg viewBox="0 0 500 200">
  <rect x="50" y="30" width="160" height="60" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="290" y="30" width="160" height="60" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="50" y="120" width="160" height="60" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <rect x="290" y="120" width="160" height="60" fill="#fff0e0" stroke="#000" stroke-width="2"/>
  <text x="130" y="50" text-anchor="middle" font-family="sans-serif">Thread 1</text>
  <text x="370" y="50" text-anchor="middle" font-family="sans-serif">Thread 2</text>
  <text x="130" y="140" text-anchor="middle" font-family="sans-serif">Mutex A</text>
  <text x="370" y="140" text-anchor="middle" font-family="sans-serif">Mutex B</text>
  <text x="130" y="80" text-anchor="middle" font-family="sans-serif" font-size="12">Holds Mutex A</text>
  <text x="130" y="95" text-anchor="middle" font-family="sans-serif" font-size="12">Wants Mutex B</text>
  <text x="370" y="80" text-anchor="middle" font-family="sans-serif" font-size="12">Holds Mutex B</text>
  <text x="370" y="95" text-anchor="middle" font-family="sans-serif" font-size="12">Wants Mutex A</text>
  <path d="M130,90 C160,105 180,115 230,130 C280,145 300,155 370,140" stroke="#000" stroke-width="2" marker-end="url(#dead-arrow)"/>
  <path d="M370,90 C340,105 320,115 270,130 C220,145 200,155 130,140" stroke="#000" stroke-width="2" marker-end="url(#dead-arrow)"/>
  <defs>
    <marker id="dead-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Deadlock Prevention

- Avoiding one or more of the necessary conditions
- Resource allocation strategies:
    1. Request all resources at once
    1. Release resources before requesting new ones
    1. Order resources hierarchically
    1. Use timeouts in lock requests
    1. Deadlock detection and recovery

---

## Atomic Operations

- Operations that appear to execute instantaneously
- Indivisible - cannot be interrupted
- Implemented using hardware primitives
- Common operations:
    1. fetch-and-add
    1. compare-and-swap (CAS)
    1. test-and-set
    1. load-link/store-conditional

```cpp
#include <atomic>
std::atomic<int> counter(0);

void increment() {
    counter++;  // Atomic increment
}

void add(int val) {
    counter.fetch_add(val);  // Atomic add
}
```

---

## Thread-Local Storage

- Data specific to each thread
- Not shared between threads
- Useful for thread-specific state
- Implementation:
    1. C: `_Thread_local` or `__thread`
    1. C++: `thread_local`
    1. POSIX: pthread_key_* functions

```c
_Thread_local int thread_id;  // Each thread has its own copy

void *thread_function(void *arg) {
    thread_id = (int)(intptr_t)arg;
    printf("Thread %d running\n", thread_id);
    return NULL;
}
```

---

## Multi-Processing Overview

- Multiple processes executing concurrently
- Full memory isolation between processes
- Communication requires IPC mechanisms
- More robust against failures
- Higher overhead than threading

---

## Process Creation

- UNIX: `fork()` and `exec()`
- Windows: `CreateProcess()`
- Spawning child processes
- Parent-child relationships
- Process groups and sessions

```c
#include <unistd.h>
#include <sys/types.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // Child process
        execl("/bin/ls", "ls", "-l", NULL);
    } else if (pid > 0) {
        // Parent process
        wait(NULL);  // Wait for child to complete
    }
    return 0;
}
```

---

## Inter-Process Communication (IPC)

- Mechanisms for data exchange between processes
- Types of IPC:
    1. Pipes and FIFOs
    1. Message queues
    1. Shared memory
    1. Semaphores
    1. Sockets
    1. Memory-mapped files

<svg viewBox="0 0 500 180">
  <rect x="50" y="40" width="150" height="80" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="300" y="40" width="150" height="80" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="170" y="65" width="160" height="30" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <text x="125" y="80" text-anchor="middle" font-family="sans-serif">Process A</text>
  <text x="375" y="80" text-anchor="middle" font-family="sans-serif">Process B</text>
  <text x="250" y="85" text-anchor="middle" font-family="sans-serif">IPC Channel</text>
  <path d="M125,60 C150,40 200,30 250,50" stroke="#000" stroke-width="2" marker-end="url(#ipc-arrow)"/>
  <path d="M250,110 C200,130 150,120 125,100" stroke="#000" stroke-width="2" marker-end="url(#ipc-arrow)"/>
  <path d="M375,60 C350,40 300,30 250,50" stroke="#000" stroke-width="2" marker-end="url(#ipc-arrow)"/>
  <path d="M250,110 C300,130 350,120 375,100" stroke="#000" stroke-width="2" marker-end="url(#ipc-arrow)"/>
  <defs>
    <marker id="ipc-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Pipes and Named Pipes

- Unidirectional data channels
- Anonymous pipes: between related processes (parent-child)
- Named pipes (FIFOs): between unrelated processes
- Used for producer-consumer patterns

```c
#include <unistd.h>

int main() {
    int pipefd[2];
    pipe(pipefd);  // Create pipe

    if (fork() == 0) {
        // Child process (reader)
        close(pipefd[1]);  // Close write end
        char buffer[100];
        read(pipefd[0], buffer, sizeof(buffer));
        close(pipefd[0]);
    } else {
        // Parent process (writer)
        close(pipefd[0]);  // Close read end
        write(pipefd[1], "Hello", 5);
        close(pipefd[1]);
    }
    return 0;
}
```

---

## Message Queues

- Store messages in kernel space
- Support multiple consumers and producers
- Messages have types and priorities
- More structured than pipes
- POSIX: mq_* functions
- System V: msgget(), msgsnd(), msgrcv()

---

## Shared Memory

- Fastest IPC mechanism
- Multiple processes map the same memory region
- Direct memory access without system calls
- Requires synchronization between processes
- POSIX: shm_open(), mmap()
- System V: shmget(), shmat()

<svg viewBox="0 0 500 200">
  <rect x="50" y="40" width="400" height="50" fill="#e0ffff" stroke="#000" stroke-width="2"/>
  <text x="250" y="70" text-anchor="middle" font-family="sans-serif">Physical Memory</text>
  <rect x="50" y="120" width="150" height="60" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="300" y="120" width="150" height="60" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="100" y="140" width="50" height="30" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <rect x="350" y="140" width="50" height="30" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <text x="125" y="135" text-anchor="middle" font-family="sans-serif">Process A</text>
  <text x="375" y="135" text-anchor="middle" font-family="sans-serif">Process B</text>
  <text x="125" y="155" text-anchor="middle" font-family="sans-serif" font-size="10">Address</text>
  <text x="125" y="165" text-anchor="middle" font-family="sans-serif" font-size="10">Space</text>
  <text x="375" y="155" text-anchor="middle" font-family="sans-serif" font-size="10">Address</text>
  <text x="375" y="165" text-anchor="middle" font-family="sans-serif" font-size="10">Space</text>
  <path d="M125,140 C150,110 200,90 250,65" stroke="#000" stroke-width="2" marker-end="url(#shm-arrow)"/>
  <path d="M375,140 C350,110 300,90 250,65" stroke="#000" stroke-width="2" marker-end="url(#shm-arrow)"/>
  <defs>
    <marker id="shm-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Sockets

- Communication endpoints for networking
- Can be used between processes on same machine (Unix domain sockets)
- Support various communication protocols (TCP, UDP)
- Connection-oriented or connectionless
- Flexible and widely used IPC mechanism

```c
// Basic socket server code (abbreviated)
#include <sys/socket.h>
#include <netinet/in.h>

int server_fd = socket(AF_INET, SOCK_STREAM, 0);
// Bind, listen, accept...

// Basic socket client code (abbreviated)
int sock = socket(AF_INET, SOCK_STREAM, 0);
// Connect to server...
```

---

## Memory-Mapped Files

- Map file contents directly into process address space
- Used for file I/O and IPC
- Multiple processes can map the same file
- Efficient for large data sets
- `mmap()` system call

```c
#include <sys/mman.h>
#include <fcntl.h>

int fd = open("data.bin", O_RDWR);
void *addr = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
// Now access mapped memory directly
munmap(addr, size);  // Unmap when done
```

---

## Thread Pools

- Group of pre-created worker threads
- Tasks submitted to a work queue
- Threads take tasks from queue and execute them
- Reduces thread creation overhead
- Better resource management
- Load balancing across cores

<svg viewBox="0 0 500 200">
  <rect x="50" y="30" width="150" height="40" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <text x="125" y="55" text-anchor="middle" font-family="sans-serif">Task Queue</text>
  <rect x="60" y="40" width="20" height="20" fill="#fff" stroke="#000"/>
  <rect x="90" y="40" width="20" height="20" fill="#fff" stroke="#000"/>
  <rect x="120" y="40" width="20" height="20" fill="#fff" stroke="#000"/>
  <rect x="150" y="40" width="20" height="20" fill="#fff" stroke="#000"/>
  <rect x="50" y="90" width="400" height="80" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="250" y="110" text-anchor="middle" font-family="sans-serif">Thread Pool</text>
  <rect x="70" y="120" width="80" height="30" fill="#fff" stroke="#000" stroke-width="2"/>
  <rect x="170" y="120" width="80" height="30" fill="#fff" stroke="#000" stroke-width="2"/>
  <rect x="270" y="120" width="80" height="30" fill="#fff" stroke="#000" stroke-width="2"/>
  <rect x="370" y="120" width="60" height="30" fill="#fff" stroke="#000" stroke-width="2"/>
  <text x="110" y="140" text-anchor="middle" font-family="sans-serif" font-size="12">Worker 1</text>
  <text x="210" y="140" text-anchor="middle" font-family="sans-serif" font-size="12">Worker 2</text>
  <text x="310" y="140" text-anchor="middle" font-family="sans-serif" font-size="12">Worker 3</text>
  <text x="400" y="140" text-anchor="middle" font-family="sans-serif" font-size="12">...</text>
  <path d="M110,70 L110,120" stroke="#000" stroke-width="2" marker-end="url(#pool-arrow)"/>
  <path d="M210,30 C210,10 150,10 110,30" stroke="#000" stroke-width="2" marker-end="url(#pool-arrow)"/>
  <path d="M310,30 C310,10 200,0 110,30" stroke="#000" stroke-width="2" marker-end="url(#pool-arrow)"/>
  <defs>
    <marker id="pool-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Thread Pool Implementation

```cpp
#include <thread>
#include <mutex>
#include <condition_variable>
#include <queue>
#include <functional>
#include <vector>

class ThreadPool {
private:
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex queue_mutex;
    std::condition_variable condition;
    bool stop;

public:
    ThreadPool(size_t threads) : stop(false) {
        for (size_t i = 0; i < threads; ++i) {
            workers.emplace_back([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock<std::mutex> lock(queue_mutex);
                        condition.wait(lock, [this] {
                            return stop || !tasks.empty();
                        });
                        if (stop && tasks.empty()) return;
                        task = std::move(tasks.front());
                        tasks.pop();
                    }
                    task();
                }
            });
        }
    }

    // Add task to the pool
    template<class F>
    void enqueue(F&& f) {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            tasks.emplace(std::forward<F>(f));
        }
        condition.notify_one();
    }

    // Destructor joins all threads
    ~ThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            stop = true;
        }
        condition.notify_all();
        for (std::thread &worker : workers) {
            worker.join();
        }
    }
};
```

---

## Parallel Programming Patterns

- Task parallelism
- Data parallelism
- Pipeline parallelism
- Divide and conquer
- Map-reduce
- Producer-consumer
- Work stealing

---

## Task Parallelism

- Different tasks executed in parallel
- Tasks may be independent or with dependencies
- Suitable for heterogeneous workloads
- Focus on distributing functional units

<svg viewBox="0 0 500 180">
  <rect x="50" y="30" width="400" height="40" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <text x="250" y="55" text-anchor="middle" font-family="sans-serif">Main Program</text>
  <rect x="50" y="100" width="110" height="60" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="190" y="100" width="110" height="60" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <rect x="330" y="100" width="110" height="60" fill="#fff0e0" stroke="#000" stroke-width="2"/>
  <text x="105" y="135" text-anchor="middle" font-family="sans-serif">Task A</text>
  <text x="245" y="135" text-anchor="middle" font-family="sans-serif">Task B</text>
  <text x="385" y="135" text-anchor="middle" font-family="sans-serif">Task C</text>
  <path d="M250,70 L105,100" stroke="#000" stroke-width="2" marker-end="url(#task-arrow)"/>
  <path d="M250,70 L245,100" stroke="#000" stroke-width="2" marker-end="url(#task-arrow)"/>
  <path d="M250,70 L385,100" stroke="#000" stroke-width="2" marker-end="url(#task-arrow)"/>
  <defs>
    <marker id="task-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Data Parallelism

- Same operation applied to different data elements
- SIMD (Single Instruction Multiple Data) model
- Examples: array operations, matrix operations
- Suited for regular workloads and homogeneous data

<svg viewBox="0 0 500 180">
  <rect x="50" y="30" width="400" height="40" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <text x="250" y="55" text-anchor="middle" font-family="sans-serif">Data[]</text>
  <rect x="50" y="100" width="90" height="60" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="150" y="100" width="90" height="60" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="250" y="100" width="90" height="60" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="350" y="100" width="90" height="60" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="95" y="125" text-anchor="middle" font-family="sans-serif" font-size="12">Thread 1</text>
  <text x="95" y="145" text-anchor="middle" font-family="sans-serif" font-size="12">process()</text>
  <text x="195" y="125" text-anchor="middle" font-family="sans-serif" font-size="12">Thread 2</text>
  <text x="195" y="145" text-anchor="middle" font-family="sans-serif" font-size="12">process()</text>
  <text x="295" y="125" text-anchor="middle" font-family="sans-serif" font-size="12">Thread 3</text>
  <text x="295" y="145" text-anchor="middle" font-family="sans-serif" font-size="12">process()</text>
  <text x="395" y="125" text-anchor="middle" font-family="sans-serif" font-size="12">Thread 4</text>
  <text x="395" y="145" text-anchor="middle" font-family="sans-serif" font-size="12">process()</text>
  <path d="M90,70 L90,100" stroke="#000" stroke-width="2" marker-end="url(#data-arrow)"/>
  <path d="M190,70 L190,100" stroke="#000" stroke-width="2" marker-end="url(#data-arrow)"/>
  <path d="M290,70 L290,100" stroke="#000" stroke-width="2" marker-end="url(#data-arrow)"/>
  <path d="M390,70 L390,100" stroke="#000" stroke-width="2" marker-end="url(#data-arrow)"/>
  <defs>
    <marker id="data-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Pipeline Parallelism

- Series of stages, each performing a specific task
- Output of one stage is input to the next
- Each stage can run in parallel
- Used in streaming processing, assembly lines

<svg viewBox="0 0 500 150">
  <rect x="50" y="50" width="90" height="50" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="170" y="50" width="90" height="50" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="290" y="50" width="90" height="50" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <rect x="410" y="50" width="40" height="50" fill="#fff0e0" stroke="#000" stroke-width="2"/>
  <text x="95" y="75" text-anchor="middle" font-family="sans-serif">Stage 1</text>
  <text x="215" y="75" text-anchor="middle" font-family="sans-serif">Stage 2</text>
  <text x="335" y="75" text-anchor="middle" font-family="sans-serif">Stage 3</text>
  <text x="430" y="75" text-anchor="middle" font-family="sans-serif">...</text>
  <path d="M140,75 L170,75" stroke="#000" stroke-width="2" marker-end="url(#pipe-arrow)"/>
  <path d="M260,75 L290,75" stroke="#000" stroke-width="2" marker-end="url(#pipe-arrow)"/>
  <path d="M380,75 L410,75" stroke="#000" stroke-width="2" marker-end="url(#pipe-arrow)"/>
  <path d="M20,75 L50,75" stroke="#000" stroke-width="2" marker-end="url(#pipe-arrow)"/>
  <defs>
    <marker id="pipe-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Producer-Consumer Pattern

- Producers create data or tasks
- Consumers process data or tasks
- Shared buffer or queue between them
- Synchronization needed for buffer access
- Common in event-driven systems

```cpp
std::queue<int> buffer;
std::mutex mutex;
std::condition_variable not_empty;
std::condition_variable not_full;
const int BUFFER_SIZE = 10;

void producer() {
    while (true) {
        int item = produce_item();  // Generate an item

        std::unique_lock<std::mutex> lock(mutex);
        not_full.wait(lock, []{return buffer.size() < BUFFER_SIZE;});

        buffer.push(item);

        lock.unlock();
        not_empty.notify_one();
    }
}

void consumer() {
    while (true) {
        std::unique_lock<std::mutex> lock(mutex);
        not_empty.wait(lock, []{return !buffer.empty();});

        int item = buffer.front();
        buffer.pop();

        lock.unlock();
        not_full.notify_one();

        consume_item(item);  // Process the item
    }
}
```

---

## Work Stealing

- Dynamic load balancing technique
- Idle threads "steal" work from busy threads
- Reduces wait time and improves utilization
- Used in modern thread pool implementations
- Helps with irregular workloads

<svg viewBox="0 0 500 180">
  <rect x="50" y="50" width="120" height="100" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="190" y="50" width="120" height="100" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="330" y="50" width="120" height="100" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <text x="110" y="40" text-anchor="middle" font-family="sans-serif">Thread 1</text>
  <text x="250" y="40" text-anchor="middle" font-family="sans-serif">Thread 2</text>
  <text x="390" y="40" text-anchor="middle" font-family="sans-serif">Thread 3</text>
  <rect x="60" y="70" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="60" y="95" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="60" y="120" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="95" y="70" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="95" y="95" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="200" y="70" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="200" y="95" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="200" y="120" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="235" y="70" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="235" y="95" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="235" y="120" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="270" y="70" width="30" height="20" fill="#fff" stroke="#000"/>
  <rect x="340" y="70" width="30" height="20" fill="#fff" stroke="#000"/>
  <path d="M340,70 C310,30 290,10 110,60" stroke="#000" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#steal-arrow)"/>
  <text x="250" y="15" text-anchor="middle" font-family="sans-serif" font-size="12">Stealing Work</text>
  <defs>
    <marker id="steal-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Parallel Programming Libraries

- OpenMP: pragma-based parallelism
- Threading Building Blocks (TBB)
- Grand Central Dispatch (GCD)
- MPI (Message Passing Interface)
- Cilk Plus
- Java Fork/Join framework
- .NET Task Parallel Library

---

## OpenMP Example

```cpp
#include <omp.h>
#include <iostream>
#include <vector>

void process_array(std::vector<int>& data) {
    // Parallelize the loop
    #pragma omp parallel for
    for (int i = 0; i < data.size(); i++) {
        // Each iteration can run on a different thread
        data[i] = perform_calculation(data[i]);
    }

    // Reduction operation
    int sum = 0;
    #pragma omp parallel for reduction(+:sum)
    for (int i = 0; i < data.size(); i++) {
        sum += data[i];
    }
}
```

---

## Performance Considerations

- Thread creation costs
- Context switching overhead
- Cache coherency
- False sharing
- Lock contention
- Memory allocation in threaded code
- Thread scheduling impacts
- Load balancing

---

## Cache Coherency and False Sharing

- Cache coherency: keeping multiple caches consistent
- False sharing: performance issue when threads update different variables in the same cache line
- Can severely impact multi-threaded performance
- Solution: padding variables to avoid sharing cache lines

<svg viewBox="0 0 500 180">
  <rect x="50" y="30" width="400" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <text x="250" y="50" text-anchor="middle" font-family="sans-serif">Cache Line (64 bytes)</text>
  <rect x="50" y="60" width="50" height="30" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="100" y="60" width="50" height="30" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <rect x="150" y="60" width="50" height="30" fill="#fff0e0" stroke="#000" stroke-width="2"/>
  <rect x="200" y="60" width="50" height="30" fill="#f0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="250" y="60" width="50" height="30" fill="#e0ffff" stroke="#000" stroke-width="2"/>
  <rect x="300" y="60" width="50" height="30" fill="#ffffe0" stroke="#000" stroke-width="2"/>
  <rect x="350" y="60" width="50" height="30" fill="#ffe0ff" stroke="#000" stroke-width="2"/>
  <rect x="400" y="60" width="50" height="30" fill="#e0fff0" stroke="#000" stroke-width="2"/>
  <text x="75" y="80" text-anchor="middle" font-family="sans-serif" font-size="10">var A</text>
  <text x="125" y="80" text-anchor="middle" font-family="sans-serif" font-size="10">var B</text>
  <text x="175" y="80" text-anchor="middle" font-family="sans-serif" font-size="10">var C</text>
  <text x="225" y="80" text-anchor="middle" font-family="sans-serif" font-size="10">var D</text>
  <text x="275" y="80" text-anchor="middle" font-family="sans-serif" font-size="10">var E</text>
  <text x="325" y="80" text-anchor="middle" font-family="sans-serif" font-size="10">var F</text>
  <text x="375" y="80" text-anchor="middle" font-family="sans-serif" font-size="10">var G</text>
  <text x="425" y="80" text-anchor="middle" font-family="sans-serif" font-size="10">var H</text>
  <rect x="50" y="120" width="150" height="40" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="300" y="120" width="150" height="40" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="125" y="145" text-anchor="middle" font-family="sans-serif">Thread 1 (modifies A)</text>
  <text x="375" y="145" text-anchor="middle" font-family="sans-serif">Thread 2 (modifies H)</text>
  <path d="M75,120 L75,90" stroke="#000" stroke-width="2" marker-end="url(#cache-arrow)"/>
  <path d="M425,120 L425,90" stroke="#000" stroke-width="2" marker-end="url(#cache-arrow)"/>
  <defs>
    <marker id="cache-arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Scalability Challenges

- Amdahl's Law: limits of parallel speedup
- Synchronization bottlenecks
- Communication overhead
- Resource contention
- Memory bandwidth limitations
- System topology awareness

---

## Amdahl's Law

- Maximum theoretical speedup is limited by the sequential portion
- Formula: Speedup = 1 / (S + (1-S)/N)
    1. S = Serial portion
    1. N = Number of processors
- Even small serial portions limit overall speedup

<svg viewBox="0 0 500 200">
  <rect x="50" y="50" width="400" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="50" y="50" width="100" height="30" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="50" y="90" width="400" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="50" y="90" width="100" height="30" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <rect x="50" y="130" width="400" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="50" y="130" width="100" height="30" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="100" y="70" text-anchor="middle" font-family="sans-serif" fill="#000">Serial</text>
  <text x="300" y="70" text-anchor="middle" font-family="sans-serif" fill="#000">Parallel</text>
  <text x="475" y="70" text-anchor="middle" font-family="sans-serif" font-size="12">1 Core</text>
  <text x="475" y="110" text-anchor="middle" font-family="sans-serif" font-size="12">2 Cores</text>
  <text x="475" y="150" text-anchor="middle" font-family="sans-serif" font-size="12">4 Cores</text>
  <text x="25" y="70" text-anchor="middle" font-family="sans-serif" font-size="12">Time</text>
  <text x="25" y="110" text-anchor="middle" font-family="sans-serif" font-size="12">Time</text>
  <text x="25" y="150" text-anchor="middle" font-family="sans-serif" font-size="12">Time</text>
  <rect x="150" y="90" width="175" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="150" y="130" width="87.5" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
</svg>

---

## Debugging Multi-Threaded Programs

- Race condition detection
- Deadlock detection
- Thread state visualization
- Tools:
    1. Valgrind (Helgrind)
    1. Thread Sanitizer
    1. Intel Inspector
    1. Visual Studio Concurrency Visualizer
    1. GDB with thread support

---

## Thread Safety

- Code that functions correctly with concurrent access
- Approaches:
    1. Immutability
    1. Thread-local storage
    1. Synchronization
    1. Atomic operations
    1. Lock-free algorithms
- Challenges in large codebases

---

## Real-World Applications

- Web servers
- Database systems
- Game engines
- Graphics rendering
- Scientific computing
- Financial systems
- Operating systems
- AI and machine learning

---

## Summary

- Multi-threading and multi-processing are essential for modern software
- Threads share memory space, processes are isolated
- Synchronization is critical for correct concurrent programs
- Various mechanisms exist for inter-thread and inter-process communication
- Performance optimizations must consider hardware characteristics
- Parallel patterns help structure concurrent code effectively
- Testing and debugging concurrent programs presents unique challenges
