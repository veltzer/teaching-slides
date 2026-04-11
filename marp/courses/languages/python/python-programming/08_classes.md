---
tags:
  - languages:python
level: beginner
category: language
audience:
  - audiences:developers

---
# Classes

---
## What is a Class?
- A blueprint for creating objects
- Bundles data (attributes) and behavior (methods)
- Supports code reuse through inheritance

```python
class Dog:
    def __init__(self, name):
        self.name = name

    def bark(self):
        return f"{self.name} says Woof!"

rex = Dog("Rex")
print(rex.bark())  # Rex says Woof!
```

---
## Class vs Instance
- **Class**: The blueprint (template)
- **Instance**: A specific object created from the class
- Each instance has its own data

```python
class Dog:
    def __init__(self, name):
        self.name = name

dog1 = Dog("Rex")    # Instance 1
dog2 = Dog("Buddy")  # Instance 2
print(dog1.name)      # Rex
print(dog2.name)      # Buddy
```

---
## The `__init__` Method
- Called automatically when creating an instance
- Initializes instance attributes
- `self` refers to the instance being created

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(p.x, p.y)  # 3 4
```

---
## The `self` Parameter
- First parameter of every instance method
- Refers to the current instance
- Must be explicit (unlike `this` in Java/C++)

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius
```

---
## Instance Attributes vs Class Attributes

```python
class Dog:
    species = "Canis familiaris"  # Class attribute

    def __init__(self, name):
        self.name = name          # Instance attribute

dog1 = Dog("Rex")
dog2 = Dog("Buddy")

print(dog1.species)  # Canis familiaris (shared)
print(dog2.species)  # Canis familiaris (shared)
print(dog1.name)     # Rex (per instance)
print(dog2.name)     # Buddy (per instance)
```

---
## Class Attribute Gotcha

```python
class MyClass:
    items = []  # Shared mutable - dangerous!

a = MyClass()
b = MyClass()
a.items.append(1)
print(b.items)  # [1] - both see the change!

# Fix: initialize in __init__
class MyClass:
    def __init__(self):
        self.items = []  # Each instance gets its own
```

---
## Methods

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance
```

---
## Using the BankAccount Class

```python
account = BankAccount("Alice", 1000)
print(account.deposit(500))    # 1500
print(account.withdraw(200))   # 1300
print(account.balance)         # 1300
print(account.owner)           # Alice
```

---
## Class Methods

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_str):
        year, month, day = map(int, date_str.split("-"))
        return cls(year, month, day)

d = Date.from_string("2026-03-11")
print(d.year)  # 2026
```

- `@classmethod` receives the class, not instance
- Often used as alternative constructors

---
## Static Methods

```python
class MathUtils:
    @staticmethod
    def is_even(n):
        return n % 2 == 0

    @staticmethod
    def factorial(n):
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

print(MathUtils.is_even(4))    # True
print(MathUtils.factorial(5))  # 120
```

- `@staticmethod` has no `self` or `cls` parameter
- Just a function that lives in the class namespace

---
## `__str__` and `__repr__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p = Point(3, 4)
print(p)        # (3, 4)        - uses __str__
print(repr(p))  # Point(3, 4)   - uses __repr__
print([p])      # [Point(3, 4)] - uses __repr__
```

---
## `__str__` vs `__repr__`
- `__str__`: Human-readable representation
    - Used by `print()` and `str()`
- `__repr__`: Unambiguous developer representation
    - Used in the REPL and `repr()`
    - Ideally, `eval(repr(obj))` recreates the object
- If only one is defined, implement `__repr__`

---
## Comparison Methods

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

p1 = Point(1, 2)
p2 = Point(1, 2)
p3 = Point(3, 4)
print(p1 == p2)  # True
print(p1 < p3)   # True
```

---
## Using `@functools.total_ordering`

```python
from functools import total_ordering

@total_ordering
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

# Now <=, >, >= also work automatically
```

---
## Arithmetic Operator Overloading

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)    # Vector(4, 6)
print(v1 * 3)     # Vector(3, 6)
```

---
## Operator Overloading Methods
| Operator | Method |
|----------|--------|
| `+` | `__add__` |
| `-` | `__sub__` |
| `*` | `__mul__` |
| `/` | `__truediv__` |
| `//` | `__floordiv__` |
| `%` | `__mod__` |
| `**` | `__pow__` |
| `==` | `__eq__` |
| `<` | `__lt__` |
| `len()` | `__len__` |
| `[]` | `__getitem__` |

---
## The `__len__` and `__getitem__` Methods

```python
class Playlist:
    def __init__(self, songs):
        self._songs = list(songs)

    def __len__(self):
        return len(self._songs)

    def __getitem__(self, index):
        return self._songs[index]

p = Playlist(["Song A", "Song B", "Song C"])
print(len(p))     # 3
print(p[0])       # Song A
print(p[-1])      # Song C
for song in p:    # Iteration works too
    print(song)
```

---
## The `__contains__` Method

```python
class Playlist:
    def __init__(self, songs):
        self._songs = list(songs)

    def __contains__(self, song):
        return song in self._songs

p = Playlist(["Song A", "Song B"])
print("Song A" in p)  # True
print("Song C" in p)  # False
```

---
## The `__bool__` Method

```python
class Playlist:
    def __init__(self, songs):
        self._songs = list(songs)

    def __bool__(self):
        return len(self._songs) > 0

empty = Playlist([])
full = Playlist(["Song A"])

if empty:
    print("Has songs")
else:
    print("Empty")  # This prints

if full:
    print("Has songs")  # This prints
```

---
## The `__hash__` Method

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        return hash((self.x, self.y))

# Can now use as dict key or in sets
points = {Point(1, 2), Point(3, 4)}
cache = {Point(0, 0): "origin"}
```

---
## Inheritance - Basic

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

dog = Dog("Rex")
cat = Cat("Whiskers")
print(dog.speak())  # Rex says Woof!
print(cat.speak())  # Whiskers says Meow!
```

---
## Inheritance - `super()`

```python
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Dog(Animal):
    def __init__(self, name, age, breed):
        super().__init__(name, age)
        self.breed = breed

dog = Dog("Rex", 5, "Labrador")
print(dog.name)   # Rex
print(dog.age)    # 5
print(dog.breed)  # Labrador
```

---
## Checking Inheritance

```python
class Animal:
    pass

class Dog(Animal):
    pass

dog = Dog()
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True
print(issubclass(Dog, Animal))  # True
print(issubclass(Animal, Dog))  # False
```

---
## Multiple Inheritance

```python
class Flyable:
    def fly(self):
        return "I can fly!"

class Swimmable:
    def swim(self):
        return "I can swim!"

class Duck(Flyable, Swimmable):
    def quack(self):
        return "Quack!"

duck = Duck()
print(duck.fly())    # I can fly!
print(duck.swim())   # I can swim!
print(duck.quack())  # Quack!
```

---
## Method Resolution Order (MRO)

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

d = D()
print(d.method())  # "B"
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

---
## MRO - C3 Linearization

![mro_c3_linearization](svg/courses/languages/python/python-programming/08_classes/mro_c3_linearization.svg)

---
## MRO - C3 Linearization

- Python uses C3 linearization algorithm
- Guarantees each class appears only once
- Respects the inheritance order
- Use `ClassName.__mro__` or `ClassName.mro()` to inspect

---
## Mixins
- A class designed to add specific behavior
- Not meant to be instantiated on its own

```python
class JsonMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class Person(JsonMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 30)
print(p.to_json())  # {"name": "Alice", "age": 30}
```

---
## Abstract Base Classes

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

# shape = Shape()  # TypeError: Can't instantiate
```

---
## Properties - The Problem

```python
class Person:
    def __init__(self, age):
        self.age = age  # No validation!

p = Person(30)
p.age = -5   # Allowed but wrong!
print(p.age)  # -5
```

---
## Properties - The Solution

```python
class Person:
    def __init__(self, age):
        self.age = age  # Calls the setter

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Age must be non-negative")
        self._age = value

p = Person(30)
print(p.age)  # 30
# p.age = -5  # ValueError!
```

---
## Read-Only Properties

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(c.radius)  # 5
print(c.area)    # 78.53975
# c.area = 100   # AttributeError: can't set attribute
```

---
## Property Deleter

```python
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        print(f"Deleting {self._name}")
        self._name = None

p = Person("Alice")
del p.name  # Prints: Deleting Alice
```

---
## Class Decorators

```python
def add_repr(cls):
    def __repr__(self):
        attrs = ", ".join(
            f"{k}={v!r}"
            for k, v in self.__dict__.items()
        )
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

print(Point(3, 4))  # Point(x=3, y=4)
```

---
## `dataclasses` (Python 3.7+)

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p = Point(3, 4)
print(p)          # Point(x=3, y=4)
print(p.x)        # 3
print(p == Point(3, 4))  # True
```

- Auto-generates `__init__`, `__repr__`, `__eq__`

---
## `dataclasses` - Options

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)  # Immutable
class Color:
    r: int
    g: int
    b: int

@dataclass
class Student:
    name: str
    age: int
    grades: list = field(default_factory=list)

s = Student("Alice", 20)
s.grades.append(95)
print(s)  # Student(name='Alice', age=20, grades=[95])
```

---
## `__slots__`
- Restricts attributes to a fixed set
- Saves memory, slightly faster attribute access

```python
class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(p.x)     # 3
# p.z = 5      # AttributeError!
```

---
## Private and Protected Naming
- Python has no true private attributes
- Convention only:
    - `_name`: Protected (internal use, do not access from outside)
    - `__name`: Name-mangled (harder to access from outside)

```python
class MyClass:
    def __init__(self):
        self.public = 1
        self._protected = 2
        self.__private = 3

obj = MyClass()
print(obj.public)           # 1
print(obj._protected)       # 2 (works but discouraged)
print(obj._MyClass__private)  # 3 (name-mangled)
```

---
## The `__dict__` Attribute
- Every instance stores its attributes in `__dict__`

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

p = Person("Alice", 30)
print(p.__dict__)
# {'name': 'Alice', 'age': 30}

# You can even modify it directly
p.__dict__["email"] = "alice@example.com"
print(p.email)  # alice@example.com
```

---
## Context Managers with Classes

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
        return False  # Don't suppress exceptions

with FileManager("test.txt", "w") as f:
    f.write("Hello!")
```

---
## The `__call__` Method

```python
class Polynomial:
    def __init__(self, *coefficients):
        self.coefficients = coefficients

    def __call__(self, x):
        result = 0
        for i, coeff in enumerate(self.coefficients):
            result += coeff * x ** i
        return result

# f(x) = 1 + 2x + 3x^2
f = Polynomial(1, 2, 3)
print(f(0))   # 1
print(f(1))   # 6
print(f(2))   # 17
```

---
## Descriptors

```python
class Positive:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        return obj.__dict__.get(self.name, 0)

    def __set__(self, obj, value):
        if value < 0:
            raise ValueError(f"{self.name} must be positive")
        obj.__dict__[self.name] = value

class Product:
    price = Positive()
    quantity = Positive()

p = Product()
p.price = 10     # OK
# p.price = -1   # ValueError!
```

---
## Composition vs Inheritance
- Inheritance: "is-a" relationship
- Composition: "has-a" relationship

```python
# Composition (preferred when possible)
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self):
        self.engine = Engine()

    def start(self):
        return self.engine.start()

car = Car()
print(car.start())  # Engine started
```

---
## Summary
- Classes bundle data and behavior into objects
- `__init__` initializes instances; `self` refers to the instance
- Special methods (`__str__`, `__repr__`, `__eq__`, etc.) customize behavior
- Inheritance enables code reuse; use `super()` to call parent methods
- MRO determines method resolution in multiple inheritance
- Properties provide controlled attribute access
- `@dataclass` simplifies class creation
- Prefer composition over inheritance when appropriate
