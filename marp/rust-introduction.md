---
marp: true
theme: default
paginate: true
_paginate: false
---

# Introduction to Rust

---

## What is Rust?

- A systems programming language
- Designed for performance, safety, and concurrency
- Developed by Mozilla Research

---

## Key Features of Rust

1. **Memory Safety**: Rust's ownership and borrowing rules prevent common memory management bugs.
2. **Concurrency**: Rust's type system and ownership model make it easier to write concurrent code without data races.
3. **Performance**: Rust is designed to be as fast as C and C++, with a focus on zero-cost abstractions.

---

## Getting Started with Rust

1. Install Rust from the official website: https://www.rust-lang.org/
2. Create a new Rust project using `cargo new my-rust-project`
3. Start writing Rust code in the `src/main.rs` file

---

## Example Rust Code

```rust
fn main() {
    println!("Hello, Rust!");
}
