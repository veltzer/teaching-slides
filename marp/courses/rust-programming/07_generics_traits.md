# Generic Types and Traits
## Chapter 6: Abstraction and Code Reuse

---
## What are Generics

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Generics: Write Once, Use with Any Type</text>
  <rect x="20" y="30" width="170" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="48" text-anchor="middle" font-size="10" font-weight="bold">Generic Functions</text>
  <text x="105" y="63" text-anchor="middle" font-size="9">fn largest&lt;T&gt;(list: &amp;[T])</text>
  <text x="105" y="76" text-anchor="middle" font-size="9">Type param T resolved</text>
  <text x="105" y="87" text-anchor="middle" font-size="9">at compile time</text>
  <rect x="215" y="30" width="170" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="48" text-anchor="middle" font-size="10" font-weight="bold">Generic Structs</text>
  <text x="300" y="63" text-anchor="middle" font-size="9">struct Point&lt;T&gt; { x: T }</text>
  <text x="300" y="76" text-anchor="middle" font-size="9">Point&lt;i32&gt;, Point&lt;f64&gt;</text>
  <text x="300" y="87" text-anchor="middle" font-size="9">each a distinct type</text>
  <rect x="410" y="30" width="170" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="48" text-anchor="middle" font-size="10" font-weight="bold">Generic Enums</text>
  <text x="495" y="63" text-anchor="middle" font-size="9">Option&lt;T&gt;, Result&lt;T,E&gt;</text>
  <text x="495" y="76" text-anchor="middle" font-size="9">Built into the language</text>
  <text x="495" y="87" text-anchor="middle" font-size="9">used everywhere</text>
  <rect x="60" y="105" width="480" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="122" text-anchor="middle" font-size="11" font-weight="bold">Monomorphization</text>
  <text x="300" y="137" text-anchor="middle" font-size="10">Compiler generates specialized code for each concrete type used -- zero runtime cost</text>
  <rect x="60" y="160" width="230" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="175" y="179" text-anchor="middle" font-size="9">fn foo&lt;T&gt;(x: T) with i32 -> fn foo_i32(x: i32)</text>
  <rect x="310" y="160" width="230" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="425" y="179" text-anchor="middle" font-size="9">fn foo&lt;T&gt;(x: T) with f64 -> fn foo_f64(x: f64)</text>
</svg>

---

## Function with Generics

```rust
fn largest<T>(list: &[T]) -> &T
where T: PartialOrd {
    let mut largest = &list[0];

    for item in list {
        if item > largest {
            largest = item;
        }
    }

    largest
}
```

---

## Generic Structs

```rust
struct Point<T> {
    x: T,
    y: T,
}

// Usage
let integer = Point { x: 5, y: 10 };
let float = Point { x: 1.0, y: 4.0 };
```

---

## Multiple Generic Parameters

```rust
struct Point<T, U> {
    x: T,
    y: U,
}

let mixed = Point { x: 5, y: 4.0 };
```

---

## Generic Enums

```rust
enum Option<T> {
    Some(T),
    None,
}

enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

---

## Generic Methods

```rust
impl<T> Point<T> {
    fn x(&self) -> &T {
        &self.x
    }
}

// Specific type implementation
impl Point<f64> {
    fn distance_from_origin(&self) -> f64 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}
```

---

## What are Traits

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_trait" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Traits: Shared Behavior (like interfaces)</text>
  <rect x="20" y="30" width="150" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="95" y="48" text-anchor="middle" font-size="10" font-weight="bold">trait Summary</text>
  <text x="95" y="63" text-anchor="middle" font-size="9">fn summarize(&amp;self)</text>
  <text x="95" y="76" text-anchor="middle" font-size="9">  -> String</text>
  <rect x="225" y="25" width="150" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="40" text-anchor="middle" font-size="10" font-weight="bold">NewsArticle</text>
  <text x="300" y="54" text-anchor="middle" font-size="9">impl Summary for ...</text>
  <rect x="225" y="65" width="150" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="80" text-anchor="middle" font-size="10" font-weight="bold">Tweet</text>
  <text x="300" y="94" text-anchor="middle" font-size="9">impl Summary for ...</text>
  <line x1="170" y1="50" x2="225" y2="42" stroke="#333" stroke-width="2" marker-end="url(#arr_trait)"/>
  <line x1="170" y1="65" x2="225" y2="82" stroke="#333" stroke-width="2" marker-end="url(#arr_trait)"/>
  <rect x="430" y="25" width="150" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="42" text-anchor="middle" font-size="10" font-weight="bold">Static Dispatch</text>
  <text x="505" y="56" text-anchor="middle" font-size="9">fn notify&lt;T: Summary&gt;</text>
  <text x="505" y="70" text-anchor="middle" font-size="9">Monomorphized, inlined</text>
  <text x="505" y="84" text-anchor="middle" font-size="10" font-weight="bold">Dynamic Dispatch</text>
  <text x="505" y="98" text-anchor="middle" font-size="9">dyn Summary (vtable)</text>
  <rect x="20" y="115" width="280" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="160" y="130" text-anchor="middle" font-size="10" font-weight="bold">Trait Bounds: T: Display + Clone</text>
  <text x="160" y="144" text-anchor="middle" font-size="9">Constrain generic types to required behavior</text>
  <rect x="320" y="115" width="260" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="450" y="130" text-anchor="middle" font-size="10" font-weight="bold">Default Implementations</text>
  <text x="450" y="144" text-anchor="middle" font-size="9">Provide fallback method bodies in trait</text>
  <rect x="100" y="165" width="400" height="25" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="182" text-anchor="middle" font-size="10">Traits = Rust's primary abstraction mechanism (no inheritance)</text>
</svg>

---

## Defining Traits

```rust
trait Summary {
    fn summarize(&self) -> String;

    fn default_behavior(&self) -> String {
        String::from("Default implementation")
    }
}
```

---

## Implementing Traits

```rust
struct NewsArticle {
    pub headline: String,
    pub content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}", self.headline)
    }
}
```

---

## Trait Bounds

```rust
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}

// Multiple bounds
pub fn notify<T: Summary + Display>(item: &T)
```

---

## Where Clauses

```rust
fn some_function<T, U>(t: &T, u: &U) -> i32
    where T: Display + Clone,
          U: Clone + Debug
{
    // function body
}
```

---

## Default Implementations

```rust
trait Summary {
    fn summarize_author(&self) -> String;

    fn summarize(&self) -> String {
        format!("(Read more from {}...)", self.summarize_author())
    }
}
```

---

## Trait Objects

```rust
pub trait Draw {
    fn draw(&self);
}

pub struct Screen {
    pub components: Vec<Box<dyn Draw>>,
}

impl Screen {
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}
```

---

## Object Safety

```rust
trait Clone {
    fn clone(&self) -> Self;  // Not object safe
}

trait Draw {
    fn draw(&self);  // Object safe
}
```

---

## Associated Types

```rust
trait Iterator {
    type Item;  // Associated type

    fn next(&mut self) -> Option<Self::Item>;
}
```

---

## Operator Overloading

```rust
use std::ops::Add;

impl Add for Point {
    type Output = Point;

    fn add(self, other: Point) -> Point {
        Point {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}
```

---

## Supertraits

```rust
trait OutlinePrint: Display {
    fn outline_print(&self) {
        let output = self.to_string();
        println!("*************");
        println!("*{}*", output);
        println!("*************");
    }
}
```

---

## Newtype Pattern

```rust
struct Wrapper(Vec<String>);

impl Display for Wrapper {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "[{}]", self.0.join(", "))
    }
}
```

---

## Conditional Implementation

```rust
impl<T: Display> ToString for T {
    // --snip--
}

impl<T: Display + PartialOrd> MyTrait for T {
    fn compare(&self, other: &T) -> bool {
        self > other
    }
}
```

---

## Common Traits

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Essential Std Library Traits</text>
  <rect x="20" y="28" width="130" height="50" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="85" y="44" text-anchor="middle" font-size="10" font-weight="bold">Display/Debug</text>
  <text x="85" y="58" text-anchor="middle" font-size="9">Formatting output</text>
  <text x="85" y="70" text-anchor="middle" font-size="9">{} and {:?}</text>
  <rect x="160" y="28" width="130" height="50" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="225" y="44" text-anchor="middle" font-size="10" font-weight="bold">Clone/Copy</text>
  <text x="225" y="58" text-anchor="middle" font-size="9">Duplication semantics</text>
  <text x="225" y="70" text-anchor="middle" font-size="9">deep vs bitwise</text>
  <rect x="300" y="28" width="130" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="365" y="44" text-anchor="middle" font-size="10" font-weight="bold">PartialEq/Eq</text>
  <text x="365" y="58" text-anchor="middle" font-size="9">Equality comparison</text>
  <text x="365" y="70" text-anchor="middle" font-size="9">== and !=</text>
  <rect x="440" y="28" width="140" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="510" y="44" text-anchor="middle" font-size="10" font-weight="bold">PartialOrd/Ord</text>
  <text x="510" y="58" text-anchor="middle" font-size="9">Ordering comparison</text>
  <text x="510" y="70" text-anchor="middle" font-size="9">&lt; &gt; &lt;= &gt;= .sort()</text>
  <rect x="20" y="90" width="130" height="50" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="85" y="106" text-anchor="middle" font-size="10" font-weight="bold">From/Into</text>
  <text x="85" y="120" text-anchor="middle" font-size="9">Type conversion</text>
  <text x="85" y="132" text-anchor="middle" font-size="9">impl From&lt;T&gt;</text>
  <rect x="160" y="90" width="130" height="50" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="225" y="106" text-anchor="middle" font-size="10" font-weight="bold">Drop</text>
  <text x="225" y="120" text-anchor="middle" font-size="9">Destructor / cleanup</text>
  <text x="225" y="132" text-anchor="middle" font-size="9">RAII pattern</text>
  <rect x="300" y="90" width="130" height="50" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="365" y="106" text-anchor="middle" font-size="10" font-weight="bold">Iterator</text>
  <text x="365" y="120" text-anchor="middle" font-size="9">Lazy sequences</text>
  <text x="365" y="132" text-anchor="middle" font-size="9">.next() -> Option</text>
  <rect x="440" y="90" width="140" height="50" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="510" y="106" text-anchor="middle" font-size="10" font-weight="bold">AsRef/Deref</text>
  <text x="510" y="120" text-anchor="middle" font-size="9">Cheap conversion</text>
  <text x="510" y="132" text-anchor="middle" font-size="9">auto-dereferencing</text>
  <rect x="100" y="155" width="400" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="170" text-anchor="middle" font-size="10" font-weight="bold">Most can be derived: #[derive(Debug, Clone, PartialEq)]</text>
  <text x="300" y="184" text-anchor="middle" font-size="9">Compiler auto-generates implementations for simple structs/enums</text>
</svg>

---

## From and Into

```rust
struct Number {
    value: i32,
}

impl From<i32> for Number {
    fn from(item: i32) -> Self {
        Number { value: item }
    }
}

let num = Number::from(30);
let int: i32 = num.into();
```

---

## AsRef and AsMut

```rust
fn process<T: AsRef<str>>(data: T) {
    let s = data.as_ref();
    // Process the string slice
}

// Can be used with String, &str, Path, etc.
process("hello");
process(String::from("hello"));
```

---

## Drop Trait

```rust
struct CustomSmartPointer {
    data: String,
}

impl Drop for CustomSmartPointer {
    fn drop(&mut self) {
        println!("Dropping CustomSmartPointer!");
    }
}
```

---

## Sized Trait

```rust
// T must be Sized
fn generic<T>(t: T) {
    // --snip--
}

// T may not be Sized
fn generic<T: ?Sized>(t: &T) {
    // --snip--
}
```

---

## Practice Exercise

Create a generic data structure that:
1. Stores any type
1. Implements multiple traits
1. Uses associated types
1. Provides custom operators

---

## Performance Considerations

```rust
// Monomorphization
fn process<T: Display>(x: T) {
    println!("{}", x);
}

// Becomes:
fn process_i32(x: i32) {
    println!("{}", x);
}
fn process_string(x: String) {
    println!("{}", x);
}
```

---

## Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="5" width="200" height="35" fill="#673ab7" stroke="#333" stroke-width="2" rx="8"/>
  <text x="300" y="28" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Generics/Traits Tips</text>
  <line x1="250" y1="40" x2="120" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="40" x2="120" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="125" stroke="#333" stroke-width="2"/>
  <rect x="30" y="53" width="180" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="70" text-anchor="middle" font-size="10" font-weight="bold">Minimal bounds</text>
  <text x="120" y="84" text-anchor="middle" font-size="9">Only require traits you</text>
  <text x="120" y="95" text-anchor="middle" font-size="9">actually call methods on</text>
  <rect x="390" y="53" width="180" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="70" text-anchor="middle" font-size="10" font-weight="bold">Static over dynamic</text>
  <text x="480" y="84" text-anchor="middle" font-size="9">Prefer impl Trait / generics</text>
  <text x="480" y="95" text-anchor="middle" font-size="9">over dyn Trait when possible</text>
  <rect x="30" y="120" width="180" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="137" text-anchor="middle" font-size="10" font-weight="bold">#[derive] first</text>
  <text x="120" y="151" text-anchor="middle" font-size="9">Auto-derive Debug, Clone,</text>
  <text x="120" y="162" text-anchor="middle" font-size="9">PartialEq before manual impl</text>
  <rect x="390" y="120" width="180" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="137" text-anchor="middle" font-size="10" font-weight="bold">Coherence rules</text>
  <text x="480" y="151" text-anchor="middle" font-size="9">Orphan rule: impl trait for</text>
  <text x="480" y="162" text-anchor="middle" font-size="9">type only if one is local</text>
  <rect x="150" y="178" width="300" height="18" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="191" text-anchor="middle" font-size="9">Use where clauses for readability with complex bounds</text>
</svg>

---
## Common Pitfalls
1. Overly generic code
1. Unnecessary trait bounds
1. Object safety violations
1. Trait coherence issues
1. Performance implications
---
## Summary
- Generic types
- Traits and bounds
- Associated types
- Trait objects
- Best practices
