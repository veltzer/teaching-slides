# Advanced Traits

Trait Objects, Generics, Associated Types, and Dispatch

---

## Overview

- Trait objects vs generics (static vs dynamic dispatch)
- Associated types and type parameters
- Supertraits and trait inheritance
- Marker traits: `Send`, `Sync`, `Sized`, `Unpin`
- Orphan rule and trait coherence
- Blanket implementations
- Performance comparison

---

## Part 1: Static Dispatch vs Dynamic Dispatch

Monomorphization vs vtables

---

## Static Dispatch with Generics

```rust
trait Shape {
    fn area(&self) -> f64;
    fn name(&self) -> &str;
}

struct Circle { radius: f64 }
struct Rectangle { width: f64, height: f64 }

impl Shape for Circle {
    fn area(&self) -> f64 { std::f64::consts::PI * self.radius * self.radius }
    fn name(&self) -> &str { "Circle" }
}

impl Shape for Rectangle {
    fn area(&self) -> f64 { self.width * self.height }
    fn name(&self) -> &str { "Rectangle" }
}

// Static dispatch: compiler generates specialized code for each type
fn print_area<T: Shape>(shape: &T) {
    println!("{}: area = {:.2}", shape.name(), shape.area());
}
```

---

## How Monomorphization Works

The compiler generates a separate function for each concrete type:

```rust
// What you write:
fn print_area<T: Shape>(shape: &T) {
    println!("{}: area = {:.2}", shape.name(), shape.area());
}

// What the compiler generates (conceptually):
fn print_area_circle(shape: &Circle) {
    println!("{}: area = {:.2}", shape.name(), shape.area());
}

fn print_area_rectangle(shape: &Rectangle) {
    println!("{}: area = {:.2}", shape.name(), shape.area());
}
```

Calls are resolved at compile time - zero runtime cost.

---

## Dynamic Dispatch with Trait Objects

```rust
// Dynamic dispatch: uses a vtable at runtime
fn print_area_dyn(shape: &dyn Shape) {
    println!("{}: area = {:.2}", shape.name(), shape.area());
}

fn main() {
    let shapes: Vec<Box<dyn Shape>> = vec![
        Box::new(Circle { radius: 5.0 }),
        Box::new(Rectangle { width: 3.0, height: 4.0 }),
    ];

    for shape in &shapes {
        print_area_dyn(shape.as_ref());
    }
}
```

---

## Vtable Layout

A trait object is a fat pointer: data pointer + vtable pointer (2 x usize).

---

## Vtable Layout

![vtable_layout](svg/courses/languages/rust/advanced-rust/03_advanced_traits/vtable_layout.svg)

---

## When to Use Which

| Aspect | Generics (static) | Trait objects (dynamic) |
|--------|-------------------|----------------------|
| Performance | Inlined, zero-cost | Indirect call overhead |
| Binary size | Larger (monomorphized) | Smaller (shared code) |
| Heterogeneous collections | No | Yes |
| Compile time | Slower | Faster |
| Type known at compile time | Yes | No |

---

## Object Safety Rules

Not all traits can be used as trait objects. A trait is object-safe if:

- All methods have `&self`, `&mut self`, or `self` receiver
- No methods return `Self`
- No methods have generic type parameters
- No associated functions (methods without `self`)
- The trait does not require `Sized`

```rust
// NOT object-safe:
trait Clone {
    fn clone(&self) -> Self; // Returns Self
}

// NOT object-safe:
trait Serialize {
    fn serialize<W: Write>(&self, writer: &mut W); // Generic parameter
}
```

---

## Making Traits Object-Safe

```rust
// Not object-safe because of Clone
trait Animal: Clone {
    fn speak(&self) -> String;
}

// Object-safe version using a workaround
trait Animal {
    fn speak(&self) -> String;
    fn clone_box(&self) -> Box<dyn Animal>;
}

impl<T: Animal + Clone + 'static> Clone for Box<dyn Animal> {
    fn clone(&self) -> Self {
        self.clone_box()
    }
}
```

---

## Restricting to Static Dispatch with Sized

```rust
trait MyTrait {
    // This method is only available for statically-dispatched calls
    fn static_only(&self) -> Self where Self: Sized;

    // This method is available for both static and dynamic dispatch
    fn works_everywhere(&self) -> String;
}

fn use_dynamic(t: &dyn MyTrait) {
    // t.static_only(); // ERROR: method not available on dyn MyTrait
    println!("{}", t.works_everywhere()); // OK
}
```

---

## Performance Benchmark: Static vs Dynamic

```rust
use std::time::Instant;

fn sum_areas_static<T: Shape>(shapes: &[T]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}

fn sum_areas_dynamic(shapes: &[Box<dyn Shape>]) -> f64 {
    shapes.iter().map(|s| s.area()).sum()
}

fn main() {
    let circles: Vec<Circle> = (0..1_000_000)
        .map(|i| Circle { radius: i as f64 })
        .collect();

    let start = Instant::now();
    let _sum = sum_areas_static(&circles);
    println!("Static dispatch: {:?}", start.elapsed());

    let boxed: Vec<Box<dyn Shape>> = (0..1_000_000)
        .map(|i| Box::new(Circle { radius: i as f64 }) as Box<dyn Shape>)
        .collect();

    let start = Instant::now();
    let _sum = sum_areas_dynamic(&boxed);
    println!("Dynamic dispatch: {:?}", start.elapsed());
}
```

---

## Part 2: Associated Types

Type placeholders in trait definitions

---

## Associated Types vs Type Parameters

```rust
// With type parameter - callers must specify the type
trait Iterator<Item> {
    fn next(&mut self) -> Option<Item>;
}

// With associated type - the implementor decides the type
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

A type can only implement `Iterator` once with associated types,
but could implement `Iterator<u32>` AND `Iterator<String>` with type parameters.

---

## Implementing Associated Types

```rust
struct Counter {
    count: u32,
    max: u32,
}

impl Counter {
    fn new(max: u32) -> Self {
        Counter { count: 0, max }
    }
}

impl Iterator for Counter {
    type Item = u32;

    fn next(&mut self) -> Option<Self::Item> {
        if self.count < self.max {
            self.count += 1;
            Some(self.count)
        } else {
            None
        }
    }
}
```

---

## Associated Types with Defaults

```rust
trait Container {
    type Item;
    type Error = std::io::Error; // Default associated type

    fn get(&self, index: usize) -> Result<&Self::Item, Self::Error>;
    fn len(&self) -> usize;
}

struct SimpleVec<T> {
    data: Vec<T>,
}

impl<T> Container for SimpleVec<T> {
    type Item = T;
    // Error uses the default std::io::Error

    fn get(&self, index: usize) -> Result<&T, std::io::Error> {
        self.data.get(index).ok_or_else(|| {
            std::io::Error::new(std::io::ErrorKind::NotFound, "index out of bounds")
        })
    }

    fn len(&self) -> usize { self.data.len() }
}
```

---

## Associated Types with Bounds

```rust
trait Graph {
    type Node: std::fmt::Display + Clone;
    type Edge: std::fmt::Display;

    fn nodes(&self) -> Vec<Self::Node>;
    fn edges(&self) -> Vec<(Self::Node, Self::Node, Self::Edge)>;
    fn add_edge(&mut self, from: Self::Node, to: Self::Node, weight: Self::Edge);
}

struct WeightedGraph {
    adjacency: Vec<Vec<(usize, f64)>>,
    labels: Vec<String>,
}

impl Graph for WeightedGraph {
    type Node = String;
    type Edge = f64;

    fn nodes(&self) -> Vec<String> { self.labels.clone() }
    fn edges(&self) -> Vec<(String, String, f64)> { todo!() }
    fn add_edge(&mut self, from: String, to: String, weight: f64) { todo!() }
}
```

---

## GATs - Generic Associated Types

```rust
trait LendingIterator {
    type Item<'a> where Self: 'a;

    fn next(&mut self) -> Option<Self::Item<'_>>;
}

struct WindowsMut<'w, T> {
    data: &'w mut [T],
    pos: usize,
    size: usize,
}

impl<'w, T> LendingIterator for WindowsMut<'w, T> {
    type Item<'a> = &'a mut [T] where Self: 'a;

    fn next(&mut self) -> Option<Self::Item<'_>> {
        if self.pos + self.size <= self.data.len() {
            let start = self.pos;
            self.pos += 1;
            Some(&mut self.data[start..start + self.size])
        } else {
            None
        }
    }
}
```

---

## Part 3: Supertraits

Trait inheritance hierarchies

---

## Basic Supertraits

```rust
use std::fmt;

// Display is a supertrait of PrettyPrint
trait PrettyPrint: fmt::Display {
    fn pretty_print(&self) {
        println!("=== {} ===", self); // Can use Display methods
    }
}

struct Point { x: f64, y: f64 }

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "({}, {})", self.x, self.y)
    }
}

// Must implement Display before implementing PrettyPrint
impl PrettyPrint for Point {}
```

---

## Multiple Supertraits

```rust
use std::fmt;

trait Serializable: fmt::Display + fmt::Debug + Clone {
    fn to_bytes(&self) -> Vec<u8>;
    fn from_bytes(bytes: &[u8]) -> Result<Self, String> where Self: Sized;
}

#[derive(Debug, Clone)]
struct Config {
    name: String,
    value: i32,
}

impl fmt::Display for Config {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}={}", self.name, self.value)
    }
}

impl Serializable for Config {
    fn to_bytes(&self) -> Vec<u8> {
        format!("{}:{}", self.name, self.value).into_bytes()
    }
    fn from_bytes(bytes: &[u8]) -> Result<Self, String> {
        let s = std::str::from_utf8(bytes).map_err(|e| e.to_string())?;
        let parts: Vec<&str> = s.splitn(2, ':').collect();
        Ok(Config {
            name: parts[0].to_string(),
            value: parts[1].parse().map_err(|e: std::num::ParseIntError| e.to_string())?,
        })
    }
}
```

---

## Supertrait Diamond Pattern

```rust
trait A {
    fn method_a(&self) -> String;
}

trait B: A {
    fn method_b(&self) -> String;
}

trait C: A {
    fn method_c(&self) -> String;
}

// D requires both B and C, which both require A
// A only needs to be implemented once
trait D: B + C {
    fn method_d(&self) -> String;
}
```

No ambiguity - Rust uses explicit trait names for disambiguation.

---

## Part 4: Marker Traits

`Send`, `Sync`, `Sized`, and `Unpin`

---

## Send and Sync

```rust
// Send: safe to transfer between threads
// Sync: safe to reference from multiple threads
// T is Sync if &T is Send

// Automatically derived for most types
struct SafeData {
    name: String,      // Send + Sync
    values: Vec<i32>,  // Send + Sync
}
// SafeData is automatically Send + Sync

// NOT Send or Sync:
use std::rc::Rc;
struct UnsafeData {
    shared: Rc<String>, // Rc is NOT Send or Sync
}
// UnsafeData is NOT Send or Sync
```

---

## Send and Sync in Practice

```rust
use std::sync::Arc;
use std::thread;

fn requires_send<T: Send>(val: T) {
    thread::spawn(move || {
        println!("Got value in new thread");
        drop(val);
    });
}

fn requires_sync<T: Sync>(val: &T) {
    // Can safely share &T across threads
}

fn main() {
    let data = Arc::new(vec![1, 2, 3]); // Arc<Vec<i32>> is Send + Sync
    requires_send(data.clone());
    requires_sync(&*data);
}
```

---

## Implementing Send and Sync Manually

```rust
struct MyPointerWrapper {
    ptr: *mut u8,
    len: usize,
}

// Raw pointers are not Send/Sync by default.
// We assert that our type is safe to use across threads.
// This is unsafe because the compiler cannot verify our claim.
unsafe impl Send for MyPointerWrapper {}
unsafe impl Sync for MyPointerWrapper {}

// DANGER: Only do this if you can guarantee:
// - For Send: no data races when moved between threads
// - For Sync: no data races when shared between threads
```

---

## Negative Trait Bounds

```rust
use std::marker::PhantomData;
use std::cell::Cell;

// Cell<T> is explicitly NOT Sync (even when T is Send)
// This is because Cell allows interior mutation without &mut

struct NotSyncType {
    data: Cell<i32>,  // Cell is !Sync
}

// You cannot send a reference to NotSyncType across threads
fn try_share(val: &NotSyncType) {
    // thread::spawn(move || {
    //     val.data.get(); // ERROR: NotSyncType is not Sync
    // });
}

// PhantomData can be used to opt out of auto traits
struct NotSend {
    _marker: PhantomData<*const ()>, // *const () is !Send
}
```

---

## The Sized Trait

```rust
// Most types are Sized - their size is known at compile time
fn takes_sized<T: Sized>(val: T) { } // T: Sized is the default

// Unsized types (dynamically sized types - DSTs):
// - str (not &str)
// - [T] (not &[T] or Vec<T>)
// - dyn Trait (not &dyn Trait or Box<dyn Trait>)

// To accept unsized types, use ?Sized
fn takes_maybe_unsized<T: ?Sized>(val: &T) { }

// This is why trait objects work:
fn print_shape(shape: &dyn Shape) { } // dyn Shape is ?Sized
```

---

## Sized in Struct Definitions

```rust
// Last field of a struct can be unsized
struct MySlice {
    len: usize,
    data: [u8], // Unsized - must be last field
}

// Generic structs default to Sized
struct Wrapper<T> { // implicitly T: Sized
    value: T,
}

// Opt out to allow unsized types
struct WrapperRef<T: ?Sized> {
    value: Box<T>, // or &T - needs indirection
}

fn main() {
    let w: WrapperRef<dyn std::fmt::Display> = WrapperRef {
        value: Box::new(42i32),
    };
    println!("{}", w.value);
}
```

---

## Unpin Trait

```rust
use std::pin::Pin;
use std::marker::Unpin;

// Most types are Unpin - they can be safely moved after being pinned
// Types that are !Unpin: self-referential types, most Futures

struct MovableData {
    value: String,
}
// MovableData: Unpin (automatically)

// A self-referential struct should NOT be moved
struct SelfRef {
    data: String,
    ptr: *const String, // Points to self.data - moving breaks this!
}
// SelfRef should be !Unpin

// Pin<&mut T> prevents moving T (if T: !Unpin)
fn pin_example(pinned: Pin<&mut SelfRef>) {
    // Cannot call std::mem::swap or move the inner value
    // pinned.get_mut() would require T: Unpin
}
```

---

## Part 5: Orphan Rule and Coherence

Preventing conflicting trait implementations

---

## The Orphan Rule

```rust
// You can implement a trait for a type ONLY IF:
// - You defined the trait, OR
// - You defined the type

// OK: Your trait on foreign type
trait MyTrait {
    fn do_thing(&self);
}
impl MyTrait for Vec<u32> {
    fn do_thing(&self) { println!("vec length: {}", self.len()); }
}

// OK: Foreign trait on your type
struct MyType;
impl std::fmt::Display for MyType {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "MyType")
    }
}

// ERROR: Foreign trait on foreign type
// impl std::fmt::Display for Vec<u32> { } // NOT ALLOWED
```

---

## The Newtype Pattern

```rust
// Workaround for the orphan rule: wrap the foreign type

struct Wrapper(Vec<String>);

impl std::fmt::Display for Wrapper {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "[{}]", self.0.join(", "))
    }
}

// Use Deref for transparent access
use std::ops::Deref;

impl Deref for Wrapper {
    type Target = Vec<String>;
    fn deref(&self) -> &Vec<String> { &self.0 }
}

fn main() {
    let w = Wrapper(vec!["hello".into(), "world".into()]);
    println!("{}", w);       // Uses our Display
    println!("{}", w.len()); // Deref to Vec methods
}
```

---

## Trait Coherence Rules

```rust
// The compiler ensures no two implementations can overlap

trait Process {
    fn process(&self);
}

impl<T: std::fmt::Display> Process for T {
    fn process(&self) { println!("Processing: {}", self); }
}

// ERROR: This would overlap with the blanket impl above
// because MyType could implement Display
// impl Process for MyType {
//     fn process(&self) { println!("Custom processing"); }
// }

// To fix: either don't have the blanket impl,
// or don't implement Display for MyType
```

---

## Part 6: Blanket Implementations

Implementing traits for broad categories of types

---

## Standard Library Blanket Impls

```rust
// From the standard library:

// Every type that implements Display automatically gets ToString
impl<T: fmt::Display> ToString for T {
    fn to_string(&self) -> String {
        format!("{}", self)
    }
}

// Every &T where T: Read also implements Read
impl<R: Read + ?Sized> Read for &mut R {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        (**self).read(buf)
    }
}

// Every T automatically implements From<T> (identity conversion)
impl<T> From<T> for T {
    fn from(t: T) -> T { t }
}
```

---

## Writing Your Own Blanket Implementations

```rust
trait Greet {
    fn greeting(&self) -> String;
}

// Blanket impl: anything that implements Display can greet
impl<T: std::fmt::Display> Greet for T {
    fn greeting(&self) -> String {
        format!("Hello, I am {}", self)
    }
}

fn main() {
    println!("{}", 42.greeting());
    println!("{}", "world".greeting());
    println!("{}", 3.14f64.greeting());
}
```

---

## Conditional Trait Implementation

```rust
struct Pair<T> {
    first: T,
    second: T,
}

// Display is only implemented when T: Display
impl<T: std::fmt::Display> std::fmt::Display for Pair<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "({}, {})", self.first, self.second)
    }
}

// Debug is only implemented when T: Debug
impl<T: std::fmt::Debug> std::fmt::Debug for Pair<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        f.debug_struct("Pair")
            .field("first", &self.first)
            .field("second", &self.second)
            .finish()
    }
}
```

---

## Extension Traits

```rust
// Add methods to existing types without orphan rule issues

trait StringExt {
    fn truncate_with_ellipsis(&self, max_len: usize) -> String;
    fn is_blank(&self) -> bool;
}

impl StringExt for str {
    fn truncate_with_ellipsis(&self, max_len: usize) -> String {
        if self.len() <= max_len {
            self.to_string()
        } else {
            format!("{}...", &self[..max_len.saturating_sub(3)])
        }
    }

    fn is_blank(&self) -> bool {
        self.trim().is_empty()
    }
}

fn main() {
    let s = "Hello, this is a very long string";
    println!("{}", s.truncate_with_ellipsis(15)); // "Hello, this ..."
    println!("{}", "   ".is_blank());             // true
}
```

---

## Part 7: Advanced Trait Patterns

Real-world patterns and idioms

---

## The Builder Pattern with Traits

```rust
trait Builder {
    type Output;
    fn build(self) -> Result<Self::Output, String>;
}

struct ServerConfig {
    host: String,
    port: u16,
    max_connections: usize,
}

struct ServerConfigBuilder {
    host: Option<String>,
    port: Option<u16>,
    max_connections: Option<usize>,
}

impl ServerConfigBuilder {
    fn new() -> Self {
        ServerConfigBuilder { host: None, port: None, max_connections: None }
    }
    fn host(mut self, host: &str) -> Self { self.host = Some(host.into()); self }
    fn port(mut self, port: u16) -> Self { self.port = Some(port); self }
    fn max_connections(mut self, n: usize) -> Self { self.max_connections = Some(n); self }
}

impl Builder for ServerConfigBuilder {
    type Output = ServerConfig;
    fn build(self) -> Result<ServerConfig, String> {
        Ok(ServerConfig {
            host: self.host.ok_or("host is required")?,
            port: self.port.unwrap_or(8080),
            max_connections: self.max_connections.unwrap_or(100),
        })
    }
}
```

---

## Type-State Pattern with Traits

```rust
// Use the type system to enforce state machine transitions

struct Locked;
struct Unlocked;

struct Door<State> {
    _state: std::marker::PhantomData<State>,
}

impl Door<Locked> {
    fn new() -> Self {
        Door { _state: std::marker::PhantomData }
    }

    fn unlock(self) -> Door<Unlocked> {
        println!("Door unlocked");
        Door { _state: std::marker::PhantomData }
    }
}

impl Door<Unlocked> {
    fn lock(self) -> Door<Locked> {
        println!("Door locked");
        Door { _state: std::marker::PhantomData }
    }

    fn open(&self) {
        println!("Door opened");
    }
}

fn main() {
    let door = Door::<Locked>::new();
    // door.open(); // ERROR: no method `open` for Door<Locked>
    let door = door.unlock();
    door.open(); // OK
}
```

---

## Trait Aliases (Nightly / Workaround)

```rust
// Trait aliases are not yet stable, but you can emulate them:

// The verbose way
fn process<T: std::fmt::Display + std::fmt::Debug + Clone + Send + 'static>(val: T) {
    // ...
}

// Create a "trait alias" with a blanket impl
trait Processable: std::fmt::Display + std::fmt::Debug + Clone + Send + 'static {}

impl<T> Processable for T
where
    T: std::fmt::Display + std::fmt::Debug + Clone + Send + 'static
{}

// Much cleaner
fn process<T: Processable>(val: T) {
    println!("{} ({:?})", val, val);
}
```

---

## Dispatch Enum Pattern

```rust
// When you know all variants at compile time, use an enum
// instead of trait objects for better performance

enum Shape {
    Circle(f64),
    Rectangle(f64, f64),
    Triangle(f64, f64, f64),
}

impl Shape {
    fn area(&self) -> f64 {
        match self {
            Shape::Circle(r) => std::f64::consts::PI * r * r,
            Shape::Rectangle(w, h) => w * h,
            Shape::Triangle(a, b, c) => {
                let s = (a + b + c) / 2.0;
                (s * (s - a) * (s - b) * (s - c)).sqrt()
            }
        }
    }
}

// Advantages over dyn Trait:
// - No heap allocation (no Box needed)
// - No vtable indirection
// - Compiler can optimize match arms
// - Size is known at compile time
```

---

## Summary

![summary](svg/courses/languages/rust/advanced-rust/03_advanced_traits/summary.svg)

---

## Exercises

1. Implement a `Drawable` trait with both static and dynamic dispatch consumers. Benchmark them.
1. Create a type-state machine for a TCP connection: `Closed -> SynSent -> Established -> Closed`.
1. Write an extension trait that adds a `.tap()` method to all types (like in Ruby).
1. Implement a plugin system using trait objects with a registry pattern.
1. Create a generic `Cache<K, V>` trait with associated types for the error type.
