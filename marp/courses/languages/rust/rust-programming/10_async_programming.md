---
tags:
  - languages:rust
  - concepts:programming
  - concepts:concurrency
level: beginner
category: language
audience:
  - audiences:developers

---
# Async Programming
## Chapter 9: Asynchronous Programming in Rust

---

## Why Async

![why_async](svg/courses/languages/rust/rust-programming/10_async_programming/why_async.svg)

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

![resource_management](svg/courses/languages/rust/rust-programming/10_async_programming/resource_management.svg)

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

![best_practices](svg/courses/languages/rust/rust-programming/10_async_programming/best_practices.svg)

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
