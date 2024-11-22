# Project Structure and Tools

## Chapter 10: Organizing and Managing Rust Projects

---

## Cargo Project Structure

![0](../../../out/mermaid/marp/courses/rust-programming/10_project_structure/0.png)

---

## Basic Project Layout

```text
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

![1](../../../out/mermaid/marp/courses/rust-programming/10_project_structure/1.png)

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

![2](../../../out/mermaid/marp/courses/rust-programming/10_project_structure/2.png)

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

![3](../../../out/mermaid/marp/courses/rust-programming/10_project_structure/3.png)

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

![4](../../../out/mermaid/marp/courses/rust-programming/10_project_structure/4.png)

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
