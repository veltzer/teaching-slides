---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---
# Object Oriented Python Toolkit

## Overview
- Object-Oriented refresher in Python
- Functions as first-class objects
- Classes and inheritance
- Advanced OOP features
- Dynamic class and method manipulation

---

## Inheritance in Python: Basic Inheritance

- Classes can inherit from other classes
- Access to parent's methods and attributes
- Extend or override parent's functionality
- Use `super()` to call parent methods

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, my name is {self.name}"

class Employee(Person):
    def __init__(self, name, age, employee_id):
        super().__init__(name, age)
        self.employee_id = employee_id

    def greet(self):
        return f"{super().greet()} and I work here"
```

---

## Inheritance in Python: Method Resolution Order (MRO)

- Determines which method is called
- Left-to-right, depth-first search
- C3 linearization algorithm for complex hierarchies
- View with `ClassName.__mro__`

```python
class A:
    def method(self):
        return "A.method"

class B(A):
    def method(self):
        return "B.method"

class C(A):
    def method(self):
        return "C.method"

class D(B, C):
    pass

d = D()
print(d.method())  # B.method - follows MRO
print(D.__mro__)   # (D, B, C, A, object)
```

---

## Inheritance in Python: Multiple Inheritance

- Python supports inheriting from multiple classes
- Combines features from all parent classes
- MRO resolves method call conflicts
- Requires careful design to avoid complexity

```python
class Flyable:
    def fly(self):
        return "Flying!"

class Swimmable:
    def swim(self):
        return "Swimming!"

class Duck(Flyable, Swimmable):
    def speak(self):
        return "Quack!"

duck = Duck()
print(duck.fly())    # Flying!
print(duck.swim())   # Swimming!
print(duck.speak())  # Quack!
```

---

## Diamond Problem and MRO

![diamond_problem_mro](svg/courses/languages/python/advanced-python/05_oop_toolkit/diamond_problem_mro.svg)

---

## The Diamond Problem
- A class inherits from two classes with common ancestor
- Which method should be called when both inherit same method?
- MRO provides consistent resolution
- Python's C3 linearization makes this predictable

```python
class Base:
    def method(self):
        return "Base.method"

class Left(Base):
    def method(self):
        return "Left.method"

class Right(Base):
    def method(self):
        return "Right.method"

class Bottom(Left, Right):
    pass

b = Bottom()
print(b.method())  # Left.method
print(Bottom.__mro__)  # (Bottom, Left, Right, Base, object)
```

---

## Functions: Functions as First-Class Objects

- Functions are objects in Python
- Can be assigned to variables
- Passed as arguments
- Returned from other functions
- Stored in data structures

```python
def greet(name):
    return f"Hello, {name}"

# Assign to variable
say_hello = greet

# Pass as argument
def apply_function(func, value):
    return func(value)

result = apply_function(say_hello, "Alice")
print(result)  # Hello, Alice

# Store in data structure
function_list = [greet, str.upper, len]
for func in function_list:
    print(func("test"))
```

---

## Functions: Inner Functions and Closures

- Functions defined inside other functions
- Access to variables in enclosing scope
- Retain state even after outer function completes
- Foundation for decorators and advanced patterns

```python
def create_multiplier(factor):
    # factor is captured in closure
    def multiply(number):
        return number * factor
    return multiply

double = create_multiplier(2)
triple = create_multiplier(3)

print(double(5))  # 10
print(triple(5))  # 15
```

---

## Functions: Nonlocal Variables

- Used in nested functions
- Modify variables in enclosing scope
- Different from global variables
- Allows stateful closures

```python
def create_counter(start=0):
    count = start  # Local to create_counter

    def increment():
        nonlocal count  # Use count from outer scope
        count += 1
        return count

    return increment

counter = create_counter(10)
print(counter())  # 11
print(counter())  # 12
print(counter())  # 13
```

---

## Classes: Class vs Instance Attributes

- Class attributes shared by all instances
- Instance attributes unique to each instance
- Class attributes defined at class level
- Instance attributes usually defined in __init__

```python
class Dog:
    # Class attribute - shared by all instances
    species = "Canis familiaris"

    def __init__(self, name, breed):
        # Instance attributes - unique to each instance
        self.name = name
        self.breed = breed

dog1 = Dog("Rex", "German Shepherd")
dog2 = Dog("Buddy", "Golden Retriever")

print(dog1.species)  # Canis familiaris
print(dog2.species)  # Canis familiaris

# Changing class attribute affects all instances
Dog.species = "Canis lupus familiaris"
print(dog1.species)  # Canis lupus familiaris
```

---

## Classes: Instance vs Class Variables

- Instance variables stored in instance (__dict__)
- Class variables stored in class (__dict__)
- Inheritance affects what class variables are visible
- Modifying class variable changes it for all instances

```python
class Counter:
    count = 0  # Class variable shared by all instances

    def __init__(self, name):
        self.name = name  # Instance variable
        Counter.count += 1

c1 = Counter("First")
c2 = Counter("Second")
c3 = Counter("Third")

print(Counter.count)  # 3
print(c1.count)       # 3
print(c2.count)       # 3

# Assigning to instance.count creates instance variable
c1.count = 10
print(c1.count)       # 10 (instance variable)
print(Counter.count)  # 3 (class variable unchanged)
```

---

## Abstract Classes: Abstract Base Classes

- Define interfaces without implementation
- Created with `abc` module
- Force subclasses to implement specific methods
- Cannot be instantiated directly

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        """Calculate area of the shape"""
        pass

    @abstractmethod
    def perimeter(self):
        """Calculate perimeter of the shape"""
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

# rect = Shape()  # TypeError: Can't instantiate abstract class
rect = Rectangle(5, 10)
print(rect.area())       # 50
print(rect.perimeter())  # 30
```

---

## Abstract Classes: Practical Uses of ABCs

- Define common interfaces
- Enforce consistent implementations
- Document required methods
- Ensure proper subclassing

```python
from abc import ABC, abstractmethod

class DataProcessor(ABC):
    @abstractmethod
    def process(self, data):
        """Process the input data"""
        pass

    @abstractmethod
    def validate(self, data):
        """Validate the input data"""
        pass

    def run(self, data):
        """Template method - final implementation"""
        if self.validate(data):
            return self.process(data)
        else:
            raise ValueError("Invalid data")

class IntegerProcessor(DataProcessor):
    def process(self, data):
        return sum(data)

    def validate(self, data):
        return all(isinstance(x, int) for x in data)

processor = IntegerProcessor()
print(processor.run([1, 2, 3, 4]))  # 10
# processor.run([1, "2", 3])  # ValueError: Invalid data
```

---

## Abstract Classes: collections.abc Module

- Built-in abstract base classes
- Define interfaces for common collection types
- Includes: Sequence, Mapping, MutableMapping, Set
- Use for type checking and interface enforcement

```python
from collections.abc import Sequence, MutableSequence

# Check if object implements sequence protocol
print(isinstance([1, 2, 3], Sequence))     # True
print(isinstance((1, 2, 3), Sequence))     # True
print(isinstance("abc", Sequence))         # True
print(isinstance({1, 2, 3}, Sequence))     # False

# Check if object is mutable sequence
print(isinstance([1, 2, 3], MutableSequence))  # True
print(isinstance((1, 2, 3), MutableSequence))  # False
print(isinstance("abc", MutableSequence))      # False
```

---

## Properties: Basic Properties

- Method that behaves like an attribute
- Control access to attributes
- Add validation, computation, side effects
- Created with @property decorator

```python
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def email(self):
        return f"{self.first_name.lower()}.{self.last_name.lower()}@example.com"

person = Person("John", "Doe")
print(person.full_name)  # John Doe
print(person.email)      # john.doe@example.com

# Cannot assign to property without a setter
# person.full_name = "Jane Smith"  # AttributeError
```

---

## Properties: Property Getters and Setters

- Control both read and write access
- Add validation for setting values
- Maintain API compatibility when implementation changes
- Keep attribute-like syntax for properties

```python
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value

    @property
    def area(self):
        return self._width * self._height

rect = Rectangle(10, 20)
print(rect.width)  # 10
rect.width = 15    # Uses setter with validation
print(rect.area)   # 300
# rect.width = -5  # ValueError: Width must be positive
```

---

## Properties: Property Deleter

- Control attribute deletion
- Complete the property interface
- Not as commonly used as getters/setters
- Useful for cleanup or invalidation

```python
class CachedProperty:
    def __init__(self):
        self._data = None
        self._cached = False

    @property
    def data(self):
        if not self._cached:
            print("Computing value...")
            self._data = self._compute_expensive_value()
            self._cached = True
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self._cached = True

    @data.deleter
    def data(self):
        print("Clearing cache...")
        self._data = None
        self._cached = False

    def _compute_expensive_value(self):
        # Simulating expensive computation
        import time
        time.sleep(0.1)
        return 42
```

---

## Property Deleter: Usage

```python
obj = CachedProperty()
print(obj.data)  # Computing value... \n 42
print(obj.data)  # 42 (from cache)
del obj.data     # Clearing cache...
print(obj.data)  # Computing value... \n 42
```

---

## Properties: Property vs Private Attributes

- Python uses name mangling for "private" attributes
- Names starting with double underscore (__name)
- Transformed to _ClassName__name
- Properties provide cleaner interface than direct access

```python
class Account:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.__balance = balance  # "Private" attribute

    @property
    def balance(self):
        return self.__balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount
        return self.__balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        return self.__balance

acct = Account("John", 100)
print(acct.balance)  # 100
acct.deposit(50)
print(acct.balance)  # 150
# print(acct.__balance)  # AttributeError
# Name mangling makes this inaccessible
print(acct._Account__balance)  # 150 (not recommended)
```

---

## Multiple Inheritance: Mix-ins

- Small, focused classes that provide specific functionality
- Not meant to be instantiated alone
- "Mixed in" to other classes via inheritance
- Usually named with "Mixin" or "able" suffix

```python
class JSONSerializableMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class LoggableMixin:
    def log(self, message):
        print(f"[LOG] {self.__class__.__name__}: {message}")

class Person(JSONSerializableMixin, LoggableMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.log("Person instance created")

person = Person("Alice", 30)
print(person.to_json())  # {"name": "Alice", "age": 30}
person.log("Data updated")  # [LOG] Person: Data updated
```

---

## Multiple Inheritance: Common Mix-in Use Cases

- Serialization (to JSON, XML, etc.)
- Equality and comparison
- Iteration capabilities
- Compatibility with different libraries
- Logging and debugging

```python
class EqualityMixin:
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)

class DisplayMixin:
    def display(self):
        attrs = ', '.join(f"{k}={v}" for k, v in self.__dict__.items())
        print(f"{self.__class__.__name__}({attrs})")

class User(EqualityMixin, DisplayMixin):
    def __init__(self, username, email):
        self.username = username
        self.email = email

u1 = User("alice", "alice@example.com")
u2 = User("alice", "alice@example.com")
u3 = User("bob", "bob@example.com")
u1.display()  # User(username=alice, email=alice@example.com)
print(u1 == u2)  # True
print(u1 == u3)  # False
```

---

## Multiple Inheritance: Diamond Problem Solution

- Super() automatically follows MRO
- Create "cooperative" multiple inheritance
- Each class calls super() to ensure all ancestors run
- Pass no arguments to super() for automatic MRO traversal

```python
class A:
    def __init__(self):
        print("A.__init__")

class B(A):
    def __init__(self):
        print("B.__init__")
        super().__init__()

class C(A):
    def __init__(self):
        print("C.__init__")
        super().__init__()

class D(B, C):
    def __init__(self):
        print("D.__init__")
        super().__init__()

d = D()
# Output:
# D.__init__
# B.__init__
# C.__init__
# A.__init__

print(D.__mro__)
# (D, B, C, A, object)
```

---

## Static Methods: Basic Static Methods

- Methods that don't need class or instance
- Defined with @staticmethod decorator
- No special first parameter (self or cls)
- Logically related to the class

```python
class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def is_even(n):
        return n % 2 == 0

    @staticmethod
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

print(MathUtils.add(5, 3))       # 8
print(MathUtils.multiply(4, 2))  # 8
print(MathUtils.is_even(5))      # False
print(MathUtils.is_prime(7))     # True
```

---

## Static Methods: When to Use Static Methods

- Utility functions related to the class
- Functionality that doesn't need instance state
- Methods that make sense as part of the class
- Group related functions within a class namespace

```python
class StringUtils:
    @staticmethod
    def is_palindrome(s):
        s = s.lower().replace(" ", "")
        return s == s[::-1]

    @staticmethod
    def reverse_words(s):
        return " ".join(s.split()[::-1])

    @staticmethod
    def count_vowels(s):
        return sum(1 for char in s.lower() if char in "aeiou")

print(StringUtils.is_palindrome("radar"))        # True
print(StringUtils.is_palindrome("hello"))        # False
print(StringUtils.reverse_words("hello world"))  # world hello
print(StringUtils.count_vowels("beautiful"))     # 5
```

---

## Class Methods: Basic Class Methods

- Methods that operate on the class, not instances
- Defined with @classmethod decorator
- First parameter is the class itself (cls)
- Can be called on class or instances

```python
class Student:
    count = 0

    def __init__(self, name):
        self.name = name
        Student.count += 1

    @classmethod
    def get_count(cls):
        return cls.count

    @classmethod
    def create_anonymous(cls):
        return cls("Anonymous Student")

s1 = Student("Alice")
s2 = Student("Bob")
print(Student.get_count())  # 2
print(s1.get_count())       # 2 (same as Student.get_count())

anon = Student.create_anonymous()
print(anon.name)            # Anonymous Student
print(Student.get_count())  # 3
```

---

## Class Methods: Alternative Constructors

- Factory methods for creating instances
- Different ways to create objects
- More descriptive than overloaded __init__
- Support different initialization patterns

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_string):
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)

    @classmethod
    def from_timestamp(cls, timestamp):
        import datetime
        dt = datetime.datetime.fromtimestamp(timestamp)
        return cls(dt.year, dt.month, dt.day)

    @classmethod
    def today(cls):
        import datetime
        dt = datetime.datetime.now()
        return cls(dt.year, dt.month, dt.day)

    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

date1 = Date(2023, 5, 15)
date2 = Date.from_string("2023-06-20")
date3 = Date.from_timestamp(1672531200)  # 2023-01-01
date4 = Date.today()
print(date1)  # 2023-05-15
print(date2)  # 2023-06-20
print(date3)  # 2023-01-01
```

---

## Class Methods vs Static Methods

## Choosing Between Them
- _Class methods_:
    - Need access to the class
    - Create instances using cls
    - Used for alternative constructors
    - Operate on class-level attributes
- _Static methods_:
    - Don't need access to class or instance
    - Utility functions related to the class domain
    - Purely functional operations

```python
class Sample:
    count = 0

    def __init__(self, value):
        self.value = value
        Sample.count += 1

    # Class method - uses the class
    @classmethod
    def get_count(cls):
        return cls.count

    # Static method - doesn't need the class
    @staticmethod
    def is_valid_value(value):
        return isinstance(value, (int, float)) and value >= 0

    # Instance method - needs an instance
    def process(self):
        if self.is_valid_value(self.value):
            return self.value * 2
        return None

print(Sample.is_valid_value(5))   # True - static method
print(Sample.get_count())         # 0 - class method
s = Sample(10)
print(s.process())                # 20 - instance method
print(Sample.get_count())         # 1 - class method
```

---

## Method Overriding: Basic Method Overriding

- Replace parent class method in subclass
- Same method name, potentially different implementation
- Customizes behavior for specific subclasses
- Maintains interface compatibility

```python
class Animal:
    def speak(self):
        return "Some generic animal sound"

    def move(self):
        return "Moving"

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class Fish(Animal):
    def speak(self):
        return "Blub!"

    def move(self):
        return "Swimming"

animals = [Animal(), Dog(), Cat(), Fish()]
for animal in animals:
    print(f"{animal.__class__.__name__} says: {animal.speak()}")
    print(f"{animal.__class__.__name__} moves by: {animal.move()}")
```

---

## Method Overriding: Using super() for Extension

- Call the parent's method in the override
- Extend functionality rather than replace
- Maintain parent behavior while adding features
- Follows the principle of "open for extension, closed for modification"

```python
class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def info(self):
        return f"{self.make} {self.model}"

    def start(self):
        return f"{self.info()} is starting"

class Car(Vehicle):
    def __init__(self, make, model, year):
        super().__init__(make, model)
        self.year = year

    def info(self):
        # Extend parent's info method
        return f"{self.year} {super().info()}"

class ElectricCar(Car):
    def __init__(self, make, model, year, battery_size):
        super().__init__(make, model, year)
        self.battery_size = battery_size

    def start(self):
        # Extend parent's start method
        return f"{super().start()} silently with {self.battery_size} kWh battery"

ev = ElectricCar("Tesla", "Model 3", 2023, 75)
print(ev.info())   # 2023 Tesla Model 3
print(ev.start())  # 2023 Tesla Model 3 is starting silently with 75 kWh battery
```

---

## Special Methods: Operator Overloading

- Methods named with double underscores
- Called automatically for built-in operations
- Allows custom classes to behave like built-ins
- Enables natural syntax with your objects

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"Vector({self.x}, {self.y})"

v1 = Vector(2, 3)
v2 = Vector(3, 4)
print(v1 + v2)     # Vector(5, 7)
print(v1 - v2)     # Vector(-1, -1)
print(v1 * 2)      # Vector(4, 6)
print(v1 == v2)    # False
```

---

## Special Methods: Container Special Methods

- `__len__`: Length of container (len())
- `__getitem__`: Access items with [] notation
- `__setitem__`: Set items with [] notation
- `__contains__`: Membership testing with 'in'
- `__iter__`: Create iterator (for loops)

```python
class CustomList:
    def __init__(self, items):
        self.items = list(items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, value):
        self.items[index] = value

    def __contains__(self, item):
        return item in self.items

    def __iter__(self):
        return iter(self.items)

    def __str__(self):
        return f"CustomList({self.items})"

my_list = CustomList([1, 2, 3, 4])
print(len(my_list))       # 4
print(my_list[2])         # 3
my_list[1] = 10
print(3 in my_list)       # True
print([x * 2 for x in my_list])  # [2, 20, 6, 8]
print(my_list)            # CustomList([1, 10, 3, 4])
```

---

## Special Methods: String Representation Methods

- `__str__`: Human-readable string (str())
- `__repr__`: Developer-readable string (repr())
- `__format__`: Formatted string representation (format())
- Best practice: make eval(repr(obj)) recreate the object

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """Informal string representation for users"""
        return f"Point at ({self.x}, {self.y})"

    def __repr__(self):
        """Formal representation for developers"""
        return f"Point({self.x}, {self.y})"

    def __format__(self, format_spec):
        """Custom formatting"""
        if format_spec == "polar":
            r = (self.x**2 + self.y**2)**0.5
            theta = math.atan2(self.y, self.x)
            return f"r={r:.2f}, θ={theta:.2f}"
        return str(self)

p = Point(3, 4)
print(str(p))     # Point at (3, 4)
print(repr(p))    # Point(3, 4)
print(f"{p}")     # Point at (3, 4)
print(f"{p:polar}")  # r=5.00, θ=0.93
```

---

## Dynamic Method Modification: Overwriting Methods at Runtime

- Replace instance methods during execution
- Custom behavior for specific instances
- Requires knowledge of method binding
- Use `types.MethodType` for binding

```python
import types

class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, I'm {self.name}"

alice = Person("Alice")
bob = Person("Bob")

# Original behavior
print(alice.greet())  # Hello, I'm Alice
print(bob.greet())    # Hello, I'm Bob

# Define a new method
def formal_greet(self):
    return f"Good day, my name is {self.name}."

# Bind it to alice only
alice.greet = types.MethodType(formal_greet, alice)

# Now the instances behave differently
print(alice.greet())  # Good day, my name is Alice.
print(bob.greet())    # Hello, I'm Bob
```

---

## Dynamic Method Modification: Monkey Patching

- Modify or extend classes at runtime
- Add new methods to existing classes
- Useful for adding functionality to third-party code
- Powerful but can lead to maintenance issues

```python
# Extending a built-in class (not recommended in production)
def reverse_words(self):
    return " ".join(self.split()[::-1])

# Add method to the string class
str.reverse_words = reverse_words

# Now all strings have this method
s = "Hello world Python"
print(s.reverse_words())  # Python world Hello

# A safer approach is to extend only your own classes
class MyClass:
    def __init__(self, value):
        self.value = value

# Later in the code
def double_value(self):
    return self.value * 2

# Add the method
MyClass.double_value = double_value

# Test it
obj = MyClass(5)
print(obj.double_value())  # 10
```

---

## Dynamic Method Modification: Method Replacement with Decorators

- Add behavior without changing original methods
- Apply consistently across multiple methods
- Maintain compatibility with original interface
- Common patterns: logging, timing, caching

```python
import time
import functools

def log_calls(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} returned {result} in {elapsed:.6f} seconds")
        return result
    return wrapper

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def multiply(self, a, b):
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result
```

---

## Method Replacement: Applying the Decorator

```python
# Create instance
calc = Calculator()

# Replace methods with decorated versions
calc.add = log_calls(calc.add)
calc.multiply = log_calls(calc.multiply)

# Use the modified methods
calc.add(2, 3)
# Calling add
# add returned 5 in 0.000010 seconds

calc.multiply(4, 5)
# Calling multiply
# multiply returned 20 in 0.000008 seconds
```

---

## Dynamic Method Modification: Adding Methods at Runtime

- Add entirely new methods to instances
- Extend functionality on demand
- Uniquely powerful feature of Python
- Useful for plugins and extensions

```python
import types

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

alice = Person("Alice", 30)

# Define a new method
def celebrate_birthday(self):
    self.age += 1
    return f"Happy birthday! {self.name} is now {self.age}"

# Add the method to the instance
alice.celebrate_birthday = types.MethodType(celebrate_birthday, alice)

# Use the new method
print(alice.celebrate_birthday())  # Happy birthday! Alice is now 31
print(alice.age)  # 31

# Note: bob doesn't have this method
bob = Person("Bob", 25)
# bob.celebrate_birthday()  # AttributeError
```

---

## Modules: Python Modules

- Files containing Python code
- Organize code into logical units
- Single namespace for related functionality
- Imported with import statement

```python
# mymodule.py
def hello(name):
    return f"Hello, {name}!"

PI = 3.14159

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return PI * self.radius ** 2
```

```python
# Using the module
import mymodule

print(mymodule.hello("Alice"))
print(mymodule.PI)
circle = mymodule.Circle(5)
print(circle.area())
```

---

## Modules: Module Import Patterns

- Different ways to import modules
- Control what gets imported
- Manage namespace conflicts
- Alias imports for clarity or brevity

```python
# Import entire module
import math
print(math.sqrt(16))  # 4.0

# Import specific names
from random import randint, choice
print(randint(1, 10))
print(choice(["apple", "banana", "cherry"]))

# Import with alias
import numpy as np
arr = np.array([1, 2, 3])

# Import all names (not recommended)
from math import *
print(sqrt(16))  # 4.0

# Conditional import
try:
    import json
except ImportError:
    import simplejson as json
```

---

## Modules: Module Execution

- Modules execute on first import
- Code outside functions runs at import time
- `__name__` helps distinguish import vs direct run
- Enables modules to act as both libraries and scripts

```python
# mymodule.py
print(f"Module {__name__} is being imported")

def main():
    print("Running module as script")

if __name__ == "__main__":
    main()
```

```python
# When imported
import mymodule  # Prints: Module mymodule is being imported

# When run directly
# $ python mymodule.py
# Prints:
# Module __main__ is being imported
# Running module as script
```

---

## Modules: Module Attributes

- `__name__`: Module's name (or "__main__" if run directly)
- `__file__`: Path to module file
- `__doc__`: Module's docstring
- `__dict__`: Module's namespace dictionary
- `__package__`: Module's package

```python
# example.py
"""This is a sample module to demonstrate module attributes."""

def example_function():
    """This is a sample function."""
    pass

if __name__ == "__main__":
    # Print module attributes
    print(f"Module name: {__name__}")
    print(f"Module file: {__file__}")
    print(f"Module docstring: {__doc__}")
    print(f"Module package: {__package__}")
```

---

## Package Basics: Python Packages

- Directories containing modules
- Organize related modules together
- Must contain `__init__.py` (for Python < 3.3)
- Can contain sub-packages

```tree
mypackage/
├── __init__.py
├── module1.py
├── module2.py
└── subpackage/
    ├── __init__.py
    └── module3.py
```

```python
# Using the package
import mypackage.module1
import mypackage.subpackage.module3

from mypackage import module2
from mypackage.subpackage import module3

# If __init__.py sets up imports
import mypackage  # May provide direct access to modules
```

---

## Package Basics: The __init__.py File

- Makes directory a package
- Executed when package is imported
- Can set up package-level variables
- Can import names from modules for convenience
- Can be empty

```python
# mypackage/__init__.py
"""My example package."""

# Package-level variable
version = "1.0.0"

# Import common functions for easier access
from .module1 import function1, function2
from .module2 import Class1, Class2

# Internal imports
from . import subpackage
```

```python
# Using the configured package
import mypackage

print(mypackage.version)  # 1.0.0
mypackage.function1()     # From module1
obj = mypackage.Class1()  # From module2
```

---

## Practical Examples: Example: Inheritance Hierarchy

```python
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.is_running = False

    def start(self):
        self.is_running = True
        return f"{self.make} {self.model} started"

    def stop(self):
        self.is_running = False
        return f"{self.make} {self.model} stopped"

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class Car(Vehicle):
    def __init__(self, make, model, year, fuel_type):
        super().__init__(make, model, year)
        self.fuel_type = fuel_type
        self.doors = 4

    def honk(self):
        return "Beep beep!"
```

---

## Inheritance Hierarchy: Motorcycle and `ElectricCar`

```python
class Motorcycle(Vehicle):
    def __init__(self, make, model, year, has_sidecar=False):
        super().__init__(make, model, year)
        self.has_sidecar = has_sidecar

    def wheelie(self):
        return "Doing a wheelie!" if not self.has_sidecar else "Cannot do a wheelie with a sidecar"

class ElectricCar(Car):
    def __init__(self, make, model, year, battery_capacity):
        super().__init__(make, model, year, "electric")
        self.battery_capacity = battery_capacity

    def start(self):
        return f"{super().start()} silently"

    def charge(self):
        return f"Charging {self.make} {self.model} battery"
```

---

## Practical Examples: Example: Mix-in Based Design

```python
class JSONSerializableMixin:
    def to_json(self):
        import json
        # Filter out private attributes
        data = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        return json.dumps(data)

class CSVSerializableMixin:
    def to_csv(self):
        # Get public attributes as CSV row
        values = [str(getattr(self, attr)) for attr in self.csv_attributes]
        return ','.join(values)

    @classmethod
    def csv_header(cls):
        return ','.join(cls.csv_attributes)

class LoggableMixin:
    def log(self, message, level="INFO"):
        print(f"[{level}] {self.__class__.__name__}: {message}")

class ValidationMixin:
    def validate(self):
        for field in self.required_fields:
            value = getattr(self, field, None)
            if value is None or value == '':
                return False
        return True
```

---

## Mix-in Based Design: Combining Mixins in User

```python
class User(JSONSerializableMixin, CSVSerializableMixin, LoggableMixin, ValidationMixin):
    csv_attributes = ['id', 'username', 'email']
    required_fields = ['username', 'email']

    def __init__(self, id, username, email, password=None):
        self.id = id
        self.username = username
        self.email = email
        self._password = password
        self.log("User created")
```

---

## Practical Examples: Example: Class Factory

```python
def create_model_class(name, fields):
    """Create a new model class with the given fields."""
    class Meta(type):
        def __new__(mcs, name, bases, attrs):
            # Add __init__ method
            def __init__(self, **kwargs):
                for field in fields:
                    setattr(self, field, kwargs.get(field))
            attrs['__init__'] = __init__

            # Add string representation
            def __str__(self):
                field_strs = [f"{field}={getattr(self, field)}" for field in fields]
                return f"{name}({', '.join(field_strs)})"
            attrs['__str__'] = __str__

            # Add validation method
            def is_valid(self):
                return all(getattr(self, field) is not None for field in fields)
            attrs['is_valid'] = is_valid

            return super().__new__(mcs, name, bases, attrs)

    # Create and return the new class
    return Meta(name, (), {'fields': fields})

# Use the factory to create model classes
User = create_model_class('User', ['id', 'name', 'email'])
Product = create_model_class('Product', ['id', 'name', 'price'])

# Create instances
user = User(id=1, name="Alice", email="alice@example.com")
product = Product(id=101, name="Laptop", price=999.99)

print(user)  # User(id=1, name=Alice, email=alice@example.com)
print(product)  # Product(id=101, name=Laptop, price=999.99)
print(user.is_valid())  # True
```

---

## Practical Examples: Example: Property-Based Class

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

    @property
    def kelvin(self):
        return self._celsius + 273.15

    @kelvin.setter
    def kelvin(self, value):
        self.celsius = value - 273.15

    def __str__(self):
        return f"{self._celsius}°C ({self.fahrenheit}°F, {self.kelvin}K)"
```

---

## Property-Based Class: Usage

```python
# Create and use the class
temp = Temperature(25)
print(temp)  # 25°C (77.0°F, 298.15K)
temp.fahrenheit = 68
print(temp)  # 20.0°C (68.0°F, 293.15K)
temp.kelvin = 300
print(temp)  # 26.85°C (80.33°F, 300K)
```

---

## Summary

## Key Takeaways
- Python offers rich OOP features
- Inheritance provides code reuse and specialization
- Properties allow attribute-like access with control
- Mix-ins enable composition over inheritance
- Special methods customize object behavior
- Static and class methods serve different purposes
- Dynamic nature enables runtime modifications
- Modules and packages organize code effectively

---

## Next Steps

## Further Exploration
- Design patterns in Python
- Meta-programming with metaclasses
- Attribute access customization
- Type annotations and generics
- Advanced class decorators
- Context managers for resource management
- Descriptor protocol

---

## Resources

## Further Reading
- "Fluent Python" by Luciano Ramalho
- "Python Cookbook" by David Beazley and Brian K. Jones
- "Effective Python" by Brett Slatkin
- Python documentation on Classes and OOP
- Raymond Hettinger's talks on Python's Class Development Toolkit
