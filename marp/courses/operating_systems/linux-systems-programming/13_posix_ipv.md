# POSIX IPC

---

## What is POSIX IPC?

1. A set of IPC standards defined by POSIX to address the shortcomings of earlier mechanisms like System V IPC.
1. They are designed to be more consistent with the `UNIX` file I/O model.
1. Key characteristics:
    - Objects are often referenced by names (like file paths) rather than keys.
    - Many objects are accessed via file descriptors, allowing the use of standard I/O calls (`read`, `write`, `close`) and I/O multiplexing (`select`, `poll`, `epoll`).
1. The main mechanisms are:
    - Message Queues
    - Semaphores
    - Shared Memory

---

## POSIX IPC vs System V IPC

![posix_ipc_vs_sysv](svg/courses/operating_systems/linux-systems-programming/13_posix_ipv/posix_ipc_vs_sysv.svg)

---

## POSIX Message Queues

1. A more robust and flexible replacement for Sys V message queues.
1. Queues are identified by a name, which looks like a file path (e.g., `/my_queue`).
1. The underlying implementation often uses a virtual file system (`mqueuefs`).
1. Messages have priorities, and are always retrieved from the queue in priority order.

---

## POSIX Message Queue API

1. `mq_open(3)`: Create or open a message queue. Returns a message queue descriptor (like a file descriptor).
    ```c
    mqd_t mq_open(const char *name, int oflag, mode_t mode, struct mq_attr *attr);
    ```
1. `mq_send(3)`: Send a message to a queue.
    ```c
    int mq_send(mqd_t mqdes, const char *msg_ptr, size_t msg_len, unsigned int msg_prio);
    ```
1. `mq_receive(3)`: Receive a message from a queue.
    ```c
    ssize_t mq_receive(mqd_t mqdes, char *msg_ptr, size_t msg_len, unsigned int *msg_prio);
    ```
1. `mq_close(3)`: Close the message queue descriptor.
1. `mq_unlink(3)`: Remove the message queue from the system.

---

## POSIX Semaphores

1. A simpler, more modern alternative to Sys V semaphores.
1. Two types exist:
    - **Named Semaphores:** Identified by a name (e.g., `/my_semaphore`). Usable by unrelated processes.
    - **Unnamed Semaphores:** Stored in memory shared between processes or threads (e.g., in a shared memory segment). More efficient.

---

## Named Semaphore API

1. `sem_open(3)`: Create or open a named semaphore. Returns a `sem_t*` pointer.
    ```c
    sem_t *sem_open(const char *name, int oflag, mode_t mode, unsigned int value);
    ```
1. `sem_wait(3)`: Decrement (lock) the semaphore. Blocks if the value is zero.
1. `sem_post(3)`: Increment (unlock) the semaphore.
1. `sem_close(3)`: Close the semaphore.
1. `sem_unlink(3)`: Remove the named semaphore.

---

## Unnamed Semaphore API

1. `sem_init(3)`: Initialize a semaphore located in shared memory.
    ```c
    int sem_init(sem_t *sem, int pshared, unsigned int value);
    // pshared must be non-zero for sharing between processes
    ```
1. `sem_wait(3)` and `sem_post(3)` are used just like with named semaphores.
1. `sem_destroy(3)`: Destroy the unnamed semaphore.

---

## POSIX Shared Memory

1. Provides an alternative to the Sys V shared memory API.
1. The key difference is that it uses a file descriptor-based model.
1. This makes it feel more like standard file manipulation.

---

## POSIX Shared Memory API

1. `shm_open(3)`: Create or open a shared memory object. It returns a file descriptor. The name (e.g., `/my_shm`) identifies the object.
    ```c
    int shm_open(const char *name, int oflag, mode_t mode);
    ```
1. `ftruncate(2)`: Set the size of the shared memory object. This must be done after creating it.
1. `mmap(2)`: Map the shared memory object into the process's address space using the file descriptor from `shm_open`.
1. `munmap(2)`: Unmap the memory region.
1. `shm_unlink(3)`: Remove the shared memory object from the system.

---

## Performance Compared to Sys V Equivalents

1. **Message Queues:** POSIX is generally superior. The ability to use I/O multiplexing via the descriptor is a major advantage for modern application design.
1. **Semaphores:** POSIX unnamed semaphores are typically faster as they can live in shared memory without kernel overhead on every operation. Named semaphores have similar performance to Sys V.
1. **Shared Memory:** The underlying performance is nearly identical. The choice is primarily about which API style you prefer. The POSIX file descriptor model is often seen as more consistent and flexible.

---

## Advantages of POSIX IPC

1. **Consistent API:** The use of names and file descriptors aligns well with the rest of the `UNIX` API.
1. **I/O Multiplexing:** Message queues and shared memory objects (via their file descriptors) can be monitored with `select(2)`, `poll(2)`, and `epoll(2)`.
1. **Cleanup:** The `unlink` model is explicit and clear.
1. **Flexibility:** Features like message priorities and unnamed semaphores provide more options for developers.

---

## Chapter Summary

1. We introduced the POSIX IPC mechanisms as modern replacements for the System V interfaces.
1. We explored the APIs for POSIX message queues, semaphores (both named and unnamed), and shared memory.
1. We highlighted the key design principle: using names for identification and file descriptors for access.
1. We compared the performance and features to their Sys V counterparts, noting the advantages of the POSIX versions, especially in API consistency and integration with event-driven models.
