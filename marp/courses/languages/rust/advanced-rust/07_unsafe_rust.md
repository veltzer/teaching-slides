---
tags:
  - languages:rust
  - concepts:programming
level: advanced
category: language
audience:
  - audiences:developers

---
# Unsafe Rust

Raw Pointers, Interior Mutability, Memory Layout, and Soundness

---

## Overview

- Unsafe superpowers
- Raw pointers
- Unsafe functions and traits
- Interior mutability: `Cell`, `RefCell`, `UnsafeCell`
- Memory layout and `repr`
- `transmute` and type punning
- Working with unions
- Soundness and safety invariants

---

## Unsafe Superpowers

What unsafe unlocks

---

## Unsafe Operations

![unsafe_operations](svg/courses/languages/rust/advanced-rust/07_unsafe_rust/unsafe_operations.svg)

---

## The Five Unsafe Superpowers

```rust
unsafe {
    // 1. Dereference raw pointers
    let ptr: *const i32 = &42;
    let val = *ptr;

    // 2. Call unsafe functions
    dangerous_function();

    // 3. Access mutable static variables
    COUNTER += 1;

    // 4. Implement unsafe traits
    // (done at impl level, not in unsafe block)

    // 5. Access fields of unions
    let u = MyUnion { i: 42 };
    let f = u.f;
}

static mut COUNTER: i32 = 0;
unsafe fn dangerous_function() {}
```

---

## Unsafe Does NOT Disable the Borrow Checker

```rust
fn main() {
    let mut x = 5;
    let r1 = &x;

    unsafe {
        // The borrow checker still works inside unsafe blocks!
        // let r2 = &mut x; // ERROR: cannot borrow as mutable
        println!("{}", r1);
    }

    // Unsafe only enables the five superpowers
    // All other Rust rules still apply
}
```

---

## unsafe fn vs unsafe Block

```rust
// An unsafe function: caller must uphold invariants
unsafe fn slice_from_raw(ptr: *const u8, len: usize) -> &'static [u8] {
    std::slice::from_raw_parts(ptr, len)
}

// A safe function with an internal unsafe block
fn safe_wrapper(data: &[u8]) -> &[u8] {
    // We verify the preconditions, then use unsafe
    if data.is_empty() {
        return &[];
    }
    unsafe {
        // SAFETY: ptr is valid because it comes from a valid slice,
        // and len is valid because we checked data is non-empty
        std::slice::from_raw_parts(data.as_ptr(), data.len())
    }
}

// Best practice: minimize the unsafe surface area
// Write safe wrappers around unsafe code
// Document SAFETY comments explaining why the unsafe is sound
```

---

## Raw Pointers

`*const T` and `*mut T`

---

## Raw Pointer Types

![raw_pointer_types](svg/courses/languages/rust/advanced-rust/07_unsafe_rust/raw_pointer_types.svg)

---

## Creating Raw Pointers

```rust
fn main() {
    // From references (always valid)
    let x = 42;
    let ptr: *const i32 = &x;
    let mut y = 10;
    let mut_ptr: *mut i32 = &mut y;

    // From addresses (may be invalid)
    let arbitrary_ptr = 0xDEADBEEF as *const i32;

    // Null pointers
    let null_ptr: *const i32 = std::ptr::null();
    let null_mut: *mut i32 = std::ptr::null_mut();

    // Creating raw pointers is safe
    // Dereferencing them requires unsafe
    unsafe {
        println!("*ptr = {}", *ptr);
        *mut_ptr = 20;
        println!("y = {}", y); // 20

        // Dereferencing arbitrary_ptr would be UB!
        // println!("{}", *arbitrary_ptr); // CRASH or UB
    }

    println!("null? {}", null_ptr.is_null()); // true
}
```

---

## Pointer Arithmetic

```rust
fn main() {
    let arr = [10, 20, 30, 40, 50];
    let ptr = arr.as_ptr();

    unsafe {
        // offset() moves by N elements (not bytes)
        println!("{}", *ptr);              // 10
        println!("{}", *ptr.add(1));       // 20
        println!("{}", *ptr.add(4));       // 50

        // Iterating through an array with pointers
        for i in 0..arr.len() {
            print!("{} ", *ptr.add(i));
        }
        println!();

        // sub() goes backward
        let end = ptr.add(4);
        println!("{}", *end.sub(2)); // 30

        // offset_from: distance between pointers
        let dist = end.offset_from(ptr);
        println!("Distance: {}", dist); // 4
    }
}
```

---

## Raw Pointers and Aliasing

```rust
fn main() {
    let mut data = 42;

    // In safe Rust, you cannot have &mut and & simultaneously
    // With raw pointers, you CAN (but must be careful)
    let ptr1: *mut i32 = &mut data;
    let ptr2: *const i32 = &data;

    // This is technically UB if you write through ptr1
    // while ptr2 exists and is used
    unsafe {
        *ptr1 = 100;
        // Reading through ptr2 here may or may not see the update
        // depending on compiler optimizations
        // This is a data race at the language level
    }

    // The correct way: only create one pointer at a time
    let ptr = &mut data as *mut i32;
    unsafe {
        *ptr = 200;
        println!("{}", *ptr); // 200
    }
}
```

---

## Building a Safe Abstraction

```rust
/// A simple fixed-size ring buffer
struct RingBuffer<T> {
    data: *mut T,
    capacity: usize,
    head: usize,
    len: usize,
}

impl<T> RingBuffer<T> {
    fn new(capacity: usize) -> Self {
        let layout = std::alloc::Layout::array::<T>(capacity).unwrap();
        let data = unsafe { std::alloc::alloc(layout) as *mut T };
        if data.is_null() {
            std::alloc::handle_alloc_error(layout);
        }
        RingBuffer { data, capacity, head: 0, len: 0 }
    }

    fn push(&mut self, value: T) -> Option<T> {
        let old = if self.len == self.capacity {
            // Buffer is full, overwrite oldest
            let idx = self.head;
            let old = unsafe { std::ptr::read(self.data.add(idx)) };
            self.head = (self.head + 1) % self.capacity;
            Some(old)
        } else {
            self.len += 1;
            None
        };
        let write_idx = (self.head + self.len - 1) % self.capacity;
        unsafe { std::ptr::write(self.data.add(write_idx), value); }
        old
    }
}
```

---

## Building a Safe Abstraction: Drop

```rust
impl<T> Drop for RingBuffer<T> {
    fn drop(&mut self) {
        // Drop all live elements
        for i in 0..self.len {
            let idx = (self.head + i) % self.capacity;
            unsafe { std::ptr::drop_in_place(self.data.add(idx)); }
        }
        let layout = std::alloc::Layout::array::<T>(self.capacity).unwrap();
        unsafe { std::alloc::dealloc(self.data as *mut u8, layout); }
    }
}
```

---

## Unsafe Functions and Traits

Documenting and enforcing safety contracts

---

## Writing Unsafe Functions

```rust
/// Splits a mutable slice into two at the given index.
///
/// # Safety
///
/// - `mid` must be less than or equal to `slice.len()`
/// - The caller must not create overlapping mutable references
unsafe fn split_at_mut_unchecked<T>(
    slice: &mut [T],
    mid: usize,
) -> (&mut [T], &mut [T]) {
    let ptr = slice.as_mut_ptr();
    let len = slice.len();
    // SAFETY: caller guarantees mid <= len
    (
        std::slice::from_raw_parts_mut(ptr, mid),
        std::slice::from_raw_parts_mut(ptr.add(mid), len - mid),
    )
}

// The safe version in std:
fn split_at_mut<T>(slice: &mut [T], mid: usize) -> (&mut [T], &mut [T]) {
    assert!(mid <= slice.len());
    // SAFETY: we verified mid <= len
    unsafe { split_at_mut_unchecked(slice, mid) }
}
```

---

## Unsafe Traits

```rust
/// A trait for types that can be safely initialized from zeroed memory.
///
/// # Safety
///
/// Implementing this trait asserts that a value of this type where
/// all bytes are zero is a valid, well-defined value.
unsafe trait ZeroInit {
    fn zeroed() -> Self;
}

unsafe impl ZeroInit for u32 {
    fn zeroed() -> Self { 0 }
}

unsafe impl ZeroInit for f64 {
    fn zeroed() -> Self { 0.0 }
}

// NOT safe to implement for bool (0 is false, but what about padding?)
// NOT safe for references (null is not a valid reference)
// NOT safe for String (needs valid heap pointer)

fn allocate_zeroed<T: ZeroInit>() -> T {
    T::zeroed()
}
```

---

## Interior Mutability

Mutating data behind shared references

---

## The Interior Mutability Pattern

![the_interior_mutability_pattern](svg/courses/languages/rust/advanced-rust/07_unsafe_rust/the_interior_mutability_pattern.svg)

---

## Cell<T>

```rust
use std::cell::Cell;

struct Counter {
    count: Cell<u32>,
    name: String,
}

impl Counter {
    fn new(name: &str) -> Self {
        Counter {
            count: Cell::new(0),
            name: name.to_string(),
        }
    }

    fn increment(&self) {
        // Can mutate through &self!
        self.count.set(self.count.get() + 1);
    }

    fn value(&self) -> u32 {
        self.count.get()
    }
}

fn main() {
    let counter = Counter::new("clicks");
    counter.increment(); // No &mut needed
    counter.increment();
    println!("{}: {}", counter.name, counter.value()); // clicks: 2
}
```

Cell works by copying values in and out. T must implement Copy.

---

## RefCell<T>

```rust
use std::cell::RefCell;

struct Document {
    content: RefCell<String>,
    title: String,
}

impl Document {
    fn new(title: &str) -> Self {
        Document {
            content: RefCell::new(String::new()),
            title: title.to_string(),
        }
    }

    fn append(&self, text: &str) {
        // borrow_mut() returns a RefMut<String>
        // Panics at runtime if already borrowed
        self.content.borrow_mut().push_str(text);
    }

    fn len(&self) -> usize {
        // borrow() returns a Ref<String>
        self.content.borrow().len()
    }
}
```

---

## RefCell<T>: Runtime Borrow Checks

```rust
fn main() {
    let doc = Document::new("Notes");
    doc.append("Hello ");
    doc.append("World");
    println!("{}: {} chars", doc.title, doc.len());

    // Runtime borrow checking:
    let r = doc.content.borrow();
    // doc.content.borrow_mut(); // PANIC: already borrowed!
    drop(r);
    doc.content.borrow_mut().push_str("!"); // OK now
}
```

---

## UnsafeCell<T>

```rust
use std::cell::UnsafeCell;

// UnsafeCell is the ONLY way to get interior mutability
// All other interior mutability types use it internally

struct MyCell<T> {
    value: UnsafeCell<T>,
}

// Not Sync: cannot be shared between threads safely
// (UnsafeCell opts out of Sync automatically)

impl<T: Copy> MyCell<T> {
    fn new(value: T) -> Self {
        MyCell { value: UnsafeCell::new(value) }
    }

    fn get(&self) -> T {
        // SAFETY: we only do Copy reads, never hand out references
        unsafe { *self.value.get() }
    }

    fn set(&self, value: T) {
        // SAFETY: no references to the inner value exist
        // because get() copies and we never return &T
        unsafe { *self.value.get() = value; }
    }
}
```

---

## Memory Layout and repr

Controlling how types are laid out in memory

---

## Default Rust Layout

```rust
// Rust makes NO guarantees about field ordering or padding
// The compiler may reorder fields for efficiency

struct Example {
    a: u8,    // 1 byte
    b: u32,   // 4 bytes
    c: u8,    // 1 byte
    d: u16,   // 2 bytes
}

fn main() {
    // Might be reordered to: b, d, a, c (to minimize padding)
    println!("Size: {}", std::mem::size_of::<Example>());
    println!("Align: {}", std::mem::align_of::<Example>());

    // Likely 8 bytes (reordered), not 12 bytes (naive layout)
}
```

---

## repr(C)

```rust
// C-compatible layout: fields in declaration order with C padding rules

#[repr(C)]
struct CLayout {
    a: u8,    // offset 0, 1 byte
              // 3 bytes padding
    b: u32,   // offset 4, 4 bytes
    c: u8,    // offset 8, 1 byte
              // 1 byte padding
    d: u16,   // offset 10, 2 bytes
}             // Total: 12 bytes

fn main() {
    println!("Size: {}", std::mem::size_of::<CLayout>()); // 12
    println!("Align: {}", std::mem::align_of::<CLayout>()); // 4

    // Field offsets are predictable
    println!("offset of b: {}", std::mem::offset_of!(CLayout, b)); // 4
}
```

---

## repr(packed) and repr(align)

```rust
// Remove all padding
#[repr(C, packed)]
struct Packed {
    a: u8,   // offset 0
    b: u32,  // offset 1 (unaligned!)
    c: u8,   // offset 5
}
// Size: 6, Align: 1

// Set minimum alignment
#[repr(C, align(64))]
struct CacheAligned {
    data: [u8; 32],
}
// Size: 64, Align: 64

fn main() {
    println!("Packed size: {}", std::mem::size_of::<Packed>());     // 6
    println!("Aligned size: {}", std::mem::size_of::<CacheAligned>()); // 64

    // WARNING: taking references to packed struct fields is unsafe
    // because the reference may be unaligned
    let p = Packed { a: 1, b: 2, c: 3 };
    // let r = &p.b; // ERROR: reference to unaligned field
    let b = { p.b }; // OK: copies the value
    println!("{}", b);
}
```

---

## Enum Layout

```rust
#[repr(u8)]
enum Color {
    Red = 0,
    Green = 1,
    Blue = 2,
}

#[repr(C)]
enum CEnum {
    A(u32),
    B(f64),
    C { x: i32, y: i32 },
}

// Niche optimization: Option<&T> is the same size as &T
fn main() {
    println!("Color size: {}", std::mem::size_of::<Color>());    // 1
    println!("CEnum size: {}", std::mem::size_of::<CEnum>());    // 16

    // Niche optimization example
    println!("&i32 size: {}", std::mem::size_of::<&i32>());           // 8
    println!("Option<&i32> size: {}", std::mem::size_of::<Option<&i32>>()); // 8 (same!)

    // None is represented as null pointer (the "niche")
    println!("Option<Box<i32>> size: {}", std::mem::size_of::<Option<Box<i32>>>()); // 8
}
```

---

## transmute

Type punning and raw conversions

---

## std::mem::transmute

```rust
use std::mem;

fn main() {
    // transmute reinterprets the bits of a value as another type
    // Both types must have the same size

    // Float to integer bit representation
    let float: f32 = 3.14;
    let bits: u32 = unsafe { mem::transmute(float) };
    println!("3.14 as bits: 0x{:08X}", bits); // 0x4048F5C3

    // Integer back to float
    let back: f32 = unsafe { mem::transmute(bits) };
    println!("Back to float: {}", back); // 3.14

    // Enum to integer
    #[repr(u8)]
    enum Direction { North = 0, South = 1, East = 2, West = 3 }
    let dir = Direction::East;
    let val: u8 = unsafe { mem::transmute(dir) };
    println!("East = {}", val); // 2
}
```

---

## Safer Alternatives to transmute

```rust
fn main() {
    // Instead of transmute for numeric casts:
    let x: u32 = 42;
    let y: i32 = x as i32; // Use 'as' for numeric types

    // Instead of transmute for pointer casts:
    let ptr: *const u8 = &42u8;
    let int_ptr: *const i8 = ptr as *const i8; // Use 'as' for pointers

    // For byte reinterpretation, use from/to_ne_bytes:
    let float: f64 = 3.14;
    let bytes = float.to_ne_bytes();
    let back = f64::from_ne_bytes(bytes);
    println!("{}", back);

    // For slices, use bytemuck or zerocopy crates
    // which provide safe transmute-like operations

    // transmute_copy for different-sized types (copies)
    let v: [u8; 4] = [0x01, 0x02, 0x03, 0x04];
    let n: u32 = unsafe { std::mem::transmute_copy(&v) };
    println!("0x{:08X}", n);
}
```

---

## Unions

C-compatible untagged unions

---

## Basic Unions

```rust
#[repr(C)]
union IntOrFloat {
    i: i32,
    f: f32,
}

fn main() {
    let mut u = IntOrFloat { i: 42 };

    // Reading from a union is unsafe
    // because the compiler cannot know which field is active
    unsafe {
        println!("As int: {}", u.i);   // 42
        println!("As float: {}", u.f); // Some garbage float value

        u.f = 3.14;
        println!("As float: {}", u.f); // 3.14
        println!("As int: {}", u.i);   // 0x4048F5C3 (bit pattern of 3.14)
    }

    println!("Size: {}", std::mem::size_of::<IntOrFloat>()); // 4
    // Union size = max field size
}
```

---

## Tagged Union (Manual Enum)

```rust
#[repr(C)]
union ValueData {
    integer: i64,
    float: f64,
    boolean: bool,
}

#[repr(u8)]
#[derive(Clone, Copy)]
enum ValueTag {
    Integer = 0,
    Float = 1,
    Boolean = 2,
}

#[repr(C)]
struct TaggedValue {
    tag: ValueTag,
    data: ValueData,
}

impl TaggedValue {
    fn new_int(val: i64) -> Self {
        TaggedValue { tag: ValueTag::Integer, data: ValueData { integer: val } }
    }

    fn new_float(val: f64) -> Self {
        TaggedValue { tag: ValueTag::Float, data: ValueData { float: val } }
    }

    fn as_int(&self) -> Option<i64> {
        match self.tag {
            ValueTag::Integer => unsafe { Some(self.data.integer) },
            _ => None,
        }
    }
}
```

---

## ManuallyDrop in Unions

```rust
use std::mem::ManuallyDrop;

// Unions with non-Copy fields need ManuallyDrop
union StringOrVec {
    s: ManuallyDrop<String>,
    v: ManuallyDrop<Vec<u8>>,
}

impl StringOrVec {
    fn from_string(s: String) -> Self {
        StringOrVec { s: ManuallyDrop::new(s) }
    }

    fn from_vec(v: Vec<u8>) -> Self {
        StringOrVec { v: ManuallyDrop::new(v) }
    }

    /// # Safety
    /// Must only be called when the union contains a String
    unsafe fn drop_string(&mut self) {
        ManuallyDrop::drop(&mut self.s);
    }

    /// # Safety
    /// Must only be called when the union contains a Vec
    unsafe fn drop_vec(&mut self) {
        ManuallyDrop::drop(&mut self.v);
    }
}
```

---

## Soundness and Safety Invariants

Writing correct unsafe code

---

## What is Soundness?

```rust
// A safe API is SOUND if no sequence of safe calls can cause
// undefined behavior

// This is UNSOUND:
struct BadVec<T> {
    ptr: *mut T,
    len: usize,
}

impl<T> BadVec<T> {
    fn get(&self, index: usize) -> &T {
        // BUG: no bounds checking!
        unsafe { &*self.ptr.add(index) }
    }
}

// This is SOUND:
impl<T> BadVec<T> {
    fn get_safe(&self, index: usize) -> Option<&T> {
        if index < self.len {
            unsafe { Some(&*self.ptr.add(index)) }
        } else {
            None
        }
    }
}
```

---

## Common Sources of Unsoundness

```rust
// 1. Missing bounds checks
// 2. Incorrect Send/Sync implementations
// 3. Aliased &mut references
// 4. Use after free
// 5. Uninitialized memory read
// 6. Data races
// 7. Invalid values (null references, invalid enum discriminants)

// Tools to detect unsoundness:

// Miri - an interpreter that detects UB
// $ cargo +nightly miri run
// $ cargo +nightly miri test

// Sanitizers
// $ RUSTFLAGS="-Zsanitizer=address" cargo +nightly run
// $ RUSTFLAGS="-Zsanitizer=thread" cargo +nightly run

// Loom - for testing concurrent code
// use loom::sync::Arc;
// use loom::thread;
```

---

## SAFETY Comments Convention

```rust
/// A buffer that manages its own memory.
struct Buffer {
    ptr: *mut u8,
    len: usize,
    cap: usize,
}

impl Buffer {
    fn new(cap: usize) -> Self {
        let layout = std::alloc::Layout::array::<u8>(cap).unwrap();
        // SAFETY: layout has non-zero size because cap > 0
        let ptr = unsafe { std::alloc::alloc(layout) };
        if ptr.is_null() {
            std::alloc::handle_alloc_error(layout);
        }
        Buffer { ptr, len: 0, cap }
    }

    fn push(&mut self, byte: u8) {
        assert!(self.len < self.cap, "buffer full");
        // SAFETY: we verified len < cap, and ptr is valid
        // for writes up to cap bytes (allocated in new())
        unsafe {
            self.ptr.add(self.len).write(byte);
        }
        self.len += 1;
    }

    fn as_slice(&self) -> &[u8] {
        // SAFETY: ptr is valid for len bytes (maintained by push),
        // and no &mut [u8] exists (we hold &self)
        unsafe {
            std::slice::from_raw_parts(self.ptr, self.len)
        }
    }
}
```

---

## SAFETY Comments Convention: Drop

```rust
impl Drop for Buffer {
    fn drop(&mut self) {
        let layout = std::alloc::Layout::array::<u8>(self.cap).unwrap();
        // SAFETY: ptr was allocated with this layout in new()
        unsafe { std::alloc::dealloc(self.ptr, layout); }
    }
}
```

---

## The Nomicon Rules Summary

![the_nomicon_rules_summary](svg/courses/languages/rust/advanced-rust/07_unsafe_rust/the_nomicon_rules_summary.svg)

---

## MaybeUninit for Uninitialized Memory

```rust
use std::mem::MaybeUninit;

fn create_array() -> [u32; 1000] {
    // WRONG: reading uninitialized memory is UB
    // let arr: [u32; 1000] = unsafe { std::mem::uninitialized() }; // DEPRECATED

    // RIGHT: use MaybeUninit
    let mut arr: [MaybeUninit<u32>; 1000] = unsafe {
        MaybeUninit::uninit().assume_init()
    };

    // Initialize each element
    for (i, elem) in arr.iter_mut().enumerate() {
        elem.write(i as u32);
    }

    // SAFETY: all elements have been initialized
    unsafe {
        // Transmute array of MaybeUninit<u32> to array of u32
        let ptr = arr.as_ptr() as *const [u32; 1000];
        ptr.read()
    }
}

fn main() {
    let arr = create_array();
    println!("First: {}, Last: {}", arr[0], arr[999]);
}
```

---

## Summary

![summary](svg/courses/languages/rust/advanced-rust/07_unsafe_rust/summary.svg)

---

## Exercises

1. Implement a safe `split_at_mut` using raw pointers.
1. Build a `Cell`-like type from `UnsafeCell` that works for any `Copy` type.
1. Create a `#[repr(C)]` struct and verify its layout matches C expectations.
1. Implement a simple bump allocator using raw pointer arithmetic.
1. Write a tagged union type with safe accessors and test it with Miri.
1. Use `MaybeUninit` to efficiently initialize a large array.
