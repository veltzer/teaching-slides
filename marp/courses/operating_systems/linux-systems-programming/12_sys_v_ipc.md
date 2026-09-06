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

# Sys V IPC

---

## What is System V IPC?

1. A set of Inter-Process Communication (IPC) mechanisms that first appeared in UNIX System V.
1. They are now considered legacy but are still supported by `Linux` and other `UNIX`-like systems.
1. They provide features not originally present in the classic `UNIX` toolkit (like pipes).
1. The main mechanisms are:
    - Message Queues
    - Semaphores
    - Shared Memory

---

## System V IPC Architecture

![sysv_ipc_architecture](svg/courses/operating_systems/linux-systems-programming/12_sys_v_ipc/sysv_ipc_architecture.svg)

---

## Common Characteristics of Sys V IPC

1. **Kernel Persistence:** IPC objects exist independently of any process. They remain in the kernel until explicitly removed by a process or a system reboot.
1. **No File Descriptors:** They are not accessed via file descriptors. Instead, they are identified by integer IDs.
1. **Keys and IDs:** A `key_t` key is used to look up an integer ID for an IPC object. The `ftok(3)` function is often used to generate a key from a file path.
1. **Permissions:** Each object has an associated permissions structure, similar to file permissions (`owner`, `group`, `mode`).
1. **Tools:** The `ipcs` and `ipcrm` command-line tools are used to inspect and remove Sys V IPC objects.

---

## `ftok(3)` - Generating Keys

```c
#include <sys/types.h>
#include <sys/ipc.h>

key_t ftok(const char *pathname, int proj_id);
```

1. `ftok` ("file to key") creates a key based on a file's i-node number and the `proj_id`.
1. This provides a way for unrelated processes to generate the same key by agreeing on a file path and project ID.
1. The file at `pathname` must exist and be accessible.
1. It's a common convention, not a requirement. Any `key_t` value can be used.

---

## Sys V Message Queues

1. Provides a mechanism for processes to exchange messages in a structured way.
1. The kernel manages a queue of messages for each message queue object.
1. Messages have a type (a positive integer) and a data payload.
1. Receivers can choose to read messages of a specific type or the first message on the queue.

---

## Message Queue API

1. `msgget(2)`: Get a message queue ID. Creates a new queue or gets an existing one.
   ```c
    int msgget(key_t key, int msgflg);
   ```
1. `msgsnd(2)`: Send a message to a queue. The call can block if the queue is full.
   ```c
    int msgsnd(int msqid, const void *msgp, size_t msgsz, int msgflg);
   ```
1. `msgrcv(2)`: Receive a message from a queue. Can block if the queue is empty.
   ```c
    ssize_t msgrcv(int msqid, void *msgp, size_t msgsz, long msgtyp, int msgflg);
   ```
1. `msgctl(2)`: Control operations (e.g., query status, set permissions, remove queue).

---

## Sys V Semaphores

1. A semaphore is a counter used to control access to shared resources.
1. Sys V semaphores are more complex than POSIX semaphores.
1. They are managed in **sets**. A single semaphore ID can refer to an array of individual semaphores.
1. Operations can be performed on multiple semaphores within a set atomically.

---

## Semaphore API

1. `semget(2)`: Get a semaphore set ID.
   ```c
    int semget(key_t key, int nsems, int semflg);
   ```
1. `semop(2)`: Perform operations on semaphores in a set. This is the core function. It takes an array of `sembuf` structures, each specifying an operation (increment, decrement, or wait-for-zero) on a semaphore in the set.
   ```c
    int semop(int semid, struct sembuf *sops, size_t nsops);
   ```
1. `semctl(2)`: Control operations (e.g., initialize value, get value, remove set).

---

## Sys V Shared Memory

1. Provides a way for multiple processes to share a region of memory.
1. This is the fastest form of IPC, as data does not need to be copied between the kernel and user space.
1. Once a shared memory segment is attached to a process's address space, it can be accessed like any other memory region (e.g., via pointers).
1. Synchronization (e.g., using semaphores) is required to prevent race conditions.

---

## Shared Memory API

1. `shmget(2)`: Get a shared memory segment ID.
   ```c
    int shmget(key_t key, size_t size, int shmflg);
   ```
1. `shmat(2)`: Attach the shared memory segment to the process's address space. It returns a pointer to the start of the segment.
   ```c
    void *shmat(int shmid, const void *shmaddr, int shmflg);
   ```
1. `shmdt(2)`: Detach the segment from the process's address space.
   ```c
    int shmdt(const void *shmaddr);
   ```
1. `shmctl(2)`: Control operations (e.g., query status, set permissions, remove segment).

---

## Performance Compared to POSIX Equivalents

| IPC Type | System V | POSIX | Performance Comparison |
| :--- | :--- | :--- | :--- |
| **Message Queues** | `msgget` family | `mq_open` family | POSIX is generally faster and more flexible. POSIX queues can be used with `select`/`poll`/`epoll`. |
| **Semaphores** | `semget` family | `sem_open` family | POSIX semaphores are much simpler and lighter-weight. Sys V semaphores are complex but offer atomic operations on sets. |
| **Shared Memory** | `shmget` family | `shm_open` family | Performance is very similar. The main difference is the API. POSIX shared memory uses file descriptors, which can be more convenient. |

---

## Drawbacks of Sys V IPC

1. **Clumsy API:** The key/ID system and multi-purpose `ctl` functions are less intuitive than the file descriptor-based approach of POSIX IPC.
1. **No `select`/`poll`/`epoll`:** You cannot use standard I/O multiplexing on Sys V IPC objects, making them difficult to integrate into event-driven applications.
1. **Kernel Persistence:** Can lead to resource leaks if objects are not explicitly cleaned up. A crashed program can leave behind its IPC objects.
1. **Namespace Pollution:** The keys exist in a single system-wide namespace, which can lead to collisions.

---

## Chapter Summary

1. We introduced the three main types of System V IPC: message queues, semaphores, and shared memory.
1. We discussed their common characteristics: kernel persistence, key-based identification, and lack of file descriptors.
1. We reviewed the basic API for each mechanism (`get`, `snd`/`rcv`/`op`/`at`, `ctl`).
1. We noted that while still supported, they are largely considered legacy and have been superseded by the more modern POSIX IPC equivalents.
1. We highlighted the performance and usability drawbacks compared to their POSIX counterparts.
