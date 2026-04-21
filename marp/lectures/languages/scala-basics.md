---
tags:
- languages:scala
- concepts:programming
- concepts:functional-programming
level: beginner
category: language
audience:
- audiences:developers

---
# Scala Programming
## A Comprehensive Guide
## Mark Veltzer
## [mark.veltzer@gmail.com](mailto:mark.veltzer@gmail.com)

---

## Introduction to Scala

![title](svg/lectures/languages/scala-basics/title.svg)

---

## Introduction to Scala: Details

- Multi-paradigm programming language
- Runs on JVM
- Combines object-oriented and functional programming
- Strong static type system

---

## Setting Up Scala
```scala
// Installing via coursier
cs setup

// Running Scala REPL
scala
```

---

## Variables
```scala
val immutable = 42        // Immutable
var mutable = "Hello"     // Mutable
lazy val computed = heavyComputation()
```

---

## Type System Basics
```scala
val explicit: Int = 42
val inferred = 42         // Type inference
val nullable: String = null
```

---

## 5. Basic Types
- Numeric: `Byte`, `Short`, `Int`, `Long`
- Floating-point: `Float`, `Double`
- Text: `Char`, `String`
- Boolean: `true`, `false`
- Unit: `()`

---

## 6. String Operations I
```scala
val name = "World"
s"Hello $name"            // String interpolation
f"Pi = ${math.Pi}%.2f"   // Format interpolation
```

---

## 7. String Operations II
```scala
"""This is a
  |multiline
  |string""".stripMargin

"hello".toUpperCase
"hello".length
```

---

## Basic Control Structures
```scala
if (x > 0) "positive" else "negative"

while (condition) {
  // do something
}
```

---

## For Loops - Basic
```scala
for (i <- 1 to 5) println(i)
for (i <- 1 until 5) println(i)
```

---

## For Comprehensions
```scala
for {
  i <- 1 to 3
  j <- 1 to i
} yield (i, j)
```

---

## Pattern Matching Basics
```scala
value match {
  case 0 => "zero"
  case n if n > 0 => "positive"
  case _ => "negative"
}
```

---

## Pattern Matching Advanced
```scala
(x, y) match {
  case (0, 0) => "origin"
  case (_, 0) => "x-axis"
  case (0, _) => "y-axis"
  case (x, y) => s"point($x, $y)"
}
```

---

## Collections - List
```scala
val numbers = List(1, 2, 3)
val empty = List.empty[Int]
val cons = 1 :: List(2, 3)
```

---

## Collections - Set
```scala
val unique = Set(1, 2, 3)
unique + 4    // Add element
unique - 1    // Remove element
```

---

## Collections - Map
```scala
val dict = Map(
  "one" -> 1,
  "two" -> 2
)
dict.get("one")  // Some(1)
```

---

## Collection Operations I
```scala
list.map(_ * 2)
list.filter(_ > 2)
list.find(_ == 3)
```

---

## Collection Operations II
```scala
list.foldLeft(0)(_ + _)
list.reduce(_ + _)
list.groupBy(_ % 2)
```

---

## Collection Operations III
```scala
list.flatten
list.flatMap(x => List(x, x))
list.collect { case x if x > 2 => x * 2 }
```

---

## Functions - Basics
```scala
def add(x: Int, y: Int): Int = x + y
def greet() = println("Hello")
```

---

## Functions - Parameters
```scala
def default(x: Int = 0) = x + 1
def repeated(x: Int*) = x.sum
def named(x: Int, y: Int) = x + y
```

---

## Anonymous Functions
```scala
val add = (x: Int, y: Int) => x + y
List(1,2,3).map(x => x * 2)
List(1,2,3).map(_ * 2)  // Shorthand
```

---

## Higher-Order Functions
```scala
def operate(x: Int, y: Int, f: (Int, Int) => Int) = f(x, y)
operate(2, 3, _ + _)
operate(2, 3, _ * _)
```

---

## Function Composition
```scala
val double = (x: Int) => x * 2
val addOne = (x: Int) => x + 1
val composed = double.compose(addOne)
```

---

## Currying
```scala
def multiply(x: Int)(y: Int) = x * y
val timesFive = multiply(5)_
timesFive(3)  // 15
```

---

## Classes - Basics
```scala
class Person(name: String, age: Int) {
  def greet = s"Hi, I'm $name"
}
```

---

## Classes - Constructor Parameters
```scala
class Person(
  val name: String,      // Public field
  private val id: Int    // Private field
)
```

---

## Case Classes
```scala
case class Point(x: Int, y: Int)
val origin = Point(0, 0)
val Point(x, y) = origin  // Destructuring
```

---

## Objects
```scala
object Singleton {
  def getInstance = new Instance()
}
```

---

## Companion Objects
```scala
case class Person(name: String)
object Person {
  def apply(fullName: String) =
    new Person(fullName.trim)
}
```

---

## Traits - Basics
```scala
trait Greeting {
  def greet: String
}
```

---

## Traits - Implementation
```scala
trait Logged {
  def log(msg: String): Unit = println(msg)
}
class Service extends Logged {
  def process() = log("processing")
}
```

---

## Inheritance
```scala
class Employee(
  name: String,
  age: Int,
  val role: String
) extends Person(name, age)
```

---

## Abstract Classes
```scala
abstract class Animal {
  def sound: String
  def makeSound() = println(sound)
}
```

---

## Option Type
```scala
val present: Option[String] = Some("value")
val absent: Option[String] = None
```

---

## Option Operations
```scala
opt.getOrElse("default")
opt.map(_.toUpperCase)
opt.flatMap(x => Some(x.length))
```

---

## Either Type
```scala
def divide(x: Int, y: Int): Either[String, Int] =
  if (y == 0) Left("division by zero")
  else Right(x / y)
```

---

## Try Type
```scala
import scala.util.{Try, Success, Failure}
val result = Try {
  // code that might throw
}
```

---

## Error Handling
```scala
try {
  // risky code
} catch {
  case e: Exception => handleError(e)
} finally {
  // cleanup
}
```

---

## Implicit Parameters
```scala
def greet(name: String)(implicit greeting: String) =
  s"$greeting, $name"
implicit val defaultGreeting: String = "Hello"
```

---

## Implicit Conversions
```scala
implicit class StringOps(s: String) {
  def exclaim: String = s + "!"
}
"hello".exclaim  // "hello!"
```

---

## Type Parameters
```scala
class Box[T](value: T) {
  def get: T = value
}
```

---

## Variance
```scala
class Covariant[+T]
class Contravariant[-T]
class Invariant[T]
```

---

## Type Bounds
```scala
def process[T <: Number](value: T): Double
class Container[T >: String]
```

---

## Lazy Evaluation
```scala
lazy val expensive = {
  // computed only when needed
  heavyComputation()
}
```

---

## By-Name Parameters
```scala
def debug(msg: => String) =
  if (logging) println(msg)
```

---

## Partial Functions
```scala
val sqrt = new PartialFunction[Double, Double] {
  def isDefinedAt(x: Double) = x >= 0
  def apply(x: Double) = math.sqrt(x)
}
```

---

## Collection Views
```scala
val view = List(1,2,3).view
  .map(_ + 1)
  .filter(_ % 2 == 0)
```

---

## Futures
```scala
import scala.concurrent.Future
import scala.concurrent.ExecutionContext.Implicits.global

val f = Future {
  // async computation
}
```

---

## Promises
```scala
import scala.concurrent.Promise

val p = Promise[String]()
val f = p.future
p.success("Done!")
```

---

## Best Practices
- Prefer immutability
- Use pattern matching
- Leverage type inference
- Handle errors explicitly
- Write functional code
