# Spark Core

## What is Spark Core?

1. Foundation of Spark ecosystem
1. Provides basic functionality
1. Implements RDDs
1. Handles task scheduling
1. Manages memory

---

## Core Components

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Spark Core</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## RDD Basics

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">RDD</text>
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

## RDD Characteristics

1. Immutable
1. Partitioned
1. Lazy evaluation
1. Fault-tolerant
1. Type-safe

---

## Creating RDDs

```scala
// From a collection
val data = Array(1, 2, 3, 4, 5)
val rdd = sc.parallelize(data)

// From a file
val textFile = sc.textFile("data.txt")

// From another RDD
val mappedRDD = rdd.map(_ * 2)
```

---

## RDD Operations Flow

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Source RDD</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">B</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">C</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">|Triggers| D</text>
  <rect x="25" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">D</text>
  <rect x="225" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">E</text>
  <rect x="425" y="125" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="155" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Lazy</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="100" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="100" y1="150" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Transformations Hierarchy

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Transformations</text>
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
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Transformation Examples

```scala
// Map transformation
val numbers = sc.parallelize(1 to 10)
val doubled = numbers.map(_ * 2)

// Filter transformation
val evens = numbers.filter(_ % 2 == 0)

// FlatMap transformation
val lines = sc.parallelize(List("hello world", "hi there"))
val words = lines.flatMap(_.split(" "))
```

---

## Action Types

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Actions</text>
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
  <line x1="300" y1="50" x2="700" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="300" y1="50" x2="100" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="300" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="500" y1="50" x2="500" y2="150" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

---

## Action Examples

```scala
// Collect action
val result = doubled.collect()

// Count action
val total = evens.count()

// Reduce action
val sum = numbers.reduce(_ + _)
```

---

[Continue with remaining slides, adding mermaid diagrams for concepts like:]

## Execution Model

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">RDD</text>
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
</svg>

---

## Data Partitioning

<svg viewBox="0 0 900 600" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="100" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Data Chunk 1</text>
  <rect x="225" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="300" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Data Chunk 2</text>
  <rect x="425" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="500" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Data Chunk 3</text>
  <rect x="625" y="25" width="150" height="50" rx="5" fill="#e8f4f8" stroke="#4a90e2" stroke-width="2"/>
  <text x="700" y="55" text-anchor="middle" font-family="Arial, sans-serif" font-size="14">Task</text>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
  <line x1="700" y1="50" x2="100" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="300" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="700" y1="50" x2="500" y2="50" stroke="#666" stroke-width="2" marker-end="url(#arrowhead)"/>
</svg>

[Continue with remaining content and diagrams...]
