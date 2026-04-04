# Async Programming
## Chapter 9: Asynchronous Programming in Rust

---

## Why Async

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_async" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Sync vs Async Execution Model</text>
  <rect x="20" y="30" width="170" height="65" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="48" text-anchor="middle" font-size="10" font-weight="bold">Synchronous</text>
  <text x="105" y="63" text-anchor="middle" font-size="9">1 thread per connection</text>
  <text x="105" y="76" text-anchor="middle" font-size="9">Blocks on I/O (idle CPU)</text>
  <text x="105" y="89" text-anchor="middle" font-size="9">10K threads = high overhead</text>
  <rect x="215" y="30" width="170" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="48" text-anchor="middle" font-size="10" font-weight="bold">Async (Rust)</text>
  <text x="300" y="63" text-anchor="middle" font-size="9">Many tasks on few threads</text>
  <text x="300" y="76" text-anchor="middle" font-size="9">Yields on .await (no block)</text>
  <text x="300" y="89" text-anchor="middle" font-size="9">100K+ tasks, low overhead</text>
  <rect x="410" y="30" width="170" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="48" text-anchor="middle" font-size="10" font-weight="bold">Tokio Runtime</text>
  <text x="495" y="63" text-anchor="middle" font-size="9">Executor: polls Futures</text>
  <text x="495" y="76" text-anchor="middle" font-size="9">Reactor: watches I/O</text>
  <text x="495" y="89" text-anchor="middle" font-size="9">Work-stealing scheduler</text>
  <line x1="190" y1="62" x2="215" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arr_async)"/>
  <line x1="385" y1="62" x2="410" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arr_async)"/>
  <rect x="50" y="110" width="500" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="125" text-anchor="middle" font-size="10" font-weight="bold">async fn -> impl Future: compiler transforms to state machine</text>
  <text x="300" y="139" text-anchor="middle" font-size="9">Each .await is a yield point. No threads blocked. No callback hell.</text>
  <rect x="100" y="160" width="400" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="180" text-anchor="middle" font-size="10">Use async for I/O-bound work; use threads for CPU-bound work</text>
</svg>

---

## Async/Await Basics

```rust
async fn hello_world() {
    println!("hello, world!");
}

#[tokio::main]
async fn main() {
    hello_world().await;
}
```

---

## Futures

```rust
use std::future::Future;

// A Future represents an asynchronous computation
async fn example() -> i32 {
    42
}

// The type is impl Future<Output = i32>
let future = example();
```

---

## Async Runtime: Tokio

```rust
use tokio;

#[tokio::main]
async fn main() {
    // Spawn an async task
    tokio::spawn(async {
        println!("Hello from task!");
    });
    println!("Hello from main!");
}
```

---

## Task Spawning

```rust
#[tokio::main]
async fn main() {
    let handle = tokio::spawn(async {
        // Long running operation
        tokio::time::sleep(Duration::from_secs(1)).await;
        42
    });
    let result = handle.await.unwrap();
    println!("Got: {}", result);
}
```

---

## Async Streams

```rust
use tokio_stream::{self as stream, StreamExt};

async fn process_stream() {
    let mut stream = stream::iter(1..=3);

    while let Some(num) = stream.next().await {
        println!("Got: {}", num);
    }
}
```

---

## Error Handling in Async

```rust
async fn fetch_data() -> Result<String, Error> {
    let response = reqwest::get("https://example.com").await?;

    let body = response.text().await?;
    Ok(body)
}
```

---

## Async IO Operations

```rust
use tokio::fs::File;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

async fn read_file() -> Result<(), std::io::Error> {
    let mut file = File::open("hello.txt").await?;
    let mut contents = String::new();
    file.read_to_string(&mut contents).await?;
    Ok(())
}
```

---

## Select! Macro

```rust
use tokio::select;

async fn process() {
    let mut interval = tokio::time::interval(Duration::from_secs(1));
    select! {
        _ = interval.tick() => println!("Tick"),
        Some(msg) = rx.recv() => println!("Got message: {}", msg),
        else => println!("No message received"),
    }
}
```

---

## Channels in Async

```rust
use tokio::sync::mpsc;

async fn channel_example() {
    let (tx, mut rx) = mpsc::channel(100);
    tokio::spawn(async move {
        tx.send(42).await.unwrap();
    });
    while let Some(value) = rx.recv().await {
        println!("got = {}", value);
    }
}
```

---

## Async Mutex

```rust
use tokio::sync::Mutex;

async fn shared_state() {
    let counter = Arc::new(Mutex::new(0));
    let counter_clone = counter.clone();
    tokio::spawn(async move {
        let mut lock = counter_clone.lock().await;
        *lock += 1;
    });
}
```

---

## RwLock in Async

```rust
use tokio::sync::RwLock;

async fn reader_writer() {
    let lock = Arc::new(RwLock::new(0));
    // Multiple readers
    let read = lock.read().await;
    // Single writer
    let mut write = lock.write().await;
    *write += 1;
}
```

---

## Broadcast Channels

```rust
use tokio::sync::broadcast;

async fn broadcast_example() {
    let (tx, mut rx1) = broadcast::channel(16);
    let mut rx2 = tx.subscribe();
    tokio::spawn(async move {
        tx.send(10).unwrap();
    });
    println!("rx1: {}", rx1.recv().await.unwrap());
    println!("rx2: {}", rx2.recv().await.unwrap());
}
```

---
## Stream Processing

```rust
use futures::stream::{self, StreamExt};

async fn process_items() {
    let stream = stream::iter(1..=3)
        .map(|x| x * 2)
        .filter(|x| future::ready(*x > 2))
        .collect::<Vec<_>>()
        .await;
    println!("Results: {:?}", stream);
}
```

---
## Async Traits

```rust
#[async_trait]
trait DataFetcher {
    async fn fetch_data(&self) -> Result<Vec<u8>, Error>;
    async fn process(&self, data: Vec<u8>);
}
```

---

## Timeout Handling

```rust
use tokio::time::{timeout, Duration};

async fn with_timeout() {
    let result = timeout(
        Duration::from_secs(1),
        async {
            // Long operation
            tokio::time::sleep(Duration::from_secs(2)).await;
            42
        }
    ).await;
    match result {
        Ok(value) => println!("Completed with: {}", value),
        Err(_) => println!("Operation timed out"),
    }
}
```

---

## Graceful Shutdown

```rust
use tokio::signal;

async fn shutdown_signal() {
    tokio::select! {
        _ = signal::ctrl_c() => {
            println!("Received Ctrl+C!");
        }
        _ = signal::unix::signal(signal::unix::SignalKind::terminate()) => {
            println!("Received terminate signal!");
        }
    }
}
```

---

## Error Propagation

```rust
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let result = async_operation().await?;
    process_result(result).await?;
    Ok(())
}
```

---

## Task Groups

```rust
use tokio::task::JoinSet;

async fn parallel_tasks() {
    let mut set = JoinSet::new();
    for i in 0..10 {
        set.spawn(async move {
            process_item(i).await
        });
    }
    while let Some(res) = set.join_next().await {
        println!("Task completed: {:?}", res);
    }
}
```

---

## Resource Management

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_res" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Async Resource Management</text>
  <rect x="20" y="30" width="170" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="48" text-anchor="middle" font-size="10" font-weight="bold">Semaphore</text>
  <text x="105" y="63" text-anchor="middle" font-size="9">Limit concurrent access</text>
  <text x="105" y="78" text-anchor="middle" font-size="9">tokio::sync::Semaphore</text>
  <rect x="215" y="30" width="170" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="48" text-anchor="middle" font-size="10" font-weight="bold">JoinSet</text>
  <text x="300" y="63" text-anchor="middle" font-size="9">Manage task groups</text>
  <text x="300" y="78" text-anchor="middle" font-size="9">Collect results, cancel all</text>
  <rect x="410" y="30" width="170" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="48" text-anchor="middle" font-size="10" font-weight="bold">CancellationToken</text>
  <text x="495" y="63" text-anchor="middle" font-size="9">Graceful shutdown signal</text>
  <text x="495" y="78" text-anchor="middle" font-size="9">tokio_util::sync</text>
  <rect x="20" y="105" width="270" height="40" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="155" y="120" text-anchor="middle" font-size="10" font-weight="bold">tokio::sync::Mutex (async-aware)</text>
  <text x="155" y="135" text-anchor="middle" font-size="9">Use when lock is held across .await points</text>
  <rect x="310" y="105" width="270" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="445" y="120" text-anchor="middle" font-size="10" font-weight="bold">std::sync::Mutex (sync)</text>
  <text x="445" y="135" text-anchor="middle" font-size="9">Use for short critical sections without .await</text>
  <rect x="80" y="160" width="440" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="175" text-anchor="middle" font-size="10">RAII still works: Drop runs when task completes or is cancelled</text>
  <text x="300" y="188" text-anchor="middle" font-size="9">Use timeout() to prevent tasks from running forever</text>
</svg>

---

## Testing Async Code

```rust
#[tokio::test]
async fn test_async_function() {
    let result = async_operation().await;
    assert_eq!(result, expected_value);
}
```

---

## Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="5" width="200" height="35" fill="#673ab7" stroke="#333" stroke-width="2" rx="8"/>
  <text x="300" y="28" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Async Best Practices</text>
  <line x1="250" y1="40" x2="120" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="40" x2="120" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="125" stroke="#333" stroke-width="2"/>
  <rect x="30" y="53" width="180" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="70" text-anchor="middle" font-size="10" font-weight="bold">Never block in async</text>
  <text x="120" y="84" text-anchor="middle" font-size="9">Use spawn_blocking() for</text>
  <text x="120" y="95" text-anchor="middle" font-size="9">CPU-heavy or sync I/O work</text>
  <rect x="390" y="53" width="180" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="70" text-anchor="middle" font-size="10" font-weight="bold">Use select! wisely</text>
  <text x="480" y="84" text-anchor="middle" font-size="9">Race futures, cancel losers</text>
  <text x="480" y="95" text-anchor="middle" font-size="9">Great for timeouts</text>
  <rect x="30" y="120" width="180" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="137" text-anchor="middle" font-size="10" font-weight="bold">Bound concurrency</text>
  <text x="120" y="151" text-anchor="middle" font-size="9">Use Semaphore or buffered</text>
  <text x="120" y="162" text-anchor="middle" font-size="9">streams to limit parallelism</text>
  <rect x="390" y="120" width="180" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="137" text-anchor="middle" font-size="10" font-weight="bold">Graceful shutdown</text>
  <text x="480" y="151" text-anchor="middle" font-size="9">Handle Ctrl+C signals</text>
  <text x="480" y="162" text-anchor="middle" font-size="9">Drain tasks before exit</text>
  <rect x="150" y="178" width="300" height="18" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="191" text-anchor="middle" font-size="9">Keep async tasks small; use channels for coordination between tasks</text>
</svg>

---

## Common Patterns

1. Producer-Consumer
1. Fan-out/Fan-in
1. Load Balancing
1. Circuit Breaking
1. Retry Logic

---

## Performance Considerations

<div class="columns">
<div>

## To Consider
- Task size
- Blocking operations
- Memory usage
- Thread pool size

</div>
<div>

## To Avoid
- CPU-bound tasks
- Long-running tasks
- Excessive spawning
- Resource leaks

</div>
</div>

---

## Practice Exercise

Create an async application that:
1. Handles HTTP requests
1. Processes data streams
1. Uses proper error handling
1. Implements timeouts
1. Manages resources efficiently

---

## Common Pitfalls
1. Blocking in async
1. Task starvation
1. Resource leaks
1. Poor error handling
1. Callback hell

---

## Summary
- Async/Await syntax
- Future and Stream
- Task management
- Resource handling
- Error management
