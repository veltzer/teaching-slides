# Scala Refresher for Apache Spark

## Course Overview

1. Basic Scala Syntax
1. Object-Oriented Features
1. Functional Programming
1. Collections and Data Structures
1. Error Handling
1. Pattern Matching

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

## Basic Data Types

1. Numeric Types
1. Text Types
1. Boolean Type
1. Unit Type
1. Null and Nothing

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

---

## String Interpolation

```scala
val name = "Alice"
val age = 25

// s-interpolator
val s1 = s"$name is $age years old"

// f-interpolator
val height = 1.75
val s2 = f"$name is $height%.2f meters tall"

// raw-interpolator
val path = raw"C:\new\text.txt"
```

---

## Multiline Strings

```scala
val query = """
  SELECT *
  FROM users
  WHERE age > 18
  AND country = 'US'
  ORDER BY name
"""

val formatted = s"""
  |This is a
  |formatted multiline
  |string with $name
""".stripMargin
```

---

## Functions - Basics

1. Method Definition
1. Parameters
1. Return Types
1. Default Values
1. Named Parameters

---

## Function Definition Examples

```scala
// Basic function
def add(a: Int, b: Int): Int = a + b

// Multi-line function
def factorial(n: Int): Int = {
  if (n <= 1) 1
  else n * factorial(n - 1)
}

// Default parameters
def greet(name: String = "World"): String =
  s"Hello, $name!"
```

---

## Parameter Types

```scala
// Multiple parameter lists
def multiply(x: Int)(y: Int): Int = x * y

// Variable length arguments
def sum(numbers: Int*): Int = numbers.sum

// Named parameters
def divide(dividend: Int, divisor: Int): Double =
  dividend.toDouble / divisor
```

---

## Type Parameters

```scala
// Generic function
def firstElement[A](list: List[A]): Option[A] =
  list.headOption

// Multiple type parameters
def pair[A, B](a: A, b: B): (A, B) = (a, b)

// Bounded type parameters
def maximum[T <: Ordered[T]](a: T, b: T): T =
  if (a > b) a else b
```

---

## Anonymous Functions

```scala
// Basic syntax
val double = (x: Int) => x * 2

// Multiple parameters
val add = (x: Int, y: Int) => x + y

// With type annotation
val isEven: Int => Boolean = x => x % 2 == 0

// Using placeholder syntax
val triple = (_: Int) * 3
```

---

## Higher-Order Functions

```scala
// Function that takes a function
def transform(x: Int, f: Int => Int): Int = f(x)

// Function that returns a function
def multiplier(factor: Int): Int => Int =
  (x: Int) => x * factor

// Usage
val result1 = transform(3, x => x * x)
val doubler = multiplier(2)
```

---

## Collections - Overview

1. Immutable Collections
1. Mutable Collections
1. Sequences
1. Sets
1. Maps

---

## Lists

```scala
// Creating lists
val numbers = List(1, 2, 3, 4, 5)
val empty = List.empty[Int]

// Cons operator
val newList = 0 :: numbers

// List operations
val head = numbers.head
val tail = numbers.tail
val reversed = numbers.reverse
```

---

## List Operations

```scala
val numbers = List(1, 2, 3, 4, 5)

// Transformations
val doubled = numbers.map(_ * 2)
val evens = numbers.filter(_ % 2 == 0)
val sum = numbers.reduce(_ + _)

// Folding
val product = numbers.fold(1)(_ * _)
```

---

## Arrays

```scala
// Creating arrays
val numbers = Array(1, 2, 3, 4, 5)
val zeros = new Array[Int](5)

// Multidimensional arrays
val matrix = Array.ofDim[Int](3, 3)

// Operations
numbers(0) = 10
val first = numbers(0)
```

---

## Sets

```scala
// Immutable set
val uniqueNumbers = Set(1, 2, 3, 3, 4)

// Mutable set
val mutableSet = scala.collection.mutable.Set(1, 2, 3)

// Set operations
val combined = uniqueNumbers ++ Set(4, 5, 6)
val intersection = uniqueNumbers & Set(2, 3, 4)
```

---

## Maps

```scala
// Immutable map
val scores = Map("Alice" -> 95, "Bob" -> 88)

// Mutable map
val mutableScores =
  scala.collection.mutable.Map[String, Int]()

// Operations
val aliceScore = scores.get("Alice")
mutableScores += ("Charlie" -> 90)
```

---

## Collection Operations

```scala
val numbers = List(1, 2, 3, 4, 5)

// Basic operations
val doubled = numbers.map(_ * 2)
val evens = numbers.filter(_ % 2 == 0)
val sum = numbers.sum

// Advanced operations
val pairs = numbers.grouped(2).toList
val sliding = numbers.sliding(3).toList
```

---

## Pattern Matching - Basics

```scala
def describe(x: Any): String = x match {
  case i: Int => s"Integer: $i"
  case s: String => s"String: $s"
  case list: List[_] => s"List with ${list.size} elements"
  case _ => "Unknown type"
}
```

---

## Pattern Types

```scala
val result = someValue match {
  // Constant patterns
  case 0 => "Zero"
  case true => "True"

  // Constructor patterns
  case Person(name, age) => s"Person: $name, $age"

  // Sequence patterns
  case List(1, 2, _*) => "List starting with 1, 2"

  // Type patterns
  case s: String => s"String: $s"
}
```

---

## Case Classes

```scala
case class Person(name: String, age: Int)

// Creation
val alice = Person("Alice", 25)

// Pattern matching
def greet(person: Person): String = person match {
  case Person(name, age) if age < 18 =>
    s"Hey $name!"
  case Person(name, _) =>
    s"Hello Mr/Ms $name"
}
```

---

## Error Handling - Try

```scala
import scala.util.{Try, Success, Failure}

def divide(a: Int, b: Int): Try[Int] = Try(a / b)

divide(10, 2) match {
  case Success(result) => println(s"Result: $result")
  case Failure(e) => println(s"Error: ${e.getMessage}")
}
```

---

## Option Type

```scala
def findPerson(id: Int): Option[Person] = {
  if (id > 0) Some(Person("John", 30))
  else None
}

// Usage
val person = findPerson(1)
val name = person.map(_.name).getOrElse("Unknown")
```

---

## Either Type

```scala
def divide(a: Int, b: Int): Either[String, Int] = {
  if (b == 0) Left("Division by zero")
  else Right(a / b)
}

divide(10, 2) match {
  case Right(result) => s"Result: $result"
  case Left(error) => s"Error: $error"
}
```

---

## For Comprehensions

```scala
case class User(name: String)
case class Address(street: String)

def findUser(id: Int): Option[User] = ???
def findAddress(user: User): Option[Address] = ???

val result = for {
  user <- findUser(1)
  addr <- findAddress(user)
} yield (user.name, addr.street)
```

---

## Advanced Pattern Matching

```scala
// Extractors
object Email {
  def unapply(str: String): Option[(String, String)] = {
    val parts = str.split("@")
    if (parts.length == 2) Some(parts(0), parts(1))
    else None
  }
}

"user@domain.com" match {
  case Email(user, domain) =>
    s"User: $user, Domain: $domain"
  case _ => "Invalid email"
}
```

---

## Implicits

```scala
// Implicit conversion
implicit def intToString(x: Int): String = x.toString

// Implicit parameters
def multiply(x: Int)(implicit factor: Int): Int =
  x * factor

implicit val defaultFactor: Int = 2
println(multiply(4)) // Uses defaultFactor
```

---

## Type Classes

```scala
trait Printable[A] {
  def format(value: A): String
}

implicit val intPrintable: Printable[Int] =
  new Printable[Int] {
    def format(value: Int): String = value.toString
  }

def format[A](value: A)(implicit p: Printable[A]): String =
  p.format(value)
```

---

## Functional Concepts

```scala
// Pure functions
def add(a: Int, b: Int): Int = a + b

// Function composition
val double = (x: Int) => x * 2
val addOne = (x: Int) => x + 1
val doubleAndAddOne = double andThen addOne

// Partial application
def multiply(x: Int)(y: Int) = x * y
val multiplyByTwo = multiply(2)_
```

---

## Collections - Advanced

```scala
// Views for lazy evaluation
val numbers = (1 to 1000000).view
  .map(_ * 2)
  .filter(_ % 3 == 0)
  .take(10)
  .toList

// Parallel collections
val result = (1 to 1000000).par
  .filter(_ % 2 == 0)
  .sum
```

---

## Best Practices

1. Prefer immutability
1. Use type inference wisely
1. Leverage pattern matching
1. Handle errors explicitly
1. Use pure functions
1. Consider performance implications

---

## Practice Exercise

```scala
// Create a case class hierarchy for a simple banking system
case class Account(id: String, balance: Double)
case class Transaction(from: String, to: String, amount: Double)

// Implement basic operations
def transfer(accounts: Map[String, Account],
            tx: Transaction): Either[String, Map[String, Account]] = {
  // Implementation exercise for students
}
```

---

## Solution Overview

```scala
def transfer(accounts: Map[String, Account],
            tx: Transaction): Either[String, Map[String, Account]] = {
  for {
    from <- accounts.get(tx.from)
      .toRight(s"Account ${tx.from} not found")
    to <- accounts.get(tx.to)
      .toRight(s"Account ${tx.to} not found")
    _ <- Either.cond(from.balance >= tx.amount,
      (),
      "Insufficient funds")
  } yield accounts
    .updated(tx.from, Account(tx.from, from.balance - tx.amount))
    .updated(tx.to, Account(tx.to, to.balance + tx.amount))
}
```
