# Error Handling and Testing
## Chapter 7: Writing Reliable Code

---

## Types of Errors

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_07_error_handling_and_testing)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_07_error_handling_and_testing)"/>
  <defs>
    <marker id="arrowd0_07_error_handling_and_testing" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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
