---
tags:
  - languages:scala
  - data-and-ai:big-data
level: intermediate
category: big-data
audience:
  - audiences:developers

---
# Scala Refresher for Apache Spark

---
## Course Overview

1. Basic Scala Syntax
1. Object-Oriented Features
1. Functional Programming
1. Collections and Data Structures
1. Error Handling
1. Pattern Matching

---

## Scala Type Hierarchy

![scala_type_hierarchy](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/scala_type_hierarchy.svg)

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

![collection_hierarchy](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/collection_hierarchy.svg)

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

![type_conversion_flow](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/type_conversion_flow.svg)

---

## String Operations

![string_operations](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/string_operations.svg)

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

![control_structures_flow](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/control_structures_flow.svg)

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

![function_types](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/function_types.svg)

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

![higher_order_functions](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/higher_order_functions.svg)

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

![object_oriented_features](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/object_oriented_features.svg)

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

![trait_hierarchy](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/trait_hierarchy.svg)

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

![collections_operations_flow](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/collections_operations_flow.svg)

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

![collection_performance_characteristics](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/collection_performance_characteristics.svg)

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

![pattern_matching_flow](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/pattern_matching_flow.svg)

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

![error_handling_hierarchy](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/error_handling_hierarchy.svg)

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

![for_comprehension_flow](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/for_comprehension_flow.svg)

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

![type_classes](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/type_classes.svg)

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

![implicits_flow](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/implicits_flow.svg)

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

![final_architecture](svg/courses/big_data/apache-spark-with-scala/01_scala_refresher/final_architecture.svg)

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
