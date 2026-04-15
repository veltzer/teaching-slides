---
tags:
  - languages:rust
  - concepts:programming
  - concepts:performance
level: advanced
category: language
audience:
  - audiences:developers

---
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

![what_zero_cost_means](svg/courses/languages/rust/advanced-rust/09_performance/what_zero_cost_means.svg)

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

![llvm_optimization_pipeline](svg/courses/languages/rust/advanced-rust/09_performance/llvm_optimization_pipeline.svg)

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

---
## Flamegraphs

![stack_depth_call_chain](svg/courses/languages/rust/advanced-rust/09_performance/stack_depth_call_chain.svg)

---
## Flamegraphs

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

---
## Using mimalloc

![cargo_toml](svg/courses/languages/rust/advanced-rust/09_performance/cargo_toml.svg)

---
## Part 6: SIMD

Single Instruction, Multiple Data

---
## SIMD Concepts

![simd_concepts](svg/courses/languages/rust/advanced-rust/09_performance/simd_concepts.svg)

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

1. 1. **Sequential access beats random access**
    - `Vec<T>` >> `LinkedList<T>` for iteration
1. 1. **Keep hot data together**
    - SoA layout: few fields, many items
    - AoS layout: all fields, few items
1. 1. **Minimize struct size**
    - Less data per cache line = more items per line
    - Use `#[repr(C)]` or reorder fields
1. 1. **Avoid pointer chasing**
    - `Vec<T>` instead of `Vec<Box<T>>`
    - Flatten nested structures when possible
1. 1. **Use indices instead of pointers for graphs/trees**
    - Store nodes in a `Vec`, reference by index (arena pattern)

*Cache line = 64 bytes on x86. L1 ~1 ns, L2 ~5 ns, L3 ~20 ns, DRAM ~100 ns.*

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

---
## Configuring LTO

![lto_false_default_no_cross_crate_optimization](svg/courses/languages/rust/advanced-rust/09_performance/lto_false_default_no_cross_crate_optimization.svg)

---
## LTO Trade-offs

![lto_trade_offs](svg/courses/languages/rust/advanced-rust/09_performance/lto_trade_offs.svg)

---
## Part 10: Profile-Guided Optimization (PGO)

Optimize based on real workload data

---
## PGO Workflow

![pgo_workflow](svg/courses/languages/rust/advanced-rust/09_performance/pgo_workflow.svg)

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

![when_to_use_inline](svg/courses/languages/rust/advanced-rust/09_performance/when_to_use_inline.svg)

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

![summary](svg/courses/languages/rust/advanced-rust/09_performance/summary.svg)

---
## Exercises

1. Use `cargo asm` or Compiler Explorer to compare the assembly of an iterator chain vs a hand-written loop. Are they identical?
1. Set up `criterion` benchmarks comparing `Vec<PointAoS>` vs `PointsSoA` for computing distances on 1M points.
1. Implement a custom `GlobalAlloc` that logs all allocations larger than 1 KB.
1. Write a const fn that generates a CRC32 lookup table at compile time.
1. Build a project with LTO enabled and compare binary size and runtime performance vs the default.
1. Use `cargo flamegraph` to identify the hottest function in a sample program and optimize it.
