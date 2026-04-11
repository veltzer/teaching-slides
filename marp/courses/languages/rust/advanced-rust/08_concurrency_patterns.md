---
tags:
  - languages:rust
  - concepts:programming
  - concepts:concurrency
level: advanced
category: language
audience:
  - audiences:developers

---
# Concurrency Patterns

Channels, Shared State, Data Parallelism, and Advanced Patterns

---
## Overview

- Channels: `mpsc`, `crossbeam-channel`
- Shared state: `Mutex`, `RwLock`, atomics
- Lock-free data structures introduction
- Rayon for data parallelism
- `Arc` patterns
- Deadlock prevention strategies
- Concurrent collections (`DashMap`)
- Thread pools
- Scoped threads (`std::thread::scope`)
- Actor pattern with channels

---
## Part 1: Channels

Message passing for safe concurrency

---
## std::sync::mpsc Basics

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    // mpsc = Multiple Producer, Single Consumer
    let (tx, rx) = mpsc::channel();

    thread::spawn(move || {
        tx.send("Hello from thread!".to_string()).unwrap();
        tx.send("Another message".to_string()).unwrap();
    });

    // recv() blocks until a message arrives
    println!("{}", rx.recv().unwrap());
    println!("{}", rx.recv().unwrap());
}
```

---
## std::sync::mpsc Basics

![std_sync_mpsc_basics](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/std_sync_mpsc_basics.svg)

---
## Multiple Producers

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (tx, rx) = mpsc::channel();

    // Clone the sender for each producer thread
    for i in 0..4 {
        let tx = tx.clone();
        thread::spawn(move || {
            for j in 0..3 {
                tx.send(format!("Thread {}: message {}", i, j)).unwrap();
            }
        });
    }

    // Drop the original sender so the channel closes when all clones drop
    drop(tx);

    // Iterate over received messages until channel closes
    for msg in rx {
        println!("{}", msg);
    }

    println!("All producers done.");
}
```

---
## Synchronous (Bounded) Channels

```rust
use std::sync::mpsc;
use std::thread;
use std::time::Duration;

fn main() {
    // sync_channel with buffer size 2
    // send() blocks when buffer is full (backpressure)
    let (tx, rx) = mpsc::sync_channel(2);

    thread::spawn(move || {
        for i in 0..5 {
            println!("Sending {}", i);
            tx.send(i).unwrap(); // Blocks when buffer is full
            println!("Sent {}", i);
        }
    });

    for _ in 0..5 {
        thread::sleep(Duration::from_millis(500));
        let val = rx.recv().unwrap();
        println!("Received: {}", val);
    }
}
```

| Channel Type      | Buffer   | Send Behavior            |
|-------------------|----------|--------------------------|
| `channel()`       | Infinite | Never blocks             |
| `sync_channel(0)` | None     | Blocks until recv called |
| `sync_channel(n)` | n items  | Blocks when full         |

---
## Channel Types Comparison

![channel_types_comparison](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/channel_types_comparison.svg)

---
## Crossbeam Channels

```rust
// Cargo.toml: crossbeam-channel = "0.5"
use crossbeam_channel::{bounded, select, unbounded, Receiver, Sender};
use std::thread;
use std::time::Duration;

fn main() {
    let (tx1, rx1) = bounded::<String>(10);
    let (tx2, rx2) = bounded::<String>(10);

    // Producer 1
    thread::spawn(move || {
        for i in 0..5 {
            thread::sleep(Duration::from_millis(100));
            tx1.send(format!("fast-{}", i)).unwrap();
        }
    });

    // Producer 2
    thread::spawn(move || {
        for i in 0..3 {
            thread::sleep(Duration::from_millis(250));
            tx2.send(format!("slow-{}", i)).unwrap();
        }
    });

    // Select across multiple channels (like Go's select)
    loop {
        select! {
            recv(rx1) -> msg => match msg {
                Ok(m) => println!("Channel 1: {}", m),
                Err(_) => println!("Channel 1 closed"),
            },
            recv(rx2) -> msg => match msg {
                Ok(m) => println!("Channel 2: {}", m),
                Err(_) => println!("Channel 2 closed"),
            },
            default(Duration::from_secs(1)) => {
                println!("Timeout, exiting");
                break;
            }
        }
    }
}
```

---
## Crossbeam vs std::sync::mpsc

![crossbeam_vs_std_sync_mpsc](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/crossbeam_vs_std_sync_mpsc.svg)

---
## Channel Patterns: Fan-Out / Fan-In

```rust
use std::sync::mpsc;
use std::thread;

fn main() {
    let (result_tx, result_rx) = mpsc::channel();

    // Fan-out: distribute work to multiple workers
    let items = vec![1, 2, 3, 4, 5, 6, 7, 8];
    let chunk_size = 2;

    for chunk in items.chunks(chunk_size) {
        let tx = result_tx.clone();
        let data = chunk.to_vec();
        thread::spawn(move || {
            let sum: i32 = data.iter().map(|x| x * x).sum();
            tx.send(sum).unwrap();
        });
    }
    drop(result_tx);

    // Fan-in: collect results
    let total: i32 = result_rx.iter().sum();
    println!("Sum of squares: {}", total); // 204
}
```

---
## Channel Patterns: Fan-Out / Fan-In

![channel_patterns_fan_out_fan_in](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/channel_patterns_fan_out_fan_in.svg)

---
## Part 2: Shared State

Mutex, RwLock, and Atomics

---
## Mutex Basics

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let counter = Arc::new(Mutex::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            // lock() returns a MutexGuard (RAII)
            let mut num = counter.lock().unwrap();
            *num += 1;
            // MutexGuard dropped here, releasing the lock
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Final count: {}", *counter.lock().unwrap()); // 10
}
```

---
## Mutex Poisoning

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let data = Arc::new(Mutex::new(vec![1, 2, 3]));

    let data_clone = Arc::clone(&data);
    let handle = thread::spawn(move || {
        let mut guard = data_clone.lock().unwrap();
        guard.push(4);
        panic!("Thread panicked while holding the lock!");
    });

    let _ = handle.join(); // Thread panicked

    // The mutex is now "poisoned"
    match data.lock() {
        Ok(guard) => println!("Data: {:?}", *guard),
        Err(poisoned) => {
            // We can still recover the data
            let guard = poisoned.into_inner();
            println!("Recovered from poisoned mutex: {:?}", *guard);
        }
    }
}
```

---
## RwLock: Multiple Readers, Single Writer

```rust
use std::sync::{Arc, RwLock};
use std::thread;
use std::time::Duration;

fn main() {
    let config = Arc::new(RwLock::new(vec![
        ("host".to_string(), "localhost".to_string()),
        ("port".to_string(), "8080".to_string()),
    ]));

    // Multiple readers can acquire the lock simultaneously
    for i in 0..4 {
        let config = Arc::clone(&config);
        thread::spawn(move || {
            let reader = config.read().unwrap();
            println!("Reader {}: {:?}", i, *reader);
            thread::sleep(Duration::from_millis(100));
            // Multiple readers coexist here
        });
    }

    thread::sleep(Duration::from_millis(50));

    // Writer gets exclusive access
    {
        let mut writer = config.write().unwrap();
        writer.push(("timeout".to_string(), "30".to_string()));
        println!("Writer updated config");
    }

    thread::sleep(Duration::from_millis(200));
    println!("Final config: {:?}", *config.read().unwrap());
}
```

---
## When to Use Mutex vs RwLock

![when_to_use_mutex_vs_rwlock](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/when_to_use_mutex_vs_rwlock.svg)

---
## Atomic Types

```rust
use std::sync::atomic::{AtomicU64, AtomicBool, Ordering};
use std::sync::Arc;
use std::thread;

fn main() {
    let counter = Arc::new(AtomicU64::new(0));
    let running = Arc::new(AtomicBool::new(true));

    let mut handles = vec![];

    for _ in 0..4 {
        let counter = Arc::clone(&counter);
        let running = Arc::clone(&running);
        handles.push(thread::spawn(move || {
            while running.load(Ordering::Relaxed) {
                counter.fetch_add(1, Ordering::Relaxed);
                if counter.load(Ordering::Relaxed) >= 1_000_000 {
                    running.store(false, Ordering::Relaxed);
                }
            }
        }));
    }

    for h in handles {
        h.join().unwrap();
    }

    println!("Final count: {}", counter.load(Ordering::Relaxed));
}
```

---
## Atomic Orderings Explained

![atomic_orderings_explained](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/atomic_orderings_explained.svg)

---
## Acquire/Release Pattern

```rust
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Arc;
use std::thread;

fn main() {
    let data = Arc::new(AtomicU64::new(0));
    let ready = Arc::new(AtomicBool::new(false));

    let data_clone = Arc::clone(&data);
    let ready_clone = Arc::clone(&ready);

    // Producer: write data, then signal ready
    let producer = thread::spawn(move || {
        data_clone.store(42, Ordering::Relaxed);
        // Release ensures the store above is visible
        // to any thread that does an Acquire load of `ready`
        ready_clone.store(true, Ordering::Release);
    });

    // Consumer: wait for ready, then read data
    let consumer = thread::spawn(move || {
        // Spin until ready (Acquire pairs with Release)
        while !ready.load(Ordering::Acquire) {
            std::hint::spin_loop();
        }
        // Guaranteed to see data = 42
        assert_eq!(data.load(Ordering::Relaxed), 42);
        println!("Data: {}", data.load(Ordering::Relaxed));
    });

    producer.join().unwrap();
    consumer.join().unwrap();
}
```

---
## Compare-and-Swap (CAS)

```rust
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::thread;

/// Lock-free stack push using CAS
fn atomic_max(val: &AtomicUsize, new: usize) {
    let mut current = val.load(Ordering::Relaxed);
    loop {
        if current >= new {
            return; // Current value is already >= new
        }
        // Try to swap: if val still == current, set it to new
        match val.compare_exchange_weak(
            current,
            new,
            Ordering::AcqRel,
            Ordering::Relaxed,
        ) {
            Ok(_) => return,         // Successfully updated
            Err(actual) => current = actual, // Someone else changed it, retry
        }
    }
}

fn main() {
    let max_val = Arc::new(AtomicUsize::new(0));
    let mut handles = vec![];

    for i in 0..100 {
        let max_val = Arc::clone(&max_val);
        handles.push(thread::spawn(move || {
            atomic_max(&max_val, i);
        }));
    }

    for h in handles {
        h.join().unwrap();
    }

    println!("Max: {}", max_val.load(Ordering::Relaxed)); // 99
}
```

---
## Part 3: Lock-Free Data Structures

An introduction to lock-free programming

---
## Lock-Free Queue Operations

![lock_free_queue_operations](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/lock_free_queue_operations.svg)

---
## Lock-Free Stack (Treiber Stack)

```rust
use std::sync::atomic::{AtomicPtr, Ordering};
use std::ptr;

struct Node<T> {
    data: T,
    next: *mut Node<T>,
}

pub struct LockFreeStack<T> {
    head: AtomicPtr<Node<T>>,
}

unsafe impl<T: Send> Send for LockFreeStack<T> {}
unsafe impl<T: Send> Sync for LockFreeStack<T> {}

impl<T> LockFreeStack<T> {
    pub fn new() -> Self {
        LockFreeStack {
            head: AtomicPtr::new(ptr::null_mut()),
        }
    }

    pub fn push(&self, data: T) {
        let new_node = Box::into_raw(Box::new(Node {
            data,
            next: ptr::null_mut(),
        }));

        loop {
            let old_head = self.head.load(Ordering::Acquire);
            unsafe { (*new_node).next = old_head; }

            if self.head
                .compare_exchange_weak(old_head, new_node, Ordering::Release, Ordering::Relaxed)
                .is_ok()
            {
                break;
            }
        }
    }

    pub fn pop(&self) -> Option<T> {
        loop {
            let old_head = self.head.load(Ordering::Acquire);
            if old_head.is_null() {
                return None;
            }

            let next = unsafe { (*old_head).next };

            if self.head
                .compare_exchange_weak(old_head, next, Ordering::Release, Ordering::Relaxed)
                .is_ok()
            {
                let node = unsafe { Box::from_raw(old_head) };
                return Some(node.data);
            }
        }
    }
}

fn main() {
    use std::sync::Arc;
    use std::thread;

    let stack = Arc::new(LockFreeStack::new());

    // Push from multiple threads
    let mut handles = vec![];
    for i in 0..8 {
        let stack = Arc::clone(&stack);
        handles.push(thread::spawn(move || {
            for j in 0..100 {
                stack.push(i * 100 + j);
            }
        }));
    }
    for h in handles {
        h.join().unwrap();
    }

    // Pop all items
    let mut count = 0;
    while stack.pop().is_some() {
        count += 1;
    }
    println!("Popped {} items", count); // 800
}
```

---
## Lock-Free vs Lock-Based Trade-offs

![lock_free_vs_lock_based_trade_offs](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/lock_free_vs_lock_based_trade_offs.svg)

---
## Rayon Work Stealing

![rayon_work_stealing](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/rayon_work_stealing.svg)

---
## Part 4: Rayon for Data Parallelism

Effortless parallel iterators

---
## Rayon Basics: par_iter

```rust
// Cargo.toml: rayon = "1.10"
use rayon::prelude::*;

fn main() {
    let numbers: Vec<u64> = (1..=10_000_000).collect();

    // Sequential
    let seq_sum: u64 = numbers.iter().map(|&x| x * x).sum();

    // Parallel -- just change iter() to par_iter()
    let par_sum: u64 = numbers.par_iter().map(|&x| x * x).sum();

    assert_eq!(seq_sum, par_sum);
    println!("Sum of squares: {}", par_sum);
}
```

---
## Rayon Basics: par_iter

![rayon_basics_pariter](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/rayon_basics_pariter.svg)

---
## Rayon: Parallel Sorting and Searching

```rust
use rayon::prelude::*;

fn main() {
    let mut data: Vec<i32> = (0..1_000_000).rev().collect();

    // Parallel sort
    data.par_sort();
    assert!(data.windows(2).all(|w| w[0] <= w[1]));
    println!("Sorted {} elements", data.len());

    // Parallel sort with custom comparator
    let mut words = vec!["banana", "apple", "cherry", "date"];
    words.par_sort_by(|a, b| a.len().cmp(&b.len()));
    println!("{:?}", words);

    // Parallel find
    let big_data: Vec<u64> = (0..10_000_000).collect();
    let found = big_data.par_iter().find_any(|&&x| x == 7_777_777);
    println!("Found: {:?}", found);

    // Parallel all/any
    let all_positive = big_data.par_iter().all(|&x| x < 10_000_000);
    let has_zero = big_data.par_iter().any(|&x| x == 0);
    println!("All positive: {}, has zero: {}", all_positive, has_zero);
}
```

---
## Rayon: par_bridge for Non-Rayon Iterators

```rust
use rayon::prelude::*;
use std::io::{BufRead, BufReader, Cursor};

fn main() {
    // Simulate reading lines from a file
    let data = "line one\nline two\nline three\nline four\nline five\n";
    let reader = BufReader::new(Cursor::new(data));

    // par_bridge() converts any Iterator into a ParallelIterator
    let results: Vec<String> = reader
        .lines()
        .map(|l| l.unwrap())
        .par_bridge()
        .map(|line| {
            // Process each line in parallel
            format!("Processed: {}", line.to_uppercase())
        })
        .collect();

    for r in &results {
        println!("{}", r);
    }
}
```

Note: `par_bridge()` has overhead compared to `par_iter()` because it cannot split the input evenly. Use `par_iter()` when you have a slice or vector.

---
## Work Stealing Scheduler

![work_stealing_scheduler](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/work_stealing_scheduler.svg)

---
## Rayon: Custom Thread Pool

```rust
use rayon::prelude::*;
use rayon::ThreadPoolBuilder;

fn main() {
    // Configure a custom thread pool
    let pool = ThreadPoolBuilder::new()
        .num_threads(4)
        .thread_name(|i| format!("worker-{}", i))
        .build()
        .unwrap();

    // Run work on the custom pool
    pool.install(|| {
        let data: Vec<i32> = (0..1000).collect();
        let sum: i32 = data.par_iter().sum();
        println!("Sum: {} (computed with 4 threads)", sum);
    });

    // The global pool is separate and uses all CPUs by default
    let global_sum: i32 = (0..1000).into_par_iter().sum();
    println!("Global pool sum: {}", global_sum);
}
```

---
## Rayon: Parallel Reduction and Fold

```rust
use rayon::prelude::*;

fn main() {
    let words = vec!["hello", "world", "rust", "is", "fast"];

    // reduce: combine results in parallel
    // Identity function must satisfy: op(identity, x) == x
    let longest = words.par_iter().reduce(
        || &"",
        |a, b| if a.len() >= b.len() { a } else { b },
    );
    println!("Longest: {}", longest);

    // fold + reduce: fold per-thread, then reduce across threads
    let numbers: Vec<i32> = (1..=100).collect();

    let (sum, count) = numbers
        .par_iter()
        .fold(
            || (0i64, 0usize),                    // per-thread identity
            |(sum, count), &x| (sum + x as i64, count + 1), // per-thread fold
        )
        .reduce(
            || (0, 0),                             // reduction identity
            |(s1, c1), (s2, c2)| (s1 + s2, c1 + c2), // combine thread results
        );

    println!("Sum: {}, Count: {}, Avg: {:.1}", sum, count, sum as f64 / count as f64);
}
```

---
## Part 5: Arc Patterns

Sharing ownership across threads

---
## Arc with Interior Mutability

```rust
use std::sync::{Arc, Mutex, RwLock};
use std::thread;

/// Common patterns for shared mutable state across threads
fn main() {
    // Pattern 1: Arc<Mutex<T>> for mutable shared state
    let shared_vec = Arc::new(Mutex::new(Vec::<i32>::new()));

    let mut handles = vec![];
    for i in 0..4 {
        let vec = Arc::clone(&shared_vec);
        handles.push(thread::spawn(move || {
            let mut v = vec.lock().unwrap();
            v.push(i);
        }));
    }
    for h in handles { h.join().unwrap(); }
    println!("Vec: {:?}", shared_vec.lock().unwrap());

    // Pattern 2: Arc<RwLock<T>> for read-heavy shared state
    let config = Arc::new(RwLock::new(String::from("v1.0")));

    let readers: Vec<_> = (0..4).map(|i| {
        let cfg = Arc::clone(&config);
        thread::spawn(move || {
            let val = cfg.read().unwrap();
            println!("Reader {}: {}", i, *val);
        })
    }).collect();

    for r in readers { r.join().unwrap(); }

    // Pattern 3: Arc<T> for read-only sharing (no lock needed)
    let shared_data = Arc::new(vec![1, 2, 3, 4, 5]);
    let handles: Vec<_> = (0..4).map(|i| {
        let data = Arc::clone(&shared_data);
        thread::spawn(move || {
            println!("Thread {}: sum = {}", i, data.iter().sum::<i32>());
        })
    }).collect();
    for h in handles { h.join().unwrap(); }
}
```

---
## Arc::new_cyclic and Weak References

```rust
use std::sync::{Arc, Weak, Mutex};

struct Node {
    id: usize,
    parent: Option<Weak<Mutex<Node>>>,
    children: Vec<Arc<Mutex<Node>>>,
}

fn main() {
    // Create a parent node
    let parent = Arc::new(Mutex::new(Node {
        id: 0,
        parent: None,
        children: vec![],
    }));

    // Create a child that references the parent via Weak
    let child = Arc::new(Mutex::new(Node {
        id: 1,
        parent: Some(Arc::downgrade(&parent)),
        children: vec![],
    }));

    // Add child to parent
    parent.lock().unwrap().children.push(Arc::clone(&child));

    // Access parent from child
    let child_lock = child.lock().unwrap();
    if let Some(weak_parent) = &child_lock.parent {
        if let Some(strong_parent) = weak_parent.upgrade() {
            println!("Child {} -> Parent {}", child_lock.id,
                     strong_parent.lock().unwrap().id);
        }
    }

    // Weak references do not prevent deallocation
    println!("Strong count: {}", Arc::strong_count(&parent)); // 1
    println!("Weak count: {}", Arc::weak_count(&parent));     // 1
}
```

---
## Part 6: Deadlock Prevention

Strategies to avoid deadlocks

---
## Classic Deadlock

```rust
use std::sync::{Arc, Mutex};
use std::thread;

fn main() {
    let lock_a = Arc::new(Mutex::new("A"));
    let lock_b = Arc::new(Mutex::new("B"));

    let a = Arc::clone(&lock_a);
    let b = Arc::clone(&lock_b);

    // Thread 1: locks A, then B
    let t1 = thread::spawn(move || {
        let _a = a.lock().unwrap();
        // Small delay makes deadlock more likely
        thread::sleep(std::time::Duration::from_millis(10));
        let _b = b.lock().unwrap(); // DEADLOCK: thread 2 holds B
        println!("Thread 1 got both locks");
    });

    let a = Arc::clone(&lock_a);
    let b = Arc::clone(&lock_b);

    // Thread 2: locks B, then A
    let t2 = thread::spawn(move || {
        let _b = b.lock().unwrap();
        thread::sleep(std::time::Duration::from_millis(10));
        let _a = a.lock().unwrap(); // DEADLOCK: thread 1 holds A
        println!("Thread 2 got both locks");
    });

    // This program will hang forever!
    t1.join().unwrap();
    t2.join().unwrap();
}
```

---
## Deadlock Prevention Strategies

![deadlock_prevention_strategies](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/deadlock_prevention_strategies.svg)

---
## Lock Ordering Solution

```rust
use std::sync::{Arc, Mutex};
use std::thread;

/// Always lock in a consistent order based on address
fn lock_two<'a, T>(
    a: &'a Mutex<T>,
    b: &'a Mutex<T>,
) -> (std::sync::MutexGuard<'a, T>, std::sync::MutexGuard<'a, T>) {
    // Use pointer addresses to determine order
    let addr_a = a as *const _ as usize;
    let addr_b = b as *const _ as usize;

    if addr_a < addr_b {
        let ga = a.lock().unwrap();
        let gb = b.lock().unwrap();
        (ga, gb)
    } else {
        let gb = b.lock().unwrap();
        let ga = a.lock().unwrap();
        (ga, gb)
    }
}

fn main() {
    let lock_a = Arc::new(Mutex::new(1));
    let lock_b = Arc::new(Mutex::new(2));

    let a1 = Arc::clone(&lock_a);
    let b1 = Arc::clone(&lock_b);
    let t1 = thread::spawn(move || {
        let (mut ga, mut gb) = lock_two(&a1, &b1);
        *ga += 10;
        *gb += 10;
        println!("Thread 1: a={}, b={}", *ga, *gb);
    });

    let a2 = Arc::clone(&lock_a);
    let b2 = Arc::clone(&lock_b);
    let t2 = thread::spawn(move || {
        let (mut ga, mut gb) = lock_two(&b2, &a2);
        *ga += 100;
        *gb += 100;
        println!("Thread 2: a={}, b={}", *gb, *ga);
    });

    t1.join().unwrap();
    t2.join().unwrap();
}
```

---
## try_lock with Backoff

```rust
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

fn try_lock_both(
    a: &Mutex<i32>,
    b: &Mutex<i32>,
) -> (i32, i32) {
    loop {
        // Try to acquire both locks without blocking
        if let Ok(ga) = a.try_lock() {
            if let Ok(gb) = b.try_lock() {
                return (*ga, *gb);
            }
            // Could not get b, release a and retry
        }
        // Backoff before retrying to reduce contention
        thread::sleep(Duration::from_micros(100));
    }
}

fn main() {
    let a = Arc::new(Mutex::new(1));
    let b = Arc::new(Mutex::new(2));

    let a1 = Arc::clone(&a);
    let b1 = Arc::clone(&b);
    let t1 = thread::spawn(move || {
        let (va, vb) = try_lock_both(&a1, &b1);
        println!("Thread 1: a={}, b={}", va, vb);
    });

    let a2 = Arc::clone(&a);
    let b2 = Arc::clone(&b);
    let t2 = thread::spawn(move || {
        let (va, vb) = try_lock_both(&b2, &a2);
        println!("Thread 2: a={}, b={}", va, vb);
    });

    t1.join().unwrap();
    t2.join().unwrap();
}
```

---
## Concurrent Data Structures

![concurrent_data_structures](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/concurrent_data_structures.svg)

---
## Part 7: Concurrent Collections

DashMap and friends

---
## DashMap: Concurrent HashMap

```rust
// Cargo.toml: dashmap = "6"
use dashmap::DashMap;
use std::sync::Arc;
use std::thread;

fn main() {
    let map = Arc::new(DashMap::new());

    // Multiple threads can read and write simultaneously
    let mut handles = vec![];
    for i in 0..8 {
        let map = Arc::clone(&map);
        handles.push(thread::spawn(move || {
            for j in 0..100 {
                let key = format!("key-{}-{}", i, j);
                map.insert(key.clone(), i * 100 + j);
            }

            // Read while others are writing
            if let Some(entry) = map.get(&format!("key-{}-0", i)) {
                println!("Thread {} read: {}", i, *entry);
            }
        }));
    }

    for h in handles { h.join().unwrap(); }
    println!("Total entries: {}", map.len()); // 800

    // Iterate over entries
    let sum: i32 = map.iter().map(|entry| *entry.value()).sum();
    println!("Sum of all values: {}", sum);
}
```

---
## DashMap: Advanced Operations

```rust
use dashmap::DashMap;

fn main() {
    let scores: DashMap<String, Vec<i32>> = DashMap::new();

    // entry API: insert-or-update pattern
    scores.entry("alice".to_string()).or_insert_with(Vec::new).push(95);
    scores.entry("alice".to_string()).or_insert_with(Vec::new).push(87);
    scores.entry("bob".to_string()).or_insert_with(Vec::new).push(72);

    // alter: modify a value in-place
    scores.alter("alice", |_, mut v| {
        v.push(100);
        v
    });

    // retain: remove entries that don't match
    scores.retain(|_key, val| val.len() > 1);

    println!("Remaining entries: {}", scores.len()); // 1 (alice)

    for entry in scores.iter() {
        println!("{}: {:?}", entry.key(), entry.value());
    }
}
```

---
## DashMap vs Mutex<HashMap>

![dashmap_vs_mutex](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/dashmap_vs_mutex.svg)

---
## Part 8: Thread Pools

Managing threads efficiently

---
## Thread Pool Architecture

![thread_pool_architecture](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/thread_pool_architecture.svg)

---
## Building a Simple Thread Pool

```rust
use std::sync::{mpsc, Arc, Mutex};
use std::thread;

type Job = Box<dyn FnOnce() + Send + 'static>;

struct ThreadPool {
    workers: Vec<thread::JoinHandle<()>>,
    sender: Option<mpsc::Sender<Job>>,
}

impl ThreadPool {
    fn new(size: usize) -> Self {
        let (sender, receiver) = mpsc::channel::<Job>();
        let receiver = Arc::new(Mutex::new(receiver));

        let workers: Vec<_> = (0..size)
            .map(|id| {
                let rx = Arc::clone(&receiver);
                thread::spawn(move || {
                    loop {
                        // Lock the receiver to get the next job
                        let job = rx.lock().unwrap().recv();
                        match job {
                            Ok(job) => {
                                println!("Worker {} executing job", id);
                                job();
                            }
                            Err(_) => {
                                println!("Worker {} shutting down", id);
                                break;
                            }
                        }
                    }
                })
            })
            .collect();

        ThreadPool {
            workers,
            sender: Some(sender),
        }
    }

    fn execute<F: FnOnce() + Send + 'static>(&self, f: F) {
        self.sender.as_ref().unwrap().send(Box::new(f)).unwrap();
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        // Drop sender to signal workers to stop
        self.sender.take();
        for worker in self.workers.drain(..) {
            worker.join().unwrap();
        }
    }
}

fn main() {
    let pool = ThreadPool::new(4);

    for i in 0..8 {
        pool.execute(move || {
            println!("Task {} running on {:?}", i, thread::current().id());
            thread::sleep(std::time::Duration::from_millis(100));
        });
    }

    // Pool is dropped here, waits for all tasks to complete
}
```

---
## Part 9: Scoped Threads

Borrowing stack data in threads

---
## std::thread::scope (Rust 1.63+)

```rust
use std::thread;

fn main() {
    let mut data = vec![1, 2, 3, 4, 5, 6, 7, 8];
    let len = data.len();

    // Scoped threads can borrow local variables!
    // No need for Arc or 'static bounds.
    thread::scope(|s| {
        // Split mutable borrow into non-overlapping slices
        let (left, right) = data.split_at_mut(len / 2);

        s.spawn(|| {
            for val in left.iter_mut() {
                *val *= 2;
            }
            println!("Left done: {:?}", left);
        });

        s.spawn(|| {
            for val in right.iter_mut() {
                *val *= 3;
            }
            println!("Right done: {:?}", right);
        });

        // All spawned threads are joined here automatically
    });

    // data is accessible again after scope ends
    println!("Result: {:?}", data);
    // [2, 4, 6, 8, 15, 18, 21, 24]
}
```

---
## Scoped Threads: Shared Read Access

```rust
use std::thread;

fn main() {
    let matrix = vec![
        vec![1, 2, 3],
        vec![4, 5, 6],
        vec![7, 8, 9],
    ];

    // Multiple threads can immutably borrow the same data
    let row_sums: Vec<i32> = thread::scope(|s| {
        let handles: Vec<_> = matrix
            .iter()
            .map(|row| {
                s.spawn(|| -> i32 {
                    // Borrows row from the outer scope
                    row.iter().sum()
                })
            })
            .collect();

        handles
            .into_iter()
            .map(|h| h.join().unwrap())
            .collect()
    });

    println!("Row sums: {:?}", row_sums); // [6, 15, 24]
    println!("Total: {}", row_sums.iter().sum::<i32>()); // 45
}
```

---
## Scoped Threads vs Regular Threads

![scoped_threads_vs_regular_threads](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/scoped_threads_vs_regular_threads.svg)

---
## Part 10: Actor Pattern

Message-driven concurrency

---
## Actor Model Architecture

![actor_model_architecture](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/actor_model_architecture.svg)

---
## Actor Pattern with Channels

```rust
use std::sync::mpsc;
use std::thread;

// Messages the actor can receive
enum BankMessage {
    Deposit(f64),
    Withdraw(f64),
    GetBalance(mpsc::Sender<f64>),
    Shutdown,
}

// The actor: owns its state, processes messages sequentially
fn bank_account_actor(rx: mpsc::Receiver<BankMessage>) {
    let mut balance = 0.0_f64;

    for msg in rx {
        match msg {
            BankMessage::Deposit(amount) => {
                balance += amount;
                println!("Deposited {:.2}, balance: {:.2}", amount, balance);
            }
            BankMessage::Withdraw(amount) => {
                if balance >= amount {
                    balance -= amount;
                    println!("Withdrew {:.2}, balance: {:.2}", amount, balance);
                } else {
                    println!("Insufficient funds for {:.2}, balance: {:.2}",
                             amount, balance);
                }
            }
            BankMessage::GetBalance(reply) => {
                reply.send(balance).unwrap();
            }
            BankMessage::Shutdown => {
                println!("Account shutting down, final balance: {:.2}", balance);
                break;
            }
        }
    }
}

fn main() {
    let (tx, rx) = mpsc::channel();
    let actor = thread::spawn(move || bank_account_actor(rx));

    // Multiple "clients" can send messages
    let tx1 = tx.clone();
    let client1 = thread::spawn(move || {
        tx1.send(BankMessage::Deposit(100.0)).unwrap();
        tx1.send(BankMessage::Deposit(50.0)).unwrap();
    });

    let tx2 = tx.clone();
    let client2 = thread::spawn(move || {
        tx2.send(BankMessage::Withdraw(30.0)).unwrap();
    });

    client1.join().unwrap();
    client2.join().unwrap();

    // Query balance
    let (reply_tx, reply_rx) = mpsc::channel();
    tx.send(BankMessage::GetBalance(reply_tx)).unwrap();
    println!("Balance query result: {:.2}", reply_rx.recv().unwrap());

    tx.send(BankMessage::Shutdown).unwrap();
    actor.join().unwrap();
}
```

---
## Actor Pattern: Multiple Actors

```rust
use std::collections::HashMap;
use std::sync::mpsc;
use std::thread;

type ActorId = usize;

enum RouterMessage {
    Send { to: ActorId, payload: String },
    Register { id: ActorId, tx: mpsc::Sender<String> },
    Shutdown,
}

fn router(rx: mpsc::Receiver<RouterMessage>) {
    let mut actors: HashMap<ActorId, mpsc::Sender<String>> = HashMap::new();

    for msg in rx {
        match msg {
            RouterMessage::Register { id, tx } => {
                println!("Router: registered actor {}", id);
                actors.insert(id, tx);
            }
            RouterMessage::Send { to, payload } => {
                if let Some(tx) = actors.get(&to) {
                    let _ = tx.send(payload);
                } else {
                    println!("Router: actor {} not found", to);
                }
            }
            RouterMessage::Shutdown => {
                println!("Router shutting down");
                break;
            }
        }
    }
}

fn worker_actor(id: ActorId, rx: mpsc::Receiver<String>) {
    for msg in rx {
        println!("Actor {}: received '{}'", id, msg);
    }
    println!("Actor {}: shutting down", id);
}

fn main() {
    let (router_tx, router_rx) = mpsc::channel();
    let router_handle = thread::spawn(move || router(router_rx));

    // Spawn worker actors and register them
    let mut worker_handles = vec![];
    for id in 0..3 {
        let (worker_tx, worker_rx) = mpsc::channel();
        router_tx
            .send(RouterMessage::Register { id, tx: worker_tx })
            .unwrap();
        worker_handles.push(thread::spawn(move || worker_actor(id, worker_rx)));
    }

    // Send messages through the router
    for i in 0..9 {
        router_tx
            .send(RouterMessage::Send {
                to: i % 3,
                payload: format!("message-{}", i),
            })
            .unwrap();
    }

    router_tx.send(RouterMessage::Shutdown).unwrap();
    router_handle.join().unwrap();

    // Workers shut down when their senders are dropped
    for h in worker_handles {
        h.join().unwrap();
    }
}
```

---
## Actor Pattern: Benefits

![actor_pattern_benefits](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/actor_pattern_benefits.svg)

---
## Summary

![summary](svg/courses/languages/rust/advanced-rust/08_concurrency_patterns/summary.svg)

---
## Exercises

1. Implement a producer-consumer pipeline using `crossbeam-channel` with `select!` and a timeout.
1. Build a concurrent word-frequency counter using `DashMap` and scoped threads.
1. Convert a sequential image-processing pipeline to use `rayon::par_iter`.
1. Implement a lock-free counter using `AtomicU64` with `compare_exchange`.
1. Build a chat room using the actor pattern where each user is an actor.
1. Create a thread pool that supports task priorities (hint: use `BinaryHeap` behind a `Mutex`).
