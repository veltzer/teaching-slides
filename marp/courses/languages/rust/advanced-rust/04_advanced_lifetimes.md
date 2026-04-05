# Advanced Lifetimes

Elision, Bounds, Variance, and Self-Referential Structs

---

## Overview

- Lifetime elision rules
- Named lifetimes in structs and impl blocks
- Lifetime bounds on generics
- Higher-ranked trait bounds (`for<'a>`)
- Lifetime variance (covariance, contravariance, invariance)
- Self-referential structs and `Pin`
- Common lifetime puzzles and solutions

---

## Part 1: Lifetime Elision Rules

When you can omit lifetime annotations

---

## The Three Elision Rules

```rust
// Rule 1: Each reference parameter gets its own lifetime
fn foo(x: &str, y: &str) -> ...
// becomes: fn foo<'a, 'b>(x: &'a str, y: &'b str) -> ...

// Rule 2: If there is exactly one input lifetime, it is
// assigned to all output lifetimes
fn foo(x: &str) -> &str
// becomes: fn foo<'a>(x: &'a str) -> &'a str

// Rule 3: If one of the parameters is &self or &mut self,
// its lifetime is assigned to all output lifetimes
impl MyStruct {
    fn foo(&self, x: &str) -> &str
    // becomes: fn foo<'a, 'b>(&'a self, x: &'b str) -> &'a str
}
```

---

## When Elision Fails

```rust
// Two input references, no &self - compiler cannot determine
// which lifetime to assign to the output

// This fails:
// fn longest(x: &str, y: &str) -> &str { ... }

// Must be explicit:
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Different lifetimes when only one is returned:
fn first<'a, 'b>(x: &'a str, _y: &'b str) -> &'a str {
    x
}
```

---

## Elision in Closures vs Functions

```rust
// Functions get elision rules:
fn first_word(s: &str) -> &str {
    s.split_whitespace().next().unwrap_or("")
}

// Closures do NOT get elision in all cases:
// let first_word = |s: &str| -> &str { ... }; // May fail

// Workaround: use a helper function or explicit annotation
fn apply_to_str<F>(s: &str, f: F) -> String
where
    F: Fn(&str) -> &str,
{
    f(s).to_string()
}
```

---

## Part 2: Lifetimes in Structs

Structs that borrow data

---

## Basic Struct Lifetimes

```rust
// A struct that borrows a string slice
struct Excerpt<'a> {
    text: &'a str,
    line_number: usize,
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence;
    {
        let sentences: Vec<&str> = novel.split('.').collect();
        first_sentence = Excerpt {
            text: sentences[0],
            line_number: 1,
        };
    }
    // first_sentence is still valid because novel is still alive
    println!("Excerpt: {} (line {})", first_sentence.text, first_sentence.line_number);
}
```

---

## Multiple Lifetimes in Structs

```rust
struct Parser<'input, 'config> {
    input: &'input str,
    config: &'config ParserConfig,
    position: usize,
}

struct ParserConfig {
    delimiter: char,
    skip_whitespace: bool,
}

impl<'input, 'config> Parser<'input, 'config> {
    fn new(input: &'input str, config: &'config ParserConfig) -> Self {
        Parser { input, config, position: 0 }
    }

    fn next_token(&mut self) -> Option<&'input str> {
        if self.position >= self.input.len() {
            return None;
        }
        let rest = &self.input[self.position..];
        if let Some(pos) = rest.find(self.config.delimiter) {
            self.position += pos + 1;
            Some(&rest[..pos])
        } else {
            self.position = self.input.len();
            Some(rest)
        }
    }
}
```

---

## Lifetimes in Impl Blocks

```rust
struct TextBuffer<'a> {
    content: &'a str,
    cursor: usize,
}

// Lifetime must be declared on impl
impl<'a> TextBuffer<'a> {
    fn new(content: &'a str) -> Self {
        TextBuffer { content, cursor: 0 }
    }

    // Returns a reference tied to the buffer's lifetime
    fn current_line(&self) -> &'a str {
        let rest = &self.content[self.cursor..];
        match rest.find('\n') {
            Some(pos) => &rest[..pos],
            None => rest,
        }
    }

    // Returns a reference tied to &self lifetime (elision rule 3)
    fn peek(&self) -> Option<char> {
        self.content[self.cursor..].chars().next()
    }
}
```

---

## The 'static Lifetime

```rust
// 'static means the reference lives for the entire program

// String literals are always 'static
let s: &'static str = "I live forever";

// Owned types satisfy 'static bounds (they have no borrows)
fn spawn_thread<T: Send + 'static>(val: T) {
    std::thread::spawn(move || {
        println!("Using value in thread");
        drop(val);
    });
}

// 'static does NOT mean "lives forever" - it means
// "CAN live as long as needed" or "contains no non-static borrows"
fn main() {
    let owned = String::from("hello");
    spawn_thread(owned); // String is 'static because it owns its data
}
```

---

## Part 3: Lifetime Bounds on Generics

Constraining generic type lifetimes

---

## Lifetime Bounds

```rust
// T: 'a means "T can live at least as long as 'a"
// This means all references inside T must outlive 'a

struct Ref<'a, T: 'a> {
    value: &'a T,
}

// Since Rust 2021, T: 'a is inferred from &'a T
// So this is equivalent:
struct Ref2<'a, T> {
    value: &'a T, // T: 'a is implied
}

// T: 'static means T contains no non-static references
fn store_globally<T: 'static>(val: T) {
    // Safe to store in a global or leak
    let leaked: &'static T = Box::leak(Box::new(val));
    println!("Stored at: {:p}", leaked);
}
```

---

## Combining Lifetime and Trait Bounds

```rust
use std::fmt::Display;

// T must implement Display AND outlive 'a
fn print_ref<'a, T: Display + 'a>(val: &'a T) {
    println!("Value: {}", val);
}

// Multiple bounds with where clause
fn complex_function<'a, 'b, T, U>(t: &'a T, u: &'b U) -> String
where
    T: Display + Clone + 'a,
    U: Display + 'b,
    'b: 'a, // 'b outlives 'a
{
    format!("{} and {}", t, u)
}
```

---

## Lifetime Bounds in Trait Definitions

```rust
trait Cache {
    type Item;

    fn get<'a>(&'a self, key: &str) -> Option<&'a Self::Item>;
    fn insert(&mut self, key: String, value: Self::Item);
}

// A cache that returns borrowed data
struct StringCache {
    data: std::collections::HashMap<String, String>,
}

impl Cache for StringCache {
    type Item = String;

    fn get<'a>(&'a self, key: &str) -> Option<&'a String> {
        self.data.get(key)
    }

    fn insert(&mut self, key: String, value: String) {
        self.data.insert(key, value);
    }
}
```

---

## Part 4: Higher-Ranked Trait Bounds

`for<'a>` - universally quantified lifetimes

---

## The Problem HRTBs Solve

```rust
// We want a function that can process any reference with any lifetime
// This does NOT work:
// fn apply<'a>(f: fn(&'a str) -> &'a str, s: &'a str) -> &'a str
// Because 'a is fixed when apply is called

// We need: "f works for ALL possible lifetimes"
fn apply(f: for<'a> fn(&'a str) -> &'a str, s: &str) -> &str {
    f(s)
}

fn to_upper(s: &str) -> &str {
    // In real code this would allocate, but for demonstration:
    s
}

fn main() {
    let result = apply(to_upper, "hello");
    println!("{}", result);
}
```

---

## HRTBs with Closures

```rust
// The Fn traits use HRTBs implicitly:
// Fn(&str) -> &str is actually for<'a> Fn(&'a str) -> &'a str

fn apply_to_words<F>(text: &str, f: F) -> Vec<String>
where
    F: for<'a> Fn(&'a str) -> &'a str,  // Explicit HRTB
    // F: Fn(&str) -> &str,              // Same thing (sugar)
{
    text.split_whitespace()
        .map(|word| f(word).to_string())
        .collect()
}

fn main() {
    let words = apply_to_words("hello world rust", |s| s);
    println!("{:?}", words);
}
```

---

## HRTBs in Practice

```rust
use std::fmt::Debug;

// A trait for things that can be compared with any lifetime
trait Matcher {
    fn matches(&self, input: &str) -> bool;
}

struct StartsWith(String);

impl Matcher for StartsWith {
    fn matches(&self, input: &str) -> bool {
        input.starts_with(&self.0)
    }
}

// A function that accepts any Matcher
fn find_matching<'a, M: Matcher>(items: &'a [String], matcher: &M) -> Vec<&'a str> {
    items
        .iter()
        .filter(|item| matcher.matches(item))
        .map(|s| s.as_str())
        .collect()
}
```

---

## Part 5: Lifetime Variance

How lifetimes interact with subtyping

---

## Covariance

```rust
// &'a T is COVARIANT in 'a
// A longer lifetime can be used where a shorter one is expected

fn example<'long, 'short>(long_ref: &'long str, short_ref: &'short str)
where
    'long: 'short, // 'long outlives 'short
{
    // Can use &'long str where &'short str is expected
    let _: &'short str = long_ref; // OK: covariance

    // Cannot use &'short str where &'long str is expected
    // let _: &'long str = short_ref; // ERROR
}
```

---

## Variance Table

```text
  ┌─────────────────────┬─────────────────┬──────────────┐
  │ Type                │ Variance in 'a  │ Variance in T│
  ├─────────────────────┼─────────────────┼──────────────┤
  │ &'a T               │ covariant       │ covariant    │
  │ &'a mut T           │ covariant       │ invariant    │
  │ Box<T>              │ -               │ covariant    │
  │ Vec<T>              │ -               │ covariant    │
  │ Cell<T>             │ -               │ invariant    │
  │ UnsafeCell<T>       │ -               │ invariant    │
  │ fn(T) -> U          │ -               │ contra / co  │
  │ *const T            │ -               │ covariant    │
  │ *mut T              │ -               │ invariant    │
  └─────────────────────┴─────────────────┴──────────────┘
```

---

## Why &mut T is Invariant in T

```rust
fn evil_swap<'a, 'b>(
    r: &mut &'a str,
    s: &'b str,
) where 'b: 'a {
    // If &mut T were covariant in T, we could do:
    // *r = s;
    // But this would be unsound if 'b is actually shorter!
}

// Example of why invariance is needed:
fn main() {
    let mut long_lived = "I live long";
    let r = &mut long_lived;

    {
        let short_lived = String::from("I die soon");
        // If this were allowed, long_lived would point to freed memory
        // evil_swap(r, &short_lived); // Not allowed due to invariance
    }

    println!("{}", long_lived); // Would be use-after-free!
}
```

---

## Variance in Practice

```rust
// PhantomData controls variance for unused type parameters

use std::marker::PhantomData;

// Covariant in T (like &T)
struct CovariantWrapper<T> {
    _marker: PhantomData<T>,
}

// Invariant in T (like &mut T or Cell<T>)
struct InvariantWrapper<T> {
    _marker: PhantomData<fn(T) -> T>, // fn contravariant + covariant = invariant
}

// Contravariant in T (like fn(T))
struct ContravariantWrapper<T> {
    _marker: PhantomData<fn(T)>,
}
```

---

## Part 6: Self-Referential Structs

The hardest lifetime problem in Rust

---

## The Problem

```rust
// This does NOT compile:
struct SelfRef {
    data: String,
    slice: &str, // What lifetime? It borrows from data!
}

// You cannot express "slice borrows from data" in Rust's type system
// because the struct might be moved, invalidating the pointer.

// Why moving is dangerous:
//   Before move:         After move:
//   ┌──────────┐         ┌──────────┐    ┌──────────┐
//   │ data ────────┐     │ data ────────┐│ (freed)  │
//   │ slice ───┐   │     │ slice ───┐   ││          │
//   └──────────┘   │     └──────────┘   │└──────────┘
//              │   │                │   │
//              └───┘                └───X  DANGLING!
```

---

## Solution 1: Indices Instead of References

```rust
struct Document {
    content: String,
    // Store byte offsets instead of references
    highlights: Vec<(usize, usize)>, // (start, end) pairs
}

impl Document {
    fn new(content: String) -> Self {
        Document { content, highlights: Vec::new() }
    }

    fn add_highlight(&mut self, start: usize, end: usize) {
        assert!(end <= self.content.len());
        self.highlights.push((start, end));
    }

    fn get_highlight(&self, index: usize) -> &str {
        let (start, end) = self.highlights[index];
        &self.content[start..end]
    }
}
```

---

## Solution 2: Pin + Unsafe

```rust
use std::pin::Pin;
use std::marker::PhantomPinned;

struct SelfRef {
    data: String,
    ptr: *const String, // Raw pointer to data
    _pin: PhantomPinned, // Opts out of Unpin
}

impl SelfRef {
    fn new(data: String) -> Pin<Box<Self>> {
        let s = SelfRef {
            data,
            ptr: std::ptr::null(),
            _pin: PhantomPinned,
        };
        let mut boxed = Box::pin(s);
        let self_ptr: *const String = &boxed.data;
        unsafe {
            let mut_ref = Pin::as_mut(&mut boxed);
            Pin::get_unchecked_mut(mut_ref).ptr = self_ptr;
        }
        boxed
    }

    fn data(&self) -> &str {
        unsafe { &*self.ptr }
    }
}
```

---

## Solution 3: The ouroboros Crate

```rust
// The ouroboros crate automates self-referential structs

use ouroboros::self_referencing;

#[self_referencing]
struct ParsedDocument {
    raw: String,
    #[borrows(raw)]
    #[covariant]
    parsed: Vec<&'this str>,
}

fn main() {
    let doc = ParsedDocumentBuilder {
        raw: "hello world foo bar".to_string(),
        parsed_builder: |raw: &String| {
            raw.split_whitespace().collect()
        },
    }.build();

    doc.with_parsed(|words| {
        println!("Words: {:?}", words);
    });
}
```

---

## Part 7: Common Lifetime Puzzles

Tricky scenarios and their solutions

---

## Puzzle 1: Returning References from Collections

```rust
struct Registry {
    items: Vec<String>,
}

impl Registry {
    fn add(&mut self, item: String) -> usize {
        self.items.push(item);
        self.items.len() - 1
    }

    // This works: returning &str tied to &self
    fn get(&self, index: usize) -> Option<&str> {
        self.items.get(index).map(|s| s.as_str())
    }

    // This does NOT work: cannot return ref while holding &mut self
    // fn add_and_get(&mut self, item: String) -> &str {
    //     self.items.push(item);
    //     self.items.last().unwrap()
    // }

    // Solution: return an index, get reference later
    fn add_and_get_index(&mut self, item: String) -> usize {
        self.items.push(item);
        self.items.len() - 1
    }
}
```

---

## Puzzle 2: Multiple Borrows of Different Fields

```rust
struct World {
    entities: Vec<Entity>,
    physics: PhysicsEngine,
    renderer: Renderer,
}

struct Entity { x: f64, y: f64, name: String }
struct PhysicsEngine;
struct Renderer;

impl PhysicsEngine {
    fn update(&mut self, entities: &mut [Entity]) {
        for e in entities { e.x += 1.0; }
    }
}

impl Renderer {
    fn draw(&self, entities: &[Entity]) {
        for e in entities { println!("Drawing {} at ({}, {})", e.name, e.x, e.y); }
    }
}

impl World {
    fn tick(&mut self) {
        // Rust allows borrowing different fields simultaneously
        self.physics.update(&mut self.entities); // &mut self.physics + &mut self.entities
        self.renderer.draw(&self.entities);       // &self.renderer + &self.entities
    }
}
```

---

## Puzzle 3: Lifetime of Temporaries

```rust
fn main() {
    // Temporaries live until the end of the statement
    let r;
    {
        let s = String::from("hello");
        r = &s; // ERROR: s does not live long enough
    }
    // println!("{}", r);

    // But this works! The temporary lives long enough:
    let r = &String::from("hello");
    // The temporary String lives until end of the enclosing block

    // Common gotcha with method chaining:
    // let s = String::from("hello").as_str(); // ERROR
    // The String is a temporary that dies at the semicolon

    // Fix: bind the intermediate value
    let owned = String::from("hello");
    let s = owned.as_str();
    println!("{}", s);
}
```

---

## Puzzle 4: Lifetimes in Callbacks

```rust
struct EventEmitter {
    // Cannot store closures that borrow from the environment
    // unless we add lifetime parameters
    handlers: Vec<Box<dyn Fn(&str)>>,
}

impl EventEmitter {
    fn new() -> Self {
        EventEmitter { handlers: Vec::new() }
    }

    fn on<F: Fn(&str) + 'static>(&mut self, handler: F) {
        // 'static bound means the closure cannot borrow local variables
        self.handlers.push(Box::new(handler));
    }

    fn emit(&self, event: &str) {
        for handler in &self.handlers {
            handler(event);
        }
    }
}

fn main() {
    let mut emitter = EventEmitter::new();
    let prefix = String::from("EVENT");
    // Must move owned data into the closure
    emitter.on(move |event| println!("{}: {}", prefix, event));
    emitter.emit("click");
}
```

---

## Puzzle 5: Lifetime Bounds and Trait Objects

```rust
// trait objects have an implicit lifetime bound

// &'a dyn Trait means &'a (dyn Trait + 'a) by default
// Box<dyn Trait> means Box<dyn Trait + 'static> by default

trait Processor {
    fn process(&self, data: &str) -> String;
}

// This requires 'static data in the trait object
fn store_processor(p: Box<dyn Processor>) {
    // p must be 'static
}

// This allows non-'static data
fn use_processor<'a>(p: &'a dyn Processor, data: &str) -> String {
    p.process(data)
}

// Explicit lifetime bound on trait object
fn store_processor_with_lifetime<'a>(p: Box<dyn Processor + 'a>) {
    // p can contain references with lifetime 'a
}
```

---

## Puzzle 6: Structs Returning Iterators

```rust
struct WordCounter {
    text: String,
}

impl WordCounter {
    fn new(text: &str) -> Self {
        WordCounter { text: text.to_string() }
    }

    // Return an iterator that borrows from self
    fn words(&self) -> impl Iterator<Item = &str> {
        self.text.split_whitespace()
    }

    // Count unique words
    fn unique_count(&self) -> usize {
        let mut seen = std::collections::HashSet::new();
        for word in self.words() {
            seen.insert(word);
        }
        seen.len()
    }

    // Return words as owned Strings (no lifetime issues)
    fn words_owned(&self) -> Vec<String> {
        self.text.split_whitespace().map(String::from).collect()
    }
}
```

---

## Reborrowing

```rust
// &mut references cannot be copied, but they can be "reborrowed"

fn takes_mut_ref(s: &mut String) {
    s.push_str(" world");
}

fn main() {
    let mut s = String::from("hello");
    let r = &mut s;

    // This looks like it should fail (moving r), but it works!
    takes_mut_ref(r); // Implicit reborrow: &mut *r
    takes_mut_ref(r); // r is still valid!

    // Explicit reborrow:
    let r2: &mut String = &mut *r;
    takes_mut_ref(r2);

    // r is usable again after r2 is done
    r.push_str("!");
    println!("{}", r);
}
```

---

## Lifetime Subtyping

```rust
// 'long: 'short means 'long outlives 'short
// &'long T can be used where &'short T is expected

fn choose_first<'long, 'short>(
    first: &'long str,
    _second: &'short str,
) -> &'short str
where
    'long: 'short,
{
    // We can return first because 'long outlives 'short
    // so &'long str can be coerced to &'short str
    first
}

fn main() {
    let long_lived = String::from("long");
    let result;
    {
        let short_lived = String::from("short");
        result = choose_first(&long_lived, &short_lived);
        println!("{}", result);
    }
    // result is no longer valid here (tied to 'short)
}
```

---

## Summary

```text
  ┌──────────────────────────────────────────────────────────┐
  │              Advanced Lifetimes Cheatsheet                │
  ├──────────────────────────────────────────────────────────┤
  │ Elision rule 1 : each param gets own lifetime            │
  │ Elision rule 2 : single input -> all outputs             │
  │ Elision rule 3 : &self lifetime -> all outputs           │
  │ 'static        : no non-static borrows (or string lits) │
  │ T: 'a          : all refs in T outlive 'a                │
  │ for<'a>        : works for ALL lifetimes                 │
  │ Covariant      : longer life usable as shorter           │
  │ Invariant      : exact lifetime match required           │
  │ Self-ref       : use indices, Pin, or ouroboros           │
  │ Reborrowing    : &mut *r creates shorter-lived &mut      │
  └──────────────────────────────────────────────────────────┘
```

---

## Exercises

1. Write a struct `CachedParser<'input>` that borrows input and caches parsed tokens as slices.
2. Implement a function with HRTBs that accepts a closure operating on borrowed data.
3. Create a `SplitIterator` that borrows a string and yields splits without allocating.
4. Build a struct that holds both owned and borrowed data with proper lifetime annotations.
5. Fix a series of "lifetime does not live long enough" compiler errors (instructor-provided code).
