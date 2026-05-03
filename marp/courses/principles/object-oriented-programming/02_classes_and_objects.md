---
tags:
  - concepts:oop
  - languages:python
  - languages:java
level: beginner
category: design-patterns
audience:
  - audiences:developers

---
# Classes and Objects

---
## What This Chapter Covers

- Defining classes
- Creating and using objects
- Attributes (fields) and methods
- Constructors
- Instance vs class members
- Object identity vs equality
- Same examples in Python and Java

---
## Anatomy Of A Class

![object_anatomy](svg/courses/principles/object-oriented-programming/02_classes_and_objects/object_anatomy.svg)

---
## A Class in Python

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name} says woof")
```

- `class` keyword introduces a class
- `__init__` is the constructor
- `self` is the current instance — always the first parameter
- Attributes are set on `self`

---
## The Same Class in Java

```java
public class Dog {
    private String name;
    private int age;

    public Dog(String name, int age) {
        this.name = name;
        this.age = age;
    }

    public void bark() {
        System.out.println(name + " says woof");
    }
}
```

- Field declarations at the top
- Constructor: same name as the class, no return type
- `this` refers to the current instance (often optional)
- Java is verbose; the structure is the same

---
## Creating Instances

```python
rex = Dog("Rex", 3)
lassie = Dog("Lassie", 5)
rex.bark()      # Rex says woof
lassie.bark()   # Lassie says woof
```

```java
Dog rex = new Dog("Rex", 3);
Dog lassie = new Dog("Lassie", 5);
rex.bark();
lassie.bark();
```

- Each `new` (or constructor call) creates a fresh object
- Each object has its own state

---
## Attributes / Fields

- Belong to a single instance
- Hold the per-object state
- Different instances have different attribute values
- Two `Dog` objects share no attribute state — only the class definition

---
## Methods

- Functions defined inside a class
- First parameter is the receiver (`self` in Python, implicit `this` in Java)
- Operate on the receiver's attributes
- Define what objects of the class can *do*

---
## Constructors

- Run when the object is being created
- Set up initial state
- Validate arguments — fail loudly on bad input
- Once construction returns, the object should be usable
- Avoid heavy work in the constructor — separate concerns

---
## Instance Members vs Class Members

```python
class Dog:
    SPECIES = "Canis lupus familiaris"  # class attribute

    def __init__(self, name):
        self.name = name                  # instance attribute
```

- Class members (static, in Java) belong to the *class*
- Instance members belong to each *object*
- Class members are shared by all instances
- Use class members for constants and counters

---
## Object Identity vs Equality

- **Identity**: are these two references to the *same* object?
- **Equality**: do these two objects have the *same content*?
- Python: `is` for identity, `==` for equality
- Java: `==` for identity, `.equals()` for equality
- Default `==`/`.equals()` is identity unless you override

---
## Implementing Equality

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        return isinstance(other, Point) \
            and self.x == other.x \
            and self.y == other.y
```

- Override `__eq__` (Python) or `equals` (Java) to define value equality
- If you override equality, override `__hash__` too — they must agree
- Equality should be reflexive, symmetric, transitive

---
## Constructors with Defaults

```python
class Dog:
    def __init__(self, name, age=0):
        self.name = name
        self.age = age
```

- Default arguments give optional construction
- In Java, this is done with constructor overloading
- Don't use mutable defaults in Python — they're shared across calls

---
## Object Lifecycle

- Created (constructor runs)
- Used (methods called, attributes read/written)
- Eligible for collection when no references remain (Python, Java)
- Manual destruction in C++; not your problem in managed languages
- "Destructors" exist (`__del__`, `finalize`) but should not be used for cleanup

---
## Naming Conventions

- Class names: `PascalCase` (Dog, OrderService, HttpClient)
- Method names: `snake_case` in Python, `camelCase` in Java
- Constants (class members): `UPPER_SNAKE_CASE`
- Private fields: leading underscore in Python, `private` in Java
- Consistent naming within a project matters more than which style

---
## A First Mental Model

- Class = a kind of thing
- Object = a specific instance of that kind
- Methods = the things you can ask it to do
- Attributes = what it remembers
- Identity = "is this the same one?"; equality = "is this an equivalent one?"

---
## Common Mistakes

- Treating classes as namespaces for unrelated functions
- Constructors that do too much work (DB calls, network I/O)
- Overriding `equals` without `hashCode` — collections break in subtle ways
- Mutable defaults in Python constructors
- Putting business logic in `__init__` instead of explicit methods
