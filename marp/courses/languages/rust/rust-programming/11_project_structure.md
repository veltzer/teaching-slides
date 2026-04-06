# Project Structure and Tools

## Chapter 10: Organizing and Managing Rust Projects

---

## Cargo Project Structure

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="220" y="10" width="160" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="33" text-anchor="middle" font-size="12" font-weight="bold">Workspace</text>
  <rect x="50" y="75" width="130" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="115" y="97" text-anchor="middle" font-size="11">crate: app</text>
  <rect x="235" y="75" width="130" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="97" text-anchor="middle" font-size="11">crate: core</text>
  <rect x="420" y="75" width="130" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="485" y="97" text-anchor="middle" font-size="11">crate: utils</text>
  <rect x="30" y="140" width="100" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="80" y="160" text-anchor="middle" font-size="10">mod main</text>
  <rect x="145" y="140" width="100" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="195" y="160" text-anchor="middle" font-size="10">mod config</text>
  <rect x="260" y="140" width="100" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="310" y="160" text-anchor="middle" font-size="10">mod lib</text>
  <rect x="375" y="140" width="100" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="425" y="160" text-anchor="middle" font-size="10">mod models</text>
  <rect x="490" y="140" width="100" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="540" y="160" text-anchor="middle" font-size="10">mod helpers</text>
  <line x1="260" y1="45" x2="115" y2="75" stroke="#333" stroke-width="1.5"/>
  <line x1="300" y1="45" x2="300" y2="75" stroke="#333" stroke-width="1.5"/>
  <line x1="340" y1="45" x2="485" y2="75" stroke="#333" stroke-width="1.5"/>
  <line x1="80" y1="110" x2="80" y2="140" stroke="#333" stroke-width="1.5"/>
  <line x1="150" y1="110" x2="195" y2="140" stroke="#333" stroke-width="1.5"/>
  <line x1="300" y1="110" x2="310" y2="140" stroke="#333" stroke-width="1.5"/>
  <line x1="420" y1="110" x2="425" y2="140" stroke="#333" stroke-width="1.5"/>
  <line x1="550" y1="110" x2="540" y2="140" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Basic Project Layout

```tree
my_project/
+-- Cargo.toml
+-- Cargo.lock
+-- src/
|   +-- main.rs
|   +-- lib.rs
|   +-- bin/
+-- tests/
+-- examples/
+-- benches/
+-- docs/
```

---

## Cargo.toml Structure

```toml
[package]
name = "my_project"
version = "0.1.0"
authors = ["Your Name <you@example.com>"]
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1.0", features = ["full"] }

[dev-dependencies]
pretty_assertions = "1.0"

[build-dependencies]
cc = "1.0"
```

---

## Workspace Structure

```toml
# workspace root Cargo.toml
[workspace]
members = [
    "app",
    "core",
    "utils",
]

[workspace.dependencies]
serde = "1.0"
```

---

## Module Organization

```rust
// lib.rs
mod front_of_house;
pub mod customer;

// front_of_house.rs
pub mod hosting {
    pub fn add_to_waitlist() {}
}

// customer.rs
use crate::front_of_house::hosting;
```

---

## Use Declarations

```rust
use std::{fmt, io};
use std::collections::*;
use self::front_of_house::hosting;
pub use crate::front_of_house::hosting;

fn main() {
    hosting::add_to_waitlist();
}
```

---

## Project Configuration

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="10" width="200" height="35" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="33" text-anchor="middle" font-size="12" font-weight="bold">Cargo.toml</text>
  <rect x="30" y="75" width="120" height="30" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="90" y="95" text-anchor="middle" font-size="10">[package]</text>
  <rect x="170" y="75" width="120" height="30" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="230" y="95" text-anchor="middle" font-size="10">[dependencies]</text>
  <rect x="310" y="75" width="130" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="375" y="95" text-anchor="middle" font-size="10">[dev-dependencies]</text>
  <rect x="460" y="75" width="120" height="30" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="520" y="95" text-anchor="middle" font-size="10">[features]</text>
  <rect x="140" y="135" width="100" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="190" y="154" text-anchor="middle" font-size="10">serde 1.0</text>
  <rect x="260" y="135" width="100" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="310" y="154" text-anchor="middle" font-size="10">tokio 1.0</text>
  <rect x="380" y="135" width="110" height="28" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="435" y="154" text-anchor="middle" font-size="10">pretty_assertions</text>
  <rect x="200" y="170" width="90" height="24" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="245" y="187" text-anchor="middle" font-size="9">serde_json</text>
  <line x1="230" y1="105" x2="190" y2="135" stroke="#333" stroke-width="1.5"/>
  <line x1="230" y1="105" x2="310" y2="135" stroke="#333" stroke-width="1.5"/>
  <line x1="375" y1="105" x2="435" y2="135" stroke="#333" stroke-width="1.5"/>
  <line x1="190" y1="163" x2="245" y2="170" stroke="#333" stroke-width="1"/>
</svg>

---

## Build Profiles

```toml
[profile.dev]
opt-level = 0
debug = true

[profile.release]
opt-level = 3
debug = false
lto = true

[profile.test]
opt-level = 0
debug = true
```

---

## Feature Flags

```toml
[features]
default = ["console"]
console = []
gui = ["gtk"]

[dependencies]
gtk = { version = "0.1", optional = true }
```

---

## Development Tools

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="150" rx="60" ry="40" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="80" rx="50" ry="30" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="80" rx="50" ry="30" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="220" rx="50" ry="30" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="220" rx="50" ry="30" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-size="12" fill="white">Core</text>
  <text x="150" y="85" text-anchor="middle" font-size="11">Concept 1</text>
  <text x="450" y="85" text-anchor="middle" font-size="11">Concept 2</text>
  <text x="150" y="225" text-anchor="middle" font-size="11">Concept 3</text>
  <text x="450" y="225" text-anchor="middle" font-size="11">Concept 4</text>
  <line x1="250" y1="130" x2="190" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="130" x2="410" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="170" x2="190" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="170" x2="410" y2="200" stroke="#333" stroke-width="2"/>
</svg>

---

## Code Organization Best Practices

<div class="columns">
<div>

## Structure
- Clear hierarchy
- Logical grouping
- Public interfaces
- Private implementation

</div>
<div>

## Naming
- Descriptive names
- Consistent style
- Clear purpose
- Module hierarchy

</div>
</div>

---

## Documentation

```rust
/// Adds two numbers together
///
/// # Examples
///
/// ```
/// let sum = my_crate::add(2, 2);
/// assert_eq!(sum, 4);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

---

## Testing Organization

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn unit_test() {
        // test implementation
    }
}

// tests/integration_test.rs
use my_crate;

#[test]
fn integration_test() {
    // test implementation
}
```

---

## Continuous Integration

```yaml
# .github/workflows/rust.yml
name: Rust CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build
      run: cargo build --verbose
    - name: Run tests
      run: cargo test --verbose
```

---

## Publishing to crates.io

```bash
# Update version in Cargo.toml
# Verify package
cargo publish --dry-run

# Publish
cargo publish
```

---

## Version Control Best Practices

```gitignore
/target
**/*.rs.bk
Cargo.lock
.env
```

---

## Build Scripts

```rust
// build.rs
fn main() {
    println!("cargo:rerun-if-changed=src/hello.c");
    cc::Build::new()
        .file("src/hello.c")
        .compile("hello");
}
```

---

## Dependency Management

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowvis" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="10" y="15" width="130" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="35" text-anchor="middle" font-size="11" font-weight="bold">crate root</text>
  <text x="75" y="52" text-anchor="middle" font-size="10">(lib.rs)</text>
  <rect x="10" y="90" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="70" y="115" text-anchor="middle" font-size="10">pub mod api</text>
  <rect x="10" y="150" width="120" height="40" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="70" y="175" text-anchor="middle" font-size="10">mod internal</text>
  <rect x="200" y="90" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="260" y="115" text-anchor="middle" font-size="10">pub fn serve()</text>
  <rect x="200" y="150" width="130" height="40" fill="#ffebee" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="265" y="175" text-anchor="middle" font-size="10">fn helper()</text>
  <rect x="400" y="20" width="190" height="80" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="495" y="42" text-anchor="middle" font-size="11" font-weight="bold">Visibility Rules</text>
  <text x="495" y="60" text-anchor="middle" font-size="10" fill="#2e7d32">pub = accessible outside</text>
  <text x="495" y="78" text-anchor="middle" font-size="10" fill="#c62828">no pub = private to module</text>
  <rect x="400" y="120" width="190" height="70" fill="#f3e5f5" stroke="#333" stroke-width="1.5" rx="5"/>
  <text x="495" y="142" text-anchor="middle" font-size="10">pub(crate) = crate only</text>
  <text x="495" y="160" text-anchor="middle" font-size="10">pub(super) = parent only</text>
  <text x="495" y="178" text-anchor="middle" font-size="10">pub(in path) = specific</text>
  <line x1="75" y1="70" x2="70" y2="90" stroke="#333" stroke-width="1.5"/>
  <line x1="75" y1="70" x2="70" y2="150" stroke="#333" stroke-width="1.5"/>
  <line x1="130" y1="110" x2="200" y2="110" stroke="#333" stroke-width="1.5" marker-end="url(#arrowvis)"/>
  <line x1="130" y1="170" x2="200" y2="170" stroke="#333" stroke-width="1.5" marker-end="url(#arrowvis)"/>
</svg>

---

## Cross Compilation

```toml
# .cargo/config.toml
[target.x86_64-pc-windows-gnu]
linker = "x86_64-w64-mingw32-gcc"
ar = "x86_64-w64-mingw32-ar"
```

---
## Project Automation

```bash
#!/bin/bash
# build.sh

cargo fmt -- --check
cargo clippy -- -D warnings
cargo test
cargo build --release
```

---

## IDE Integration

```json
{
    "rust-analyzer.checkOnSave.command": "clippy",
    "rust-analyzer.cargo.features": ["full"],
    "rust-analyzer.inlayHints.enable": true
}
```

---

## Benchmarking

```rust
#[bench]
fn bench_add(b: &mut test::Bencher) {
    b.iter(|| {
        // Code to benchmark
        add(2, 2)
    });
}
```

---
## Profiling Tools

```bash
# Flamegraph generation
cargo install flamegraph
cargo flamegraph

# Memory profiling
valgrind --leak-check=full ./target/debug/myapp
```

---

## Error Handling Strategy

```rust
#[derive(Debug)]
pub enum AppError {
    IoError(std::io::Error),
    ParseError(std::num::ParseIntError),
    CustomError(String),
}

impl std::error::Error for AppError {}
```

---

### Project Templates

```bash
# Create new project from template
cargo generate --git https://github.com/user/template

# Or using cargo-new
cargo new my_project --bin
```

---

## Security Best Practices

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="150" rx="60" ry="40" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="80" rx="50" ry="30" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="80" rx="50" ry="30" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <ellipse cx="150" cy="220" rx="50" ry="30" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <ellipse cx="450" cy="220" rx="50" ry="30" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-size="12" fill="white">Core</text>
  <text x="150" y="85" text-anchor="middle" font-size="11">Concept 1</text>
  <text x="450" y="85" text-anchor="middle" font-size="11">Concept 2</text>
  <text x="150" y="225" text-anchor="middle" font-size="11">Concept 3</text>
  <text x="450" y="225" text-anchor="middle" font-size="11">Concept 4</text>
  <line x1="250" y1="130" x2="190" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="130" x2="410" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="170" x2="190" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="170" x2="410" y2="200" stroke="#333" stroke-width="2"/>
</svg>

---

## Practice Exercise

Create a complete project that:
1. Uses proper structure
1. Implements workspaces
1. Has comprehensive tests
1. Includes documentation
1. Uses CI/CD

---

## Summary
- Project organization
- Tools and workflows
- Documentation
- Testing strategy
- Publishing process
