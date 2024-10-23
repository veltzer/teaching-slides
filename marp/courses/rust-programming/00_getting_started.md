# Getting Started with Rust
## Chapter 1: Introduction to Rust Programming

---

# What is Rust?

![bg right:40% 80%](https://raw.githubusercontent.com/rust-lang/rust-artwork/master/logo/rust-logo-blk.svg)

- Systems programming language
- Focuses on safety, concurrency, and performance
- Created by Mozilla Research
- First released in 2015
- Now used by: Mozilla, Microsoft, Amazon, Google

---

# Key Features of Rust

```mermaid
mindmap
  root((Rust))
    Safety
      Memory safety
      Thread safety
      No null pointers
    Performance
      Zero-cost abstractions
      No garbage collector
      Predictable performance
    Tooling
      Cargo package manager
      Built-in testing
      Great documentation
    Modern Features
      Pattern matching
      Type inference
      Trait-based generics
```

---

# Why Choose Rust?

<div class="columns">
<div>

## Benefits
- Memory safety
- Zero-cost abstractions
- Modern tooling
- Growing ecosystem

</div>
<div>

## Features
- No garbage collector
- Concurrency support
- Cross-platform
- Great documentation

</div>
</div>

---

# Use Cases for Rust

```mermaid
graph TD
    R[Rust Applications] --> Sys[Systems Programming]
    R --> Web[WebAssembly]
    R --> CLI[Command Line Tools]
    R --> Net[Network Services]
    R --> Emb[Embedded Systems]
    R --> OS[Operating Systems]
    R --> Game[Game Development]
```

---

# Rust vs Other Languages

```mermaid
graph LR
    R[Rust] --> Safety[Memory Safety]
    R --> Performance[C++ Level Performance]
    R --> Modern[Modern Ecosystem]
    
    C[C/C++] --> Performance
    C --> Legacy[Legacy Support]
    
    Go[Go] --> Modern
    Go --> GC[Garbage Collection]
    
    Java[Java] --> GC
    Java --> Modern
```

---

# Installing Rust

<div class="columns">
<div>

## Unix/Linux/macOS
```bash
curl --proto '=https' --tlsv1.2 \
     -sSf https://sh.rustup.rs | sh
```

</div>
<div>

## Windows
- Download rustup-init.exe
- Run installer
- Follow prompts

</div>
</div>

---

# Rustup Components

```mermaid
graph TD
    Rustup --> Rustc[rustc - Compiler]
    Rustup --> Cargo[cargo - Package Manager]
    Rustup --> Fmt[rustfmt - Formatter]
    Rustup --> Clippy[clippy - Linter]
    Rustup --> Docs[rust-docs - Documentation]
```

---

# Verifying Installation

```bash
# Check Rust compiler version
rustc --version

# Check Cargo version
cargo --version

# View installed components
rustup component list
```

---

# Development Environment

![bg right:40% 90%](https://code.visualstudio.com/assets/images/code-stable.png)

## Recommended Setup
- VS Code
- rust-analyzer extension
- CodeLLDB extension
- Even Better TOML extension

---

# Cargo: Rust's Package Manager

```mermaid
graph TD
    A[cargo new] --> B[Project Creation]
    B --> C[cargo build]
    C --> D[cargo run]
    C --> E[cargo test]
    B --> F[cargo check]
    B --> G[cargo doc]
```

---

# Common Cargo Commands

<div class="columns">
<div>

## Project Management
```bash
cargo new project_name
cargo build
cargo run
```

</div>
<div>

## Development
```bash
cargo check
cargo test
cargo doc
```

</div>
</div>

---

# Project Structure

```
my_project/
├── Cargo.toml          # Project manifest
├── Cargo.lock          # Lock file
└── src/
    └── main.rs         # Source code
```

---

# Cargo.toml Explained

```toml
[package]
name = "my_project"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = "1.0"
tokio = { version = "1.0", features = ["full"] }
```

---

# Hello, World!

```rust
fn main() {
    println!("Hello, World!");
}
```

---

# Basic Program Structure

```rust
// Import standard library
use std::io;

// Main function
fn main() {
    // Your code here
    println!("Basic Rust Program");
}
```

---

# Comments in Rust

```rust
// Line comment

/* Block comment
   Multiple lines */

/// Documentation comment
/// Generates docs for the following item

//! Inner documentation comment
//! Typically used at the start of a file
```

---

# Basic Syntax Elements

```mermaid
mindmap
  root((Syntax))
    Keywords
      fn
      let
      use
    Identifiers
      Variables
      Functions
      Types
    Expressions
      Operators
      Function calls
      Blocks
    Statements
      Declarations
      Assignments
      Control flow
```

---

# Function Syntax

```rust
// Basic function
fn function_name(param1: Type1, param2: Type2) -> ReturnType {
    // Function body
    return_value
}

// Example
fn add(a: i32, b: i32) -> i32 {
    a + b  // Implicit return
}
```

---

# Macro Usage

```rust
// Common macros
println!("Hello");          // Print line
format!("Value: {}", x);    // Format string
vec![1, 2, 3];             // Create vector
assert!(condition);         // Assertion

// Example usage
let name = "Rust";
println!("Hello, {}!", name);
```

---

# Basic Input/Output

```rust
use std::io;

fn main() {
    println!("What's your name?");
    
    let mut input = String::new();
    
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");
        
    println!("Hello, {}!", input.trim());
}
```

---

# Code Organization

```mermaid
graph TD
    A[Project] --> B[Modules]
    B --> C[Functions]
    B --> D[Types]
    B --> E[Tests]
    A --> F[Dependencies]
    F --> G[External Crates]
    F --> H[Standard Library]
```

---

# Best Practices

<div class="columns">
<div>

## Development
- Use rust-analyzer
- Follow style guide
- Write documentation
- Run `cargo fmt`

</div>
<div>

## Code Quality
- Use `cargo clippy`
- Write tests
- Handle errors
- Document APIs

</div>
</div>

---

# Common Mistakes to Avoid

```mermaid
mindmap
  root((Mistakes))
    Tooling
      Ignoring warnings
      Skipping cargo fmt
      Not using clippy
    Code
      Fighting borrow checker
      Premature optimization
      Poor error handling
    Process
      No documentation
      Skipping tests
      Cargo.lock in git
```

---

# Resources for Learning

<div class="columns">
<div>

## Official
- The Rust Book
- Rust by Example
- Standard Library Docs
- Rustlings

</div>
<div>

## Community
- Discord
- Reddit (r/rust)
- Stack Overflow
- GitHub

</div>
</div>

---

# Practice Exercise

Create a simple calculator that:
1. Accepts two numbers
2. Asks for operation (+, -, *, /)
3. Prints the result
4. Handles basic errors

---

# Questions?

```mermaid
graph LR
    A[Questions?] --> B[Discord]
    A --> C[Reddit]
    A --> D[GitHub]
    A --> E[Forum]
    
    B --> F[rust-lang]
    C --> G[r/rust]
    D --> H[rust-lang/rust]
    E --> I[users.rust-lang.org]
```
