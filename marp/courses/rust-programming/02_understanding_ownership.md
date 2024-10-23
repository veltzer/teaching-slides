---

# Understanding Ownership
## Chapter 3: Rust's Unique Memory Management

---

# What is Ownership?

```mermaid
mindmap
  root((Ownership))
    Memory Management
      No garbage collector
      No manual memory management
      Compile-time checks
    Rules
      Each value has one owner
      One owner at a time
      Scope rules apply
    Benefits
      Memory safety
      Thread safety
      Zero cost
```

---

# Ownership Rules

1. Each value has exactly one owner
2. Only one owner at a time
3. When owner goes out of scope, value is dropped

```rust
{
    let s = String::from("hello"); // s is valid from this point
    // do stuff with s
}                                  // scope is over, s is dropped
```

---

# Variable Scope

```rust
fn main() {
    // s is not valid here
    {
        let s = "hello"; // s is valid from this point
        println!("{}", s);
    } // scope is over, s is no longer valid
    // s is not valid here
}
```
