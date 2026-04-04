# Threads and Concurrency
## Chapter 8: Parallel Programming in Rust

---
## Concurrency Models

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Rust Concurrency Models</text>
  <rect x="20" y="28" width="170" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="46" text-anchor="middle" font-size="10" font-weight="bold">Message Passing</text>
  <text x="105" y="61" text-anchor="middle" font-size="9">mpsc::channel()</text>
  <text x="105" y="74" text-anchor="middle" font-size="9">tx.send() / rx.recv()</text>
  <text x="105" y="87" text-anchor="middle" font-size="9">"Share by communicating"</text>
  <rect x="215" y="28" width="170" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="46" text-anchor="middle" font-size="10" font-weight="bold">Shared State</text>
  <text x="300" y="61" text-anchor="middle" font-size="9">Arc&lt;Mutex&lt;T&gt;&gt;</text>
  <text x="300" y="74" text-anchor="middle" font-size="9">Arc&lt;RwLock&lt;T&gt;&gt;</text>
  <text x="300" y="87" text-anchor="middle" font-size="9">Atomic types</text>
  <rect x="410" y="28" width="170" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="46" text-anchor="middle" font-size="10" font-weight="bold">Thread Spawn</text>
  <text x="495" y="61" text-anchor="middle" font-size="9">thread::spawn(move || {})</text>
  <text x="495" y="74" text-anchor="middle" font-size="9">handle.join()</text>
  <text x="495" y="87" text-anchor="middle" font-size="9">OS-level threads</text>
  <rect x="60" y="110" width="200" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="160" y="125" text-anchor="middle" font-size="10" font-weight="bold">Send trait</text>
  <text x="160" y="139" text-anchor="middle" font-size="9">Type can be transferred between threads</text>
  <rect x="290" y="110" width="200" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="390" y="125" text-anchor="middle" font-size="10" font-weight="bold">Sync trait</text>
  <text x="390" y="139" text-anchor="middle" font-size="9">Type can be shared (&amp;T) between threads</text>
  <rect x="80" y="160" width="440" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="180" text-anchor="middle" font-size="10">Compiler enforces thread safety: data races are compile errors, not runtime bugs</text>
</svg>

---
## Creating Threads

```rust
use std::thread;
use std::time::Duration;

fn main() {
    let handle = thread::spawn(|| {
        for i in 1..10 {
            println!("hi number {} from spawned thread!", i);
            thread::sleep(Duration::from_millis(1));
        }
    });

    handle.join().unwrap();
}
```

---
## Thread Handles

```rust
let handle = thread::spawn(|| {
    // Thread code
});

// Do other work

// Wait for thread to finish
match handle.join() {
    Ok(result) => println!("Thread finished: {:?}", result),
    Err(e) => println!("Thread panicked: {:?}", e),
}
```

---
## Moving Values into Threads

```rust
let v = vec![1, 2, 3];

let handle = thread::spawn(move || {
    println!("Vector: {:?}", v);
});

// v is no longer accessible here
handle.join().unwrap();
```

---
## Message Passing: Channels

```rust
use std::sync::mpsc;
use std::thread;

let (tx, rx) = mpsc::channel();

thread::spawn(move || {
    tx.send(String::from("hello")).unwrap();
});

let received = rx.recv().unwrap();
println!("Got: {}", received);
```

---
## Multiple Producers

```rust
let (tx, rx) = mpsc::channel();
let tx1 = tx.clone();

thread::spawn(move || {
    tx.send(1).unwrap();
});

thread::spawn(move || {
    tx1.send(2).unwrap();
});

for received in rx {
    println!("Got: {}", received);
}
```

---
## Channel Types

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_chan" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Channel Types: Message Passing</text>
  <rect x="20" y="30" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="48" text-anchor="middle" font-size="10" font-weight="bold">Producer (tx)</text>
  <text x="80" y="63" text-anchor="middle" font-size="9">tx.send(msg)</text>
  <text x="80" y="76" text-anchor="middle" font-size="9">can clone tx</text>
  <rect x="240" y="30" width="120" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="48" text-anchor="middle" font-size="10" font-weight="bold">Channel</text>
  <text x="300" y="63" text-anchor="middle" font-size="9">FIFO queue</text>
  <text x="300" y="76" text-anchor="middle" font-size="9">buffered/unbuffered</text>
  <rect x="460" y="30" width="120" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="520" y="48" text-anchor="middle" font-size="10" font-weight="bold">Consumer (rx)</text>
  <text x="520" y="63" text-anchor="middle" font-size="9">rx.recv()</text>
  <text x="520" y="76" text-anchor="middle" font-size="9">blocks until msg</text>
  <line x1="140" y1="57" x2="240" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arr_chan)"/>
  <text x="190" y="50" text-anchor="middle" font-size="9">send</text>
  <line x1="360" y1="57" x2="460" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arr_chan)"/>
  <text x="410" y="50" text-anchor="middle" font-size="9">recv</text>
  <rect x="20" y="100" width="270" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="155" y="116" text-anchor="middle" font-size="10" font-weight="bold">mpsc (multi-producer, single-consumer)</text>
  <text x="155" y="132" text-anchor="middle" font-size="9">Multiple tx clones, one rx. Ownership transferred on send.</text>
  <rect x="310" y="100" width="270" height="40" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="445" y="116" text-anchor="middle" font-size="10" font-weight="bold">sync_channel (bounded)</text>
  <text x="445" y="132" text-anchor="middle" font-size="9">Fixed buffer size. send() blocks when full.</text>
  <rect x="100" y="155" width="400" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="170" text-anchor="middle" font-size="10">Message ownership is moved through the channel</text>
  <text x="300" y="184" text-anchor="middle" font-size="9">Sender cannot use value after send -- compiler enforced</text>
</svg>

---
## Shared State: Mutex

```rust
use std::sync::Mutex;

let m = Mutex::new(5);

{
    let mut num = m.lock().unwrap();
    *num = 6;
}

println!("m = {:?}", m);
```

---
## Mutex Between Threads

```rust
use std::sync::{Arc, Mutex};
use std::thread;

let counter = Arc::new(Mutex::new(0));
let mut handles = vec![];

for _ in 0..10 {
    let counter = Arc::clone(&counter);
    let handle = thread::spawn(move || {
        let mut num = counter.lock().unwrap();
        *num += 1;
    });
    handles.push(handle);
}
```

---
## Arc (Atomic Reference Counting)

```rust
use std::sync::Arc;

let data = Arc::new(vec![1, 2, 3, 4]);
let mut handles = vec![];

for _ in 0..3 {
    let data_ref = Arc::clone(&data);
    handles.push(thread::spawn(move || {
        println!("{:?}", *data_ref);
    }));
}
```

---
## Atomic Types

```rust
use std::sync::atomic::{AtomicI32, Ordering};

let counter = AtomicI32::new(0);

counter.fetch_add(1, Ordering::SeqCst);
println!("Count: {}", counter.load(Ordering::SeqCst));
```

---
## Memory Ordering

```rust
use std::sync::atomic::Ordering;

// Available orderings
Ordering::Relaxed;    // Weakest
Ordering::Release;    // Store with release semantics
Ordering::Acquire;    // Load with acquire semantics
Ordering::AcqRel;     // Both acquire and release
Ordering::SeqCst;     // Strongest
```

---
## RwLock (Reader-Writer Lock)

```rust
use std::sync::RwLock;

let lock = RwLock::new(5);

// Multiple readers
let r1 = lock.read().unwrap();
let r2 = lock.read().unwrap();

// One writer
let w = lock.write().unwrap();
*w = 6;
```

---
## Thread Pools

```rust
use threadpool::ThreadPool;

let pool = ThreadPool::new(4);

for i in 0..8 {
    pool.execute(move || {
        println!("Task {} executed", i);
    });
}
```

---
## Barrier Synchronization

```rust
use std::sync::{Arc, Barrier};

let barrier = Arc::new(Barrier::new(3));

for _ in 0..3 {
    let b = Arc::clone(&barrier);
    thread::spawn(move || {
        println!("before wait");
        b.wait();
        println!("after wait");
    });
}
```

---
## Condition Variables

```rust
use std::sync::{Arc, Mutex, Condvar};

let pair = Arc::new((Mutex::new(false), Condvar::new()));
let pair2 = Arc::clone(&pair);

thread::spawn(move || {
    let (lock, cvar) = &*pair2;
    let mut started = lock.lock().unwrap();
    *started = true;
    cvar.notify_one();
});
```

---
## Thread Safety Traits

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Send and Sync: Thread Safety Markers</text>
  <rect x="20" y="30" width="270" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="48" text-anchor="middle" font-size="11" font-weight="bold">Send</text>
  <text x="155" y="63" text-anchor="middle" font-size="10">Ownership can transfer between threads</text>
  <text x="155" y="78" text-anchor="middle" font-size="9">Most types are Send (i32, String, Vec...)</text>
  <text x="155" y="92" text-anchor="middle" font-size="9" fill="#c62828">NOT Send: Rc&lt;T&gt;, raw pointers</text>
  <rect x="310" y="30" width="270" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="48" text-anchor="middle" font-size="11" font-weight="bold">Sync</text>
  <text x="445" y="63" text-anchor="middle" font-size="10">&amp;T can be shared between threads</text>
  <text x="445" y="78" text-anchor="middle" font-size="9">T is Sync if &amp;T is Send</text>
  <text x="445" y="92" text-anchor="middle" font-size="9" fill="#c62828">NOT Sync: Cell&lt;T&gt;, RefCell&lt;T&gt;</text>
  <rect x="20" y="115" width="180" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="110" y="130" text-anchor="middle" font-size="10" font-weight="bold">Arc&lt;T&gt;</text>
  <text x="110" y="144" text-anchor="middle" font-size="9">Send + Sync ref counting</text>
  <rect x="210" y="115" width="180" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="130" text-anchor="middle" font-size="10" font-weight="bold">Mutex&lt;T&gt;</text>
  <text x="300" y="144" text-anchor="middle" font-size="9">Makes T Sync via locking</text>
  <rect x="400" y="115" width="180" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="490" y="130" text-anchor="middle" font-size="10" font-weight="bold">RwLock&lt;T&gt;</text>
  <text x="490" y="144" text-anchor="middle" font-size="9">Many readers OR one writer</text>
  <rect x="80" y="165" width="440" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="182" text-anchor="middle" font-size="10">Auto-traits: compiler derives Send/Sync if all fields are Send/Sync</text>
</svg>

---
## Send and Sync

```rust
// Types that can be transferred across threads
trait Send {}

// Types that can be shared between threads
trait Sync {}

// Example
#[derive(Debug)]
struct MySendType;
unsafe impl Send for MySendType {}
```

---
## Deadlock Prevention

```rust
use std::sync::{Mutex, MutexGuard};

fn transfer(
    source: &Mutex<i32>,
    dest: &Mutex<i32>,
    amount: i32,
) {
    let mut source_guard: MutexGuard<i32>;
    let mut dest_guard: MutexGuard<i32>;

    // Acquire locks in a consistent order
    if std::ptr::eq(source, dest) {
        return;
    } else if source as *const _ < dest as *const _ {
        source_guard = source.lock().unwrap();
        dest_guard = dest.lock().unwrap();
    } else {
        dest_guard = dest.lock().unwrap();
        source_guard = source.lock().unwrap();
    }
}
```

---
## Thread Local Storage

```rust
thread_local! {
    static COUNTER: RefCell<u32> = RefCell::new(0);
}

COUNTER.with(|c| {
    *c.borrow_mut() += 1;
    println!("Counter: {}", *c.borrow());
});
```

---
## Scoped Threads

```rust
let mut v = vec![1, 2, 3];

thread::scope(|s| {
    s.spawn(|| {
        println!("can borrow v here: {:?}", &v);
    });
});

println!("v: {:?}", v);
```

---
## Error Handling in Threads

```rust
let handle = thread::spawn(|| {
    if some_condition {
        Err("Something went wrong")
    } else {
        Ok("Success!")
    }
});

match handle.join() {
    Ok(Ok(success)) => println!("Success: {}", success),
    Ok(Err(err)) => println!("Thread returned error: {}", err),
    Err(e) => println!("Thread panicked: {:?}", e),
}
```

---
## Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="5" width="200" height="35" fill="#673ab7" stroke="#333" stroke-width="2" rx="8"/>
  <text x="300" y="28" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Concurrency Tips</text>
  <line x1="250" y1="40" x2="120" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="40" x2="120" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="125" stroke="#333" stroke-width="2"/>
  <rect x="30" y="53" width="180" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="70" text-anchor="middle" font-size="10" font-weight="bold">Channels over mutexes</text>
  <text x="120" y="84" text-anchor="middle" font-size="9">Message passing avoids</text>
  <text x="120" y="95" text-anchor="middle" font-size="9">shared state complexity</text>
  <rect x="390" y="53" width="180" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="70" text-anchor="middle" font-size="10" font-weight="bold">Minimize lock scope</text>
  <text x="480" y="84" text-anchor="middle" font-size="9">Hold Mutex lock briefly</text>
  <text x="480" y="95" text-anchor="middle" font-size="9">Drop guard ASAP</text>
  <rect x="30" y="120" width="180" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="137" text-anchor="middle" font-size="10" font-weight="bold">Use scoped threads</text>
  <text x="120" y="151" text-anchor="middle" font-size="9">thread::scope() borrows</text>
  <text x="120" y="162" text-anchor="middle" font-size="9">data without Arc/move</text>
  <rect x="390" y="120" width="180" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="137" text-anchor="middle" font-size="10" font-weight="bold">Consistent lock order</text>
  <text x="480" y="151" text-anchor="middle" font-size="9">Always acquire locks in</text>
  <text x="480" y="162" text-anchor="middle" font-size="9">the same order (no deadlock)</text>
  <rect x="150" y="178" width="300" height="18" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="191" text-anchor="middle" font-size="9">Prefer Arc&lt;Mutex&lt;T&gt;&gt; for simple sharing; channels for pipelines</text>
</svg>

---
## Performance Considerations
1. Thread creation overhead
1. Context switching costs
1. Cache coherency
1. Lock contention
1. Memory ordering impact
---
## Practice Exercise
Create a concurrent application that:
1. Uses multiple threads
1. Shares data safely
1. Handles errors
1. Prevents deadlocks
1. Uses message passing
---
## Common Pitfalls
1. Race conditions
1. Deadlocks
1. Thread leak
1. Lock contention
1. Incorrect synchronization
---
## Summary
- Thread basics
- Message passing
- Shared state
- Synchronization
- Best practices
