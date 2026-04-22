---
tags:
  - languages:rust
  - concepts:programming
level: beginner
category: language
audience:
  - audiences:developers

---
# Project Structure and Tools

## Chapter 10: Organizing and Managing Rust Projects

---

## Cargo Project Structure

![cargo_project_structure](svg/courses/languages/rust/rust-programming/11_project_structure/cargo_project_structure.svg)

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
edition = "2024"

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

![project_configuration](svg/courses/languages/rust/rust-programming/11_project_structure/project_configuration.svg)

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

![development_tools](svg/courses/languages/rust/rust-programming/11_project_structure/development_tools.svg)

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
    - uses: actions/checkout@v4
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
.env
```

- Commit `Cargo.lock` for binaries and workspaces
- Ignore `Cargo.lock` only for pure library crates

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

![dependency_management](svg/courses/languages/rust/rust-programming/11_project_structure/dependency_management.svg)

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
// `#[bench]` is nightly-only. On stable, use the `criterion` crate.
use criterion::{black_box, criterion_group, criterion_main, Criterion};

fn bench_add(c: &mut Criterion) {
    c.bench_function("add 2+2", |b| {
        b.iter(|| add(black_box(2), black_box(2)))
    });
}

criterion_group!(benches, bench_add);
criterion_main!(benches);
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

![security_best_practices](svg/courses/languages/rust/rust-programming/11_project_structure/security_best_practices.svg)

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
