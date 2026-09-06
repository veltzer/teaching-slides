---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---

# Python Multi-Threading and Multi-Processing

---

## Introduction to Python Concurrency

- Python offers multiple approaches to concurrent programming
- Threading vs Multiprocessing vs Asynchronous I/O
- Understanding Python's execution model is essential
- Different concurrency models for different use cases
- Enables better resource utilization in Python applications

---

## Concurrency vs. Parallelism in Python: Details

- Concurrency: dealing with multiple tasks at once
- Parallelism: executing multiple tasks simultaneously
- Python can handle both, but with different tools
- Understanding the difference guides tool selection

---

## Concurrency vs. Parallelism in Python

![concurrency_vs_parallelism_in_python](svg/courses/languages/python/advanced-python/20_multi_threading_multi_processing/concurrency_vs_parallelism_in_python.svg)

---

## Python's Global Interpreter Lock (GIL)

- A mutex that protects access to Python objects
- Only one thread can execute Python bytecode at a time
- Simplifies memory management in CPython
- Limits CPU-bound thread parallelism
- I/O-bound threads can still provide concurrency benefits
- Key consideration when choosing concurrency approach

---

## Python Concurrency Models: Details

- Threading: lightweight, shares memory, affected by GIL
- Multiprocessing: separate processes, bypasses GIL, higher overhead
- Asyncio: cooperative multitasking, single-threaded, event loop
- Concurrent.futures: high-level abstraction for both threading and multiprocessing
- Third-party libraries (Dask, Joblib, etc.)

---

## Python Concurrency Models

![python_concurrency_models](svg/courses/languages/python/advanced-python/20_multi_threading_multi_processing/python_concurrency_models.svg)

---

## When to Use Each Concurrency Model

- Threading:
  1. I/O-bound tasks (network, file operations)
  1. GUI applications
  1. Tasks that need shared memory
- Multiprocessing:
  1. CPU-bound tasks
  1. Tasks that need to bypass the GIL
  1. When memory isolation is desired
- Asyncio:
  1. Many concurrent I/O operations
  1. Network servers, clients
  1. When cooperative multitasking fits the problem

---

## Python's threading Module

- Standard library module for thread-based parallelism
- Thread class for creating and managing threads
- `start()`, `join()`, `is_alive()` methods
- Thread synchronization primitives
- Daemon threads vs non-daemon threads

```python
import threading
import time

def worker(name):
    print(f"Worker {name} starting")
    time.sleep(1)
    print(f"Worker {name} finished")

# Create and start threads
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

# Wait for all threads to complete
for t in threads:
    t.join()
```

---

## Thread Class Constructor

- `threading.Thread` constructor parameters:
  1. `target`: function to run in thread
  1. `args`: arguments to pass to target function
  1. `kwargs`: keyword arguments for target function
  1. `daemon`: boolean for daemon status
  1. `name`: thread name for identification

```python
# Example with more parameters
thread = threading.Thread(
    target=worker,
    args=(1, 2),
    kwargs={'debug': True},
    daemon=True,
    name="WorkerThread"
)
```

---

## Thread Subclassing

- Custom thread behavior by subclassing `threading.Thread`
- Override `run()` method to define thread behavior
- Access to thread instance attributes

```python
import threading

class MyThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay

    def run(self):
        print(f"Thread {self.name} starting")
        time.sleep(self.delay)
        print(f"Thread {self.name} finished")

# Create and start thread instances
threads = [MyThread(f"Thread-{i}", i) for i in range(3)]
for t in threads:
    t.start()
```

---

## Thread Lifecycle in Python: Details

- New: thread object created
- Runnable: thread started with `start()`
- Running: thread is executing
- Blocked/Waiting: thread is waiting for resources/events
- Terminated: thread execution completed

---

## Thread Lifecycle in Python

![thread_lifecycle_in_python](svg/courses/languages/python/advanced-python/20_multi_threading_multi_processing/thread_lifecycle_in_python.svg)

---

## Daemon Threads

- Background threads that don't block program exit
- Program terminates when only daemon threads remain
- Useful for service threads (monitoring, logging)
- Set with `thread.daemon = True` or constructor

```python
import threading
import time

def background_task():
    while True:
        print("Background task running...")
        time.sleep(2)

# Create a daemon thread
daemon_thread = threading.Thread(
    target=background_task,
    daemon=True
)
daemon_thread.start()

# Main thread work
print("Main thread working...")
time.sleep(5)
print("Main thread exiting")
```

---

## Race Conditions in Python

- Multiple threads accessing shared data concurrently
- Results depend on execution timing
- Common in counter increments, shared collections
- GIL doesn't prevent all race conditions!

```python
import threading

counter = 0

def increment():
    global counter
    for _ in range(100000):
        counter += 1  # Race condition here

threads = []
for _ in range(10):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"Final counter value: {counter}")
# Expected: 1,000,000
# Actual: Often less
```

---

## Thread Synchronization in Python

- Lock (mutex): basic mutual exclusion
- RLock: reentrant lock for nested lock acquisition
- Semaphore: controls access to a resource pool
- BoundedSemaphore: semaphore that checks for overrelease
- Event: signals between threads
- Condition: complex signaling and coordination
- Barrier: synchronization point for multiple threads

---

## Locks (Mutexes)

- Basic synchronization primitive
- Protects critical sections
- Prevents concurrent execution
- Two states: locked and unlocked
- Methods: `acquire()` and `release()`
- Context manager support with `with` statement

```python
import threading

counter = 0
counter_lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        with counter_lock:  # acquire() and release()
            counter += 1

threads = []
for _ in range(10):
    t = threading.Thread(target=increment)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

---

## RLock (Reentrant Lock)

- Can be acquired multiple times by same thread
- Must be released same number of times
- Useful for recursive function calls
- Prevents deadlocks in nested lock scenarios

```python
import threading

class SharedResource:
    def __init__(self):
        self.lock = threading.RLock()
        self.value = 0

    def method1(self):
        with self.lock:
            self.value += 1
            # Can call method2 while holding the lock
            self.method2()

    def method2(self):
        with self.lock:  # Would deadlock with regular Lock
            self.value += 2
```

---

## Semaphores

- Counter-based synchronization primitive
- Controls access to a limited resource pool
- `acquire()` decrements counter, waits if zero
- `release()` increments counter
- Useful for limiting concurrent access

```python
import threading
import time

# Limit to 3 concurrent threads
semaphore = threading.Semaphore(3)

def worker(name):
    with semaphore:
        print(f"Worker {name} acquired semaphore")
        time.sleep(1)  # Simulate work
        print(f"Worker {name} releasing")

# Create 10 worker threads
threads = []
for i in range(10):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
```

---

## Events

- Simple communication between threads
- Binary state: set or clear
- Methods: `set()`, `clear()`, `wait()`, `is_set()`
- Useful for signaling state changes

```python
import threading
import time

# Create an event object
start_event = threading.Event()

def worker(name):
    print(f"Worker {name} waiting for start signal")
    # Wait for event to be set
    start_event.wait()
    print(f"Worker {name} started working")

# Create worker threads
threads = []
for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

time.sleep(2)
print("Signaling workers to start")
start_event.set()  # Signal all threads to proceed
```

---

## Condition Variables

- Allow threads to wait for a specific condition
- Used with a predicate (condition to be true)
- Methods: `wait()`, `notify()`, `notify_all()`
- More sophisticated than simple events
- Useful for producer-consumer patterns

```python
import threading
import queue
import time

class BoundedQueue:
    def __init__(self, size):
        self.queue = queue.deque()
        self.size = size
        self.condition = threading.Condition()

    def put(self, item):
        with self.condition:
            while len(self.queue) >= self.size:
                self.condition.wait()
            self.queue.append(item)
            self.condition.notify()
```

---

## Barriers

- Synchronization point for a group of threads
- Threads wait until all reach the barrier
- Useful for phases of parallel algorithms
- `wait()` method blocks until all threads arrive

```python
import threading
import time

# Initialize barrier for 4 threads
barrier = threading.Barrier(4)

def worker(name):
    print(f"Worker {name} started phase 1")
    time.sleep(1)  # Simulate work
    print(f"Worker {name} reached barrier")

    # Wait for all threads to reach the barrier
    barrier.wait()
    print(f"Worker {name} starting phase 2")
```

---

## Deadlocks in Python

- Circular waiting for resources
- Can occur when threads acquire multiple locks
- Python doesn't provide deadlock detection
- Can be prevented by lock ordering

```python
import threading
import time

# Two locks
lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1():
    with lock_a:
        print("Thread 1 acquired lock A")
        time.sleep(0.5)
        with lock_b:
            print("Thread 1 acquired lock B")

def thread_2():
    with lock_b:
        print("Thread 2 acquired lock B")
        time.sleep(0.5)
        with lock_a:
            print("Thread 2 acquired lock A")
```

---

## Avoiding Deadlocks

- Acquire locks in a consistent order
- Use timeouts when acquiring locks
- Use higher-level synchronization (Queue)
- Avoid nested locks where possible

```python
import threading

# Two locks
lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1_safe():
    # Always acquire lock_a first, then lock_b
    with lock_a:
        print("Thread 1 acquired lock A")
        with lock_b:
            print("Thread 1 acquired lock B")

def thread_2_safe():
    # Same order: lock_a first, then lock_b
    with lock_a:
        print("Thread 2 acquired lock A")
        with lock_b:
            print("Thread 2 acquired lock B")
```

---

## Thread-Local Storage

- Data private to each thread
- Created with `threading.local()`
- Useful for thread-specific state or context
- Thread-safe without explicit synchronization

```python
import threading
import random

# Create thread-local data
thread_data = threading.local()

def worker():
    # Each thread has its own copy of thread_data.value
    thread_data.value = random.randint(1, 100)
    print(f"Thread {threading.current_thread().name}: {thread_data.value}")
    process_data()

def process_data():
    # Access the thread-local data
    print(f"Processing: {thread_data.value}")
```

---

## Thread Pools with concurrent.futures

- High-level interface for asynchronous execution
- `ThreadPoolExecutor` for thread-based parallelism
- Manages a pool of worker threads
- Submit tasks with `submit()` or `map()`
- Get results with `Future` objects

```python
import concurrent.futures
import time

def task(name):
    print(f"Task {name} starting")
    time.sleep(1)
    return f"Task {name} result"

# Create a thread pool with 5 worker threads
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Submit tasks and get Future objects
    futures = [executor.submit(task, i) for i in range(10)]

    # Process results as they complete
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        print(result)
```

---

## Python's multiprocessing Module

- Process-based parallelism
- Similar API to threading
- Bypasses the GIL limitation
- Each process has its own Python interpreter
- Inter-process communication mechanisms
- Process pools for task execution

---

## Process Creation

- `Process` class similar to `Thread`
- `start()`, `join()`, `is_alive()` methods
- Separate memory space

```python
import multiprocessing
import os
import time

def worker(name):
    print(f"Worker {name} (PID: {os.getpid()}) starting")
    time.sleep(1)
    print(f"Worker {name} finished")

if __name__ == "__main__":  # Required for Windows
    print(f"Main process PID: {os.getpid()}")

    # Create and start processes
    processes = []
    for i in range(3):
        p = multiprocessing.Process(target=worker, args=(i,))
        processes.append(p)
        p.start()

    # Wait for processes to complete
    for p in processes:
        p.join()
```

---

## Process vs Thread Memory Model: Details

- Processes have separate memory spaces
- Threads share memory within a process
- Process values are copied, not shared by default
- Explicit sharing mechanisms needed for processes

---

## Process vs Thread Memory Model

![process_vs_thread_memory_model](svg/courses/languages/python/advanced-python/20_multi_threading_multi_processing/process_vs_thread_memory_model.svg)

---

## Inter-Process Communication (IPC)

- Share data between Python processes
- multiprocessing module provides:
  1. Queue: thread and process safe FIFO queue
  1. Pipe: bidirectional communication channel
  1. Value/Array: shared memory objects
  1. Manager: proxy objects for sharing
  1. RLock, Event, Condition, Semaphore (like threading)

---

## Using Queue for IPC

- Thread and process safe FIFO queue
- `put()` and `get()` methods
- Useful for producer-consumer patterns

```python
import multiprocessing
import time

def producer(queue):
    print("Producer process starting")
    for i in range(5):
        item = f"Item {i}"
        queue.put(item)
        print(f"Produced: {item}")
        time.sleep(1)
    # Signal the end
    queue.put(None)

def consumer(queue):
    print("Consumer process starting")
    while True:
        item = queue.get()
        if item is None:  # End signal
            break
        print(f"Consumed: {item}")
```

---

## Pipes for IPC

- Bidirectional communication channel
- Returns a pair of connection objects
- Methods: `send()`, `recv()`, `poll()`
- More direct than Queue

```python
import multiprocessing
import time

def sender(conn):
    print("Sender process starting")
    conn.send("Hello")
    time.sleep(1)
    conn.send("World")
    conn.close()

def receiver(conn):
    print("Receiver process starting")
    print(f"Received: {conn.recv()}")
    print(f"Received: {conn.recv()}")
    conn.close()

if __name__ == "__main__":
    # Create a pipe
    parent_conn, child_conn = multiprocessing.Pipe()
```

---

## Shared Memory with Value and Array

- Direct memory sharing between processes
- `Value`: shared scalar value
- `Array`: shared array
- Faster than queues and pipes for large data
- Use lock for synchronization

```python
import multiprocessing

def worker(n, shared_value, lock):
    for _ in range(5):
        with lock:
            shared_value.value += 1
        print(f"Process {n}: value = {shared_value.value}")

if __name__ == "__main__":
    # Create a shared value and lock
    shared_value = multiprocessing.Value('i', 0)  # 'i' = integer
    lock = multiprocessing.Lock()

    # Create processes
    processes = []
    for i in range(3):
        p = multiprocessing.Process(
            target=worker,
            args=(i, shared_value, lock)
        )
        processes.append(p)
        p.start()
```

---

## Process Pools

- Manage a pool of worker processes
- Distribute tasks across processes
- `Pool` class from multiprocessing
- Methods: `apply()`, `apply_async()`, `map()`, `map_async()`

```python
import multiprocessing
import time
import os

def cpu_bound_task(n):
    print(f"Task {n} running on PID: {os.getpid()}")
    # CPU-intensive calculation
    total = sum(i*i for i in range(10**6))
    return f"Task {n} result: {total}"

if __name__ == "__main__":
    # Create a pool with one process per core
    with multiprocessing.Pool() as pool:
        # Map tasks to the pool
        results = pool.map(cpu_bound_task, range(4))
```

---

## ProcessPoolExecutor (concurrent.futures)

- Simpler interface for process pools
- Part of concurrent.futures module
- Similar to ThreadPoolExecutor
- Better for CPU-bound tasks

```python
import concurrent.futures
import math
import time

def complex_calculation(x):
    # Simulate a CPU-intensive task
    return sum(i*i for i in range(x * 100000))

if __name__ == "__main__":
    numbers = list(range(10))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(complex_calculation, numbers))
        for num, result in zip(numbers, results):
            print(f"Result for {num}: {result}")
```

---

## Choosing Between Process Pool and Thread Pool

```python
import concurrent.futures
import time
import requests

# I/O-bound task (network operation)
def download_url(url):
    response = requests.get(url)
    return f"{url}: {len(response.content)} bytes"

# CPU-bound task
def complex_calculation(n):
    return sum(i*i for i in range(n * 100000))

if __name__ == "__main__":
    urls = [
        "https://www.python.org",
        "https://www.google.com",
        "https://www.github.com",
    ]

    # I/O-bound: use ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(download_url, urls)

    # CPU-bound: use ProcessPoolExecutor
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(complex_calculation, range(5))
```

---

## Python's asyncio Module

- Event loop-based concurrency
- Cooperative multitasking with coroutines
- `async`/`await` syntax
- Single-threaded but concurrent
- Excellent for I/O-bound tasks
- No CPU parallelism (still bound by GIL)

```python
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)  # Non-blocking sleep
    print(what)
    return what

async def main():
    # Run coroutines concurrently
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    # Wait for both tasks to complete
    await task1
    await task2

asyncio.run(main())
```

---

## Combining Threading and Multiprocessing

- Use processes for CPU-bound tasks
- Use threads within each process for I/O-bound tasks
- Each process can have its own thread pool
- Hierarchical task decomposition
- Best of both worlds approach

---

## Worker Pool Pattern

- Pool of workers process tasks from a queue
- Tasks are independent and can be executed in parallel
- Results collected in order or as completed

```python
import concurrent.futures
import random
import time

def process_task(task):
    # Simulate variable processing time
    time.sleep(random.uniform(0.5, 1))
    return f"Task {task} processed"

if __name__ == "__main__":
    tasks = list(range(1, 10))

    with concurrent.futures.ProcessPoolExecutor() as executor:
        future_to_task = {
            executor.submit(process_task, task): task
            for task in tasks
        }

        for future in concurrent.futures.as_completed(future_to_task):
            task = future_to_task[future]
            result = future.result()
            print(result)
```

---

## Producer-Consumer Pattern

- Producer generates data or tasks
- Consumer processes data or tasks
- Queue acts as a buffer between them
- Multiple producers and consumers can work in parallel

```python
import multiprocessing
import time

def producer(queue, id, num_items):
    for i in range(num_items):
        item = f"Producer {id} - Item {i}"
        queue.put(item)
        print(f"Produced: {item}")
        time.sleep(0.5)

def consumer(queue, id):
    while True:
        try:
            item = queue.get(timeout=1)
            print(f"Consumer {id} got: {item}")
            time.sleep(0.5)
        except:
            break
```

---

## Pipeline Pattern

- Chain of stages connected by queues
- Each stage processes data and passes to next stage
- Can have different numbers of workers at each stage
- Especially useful for data processing workflows

```python
import multiprocessing

def stage1(input_queue, output_queue):
    while True:
        try:
            item = input_queue.get(timeout=1)
            if item is None:
                break
            processed = f"Stage 1 processed {item}"
            output_queue.put(processed)
        except:
            break
    output_queue.put(None)  # Signal end

def stage2(input_queue, output_queue):
    # Similar processing pattern
    pass
```

---

## Performance Considerations in Python

- GIL impact on threaded performance
- Process creation overhead
- Communication overhead between processes
- Memory usage with multiple processes
- CPU vs I/O bound task differentiation
- Serialization costs for IPC
- Thread/process pool sizing

---

## Debugging Concurrent Python Programs

- Use logging with process/thread IDs
- `multiprocessing.current_process().name`
- `threading.current_thread().name`
- Errors in subprocesses can be lost
- Race condition detection tools
- Set timeouts on operations
- Simplified test scenarios

---

## Testing Concurrent Code

- Create deterministic tests
- Avoid race conditions in tests
- Mock time-dependent functions
- Set reasonable timeouts
- Test edge cases (process failures, etc.)
- Use synchronization primitives in tests
- Consider stress testing with many iterations

---

## Python-Specific Concurrency Tips

- Understand the GIL and its impact
- Use processes for CPU-bound work
- Use threads or asyncio for I/O-bound work
- Minimize data sharing between processes
- Use higher-level abstractions (concurrent.futures)
- Avoid fine-grained parallelism with Python
- Consider Cython or C extensions for CPU bottlenecks
- Profile before parallelizing

---

## Real-World Applications

- Web scraping and crawling
- Web servers and API services
- Data processing pipelines
- Scientific computing
- Image and video processing
- Database operations
- Network services
- Task scheduling systems

---

## Summary

- Python offers multiple concurrency models
- GIL limits threading for CPU-bound tasks
- Multiprocessing bypasses GIL but has higher overhead
- Asyncio provides cooperative concurrency
- Choose the right model for your workload
- Consider hybrid approaches for complex tasks
- Higher-level abstractions simplify concurrent programming
- Understanding synchronization is key to correct programs
