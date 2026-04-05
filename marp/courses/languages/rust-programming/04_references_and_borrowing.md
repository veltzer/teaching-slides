# References and Borrowing
## Chapter 4: Memory Management in Practice

---

## What are References

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_ref0" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">References: Borrowing Without Ownership</text>
  <rect x="20" y="35" width="120" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="80" y="52" text-anchor="middle" font-size="10" font-weight="bold">&amp;s (reference)</text>
  <text x="80" y="66" text-anchor="middle" font-size="9">borrows s1</text>
  <text x="80" y="80" text-anchor="middle" font-size="9">read-only access</text>
  <rect x="220" y="35" width="140" height="55" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="290" y="52" text-anchor="middle" font-size="10" font-weight="bold">s1: String (owner)</text>
  <text x="290" y="66" text-anchor="middle" font-size="9">ptr | len:5 | cap:5</text>
  <text x="290" y="80" text-anchor="middle" font-size="9">still valid after borrow</text>
  <rect x="440" y="35" width="130" height="55" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="52" text-anchor="middle" font-size="10" font-weight="bold">Heap Data</text>
  <text x="505" y="66" text-anchor="middle" font-size="9">"hello"</text>
  <text x="505" y="80" text-anchor="middle" font-size="9">not copied</text>
  <line x1="140" y1="62" x2="220" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arr_ref0)"/>
  <text x="180" y="56" text-anchor="middle" font-size="9">points to</text>
  <line x1="360" y1="62" x2="440" y2="62" stroke="#333" stroke-width="2" marker-end="url(#arr_ref0)"/>
  <text x="400" y="56" text-anchor="middle" font-size="9">owns</text>
  <rect x="50" y="110" width="220" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="160" y="125" text-anchor="middle" font-size="10" font-weight="bold">&amp;T = immutable borrow</text>
  <text x="160" y="139" text-anchor="middle" font-size="9">Many readers allowed</text>
  <rect x="310" y="110" width="220" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="420" y="125" text-anchor="middle" font-size="10" font-weight="bold">&amp;mut T = mutable borrow</text>
  <text x="420" y="139" text-anchor="middle" font-size="9">Only ONE writer allowed</text>
  <rect x="100" y="160" width="400" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="180" text-anchor="middle" font-size="10">References never own data -- the original owner keeps ownership</text>
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
  <defs>
    <marker id="arr_ref1" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Memory Layout: &amp;s1 borrows String s1</text>
  <text x="80" y="35" text-anchor="middle" font-size="11" font-weight="bold">Stack</text>
  <rect x="20" y="45" width="120" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="80" y="64" text-anchor="middle" font-size="10">s1: { ptr, len, cap }</text>
  <rect x="20" y="75" width="120" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="80" y="92" text-anchor="middle" font-size="10">&amp;s1: ptr to s1</text>
  <text x="350" y="35" text-anchor="middle" font-size="11" font-weight="bold">Heap</text>
  <rect x="270" y="45" width="160" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="3"/>
  <text x="350" y="60" text-anchor="middle" font-size="10">"hello" (5 bytes)</text>
  <text x="350" y="73" text-anchor="middle" font-size="9">heap-allocated buffer</text>
  <line x1="140" y1="60" x2="270" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arr_ref1)" stroke-dasharray="5,3"/>
  <text x="205" y="53" text-anchor="middle" font-size="9">s1.ptr</text>
  <line x1="80" y1="75" x2="80" y2="60" stroke="#333" stroke-width="1" marker-end="url(#arr_ref1)" stroke-dasharray="3,2"/>
  <text x="100" y="70" font-size="8">&amp;s1 points to s1</text>
  <rect x="20" y="120" width="250" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="145" y="138" text-anchor="middle" font-size="10">Reference = pointer to the stack variable</text>
  <rect x="300" y="120" width="250" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="425" y="138" text-anchor="middle" font-size="10">No heap copy, no ownership transfer</text>
  <rect x="100" y="165" width="400" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="182" text-anchor="middle" font-size="10">Reference is an extra level of indirection: &amp;s1 -> s1 -> heap</text>
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
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Borrow Checker Rules at a Glance</text>
  <rect x="20" y="30" width="260" height="75" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="150" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">ALLOWED</text>
  <text x="150" y="67" text-anchor="middle" font-size="10">&amp;T + &amp;T + &amp;T (many immutable)</text>
  <text x="150" y="82" text-anchor="middle" font-size="10">&amp;mut T (one mutable, alone)</text>
  <text x="150" y="97" text-anchor="middle" font-size="9">Non-overlapping scopes: &amp;T then &amp;mut T</text>
  <rect x="320" y="30" width="260" height="75" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="450" y="50" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">REJECTED</text>
  <text x="450" y="67" text-anchor="middle" font-size="10">&amp;T + &amp;mut T (simultaneous)</text>
  <text x="450" y="82" text-anchor="middle" font-size="10">&amp;mut T + &amp;mut T (two writers)</text>
  <text x="450" y="97" text-anchor="middle" font-size="9">Dangling ref (owner dropped)</text>
  <rect x="60" y="120" width="140" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="130" y="135" text-anchor="middle" font-size="10" font-weight="bold">Compile Time</text>
  <text x="130" y="149" text-anchor="middle" font-size="9">Zero runtime cost</text>
  <rect x="230" y="120" width="140" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="135" text-anchor="middle" font-size="10" font-weight="bold">NLL (Non-Lexical)</text>
  <text x="300" y="149" text-anchor="middle" font-size="9">Ref ends at last use</text>
  <rect x="400" y="120" width="140" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="470" y="135" text-anchor="middle" font-size="10" font-weight="bold">Data Race Free</text>
  <text x="470" y="149" text-anchor="middle" font-size="9">Prevents UB at compile</text>
  <rect x="100" y="170" width="400" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="185" text-anchor="middle" font-size="10">Key insight: aliasing XOR mutation (but never both)</text>
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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="5" width="200" height="35" fill="#673ab7" stroke="#333" stroke-width="2" rx="8"/>
  <text x="300" y="28" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Borrowing Best Practices</text>
  <line x1="250" y1="40" x2="120" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="60" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="40" x2="120" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="125" stroke="#333" stroke-width="2"/>
  <rect x="30" y="55" width="180" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="72" text-anchor="middle" font-size="10" font-weight="bold">Prefer &amp;T params</text>
  <text x="120" y="86" text-anchor="middle" font-size="9">Borrow instead of taking</text>
  <text x="120" y="97" text-anchor="middle" font-size="9">ownership in functions</text>
  <rect x="390" y="55" width="180" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="72" text-anchor="middle" font-size="10" font-weight="bold">Minimize &amp;mut scope</text>
  <text x="480" y="86" text-anchor="middle" font-size="9">Drop mutable refs early</text>
  <text x="480" y="97" text-anchor="middle" font-size="9">to allow other borrows</text>
  <rect x="30" y="120" width="180" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="137" text-anchor="middle" font-size="10" font-weight="bold">Use slice params</text>
  <text x="120" y="151" text-anchor="middle" font-size="9">fn foo(s: &amp;str) not</text>
  <text x="120" y="162" text-anchor="middle" font-size="9">fn foo(s: &amp;String)</text>
  <rect x="390" y="120" width="180" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="137" text-anchor="middle" font-size="10" font-weight="bold">Avoid dangling refs</text>
  <text x="480" y="151" text-anchor="middle" font-size="9">Never return &amp;T to a</text>
  <text x="480" y="162" text-anchor="middle" font-size="9">local variable</text>
  <rect x="150" y="178" width="300" height="18" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="191" text-anchor="middle" font-size="9">Trust the borrow checker -- it prevents data races and use-after-free</text>
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
