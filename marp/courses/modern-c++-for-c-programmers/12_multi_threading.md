# Multithreading Techniques

---

## Course Overview

Modern C++ provides powerful built-in support for multithreading
- Thread creation and management
- Synchronization primitives
- Lock-free programming with atomics
- Asynchronous execution models
- Exception handling in concurrent code

---

## Why Multithreading?

Performance benefits of concurrent execution:
- Utilize multiple CPU cores
- Overlap I/O operations with computation
- Improve responsiveness in user interfaces
- Handle multiple clients simultaneously

---

## Threading Concepts

**Thread**: Independent execution path through a program
**Race Condition**: Unpredictable behavior when threads access shared data
**Synchronization**: Coordinating thread access to shared resources
**Deadlock**: Circular dependency where threads wait for each other

---

## Thread Lifecycle

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="80" height="40" fill="#e1f5fe" stroke="#0277bd" rx="5"/>
  <text x="90" y="75" text-anchor="middle" font-size="12">Created</text>

  <rect x="200" y="50" width="80" height="40" fill="#e8f5e8" stroke="#2e7d32" rx="5"/>
  <text x="240" y="75" text-anchor="middle" font-size="12">Running</text>

  <rect x="350" y="50" width="80" height="40" fill="#fff3e0" stroke="#f57c00" rx="5"/>
  <text x="390" y="75" text-anchor="middle" font-size="12">Blocked</text>

  <rect x="200" y="150" width="80" height="40" fill="#fce4ec" stroke="#c2185b" rx="5"/>
  <text x="240" y="175" text-anchor="middle" font-size="12">Terminated</text>

  <path d="M130 70 L200 70" stroke="#333" marker-end="url(#arrowhead)"/>
  <path d="M280 70 L350 70" stroke="#333" marker-end="url(#arrowhead)"/>
  <path d="M390 90 L390 120 L240 120 L240 90" stroke="#333" fill="none" marker-end="url(#arrowhead)"/>
  <path d="M240 90 L240 150" stroke="#333" marker-end="url(#arrowhead)"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Creating Threads

Basic thread creation with `std::thread`:

```cpp
#include <thread>
#include <iostream>

void worker_function() {
    std::cout << "Worker thread executing\n";
}

int main() {
    std::thread worker(worker_function);
    worker.join();  // Wait for completion
    return 0;
}
```

---

## Thread with Parameters

Passing arguments to thread functions:

```cpp
void print_numbers(int start, int end) {
    for (int i = start; i < end; ++i) {
        std::cout << i << " ";
    }
    std::cout << std::endl;
}

int main() {
    std::thread t1(print_numbers, 1, 5);
    std::thread t2(print_numbers, 10, 15);

    t1.join();
    t2.join();
    return 0;
}
```

---

## Lambda Functions with Threads

Using lambda expressions for thread tasks:

```cpp
int main() {
    int shared_value = 0;

    std::thread worker([&shared_value]() {
        for (int i = 0; i < 1000; ++i) {
            ++shared_value;  // Race condition!
        }
    });

    worker.join();
    std::cout << "Final value: " << shared_value << std::endl;
    return 0;
}
```

---

## The Race Condition Problem

Multiple threads accessing shared data without synchronization:

```cpp
#include <thread>
#include <vector>

int counter = 0;

void increment() {
    for (int i = 0; i < 100000; ++i) {
        ++counter;  // Not atomic!
    }
}

int main() {
    std::vector<std::thread> threads;

    for (int i = 0; i < 10; ++i) {
        threads.emplace_back(increment);
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "Counter: " << counter << std::endl;
    // Result is unpredictable!
    return 0;
}
```

---

## Mutex - Mutual Exclusion

`std::mutex` provides exclusive access to shared resources:

```cpp
#include <mutex>

std::mutex counter_mutex;
int counter = 0;

void safe_increment() {
    for (int i = 0; i < 100000; ++i) {
        counter_mutex.lock();
        ++counter;
        counter_mutex.unlock();
    }
}
```

---

## RAII Lock Management

Use `std::lock_guard` for automatic lock management:

```cpp
#include <mutex>

std::mutex counter_mutex;
int counter = 0;

void safe_increment() {
    for (int i = 0; i < 100000; ++i) {
        std::lock_guard<std::mutex> lock(counter_mutex);
        ++counter;
        // Lock automatically released when guard goes out of scope
    }
}
```

---

## Lock Guard Benefits

RAII ensures proper cleanup:
- Lock acquired in constructor
- Lock released in destructor
- Exception-safe
- No forgotten unlocks
- Clear scope boundaries

---

## Unique Lock

`std::unique_lock` provides more flexibility:

```cpp
std::mutex data_mutex;
std::string shared_data;

void process_data() {
    std::unique_lock<std::mutex> lock(data_mutex);

    if (shared_data.empty()) {
        lock.unlock();  // Release early
        // Do other work...
        lock.lock();    // Reacquire
    }

    shared_data += "processed";
    // Lock automatically released
}
```

---

## Deadlock Prevention

Avoid circular dependencies:

```cpp
std::mutex mutex1, mutex2;

// BAD: Potential deadlock
void function1() {
    std::lock_guard<std::mutex> lock1(mutex1);
    std::lock_guard<std::mutex> lock2(mutex2);
    // Work with both resources
}

void function2() {
    std::lock_guard<std::mutex> lock2(mutex2);  // Different order!
    std::lock_guard<std::mutex> lock1(mutex1);
    // Work with both resources
}
```

---

## Lock Multiple Mutexes

Use `std::lock` to acquire multiple locks safely:

```cpp
std::mutex mutex1, mutex2;

void safe_function() {
    std::unique_lock<std::mutex> lock1(mutex1, std::defer_lock);
    std::unique_lock<std::mutex> lock2(mutex2, std::defer_lock);

    std::lock(lock1, lock2);  // Deadlock-free acquisition

    // Work with both resources
    // Locks automatically released
}
```

---

## Shared Mutex

`std::shared_mutex` allows multiple readers, single writer:

```cpp
#include <shared_mutex>

std::shared_mutex rw_mutex;
std::string shared_resource;

void reader() {
    std::shared_lock<std::shared_mutex> lock(rw_mutex);
    std::cout << "Reading: " << shared_resource << std::endl;
    // Multiple readers can execute simultaneously
}

void writer() {
    std::unique_lock<std::shared_mutex> lock(rw_mutex);
    shared_resource = "New data";
    // Only one writer, blocks all readers
}
```

---

## Reader-Writer Pattern

<svg width="500" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="80" height="30" fill="#e1f5fe" stroke="#0277bd" rx="3"/>
  <text x="90" y="70" text-anchor="middle" font-size="11">Reader 1</text>

  <rect x="50" y="90" width="80" height="30" fill="#e1f5fe" stroke="#0277bd" rx="3"/>
  <text x="90" y="110" text-anchor="middle" font-size="11">Reader 2</text>

  <rect x="50" y="130" width="80" height="30" fill="#e1f5fe" stroke="#0277bd" rx="3"/>
  <text x="90" y="150" text-anchor="middle" font-size="11">Reader 3</text>

  <rect x="200" y="90" width="80" height="30" fill="#fff3e0" stroke="#f57c00" rx="3"/>
  <text x="240" y="110" text-anchor="middle" font-size="11">Writer</text>

  <rect x="350" y="90" width="100" height="30" fill="#e8f5e8" stroke="#2e7d32" rx="3"/>
  <text x="400" y="110" text-anchor="middle" font-size="11">Shared Data</text>

  <path d="M130 65 L350 105" stroke="#0277bd" stroke-dasharray="5,5"/>
  <path d="M130 105 L350 105" stroke="#0277bd" stroke-dasharray="5,5"/>
  <path d="M130 145 L350 105" stroke="#0277bd" stroke-dasharray="5,5"/>
  <path d="M280 105 L350 105" stroke="#f57c00" stroke-width="2"/>

  <text x="250" y="200" text-anchor="middle" font-size="12">Multiple readers OR single writer</text>
</svg>

---

## Atomic Variables

Lock-free operations with `std::atomic`:

```cpp
#include <atomic>

std::atomic<int> atomic_counter{0};

void atomic_increment() {
    for (int i = 0; i < 100000; ++i) {
        ++atomic_counter;  // Thread-safe without locks
    }
}

int main() {
    std::vector<std::thread> threads;

    for (int i = 0; i < 10; ++i) {
        threads.emplace_back(atomic_increment);
    }

    for (auto& t : threads) {
        t.join();
    }

    std::cout << "Counter: " << atomic_counter << std::endl;
    return 0;
}
```

---

## Atomic Operations

Common atomic operations:

```cpp
std::atomic<int> value{10};

// Atomic read/write
int old_val = value.load();
value.store(20);

// Atomic exchange
int prev = value.exchange(30);

// Compare and swap
int expected = 30;
bool success = value.compare_exchange_weak(expected, 40);

// Fetch and modify
int old_val = value.fetch_add(5);
```

---

## Memory Ordering

Control memory synchronization with ordering constraints:

```cpp
std::atomic<bool> ready{false};
std::atomic<int> data{0};

void producer() {
    data.store(42, std::memory_order_relaxed);
    ready.store(true, std::memory_order_release);
}

void consumer() {
    while (!ready.load(std::memory_order_acquire)) {
        // Wait for producer
    }
    int value = data.load(std::memory_order_relaxed);
    std::cout << "Received: " << value << std::endl;
}
```

---

## Condition Variables

Wait for specific conditions:

```cpp
#include <condition_variable>

std::mutex cv_mutex;
std::condition_variable cv;
bool ready = false;

void waiter() {
    std::unique_lock<std::mutex> lock(cv_mutex);
    cv.wait(lock, []{ return ready; });
    std::cout << "Condition met!" << std::endl;
}

void notifier() {
    std::this_thread::sleep_for(std::chrono::seconds(1));

    std::lock_guard<std::mutex> lock(cv_mutex);
    ready = true;
    cv.notify_one();
}
```

---

## Producer-Consumer Pattern

Classic synchronization problem:

```cpp
#include <queue>
#include <condition_variable>

class ThreadSafeQueue {
    std::queue<int> queue_;
    std::mutex mutex_;
    std::condition_variable condition_;

public:
    void push(int item) {
        std::lock_guard<std::mutex> lock(mutex_);
        queue_.push(item);
        condition_.notify_one();
    }

    int pop() {
        std::unique_lock<std::mutex> lock(mutex_);
        condition_.wait(lock, [this]{ return !queue_.empty(); });
        int result = queue_.front();
        queue_.pop();
        return result;
    }
};
```

---

## Producer Function

```cpp
void producer(ThreadSafeQueue& queue, int id) {
    for (int i = 0; i < 5; ++i) {
        int value = id * 10 + i;
        queue.push(value);
        std::cout << "Producer " << id << " pushed " << value << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}
```

---

## Consumer Function

```cpp
void consumer(ThreadSafeQueue& queue, int id) {
    for (int i = 0; i < 5; ++i) {
        int value = queue.pop();
        std::cout << "Consumer " << id << " popped " << value << std::endl;
        std::this_thread::sleep_for(std::chrono::milliseconds(150));
    }
}
```

---

## Complete Producer-Consumer Example

```cpp
int main() {
    ThreadSafeQueue queue;

    std::thread producer1(producer, std::ref(queue), 1);
    std::thread producer2(producer, std::ref(queue), 2);
    std::thread consumer1(consumer, std::ref(queue), 1);
    std::thread consumer2(consumer, std::ref(queue), 2);

    producer1.join();
    producer2.join();
    consumer1.join();
    consumer2.join();

    return 0;
}
```

---

## Asynchronous Execution

`std::async` for simple parallel tasks:

```cpp
#include <future>

int calculate_sum(int start, int end) {
    int sum = 0;
    for (int i = start; i <= end; ++i) {
        sum += i;
    }
    return sum;
}

int main() {
    auto future1 = std::async(std::launch::async, calculate_sum, 1, 1000);
    auto future2 = std::async(std::launch::async, calculate_sum, 1001, 2000);

    int result1 = future1.get();
    int result2 = future2.get();

    std::cout << "Total sum: " << (result1 + result2) << std::endl;
    return 0;
}
```

---

## Launch Policies

Control how async tasks execute:

```cpp
// Force asynchronous execution
auto future1 = std::async(std::launch::async, task);

// Allow deferred execution
auto future2 = std::async(std::launch::deferred, task);

// Let implementation decide
auto future3 = std::async(std::launch::async | std::launch::deferred, task);

// Default behavior
auto future4 = std::async(task);
```

---

## Promises and Futures

Manual result passing between threads:

```cpp
void producer_task(std::promise<int> promise) {
    // Simulate work
    std::this_thread::sleep_for(std::chrono::seconds(1));

    // Set result
    promise.set_value(42);
}

int main() {
    std::promise<int> promise;
    std::future<int> future = promise.get_future();

    std::thread worker(producer_task, std::move(promise));

    std::cout << "Waiting for result..." << std::endl;
    int result = future.get();
    std::cout << "Result: " << result << std::endl;

    worker.join();
    return 0;
}
```

---

## Exception Handling in Threads

Exceptions don't cross thread boundaries:

```cpp
void throwing_function() {
    throw std::runtime_error("Thread exception");
}

int main() {
    std::thread worker(throwing_function);

    try {
        worker.join();
    } catch (const std::exception& e) {
        // This will NOT catch the thread exception!
        std::cout << "Caught: " << e.what() << std::endl;
    }

    return 0;
}
```

---

## Exception Transport

Use promises to transport exceptions:

```cpp
void safe_throwing_function(std::promise<int> promise) {
    try {
        // Simulate work that might throw
        throw std::runtime_error("Something went wrong");
        promise.set_value(42);
    } catch (...) {
        promise.set_exception(std::current_exception());
    }
}

int main() {
    std::promise<int> promise;
    std::future<int> future = promise.get_future();

    std::thread worker(safe_throwing_function, std::move(promise));

    try {
        int result = future.get();
        std::cout << "Result: " << result << std::endl;
    } catch (const std::exception& e) {
        std::cout << "Caught exception: " << e.what() << std::endl;
    }

    worker.join();
    return 0;
}
```

---

## Thread Pool Concept

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="200" fill="#f5f5f5" stroke="#333" rx="5"/>
  <text x="125" y="40" text-anchor="middle" font-size="14" font-weight="bold">Task Queue</text>

  <rect x="70" y="70" width="110" height="25" fill="#e1f5fe" stroke="#0277bd" rx="3"/>
  <text x="125" y="87" text-anchor="middle" font-size="11">Task 1</text>

  <rect x="70" y="100" width="110" height="25" fill="#e1f5fe" stroke="#0277bd" rx="3"/>
  <text x="125" y="117" text-anchor="middle" font-size="11">Task 2</text>

  <rect x="70" y="130" width="110" height="25" fill="#e1f5fe" stroke="#0277bd" rx="3"/>
  <text x="125" y="147" text-anchor="middle" font-size="11">Task 3</text>

  <text x="125" y="180" text-anchor="middle" font-size="12">...</text>

  <rect x="250" y="70" width="80" height="40" fill="#e8f5e8" stroke="#2e7d32" rx="5"/>
  <text x="290" y="95" text-anchor="middle" font-size="11">Thread 1</text>

  <rect x="250" y="130" width="80" height="40" fill="#e8f5e8" stroke="#2e7d32" rx="5"/>
  <text x="290" y="155" text-anchor="middle" font-size="11">Thread 2</text>

  <rect x="250" y="190" width="80" height="40" fill="#e8f5e8" stroke="#2e7d32" rx="5"/>
  <text x="290" y="215" text-anchor="middle" font-size="11">Thread N</text>

  <path d="M200 90 L250 90" stroke="#333" marker-end="url(#arrowhead)"/>
  <path d="M200 150 L250 150" stroke="#333" marker-end="url(#arrowhead)"/>
  <path d="M200 210 L250 210" stroke="#333" marker-end="url(#arrowhead)"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Simple Thread Pool Implementation

```cpp
class ThreadPool {
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex queue_mutex;
    std::condition_variable condition;
    bool stop = false;

public:
    ThreadPool(size_t num_threads) {
        for (size_t i = 0; i < num_threads; ++i) {
            workers.emplace_back([this] {
                while (true) {
                    std::function<void()> task;

                    {
                        std::unique_lock<std::mutex> lock(queue_mutex);
                        condition.wait(lock, [this] { return stop || !tasks.empty(); });

                        if (stop && tasks.empty()) return;

                        task = std::move(tasks.front());
                        tasks.pop();
                    }

                    task();
                }
            });
        }
    }
```

---

## Thread Pool Task Submission

```cpp
    template<typename F>
    void enqueue(F&& f) {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            if (stop) {
                throw std::runtime_error("ThreadPool is stopped");
            }
            tasks.emplace(std::forward<F>(f));
        }
        condition.notify_one();
    }

    ~ThreadPool() {
        {
            std::unique_lock<std::mutex> lock(queue_mutex);
            stop = true;
        }

        condition.notify_all();

        for (std::thread& worker : workers) {
            worker.join();
        }
    }
};
```

---

## Using the Thread Pool

```cpp
int main() {
    ThreadPool pool(4);

    // Submit tasks
    for (int i = 0; i < 10; ++i) {
        pool.enqueue([i] {
            std::cout << "Task " << i << " executing on thread "
                      << std::this_thread::get_id() << std::endl;
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        });
    }

    // ThreadPool destructor will wait for all tasks to complete
    std::this_thread::sleep_for(std::chrono::seconds(2));
    return 0;
}
```

---

## Thread-Safe Singleton

Ensuring single instance in multithreaded environment:

```cpp
class ThreadSafeSingleton {
private:
    static std::once_flag initialized;
    static std::unique_ptr<ThreadSafeSingleton> instance;

    ThreadSafeSingleton() = default;

public:
    static ThreadSafeSingleton& getInstance() {
        std::call_once(initialized, [] {
            instance = std::make_unique<ThreadSafeSingleton>();
        });
        return *instance;
    }

    // Delete copy constructor and assignment
    ThreadSafeSingleton(const ThreadSafeSingleton&) = delete;
    ThreadSafeSingleton& operator=(const ThreadSafeSingleton&) = delete;
};

std::once_flag ThreadSafeSingleton::initialized;
std::unique_ptr<ThreadSafeSingleton> ThreadSafeSingleton::instance;
```

---

## Performance Considerations

Threading overhead factors:
- Thread creation/destruction cost
- Context switching overhead
- Memory synchronization penalties
- Cache coherency issues
- Lock contention

Best practices:
- Use thread pools for short-lived tasks
- Minimize shared state
- Prefer lock-free algorithms when possible
- Profile before optimizing

---

## Common Threading Pitfalls

1. **Race Conditions**: Unprotected shared data access
1. **Deadlocks**: Circular lock dependencies
1. **Priority Inversion**: Low-priority thread blocks high-priority
1. **Spurious Wakeups**: Condition variables may wake without reason
1. **Exception Safety**: Exceptions don't cross thread boundaries

---

## Debugging Multithreaded Code

Tools and techniques:
- Thread sanitizers (TSan)
- Helgrind (Valgrind)
- Visual Studio Concurrency Visualizer
- Print thread IDs for tracking
- Use debug builds with assertions
- Stress testing with high thread counts

---

## Testing Concurrent Code

```cpp
void stress_test_counter() {
    const int num_threads = 10;
    const int increments_per_thread = 100000;
    std::atomic<int> counter{0};

    auto start = std::chrono::high_resolution_clock::now();

    std::vector<std::thread> threads;
    for (int i = 0; i < num_threads; ++i) {
        threads.emplace_back([&counter, increments_per_thread] {
            for (int j = 0; j < increments_per_thread; ++j) {
                ++counter;
            }
        });
    }

    for (auto& t : threads) {
        t.join();
    }

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);

    std::cout << "Counter: " << counter << " (expected: "
              << num_threads * increments_per_thread << ")" << std::endl;
    std::cout << "Time: " << duration.count() << "ms" << std::endl;
}
```

---

## Best Practices Summary

1. **Prefer higher-level abstractions**: `std::async`, `std::future`
1. **Use RAII for lock management**: `std::lock_guard`, `std::unique_lock`
1. **Minimize shared state**: Reduce synchronization needs
1. **Choose appropriate synchronization**: Mutex vs atomic vs lock-free
1. **Handle exceptions properly**: Use promises for exception transport
1. **Design for composability**: Thread-safe building blocks
1. **Profile and measure**: Don't assume performance benefits

---

## Modern C++ Threading Benefits

C++11/14/17 improvements:
- Standardized threading library
- RAII-based lock management
- Atomic operations without inline assembly
- High-level async programming model
- Portable across platforms
- Type-safe thread communication
- Integration with standard library

---

## Practical Exercise

Implement a parallel file processor:
1. Create a thread pool
1. Process multiple files concurrently
1. Collect results safely
1. Handle errors appropriately
1. Measure performance improvement

**Focus on**: Thread safety, exception handling, resource management

---

## Key Takeaways

- Modern C++ provides comprehensive threading support
- RAII principles apply to synchronization primitives
- Atomic operations enable lock-free programming
- Higher-level abstractions reduce complexity
- Exception safety requires special attention in concurrent code
- Performance benefits require careful design and measurement
