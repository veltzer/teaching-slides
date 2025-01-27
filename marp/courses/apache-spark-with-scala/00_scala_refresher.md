# Scala Refresher for Apache Spark

## Course Overview

1. Basic Scala Syntax
1. Object-Oriented Features
1. Functional Programming
1. Collections and Data Structures
1. Error Handling
1. Pattern Matching

---

## Scala Type Hierarchy

```mermaid
graph TD
    Any --> AnyVal
    Any --> AnyRef
    AnyVal --> Int
    AnyVal --> Double
    AnyVal --> Boolean
    AnyRef --> String
    AnyRef --> List
    Nothing --> Int
    Nothing --> String
```

---

## Basic Syntax - Variables

1. Mutability with var
1. Immutability with val
1. Type Inference
1. Basic Types
1. Type Annotations

---

## Variable Declaration Examples

```scala
// Type inference
val message = "Hello"
var counter = 0

// Explicit typing
val greeting: String = "Hello"
var age: Int = 25

// Multiple declarations
val (x, y) = (10, 20)
```

---

## Collection Hierarchy

```mermaid
graph TD
    Traversable --> Iterable
    Iterable --> Seq
    Iterable --> Set
    Iterable --> Map
    Seq --> List
    Seq --> Vector
    Seq --> Array
```

---

## Numeric Types in Detail

```scala
// Integer types
val b: Byte = 127
val s: Short = 32767
val i: Int = 2147483647
val l: Long = 9223372036854775807L

// Floating point
val f: Float = 3.14f
val d: Double = 3.14159265359
```

---

## String Operations Flow

```mermaid
graph LR
    A[String] --> B[Length]
    A --> C[Substring]
    A --> D[Concatenation]
    A --> E[Interpolation]
    E --> F[s-interpolator]
    E --> G[f-interpolator]
    E --> H[raw-interpolator]
```

---

## String Operations - Basics

```scala
val str1 = "Hello"
val str2 = "World"

// Concatenation
val combined = str1 + " " + str2

// String length and access
val length = str1.length
val firstChar = str1(0)
```

[Previous string sections continue...]

---

## Function Types

```mermaid
graph LR
    A[Functions] --> B[Methods]
    A --> C[Function Values]
    A --> D[Partial Functions]
    B --> E[Instance Methods]
    B --> F[Static Methods]
    C --> G[Lambda Expressions]
```

---

[Previous function sections continue...]

---

## Collection Operations Flow

```mermaid
graph LR
    A[Collection] --> B[map]
    B --> C[filter]
    C --> D[reduce]
    A --> E[groupBy]
    E --> F[aggregate]
```

---

[Previous collections sections continue...]

---

## Pattern Matching Flow

```mermaid
graph TD
    A[Input] --> B{Type Match}
    B --> |Int| C[Integer Handler]
    B --> |String| D[String Handler]
    B --> |List| E[List Handler]
    B --> |_| F[Default Handler]
```

---

[Previous pattern matching sections continue...]

---

## Error Handling Hierarchy

```mermaid
graph TD
    A[Error Handling] --> B[Try]
    A --> C[Option]
    A --> D[Either]
    B --> E[Success]
    B --> F[Failure]
    C --> G[Some]
    C --> H[None]
    D --> I[Left]
    D --> J[Right]
```

---

[Previous error handling sections continue...]

---

## For Comprehension Flow

```mermaid
graph LR
    A[for] --> B[generator]
    B --> C[filter]
    C --> D[yield]
    D --> E[result]
```

---

[Previous sections continue with other content remaining the same but with "---" between slides...]

---

## Final Exercise Architecture

```mermaid
graph TD
    A[Account] --> B[Transaction]
    B --> C[Transfer]
    C --> D[Validation]
    D --> E[Update]
    E --> F[Result]
```

[Final sections and solution continue...]
