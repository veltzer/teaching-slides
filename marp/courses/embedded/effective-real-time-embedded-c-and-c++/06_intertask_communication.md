# Intertask Communication

---

## Chapter Overview

1. Race conditions and critical sections
1. Shared memory techniques
1. Synchronization primitives
1. Deadlock prevention
1. Message passing mechanisms

---

## Concurrency Challenges

![concurrency_challenges](/svg/courses/embedded/effective-real-time-embedded-c-and-c++/06_intertask_communication/concurrency_challenges.svg)

---

## Race Conditions

```c
// Unsafe shared counter
volatile int counter = 0;

// Task A
void task_a(void) {
    for (int i = 0; i < 1000; i++) {
        counter++;  // Not atomic!
    }
}

// Task B
void task_b(void) {
    for (int i = 0; i < 1000; i++) {
        counter++;  // Race condition!
    }
}
// Result: counter < 2000
```

---

## Critical Sections

```c
// Protected access
volatile int counter = 0;
volatile bool lock = false;

void increment_counter(void) {
    // Enter critical section
    while (__atomic_test_and_set(&lock, __ATOMIC_ACQUIRE));

    // Critical section
    counter++;

    // Exit critical section
    __atomic_clear(&lock, __ATOMIC_RELEASE);
}
```

---

## Interrupt Masking

```c
// Simple critical section using interrupts
uint32_t enter_critical(void) {
    uint32_t primask = __get_PRIMASK();
    __disable_irq();
    return primask;
}

void exit_critical(uint32_t primask) {
    __set_PRIMASK(primask);
}

// Usage
void safe_update(void) {
    uint32_t state = enter_critical();
    // Modify shared data
    shared_var++;
    exit_critical(state);
}
```

---

## Shared Memory Model

```c
// Shared data structure
typedef struct {
    uint8_t buffer[256];
    volatile uint32_t write_idx;
    volatile uint32_t read_idx;
    volatile uint32_t count;
} shared_buffer_t;

// Ensure cache coherency
__attribute__((section(".shared_mem")))
volatile shared_buffer_t shared_data;
```

---

## Producer-Consumer Pattern

```c
// Circular buffer implementation
typedef struct {
    uint8_t* buffer;
    size_t size;
    volatile size_t head;
    volatile size_t tail;
    volatile size_t count;
} ring_buffer_t;

bool ring_put(ring_buffer_t* rb, uint8_t data) {
    if (rb->count >= rb->size) {
        return false;  // Full
    }

    rb->buffer[rb->head] = data;
    rb->head = (rb->head + 1) % rb->size;
    __atomic_add_fetch(&rb->count, 1, __ATOMIC_RELEASE);
    return true;
}
```

---

## Lock Implementation

```c
// Spinlock
typedef volatile uint32_t spinlock_t;

void spin_lock(spinlock_t* lock) {
    while (__atomic_test_and_set(lock, __ATOMIC_ACQUIRE)) {
        // Spin
    }
}

void spin_unlock(spinlock_t* lock) {
    __atomic_clear(lock, __ATOMIC_RELEASE);
}

// Usage with timeout
bool spin_lock_timeout(spinlock_t* lock, uint32_t timeout) {
    uint32_t start = get_tick_count();
    while (__atomic_test_and_set(lock, __ATOMIC_ACQUIRE)) {
        if (get_tick_count() - start > timeout) {
            return false;
        }
    }
    return true;
}
```

---

## Mutex (Mutual Exclusion)

```c
typedef struct {
    volatile uint32_t lock;
    volatile uint32_t owner;
    volatile uint32_t count;  // For recursive mutex
} mutex_t;

bool mutex_lock(mutex_t* mtx) {
    uint32_t current_task = get_current_task_id();

    // Recursive mutex
    if (mtx->owner == current_task) {
        mtx->count++;
        return true;
    }

    // Try to acquire
    while (__atomic_test_and_set(&mtx->lock,
                                 __ATOMIC_ACQUIRE)) {
        yield();  // Give up CPU
    }

    mtx->owner = current_task;
    mtx->count = 1;
    return true;
}
```

---

## Semaphore Implementation

```c
typedef struct {
    volatile int32_t count;
    volatile uint32_t waiting_tasks;
} semaphore_t;

void sem_wait(semaphore_t* sem) {
    __atomic_add_fetch(&sem->waiting_tasks, 1,
                       __ATOMIC_ACQUIRE);

    while (1) {
        int32_t count = sem->count;
        if (count > 0) {
            if (__atomic_compare_exchange_n(&sem->count,
                                           &count,
                                           count - 1,
                                           false,
                                           __ATOMIC_ACQUIRE,
                                           __ATOMIC_RELAXED)) {
                break;
            }
        }
        yield();
    }

    __atomic_sub_fetch(&sem->waiting_tasks, 1,
                       __ATOMIC_RELEASE);
}
```

---

## Binary vs Counting Semaphores

```c
// Binary semaphore (0 or 1)
typedef struct {
    volatile uint32_t value;
} binary_sem_t;

// Counting semaphore (0 to N)
typedef struct {
    volatile uint32_t value;
    uint32_t max_count;
} counting_sem_t;

// Resource pool management
counting_sem_t resource_pool = {
    .value = 5,      // 5 resources available
    .max_count = 5
};
```

---

## Priority Inversion

![priority_inversion](/svg/courses/embedded/effective-real-time-embedded-c-and-c++/06_intertask_communication/priority_inversion.svg)

---

## Priority Inheritance

```c
typedef struct {
    volatile uint32_t lock;
    uint32_t owner_task;
    uint8_t owner_original_priority;
} priority_mutex_t;

void priority_mutex_lock(priority_mutex_t* mtx) {
    uint32_t current = get_current_task_id();

    while (__atomic_test_and_set(&mtx->lock,
                                 __ATOMIC_ACQUIRE)) {
        // Boost owner priority
        uint8_t my_prio = get_task_priority(current);
        uint8_t owner_prio = get_task_priority(mtx->owner_task);

        if (my_prio > owner_prio) {
            set_task_priority(mtx->owner_task, my_prio);
        }
        yield();
    }

    mtx->owner_task = current;
    mtx->owner_original_priority = get_task_priority(current);
}
```

---

## Deadlock Conditions

1. **Mutual Exclusion**: Resources cannot be shared
1. **Hold and Wait**: Task holds resource while waiting
1. **No Preemption**: Resources cannot be forcibly taken
1. **Circular Wait**: Circular chain of dependencies

---

## Deadlock Example

```c
// Classic dining philosophers problem
mutex_t fork[5];

void philosopher(int id) {
    int left = id;
    int right = (id + 1) % 5;

    while (1) {
        think();

        // Potential deadlock!
        mutex_lock(&fork[left]);
        mutex_lock(&fork[right]);

        eat();

        mutex_unlock(&fork[right]);
        mutex_unlock(&fork[left]);
    }
}
```

---

## Deadlock Prevention

```c
// Resource ordering - always lock in same order
void transfer_funds(account_t* from, account_t* to,
                   int amount) {
    mutex_t* first;
    mutex_t* second;

    // Order by address
    if (from < to) {
        first = &from->mutex;
        second = &to->mutex;
    } else {
        first = &to->mutex;
        second = &from->mutex;
    }

    mutex_lock(first);
    mutex_lock(second);

    // Safe to transfer
    from->balance -= amount;
    to->balance += amount;

    mutex_unlock(second);
    mutex_unlock(first);
}
```

---

## Lock-Free Programming

```c
// Lock-free stack using CAS
typedef struct node {
    void* data;
    struct node* next;
} node_t;

typedef struct {
    node_t* head;
} lock_free_stack_t;

void push(lock_free_stack_t* stack, void* data) {
    node_t* new_node = malloc(sizeof(node_t));
    new_node->data = data;

    node_t* old_head;
    do {
        old_head = stack->head;
        new_node->next = old_head;
    } while (!__atomic_compare_exchange_n(&stack->head,
                                         &old_head,
                                         new_node,
                                         false,
                                         __ATOMIC_RELEASE,
                                         __ATOMIC_ACQUIRE));
}
```

---

## Atomic Operations

```c
// Atomic primitives
volatile uint32_t counter = 0;

// Atomic increment
__atomic_add_fetch(&counter, 1, __ATOMIC_SEQ_CST);

// Atomic compare and swap
uint32_t expected = 0;
uint32_t desired = 1;
__atomic_compare_exchange_n(&counter, &expected, desired,
                           false, __ATOMIC_SEQ_CST,
                           __ATOMIC_SEQ_CST);

// Atomic load/store
uint32_t value = __atomic_load_n(&counter, __ATOMIC_ACQUIRE);
__atomic_store_n(&counter, value, __ATOMIC_RELEASE);
```

---

## Memory Barriers

```c
// Memory ordering
volatile int data_ready = 0;
volatile int data = 0;

// Producer
void producer(void) {
    data = 42;
    __atomic_thread_fence(__ATOMIC_RELEASE);
    data_ready = 1;
}

// Consumer
int consumer(void) {
    while (!data_ready);
    __atomic_thread_fence(__ATOMIC_ACQUIRE);
    return data;  // Guaranteed to see 42
}
```

---

## Signal Mechanism

```c
// Simple signal implementation
typedef struct {
    volatile uint32_t flags;
    void (*handlers[32])(int);
} signal_t;

void signal_send(signal_t* sig, int signal_num) {
    __atomic_or_fetch(&sig->flags, 1U << signal_num,
                      __ATOMIC_RELEASE);
}

void signal_process(signal_t* sig) {
    uint32_t pending = __atomic_exchange_n(&sig->flags, 0,
                                          __ATOMIC_ACQUIRE);

    while (pending) {
        int sig_num = __builtin_ffs(pending) - 1;
        if (sig->handlers[sig_num]) {
            sig->handlers[sig_num](sig_num);
        }
        pending &= ~(1U << sig_num);
    }
}
```

---

## Message Queue

```c
typedef struct {
    void* buffer;
    size_t msg_size;
    size_t capacity;
    volatile size_t head;
    volatile size_t tail;
    semaphore_t empty;
    semaphore_t full;
    mutex_t mutex;
} message_queue_t;

bool mq_send(message_queue_t* mq, const void* msg) {
    sem_wait(&mq->empty);
    mutex_lock(&mq->mutex);

    void* dest = (uint8_t*)mq->buffer +
                 (mq->tail * mq->msg_size);
    memcpy(dest, msg, mq->msg_size);
    mq->tail = (mq->tail + 1) % mq->capacity;

    mutex_unlock(&mq->mutex);
    sem_post(&mq->full);
    return true;
}
```

---

## Mailbox Pattern

```c
typedef struct {
    void* message;
    volatile bool valid;
    mutex_t mutex;
    semaphore_t available;
} mailbox_t;

void mailbox_post(mailbox_t* mb, void* msg) {
    mutex_lock(&mb->mutex);

    // Overwrite if not consumed
    mb->message = msg;
    mb->valid = true;

    mutex_unlock(&mb->mutex);
    sem_post(&mb->available);
}

void* mailbox_wait(mailbox_t* mb) {
    sem_wait(&mb->available);

    mutex_lock(&mb->mutex);
    void* msg = mb->message;
    mb->valid = false;
    mutex_unlock(&mb->mutex);

    return msg;
}
```

---

## Event Flags

```c
typedef struct {
    volatile uint32_t flags;
    mutex_t mutex;
    semaphore_t event;
} event_group_t;

void event_set(event_group_t* eg, uint32_t flags) {
    mutex_lock(&eg->mutex);
    eg->flags |= flags;
    mutex_unlock(&eg->mutex);

    sem_post(&eg->event);  // Wake waiters
}

uint32_t event_wait(event_group_t* eg, uint32_t mask,
                    bool clear_on_exit) {
    while (1) {
        mutex_lock(&eg->mutex);
        uint32_t current = eg->flags & mask;

        if (current) {
            if (clear_on_exit) {
                eg->flags &= ~current;
            }
            mutex_unlock(&eg->mutex);
            return current;
        }

        mutex_unlock(&eg->mutex);
        sem_wait(&eg->event);
    }
}
```

---

## Publish-Subscribe Pattern

```c
typedef struct subscriber {
    void (*callback)(void* data);
    struct subscriber* next;
} subscriber_t;

typedef struct {
    subscriber_t* subscribers;
    mutex_t mutex;
} publisher_t;

void publish(publisher_t* pub, void* data) {
    mutex_lock(&pub->mutex);

    subscriber_t* sub = pub->subscribers;
    while (sub) {
        sub->callback(data);
        sub = sub->next;
    }

    mutex_unlock(&pub->mutex);
}
```

---

## Best Practices

1. Minimize critical section duration
1. Avoid nested locks when possible
1. Use lock-free algorithms where appropriate
1. Always check return values
1. Design for testability

---

## Summary

1. Race conditions require synchronization
1. Multiple primitives for different needs
1. Deadlock prevention through careful design
1. Lock-free alternatives for performance
1. Message passing for loose coupling

---

## Key Takeaways

1. **Synchronization** is essential for correctness
1. **Deadlocks** can be prevented by design
1. **Atomic operations** enable lock-free code
1. **Message passing** reduces coupling
1. **Priority inversion** needs special handling
