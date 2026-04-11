---
tags:
  - languages:rust
  - concepts:programming
level: advanced
category: language
audience:
  - audiences:developers

---
# Macros

Declarative Macros, Procedural Macros, and Metaprogramming

---

## Overview

- Declarative macros (`macro_rules!`)
- Pattern matching and repetitions
- Macro hygiene
- Procedural macros: derive, attribute, function-like
- `syn` and `quote` crates
- Real-world macro examples
- When to use macros vs generics

---

## Part 1: Declarative Macros

`macro_rules!` - pattern-based code generation

---

## Basic macro_rules!

```rust
macro_rules! say_hello {
    () => {
        println!("Hello, world!");
    };
}

macro_rules! greet {
    ($name:expr) => {
        println!("Hello, {}!", $name);
    };
}

fn main() {
    say_hello!();         // Hello, world!
    greet!("Rust");       // Hello, Rust!
    greet!(42);           // Hello, 42!
}
```

---

## Fragment Specifiers

```rust
// Available fragment specifiers:
macro_rules! demo_fragments {
    // $x:expr   - an expression: 1 + 2, foo(), "hello"
    // $x:ident  - an identifier: foo, Bar, my_var
    // $x:ty     - a type: i32, Vec<String>, &str
    // $x:path   - a path: std::io::Error, crate::module
    // $x:pat    - a pattern: Some(x), (a, b), _
    // $x:stmt   - a statement: let x = 5;
    // $x:block  - a block: { ... }
    // $x:item   - an item: fn, struct, impl, use
    // $x:meta   - a meta item: cfg(test), derive(Debug)
    // $x:tt     - a single token tree (most flexible)
    // $x:literal - a literal: "hello", 42, true
    // $x:lifetime - a lifetime: 'a, 'static
    ($x:expr) => { println!("{}", $x) };
}
```

---

## Multiple Patterns

```rust
macro_rules! calculate {
    // Pattern 1: addition
    (add $a:expr, $b:expr) => {
        $a + $b
    };
    // Pattern 2: multiplication
    (mul $a:expr, $b:expr) => {
        $a * $b
    };
    // Pattern 3: power (recursive)
    (pow $base:expr, $exp:expr) => {
        ($base as f64).powi($exp as i32)
    };
}

fn main() {
    println!("{}", calculate!(add 2, 3));   // 5
    println!("{}", calculate!(mul 4, 5));   // 20
    println!("{}", calculate!(pow 2, 10));  // 1024.0
}
```

---

## Repetitions

```rust
macro_rules! vec_of_strings {
    // $( ... ),* means zero or more, comma-separated
    ( $( $element:expr ),* ) => {
        {
            let mut v = Vec::new();
            $( v.push($element.to_string()); )*
            v
        }
    };
}

macro_rules! hashmap {
    // $( key => value ),* pattern
    ( $( $key:expr => $value:expr ),* $(,)? ) => {
        {
            let mut map = std::collections::HashMap::new();
            $( map.insert($key, $value); )*
            map
        }
    };
}

fn main() {
    let names = vec_of_strings!["Alice", "Bob", "Charlie"];
    println!("{:?}", names);

    let scores = hashmap! {
        "Alice" => 95,
        "Bob" => 87,
        "Charlie" => 92,
    };
    println!("{:?}", scores);
}
```

---

## Repetition Operators

```rust
macro_rules! repeat_demo {
    // * = zero or more
    (star: $( $x:expr ),*) => {
        vec![ $( $x ),* ]
    };

    // + = one or more
    (plus: $( $x:expr ),+) => {
        vec![ $( $x ),+ ]
    };

    // ? = zero or one
    (optional: $( $x:expr )?) => {
        $( Some($x) )?
    };
}

fn main() {
    let a: Vec<i32> = repeat_demo!(star: );           // empty vec
    let b = repeat_demo!(star: 1, 2, 3);               // [1, 2, 3]
    // let c = repeat_demo!(plus: );                    // ERROR: needs at least one
    let d = repeat_demo!(plus: 1, 2);                   // [1, 2]
}
```

---

## Nested Repetitions

```rust
macro_rules! matrix {
    // Nested repetition: rows of columns
    ( $( [ $( $val:expr ),* ] ),* ) => {
        vec![ $( vec![ $( $val ),* ] ),* ]
    };
}

macro_rules! define_structs {
    (
        $(
            struct $name:ident {
                $( $field:ident : $ty:ty ),* $(,)?
            }
        )*
    ) => {
        $(
            #[derive(Debug)]
            struct $name {
                $( $field: $ty, )*
            }
        )*
    };
}

fn main() {
    let m = matrix![[1, 2, 3], [4, 5, 6], [7, 8, 9]];
    println!("{:?}", m);
}

define_structs! {
    struct Point { x: f64, y: f64 }
    struct Color { r: u8, g: u8, b: u8 }
}
```

---

## Recursive Macros

```rust
macro_rules! count {
    () => { 0usize };
    ($head:tt $( $tail:tt )*) => { 1usize + count!( $( $tail )* ) };
}

macro_rules! tuple_from_vec {
    ($v:expr; $idx:expr) => { ($v[$idx],) };
    ($v:expr; $idx:expr, $( $rest:expr ),+) => {
        {
            let head = $v[$idx];
            let rest = tuple_from_vec!($v; $( $rest ),+);
            // Flatten would need more complex macro magic
            (head, rest)
        }
    };
}

fn main() {
    let n = count!(a b c d e);
    println!("Count: {}", n); // 5

    const SIZE: usize = count!(a b c);
    let arr: [i32; SIZE] = [1, 2, 3];
    println!("{:?}", arr);
}
```

---

## Part 2: Macro Hygiene

How Rust prevents macro name collisions

---

## Hygienic Macros

```rust
macro_rules! make_variable {
    ($val:expr) => {
        let x = $val; // This 'x' is in the macro's scope
    };
}

fn main() {
    let x = 10;
    make_variable!(20);
    println!("{}", x); // Prints 10, not 20!
    // The macro's 'x' is different from the outer 'x'
}

// To intentionally affect the caller's scope, use $ident
macro_rules! make_named_variable {
    ($name:ident, $val:expr) => {
        let $name = $val;
    };
}

fn main() {
    make_named_variable!(y, 42);
    println!("{}", y); // 42 - works because we passed the name
}
```

---

## Macro Scope and Visibility

```rust
// Macros are available after their definition (textual order)
// Use #[macro_export] to make them available to other crates

#[macro_export]
macro_rules! public_macro {
    () => { println!("I am public!"); };
}

// In another crate:
// use my_crate::public_macro;
// public_macro!();

// Within the same crate, use #[macro_use] on modules
// or define macros before they are used

mod helpers {
    macro_rules! helper_macro {
        () => { "helper" };
    }
    pub(crate) use helper_macro; // Re-export for use in other modules
}

fn main() {
    println!("{}", helpers::helper_macro!());
}
```

---

## Part 3: Practical Declarative Macros

Real-world macro_rules! patterns

---

## Builder Macro

```rust
macro_rules! builder {
    (
        $name:ident {
            $( $field:ident : $ty:ty ),* $(,)?
        }
    ) => {
        #[derive(Debug)]
        struct $name {
            $( $field: $ty, )*
        }

        paste::paste! {
            struct [<$name Builder>] {
                $( $field: Option<$ty>, )*
            }

            impl [<$name Builder>] {
                fn new() -> Self {
                    Self {
                        $( $field: None, )*
                    }
                }

                $(
                    fn $field(mut self, val: $ty) -> Self {
                        self.$field = Some(val);
                        self
                    }
                )*

                fn build(self) -> Result<$name, String> {
                    Ok($name {
                        $( $field: self.$field.ok_or(
                            format!("Missing field: {}", stringify!($field))
                        )?, )*
                    })
                }
            }
        }
    };
}
```

---

## Test Helper Macros

```rust
macro_rules! assert_approx_eq {
    ($a:expr, $b:expr) => {
        assert_approx_eq!($a, $b, 1e-6);
    };
    ($a:expr, $b:expr, $eps:expr) => {
        let (a, b) = ($a, $b);
        let diff = (a - b).abs();
        assert!(
            diff < $eps,
            "assertion failed: |{} - {}| = {} >= {}",
            a, b, diff, $eps
        );
    };
}

macro_rules! test_cases {
    ($name:ident, $func:expr, $( ($input:expr, $expected:expr) ),+ $(,)? ) => {
        $(
            #[test]
            fn $name() {
                assert_eq!($func($input), $expected);
            }
        )+
    };
}

#[test]
fn test_float_math() {
    assert_approx_eq!(0.1 + 0.2, 0.3);
    assert_approx_eq!(std::f64::consts::PI, 3.14159, 1e-4);
}
```

---

## Enum Dispatch Macro

```rust
macro_rules! enum_dispatch {
    (
        trait $trait_name:ident {
            $( fn $method:ident(&self $(, $arg:ident : $arg_ty:ty )* ) -> $ret:ty; )*
        }

        enum $enum_name:ident {
            $( $variant:ident($variant_ty:ty) ),* $(,)?
        }
    ) => {
        trait $trait_name {
            $( fn $method(&self $(, $arg: $arg_ty)*) -> $ret; )*
        }

        enum $enum_name {
            $( $variant($variant_ty), )*
        }

        impl $trait_name for $enum_name {
            $(
                fn $method(&self $(, $arg: $arg_ty)*) -> $ret {
                    match self {
                        $( $enum_name::$variant(inner) => inner.$method($($arg),*), )*
                    }
                }
            )*
        }
    };
}
```

---

## Part 4: Procedural Macros

Compile-time code generation with Rust code

---

## Types of Procedural Macros

All proc macros must be in a separate crate with `proc-macro = true`.

---

## Types of Procedural Macros

![types_of_procedural_macros](svg/courses/languages/rust/advanced-rust/06_macros/types_of_procedural_macros.svg)

---

## Proc Macro Crate Setup

```toml
# Cargo.toml for the proc macro crate
[package]
name = "my-macros"
version = "0.1.0"
edition = "2021"

[lib]
proc-macro = true

[dependencies]
syn = { version = "2", features = ["full"] }
quote = "1"
proc-macro2 = "1"
```

```rust
// src/lib.rs
use proc_macro::TokenStream;
use quote::quote;
use syn;

#[proc_macro_derive(MyTrait)]
pub fn my_trait_derive(input: TokenStream) -> TokenStream {
    // Parse the input tokens
    let ast = syn::parse_macro_input!(input as syn::DeriveInput);
    // Generate code
    impl_my_trait(&ast)
}

fn impl_my_trait(ast: &syn::DeriveInput) -> TokenStream {
    let name = &ast.ident;
    let gen = quote! {
        impl MyTrait for #name {
            fn hello(&self) -> String {
                format!("Hello from {}", stringify!(#name))
            }
        }
    };
    gen.into()
}
```

---

## The syn Crate

```rust
use syn::{DeriveInput, Data, Fields};

fn analyze_struct(input: &DeriveInput) {
    let name = &input.ident;
    println!("Struct name: {}", name);

    // Match on the data type (struct, enum, union)
    match &input.data {
        Data::Struct(data) => {
            match &data.fields {
                Fields::Named(fields) => {
                    for field in &fields.named {
                        let field_name = field.ident.as_ref().unwrap();
                        let field_type = &field.ty;
                        println!("  {}: {:?}", field_name, field_type);
                    }
                }
                Fields::Unnamed(fields) => {
                    for (i, field) in fields.unnamed.iter().enumerate() {
                        println!("  .{}: {:?}", i, field.ty);
                    }
                }
                Fields::Unit => println!("  (unit struct)"),
            }
        }
        Data::Enum(data) => {
            for variant in &data.variants {
                println!("  Variant: {}", variant.ident);
            }
        }
        Data::Union(_) => println!("  (union)"),
    }
}
```

---

## The quote Crate

```rust
use quote::quote;
use syn::Ident;
use proc_macro2::Span;

fn generate_code() -> proc_macro2::TokenStream {
    let struct_name = Ident::new("GeneratedStruct", Span::call_site());
    let field_name = Ident::new("value", Span::call_site());

    // quote! creates TokenStream from Rust-like syntax
    // # interpolates variables
    let tokens = quote! {
        struct #struct_name {
            #field_name: i32,
        }

        impl #struct_name {
            fn new(val: i32) -> Self {
                Self { #field_name: val }
            }

            fn get(&self) -> i32 {
                self.#field_name
            }
        }
    };

    tokens
}
```

---

## Derive Macro: Complete Example

```rust
// my_macros/src/lib.rs
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput, Data, Fields};

#[proc_macro_derive(Describe)]
pub fn describe_derive(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = &input.ident;

    let field_descriptions = match &input.data {
        Data::Struct(data) => match &data.fields {
            Fields::Named(fields) => {
                let descs: Vec<_> = fields.named.iter().map(|f| {
                    let fname = f.ident.as_ref().unwrap();
                    let ftype = &f.ty;
                    quote! {
                        format!("  {}: {}", stringify!(#fname), stringify!(#ftype))
                    }
                }).collect();
                quote! { vec![ #( #descs ),* ] }
            }
            _ => quote! { vec![] },
        },
        _ => quote! { vec![] },
    };

    let expanded = quote! {
        impl #name {
            fn describe() -> String {
                let fields = #field_descriptions;
                format!("struct {} {{\n{}\n}}", stringify!(#name), fields.join("\n"))
            }
        }
    };

    TokenStream::from(expanded)
}
```

---

## Using the Derive Macro

```rust
// In the consuming crate
use my_macros::Describe;

#[derive(Describe)]
struct User {
    name: String,
    age: u32,
    email: String,
}

fn main() {
    println!("{}", User::describe());
    // Output:
    // struct User {
    //   name: String
    //   age: u32
    //   email: String
    // }
}
```

---

## Derive Macro with Attributes

```rust
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, DeriveInput, Data, Fields, Attribute, Lit, Meta};

#[proc_macro_derive(Validate, attributes(validate))]
pub fn validate_derive(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let name = &input.ident;

    // Parse #[validate(...)] attributes on fields
    let validations = match &input.data {
        Data::Struct(data) => match &data.fields {
            Fields::Named(fields) => {
                let checks: Vec<_> = fields.named.iter().filter_map(|f| {
                    let fname = f.ident.as_ref().unwrap();
                    for attr in &f.attrs {
                        if attr.path().is_ident("validate") {
                            return Some(quote! {
                                // Validation logic based on attribute
                                if self.#fname.is_empty() {
                                    errors.push(format!("{} must not be empty",
                                        stringify!(#fname)));
                                }
                            });
                        }
                    }
                    None
                }).collect();
                quote! { #( #checks )* }
            }
            _ => quote! {},
        },
        _ => quote! {},
    };

    let expanded = quote! {
        impl #name {
            fn validate(&self) -> Result<(), Vec<String>> {
                let mut errors = Vec::new();
                #validations
                if errors.is_empty() { Ok(()) } else { Err(errors) }
            }
        }
    };

    TokenStream::from(expanded)
}
```

---

## Attribute Macros

```rust
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, ItemFn};

#[proc_macro_attribute]
pub fn log_calls(_attr: TokenStream, item: TokenStream) -> TokenStream {
    let input = parse_macro_input!(item as ItemFn);
    let name = &input.sig.ident;
    let block = &input.block;
    let sig = &input.sig;
    let vis = &input.vis;

    let expanded = quote! {
        #vis #sig {
            println!("[LOG] Entering function: {}", stringify!(#name));
            let start = std::time::Instant::now();
            let result = (|| #block)();
            println!("[LOG] Exiting {}: {:?}", stringify!(#name), start.elapsed());
            result
        }
    };

    TokenStream::from(expanded)
}

// Usage:
// #[log_calls]
// fn expensive_computation(n: u64) -> u64 {
//     (0..n).sum()
// }
```

---

## Function-Like Procedural Macros

```rust
use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, LitStr, Token};
use syn::parse::{Parse, ParseStream};

struct SqlInput {
    query: LitStr,
}

impl Parse for SqlInput {
    fn parse(input: ParseStream) -> syn::Result<Self> {
        let query: LitStr = input.parse()?;
        Ok(SqlInput { query })
    }
}

#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
    let SqlInput { query } = parse_macro_input!(input as SqlInput);
    let query_str = query.value();

    // Validate SQL at compile time
    if !query_str.to_uppercase().starts_with("SELECT") {
        return syn::Error::new(query.span(), "Only SELECT queries are allowed")
            .to_compile_error()
            .into();
    }

    let expanded = quote! {
        {
            let query = #query_str;
            database::execute_query(query)
        }
    };

    TokenStream::from(expanded)
}

// Usage:
// let results = sql!("SELECT * FROM users WHERE id = 1");
```

---

## Part 5: Real-World Macro Examples

Patterns from popular crates

---

## How serde_derive Works

```rust
// When you write:
#[derive(Serialize, Deserialize)]
struct Point {
    x: f64,
    y: f64,
}

// The derive macro generates (simplified):
impl Serialize for Point {
    fn serialize<S: Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        let mut state = serializer.serialize_struct("Point", 2)?;
        state.serialize_field("x", &self.x)?;
        state.serialize_field("y", &self.y)?;
        state.end()
    }
}

impl<'de> Deserialize<'de> for Point {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        // Generates a Visitor implementation that handles
        // field-by-field deserialization
        todo!()
    }
}
```

---

## How thiserror Works

```rust
// When you write:
#[derive(thiserror::Error, Debug)]
enum AppError {
    #[error("io error: {0}")]
    Io(#[from] std::io::Error),

    #[error("not found: {name}")]
    NotFound { name: String },
}

// The macro generates:
impl std::fmt::Display for AppError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            AppError::Io(e) => write!(f, "io error: {}", e),
            AppError::NotFound { name } => write!(f, "not found: {}", name),
        }
    }
}

impl std::error::Error for AppError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            AppError::Io(e) => Some(e),
            _ => None,
        }
    }
}

impl From<std::io::Error> for AppError {
    fn from(e: std::io::Error) -> Self { AppError::Io(e) }
}
```

---

## Configuration DSL Macro

```rust
macro_rules! config {
    (
        $( $section:ident {
            $( $key:ident : $ty:ty = $default:expr );* $(;)?
        } )*
    ) => {
        #[derive(Debug, Clone)]
        struct Config {
            $( $( $key: $ty, )* )*
        }

        impl Default for Config {
            fn default() -> Self {
                Config {
                    $( $( $key: $default, )* )*
                }
            }
        }
    };
}

config! {
    server {
        host: String = "localhost".to_string();
        port: u16 = 8080;
        max_connections: usize = 100;
    }
    database {
        url: String = "postgres://localhost/mydb".to_string();
        pool_size: usize = 10;
    }
}

fn main() {
    let config = Config::default();
    println!("{:?}", config);
}
```

---

## Part 6: When to Use Macros vs Generics

Choosing the right abstraction

---

## Decision Guide

![decision_guide](svg/courses/languages/rust/advanced-rust/06_macros/decision_guide.svg)

---

## Generics vs Macros Example

```rust
// GENERIC approach: works when the interface is uniform
fn max<T: PartialOrd>(a: T, b: T) -> T {
    if a >= b { a } else { b }
}

// MACRO approach: needed when argument count varies
macro_rules! max {
    ($a:expr) => { $a };
    ($a:expr, $b:expr) => {
        if $a >= $b { $a } else { $b }
    };
    ($a:expr, $( $rest:expr ),+) => {
        max!($a, max!( $( $rest ),+ ))
    };
}

fn main() {
    // Generic: always two arguments
    let m = max(3, 5);

    // Macro: variable number of arguments
    let m = max!(1, 5, 3, 7, 2);
    println!("{}", m); // 7
}
```

---

## Debugging Macros

```rust
// Use cargo expand to see expanded macro output
// $ cargo install cargo-expand
// $ cargo expand

// Use trace_macros! (nightly) to trace macro expansion
// #![feature(trace_macros)]
// trace_macros!(true);
// my_macro!(args);
// trace_macros!(false);

// Use stringify! to print what the macro receives
macro_rules! debug_macro {
    ($( $tokens:tt )*) => {
        println!("Macro input: {}", stringify!($( $tokens )*));
        $( $tokens )*
    };
}

// Use compile_error! for better error messages
macro_rules! strict_macro {
    (valid $x:expr) => { $x };
    ($( $tt:tt )*) => {
        compile_error!(concat!(
            "Invalid input to strict_macro!: ",
            stringify!($( $tt )*)
        ))
    };
}
```

---

## Summary

![summary](svg/courses/languages/rust/advanced-rust/06_macros/summary.svg)

---

## Exercises

1. Write a `hashset!` macro similar to `vec!` for creating HashSets.
1. Create a `retry!` macro that retries an expression N times on failure.
1. Write a declarative macro that generates both a struct and its builder.
1. Create a derive macro that generates a `to_json()` method for structs.
1. Build an attribute macro `#[measure]` that prints execution time.
1. Write a function-like proc macro that validates email format at compile time.
