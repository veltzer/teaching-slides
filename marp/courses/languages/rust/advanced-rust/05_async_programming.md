# Async Programming

Futures, async/await, Tokio, Streams, and Patterns

---

## Overview

- The `Future` trait in depth
- async/await desugaring
- `Pin` and `Unpin` explained
- Tokio runtime internals
- Async I/O patterns
- Streams
- `select!`, `join!`, cancellation safety
- Async traits
- Common async pitfalls

---

## Part 1: The Future Trait

The foundation of async Rust

---

## The Future Trait Definition

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

pub enum Poll<T> {
    Ready(T),
    Pending,
}
```

A Future is a value that:
- May not have finished computing yet
- Can be polled to check if it is done
- Returns `Pending` with a waker to be notified later

---

## Implementing Future Manually

```rust
use std::pin::Pin;
use std::task::{Context, Poll};
use std::future::Future;

struct CountDown {
    remaining: u32,
}

impl Future for CountDown {
    type Output = String;

    fn poll(mut self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<String> {
        if self.remaining == 0 {
            Poll::Ready("Done!".to_string())
        } else {
            self.remaining -= 1;
            // Wake the task so it gets polled again
            cx.waker().wake_by_ref();
            Poll::Pending
        }
    }
}

#[tokio::main]
async fn main() {
    let result = CountDown { remaining: 5 }.await;
    println!("{}", result); // "Done!"
}
```

---

## The Waker Mechanism

The waker tells the executor: "this future is ready to make progress, poll it again."

---

## The Waker Mechanism

![the_waker_mechanism](svg/courses/languages/rust/advanced-rust/05_async_programming/the_waker_mechanism.svg)

---

## Building a Timer Future

```rust
use std::future::Future;
use std::pin::Pin;
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Waker};
use std::thread;
use std::time::Duration;

struct TimerFuture {
    shared: Arc<Mutex<SharedState>>,
}

struct SharedState {
    completed: bool,
    waker: Option<Waker>,
}

impl Future for TimerFuture {
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        let mut shared = self.shared.lock().unwrap();
        if shared.completed {
            Poll::Ready(())
        } else {
            shared.waker = Some(cx.waker().clone());
            Poll::Pending
        }
    }
}

impl TimerFuture {
    fn new(duration: Duration) -> Self {
        let shared = Arc::new(Mutex::new(SharedState {
            completed: false,
            waker: None,
        }));
        let shared_clone = shared.clone();
        thread::spawn(move || {
            thread::sleep(duration);
            let mut state = shared_clone.lock().unwrap();
            state.completed = true;
            if let Some(waker) = state.waker.take() {
                waker.wake();
            }
        });
        TimerFuture { shared }
    }
}
```

---

## Part 2: async/await Desugaring

What the compiler generates

---

## Basic Desugaring

```rust
// What you write:
async fn fetch_data(url: &str) -> String {
    let response = make_request(url).await;
    let body = read_body(response).await;
    body
}

// What the compiler (conceptually) generates:
enum FetchDataFuture<'a> {
    State0 { url: &'a str },
    State1 { url: &'a str, response_future: MakeRequestFuture<'a> },
    State2 { response: Response, body_future: ReadBodyFuture },
    Done,
}

impl<'a> Future for FetchDataFuture<'a> {
    type Output = String;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<String> {
        // State machine that advances through states
        // Each .await point is a state transition
        todo!()
    }
}
```

---

## State Machine Visualization

![state_machine_visualization](svg/courses/languages/rust/advanced-rust/05_async_programming/state_machine_visualization.svg)

---

## Async Blocks

```rust
#[tokio::main]
async fn main() {
    // async blocks create anonymous futures
    let future = async {
        println!("Computing...");
        42
    };

    // Nothing happens until we await
    let result = future.await;
    println!("Result: {}", result);

    // async move blocks capture variables by value
    let name = String::from("Rust");
    let greeting = async move {
        format!("Hello, {}!", name)
    };
    // name is moved into the future
    // println!("{}", name); // ERROR: name is moved

    println!("{}", greeting.await);
}
```

---

## Part 3: Pin and Unpin

Why async needs pinning

---

## Why Pin Exists

```rust
// An async fn that holds a reference across an await point:
async fn problematic() {
    let data = vec![1, 2, 3];
    let reference = &data; // reference points to data on this future's stack

    some_async_op().await; // Future might be moved here!

    println!("{:?}", reference); // reference would be invalid if moved
}

// The generated state machine:
// struct ProblematicFuture {
//     data: Vec<i32>,
//     reference: *const Vec<i32>, // Points to self.data!
// }
//
// If this struct is moved in memory, reference becomes dangling.
// Pin prevents this move.
```

---

## Pin API

```rust
use std::pin::Pin;

// Pin<P> wraps a pointer P and prevents moving the pointee
// unless the pointee implements Unpin

fn pin_examples() {
    // Pinning on the heap (common)
    let boxed = Box::pin(42);
    let _: Pin<Box<i32>> = boxed;

    // Pinning on the stack (using macro)
    let mut val = 42;
    let pinned = Pin::new(&mut val); // OK because i32: Unpin

    // For !Unpin types, use Box::pin or tokio::pin!
}

// Most types implement Unpin automatically
// Exceptions: futures generated by async fn, types with PhantomPinned

// If T: Unpin, Pin<&mut T> is equivalent to &mut T
fn unpin_is_transparent<T: Unpin>(val: Pin<&mut T>) -> &mut T {
    val.get_mut()
}
```

---

## Pin in Practice

```rust
use std::pin::Pin;
use std::future::Future;

// Accepting pinned futures
async fn run_future<F: Future<Output = i32>>(fut: F) -> i32 {
    fut.await
}

// When you need to pin manually (e.g., select!)
use tokio::pin;

#[tokio::main]
async fn main() {
    let fut1 = async { 1 };
    let fut2 = async { 2 };

    // tokio::pin! pins the futures on the stack
    pin!(fut1);
    pin!(fut2);

    // Now fut1 and fut2 are Pin<&mut impl Future>
    // Required for tokio::select! and similar APIs
    tokio::select! {
        val = &mut fut1 => println!("fut1 completed: {}", val),
        val = &mut fut2 => println!("fut2 completed: {}", val),
    }
}
```

---

## Part 4: Tokio Runtime Internals

How the async executor works

---

## Tokio Architecture

![tokio_architecture](svg/courses/languages/rust/advanced-rust/05_async_programming/tokio_architecture.svg)

---

## Runtime Configuration

```rust
use tokio::runtime::Builder;

// Multi-threaded runtime (default with #[tokio::main])
let rt = Builder::new_multi_thread()
    .worker_threads(4)          // Number of worker threads
    .max_blocking_threads(512)  // For spawn_blocking
    .enable_all()               // Enable I/O and timer drivers
    .thread_name("my-worker")
    .on_thread_start(|| println!("Worker thread started"))
    .build()
    .unwrap();

// Single-threaded runtime (current_thread)
let rt = Builder::new_current_thread()
    .enable_all()
    .build()
    .unwrap();

rt.block_on(async {
    println!("Running on runtime");
});
```

---

## Task Spawning Strategies

```rust
use tokio::task;

#[tokio::main]
async fn main() {
    // Spawn a task on the runtime (requires Send + 'static)
    let handle = task::spawn(async {
        expensive_computation().await
    });

    // Spawn blocking work on a dedicated thread pool
    let result = task::spawn_blocking(|| {
        // CPU-intensive or blocking I/O work
        std::thread::sleep(std::time::Duration::from_secs(1));
        42
    }).await.unwrap();

    // Spawn a !Send future on the current thread
    let local = task::LocalSet::new();
    local.run_until(async {
        task::spawn_local(async {
            // This future does not need to be Send
            let rc = std::rc::Rc::new(42);
            println!("Local: {}", rc);
        }).await.unwrap();
    }).await;
}
```

---

## Part 5: Async I/O Patterns

Real-world async programming

---

## Concurrent HTTP Requests

```rust
use reqwest;
use tokio;

async fn fetch_url(url: &str) -> Result<String, reqwest::Error> {
    reqwest::get(url).await?.text().await
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let urls = vec![
        "https://httpbin.org/get",
        "https://httpbin.org/ip",
        "https://httpbin.org/user-agent",
    ];

    // Launch all requests concurrently
    let mut handles = Vec::new();
    for url in urls {
        handles.push(tokio::spawn(async move {
            match fetch_url(url).await {
                Ok(body) => println!("{}: {} bytes", url, body.len()),
                Err(e) => eprintln!("{}: error: {}", url, e),
            }
        }));
    }

    // Wait for all to complete
    for handle in handles {
        handle.await?;
    }

    Ok(())
}
```

---

## Bounded Concurrency with Semaphore

```rust
use std::sync::Arc;
use tokio::sync::Semaphore;

#[tokio::main]
async fn main() {
    let urls: Vec<String> = (0..100)
        .map(|i| format!("https://httpbin.org/delay/{}", i % 3))
        .collect();

    // Limit to 10 concurrent requests
    let semaphore = Arc::new(Semaphore::new(10));
    let mut handles = Vec::new();

    for url in urls {
        let sem = semaphore.clone();
        handles.push(tokio::spawn(async move {
            let _permit = sem.acquire().await.unwrap();
            // Only 10 requests run at a time
            let result = reqwest::get(&url).await;
            drop(_permit); // Release permit
            result
        }));
    }

    for handle in handles {
        let _ = handle.await;
    }
}
```

---

## TCP Server with Tokio

```rust
use tokio::net::TcpListener;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    println!("Listening on :8080");

    loop {
        let (mut socket, addr) = listener.accept().await?;
        println!("Connection from: {}", addr);

        tokio::spawn(async move {
            let mut buf = [0u8; 1024];
            loop {
                match socket.read(&mut buf).await {
                    Ok(0) => break, // Connection closed
                    Ok(n) => {
                        // Echo back
                        if socket.write_all(&buf[..n]).await.is_err() {
                            break;
                        }
                    }
                    Err(_) => break,
                }
            }
        });
    }
}
```

---

## Graceful Shutdown

```rust
use tokio::signal;
use tokio::sync::broadcast;

#[tokio::main]
async fn main() {
    let (shutdown_tx, _) = broadcast::channel::<()>(1);

    // Spawn worker tasks
    for i in 0..4 {
        let mut shutdown_rx = shutdown_tx.subscribe();
        tokio::spawn(async move {
            loop {
                tokio::select! {
                    _ = shutdown_rx.recv() => {
                        println!("Worker {} shutting down", i);
                        break;
                    }
                    _ = do_work(i) => {
                        // Continue working
                    }
                }
            }
        });
    }

    // Wait for Ctrl+C
    signal::ctrl_c().await.expect("Failed to listen for ctrl+c");
    println!("Shutdown signal received");
    drop(shutdown_tx); // All receivers will get an error, triggering shutdown
    tokio::time::sleep(std::time::Duration::from_secs(1)).await;
}

async fn do_work(id: usize) {
    tokio::time::sleep(std::time::Duration::from_secs(1)).await;
    println!("Worker {} did work", id);
}
```

---

## Part 6: Streams

Async iterators

---

## The Stream Trait

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

// From the futures crate
pub trait Stream {
    type Item;

    fn poll_next(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>,
    ) -> Poll<Option<Self::Item>>;
}

// Stream is to Iterator as Future is to a plain value
//
// Iterator::next()   -> Option<Item>        (sync)
// Stream::poll_next() -> Poll<Option<Item>> (async)
```

---

## Creating Streams

```rust
use tokio_stream::{self as stream, StreamExt};
use std::time::Duration;

#[tokio::main]
async fn main() {
    // From an iterator
    let mut s = stream::iter(vec![1, 2, 3]);
    while let Some(val) = s.next().await {
        println!("Got: {}", val);
    }

    // Interval stream
    let mut interval = tokio_stream::wrappers::IntervalStream::new(
        tokio::time::interval(Duration::from_millis(100))
    );

    let mut count = 0;
    while let Some(_tick) = interval.next().await {
        count += 1;
        println!("Tick {}", count);
        if count >= 5 { break; }
    }
}
```

---

## Stream Combinators

```rust
use tokio_stream::{self as stream, StreamExt};

#[tokio::main]
async fn main() {
    let numbers = stream::iter(1..=20);

    // filter, map, take - like iterators but async
    let result: Vec<i32> = numbers
        .filter(|x| x % 2 == 0)    // Even numbers
        .map(|x| x * x)            // Square them
        .take(5)                    // First 5
        .collect()
        .await;

    println!("{:?}", result); // [4, 16, 36, 64, 100]

    // fold
    let sum = stream::iter(1..=10)
        .fold(0i32, |acc, x| async move { acc + x })
        .await;
    println!("Sum: {}", sum); // 55
}
```

---

## Async Channels as Streams

```rust
use tokio::sync::mpsc;
use tokio_stream::wrappers::ReceiverStream;
use tokio_stream::StreamExt;

#[tokio::main]
async fn main() {
    let (tx, rx) = mpsc::channel(32);

    // Producer
    tokio::spawn(async move {
        for i in 0..10 {
            tx.send(i).await.unwrap();
            tokio::time::sleep(std::time::Duration::from_millis(50)).await;
        }
    });

    // Convert receiver to a stream
    let mut stream = ReceiverStream::new(rx);

    // Consume as a stream with combinators
    while let Some(value) = stream.next().await {
        println!("Received: {}", value);
    }
}
```

---

## Part 7: select! and join!

Combining multiple futures

---

## tokio::join! - Run All to Completion

```rust
use tokio::time::{sleep, Duration};

async fn fetch_user() -> String {
    sleep(Duration::from_millis(200)).await;
    "Alice".to_string()
}

async fn fetch_orders() -> Vec<u32> {
    sleep(Duration::from_millis(300)).await;
    vec![1, 2, 3]
}

async fn fetch_balance() -> f64 {
    sleep(Duration::from_millis(100)).await;
    1234.56
}

#[tokio::main]
async fn main() {
    // All three run concurrently, total time ~300ms (not 600ms)
    let (user, orders, balance) = tokio::join!(
        fetch_user(),
        fetch_orders(),
        fetch_balance(),
    );
    println!("{} has {} orders, balance: {}", user, orders.len(), balance);
}
```

---

## tokio::try_join! - Short-Circuit on Error

```rust
use tokio::time::{sleep, Duration};

async fn might_fail(succeed: bool) -> Result<String, String> {
    sleep(Duration::from_millis(100)).await;
    if succeed {
        Ok("Success".into())
    } else {
        Err("Failed".into())
    }
}

#[tokio::main]
async fn main() {
    // If any future returns Err, try_join! returns immediately
    let result = tokio::try_join!(
        might_fail(true),
        might_fail(false), // This will fail
        might_fail(true),
    );

    match result {
        Ok((a, b, c)) => println!("All succeeded: {}, {}, {}", a, b, c),
        Err(e) => println!("One failed: {}", e),
    }
}
```

---

## tokio::select! - First to Complete Wins

```rust
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    tokio::select! {
        val = async {
            sleep(Duration::from_millis(100)).await;
            "fast"
        } => {
            println!("Fast completed: {}", val);
        }
        val = async {
            sleep(Duration::from_millis(500)).await;
            "slow"
        } => {
            println!("Slow completed: {}", val);
        }
    }
    // Output: "Fast completed: fast"
    // The slow future is DROPPED (cancelled)
}
```

---

## select! with Channels

```rust
use tokio::sync::mpsc;
use tokio::time::{sleep, Duration};

#[tokio::main]
async fn main() {
    let (tx1, mut rx1) = mpsc::channel::<String>(1);
    let (tx2, mut rx2) = mpsc::channel::<String>(1);

    tokio::spawn(async move {
        sleep(Duration::from_millis(100)).await;
        tx1.send("from channel 1".into()).await.unwrap();
    });

    tokio::spawn(async move {
        sleep(Duration::from_millis(200)).await;
        tx2.send("from channel 2".into()).await.unwrap();
    });

    // Loop with select to handle messages from either channel
    for _ in 0..2 {
        tokio::select! {
            Some(msg) = rx1.recv() => println!("rx1: {}", msg),
            Some(msg) = rx2.recv() => println!("rx2: {}", msg),
        }
    }
}
```

---

## Part 8: Cancellation Safety

A critical concern with select!

---

## The Cancellation Problem

```rust
use tokio::sync::mpsc;

async fn read_exact_two(rx: &mut mpsc::Receiver<String>) -> (String, String) {
    let first = rx.recv().await.unwrap();
    let second = rx.recv().await.unwrap(); // If cancelled here, first is lost!
    (first, second)
}

#[tokio::main]
async fn main() {
    let (tx, mut rx) = mpsc::channel(10);

    // If used in select!, read_exact_two might be cancelled
    // between the first and second recv, losing the first message

    tokio::select! {
        pair = read_exact_two(&mut rx) => {
            println!("Got pair: {:?}", pair);
        }
        _ = tokio::time::sleep(std::time::Duration::from_secs(1)) => {
            println!("Timeout - first message may be lost!");
        }
    }
}
```

---

## Cancellation-Safe Patterns

```rust
use tokio::sync::mpsc;

// Solution: Use a buffer to preserve partial state
struct MessageCollector {
    buffer: Vec<String>,
    target: usize,
}

impl MessageCollector {
    fn new(target: usize) -> Self {
        MessageCollector { buffer: Vec::new(), target }
    }

    // This is cancellation-safe: no partial state is lost
    async fn recv_one(&mut self, rx: &mut mpsc::Receiver<String>) -> Option<Vec<String>> {
        let msg = rx.recv().await?;
        self.buffer.push(msg);
        if self.buffer.len() >= self.target {
            Some(std::mem::take(&mut self.buffer))
        } else {
            None
        }
    }
}

// Cancellation-safe operations:
// - mpsc::Receiver::recv() - safe
// - oneshot::Receiver - safe
// - TcpListener::accept() - safe
// - tokio::time::sleep() - safe
//
// NOT cancellation-safe:
// - read_exact() - may have read partial data
// - read_to_end() - may have read partial data
```

---

## Part 9: Async Traits

Using async in trait definitions

---

## Async Traits (Rust 1.75+)

```rust
// Since Rust 1.75, async fn in traits works directly
trait DataStore {
    async fn get(&self, key: &str) -> Option<String>;
    async fn set(&mut self, key: &str, value: String);
    async fn delete(&mut self, key: &str) -> bool;
}

struct InMemoryStore {
    data: std::collections::HashMap<String, String>,
}

impl DataStore for InMemoryStore {
    async fn get(&self, key: &str) -> Option<String> {
        self.data.get(key).cloned()
    }

    async fn set(&mut self, key: &str, value: String) {
        self.data.insert(key.to_string(), value);
    }

    async fn delete(&mut self, key: &str) -> bool {
        self.data.remove(key).is_some()
    }
}
```

---

## Async Traits with dyn Dispatch

```rust
// async fn in traits does NOT work with dyn dispatch directly
// because async fn returns an opaque future type (different per impl)

// Solution: use the async_trait crate for dynamic dispatch
use async_trait::async_trait;

#[async_trait]
trait Repository {
    async fn find_by_id(&self, id: u64) -> Option<String>;
    async fn save(&self, id: u64, data: String) -> Result<(), String>;
}

#[async_trait]
impl Repository for MyDatabase {
    async fn find_by_id(&self, id: u64) -> Option<String> {
        // Makes a database query
        Some(format!("Record {}", id))
    }

    async fn save(&self, id: u64, data: String) -> Result<(), String> {
        Ok(())
    }
}

// Now works with dyn dispatch:
async fn use_repo(repo: &dyn Repository) {
    let item = repo.find_by_id(42).await;
    println!("{:?}", item);
}
```

---

## Send Bounds on Async Trait Methods

```rust
use async_trait::async_trait;

// By default, async_trait requires Send futures
// (needed for tokio::spawn)
#[async_trait]
trait SendService {
    async fn process(&self) -> String; // Future is Send
}

// Opt out of Send requirement for single-threaded runtimes
#[async_trait(?Send)]
trait LocalService {
    async fn process(&self) -> String; // Future is NOT Send
}

// This matters when your async method uses !Send types
struct LocalState {
    rc: std::rc::Rc<String>, // Rc is !Send
}

#[async_trait(?Send)]
impl LocalService for LocalState {
    async fn process(&self) -> String {
        self.rc.to_string()
    }
}
```

---

## Part 10: Common Async Pitfalls

Mistakes and how to avoid them

---

## Pitfall 1: Blocking the Runtime

```rust
// WRONG: This blocks a worker thread!
#[tokio::main]
async fn main() {
    let data = std::fs::read_to_string("big_file.txt").unwrap(); // BLOCKING!
    std::thread::sleep(std::time::Duration::from_secs(5));       // BLOCKING!
    println!("{}", data.len());
}

// RIGHT: Use async versions or spawn_blocking
#[tokio::main]
async fn main() {
    // Option 1: Use tokio's async I/O
    let data = tokio::fs::read_to_string("big_file.txt").await.unwrap();

    // Option 2: Offload to blocking thread pool
    let result = tokio::task::spawn_blocking(|| {
        std::thread::sleep(std::time::Duration::from_secs(5));
        "done"
    }).await.unwrap();

    println!("{}", result);
}
```

---

## Pitfall 2: Holding Locks Across Await

```rust
use std::sync::Mutex;
use tokio::sync::Mutex as TokioMutex;

// WRONG: std::sync::Mutex held across .await
async fn bad(data: &Mutex<Vec<String>>) {
    let mut guard = data.lock().unwrap();
    some_async_op().await; // Other tasks on this thread are blocked!
    guard.push("item".into());
}

// RIGHT: Use tokio::sync::Mutex for async contexts
async fn good(data: &TokioMutex<Vec<String>>) {
    let mut guard = data.lock().await;
    some_async_op().await; // OK: tokio Mutex yields properly
    guard.push("item".into());
}

// ALSO RIGHT: Drop the lock before awaiting
async fn also_good(data: &Mutex<Vec<String>>) {
    {
        let mut guard = data.lock().unwrap();
        guard.push("item".into());
    } // Lock released here
    some_async_op().await; // Safe
}

async fn some_async_op() {}
```

---

## Pitfall 3: Forgetting to Await

```rust
#[tokio::main]
async fn main() {
    // WRONG: Future is created but never polled!
    async_operation(); // Returns a Future but does nothing
    // Compiler warning: unused Future

    // RIGHT: Await the future
    async_operation().await;

    // Or spawn it as a task
    tokio::spawn(async_operation());
}

async fn async_operation() {
    println!("This runs!");
}
```

---

## Pitfall 4: Send Bounds with Spawn

```rust
use std::rc::Rc;

#[tokio::main]
async fn main() {
    // WRONG: Rc is !Send, cannot spawn across threads
    // tokio::spawn(async {
    //     let rc = Rc::new(42);
    //     tokio::time::sleep(std::time::Duration::from_secs(1)).await;
    //     println!("{}", rc); // ERROR: future is not Send
    // });

    // RIGHT: Use Arc instead
    use std::sync::Arc;
    tokio::spawn(async {
        let arc = Arc::new(42);
        tokio::time::sleep(std::time::Duration::from_secs(1)).await;
        println!("{}", arc); // OK: Arc is Send
    });

    // OR: Use spawn_local for !Send futures
    let local = tokio::task::LocalSet::new();
    local.run_until(async {
        tokio::task::spawn_local(async {
            let rc = Rc::new(42);
            println!("{}", rc);
        }).await.unwrap();
    }).await;
}
```

---

## Pitfall 5: Async Recursion

```rust
// WRONG: Infinite-size future type
// async fn factorial(n: u64) -> u64 {
//     if n <= 1 { 1 }
//     else { n * factorial(n - 1).await }
// }
// ERROR: recursive async fn has infinite size

// RIGHT: Box the recursive call
fn factorial(n: u64) -> std::pin::Pin<Box<dyn std::future::Future<Output = u64>>> {
    Box::pin(async move {
        if n <= 1 {
            1
        } else {
            n * factorial(n - 1).await
        }
    })
}

// Or use the async_recursion crate:
// #[async_recursion]
// async fn factorial(n: u64) -> u64 {
//     if n <= 1 { 1 } else { n * factorial(n - 1).await }
// }
```

---

## Summary

![summary](svg/courses/languages/rust/advanced-rust/05_async_programming/summary.svg)

---

## Exercises

1. Implement a custom `Future` that resolves after being polled N times.
1. Build an async TCP echo server with graceful shutdown using `select!`.
1. Create a rate-limited HTTP client using `Semaphore` and streams.
1. Implement a producer-consumer pattern with multiple producers using channels.
1. Write a parallel web scraper that limits concurrency and handles errors gracefully.
1. Benchmark `join!` vs sequential awaits to measure concurrency benefits.
