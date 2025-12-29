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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Any</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">AnyVal</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">AnyRef</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Unit</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Boolean</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Number</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Int</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Long</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Double</text>
  <rect x="225" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Float</text>
  <rect x="425" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">String</text>
  <rect x="625" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">List</text>
  <rect x="25" y="325" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="355" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Option</text>
  <rect x="225" y="325" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="355" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Null</text>
  <rect x="425" y="325" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="355" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Nothing</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="150" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="150" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="150" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="150" x2="300" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="350" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="350" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="350" x2="300" y2="350" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="350" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

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

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Traversable</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Iterable</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Seq</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Set</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Map</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">IndexedSeq</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">LinearSeq</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Vector</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Array</text>
  <rect x="225" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">List</text>
  <rect x="425" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Stream</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="150" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="150" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="150" x2="300" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="150" x2="500" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Numeric Types in Detail

```scala
// Integer types
val b: Byte = 127         // 8-bit signed
val s: Short = 32767      // 16-bit signed
val i: Int = 2147483647   // 32-bit signed
val l: Long = 9223372036854775807L  // 64-bit signed

// Floating point
val f: Float = 3.14f      // 32-bit IEEE 754
val d: Double = 3.14159265359  // 64-bit IEEE 754
```

---

## Type Conversion Flow

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Byte</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Short</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Int</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Long</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Float</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Double</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="150" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## String Operations

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">String Input</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">H</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">I</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="150" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="150" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="150" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## String Interpolation Types

1. s-interpolation: `s"Hello $name"`
1. f-interpolation: `f"$value%.2f"`
1. raw-interpolation: `raw"No \n escape"`

---

## String Operations Examples

```scala
val str = "Hello, Scala!"

// Basic operations
val length = str.length
val upper = str.toUpperCase
val lower = str.toLowerCase

// Substring and splitting
val sub = str.substring(0, 5)
val parts = str.split(",")

// Pattern matching
val containsScala = str matches ".*Scala.*"
```

---

## Control Structures Flow

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Control Structures</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">H</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">I</text>
  <rect x="225" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">J</text>
  <rect x="425" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">K</text>
  <rect x="625" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">L</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="300" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="500" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="700" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Control Structure Examples

```scala
// If expression
val result = if (x > 0) "positive" else "non-positive"

// Match expression
x match {
  case 0 => "zero"
  case n if n > 0 => "positive"
  case _ => "negative"
}

// For comprehension
for {
  i <- 1 to 10
  if i % 2 == 0
} yield i * i
```

---

## Function Types

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Function</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Methods</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">FunctionValues</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">PartialFunctions</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">InstanceMethods</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">StaticMethods</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Lambda</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Anonymous</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">PatternMatch</text>
  <rect x="225" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Composition</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="300" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Function Declaration Types

```scala
// Method definition
def square(x: Int): Int = x * x

// Function value
val cube = (x: Int) => x * x * x

// Partial function
val sqrt: PartialFunction[Double, Double] = {
  case x if x >= 0 => Math.sqrt(x)
}
```

---

## Higher-Order Functions

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Function</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">H</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Function Composition Examples

```scala
// Function composition
val double = (x: Int) => x * 2
val addOne = (x: Int) => x + 1
val doubleAndAddOne = double andThen addOne
val addOneAndDouble = double compose addOne

// Currying
def multiply(x: Int)(y: Int) = x * y
val multiplyByTwo = multiply(2)_
```

---

## Object-Oriented Features

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">OOP</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Classes</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Objects</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Traits</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">CaseClasses</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">CompanionObjects</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Singleton</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Interface</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Mixins</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Class Definition Examples

```scala
// Basic class
class Person(name: String, age: Int) {
  def greet(): String = s"Hello, my name is $name"
}

// Case class
case class Point(x: Int, y: Int) {
  def distance(that: Point): Double =
    Math.sqrt(Math.pow(this.x - that.x, 2) + Math.pow(this.y - that.y, 2))
}

// Object (singleton)
object MathUtils {
  def factorial(n: Int): Int =
    if (n <= 1) 1 else n * factorial(n - 1)
}
```

---

## Trait Hierarchy

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Trait</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Interface</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Implementation</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">AbstractMethods</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">ConcreteMembers</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">SelfType</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">StackableModifications</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Trait Examples

```scala
trait Loggable {
  def log(msg: String): Unit
}

trait ConsoleLogger extends Loggable {
  def log(msg: String): Unit = println(s"[LOG] $msg")
}

trait TimeStampLogger extends Loggable {
  abstract override def log(msg: String): Unit =
    super.log(s"${System.currentTimeMillis}: $msg")
}
```

---

## Collections Operations Flow

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Collection</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">H</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">I</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Collection Method Examples

```scala
val numbers = List(1, 2, 3, 4, 5)

// Transformations
val doubled = numbers.map(_ * 2)
val even = numbers.filter(_ % 2 == 0)
val flattened = List(List(1,2), List(3,4)).flatten

// Aggregations
val sum = numbers.reduce(_ + _)
val product = numbers.fold(1)(_ * _)
```

---

## Collection Performance Characteristics

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Collection</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Access</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Insert</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Delete</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">RandomAccess</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">SequentialAccess</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Head</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Tail</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Middle</text>
  <rect x="225" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">FromHead</text>
  <rect x="425" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">FromTail</text>
  <rect x="625" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">FromMiddle</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="300" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="500" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="700" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Common Collection Types

```scala
// Lists
val list = List(1, 2, 3)

// Sets
val set = Set("apple", "banana", "orange")

// Maps
val map = Map("one" -> 1, "two" -> 2)

// Vectors
val vector = Vector(1, 2, 3, 4, 5)

// Arrays
val array = Array(1, 2, 3)
```

---

## Pattern Matching Flow

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Pattern Match</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">H</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">I</text>
  <rect x="225" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">J</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="300" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Pattern Matching Examples

```scala
def describe(x: Any): String = x match {
  case i: Int if i > 0 => s"Positive number: $i"
  case 0 => "Zero"
  case s: String => s"String: $s"
  case list: List[_] if list.isEmpty => "Empty list"
  case list: List[_] => s"List with ${list.size} elements"
  case Some(x) => s"Option containing $x"
  case None => "Empty option"
  case _ => "Unknown type"
}
```

---

## Error Handling Hierarchy

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">ErrorHandling</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">TryObject</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Either</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Option</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Success</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Failure</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Left</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Right</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Some</text>
  <rect x="225" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">None</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="300" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Error Handling Examples

```scala
// Using Try
import scala.util.{Try, Success, Failure}
def toInt(s: String): Try[Int] = Try(s.toInt)

// Using Either
def divide(a: Int, b: Int): Either[String, Int] =
  if (b == 0) Left("Division by zero")
  else Right(a / b)

// Using Option
def findUser(id: Int): Option[User] =
  if (id > 0) Some(User(id))
  else None
```

---

## For Comprehension Flow

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">For Comprehension</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">H</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## For Comprehension Examples

```scala
// Basic for comprehension
for {
  x <- 1 to 3
  y <- 1 to x
} yield (x, y)

// With filters and definitions
for {
  x <- numbers
  if x % 2 == 0
  squared = x * x
  if squared < 100
} yield squared

// Working with Options
for {
  name <- findName(id)
  age <- findAge(id)
} yield Person(name, age)
```

---

## Type Classes

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">TypeClass</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Interface</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Instances</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Usage</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Methods</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">ImplicitDefs</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">ContextBounds</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">ImplicitParameters</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Type Class Examples

```scala
// Type class definition
trait Show[A] {
  def show(a: A): String
}

// Instances
implicit val intShow: Show[Int] = new Show[Int] {
  def show(n: Int): String = n.toString
}

implicit val personShow: Show[Person] = new Show[Person] {
  def show(p: Person): String = s"${p.name} (${p.age})"
}

// Usage
def printThing[A: Show](a: A): Unit =
  println(implicitly[Show[A]].show(a))
```

---

## Implicits Flow

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Implicits</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">F</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">G</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Implicit Examples

```scala
// Implicit conversion
implicit def stringToInt(s: String): Int = s.toInt

// Implicit class (extension methods)
implicit class RichString(val s: String) {
  def increment: String = s.map(c => (c + 1).toChar)
}

// Implicit parameters
def multiply[T](x: T, y: T)(implicit num: Numeric[T]): T =
  num.times(x, y)
```

---

## Best Practices

1. Immutability
1. Type Safety
1. Composition
1. Pattern Matching
1. Error Handling

---

## Final Exercise

Create a small application demonstrating:
1. Case class definition
1. Pattern matching
1. Collection operations
1. Error handling
1. For comprehensions

---

## Final Architecture

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Main</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">DataModel</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Services</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">ErrorHandling</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">CaseClasses</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Processing</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Validation</text>
  <rect x="625" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">CustomErrors</text>
  <rect x="25" y="225" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="255" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">ErrorHandlers</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="700" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="100" y2="250" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Solution Example

```scala
// Data model
case class User(id: Int, name: String, age: Int)
case class Order(userId: Int, items: List[String], total: Double)

// Service layer
trait UserService {
  def findUser(id: Int): Option[User]
  def validateAge(user: User): Either[String, User]
}

// Implementation with error handling and processing
class UserServiceImpl extends UserService {
  def findUser(id: Int): Option[User] = ???
  def validateAge(user: User): Either[String, User] = ???
}

// Main processing
def processUser(id: Int): Either[String, User] = {
  for {
    user <- findUser(id).toRight("User not found")
    validUser <- validateAge(user)
  } yield validUser
}
```
