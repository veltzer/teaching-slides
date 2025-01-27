# Scala Refresher for Apache Spark

## Basic Syntax

1. Variables and Types
1. val vs var
1. Type Inference
1. Basic Data Types
1. String Operations

## Variables and Types

```scala
// Immutable (val)
val x: Int = 42
val message = "Hello" // Type inference

// Mutable (var)
var counter: Int = 0
var name = "Alice" // Type inference
```

## Basic Data Types

```scala
val numberInt: Int = 42
val numberLong: Long = 42L
val numberDouble: Double = 42.0
val text: String = "Hello"
val isTrue: Boolean = true
val character: Char = 'A'
```

## String Operations

```scala
val str1 = "Hello"
val str2 = "World"

// Concatenation
val combined = str1 + " " + str2

// Interpolation
val name = "Alice"
val greeting = s"Hello, $name!"

// Multiline strings
val query = """
  SELECT *
  FROM users
  WHERE age > 18
"""
```

## Functions

1. Function Definition
1. Anonymous Functions
1. Higher-Order Functions
1. Partial Functions
1. Currying

## Function Definition

```scala
// Basic function
def add(a: Int, b: Int): Int = {
  a + b
}

// Single-line function
def multiply(x: Int, y: Int): Int = x * y

// Function with default parameters
def greet(name: String = "World"): String = s"Hello, $name!"

// Variable length arguments
def sum(numbers: Int*): Int = numbers.sum
```

[Content continues as before but without the marp sections and question slides...]

## Solution

```scala
case class Student(name: String, grades: List[Int]) {
  def average: Double = grades.sum.toDouble / grades.length
  def passed: Boolean = average > 60
  def highestGrade: Int = grades.max
}

val students = List(
  Student("Alice", List(95, 88, 92)),
  Student("Bob", List(75, 68, 82)),
  Student("Charlie", List(55, 48, 62))
)

val passingStudents = students.filter(_.passed)
val classAverage = students.map(_.average).sum / students.length
val topStudent = students.maxBy(_.average)
```
