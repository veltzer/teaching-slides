# Error Handling and Testing
## Chapter 7: Writing Reliable Code

---

## Types of Errors

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_err" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Rust Error Handling: Two Categories</text>
  <rect x="20" y="30" width="180" height="70" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="48" text-anchor="middle" font-size="11" font-weight="bold">Unrecoverable</text>
  <text x="110" y="63" text-anchor="middle" font-size="10">panic!("msg")</text>
  <text x="110" y="78" text-anchor="middle" font-size="9">Unwinds stack or aborts</text>
  <text x="110" y="91" text-anchor="middle" font-size="9">Bugs, invariant violations</text>
  <rect x="210" y="30" width="180" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="48" text-anchor="middle" font-size="11" font-weight="bold">Recoverable</text>
  <text x="300" y="63" text-anchor="middle" font-size="10">Result&lt;T, E&gt;</text>
  <text x="300" y="78" text-anchor="middle" font-size="9">Ok(value) | Err(error)</text>
  <text x="300" y="91" text-anchor="middle" font-size="9">File not found, parse fail</text>
  <rect x="400" y="30" width="180" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="490" y="48" text-anchor="middle" font-size="11" font-weight="bold">Absence</text>
  <text x="490" y="63" text-anchor="middle" font-size="10">Option&lt;T&gt;</text>
  <text x="490" y="78" text-anchor="middle" font-size="9">Some(value) | None</text>
  <text x="490" y="91" text-anchor="middle" font-size="9">No null pointers</text>
  <line x1="200" y1="65" x2="210" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arr_err)"/>
  <line x1="390" y1="65" x2="400" y2="65" stroke="#333" stroke-width="2" marker-end="url(#arr_err)"/>
  <rect x="20" y="115" width="560" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="130" text-anchor="middle" font-size="10" font-weight="bold">The ? Operator: Propagate errors concisely</text>
  <text x="300" y="144" text-anchor="middle" font-size="10">File::open("f.txt")?.read_to_string(&amp;mut s)? -- returns Err early if failure</text>
  <rect x="100" y="165" width="400" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="182" text-anchor="middle" font-size="10">No exceptions -- errors are values you must handle or propagate</text>
</svg>

---

## Unrecoverable Errors: panic

```rust
fn main() {
    panic!("crash and burn");
}

// Run with RUST_BACKTRACE=1 for stack trace
```

---

## Stack Unwinding vs Abort

```toml
# Cargo.toml
[profile.release]
panic = 'abort'  # Disable unwinding
```

```rust
fn main() {
    let v = vec![1, 2, 3];
    v[99]; // This will cause a panic
}
```

---
## Recoverable Errors: Result

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}

fn get_username(id: i32) -> Result<String, io::Error> {
    // ... implementation
}
```

---

## Handling Result

```rust
let f = File::open("hello.txt");

let f = match f {
    Ok(file) => file,
    Err(error) => panic!("Problem opening file: {:?}", error),
};
```

---

## Multiple Error Types

```rust
use std::io;
use std::fs::File;

fn read_username() -> Result<String, io::Error> {
    let mut username = String::new();
    File::open("hello.txt")?.read_to_string(&mut username)?;
    Ok(username)
}
```

---

## The ? Operator

```rust
fn read_file() -> Result<String, io::Error> {
    let mut f = File::open("hello.txt")?;
    let mut s = String::new();
    f.read_to_string(&mut s)?;
    Ok(s)
}
```

---

## Custom Error Types

```rust
#[derive(Debug)]
enum AppError {
    IoError(std::io::Error),
    ParseError(std::num::ParseIntError),
    ValidationError(String),
}

impl From<std::io::Error> for AppError {
    fn from(error: std::io::Error) -> Self {
        AppError::IoError(error)
    }
}
```

---

## Error Propagation

```rust
fn function_that_might_fail() -> Result<Success, Error> {
    let f = File::open("hello.txt")?;
    let contents = read_file_contents(f)?;
    process_contents(contents)
}
```

---

## Unit Testing Basics

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let result = 2 + 2;
        assert_eq!(result, 4);
    }
}
```

---

## Test Attributes

```rust
#[test]
#[should_panic(expected = "panic message")]
#[ignore]
fn expensive_test() {
    // Test implementation
}
```

---

## Assert Macros

```rust
// Basic assertions
assert!(condition);
assert_eq!(left, right);
assert_ne!(left, right);

// With custom messages
assert!(
    condition,
    "Expected condition to be true, got false"
);
```

---

## Test Organization

```rust
// Unit tests
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn internal_test() {
        // Test private functionality
    }
}

// Integration tests in tests/ directory
```

---

## Integration Tests

```rust
// In tests/integration_test.rs
use my_crate;

#[test]
fn test_external_api() {
    assert!(my_crate::public_function());
}
```

---

## Test Fixtures

```rust
#[cfg(test)]
mod tests {
    use super::*;

    fn setup() -> TestStruct {
        TestStruct::new()
    }

    #[test]
    fn test_with_fixture() {
        let test_struct = setup();
        assert!(test_struct.is_valid());
    }
}
```

---

## Running Tests

```bash
# Run all tests
cargo test

# Run single test
cargo test test_name

# Run tests with pattern
cargo test pattern

# Show output
cargo test -- --nocapture
```

---

## Test Documentation

```rust
/// ```
/// # Example
/// ```
/// let result = my_crate::add(2, 2);
/// assert_eq!(result, 4);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

---

## Parameterized Tests

```rust
#[test]
fn test_multiple_cases() {
    let test_cases = vec![
        (2, 2, 4),
        (3, 3, 6),
        (0, 1, 1),
    ];

    for (a, b, expected) in test_cases {
        assert_eq!(add(a, b), expected);
    }
}
```

---

## Mocking in Tests

```rust
trait Database {
    fn get_user(&self, id: u32) -> Result<User, Error>;
}

struct MockDatabase {
    users: HashMap<u32, User>,
}

impl Database for MockDatabase {
    fn get_user(&self, id: u32) -> Result<User, Error> {
        self.users.get(&id)
            .cloned()
            .ok_or(Error::UserNotFound)
    }
}
```

---

## Benchmark Tests

```rust
#![feature(test)]
extern crate test;

#[cfg(test)]
mod tests {
    use test::Bencher;

    #[bench]
    fn bench_add(b: &mut Bencher) {
        b.iter(|| {
            // Code to benchmark
        });
    }
}
```

---

## Result in Tests

```rust
#[test]
fn test_with_result() -> Result<(), String> {
    if 2 + 2 == 4 {
        Ok(())
    } else {
        Err(String::from("two plus two does not equal four"))
    }
}
```

---

## Testing Private Functions

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_private_function() {
        assert!(private_function());
    }
}
```

---

## Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="5" width="200" height="35" fill="#673ab7" stroke="#333" stroke-width="2" rx="8"/>
  <text x="300" y="28" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Error &amp; Testing Tips</text>
  <line x1="250" y1="40" x2="120" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="40" x2="120" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="125" stroke="#333" stroke-width="2"/>
  <rect x="30" y="53" width="180" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="70" text-anchor="middle" font-size="10" font-weight="bold">Use ? over unwrap()</text>
  <text x="120" y="84" text-anchor="middle" font-size="9">Reserve .unwrap() for tests</text>
  <text x="120" y="95" text-anchor="middle" font-size="9">and prototypes only</text>
  <rect x="390" y="53" width="180" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="70" text-anchor="middle" font-size="10" font-weight="bold">Custom error types</text>
  <text x="480" y="84" text-anchor="middle" font-size="9">enum AppError with From</text>
  <text x="480" y="95" text-anchor="middle" font-size="9">impls for conversion</text>
  <rect x="30" y="120" width="180" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="137" text-anchor="middle" font-size="10" font-weight="bold">Test edge cases</text>
  <text x="120" y="151" text-anchor="middle" font-size="9">#[should_panic] for panics</text>
  <text x="120" y="162" text-anchor="middle" font-size="9">Result returns in #[test]</text>
  <rect x="390" y="120" width="180" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="137" text-anchor="middle" font-size="10" font-weight="bold">Organize tests</text>
  <text x="480" y="151" text-anchor="middle" font-size="9">Unit: #[cfg(test)] mod</text>
  <text x="480" y="162" text-anchor="middle" font-size="9">Integration: tests/ dir</text>
  <rect x="150" y="178" width="300" height="18" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="191" text-anchor="middle" font-size="9">Use anyhow/thiserror crates for ergonomic error handling</text>
</svg>

---

## Code Coverage

```bash
# Install cargo-tarpaulin
cargo install cargo-tarpaulin

# Run coverage analysis
cargo tarpaulin

# Generate report
cargo tarpaulin -o Html
```

---
## Practice Exercise
Create a library that:
1. Implements error handling
1. Has comprehensive tests
1. Includes documentation tests
1. Uses test fixtures
1. Has integration tests
---
## Common Pitfalls
1. Inadequate error handling
1. Missing edge cases
1. Brittle tests
1. Poor test organization
1. Insufficient documentation
---
## Summary
- Error types and handling
- Testing methodology
- Test organization
- Coverage and benchmarking
- Best practices
