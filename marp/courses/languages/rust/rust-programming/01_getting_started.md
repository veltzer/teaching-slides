# Getting Started with Rust
## Chapter 1: Introduction to Rust Programming

---
## What is Rust

![bg right:40% 80%](https://raw.githubusercontent.com/rust-lang/rust-artwork/master/logo/rust-logo-blk.svg)

- Systems programming language
- Focuses on safety, concurrency, and performance
- Created by Mozilla Research
- First released in 2015
- Now used by: Mozilla, Microsoft, Amazon, Google
---
## Key Features of Rust

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <ellipse cx="100" cy="40" rx="55" ry="25" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <ellipse cx="500" cy="40" rx="55" ry="25" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <ellipse cx="100" cy="165" rx="55" ry="25" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <ellipse cx="500" cy="165" rx="55" ry="25" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="300" y="105" text-anchor="middle" font-size="12" fill="white">Rust</text>
  <text x="100" y="44" text-anchor="middle" font-size="11">Memory Safety</text>
  <text x="500" y="44" text-anchor="middle" font-size="11">Concurrency</text>
  <text x="100" y="169" text-anchor="middle" font-size="11">Performance</text>
  <text x="500" y="169" text-anchor="middle" font-size="11">Zero-Cost</text>
  <text x="500" y="181" text-anchor="middle" font-size="10">Abstractions</text>
  <line x1="245" y1="80" x2="150" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="80" x2="450" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="245" y1="120" x2="150" y2="148" stroke="#333" stroke-width="2"/>
  <line x1="355" y1="120" x2="450" y2="148" stroke="#333" stroke-width="2"/>
</svg>

---
## Why Choose Rust

<div class="columns">
<div>

### Benefits
- Memory safety
- Zero-cost abstractions
- Modern tooling
- Growing ecosystem

</div>
<div>

### Features
- No garbage collector
- Concurrency support
- Cross-platform
- Great documentation

</div>
</div>

---

## Use Cases for Rust

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="60" width="110" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="170" y="60" width="110" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="320" y="60" width="110" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="470" y="60" width="110" height="50" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="82" text-anchor="middle" font-size="11" font-weight="bold">Systems</text>
  <text x="75" y="98" text-anchor="middle" font-size="10">OS, Drivers</text>
  <text x="225" y="82" text-anchor="middle" font-size="11" font-weight="bold">WebAssembly</text>
  <text x="225" y="98" text-anchor="middle" font-size="10">Browser, Edge</text>
  <text x="375" y="82" text-anchor="middle" font-size="11" font-weight="bold">CLI Tools</text>
  <text x="375" y="98" text-anchor="middle" font-size="10">ripgrep, bat</text>
  <text x="525" y="82" text-anchor="middle" font-size="11" font-weight="bold">Networking</text>
  <text x="525" y="98" text-anchor="middle" font-size="10">Servers, APIs</text>
  <rect x="170" y="140" width="260" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="165" text-anchor="middle" font-size="12" font-weight="bold">Embedded / IoT</text>
  <line x1="75" y1="110" x2="200" y2="140" stroke="#333" stroke-width="1" stroke-dasharray="4"/>
  <line x1="525" y1="110" x2="400" y2="140" stroke="#333" stroke-width="1" stroke-dasharray="4"/>
</svg>

---

## Rust vs Other Languages

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_rvs" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="120" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="43" text-anchor="middle" font-size="11" font-weight="bold">C / C++</text>
  <text x="80" y="60" text-anchor="middle" font-size="10">Manual memory</text>
  <rect x="240" y="20" width="120" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="43" text-anchor="middle" font-size="11" font-weight="bold">Rust</text>
  <text x="300" y="60" text-anchor="middle" font-size="10">Ownership system</text>
  <rect x="460" y="20" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="520" y="43" text-anchor="middle" font-size="11" font-weight="bold">Java / Go</text>
  <text x="520" y="60" text-anchor="middle" font-size="10">Garbage collected</text>
  <line x1="140" y1="47" x2="240" y2="47" stroke="#333" stroke-width="2" marker-end="url(#arr_rvs)"/>
  <line x1="460" y1="47" x2="360" y2="47" stroke="#333" stroke-width="2" marker-end="url(#arr_rvs)"/>
  <rect x="60" y="105" width="200" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="160" y="124" text-anchor="middle" font-size="10">Speed: C/C++ ~ Rust >> Java/Go</text>
  <rect x="340" y="105" width="200" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="440" y="124" text-anchor="middle" font-size="10">Safety: Rust >> C/C++, ~ Java/Go</text>
  <rect x="150" y="155" width="300" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="175" text-anchor="middle" font-size="11" font-weight="bold">Rust = Speed + Safety (no GC!)</text>
</svg>

---

## Installing Rust

<div class="columns">
<div>

### Unix/Linux/macOS

```bash
curl --proto '=https' --tlsv1.2 -sSf 'https://sh.rustup.rs' | sh
```

</div>
<div>

### Windows
- Download rustup-init.exe
- Run installer
- Follow prompts

</div>
</div>

---

## Rustup Components

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="10" width="200" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="13" font-weight="bold">rustup</text>
  <rect x="30" y="80" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="105" text-anchor="middle" font-size="11">rustc (compiler)</text>
  <rect x="180" y="80" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="240" y="105" text-anchor="middle" font-size="11">cargo (build)</text>
  <rect x="330" y="80" width="120" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="390" y="105" text-anchor="middle" font-size="11">rustfmt (fmt)</text>
  <rect x="480" y="80" width="110" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="535" y="105" text-anchor="middle" font-size="11">clippy (lint)</text>
  <line x1="230" y1="50" x2="120" y2="80" stroke="#333" stroke-width="1.5"/>
  <line x1="280" y1="50" x2="240" y2="80" stroke="#333" stroke-width="1.5"/>
  <line x1="330" y1="50" x2="370" y2="80" stroke="#333" stroke-width="1.5"/>
  <line x1="380" y1="50" x2="510" y2="80" stroke="#333" stroke-width="1.5"/>
  <rect x="100" y="150" width="160" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="180" y="172" text-anchor="middle" font-size="10">Toolchains: stable, beta, nightly</text>
  <rect x="340" y="150" width="160" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="420" y="172" text-anchor="middle" font-size="10">Targets: x86, ARM, WASM</text>
</svg>

---

## Verifying Installation

```bash
# Check Rust compiler version
rustc --version

# Check Cargo version
cargo --version

# View installed components
rustup component list
```

---

## Development Environment

<svg width="200" height="200" xmlns="http://www.w3.org/2000/svg" style="float: right; margin: 20px;">
  <!-- VS Code Logo -->
  <rect x="10" y="10" width="180" height="180" fill="#007acc" rx="20"/>

  <!-- Left panel (darker blue) -->
  <path d="M 30 30 L 30 170 L 70 150 L 70 50 Z" fill="#0062a3"/>

  <!-- Code symbol (white) -->
  <path d="M 85 70 L 125 110 L 85 150" stroke="white" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M 155 70 L 115 110 L 155 150" stroke="white" stroke-width="12" fill="none" stroke-linecap="round" stroke-linejoin="round"/>

  <!-- VS Code text -->
  <text x="100" y="185" text-anchor="middle" font-size="14" font-weight="bold" fill="#007acc">VS Code</text>
</svg>

### Recommended Setup
- VS Code
- rust-analyzer extension
- CodeLLDB extension
- Even Better TOML extension

---

## Cargo: Rust's Package Manager

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_cargo" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="15" width="110" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="40" text-anchor="middle" font-size="11" font-weight="bold">Cargo.toml</text>
  <rect x="245" y="15" width="110" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="40" text-anchor="middle" font-size="11" font-weight="bold">cargo build</text>
  <rect x="460" y="15" width="110" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="40" text-anchor="middle" font-size="11" font-weight="bold">Binary / Lib</text>
  <line x1="140" y1="35" x2="245" y2="35" stroke="#333" stroke-width="2" marker-end="url(#arr_cargo)"/>
  <line x1="355" y1="35" x2="460" y2="35" stroke="#333" stroke-width="2" marker-end="url(#arr_cargo)"/>
  <rect x="30" y="80" width="110" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="85" y="102" text-anchor="middle" font-size="10">crates.io registry</text>
  <rect x="170" y="80" width="100" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="220" y="102" text-anchor="middle" font-size="10">cargo test</text>
  <rect x="300" y="80" width="100" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="350" y="102" text-anchor="middle" font-size="10">cargo run</text>
  <rect x="430" y="80" width="100" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="480" y="102" text-anchor="middle" font-size="10">cargo doc</text>
  <rect x="100" y="140" width="400" height="45" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="158" text-anchor="middle" font-size="10">Cargo.lock -- dependency resolution + reproducible builds</text>
  <text x="300" y="175" text-anchor="middle" font-size="10">target/ -- build artifacts (debug / release)</text>
</svg>

---

## Common Cargo Commands

<div class="columns">
<div>

### Project Management

```bash
cargo new project_name
cargo build
cargo run
```

</div>
<div>

### Development

```bash
cargo check
cargo test
cargo doc
```

</div>
</div>

---

## Project Structure

```text
my_project/
+-- Cargo.toml          # Project manifest
+-- Cargo.lock          # Lock file
+-- src/
    +-- main.rs         # Source code
```

---

## Cargo.toml Explained

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
## Hello, World

```rust
fn main() {
    println!("Hello, World!");
}
```

---
## Basic Program Structure

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
## Comments in Rust

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
## Basic Syntax Elements

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="35" text-anchor="middle" font-size="11" font-weight="bold">Variables</text>
  <rect x="160" y="10" width="120" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="220" y="28" text-anchor="middle" font-size="11" font-weight="bold">Functions</text>
  <text x="220" y="42" text-anchor="middle" font-size="10">fn name() {}</text>
  <rect x="300" y="10" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="360" y="28" text-anchor="middle" font-size="11" font-weight="bold">Types</text>
  <text x="360" y="42" text-anchor="middle" font-size="10">i32, bool, str</text>
  <rect x="440" y="10" width="140" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="28" text-anchor="middle" font-size="11" font-weight="bold">Control Flow</text>
  <text x="510" y="42" text-anchor="middle" font-size="10">if, match, loop</text>
  <rect x="20" y="70" width="560" height="50" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="90" text-anchor="middle" font-size="11" font-weight="bold">Expressions vs Statements</text>
  <text x="300" y="108" text-anchor="middle" font-size="10">Everything is an expression (returns a value) -- no trailing semicolon = return value</text>
  <rect x="20" y="140" width="175" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="107" y="158" text-anchor="middle" font-size="10">let mut x = 5;</text>
  <text x="107" y="175" text-anchor="middle" font-size="10">Immutable by default</text>
  <rect x="215" y="140" width="175" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="302" y="158" text-anchor="middle" font-size="10">println!("{}",x);</text>
  <text x="302" y="175" text-anchor="middle" font-size="10">Macros use !</text>
  <rect x="410" y="140" width="170" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="495" y="158" text-anchor="middle" font-size="10">// comment</text>
  <text x="495" y="175" text-anchor="middle" font-size="10">/// doc comment</text>
</svg>

---
## Function Syntax

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
## Macro Usage

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
## Basic Input/Output

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
## Code Organization

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_org" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="20" width="120" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="38" text-anchor="middle" font-size="11" font-weight="bold">Crate</text>
  <text x="90" y="54" text-anchor="middle" font-size="10">(compilation unit)</text>
  <rect x="200" y="20" width="120" height="45" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="260" y="38" text-anchor="middle" font-size="11" font-weight="bold">Modules</text>
  <text x="260" y="54" text-anchor="middle" font-size="10">mod my_mod {}</text>
  <rect x="370" y="20" width="120" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="430" y="38" text-anchor="middle" font-size="11" font-weight="bold">Functions</text>
  <text x="430" y="54" text-anchor="middle" font-size="10">fn / pub fn</text>
  <line x1="150" y1="42" x2="200" y2="42" stroke="#333" stroke-width="2" marker-end="url(#arr_org)"/>
  <line x1="320" y1="42" x2="370" y2="42" stroke="#333" stroke-width="2" marker-end="url(#arr_org)"/>
  <rect x="30" y="90" width="560" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="110" text-anchor="middle" font-size="11">use crate::module::function; -- path-based imports with visibility control (pub)</text>
  <rect x="30" y="140" width="170" height="45" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="115" y="158" text-anchor="middle" font-size="10" font-weight="bold">src/main.rs</text>
  <text x="115" y="175" text-anchor="middle" font-size="10">Binary crate root</text>
  <rect x="220" y="140" width="170" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="305" y="158" text-anchor="middle" font-size="10" font-weight="bold">src/lib.rs</text>
  <text x="305" y="175" text-anchor="middle" font-size="10">Library crate root</text>
  <rect x="410" y="140" width="180" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="500" y="158" text-anchor="middle" font-size="10" font-weight="bold">src/module_name.rs</text>
  <text x="500" y="175" text-anchor="middle" font-size="10">Or src/module_name/mod.rs</text>
</svg>

---
## Best Practices

<div class="columns">
<div>

### Development
- Use rust-analyzer
- Follow style guide
- Write documentation
- Run `cargo fmt`

</div>
<div>

### Code Quality
- Use `cargo clippy`
- Write tests
- Handle errors
- Document APIs

</div>
</div>

---
## Common Mistakes to Avoid

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="10" width="270" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="25" text-anchor="middle" font-size="10" fill="#c62828">let s1 = String::from("hi"); let s2 = s1;</text>
  <text x="155" y="42" text-anchor="middle" font-size="10" fill="#c62828">println!("{}", s1); // Error: value moved</text>
  <rect x="310" y="10" width="270" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="25" text-anchor="middle" font-size="10" fill="#2e7d32">let s1 = String::from("hi");</text>
  <text x="445" y="42" text-anchor="middle" font-size="10" fill="#2e7d32">let s2 = s1.clone(); // OK: deep copy</text>
  <rect x="20" y="65" width="270" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="80" text-anchor="middle" font-size="10" fill="#c62828">let mut s = String::new();</text>
  <text x="155" y="97" text-anchor="middle" font-size="10" fill="#c62828">let r1 = &amp;mut s; let r2 = &amp;mut s; // Error</text>
  <rect x="310" y="65" width="270" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="80" text-anchor="middle" font-size="10" fill="#2e7d32">Use r1, then drop scope;</text>
  <text x="445" y="97" text-anchor="middle" font-size="10" fill="#2e7d32">then create r2 // OK</text>
  <rect x="20" y="120" width="270" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="135" text-anchor="middle" font-size="10" fill="#c62828">Missing semicolons / wrong return</text>
  <text x="155" y="152" text-anchor="middle" font-size="10" fill="#c62828">fn f() -> i32 { 5; } // returns ()</text>
  <rect x="310" y="120" width="270" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="135" text-anchor="middle" font-size="10" fill="#2e7d32">Implicit return (no semicolon)</text>
  <text x="445" y="152" text-anchor="middle" font-size="10" fill="#2e7d32">fn f() -> i32 { 5 } // returns 5</text>
  <rect x="120" y="172" width="160" height="22" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="200" y="187" text-anchor="middle" font-size="10" font-weight="bold">Common Mistakes</text>
  <rect x="320" y="172" width="160" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="400" y="187" text-anchor="middle" font-size="10" font-weight="bold">Correct Patterns</text>
</svg>

---
## Resources for Learning

<div class="columns">
<div>

### Official
- The Rust Book
- Rust by Example
- Standard Library Docs
- Rustlings

</div>
<div>

### Community
- Discord
- Reddit (r/rust)
- Stack Overflow
- GitHub

</div>
</div>
