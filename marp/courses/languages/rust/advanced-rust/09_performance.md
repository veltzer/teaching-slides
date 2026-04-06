# Performance

Zero-Cost Abstractions, Profiling, Benchmarking, and Optimization

---

## Overview

- Zero-cost abstractions deep dive
- LLVM optimization passes
- Profiling with `perf` and flamegraph
- Benchmarking with `criterion`
- Memory allocators (`jemalloc`, `mimalloc`, `GlobalAlloc`)
- SIMD with `std::simd`
- Cache-friendly data structures (SoA vs AoS)
- Compile-time computation (`const fn`, const generics)
- Link-time optimization (LTO)
- Profile-guided optimization (PGO)
- `#[inline]` guidance

---

## Part 1: Zero-Cost Abstractions

You don't pay for what you don't use

---

## What Zero-Cost Means

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="270"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="640" height="90" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="30" font-family="sans-serif" font-size="13" fill="#1565c0" text-anchor="start" font-weight="bold">Bjarne Stroustrup's Principle:</text><text x="28" y="50" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start">"What you don't use, you don't pay for.</text><text x="28" y="66" font-family="sans-serif" font-size="12" fill="#333" text-anchor="start"> What you do use, you couldn't hand-code any better."</text><text x="20" y="120" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">Rust zero-cost abstractions:</text><text x="28" y="138" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Iterators compile to the same code as hand-written loops</text><text x="28" y="160" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Generics are monomorphized (no virtual dispatch overhead)</text><text x="28" y="182" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Traits with static dispatch are inlined away</text><text x="28" y="204" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• Option<&T> is the same size as *const T (null pointer opt)</text><text x="28" y="226" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">• String bounds checks are elided when the compiler can prove safety</text></svg>

---

## Iterator vs Hand-Written Loop

```rust
// These two produce IDENTICAL assembly with optimizations on

fn sum_squares_iterator(data: &[i32]) -> i64 {
    data.iter()
        .filter(|&&x| x > 0)
        .map(|&x| (x as i64) * (x as i64))
        .sum()
}

fn sum_squares_manual(data: &[i32]) -> i64 {
    let mut sum: i64 = 0;
    for i in 0..data.len() {
        if data[i] > 0 {
            sum += (data[i] as i64) * (data[i] as i64);
        }
    }
    sum
}

fn main() {
    let data: Vec<i32> = (-1000..=1000).collect();
    assert_eq!(
        sum_squares_iterator(&data),
        sum_squares_manual(&data)
    );
    println!("Both produce: {}", sum_squares_iterator(&data));
}
```

Use `cargo asm` or Compiler Explorer (godbolt.org) to verify.

---

## Monomorphization

```rust
// Generic function: zero-cost abstraction via monomorphization
fn max_of<T: PartialOrd>(a: T, b: T) -> T {
    if a >= b { a } else { b }
}

fn main() {
    // The compiler generates SEPARATE optimized versions:
    //   max_of::<i32>(i32, i32) -> i32
    //   max_of::<f64>(f64, f64) -> f64
    //   max_of::<&str>(&str, &str) -> &str
    let a = max_of(3, 7);
    let b = max_of(3.14, 2.71);
    let c = max_of("hello", "world");

    println!("{}, {}, {}", a, b, c);
}

// Trade-off: monomorphization increases binary size
// Each unique type instantiation = separate machine code
//
// If binary size matters, use dynamic dispatch instead:
// fn max_of_dyn(a: &dyn PartialOrd<???>, ...) -- but loses performance
```

---

## Null Pointer Optimization

```rust
use std::mem::size_of;

fn main() {
    // Option<&T> is the SAME size as &T
    // The compiler uses the null pointer as None
    assert_eq!(size_of::<&i32>(), size_of::<Option<&i32>>());
    assert_eq!(size_of::<Box<i32>>(), size_of::<Option<Box<i32>>>());

    // Also works for NonZero types
    use std::num::NonZeroU64;
    assert_eq!(size_of::<u64>(), size_of::<Option<NonZeroU64>>());

    println!("&i32:           {} bytes", size_of::<&i32>());
    println!("Option<&i32>:   {} bytes", size_of::<Option<&i32>>());
    println!("u64:            {} bytes", size_of::<u64>());
    println!("Option<NonZeroU64>: {} bytes", size_of::<Option<NonZeroU64>>());

    // But Option<i32> IS larger:
    println!("i32:            {} bytes", size_of::<i32>());
    println!("Option<i32>:    {} bytes", size_of::<Option<i32>>());
    // 4 vs 8 (needs a discriminant tag)
}
```

---

## Part 2: LLVM Optimization Passes

What the compiler does for you

---

## LLVM Optimization Pipeline

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="280"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="20" y="30" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="70" y="50" font-family="sans-serif" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">Rust Source</text><text x="70" y="68" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(.rs)</text><rect x="200" y="30" width="110" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="255" y="50" font-family="sans-serif" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">rustc</text><text x="255" y="68" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">frontend</text><rect x="390" y="30" width="100" height="50" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/><text x="440" y="50" font-family="sans-serif" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">LLVM IR</text><rect x="570" y="30" width="110" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="625" y="50" font-family="sans-serif" font-size="13" fill="#222" text-anchor="middle" font-weight="bold">Machine</text><text x="625" y="68" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Code</text><line x1="120" y1="55" x2="200" y2="55" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><line x1="310" y1="55" x2="390" y2="55" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><line x1="490" y1="55" x2="570" y2="55" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><line x1="440" y1="80" x2="440" y2="112" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><text x="448" y="104" font-family="sans-serif" font-size="11" fill="#555" text-anchor="start">Optimization Passes</text><rect x="30" y="130" width="150" height="44" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="105" y="146" font-family="sans-serif" font-size="11" fill="#222" text-anchor="middle">Inlining</text><rect x="230" y="130" width="150" height="44" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="305" y="146" font-family="sans-serif" font-size="11" fill="#222" text-anchor="middle">Dead Code</text><text x="305" y="162" font-family="sans-serif" font-size="11" fill="#222" text-anchor="middle">Elimination</text><rect x="430" y="130" width="150" height="44" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="505" y="146" font-family="sans-serif" font-size="11" fill="#222" text-anchor="middle">Vectorize</text><text x="505" y="162" font-family="sans-serif" font-size="11" fill="#222" text-anchor="middle">(SIMD)</text><rect x="30" y="195" width="150" height="44" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="105" y="211" font-family="sans-serif" font-size="11" fill="#222" text-anchor="middle">Constant</text><text x="105" y="227" font-family="sans-serif" font-size="11" fill="#222" text-anchor="middle">Folding</text><rect x="230" y="195" width="150" height="44" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="305" y="211" font-family="sans-serif" font-size="11" fill="#222" text-anchor="middle">Loop</text><text x="305" y="227" font-family="sans-serif" font-size="11" fill="#222" text-anchor="middle">Unrolling</text><rect x="430" y="195" width="150" height="44" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="505" y="211" font-family="sans-serif" font-size="11" fill="#222" text-anchor="middle">Tail Call</text><text x="505" y="227" font-family="sans-serif" font-size="11" fill="#222" text-anchor="middle">Opt</text></svg>

---

## Optimization Levels

```bash
  cargo build                   # dev profile:   opt-level = 0
  cargo build --release         # release profile: opt-level = 3

  Cargo.toml overrides:

  [profile.dev]
  opt-level = 0          # No optimization (fast compile)

  [profile.release]
  opt-level = 3          # Maximum optimization
  # opt-level = "s"      # Optimize for binary size
  # opt-level = "z"      # Aggressively optimize for size

  [profile.dev.package."*"]
  opt-level = 2          # Optimize dependencies even in dev mode
```

| Level | Speed | Compile Time | Binary Size | Debug Info |
|-------|-------|-------------|-------------|------------|
| 0     | Slow  | Fast        | Large       | Full       |
| 1     | OK    | OK          | Smaller     | Full       |
| 2     | Fast  | Slower      | Smaller     | Partial    |
| 3     | Fastest| Slowest    | Varies      | Minimal    |
| "s"   | Good  | Slower      | Small       | Minimal    |
| "z"   | Good  | Slower      | Smallest    | Minimal    |

---

## Viewing LLVM IR and Assembly

```bash
# View LLVM IR
cargo rustc --release -- --emit=llvm-ir
# Output: target/release/deps/<crate>-<hash>.ll

# View assembly
cargo rustc --release -- --emit=asm
# Output: target/release/deps/<crate>-<hash>.s

# Use cargo-asm for cleaner output
# cargo install cargo-asm
cargo asm my_crate::sum_squares_iterator

# Use cargo-show-asm (more modern)
# cargo install cargo-show-asm
cargo asm --lib my_crate::sum_squares_iterator
```

---

## Part 3: Profiling

Finding bottlenecks

---

## Profiling with perf

```bash
# Build with debug symbols in release mode
# Cargo.toml:
# [profile.release]
# debug = true

cargo build --release

# Record performance data
perf record -g --call-graph dwarf ./target/release/my_app

# View top functions
perf report

# Statistical profiling
perf stat ./target/release/my_app
#  Output includes:
#    - CPU cycles
#    - Instructions
#    - Cache misses
#    - Branch mispredictions
#    - IPC (instructions per cycle)
```

---

## Flamegraphs

```bash
# Install flamegraph tool
cargo install flamegraph

# Generate flamegraph (builds with release + debug info)
cargo flamegraph --bin my_app

# Opens flamegraph.svg in browser
# Wide bars = more time spent in that function
# Stack depth = call chain
```

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="200"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><text x="20" y="18" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">Flame Graph (CPU Time Visualization)</text><rect x="10" y="160" width="640" height="24" fill="#ffab40" stroke="#888" stroke-width="1.5" rx="4"/><text x="16" y="177" font-family="sans-serif" font-size="14" fill="#222" text-anchor="start">main</text><rect x="10" y="132" width="360" height="24" fill="#f57c00" stroke="#888" stroke-width="1.5" rx="4"/><text x="16" y="149" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start">process_data</text><rect x="370" y="132" width="280" height="24" fill="#4fc3f7" stroke="#888" stroke-width="1.5" rx="4"/><text x="376" y="149" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start">io::read_file</text><rect x="10" y="104" width="160" height="24" fill="#ef9a9a" stroke="#888" stroke-width="1.5" rx="4"/><text x="16" y="121" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start">parse</text><rect x="175" y="104" width="195" height="24" fill="#a5d6a7" stroke="#888" stroke-width="1.5" rx="4"/><text x="181" y="121" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start">transform</text><rect x="10" y="76" width="160" height="24" fill="#ce93d8" stroke="#888" stroke-width="1.5" rx="4"/><text x="16" y="93" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">serde_json ← Bottleneck!</text><text x="20" y="50" font-family="sans-serif" font-size="11" fill="#b71c1c" text-anchor="start">^ Wide bar = more CPU time.  serde_json at bottom is the bottleneck.</text></svg>

```bash
# For specific binary with arguments
cargo flamegraph -- --input data.csv --threads 4

# Filter to specific functions
cargo flamegraph --flamechart  # Time-ordered view
```

---

## Part 4: Benchmarking with Criterion

Statistical benchmarking

---

## Setting Up Criterion

```toml
# Cargo.toml
[dev-dependencies]
criterion = { version = "0.5", features = ["html_reports"] }

[[bench]]
name = "my_benchmark"
harness = false
```

```rust
// benches/my_benchmark.rs
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn fibonacci(n: u64) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        n => fibonacci(n - 1) + fibonacci(n - 2),
    }
}

fn fibonacci_iterative(n: u64) -> u64 {
    let (mut a, mut b) = (0u64, 1u64);
    for _ in 0..n {
        let tmp = a;
        a = b;
        b = tmp + b;
    }
    a
}

fn bench_fibonacci(c: &mut Criterion) {
    c.bench_function("fib_recursive_20", |b| {
        b.iter(|| fibonacci(black_box(20)))
    });

    c.bench_function("fib_iterative_20", |b| {
        b.iter(|| fibonacci_iterative(black_box(20)))
    });
}

criterion_group!(benches, bench_fibonacci);
criterion_main!(benches);
```

```bash
cargo bench
# Generates HTML report in target/criterion/
```

---

## Criterion: Comparing Implementations

```rust
use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion};

fn sum_loop(data: &[i32]) -> i64 {
    let mut sum: i64 = 0;
    for &x in data {
        sum += x as i64;
    }
    sum
}

fn sum_iter(data: &[i32]) -> i64 {
    data.iter().map(|&x| x as i64).sum()
}

fn sum_chunks(data: &[i32]) -> i64 {
    data.chunks(64)
        .map(|chunk| chunk.iter().map(|&x| x as i64).sum::<i64>())
        .sum()
}

fn bench_sums(c: &mut Criterion) {
    let sizes = [100, 1_000, 10_000, 100_000];

    let mut group = c.benchmark_group("sum_implementations");
    for &size in &sizes {
        let data: Vec<i32> = (0..size).collect();

        group.bench_with_input(
            BenchmarkId::new("loop", size),
            &data,
            |b, data| b.iter(|| sum_loop(black_box(data))),
        );
        group.bench_with_input(
            BenchmarkId::new("iter", size),
            &data,
            |b, data| b.iter(|| sum_iter(black_box(data))),
        );
        group.bench_with_input(
            BenchmarkId::new("chunks", size),
            &data,
            |b, data| b.iter(|| sum_chunks(black_box(data))),
        );
    }
    group.finish();
}

criterion_group!(benches, bench_sums);
criterion_main!(benches);
```

---

## Criterion: black_box and Throughput

```rust
use criterion::{black_box, criterion_group, criterion_main, Criterion, Throughput};

fn process_bytes(data: &[u8]) -> u64 {
    data.iter().map(|&b| b as u64).sum()
}

fn bench_throughput(c: &mut Criterion) {
    let data: Vec<u8> = (0..1_000_000).map(|i| (i % 256) as u8).collect();

    let mut group = c.benchmark_group("throughput");

    // Tell criterion about the input size for throughput calculation
    group.throughput(Throughput::Bytes(data.len() as u64));

    group.bench_function("process_bytes", |b| {
        b.iter(|| process_bytes(black_box(&data)))
    });

    group.finish();
    // Output: throughput: 2.5 GiB/s
}

// black_box() prevents the compiler from optimizing away the computation.
// Without it, the compiler might realize the result is unused
// and eliminate the entire benchmark.

criterion_group!(benches, bench_throughput);
criterion_main!(benches);
```

---

## Part 5: Memory Allocators

Custom allocators for performance

---

## Global Allocator Trait

```rust
use std::alloc::{GlobalAlloc, Layout, System};
use std::sync::atomic::{AtomicUsize, Ordering};

/// A counting allocator that wraps the system allocator
struct CountingAllocator {
    alloc_count: AtomicUsize,
    dealloc_count: AtomicUsize,
    bytes_allocated: AtomicUsize,
}

unsafe impl GlobalAlloc for CountingAllocator {
    unsafe fn alloc(&self, layout: Layout) -> *mut u8 {
        self.alloc_count.fetch_add(1, Ordering::Relaxed);
        self.bytes_allocated.fetch_add(layout.size(), Ordering::Relaxed);
        unsafe { System.alloc(layout) }
    }

    unsafe fn dealloc(&self, ptr: *mut u8, layout: Layout) {
        self.dealloc_count.fetch_add(1, Ordering::Relaxed);
        self.bytes_allocated.fetch_sub(layout.size(), Ordering::Relaxed);
        unsafe { System.dealloc(ptr, layout) }
    }
}

#[global_allocator]
static ALLOC: CountingAllocator = CountingAllocator {
    alloc_count: AtomicUsize::new(0),
    dealloc_count: AtomicUsize::new(0),
    bytes_allocated: AtomicUsize::new(0),
};

fn main() {
    let before = ALLOC.alloc_count.load(Ordering::Relaxed);

    let v: Vec<i32> = (0..1000).collect();
    let s = format!("Vector has {} elements", v.len());
    println!("{}", s);

    let after = ALLOC.alloc_count.load(Ordering::Relaxed);
    println!("Allocations: {}", after - before);
    println!("Currently allocated: {} bytes",
             ALLOC.bytes_allocated.load(Ordering::Relaxed));
}
```

---

## Using jemalloc

```toml
# Cargo.toml
[dependencies]
tikv-jemallocator = "0.6"
```

```rust
// main.rs
use tikv_jemallocator::Jemalloc;

#[global_allocator]
static GLOBAL: Jemalloc = Jemalloc;

fn main() {
    // jemalloc is now the global allocator
    // Benefits:
    // - Better performance for multi-threaded workloads
    // - Per-thread caching reduces lock contention
    // - Better fragmentation behavior for long-running servers
    // - Detailed memory profiling support

    let mut vecs: Vec<Vec<u8>> = Vec::new();
    for _ in 0..1000 {
        vecs.push(vec![0u8; 4096]);
    }
    println!("Allocated {} vectors", vecs.len());
}
```

---

## Using mimalloc

```toml
# Cargo.toml
[dependencies]
mimalloc = "0.1"
```

```rust
use mimalloc::MiMalloc;

#[global_allocator]
static GLOBAL: MiMalloc = MiMalloc;

fn main() {
    // mimalloc benefits:
    // - Excellent performance across workloads
    // - Small footprint
    // - Good for both small and large allocations
    // - Free list sharding reduces contention

    let data: Vec<String> = (0..10_000)
        .map(|i| format!("item-{}", i))
        .collect();
    println!("Created {} strings", data.len());
}
```

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="185"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="680" height="28" fill="#1565c0" stroke="#333" stroke-width="1.5" rx="4"/><text x="16" y="28" font-family="sans-serif" font-size="12" fill="#fff" text-anchor="start" font-weight="bold">Allocator</text><text x="171" y="28" font-family="sans-serif" font-size="12" fill="#fff" text-anchor="start" font-weight="bold">Throughput</text><text x="291" y="28" font-family="sans-serif" font-size="12" fill="#fff" text-anchor="start" font-weight="bold">Fragmentation</text><text x="421" y="28" font-family="sans-serif" font-size="12" fill="#fff" text-anchor="start" font-weight="bold">Best For</text><line x1="165" y1="10" x2="165" y2="182" stroke="#aaa" stroke-width="1"/><line x1="285" y1="10" x2="285" y2="182" stroke="#aaa" stroke-width="1"/><line x1="415" y1="10" x2="415" y2="182" stroke="#aaa" stroke-width="1"/><line x1="540" y1="10" x2="540" y2="182" stroke="#aaa" stroke-width="1"/><rect x="10" y="38" width="680" height="36" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="16" y="54" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">System (glibc)</text><text x="171" y="54" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Baseline</text><text x="291" y="54" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Moderate</text><text x="421" y="54" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Default</text><rect x="10" y="74" width="680" height="36" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="16" y="90" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">jemalloc</text><text x="171" y="90" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">1.2–2×</text><text x="291" y="90" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Low</text><text x="421" y="90" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Servers</text><text x="421" y="106" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">multi-thread</text><rect x="10" y="110" width="680" height="36" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="16" y="126" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">mimalloc</text><text x="171" y="126" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">1.5–2×</text><text x="291" y="126" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Low</text><text x="421" y="126" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">General use</text><rect x="10" y="146" width="680" height="36" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="16" y="162" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Custom arena</text><text x="171" y="162" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Varies</text><text x="291" y="162" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">None (reset)</text><text x="421" y="162" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Game loops</text><text x="421" y="178" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">batch work</text></svg>

---

## Part 6: SIMD

Single Instruction, Multiple Data

---

## SIMD Concepts

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="250"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><text x="20" y="20" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">Scalar operation (one element at a time):</text><rect x="20" y="40" width="50" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="38" y="61" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">a</text><text x="100" y="60" font-family="sans-serif" font-size="16" fill="#222" text-anchor="start" font-weight="bold">+</text><rect x="160" y="40" width="50" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="178" y="61" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">b</text><text x="240" y="60" font-family="sans-serif" font-size="16" fill="#222" text-anchor="start" font-weight="bold">=</text><rect x="300" y="40" width="50" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="318" y="61" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">c</text><text x="400" y="60" font-family="sans-serif" font-size="12" fill="#555" text-anchor="start">→ 1 instruction per element</text><text x="20" y="110" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">SIMD operation (four elements at a time with SSE/NEON):</text><rect x="20" y="120" width="50" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="34" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">a0</text><rect x="74" y="120" width="50" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="88" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">a1</text><rect x="128" y="120" width="50" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="142" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">a2</text><rect x="182" y="120" width="50" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="196" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">a3</text><rect x="260" y="120" width="50" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="274" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">b0</text><rect x="314" y="120" width="50" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="328" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">b1</text><rect x="368" y="120" width="50" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="382" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">b2</text><rect x="422" y="120" width="50" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="436" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">b3</text><rect x="500" y="120" width="50" height="30" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/><text x="514" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">c0</text><rect x="554" y="120" width="50" height="30" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/><text x="568" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">c1</text><rect x="608" y="120" width="50" height="30" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/><text x="622" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">c2</text><rect x="662" y="120" width="50" height="30" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/><text x="676" y="141" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">c3</text><text x="232" y="141" font-family="sans-serif" font-size="16" fill="#222" text-anchor="start" font-weight="bold">+</text><text x="472" y="141" font-family="sans-serif" font-size="16" fill="#222" text-anchor="start" font-weight="bold">=</text><text x="20" y="175" font-family="sans-serif" font-size="12" fill="#1b5e20" text-anchor="start">→ 1 instruction for 4 elements  (4× throughput)</text><text x="20" y="200" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">SSE:</text><text x="90" y="200" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">128-bit  (4× f32, 2× f64, 16× u8)</text><text x="20" y="216" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">AVX2:</text><text x="90" y="216" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">256-bit  (8× f32, 4× f64, 32× u8)</text><text x="20" y="232" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">AVX-512:</text><text x="90" y="232" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">512-bit (16× f32, 8× f64, 64× u8)</text><text x="20" y="248" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">NEON:</text><text x="90" y="248" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">128-bit  (ARM)</text></svg>

---

## Portable SIMD (std::simd, nightly)

```rust
// Requires nightly: rustup run nightly cargo run
#![feature(portable_simd)]
use std::simd::prelude::*;

fn dot_product_simd(a: &[f32], b: &[f32]) -> f32 {
    assert_eq!(a.len(), b.len());

    let mut sum = f32x4::splat(0.0);
    let chunks = a.len() / 4;

    for i in 0..chunks {
        let va = f32x4::from_slice(&a[i * 4..]);
        let vb = f32x4::from_slice(&b[i * 4..]);
        sum += va * vb;
    }

    let mut result = sum.reduce_sum();

    // Handle remaining elements
    for i in (chunks * 4)..a.len() {
        result += a[i] * b[i];
    }

    result
}

fn dot_product_scalar(a: &[f32], b: &[f32]) -> f32 {
    a.iter().zip(b.iter()).map(|(x, y)| x * y).sum()
}

fn main() {
    let a: Vec<f32> = (0..1024).map(|i| i as f32).collect();
    let b: Vec<f32> = (0..1024).map(|i| (i * 2) as f32).collect();

    let simd_result = dot_product_simd(&a, &b);
    let scalar_result = dot_product_scalar(&a, &b);

    println!("SIMD:   {}", simd_result);
    println!("Scalar: {}", scalar_result);
    assert!((simd_result - scalar_result).abs() < 1.0);
}
```

---

## Auto-Vectorization

```rust
// The compiler can auto-vectorize simple loops.
// You don't always need manual SIMD.

fn sum_f32(data: &[f32]) -> f32 {
    data.iter().sum()
    // With -C opt-level=3, LLVM often vectorizes this
    // using SSE/AVX instructions automatically
}

// Tips to help auto-vectorization:
//
// 1. Use simple loops over slices
// 2. Avoid branches inside the loop
// 3. Use #[target_feature] for specific instruction sets
// 4. Avoid cross-iteration dependencies

#[target_feature(enable = "avx2")]
unsafe fn add_arrays_avx2(a: &[f32], b: &[f32], out: &mut [f32]) {
    assert_eq!(a.len(), b.len());
    assert_eq!(a.len(), out.len());
    for i in 0..a.len() {
        out[i] = a[i] + b[i];
    }
    // The compiler will use AVX2 instructions for this function
}

fn main() {
    let a: Vec<f32> = vec![1.0; 256];
    let b: Vec<f32> = vec![2.0; 256];
    let mut out = vec![0.0f32; 256];

    if is_x86_feature_detected!("avx2") {
        unsafe { add_arrays_avx2(&a, &b, &mut out); }
    } else {
        for i in 0..a.len() {
            out[i] = a[i] + b[i];
        }
    }

    println!("First 4 results: {:?}", &out[..4]);
}
```

---

## Part 7: Cache-Friendly Data Structures

AoS vs SoA

---

## Array of Structs vs Struct of Arrays

```rust
// Array of Structs (AoS) - traditional layout
struct ParticleAoS {
    x: f32,
    y: f32,
    z: f32,
    mass: f32,
    vx: f32,
    vy: f32,
    vz: f32,
    charge: f32,
}

// Memory layout (each row = one cache line, 64 bytes):
// [x,y,z,mass,vx,vy,vz,charge] [x,y,z,mass,vx,vy,vz,charge] ...
//  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
//  If you only need x,y,z you still load mass,vx,vy,vz,charge

// Struct of Arrays (SoA) - cache-friendly for field access
struct ParticlesSoA {
    x: Vec<f32>,
    y: Vec<f32>,
    z: Vec<f32>,
    mass: Vec<f32>,
    vx: Vec<f32>,
    vy: Vec<f32>,
    vz: Vec<f32>,
    charge: Vec<f32>,
}

// Memory layout:
// [x,x,x,x,x,x,x,x,...] [y,y,y,y,y,y,y,y,...] ...
//  ^^^^^^^^^^^^^^^^^^^^^^^^
//  If you only need x, every byte in the cache line is useful
```

---

## AoS vs SoA Benchmark

```rust
const N: usize = 1_000_000;

// AoS approach
struct PointAoS { x: f32, y: f32, z: f32, _padding: f32 }

fn distance_sum_aos(points: &[PointAoS]) -> f32 {
    points.iter()
        .map(|p| (p.x * p.x + p.y * p.y + p.z * p.z).sqrt())
        .sum()
}

// SoA approach
struct PointsSoA { x: Vec<f32>, y: Vec<f32>, z: Vec<f32> }

fn distance_sum_soa(points: &PointsSoA) -> f32 {
    let mut sum = 0.0f32;
    for i in 0..points.x.len() {
        let x = points.x[i];
        let y = points.y[i];
        let z = points.z[i];
        sum += (x * x + y * y + z * z).sqrt();
    }
    sum
}

fn main() {
    // AoS
    let aos: Vec<PointAoS> = (0..N)
        .map(|i| PointAoS {
            x: i as f32, y: (i * 2) as f32, z: (i * 3) as f32, _padding: 0.0
        })
        .collect();

    // SoA
    let soa = PointsSoA {
        x: (0..N).map(|i| i as f32).collect(),
        y: (0..N).map(|i| (i * 2) as f32).collect(),
        z: (0..N).map(|i| (i * 3) as f32).collect(),
    };

    let r1 = distance_sum_aos(&aos);
    let r2 = distance_sum_soa(&soa);
    println!("AoS: {}, SoA: {}", r1, r2);
    // SoA is typically 1.5-3x faster for this access pattern
}
```

---

## Cache Optimization Guidelines

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="360"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="660" height="340" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="30" font-family="sans-serif" font-size="14" fill="#0d47a1" text-anchor="start" font-weight="bold">Cache Optimization Rules</text><text x="20" y="46" font-family="sans-serif" font-size="12" fill="#1565c0" text-anchor="start" font-weight="bold">1. Sequential access beats random access</text><text x="28" y="61" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Vec<T>  >>  LinkedList<T> for iteration</text><text x="20" y="82" font-family="sans-serif" font-size="12" fill="#1565c0" text-anchor="start" font-weight="bold">2. Keep hot data together</text><text x="28" y="97" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">SoA layout: few fields, many items   |   AoS layout: all fields, few items</text><text x="20" y="118" font-family="sans-serif" font-size="12" fill="#1565c0" text-anchor="start" font-weight="bold">3. Minimize struct size</text><text x="28" y="133" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Less data per cache line = more items per line. Use #[repr(C)] or reorder fields.</text><text x="20" y="154" font-family="sans-serif" font-size="12" fill="#1565c0" text-anchor="start" font-weight="bold">4. Avoid pointer chasing</text><text x="28" y="169" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Vec<T> instead of Vec<Box<T>>   |   Flatten nested structures when possible</text><text x="20" y="190" font-family="sans-serif" font-size="12" fill="#1565c0" text-anchor="start" font-weight="bold">5. Use indices instead of pointers for graphs/trees</text><text x="28" y="205" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Store nodes in a Vec, reference by index  (arena allocation pattern)</text><line x1="20" y1="228" x2="660" y2="228" stroke="#aaa" stroke-width="1"/><text x="20" y="244" font-family="sans-serif" font-size="11" fill="#555" text-anchor="start">Cache line = 64 bytes on x86.  L1 ~1ns,  L2 ~5ns,  L3 ~20ns,  DRAM ~100ns.</text></svg>

---

## Arena Allocation for Cache Locality

```rust
struct Arena<T> {
    storage: Vec<T>,
}

#[derive(Clone, Copy)]
struct NodeId(usize);

struct TreeNode {
    value: i32,
    left: Option<NodeId>,
    right: Option<NodeId>,
}

impl Arena<TreeNode> {
    fn new() -> Self {
        Arena { storage: Vec::new() }
    }

    fn alloc(&mut self, node: TreeNode) -> NodeId {
        let id = NodeId(self.storage.len());
        self.storage.push(node);
        id
    }

    fn get(&self, id: NodeId) -> &TreeNode {
        &self.storage[id.0]
    }

    fn sum_all(&self) -> i64 {
        // Sequential memory access - very cache friendly
        self.storage.iter().map(|n| n.value as i64).sum()
    }
}

fn main() {
    let mut arena = Arena::new();

    let left = arena.alloc(TreeNode { value: 1, left: None, right: None });
    let right = arena.alloc(TreeNode { value: 3, left: None, right: None });
    let _root = arena.alloc(TreeNode { value: 2, left: Some(left), right: Some(right) });

    println!("Sum: {}", arena.sum_all()); // 6
    println!("Root value: {}", arena.get(_root).value);
}
```

---

## Part 8: Compile-Time Computation

const fn and const generics

---

## const fn

```rust
// const fn: functions evaluated at compile time
const fn factorial(n: u64) -> u64 {
    match n {
        0 | 1 => 1,
        _ => n * factorial(n - 1),
    }
}

const fn fibonacci(n: usize) -> u64 {
    let mut a: u64 = 0;
    let mut b: u64 = 1;
    let mut i = 0;
    while i < n {
        let tmp = a;
        a = b;
        b = tmp + b;
        i += 1;
    }
    a
}

// Computed at compile time - zero runtime cost
const FACT_10: u64 = factorial(10);
const FIB_20: u64 = fibonacci(20);

// Can also be used in array sizes
const TABLE_SIZE: usize = 256;
const LOOKUP_TABLE: [u8; TABLE_SIZE] = {
    let mut table = [0u8; TABLE_SIZE];
    let mut i = 0;
    while i < TABLE_SIZE {
        table[i] = (i as u8).wrapping_mul(7).wrapping_add(3);
        i += 1;
    }
    table
};

fn main() {
    println!("10! = {}", FACT_10);          // 3628800
    println!("fib(20) = {}", FIB_20);       // 6765
    println!("table[42] = {}", LOOKUP_TABLE[42]);

    // const fn can also be called at runtime
    let n = 5;
    println!("{}! = {}", n, factorial(n));
}
```

---

## Const Generics

```rust
// Const generics: generic over values, not just types

#[derive(Debug)]
struct Matrix<const ROWS: usize, const COLS: usize> {
    data: [[f64; COLS]; ROWS],
}

impl<const ROWS: usize, const COLS: usize> Matrix<ROWS, COLS> {
    fn new() -> Self {
        Matrix {
            data: [[0.0; COLS]; ROWS],
        }
    }

    fn get(&self, row: usize, col: usize) -> f64 {
        self.data[row][col]
    }

    fn set(&mut self, row: usize, col: usize, val: f64) {
        self.data[row][col] = val;
    }

    // Multiply: (ROWS x COLS) * (COLS x OTHER) = (ROWS x OTHER)
    // The compiler enforces dimension compatibility!
    fn multiply<const OTHER: usize>(
        &self,
        rhs: &Matrix<COLS, OTHER>,
    ) -> Matrix<ROWS, OTHER> {
        let mut result = Matrix::<ROWS, OTHER>::new();
        for i in 0..ROWS {
            for j in 0..OTHER {
                let mut sum = 0.0;
                for k in 0..COLS {
                    sum += self.data[i][k] * rhs.data[k][j];
                }
                result.data[i][j] = sum;
            }
        }
        result
    }
}

fn main() {
    let mut a = Matrix::<2, 3>::new();
    a.set(0, 0, 1.0); a.set(0, 1, 2.0); a.set(0, 2, 3.0);
    a.set(1, 0, 4.0); a.set(1, 1, 5.0); a.set(1, 2, 6.0);

    let mut b = Matrix::<3, 2>::new();
    b.set(0, 0, 7.0); b.set(0, 1, 8.0);
    b.set(1, 0, 9.0); b.set(1, 1, 10.0);
    b.set(2, 0, 11.0); b.set(2, 1, 12.0);

    let c: Matrix<2, 2> = a.multiply(&b);
    println!("Result [0][0] = {}", c.get(0, 0)); // 58.0
    println!("Result [1][1] = {}", c.get(1, 1)); // 154.0

    // This would fail at compile time:
    // let d = Matrix::<2, 4>::new();
    // a.multiply(&d); // ERROR: expected Matrix<3, _>, found Matrix<4, _>
}
```

---

## Compile-Time Type-Level Assertions

```rust
/// Assert properties at compile time using const evaluation
const fn assert_power_of_two(n: usize) {
    assert!(n > 0 && (n & (n - 1)) == 0, "must be a power of 2");
}

struct AlignedBuffer<const N: usize> {
    data: [u8; N],
}

impl<const N: usize> AlignedBuffer<N> {
    fn new() -> Self {
        // This check happens at compile time for const N
        assert_power_of_two(N);
        AlignedBuffer { data: [0; N] }
    }
}

fn main() {
    let _buf = AlignedBuffer::<64>::new();   // OK
    let _buf = AlignedBuffer::<256>::new();  // OK
    // let _buf = AlignedBuffer::<100>::new(); // Compile error: not power of 2

    println!("Buffers created successfully");
}
```

---

## Part 9: Link-Time Optimization (LTO)

Cross-crate optimization

---

## Configuring LTO

```toml
# Cargo.toml

[profile.release]
lto = true          # Full LTO: best optimization, slowest compile
# lto = "thin"      # Thin LTO: good optimization, faster compile
# lto = false       # Default: no cross-crate optimization

codegen-units = 1   # Single codegen unit: enables more inlining
                    # Default is 16 for parallel compilation
```

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="310"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><text x="20" y="26" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">Without LTO</text><rect x="20" y="34" width="160" height="50" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/><text x="100" y="54" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle" font-weight="bold">Crate A</text><text x="100" y="72" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">optimize alone</text><line x1="100" y1="84" x2="100" y2="105" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><rect x="210" y="34" width="160" height="50" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/><text x="290" y="54" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle" font-weight="bold">Crate B</text><text x="290" y="72" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">optimize alone</text><line x1="290" y1="84" x2="290" y2="105" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><rect x="400" y="34" width="160" height="50" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/><text x="480" y="54" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle" font-weight="bold">Crate C</text><text x="480" y="72" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">optimize alone</text><line x1="480" y1="84" x2="480" y2="105" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><line x1="100" y1="106" x2="580" y2="106" stroke="#555" stroke-width="1"/><line x1="340" y1="106" x2="340" y2="118" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><text x="345" y="114" font-family="sans-serif" font-size="10" fill="#555" text-anchor="start">link</text><rect x="265" y="122" width="150" height="30" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/><text x="340" y="142" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle" font-weight="bold">Binary</text><text x="340" y="158" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Cross-crate calls NOT inlined</text><text x="20" y="176" font-family="sans-serif" font-size="13" fill="#222" text-anchor="start" font-weight="bold">With LTO</text><rect x="20" y="184" width="160" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="100" y="204" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle" font-weight="bold">Crate A</text><text x="100" y="222" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(IR)</text><line x1="100" y1="234" x2="100" y2="255" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><rect x="210" y="184" width="160" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="290" y="204" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle" font-weight="bold">Crate B</text><text x="290" y="222" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(IR)</text><line x1="290" y1="234" x2="290" y2="255" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><rect x="400" y="184" width="160" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="480" y="204" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle" font-weight="bold">Crate C</text><text x="480" y="222" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(IR)</text><line x1="480" y1="234" x2="480" y2="255" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><line x1="100" y1="256" x2="580" y2="256" stroke="#555" stroke-width="1"/><line x1="340" y1="256" x2="340" y2="268" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><text x="345" y="264" font-family="sans-serif" font-size="10" fill="#555" text-anchor="start">merge + optimize</text><rect x="265" y="272" width="150" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="340" y="292" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle" font-weight="bold">Binary</text><text x="340" y="308" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">Full cross-crate optimization</text></svg>

---

## LTO Trade-offs

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="250"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="680" height="26" fill="#1565c0" stroke="#333" stroke-width="1.5" rx="4"/><text x="16" y="27" font-family="sans-serif" font-size="12" fill="#fff" text-anchor="start" font-weight="bold">Setting</text><text x="191" y="27" font-family="sans-serif" font-size="12" fill="#fff" text-anchor="start" font-weight="bold">Compile</text><text x="291" y="27" font-family="sans-serif" font-size="12" fill="#fff" text-anchor="start" font-weight="bold">Binary Size</text><text x="386" y="27" font-family="sans-serif" font-size="12" fill="#fff" text-anchor="start" font-weight="bold">Runtime Performance</text><line x1="185" y1="10" x2="185" y2="148" stroke="#aaa" stroke-width="1"/><line x1="285" y1="10" x2="285" y2="148" stroke="#aaa" stroke-width="1"/><line x1="380" y1="10" x2="380" y2="148" stroke="#aaa" stroke-width="1"/><rect x="10" y="36" width="680" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="16" y="54" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">lto = false</text><text x="191" y="54" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Fast</text><text x="291" y="54" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Larger</text><text x="386" y="54" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Baseline</text><rect x="10" y="64" width="680" height="28" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="16" y="82" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">lto = "thin"</text><text x="191" y="82" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Moderate</text><text x="291" y="82" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Smaller</text><text x="386" y="82" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Good (5–15% faster)</text><rect x="10" y="92" width="680" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="16" y="110" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">lto = true</text><text x="191" y="110" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Slow</text><text x="291" y="110" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Smallest</text><text x="386" y="110" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Best (10–20% faster)</text><rect x="10" y="120" width="680" height="28" fill="#f5f5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="16" y="138" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">codegen-units=1</text><text x="191" y="138" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Slower</text><text x="291" y="138" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Smaller</text><text x="386" y="138" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start">Better inlining</text><text x="20" y="172" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start" font-weight="bold">Recommended release profile for maximum performance:</text><rect x="10" y="180" width="680" height="24" fill="#fff9c4" stroke="#333" stroke-width="1.5" rx="4"/><text x="18" y="196" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">[profile.release]  lto=true  codegen-units=1  opt-level=3  strip=true  panic="abort"</text></svg>

---

## Part 10: Profile-Guided Optimization (PGO)

Optimize based on real workload data

---

## PGO Workflow

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="360"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="640" height="68" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="30" font-family="sans-serif" font-size="13" fill="#1565c0" text-anchor="start" font-weight="bold">Step 1: Build with instrumentation</text><text x="26" y="48" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">Source  →  Instrumented Binary</text><rect x="10" y="110" width="640" height="88" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="130" font-family="sans-serif" font-size="13" fill="#2e7d32" text-anchor="start" font-weight="bold">Step 2: Run representative workload</text><text x="26" y="148" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">Instrumented Binary + real workload</text><text x="26" y="168" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">→ writes profile data to profile_data/*.profraw</text><line x1="330" y1="78" x2="330" y2="110" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/><rect x="10" y="230" width="640" height="68" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="250" font-family="sans-serif" font-size="13" fill="#e65100" text-anchor="start" font-weight="bold">Step 3: Rebuild with profile data</text><text x="26" y="268" font-family="sans-serif" font-size="12" fill="#222" text-anchor="start">Source + profiles  →  Optimized Binary (5–20% faster)</text><line x1="330" y1="198" x2="330" y2="230" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/></svg>

---

## PGO Commands

```bash
# Step 1: Build with instrumentation
RUSTFLAGS="-Cprofile-generate=/tmp/pgo-data" \
    cargo build --release --target=x86_64-unknown-linux-gnu

# Step 2: Run your representative workload
./target/x86_64-unknown-linux-gnu/release/my_app --benchmark
./target/x86_64-unknown-linux-gnu/release/my_app --test-suite

# Step 3: Merge profile data
llvm-profdata merge -o /tmp/pgo-data/merged.profdata /tmp/pgo-data

# Step 4: Rebuild with profile data
RUSTFLAGS="-Cprofile-use=/tmp/pgo-data/merged.profdata -Cllvm-args=-pgo-warn-missing-function" \
    cargo build --release --target=x86_64-unknown-linux-gnu

# The resulting binary is optimized based on actual execution patterns:
# - Hot functions are inlined more aggressively
# - Branch prediction hints match real behavior
# - Code layout optimized for instruction cache
```

---

## Part 11: Inline Guidance

Helping the compiler make inlining decisions

---

## #[inline] Attributes

```rust
// The compiler decides whether to inline (usually good enough)
fn auto_inline(x: i32) -> i32 {
    x + 1
}

// Suggest inlining (hint, compiler may ignore)
#[inline]
fn suggest_inline(x: i32) -> i32 {
    x * 2 + 1
}

// Force inlining (compiler must obey)
#[inline(always)]
fn force_inline(x: i32) -> i32 {
    x * x
}

// Prevent inlining (useful for error paths, cold code)
#[inline(never)]
fn never_inline(x: i32) -> i32 {
    // Complex error handling, logging, etc.
    eprintln!("Error with value: {}", x);
    x
}

// #[cold] marks a function as unlikely to be called
// The compiler optimizes the caller assuming this path is rare
#[cold]
fn handle_error(msg: &str) -> ! {
    panic!("Fatal error: {}", msg);
}

fn main() {
    let x = 5;
    println!("{}", auto_inline(x));
    println!("{}", suggest_inline(x));
    println!("{}", force_inline(x));
}
```

---

## When to Use #[inline]

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="460"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="660" height="440" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="30" font-family="sans-serif" font-size="14" fill="#4a148c" text-anchor="start" font-weight="bold">#[inline] Guidelines</text><rect x="16" y="48" width="648" height="84" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="66" font-family="sans-serif" font-size="12" fill="#1b5e20" text-anchor="start" font-weight="bold">#[inline] — USE FOR:</text><text x="24" y="78" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Small functions in library crates (enables cross-crate inlining without LTO)</text><text x="24" y="96" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Wrapper / delegation functions</text><text x="24" y="114" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Hot-path functions identified by profiling</text><rect x="16" y="138" width="648" height="84" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="156" font-family="sans-serif" font-size="12" fill="#e65100" text-anchor="start" font-weight="bold">#[inline(always)] — USE FOR:</text><text x="24" y="168" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Very small functions (1–3 lines) that MUST be fast</text><text x="24" y="186" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Functions in performance-critical inner loops</text><text x="24" y="204" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Only when benchmarks prove it helps</text><rect x="16" y="228" width="648" height="84" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="246" font-family="sans-serif" font-size="12" fill="#1565c0" text-anchor="start" font-weight="bold">#[inline(never)] — USE FOR:</text><text x="24" y="258" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Error handling paths (keeps hot path small)</text><text x="24" y="276" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Functions you want to see in profiler output</text><text x="24" y="294" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Large functions called from many places (reduce code bloat)</text><rect x="16" y="318" width="648" height="66" fill="#fce4ec" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="336" font-family="sans-serif" font-size="12" fill="#b71c1c" text-anchor="start" font-weight="bold">DO NOT USE when:</text><text x="24" y="348" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• On every function 'just in case' (hurts compile time, may increase binary size)</text><text x="24" y="366" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">• Without profiling data to justify it</text></svg>

---

## Complete Performance Checklist

```rust
// Example: a well-optimized release configuration

// Cargo.toml:
// [profile.release]
// opt-level = 3
// lto = true
// codegen-units = 1
// strip = true
// panic = "abort"
//
// [dependencies]
// mimalloc = "0.1"    # or tikv-jemallocator

// src/main.rs
use mimalloc::MiMalloc;

#[global_allocator]
static GLOBAL: MiMalloc = MiMalloc;

// Use SoA for data-parallel workloads
struct Particles {
    x: Vec<f32>,
    y: Vec<f32>,
    mass: Vec<f32>,
}

// Use const for compile-time computation
const GRAVITY: f32 = 9.81;
const TABLE: [f32; 256] = {
    let mut t = [0.0f32; 256];
    let mut i = 0;
    while i < 256 {
        t[i] = i as f32 * 0.01;
        i += 1;
    }
    t
};

#[inline]
fn fast_path(x: f32) -> f32 {
    x * GRAVITY
}

#[inline(never)]
#[cold]
fn slow_error_path(msg: &str) {
    eprintln!("Error: {}", msg);
}

fn main() {
    let particles = Particles {
        x: vec![0.0; 10_000],
        y: vec![0.0; 10_000],
        mass: vec![1.0; 10_000],
    };

    // Use rayon for data parallelism
    // Use criterion for benchmarking
    // Use flamegraph for profiling
    // Consider PGO for the final production build

    println!("Particles: {}", particles.x.len());
    println!("Table[128]: {}", TABLE[128]);
    println!("Gravity force: {}", fast_path(10.0));
}
```

---

## Summary

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="400"><defs>
  <marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
  </marker>
</defs><rect x="10" y="10" width="660" height="380" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="20" y="30" font-family="sans-serif" font-size="14" fill="#1b5e20" text-anchor="start" font-weight="bold">Performance Optimization Cheatsheet</text><rect x="16" y="42" width="648" height="21" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="56" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">Zero-cost abstractions</text><text x="230" y="56" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Iterators, generics, Option<&T></text><rect x="16" y="63" width="648" height="21" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="77" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">LLVM passes</text><text x="230" y="77" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Inlining, vectorization, DCE</text><rect x="16" y="84" width="648" height="21" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="98" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">opt-level = 3</text><text x="230" y="98" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Maximum runtime optimization</text><rect x="16" y="105" width="648" height="21" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="119" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">perf + flamegraph</text><text x="230" y="119" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Find bottlenecks before optimizing</text><rect x="16" y="126" width="648" height="21" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="140" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">criterion</text><text x="230" y="140" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Statistical benchmarking</text><rect x="16" y="147" width="648" height="21" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="161" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">jemalloc / mimalloc</text><text x="230" y="161" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Faster multi-threaded allocation</text><rect x="16" y="168" width="648" height="21" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="182" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">SIMD</text><text x="230" y="182" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">4–16× throughput for data-parallel work</text><rect x="16" y="189" width="648" height="21" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="203" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">SoA layout</text><text x="230" y="203" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Cache-friendly field access</text><rect x="16" y="210" width="648" height="21" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="224" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">Arena alloc</text><text x="230" y="224" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Cache-friendly graph/tree traversal</text><rect x="16" y="231" width="648" height="21" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="245" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">const fn</text><text x="230" y="245" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Move computation to compile time</text><rect x="16" y="252" width="648" height="21" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="266" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">const generics</text><text x="230" y="266" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Type-safe compile-time parameters</text><rect x="16" y="273" width="648" height="21" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="287" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">LTO</text><text x="230" y="287" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Cross-crate optimization (10–20%)</text><rect x="16" y="294" width="648" height="21" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="308" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">PGO</text><text x="230" y="308" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Workload-guided optimization</text><rect x="16" y="315" width="648" height="21" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="329" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">#[inline]</text><text x="230" y="329" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Cross-crate inlining hint</text><rect x="16" y="336" width="648" height="21" fill="#c8e6c9" stroke="#333" stroke-width="1.5" rx="4"/><text x="24" y="350" font-family="sans-serif" font-size="11" fill="#222" text-anchor="start" font-weight="bold">codegen-units = 1</text><text x="230" y="350" font-family="sans-serif" font-size="11" fill="#333" text-anchor="start">Better optimization, slower compile</text><text x="20" y="375" font-family="sans-serif" font-size="12" fill="#b71c1c" text-anchor="start" font-weight="bold">Golden rule: MEASURE FIRST. Profile, benchmark, then optimize.</text></svg>

---

## Exercises

1. Use `cargo asm` or Compiler Explorer to compare the assembly of an iterator chain vs a hand-written loop. Are they identical?
2. Set up `criterion` benchmarks comparing `Vec<PointAoS>` vs `PointsSoA` for computing distances on 1M points.
3. Implement a custom `GlobalAlloc` that logs all allocations larger than 1 KB.
4. Write a const fn that generates a CRC32 lookup table at compile time.
5. Build a project with LTO enabled and compare binary size and runtime performance vs the default.
6. Use `cargo flamegraph` to identify the hottest function in a sample program and optimize it.
