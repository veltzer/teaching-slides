# Collections
## Chapter 5: Working with Data Structures

---

## Common Collections

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Rust Standard Collections</text>
  <rect x="20" y="30" width="170" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="50" text-anchor="middle" font-size="11" font-weight="bold">Vec&lt;T&gt;</text>
  <text x="105" y="65" text-anchor="middle" font-size="9">Growable array</text>
  <text x="105" y="78" text-anchor="middle" font-size="9">Contiguous heap memory</text>
  <text x="105" y="91" text-anchor="middle" font-size="9">O(1) push/pop, O(1) index</text>
  <rect x="215" y="30" width="170" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="50" text-anchor="middle" font-size="11" font-weight="bold">String</text>
  <text x="300" y="65" text-anchor="middle" font-size="9">UTF-8 encoded text</text>
  <text x="300" y="78" text-anchor="middle" font-size="9">Wrapper around Vec&lt;u8&gt;</text>
  <text x="300" y="91" text-anchor="middle" font-size="9">Owned, growable</text>
  <rect x="410" y="30" width="170" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="50" text-anchor="middle" font-size="11" font-weight="bold">HashMap&lt;K,V&gt;</text>
  <text x="495" y="65" text-anchor="middle" font-size="9">Key-value store</text>
  <text x="495" y="78" text-anchor="middle" font-size="9">Hash-based buckets</text>
  <text x="495" y="91" text-anchor="middle" font-size="9">O(1) avg lookup</text>
  <rect x="80" y="120" width="200" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="180" y="139" text-anchor="middle" font-size="10">Also: VecDeque, LinkedList, BTreeMap</text>
  <rect x="320" y="120" width="200" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="420" y="139" text-anchor="middle" font-size="10">Also: HashSet, BTreeSet, BinaryHeap</text>
  <rect x="100" y="165" width="400" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="182" text-anchor="middle" font-size="10">All collections own their data and free it on drop (RAII)</text>
</svg>

---

## Vector Basics

```rust
// Creating new vectors
let v: Vec<i32> = Vec::new();
let v = vec![1, 2, 3];

// Adding elements
let mut v = Vec::new();
v.push(5);
v.push(6);
```

---

## Accessing Vector Elements

```rust
let v = vec![1, 2, 3, 4, 5];

// Using index
let third: &i32 = &v[2];

// Using get
match v.get(2) {
    Some(third) => println!("Third element is {}", third),
    None => println!("No third element"),
}
```

---

## Vector Safety

```rust
let v = vec![1, 2, 3, 4, 5];

// Will panic
// let does_not_exist = &v[100];

// Safe access
let does_not_exist = v.get(100);
match does_not_exist {
    Some(value) => println!("Value: {}", value),
    None => println!("Index out of bounds"),
}
```

---

## Iterating Over Vectors

```rust
let v = vec![100, 32, 57];

// Immutable references
for i in &v {
    println!("{}", i);
}

// Mutable references
let mut v = vec![100, 32, 57];
for i in &mut v {
    *i += 50;
}
```

---

## Vector with Different Types

```rust
enum SpreadsheetCell {
    Int(i32),
    Float(f64),
    Text(String),
}

let row = vec![
    SpreadsheetCell::Int(3),
    SpreadsheetCell::Text(String::from("blue")),
    SpreadsheetCell::Float(10.12),
];
```

---

## Vector Methods

```rust
fn main() {
    let mut v = vec![1, 2, 3];

    v.push(4);        // Add element
    v.pop();          // Remove last
    v.len();          // Get length
    v.capacity();     // Get capacity
    v.clear();        // Remove all
    v.extend([1,2,3].iter()); // Add multiple
}
```

---

## String Creation

```rust
// Empty string
let mut s = String::new();

// From literal
let s = "initial contents".to_string();

// Using from
let s = String::from("initial contents");
```

---

## String Updates

```rust
let mut s = String::from("foo");

// Push string
s.push_str("bar");

// Push single char
s.push('!');

// Concatenation
let s1 = String::from("Hello, ");
let s2 = String::from("world!");
let s3 = s1 + &s2; // s1 has been moved
```

---

## String Internals

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arr_str" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">String Internal Layout (wraps Vec&lt;u8&gt;)</text>
  <text x="110" y="35" text-anchor="middle" font-size="11" font-weight="bold">Stack: String struct</text>
  <rect x="20" y="42" width="180" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="110" y="59" text-anchor="middle" font-size="10">ptr: 0x7fa3...</text>
  <rect x="20" y="67" width="180" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="110" y="84" text-anchor="middle" font-size="10">len: 5 (bytes used)</text>
  <rect x="20" y="92" width="180" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="110" y="109" text-anchor="middle" font-size="10">cap: 8 (bytes allocated)</text>
  <text x="420" y="35" text-anchor="middle" font-size="11" font-weight="bold">Heap: UTF-8 bytes</text>
  <rect x="290" y="45" width="35" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="307" y="64" text-anchor="middle" font-size="11">h</text>
  <rect x="325" y="45" width="35" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="342" y="64" text-anchor="middle" font-size="11">e</text>
  <rect x="360" y="45" width="35" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="377" y="64" text-anchor="middle" font-size="11">l</text>
  <rect x="395" y="45" width="35" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="412" y="64" text-anchor="middle" font-size="11">l</text>
  <rect x="430" y="45" width="35" height="30" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="447" y="64" text-anchor="middle" font-size="11">o</text>
  <rect x="465" y="45" width="35" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="482" y="64" text-anchor="middle" font-size="9">--</text>
  <rect x="500" y="45" width="35" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="517" y="64" text-anchor="middle" font-size="9">--</text>
  <rect x="535" y="45" width="35" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="552" y="64" text-anchor="middle" font-size="9">--</text>
  <text x="400" y="90" text-anchor="middle" font-size="9">|-- len: 5 used --|-- cap: 3 spare --|</text>
  <line x1="200" y1="55" x2="290" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arr_str)"/>
  <rect x="30" y="125" width="250" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="155" y="144" text-anchor="middle" font-size="10">UTF-8 encoded: multi-byte chars possible</text>
  <rect x="310" y="125" width="260" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="440" y="144" text-anchor="middle" font-size="10">No indexing by char! Use .chars() iterator</text>
  <rect x="100" y="170" width="400" height="22" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="185" text-anchor="middle" font-size="10">String = Vec&lt;u8&gt; with UTF-8 guarantee; &amp;str = &amp;[u8] slice</text>
</svg>

---

## String Slicing

```rust
let hello = "hello";

let s = &hello[0..4]; // Gets "he"

// Be careful with slicing - must be valid UTF-8 boundaries
```

---

## String Iteration

```rust
let s = String::from("hello");

// Chars
for c in s.chars() {
    println!("{}", c);
}

// Bytes
for b in s.bytes() {
    println!("{}", b);
}
```

---

## HashMap Basics

```rust
use std::collections::HashMap;

let mut scores = HashMap::new();

scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Yellow"), 50);
```

---

## Creating HashMap

```rust
use std::collections::HashMap;

// From tuples
let teams = vec![String::from("Blue"), String::from("Yellow")];
let initial_scores = vec![10, 50];

let scores: HashMap<_, _> = teams.iter()
    .zip(initial_scores.iter())
    .collect();
```

---

## Accessing HashMap Values

```rust
let mut scores = HashMap::new();
scores.insert(String::from("Blue"), 10);

// Using get
match scores.get("Blue") {
    Some(score) => println!("Blue team score: {}", score),
    None => println!("Blue team doesn't exist"),
}

// Iteration
for (key, value) in &scores {
    println!("{}: {}", key, value);
}
```

---

## Updating HashMap

```rust
let mut scores = HashMap::new();

// Overwriting
scores.insert(String::from("Blue"), 10);
scores.insert(String::from("Blue"), 25);

// Insert if key has no value
scores.entry(String::from("Yellow")).or_insert(50);
```

---

## Update Based on Old Value

```rust
use std::collections::HashMap;

let text = "hello world wonderful world";

let mut map = HashMap::new();

for word in text.split_whitespace() {
    let count = map.entry(word).or_insert(0);
    *count += 1;
}
```

---

## Hash Functions

```rust
use std::collections::HashMap;
use std::hash::BuildHasherDefault;
use std::collections::hash_map::DefaultHasher;

// Using default hasher
let mut map = HashMap::new();

// Using custom hasher
let mut map: HashMap<_, _, BuildHasherDefault<DefaultHasher>> =
    HashMap::default();
```

---

## Collection Traits

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Key Collection Traits</text>
  <rect x="20" y="30" width="170" height="65" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="48" text-anchor="middle" font-size="10" font-weight="bold">Iterator</text>
  <text x="105" y="63" text-anchor="middle" font-size="9">fn next(&amp;mut self)</text>
  <text x="105" y="76" text-anchor="middle" font-size="9">  -> Option&lt;Item&gt;</text>
  <text x="105" y="89" text-anchor="middle" font-size="9">.map() .filter() .collect()</text>
  <rect x="215" y="30" width="170" height="65" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="48" text-anchor="middle" font-size="10" font-weight="bold">FromIterator</text>
  <text x="300" y="63" text-anchor="middle" font-size="9">Enables .collect()</text>
  <text x="300" y="76" text-anchor="middle" font-size="9">Vec, String, HashMap</text>
  <text x="300" y="89" text-anchor="middle" font-size="9">all implement this</text>
  <rect x="410" y="30" width="170" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="48" text-anchor="middle" font-size="10" font-weight="bold">IntoIterator</text>
  <text x="495" y="63" text-anchor="middle" font-size="9">Enables for..in loops</text>
  <text x="495" y="76" text-anchor="middle" font-size="9">for x in collection {}</text>
  <text x="495" y="89" text-anchor="middle" font-size="9">consumes / borrows</text>
  <rect x="20" y="110" width="270" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="155" y="125" text-anchor="middle" font-size="10" font-weight="bold">Index / IndexMut</text>
  <text x="155" y="139" text-anchor="middle" font-size="9">v[i] syntax for Vec, HashMap[key]</text>
  <rect x="310" y="110" width="270" height="35" fill="#ffebee" stroke="#333" stroke-width="1" rx="5"/>
  <text x="445" y="125" text-anchor="middle" font-size="10" font-weight="bold">Extend</text>
  <text x="445" y="139" text-anchor="middle" font-size="9">Append items from iterator to collection</text>
  <rect x="100" y="160" width="400" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="300" y="177" text-anchor="middle" font-size="10">Iterators are lazy: zero-cost abstractions optimized by LLVM</text>
</svg>

---

## Vec vs Array vs Slice

<div class="columns">
<div>

## Vec<T>
- Dynamic size
- Heap allocated
- Growable

</div>
<div>

## Array/Slice
- Fixed size
- Stack possible
- Immutable size

</div>
</div>

---

## Common Methods

```rust
let mut vec = vec![1, 2, 3];
vec.push(4);              // Add to end
vec.pop();               // Remove from end
vec.remove(1);           // Remove at index
vec.insert(1, 5);        // Insert at index
vec.clear();             // Remove all
vec.extend([6,7,8]);     // Add multiple
```

---
## Performance Considerations

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Collection Performance Comparison</text>
  <rect x="20" y="25" width="80" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="60" y="42" text-anchor="middle" font-size="10" font-weight="bold">Operation</text>
  <rect x="110" y="25" width="110" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="165" y="42" text-anchor="middle" font-size="10" font-weight="bold">Vec&lt;T&gt;</text>
  <rect x="230" y="25" width="110" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="285" y="42" text-anchor="middle" font-size="10" font-weight="bold">HashMap&lt;K,V&gt;</text>
  <rect x="350" y="25" width="110" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="405" y="42" text-anchor="middle" font-size="10" font-weight="bold">BTreeMap</text>
  <rect x="470" y="25" width="110" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="525" y="42" text-anchor="middle" font-size="10" font-weight="bold">VecDeque</text>
  <rect x="20" y="55" width="80" height="22" fill="#fff3e0" stroke="#333" stroke-width="1"/>
  <text x="60" y="70" text-anchor="middle" font-size="9">Push</text>
  <rect x="110" y="55" width="110" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="165" y="70" text-anchor="middle" font-size="9">O(1) amortized</text>
  <rect x="230" y="55" width="110" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="285" y="70" text-anchor="middle" font-size="9">O(1) avg</text>
  <rect x="350" y="55" width="110" height="22" fill="#fff3e0" stroke="#333" stroke-width="1"/>
  <text x="405" y="70" text-anchor="middle" font-size="9">O(log n)</text>
  <rect x="470" y="55" width="110" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="525" y="70" text-anchor="middle" font-size="9">O(1) amortized</text>
  <rect x="20" y="80" width="80" height="22" fill="#fff3e0" stroke="#333" stroke-width="1"/>
  <text x="60" y="95" text-anchor="middle" font-size="9">Lookup</text>
  <rect x="110" y="80" width="110" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="165" y="95" text-anchor="middle" font-size="9">O(1) by index</text>
  <rect x="230" y="80" width="110" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="285" y="95" text-anchor="middle" font-size="9">O(1) avg</text>
  <rect x="350" y="80" width="110" height="22" fill="#fff3e0" stroke="#333" stroke-width="1"/>
  <text x="405" y="95" text-anchor="middle" font-size="9">O(log n)</text>
  <rect x="470" y="80" width="110" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="525" y="95" text-anchor="middle" font-size="9">O(1) by index</text>
  <rect x="20" y="105" width="80" height="22" fill="#fff3e0" stroke="#333" stroke-width="1"/>
  <text x="60" y="120" text-anchor="middle" font-size="9">Search</text>
  <rect x="110" y="105" width="110" height="22" fill="#ffebee" stroke="#333" stroke-width="1"/>
  <text x="165" y="120" text-anchor="middle" font-size="9">O(n) linear</text>
  <rect x="230" y="105" width="110" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="285" y="120" text-anchor="middle" font-size="9">O(1) by key</text>
  <rect x="350" y="105" width="110" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="405" y="120" text-anchor="middle" font-size="9">O(log n) by key</text>
  <rect x="470" y="105" width="110" height="22" fill="#ffebee" stroke="#333" stroke-width="1"/>
  <text x="525" y="120" text-anchor="middle" font-size="9">O(n) linear</text>
  <rect x="50" y="140" width="240" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="170" y="157" text-anchor="middle" font-size="9">Pre-allocate: Vec::with_capacity(n)</text>
  <rect x="310" y="140" width="240" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="430" y="157" text-anchor="middle" font-size="9">HashMap::with_capacity(n) avoids rehash</text>
  <rect x="100" y="175" width="400" height="22" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="190" text-anchor="middle" font-size="10">Choose collection by access pattern, not habit</text>
</svg>

---

## Collection Examples

```rust
// Frequency counter
fn word_frequency(text: &str) -> HashMap<String, u32> {
    let mut map = HashMap::new();

    for word in text.split_whitespace() {
        *map.entry(word.to_string()).or_insert(0) += 1;
    }

    map
}
```

---

## Error Handling

```rust
fn main() {
    let v = vec![1, 2, 3];

    // Safe index access
    match v.get(5) {
        Some(value) => println!("Value: {}", value),
        None => println!("Index out of bounds"),
    }

    // Safe key access
    let mut map = HashMap::new();
    map.insert(String::from("key"), 42);

    if let Some(value) = map.get("key") {
        println!("Value: {}", value);
    }
}
```

---

## Memory Management

```rust
fn main() {
    // Pre-allocation
    let mut v = Vec::with_capacity(10);

    // String pre-allocation
    let mut s = String::with_capacity(100);

    // HashMap with capacity
    let mut map = HashMap::with_capacity(50);
}
```

---

## Practice Exercise

Create a simple text analyzer that:
1. Counts word frequency
1. Tracks unique words
1. Finds longest/shortest words
1. Reports statistics

---

## Best Practices

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="5" width="200" height="35" fill="#673ab7" stroke="#333" stroke-width="2" rx="8"/>
  <text x="300" y="28" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Collection Best Practices</text>
  <line x1="250" y1="40" x2="120" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="58" stroke="#333" stroke-width="2"/>
  <line x1="250" y1="40" x2="120" y2="125" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="40" x2="480" y2="125" stroke="#333" stroke-width="2"/>
  <rect x="30" y="53" width="180" height="45" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="70" text-anchor="middle" font-size="10" font-weight="bold">Pre-allocate capacity</text>
  <text x="120" y="84" text-anchor="middle" font-size="9">with_capacity() avoids</text>
  <text x="120" y="95" text-anchor="middle" font-size="9">repeated re-allocation</text>
  <rect x="390" y="53" width="180" height="45" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="70" text-anchor="middle" font-size="10" font-weight="bold">Use .get() for safety</text>
  <text x="480" y="84" text-anchor="middle" font-size="9">Returns Option instead</text>
  <text x="480" y="95" text-anchor="middle" font-size="9">of panicking on bad index</text>
  <rect x="30" y="120" width="180" height="45" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="5"/>
  <text x="120" y="137" text-anchor="middle" font-size="10" font-weight="bold">Iterate, don't index</text>
  <text x="120" y="151" text-anchor="middle" font-size="9">for x in &amp;v is idiomatic</text>
  <text x="120" y="162" text-anchor="middle" font-size="9">and avoids bounds checks</text>
  <rect x="390" y="120" width="180" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="480" y="137" text-anchor="middle" font-size="10" font-weight="bold">entry() API for maps</text>
  <text x="480" y="151" text-anchor="middle" font-size="9">.entry(k).or_insert(v)</text>
  <text x="480" y="162" text-anchor="middle" font-size="9">avoids double lookup</text>
  <rect x="150" y="178" width="300" height="18" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="191" text-anchor="middle" font-size="9">Avoid .clone() on collection elements -- borrow or use references</text>
</svg>

---

## Common Pitfalls
1. Index out of bounds
1. Invalid string slicing
1. HashMap key type constraints
1. Unnecessary cloning
1. Inefficient capacity usage

---

## Summary
- Vectors for sequences
- Strings for text
- HashMaps for key-value data
- Memory management
- Performance considerations
