---
tags:
  - languages:rust
  - concepts:programming
level: advanced
category: language
audience:
  - audiences:developers

---
# Rust and C Integration

FFI, Bindgen, and `#![no_std]`

---

## Overview

- **Calling Rust from C**
    - Types and ABI
    - Concurrency considerations
- **Calling C from Rust**
    - `bindgen` and manual bindings
    - Build system integration
- **`#![no_std]` Programming**
    - Embedded and systems programming

---

## FFI Boundary: Rust ↔ C

![ffi_boundary](svg/courses/languages/rust/advanced-rust/02_c_integration/ffi_boundary.svg)

---

## Part 1: Calling Rust from C

Exposing Rust APIs to C code

---

## Why Call Rust from C?

- Add memory safety to existing C projects
- Leverage Rust's concurrency primitives
- Use Rust's ecosystem in C applications
- Gradual migration from C to Rust
- Performance-critical components

---

## Basic FFI Setup

```rust
// lib.rs
#[no_mangle]
pub extern "C" fn add_numbers(a: i32, b: i32) -> i32 {
    a + b
}
```

```c
// main.c
#include <stdio.h>

extern int add_numbers(int a, int b);

int main() {
    int result = add_numbers(5, 3);
    printf("Result: %d\n", result);
    return 0;
}
```

---

## Building a C-Compatible Library

```toml
# Cargo.toml
[package]
name = "mylib"
version = "0.1.0"

[lib]
crate-type = ["cdylib", "staticlib"]
```

```bash
# Build shared library
cargo build --release

# Creates:
# target/release/libmylib.so   (Linux)
# target/release/libmylib.dylib (macOS)
# target/release/mylib.dll     (Windows)
```

---

## Type Compatibility

| Rust Type | C Type | Notes |
|-----------|---------|-------|
| `i8/u8` | `char/unsigned char` | 8-bit |
| `i16/u16` | `short/unsigned short` | 16-bit |
| `i32/u32` | `int/unsigned int` | 32-bit |
| `i64/u64` | `long long/unsigned long long` | 64-bit |
| `f32/f64` | `float/double` | Floating point |
| `bool` | `bool` (C99) | 1 byte |
| `*const T` | `const T*` | Pointers |

---

## String Handling

```rust
use std::ffi::{CStr, CString};
use std::os::raw::c_char;

#[no_mangle]
pub extern "C" fn greet(name: *const c_char) -> *mut c_char {
    let c_str = unsafe { CStr::from_ptr(name) };
    let rust_str = c_str.to_str().unwrap();

    let greeting = format!("Hello, {}!", rust_str);
    CString::new(greeting).unwrap().into_raw()
}

#[no_mangle]
pub extern "C" fn free_string(s: *mut c_char) {
    unsafe { CString::from_raw(s) };
}
```

---

## C Header Generation

```c
// mylib.h
#ifndef MYLIB_H
#define MYLIB_H

#include <stdint.h>

int32_t add_numbers(int32_t a, int32_t b);
char* greet(const char* name);
void free_string(char* s);

#endif
```

Consider using `cbindgen` for automatic header generation!

---

## Struct Compatibility

```rust
#[repr(C)]
pub struct Point {
    x: f64,
    y: f64,
}

#[no_mangle]
pub extern "C" fn distance(p1: Point, p2: Point) -> f64 {
    let dx = p2.x - p1.x;
    let dy = p2.y - p1.y;
    (dx * dx + dy * dy).sqrt()
}
```

`#[repr(C)]` ensures C-compatible memory layout

---

## Handling Complex Types

```rust
use std::ptr;
use std::mem;

#[repr(C)]
pub struct Buffer {
    data: *mut u8,
    len: usize,
    capacity: usize,
}

#[no_mangle]
pub extern "C" fn create_buffer(size: usize) -> *mut Buffer {
    let mut vec = Vec::with_capacity(size);
    let buffer = Buffer {
        data: vec.as_mut_ptr(),
        len: 0,
        capacity: vec.capacity(),
    };
    mem::forget(vec);
    Box::into_raw(Box::new(buffer))
}
```

---

## Error Handling Across FFI

```rust
#[repr(C)]
pub enum ErrorCode {
    Success = 0,
    InvalidInput = 1,
    OutOfMemory = 2,
    Unknown = -1,
}

#[no_mangle]
pub extern "C" fn parse_int(s: *const c_char, out: *mut i32) -> ErrorCode {
    if s.is_null() || out.is_null() {
        return ErrorCode::InvalidInput;
    }

    let c_str = unsafe { CStr::from_ptr(s) };
    match c_str.to_str() {
        Ok(rust_str) => match rust_str.parse::<i32>() {
            Ok(val) => {
                unsafe { *out = val; }
                ErrorCode::Success
            }
            Err(_) => ErrorCode::InvalidInput,
        },
        Err(_) => ErrorCode::InvalidInput,
    }
}
```

---

## Concurrency Considerations

```rust
use std::sync::Mutex;

static COUNTER: Mutex<i32> = Mutex::new(0);

#[no_mangle]
pub extern "C" fn increment_counter() -> i32 {
    let mut counter = COUNTER.lock().unwrap();
    *counter += 1;
    *counter
}

// Thread-safe from C!
// But be careful with:
// - Rust's Send/Sync traits
// - Lifetime management
// - Panic safety
```

---

## Panic Safety

```rust
use std::panic;

#[no_mangle]
pub extern "C" fn safe_operation() -> i32 {
    let result = panic::catch_unwind(|| {
        // Potentially panicking code
        dangerous_operation()
    });

    match result {
        Ok(val) => val,
        Err(_) => -1, // Error code
    }
}
```

Never let panics cross FFI boundaries!

---

## Part 2: Calling C from Rust

Using C libraries in Rust

---

## Manual C Bindings

```rust
// Using libc
extern crate libc;

extern "C" {
    fn sqrt(x: f64) -> f64;
    fn rand() -> libc::c_int;
}

fn main() {
    unsafe {
        println!("sqrt(16) = {}", sqrt(16.0));
        println!("random = {}", rand());
    }
}
```

---

## Linking C Libraries

```rust
// build.rs
fn main() {
    println!("cargo:rustc-link-lib=m");      // Link math library
    println!("cargo:rustc-link-lib=sqlite3"); // Link SQLite

    // Custom library path
    println!("cargo:rustc-link-search=/usr/local/lib");
}
```

---

## Introduction to `bindgen`

```toml
# Cargo.toml
[build-dependencies]
bindgen = "0.71"

[dependencies]
libc = "0.2"
```

Automatically generates Rust FFI bindings from C headers!

---

## Basic `bindgen` Usage

```rust
// build.rs
use bindgen;

fn main() {
    let bindings = bindgen::Builder::default()
        .header("wrapper.h")
        .parse_callbacks(Box::new(bindgen::CargoCallbacks))
        .generate()
        .expect("Unable to generate bindings");

    let out_path = std::path::PathBuf::from(
        std::env::var("OUT_DIR").unwrap()
    );
    bindings
        .write_to_file(out_path.join("bindings.rs"))
        .expect("Couldn't write bindings!");
}
```

---

## Using Generated Bindings

```rust
// src/lib.rs
#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]

include!(concat!(env!("OUT_DIR"), "/bindings.rs"));

pub fn safe_wrapper() {
    unsafe {
        // Use generated functions
        let result = some_c_function(42);
        println!("Result: {}", result);
    }
}
```

---

## Customizing `bindgen`

```rust
let bindings = bindgen::Builder::default()
    .header("wrapper.h")
    .allowlist_function("mylib_.*")  // Only functions starting with mylib_
    .allowlist_type("MyStruct")      // Only specific types
    .blocklist_type("internal_.*")   // Exclude internal types
    .derive_default(true)            // Derive Default trait
    .generate_comments(true)         // Include C comments
    .generate()
    .unwrap();
```

---

## Handling Preprocessor Macros

```c
// mylib.h
#define VERSION 100
#define MAX_SIZE 1024
#define MAGIC_NUMBER 0xDEADBEEF
```

```rust
// build.rs
let bindings = bindgen::Builder::default()
    .header("mylib.h")
    .parse_callbacks(Box::new(bindgen::CargoCallbacks))
    .constified_enum_module(".*")
    .generate()
    .unwrap();
```

---

## Opaque Pointers

```c
// C library with opaque type
typedef struct Context Context;
Context* create_context(void);
void destroy_context(Context* ctx);
```

```rust
// Rust wrapper
pub struct Context {
    ptr: *mut sys::Context,
}

impl Context {
    pub fn new() -> Self {
        unsafe {
            Context {
                ptr: sys::create_context(),
            }
        }
    }
}

impl Drop for Context {
    fn drop(&mut self) {
        unsafe { sys::destroy_context(self.ptr); }
    }
}
```

---

## Const Correctness

```rust
// C function: void process(const char* input, char* output);

extern "C" {
    fn process(
        input: *const c_char,  // const pointer
        output: *mut c_char,   // mutable pointer
    );
}

// Safe wrapper
pub fn safe_process(input: &str) -> String {
    let c_input = CString::new(input).unwrap();
    let mut output = vec![0u8; 256];

    unsafe {
        process(c_input.as_ptr(), output.as_mut_ptr() as *mut c_char);
    }

    CStr::from_bytes_with_nul(&output).unwrap().to_string_lossy().into_owned()
}
```

---

## Makefile Integration

```makefile
# Makefile
RUST_LIB = target/release/libmyrust.a

$(RUST_LIB):
    cargo build --release

myapp: main.c $(RUST_LIB)
    gcc -o myapp main.c -L target/release -lmyrust -lpthread -ldl

clean:
    cargo clean
    rm -f myapp
```

---

## CMake Integration

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.10)
project(MyApp)

# Build Rust library
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/target/release/libmyrust.a
    COMMAND cargo build --release
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

add_executable(myapp main.c)
target_link_libraries(myapp
    ${CMAKE_CURRENT_SOURCE_DIR}/target/release/libmyrust.a
    pthread dl
)
```

---

## Part 3: `#![no_std]` Programming

Rust without the standard library

---

## What is `#![no_std]`?

```rust
#![no_std]

// No access to:
// - std::vec::Vec
// - std::collections::HashMap
// - std::thread
// - std::fs, std::net
// - Heap allocation (by default)

// Still have:
// - Core types (Option, Result)
// - Basic traits
// - Slice operations
// - Core algorithms
```

---

## When to Use `#![no_std]`

- Embedded systems
- Operating system kernels
- Bootloaders
- WebAssembly (sometimes)
- Extremely constrained environments
- Real-time systems

---

## Core Library Features

```rust
#![no_std]

// Available in core:
use core::mem;
use core::slice;
use core::str;
use core::fmt;
use core::ops::{Add, Sub};
use core::cmp::{min, max};
use core::option::Option;
use core::result::Result;
```

---

## Panic Handler

```rust
#![no_std]
#![no_main]

use core::panic::PanicInfo;

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    // Custom panic behavior
    // For embedded: halt, reset, or log
    loop {}
}
```

Required for `#![no_std]` binaries!

---

## Memory Allocation

```rust
#![no_std]
#![no_main]

extern crate alloc;
use alloc::vec::Vec;
use alloc::string::String;

// Must provide a global allocator
use linked_list_allocator::LockedHeap;

#[global_allocator]
static ALLOCATOR: LockedHeap = LockedHeap::empty();

// Initialize the allocator
pub fn init_heap() {
    let heap_start = 0x_0200_0000;
    let heap_size = 100 * 1024; // 100 KiB
    unsafe {
        ALLOCATOR.lock().init(heap_start, heap_size);
    }
}
```

---

## Available `no_std` Crates

**Core functionality:**
- `heapless`: Collections without allocation
- `nb`: Non-blocking I/O traits
- `embedded-hal`: Hardware abstraction

**Data structures:**
- `arrayvec`: Vector backed by array
- `smallvec`: Small vector optimization
- `hashbrown`: HashMap implementation

---

## Memory-Mapped I/O

```rust
#![no_std]

// GPIO register addresses
const GPIO_DATA: *mut u32 = 0x4002_0000 as *mut u32;
const GPIO_DIR: *mut u32 = 0x4002_0004 as *mut u32;

pub fn set_pin_high(pin: u8) {
    unsafe {
        // Set pin as output
        let dir = GPIO_DIR.read_volatile();
        GPIO_DIR.write_volatile(dir | (1 << pin));

        // Set pin high
        let data = GPIO_DATA.read_volatile();
        GPIO_DATA.write_volatile(data | (1 << pin));
    }
}
```

---

## Safe Register Access

```rust
use volatile_register::{RW, RO};

#[repr(C)]
struct GpioRegisters {
    data: RW<u32>,    // Read-write
    direction: RW<u32>,
    interrupt_enable: RW<u32>,
    interrupt_status: RO<u32>, // Read-only
}

impl GpioRegisters {
    pub fn new(base_addr: usize) -> &'static mut Self {
        unsafe { &mut *(base_addr as *mut Self) }
    }

    pub fn set_pin_output(&mut self, pin: u8) {
        self.direction.modify(|r| r | (1 << pin));
    }
}
```

---

## Embedded Example

```rust
#![no_std]
#![no_main]

use panic_halt as _; // Halt on panic
use cortex_m_rt::entry; // Runtime entry point

#[entry]
fn main() -> ! {
    // Initialize hardware
    let peripherals = init_hardware();

    // Main loop
    loop {
        // Toggle LED
        toggle_led(&peripherals);

        // Delay
        delay_ms(500);
    }
}
```

---

## `no_std` with Allocator

```rust
#![no_std]
#![feature(alloc_error_handler)]

extern crate alloc;
use alloc::vec::Vec;
use core::alloc::Layout;

#[alloc_error_handler]
fn oom(_: Layout) -> ! {
    // Handle out of memory
    panic!("Out of memory!");
}

pub fn example() {
    let mut v = Vec::new();
    v.push(1);
    v.push(2);
    // Works with custom allocator!
}
```

---

## Cross-Compilation

```toml
# .cargo/config.toml
[target.thumbv7m-none-eabi]
runner = "arm-none-eabi-gdb"
rustflags = [
  "-C", "link-arg=-Tlink.x",
]

[build]
target = "thumbv7m-none-eabi"
```

```bash
# Install target
rustup target add thumbv7m-none-eabi

# Build
cargo build --release
```

---
## Best Practices - FFI

1. **Always use `#[repr(C)]`** for FFI structs
1. **Never panic across FFI boundaries**
1. **Validate all pointers from C**
1. **Use `CString`/`CStr` for strings**
1. **Document ownership transfer clearly**
1. **Test with sanitizers and Valgrind**

---

## Best Practices - `bindgen`

1. **Use a `wrapper.h`** to include all headers
1. **Allowlist only what you need**
1. **Generate bindings in build.rs**
1. **Create safe wrappers** for unsafe functions
1. **Handle versioning** with feature flags

---

## Best Practices - `no_std`

1. **Start with `core`** functionality
1. **Add `alloc` only if needed**
1. **Use `heapless` for collections**
1. **Profile memory usage**
1. **Test on target hardware**
1. **Use const generics** for compile-time sizing
