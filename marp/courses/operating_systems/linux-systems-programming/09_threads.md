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
# Threads in Linux

---

## Chapter Overview

1. **pthread Library Overview**
1. **Creating and Managing Threads**
1. **Thread Synchronization**
1. **Mutexes and Locks**
1. **Condition Variables**
1. **Advanced Threading**
1. **Best Practices**

---

## What are Threads?

## Definition:
- **Lightweight processes** sharing memory
- **Parallel execution** within process
- **Shared address space**
- **Independent stack** per thread
- **Common heap and globals**

Threads = Concurrency within a process!

---

## Processes vs Threads

![processes_vs_threads](svg/courses/operating_systems/linux-systems-programming/09_threads/processes_vs_threads.svg)

---

## Thread Memory Layout

![thread_memory_layout](svg/courses/operating_systems/linux-systems-programming/09_threads/thread_memory_layout.svg)

---

## The pthread Library

```c
#include <pthread.h>

// Compile with: gcc -pthread program.c

// Thread function signature
void *thread_function(void *arg);

// Main thread types
pthread_t       // Thread identifier
pthread_attr_t  // Thread attributes
pthread_mutex_t // Mutual exclusion
pthread_cond_t  // Condition variable
pthread_key_t   // Thread-local storage
pthread_once_t  // One-time initialization
pthread_barrier_t // Synchronization barrier
pthread_spinlock_t // Spin lock
pthread_rwlock_t   // Read-write lock
```

---

## Creating Threads

```c
#include <pthread.h>
#include <stdio.h>

void *thread_function(void *arg) {
    int *num = (int *)arg;
    printf("Thread: received %d\n", *num);
    printf("Thread ID: %lu\n", pthread_self());

    int *result = malloc(sizeof(int));
    *result = (*num) * 2;

    return result;  // or pthread_exit(result);
}

int main() {
    pthread_t thread;
    int arg = 42;

    // Create thread
    int ret = pthread_create(&thread, NULL,
                            thread_function, &arg);
    if (ret != 0) {
        fprintf(stderr, "Error creating thread\n");
        return 1;
    }

    // Wait for thread
    void *retval;
    pthread_join(thread, &retval);

    printf("Thread returned: %d\n", *(int *)retval);
    free(retval);
}
```

---

## Thread Attributes

```c
pthread_attr_t attr;

// Initialize attributes
pthread_attr_init(&attr);

// Detach state
pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
// or PTHREAD_CREATE_JOINABLE (default)

// Stack size
size_t stacksize = 2 * 1024 * 1024;  // 2MB
pthread_attr_setstacksize(&attr, stacksize);

// Stack address (custom stack)
void *stackaddr = mmap(NULL, stacksize, ...);
pthread_attr_setstack(&attr, stackaddr, stacksize);

// Scheduling policy
pthread_attr_setschedpolicy(&attr, SCHED_RR);

// Priority
struct sched_param param = {.sched_priority = 50};
pthread_attr_setschedparam(&attr, &param);

// Create thread with attributes
pthread_create(&thread, &attr, func, arg);

// Cleanup
pthread_attr_destroy(&attr);
```

---

## Waiting for Threads

```c
// pthread_join - Wait for thread termination
void *retval;
int ret = pthread_join(thread, &retval);
if (ret != 0) {
    // Error: EDEADLK (deadlock), EINVAL, ESRCH
}

// Multiple threads
#define NUM_THREADS 5
pthread_t threads[NUM_THREADS];

// Create threads
for (int i = 0; i < NUM_THREADS; i++) {
    pthread_create(&threads[i], NULL, worker, &i);
}

// Wait for all
for (int i = 0; i < NUM_THREADS; i++) {
    pthread_join(threads[i], NULL);
}

// Note: Can only join once per thread!
```

---

## Detached Threads

```c
// Detached threads clean up automatically
// Cannot be joined

// Method 1: Create as detached
pthread_attr_t attr;
pthread_attr_init(&attr);
pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
pthread_create(&thread, &attr, func, NULL);

// Method 2: Detach after creation
pthread_t thread;
pthread_create(&thread, NULL, func, NULL);
pthread_detach(thread);

// Method 3: Self-detach
void *thread_func(void *arg) {
    pthread_detach(pthread_self());
    // Do work...
    return NULL;  // Thread cleans up automatically
}

// Check if detached
int detach_state;
pthread_attr_getdetachstate(&attr, &detach_state);
```

---

## Thread Mutexes

```c
// Mutex - Mutual Exclusion
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

// Or dynamic initialization
pthread_mutex_t mutex;
pthread_mutex_init(&mutex, NULL);

// Critical section
pthread_mutex_lock(&mutex);
// Only one thread here at a time
shared_variable++;
pthread_mutex_unlock(&mutex);

// Try lock (non-blocking)
if (pthread_mutex_trylock(&mutex) == 0) {
    // Got the lock
    do_work();
    pthread_mutex_unlock(&mutex);
} else {
    // Lock busy, do something else
}

// Cleanup
pthread_mutex_destroy(&mutex);
```

---

## Mutex Types

```c
pthread_mutexattr_t attr;
pthread_mutexattr_init(&attr);

// Set mutex type
pthread_mutexattr_settype(&attr, type);

// Types:
PTHREAD_MUTEX_NORMAL     // No error checking (default)
PTHREAD_MUTEX_ERRORCHECK // Error on relock/wrong unlock
PTHREAD_MUTEX_RECURSIVE  // Can lock multiple times
PTHREAD_MUTEX_DEFAULT    // Same as NORMAL

// Recursive mutex example
pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_RECURSIVE);
pthread_mutex_init(&mutex, &attr);

void recursive_function(int depth) {
    pthread_mutex_lock(&mutex);  // OK to relock
    if (depth > 0) {
        recursive_function(depth - 1);
    }
    pthread_mutex_unlock(&mutex);
}
```

---

## How Futexes Work

## Fast Userspace Mutexes:

```c
// Simplified futex operation (kernel interface)
// Real pthread_mutex uses this internally

typedef struct {
    int lock;  // 0=unlocked, 1=locked, 2=contended
} simple_mutex;

void lock(simple_mutex *m) {
    // Fast path - try atomic compare-and-swap
    if (__sync_bool_compare_and_swap(&m->lock, 0, 1)) {
        return;  // Got lock without kernel call!
    }

    // Slow path - need kernel help
    while (1) {
        int val = __sync_lock_test_and_set(&m->lock, 2);
        if (val == 0) return;  // Got it

        // Wait in kernel
        syscall(SYS_futex, &m->lock, FUTEX_WAIT, 2, NULL);
    }
}

void unlock(simple_mutex *m) {
    if (__sync_lock_test_and_set(&m->lock, 0) == 2) {
        // Wake one waiter
        syscall(SYS_futex, &m->lock, FUTEX_WAKE, 1);
    }
}
```

---

## Process-Shared Mutexes

```c
// Mutex in shared memory between processes
#include <sys/mman.h>

// Allocate shared memory
void *shm = mmap(NULL, sizeof(pthread_mutex_t),
                 PROT_READ | PROT_WRITE,
                 MAP_SHARED | MAP_ANONYMOUS, -1, 0);

pthread_mutex_t *mutex = (pthread_mutex_t *)shm;

// Configure for process sharing
pthread_mutexattr_t attr;
pthread_mutexattr_init(&attr);
pthread_mutexattr_setpshared(&attr, PTHREAD_PROCESS_SHARED);

// Initialize in shared memory
pthread_mutex_init(mutex, &attr);

if (fork() == 0) {
    // Child process can use mutex
    pthread_mutex_lock(mutex);
    // Critical section
    pthread_mutex_unlock(mutex);
}
```

---

## Barriers

```c
// Barrier - Wait for all threads to reach a point
pthread_barrier_t barrier;

// Initialize for N threads
pthread_barrier_init(&barrier, NULL, NUM_THREADS);

void *thread_func(void *arg) {
    int id = *(int *)arg;

    // Phase 1 work
    printf("Thread %d: Phase 1\n", id);

    // Wait for all threads
    int ret = pthread_barrier_wait(&barrier);
    if (ret == PTHREAD_BARRIER_SERIAL_THREAD) {
        // One thread gets this return value
        printf("All threads reached barrier\n");
    }

    // Phase 2 work - all start together
    printf("Thread %d: Phase 2\n", id);
}

// Cleanup
pthread_barrier_destroy(&barrier);
```

---

## Condition Variables

```c
// Condition variable - wait for condition
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int ready = 0;

// Consumer thread
void *consumer(void *arg) {
    pthread_mutex_lock(&mutex);
    while (!ready) {  // Always use while, not if!
        pthread_cond_wait(&cond, &mutex);
        // Releases mutex and waits atomically
        // Reacquires mutex when signaled
    }
    // Condition met, mutex held
    process_data();
    pthread_mutex_unlock(&mutex);
}

// Producer thread
void *producer(void *arg) {
    pthread_mutex_lock(&mutex);
    prepare_data();
    ready = 1;
    pthread_cond_signal(&cond);  // Wake one
    // or pthread_cond_broadcast(&cond);  // Wake all
    pthread_mutex_unlock(&mutex);
}
```

---

## Condition Variable Patterns

```c
// Producer-Consumer Queue
typedef struct {
    int buffer[SIZE];
    int count, in, out;
    pthread_mutex_t mutex;
    pthread_cond_t not_empty;
    pthread_cond_t not_full;
} Queue;

void queue_put(Queue *q, int item) {
    pthread_mutex_lock(&q->mutex);

    while (q->count == SIZE) {  // Queue full
        pthread_cond_wait(&q->not_full, &q->mutex);
    }

    q->buffer[q->in] = item;
    q->in = (q->in + 1) % SIZE;
    q->count++;

    pthread_cond_signal(&q->not_empty);
    pthread_mutex_unlock(&q->mutex);
}

int queue_get(Queue *q) {
    pthread_mutex_lock(&q->mutex);

    while (q->count == 0) {  // Queue empty
        pthread_cond_wait(&q->not_empty, &q->mutex);
    }

    int item = q->buffer[q->out];
    q->out = (q->out + 1) % SIZE;
    q->count--;

    pthread_cond_signal(&q->not_full);
    pthread_mutex_unlock(&q->mutex);
    return item;
}
```

---

## Reader-Writer Locks

```c
// Multiple readers, single writer
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

// Reader threads
void *reader(void *arg) {
    pthread_rwlock_rdlock(&rwlock);
    // Multiple readers here simultaneously
    read_data();
    pthread_rwlock_unlock(&rwlock);
}

// Writer thread
void *writer(void *arg) {
    pthread_rwlock_wrlock(&rwlock);
    // Exclusive access
    write_data();
    pthread_rwlock_unlock(&rwlock);
}

// Try locks
if (pthread_rwlock_tryrdlock(&rwlock) == 0) {
    // Got read lock
}
if (pthread_rwlock_trywrlock(&rwlock) == 0) {
    // Got write lock
}

// Cleanup
pthread_rwlock_destroy(&rwlock);
```

---

## Spin Locks

```c
#include <pthread.h>

// Spinlock - busy wait instead of sleep
pthread_spinlock_t spinlock;

// Initialize
pthread_spin_init(&spinlock, PTHREAD_PROCESS_PRIVATE);
// or PTHREAD_PROCESS_SHARED for IPC

// Lock - spins in userspace
pthread_spin_lock(&spinlock);
// Very short critical section only!
counter++;
pthread_spin_unlock(&spinlock);

// Try lock
if (pthread_spin_trylock(&spinlock) == 0) {
    // Got it
    pthread_spin_unlock(&spinlock);
}

// Destroy
pthread_spin_destroy(&spinlock);

// Use cases:
// - Very short critical sections
// - Low contention
// - Real-time systems
// - Avoid context switch overhead
```

---

## Thread-Specific Data (TLS)

```c
// Thread-local storage
pthread_key_t key;

// Destructor for TLS data
void destructor(void *data) {
    free(data);
}

// Create key (once in program)
pthread_key_create(&key, destructor);

// Per-thread usage
void *thread_func(void *arg) {
    // Allocate thread-specific data
    int *data = malloc(sizeof(int));
    *data = pthread_self() % 100;

    // Store in TLS
    pthread_setspecific(key, data);

    // Later, retrieve
    int *my_data = pthread_getspecific(key);
    printf("Thread data: %d\n", *my_data);

    // Destructor called automatically
    return NULL;
}

// Alternative: __thread keyword
__thread int tls_variable = 0;  // Each thread gets own copy
```

---

## Thread Cancellation

```c
// Request thread cancellation
pthread_cancel(thread);

// Cancellation state
pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, &oldstate);
// or PTHREAD_CANCEL_DISABLE

// Cancellation type
pthread_setcanceltype(PTHREAD_CANCEL_DEFERRED, &oldtype);
// or PTHREAD_CANCEL_ASYNCHRONOUS

// Cancellation points (deferred)
// - pthread_join, pthread_cond_wait
// - read, write, sleep, etc.

// Test for cancellation
pthread_testcancel();

// Thread function with cancellation
void *thread_func(void *arg) {
    pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
    pthread_setcanceltype(PTHREAD_CANCEL_DEFERRED, NULL);

    while (1) {
        do_work();
        pthread_testcancel();  // Cancellation point
    }
}
```

---

## Cleanup Handlers

```c
// Cleanup handlers for cancellation/exit
void cleanup1(void *arg) {
    printf("Cleanup 1: %s\n", (char *)arg);
    free(arg);
}

void cleanup2(void *arg) {
    int fd = *(int *)arg;
    close(fd);
}

void *thread_func(void *arg) {
    char *buffer = malloc(1024);
    int fd = open("file.txt", O_RDONLY);

    // Push cleanup handlers (LIFO)
    pthread_cleanup_push(cleanup1, buffer);
    pthread_cleanup_push(cleanup2, &fd);

    // Do work that might be cancelled
    while (1) {
        read(fd, buffer, 1024);
        process(buffer);
        pthread_testcancel();
    }

    // Pop and execute (1) or just pop (0)
    pthread_cleanup_pop(1);  // Execute cleanup2
    pthread_cleanup_pop(1);  // Execute cleanup1

    return NULL;
}
```

---

## Thread Affinity

```c
#define _GNU_SOURCE
#include <sched.h>

// Set CPU affinity for thread
void set_thread_affinity(int cpu) {
    cpu_set_t cpuset;

    CPU_ZERO(&cpuset);
    CPU_SET(cpu, &cpuset);

    pthread_t thread = pthread_self();
    pthread_setaffinity_np(thread, sizeof(cpuset), &cpuset);
}

// Get affinity
void print_affinity() {
    cpu_set_t cpuset;
    pthread_getaffinity_np(pthread_self(),
                          sizeof(cpuset), &cpuset);

    printf("Thread can run on CPUs: ");
    for (int i = 0; i < CPU_SETSIZE; i++) {
        if (CPU_ISSET(i, &cpuset)) {
            printf("%d ", i);
        }
    }
    printf("\n");
}
```

---

## Threads and Signals

```c
// Signals are process-wide but...
// Each thread has own signal mask

// Block signals in thread
sigset_t set;
sigemptyset(&set);
sigaddset(&set, SIGINT);
pthread_sigmask(SIG_BLOCK, &set, NULL);

// Dedicated signal handling thread
void *signal_thread(void *arg) {
    sigset_t set;
    int sig;

    sigemptyset(&set);
    sigaddset(&set, SIGINT);
    sigaddset(&set, SIGTERM);

    while (1) {
        sigwait(&set, &sig);  // Wait for signal
        printf("Got signal %d\n", sig);
        if (sig == SIGTERM) break;
    }
    return NULL;
}

// Send signal to specific thread
pthread_kill(thread, SIGUSR1);
```

---

## Thread Pools

```c
typedef struct {
    pthread_t *threads;
    int num_threads;
    void (*task_func)(void *);

    // Work queue
    void **tasks;
    int queue_size;
    int head, tail, count;

    pthread_mutex_t mutex;
    pthread_cond_t not_empty;
    pthread_cond_t not_full;
    int shutdown;
} ThreadPool;

void *worker_thread(void *arg) {
    ThreadPool *pool = arg;

    while (1) {
        pthread_mutex_lock(&pool->mutex);

        while (pool->count == 0 && !pool->shutdown) {
            pthread_cond_wait(&pool->not_empty, &pool->mutex);
        }

        if (pool->shutdown) {
            pthread_mutex_unlock(&pool->mutex);
            break;
        }

        void *task = pool->tasks[pool->head];
        pool->head = (pool->head + 1) % pool->queue_size;
        pool->count--;

        pthread_cond_signal(&pool->not_full);
        pthread_mutex_unlock(&pool->mutex);

        pool->task_func(task);
    }
    return NULL;
}
```

---

## Thread Safety

## Making Code Thread-Safe:

```c
// 1. Mutex protection
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;
int counter = 0;

void increment() {
    pthread_mutex_lock(&lock);
    counter++;
    pthread_mutex_unlock(&lock);
}

// 2. Atomic operations
#include <stdatomic.h>
_Atomic int atomic_counter = 0;

void atomic_increment() {
    atomic_fetch_add(&atomic_counter, 1);
}

// 3. Thread-local storage
__thread int tls_counter = 0;

void tls_increment() {
    tls_counter++;  // No synchronization needed
}

// 4. Lock-free data structures
// (Advanced - using CAS operations)
```

---

## Common Thread Bugs

## 1. Race Conditions
```c
// BAD: Unsynchronized access
int shared = 0;
void *thread1() { shared++; }
void *thread2() { shared++; }
// Result: Lost updates!
```

## 2. Deadlock
```c
// BAD: Lock ordering
// Thread 1: lock(A); lock(B);
// Thread 2: lock(B); lock(A);
```

## 3. Missing volatile
```c
// BAD: Compiler optimization
int flag = 0;  // Should be volatile
while (!flag);  // May be optimized to while(1)
```

---

## Performance Considerations

```c
// Lock granularity
// BAD: One big lock
pthread_mutex_t global_lock;

// BETTER: Fine-grained locks
typedef struct {
    int value;
    pthread_mutex_t lock;
} Counter;

Counter counters[100];

// Lock-free alternatives
_Atomic int counter = 0;
atomic_fetch_add(&counter, 1);  // No lock needed

// Reduce contention
// - Use reader-writer locks
// - Use thread-local storage
// - Minimize critical sections
// - Consider lock-free algorithms
```

---

## Debugging Threads

```bash
# GDB thread commands
gdb ./program
(gdb) info threads          # List all threads
(gdb) thread 2              # Switch to thread 2
(gdb) thread apply all bt   # Backtrace all threads
(gdb) set scheduler-locking on  # Lock thread scheduling

# Helgrind - Race condition detector
valgrind --tool=helgrind ./program

# Thread Sanitizer
gcc -fsanitize=thread -g program.c
./program

# strace threads
strace -f ./program  # Follow threads

# View threads
ps -eLf | grep program
htop  # Press H to show threads
```

---

## Thread Best Practices

1. **Minimize shared data**
    - Prefer message passing

1. **Use appropriate synchronization**
    - Mutex for mutual exclusion
    - RW locks for read-heavy
    - Spinlocks for short sections

1. **Avoid deadlocks**
    - Consistent lock ordering
    - Try-lock with timeout

1. **Keep critical sections short**

1. **Use thread pools** for task parallelism

1. **Profile before optimizing**

1. **Test thoroughly**
    - Race conditions are hard to reproduce

---

## Threads vs Processes Decision

## Use Threads When:
- Need shared memory
- Frequent communication
- Low creation overhead
- Cache efficiency matters

## Use Processes When:
- Need isolation
- Fault tolerance required
- Different privileges
- Distributed system

## Hybrid Approach:
- Multiple processes with thread pools
- Best of both worlds

---

## Summary

## Key Takeaways:

- **Threads** share memory within process
- **pthread** library for POSIX threads
- **Synchronization** is critical
- **Mutexes** for mutual exclusion
- **Condition variables** for coordination
- **Different lock types** for different needs
- **Thread safety** requires careful design
- **Debugging** needs special tools

Master threads = Concurrent programming power!
