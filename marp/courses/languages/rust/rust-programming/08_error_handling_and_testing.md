# Error Handling and Testing
## Chapter 7: Writing Reliable Code

---

## Types of Errors

![types_of_errors](svg/courses/languages/rust/rust-programming/08_error_handling_and_testing/types_of_errors.svg)

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

![best_practices](svg/courses/languages/rust/rust-programming/08_error_handling_and_testing/best_practices.svg)

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
