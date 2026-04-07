# Generic Types and Traits
## Chapter 6: Abstraction and Code Reuse

---
## What are Generics

![what_are_generics](svg/courses/languages/rust/rust-programming/07_generics_traits/what_are_generics.svg)

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

![what_are_traits](svg/courses/languages/rust/rust-programming/07_generics_traits/what_are_traits.svg)

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

![common_traits](svg/courses/languages/rust/rust-programming/07_generics_traits/common_traits.svg)

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

![best_practices](svg/courses/languages/rust/rust-programming/07_generics_traits/best_practices.svg)

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
