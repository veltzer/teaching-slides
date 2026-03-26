# References and Borrowing
## Chapter 4: Memory Management in Practice

---

## What are References

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_03_references_and_borrowing)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_03_references_and_borrowing)"/>
  <defs>
    <marker id="arrowd0_03_references_and_borrowing" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Basic References

```rust
fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(&s1);
    println!("Length of '{}' is {}", s1, len);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}
```

---

## Memory Layout: References

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_references_and_borrowing)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_references_and_borrowing)"/>
  <defs>
    <marker id="arrowd1_03_references_and_borrowing" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Reference Rules

1. At any given time, you can have either:
    - One mutable reference
    - Any number of immutable references
1. References must always be valid
1. References can't outlive their referent

---

## Mutable References

```rust
fn main() {
    let mut s = String::from("hello");
    change(&mut s);
    println!("{}", s);  // prints "hello world"
}

fn change(s: &mut String) {
    s.push_str(" world");
}
```

---

## Reference Scope

```rust
let mut s = String::from("hello");

{
    let r1 = &s; // ok
    let r2 = &s; // ok
    println!("{} and {}", r1, r2);
} // r1 and r2 go out of scope here

let r3 = &mut s; // ok
println!("{}", r3);
```

---

## Reference Restrictions

```rust
let mut s = String::from("hello");

let r1 = &mut s;
let r2 = &mut s; // ERROR!

println!("{}", r1);
```

---

## Data Race Prevention

```rust
let mut s = String::from("hello");

let r1 = &s;     // ok
let r2 = &s;     // ok
let r3 = &mut s; // ERROR!

println!("{}, {}, and {}", r1, r2, r3);
```

---

## Dangling References

```rust
fn dangle() -> &String {            // WRONG
    let s = String::from("hello");
    &s
}   // s is dropped here

fn no_dangle() -> String {         // CORRECT
    String::from("hello")
}
```

---

## Reference Lifetime

```rust
fn main() {
    let x = 5;
    let r = &x;
    println!("r: {}", r);
}  // x and r go out of scope
```

---

## Mutable and Immutable Together

```rust
let mut s = String::from("hello");

let r1 = &s; // ok
let r2 = &s; // ok
println!("{} and {}", r1, r2);
// r1 and r2 are no longer used after this point

let r3 = &mut s; // ok
println!("{}", r3);
```

---

## Borrowing Rules Visualization

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_03_references_and_borrowing)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_03_references_and_borrowing)"/>
  <defs>
    <marker id="arrowd2_03_references_and_borrowing" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Reference in Structs

```rust
struct Person {
    name: String,
    reference: &String,  // WRONG: needs lifetime
}

struct ValidPerson<'a> {
    name: String,
    reference: &'a String,  // Correct with lifetime
}
```

---

## Multiple References

```rust
fn main() {
    let mut s = String::from("hello");
    let r1 = &s;
    let r2 = &s;
    let r3 = &s;
    println!("{} {} {}", r1, r2, r3);
}
```

---

## Mutable Reference Mutation

```rust
fn main() {
    let mut s = String::from("hello");
    let r1 = &mut s;
    r1.push_str(" world");    // ok
    println!("{}", r1);       // hello world
}
```

---

## Borrowing in Functions

```rust
fn print_string(s: &String) {
    println!("{}", s);
}

fn modify_string(s: &mut String) {
    s.push_str(" world");
}

fn main() {
    let mut s = String::from("hello");
    print_string(&s);
    modify_string(&mut s);
}
```

---

## Borrowing and Ownership

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = &s1;        // borrowing
    let s3 = s1;         // ownership move
    println!("{}", s2);  // ERROR: s1 was moved
}
```

---

## References vs. Smart Pointers

```rust
use std::rc::Rc;

let s = Rc::new(String::from("hello"));
let s1 = &s;        // Reference
let s2 = Rc::clone(&s); // Smart Pointer clone
```

---

## Auto-Dereferencing

```rust
fn main() {
    let s = String::from("hello");
    let s_ref = &s;
    println!("Length: {}", s_ref.len());
    // Rust automatically dereferences s_ref
}
```

---

## References in Collections

```rust
fn main() {
    let mut vec = Vec::new();
    let s = String::from("hello");
    vec.push(&s);  // Store reference
    println!("{}", vec[0]);
}
```

---

## Common Reference Patterns

```rust
// Passing large structs
fn process_data(data: &LargeStruct) { }

// Modifying in place
fn update_data(data: &mut LargeStruct) { }

// Multiple readers
fn read_data(data1: &Data, data2: &Data) { }
```

---

## Error Patterns to Avoid

```rust
// Don't return references to local variables
fn wrong() -> &String {  // ERROR
    let s = String::from("hello");
    &s
}

// Don't create mutable references if not needed
fn unnecessary(s: &mut String) {  // Use &String if not modifying
    println!("{}", s);
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

## Practice Exercise

Create functions that:
1. Use immutable references
1. Use mutable references
1. Handle multiple references
1. Demonstrate scope rules
1. Show reference patterns

---

## Common Pitfalls
1. Fighting the borrow checker
1. Unnecessary mutable references
1. Reference lifetime issues
1. Complex borrowing patterns
1. Returning dangling references

---

## Summary
- Reference basics
- Borrowing rules
- Mutable references
- Scope and lifetime
- Best practices
