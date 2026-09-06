---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---

# Python Meta-classes

## Overview
- Understanding Python's class system
- What are metaclasses and how they work
- Use cases for metaclasses
- Creating your own metaclasses
- Examples of metaclasses in Python libraries
- Domain-specific languages with metaclasses

---

## Python's Class System

## Classes as Objects
- In Python, everything is an object
- Classes are objects too
- Classes are instances of a type called `type`
- Classes can be created, modified, and passed around at runtime
- Classes have attributes and methods like any other object

```python
# Classes are objects and can be assigned to variables
MyClass = type('MyClass', (), {})
instance = MyClass()

# Classes have attributes
print(type(MyClass))  # <class 'type'>
print(MyClass.__name__)  # MyClass

# Classes can be created dynamically
def create_class(name):
    return type(name, (), {})

NewClass = create_class('DynamicClass')
instance = NewClass()
print(type(instance))  # <class '__main__.DynamicClass'>
```

---

## Class Creation Pipeline

![class_creation_process](svg/courses/languages/python/advanced-python/12_metaclasses/class_creation_process.svg)

---

## Python's Class System: Class Creation Process

1. Python encounters a `class` statement
1. Executes the class body to create a namespace dictionary
1. Calls the metaclass to create the class object
1. The class object is bound to the class name

```python
# Under the hood, this class definition...
class MyClass:
    attribute = 42

    def method(self):
        return "Hello"

# ...is roughly equivalent to this:
namespace = {}
exec("""
attribute = 42

def method(self):
    return "Hello"
""", globals(), namespace)

MyClass = type('MyClass', (), namespace)
```

---

## Python's Class System: `type` as a Class Factory

- `type` is a metaclass - a class that creates classes
- `type(name, bases, dict)` creates a new class
- `name`: Name of the class
- `bases`: Tuple of base classes
- `dict`: Dictionary of attributes and methods

```python
# Creating a class with type
Person = type('Person', (), {
    'species': 'Homo sapiens',
    'greeting': lambda self: f"Hello, I'm {self.name}"
})

# Adding attributes/methods after creation
Person.age = 0

# Adding an __init__ method
def init_person(self, name):
    self.name = name

Person.__init__ = init_person

# Using the class
p = Person("Alice")
print(p.greeting())  # Hello, I'm Alice
print(p.species)     # Homo sapiens
```

---

## What are Metaclasses?: Metaclass Definition

- A metaclass is a class whose instances are classes
- The metaclass of a class determines how that class is constructed
- The default metaclass for all classes is `type`
- Metaclasses allow customizing class creation
- They are the "type of a type"

```python
# The metaclass relationship
class MyClass:
    pass

instance = MyClass()

print(type(instance))    # <class '__main__.MyClass'>
print(type(MyClass))     # <class 'type'>
print(type(type))        # <class 'type'> - type is its own metaclass

# Specifying a metaclass explicitly
class MyClass(metaclass=type):  # This is the default
    pass
```

---

## What are Metaclasses?: When to Use Metaclasses

- Framework development
- API design
- Class validation
- Class registration
- Automatic method generation
- Aspect-oriented programming
- Domain-specific languages

```python
# The famous quote by Tim Peters:
"""
Metaclasses are deeper magic than 99% of users should ever worry about.
If you wonder whether you need them, you don't
(the people who actually need them know with certainty that they need them,
and don't need an explanation about why).
"""
```

---

## What are Metaclasses?: The Metaclass Hierarchy

- `type` is the default metaclass
- Custom metaclasses typically inherit from `type`
- A class's metaclass is determined by:
    1. Explicit `metaclass` keyword argument
    1. Metaclasses of base classes
    1. Defaulting to `type`

```python
# Metaclass hierarchy example
class Meta(type):
    pass

class Base(metaclass=Meta):
    pass

class Derived(Base):  # Inherits Base's metaclass
    pass

print(type(Derived))  # <class '__main__.Meta'>

# Multiple inheritance can cause conflicts
class OtherMeta(type):
    pass

class OtherBase(metaclass=OtherMeta):
    pass

# This would raise TypeError due to metaclass conflict
# class Conflict(Base, OtherBase):
#     pass
```

---

## Creating Your First Metaclass: Basic Metaclass Structure

- Inherit from `type`
- Override `__new__` and/or `__init__`
- `__new__` creates the class
- `__init__` initializes the class
- Return the created class

```python
class SimpleMeta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"Creating class {name}")
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        print(f"Initializing class {name}")
        super().__init__(name, bases, namespace)

# Using the metaclass
class MyClass(metaclass=SimpleMeta):
    x = 1

    def method(self):
        return self.x

# Output:
# Creating class MyClass
# Initializing class MyClass

# Creating an instance doesn't trigger the metaclass
instance = MyClass()  # No output from metaclass
```

---

## Creating Your First Metaclass: Understanding the Parameters

- `mcs`: The metaclass itself
- `name`: Name of the class being created
- `bases`: Tuple of the class's base classes
- `namespace`: Dictionary of class attributes and methods

```python
class InspectiveMeta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"Metaclass: {mcs.__name__}")
        print(f"Class name: {name}")
        print(f"Bases: {', '.join(base.__name__ for base in bases) or 'none'}")
        print(f"Attributes: {list(namespace.keys())}")

        # Filter out special methods
        methods = [key for key, val in namespace.items()
                  if callable(val) and not key.startswith('__')]
        print(f"Methods: {methods}")

        return super().__new__(mcs, name, bases, namespace)

class MyClass(metaclass=InspectiveMeta):
    x = 1
    y = 2

    def method1(self):
        pass

    def method2(self):
        pass
```

---

## Creating Your First Metaclass: `__new__` vs `__init__`

- `__new__`: Called to create the class object
    - Can modify the class namespace before creation
    - Can create an entirely different class
    - Returns the new class object
- `__init__`: Called to initialize the created class
    - Can modify the class after creation
    - Cannot change the class type
    - Returns None

```python
class ModifyingMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Add an attribute before class creation
        namespace['added_by_new'] = 'from __new__'
        return super().__new__(mcs, name, bases, namespace)

    def __init__(cls, name, bases, namespace):
        # Add an attribute after class creation
        cls.added_by_init = 'from __init__'

class MyClass(metaclass=ModifyingMeta):
    pass

print(MyClass.added_by_new)  # from __new__
print(MyClass.added_by_init) # from __init__
```

---

## Creating Your First Metaclass: Class Decorators vs Metaclasses

- Both can modify classes
- Class decorators are simpler and more limited
- Metaclasses have access to class creation process
- Decorators can't affect inheritance
- Metaclasses apply to subclasses automatically

```python
# Class decorator
def add_method(cls):
    def new_method(self):
        return "Added by decorator"
    cls.new_method = new_method
    return cls

@add_method
class Decorated:
    pass

# Metaclass equivalent
class AddMethodMeta(type):
    def __new__(mcs, name, bases, namespace):
        def new_method(self):
            return "Added by metaclass"
        namespace['new_method'] = new_method
        return super().__new__(mcs, name, bases, namespace)

class Metaclassed(metaclass=AddMethodMeta):
    pass

# Subclass behavior differs
class DecoratedChild(Decorated):
    pass  # Doesn't inherit decorator logic

class MetaclassedChild(Metaclassed):
    pass  # Inherits metaclass logic

print(hasattr(DecoratedChild, 'new_method'))    # False
print(hasattr(MetaclassedChild, 'new_method'))  # True
```

---

## Practical Metaclass Uses: Method Registration

- Automatically register methods that match a pattern
- Create method registries for plugins/callbacks
- Organize methods by category
- Avoid manual registration

```python
class RegisterMethods(type):
    def __new__(mcs, name, bases, namespace):
        # Create registry of event handlers
        handlers = {}

        # Find methods that start with 'on_'
        for key, value in namespace.items():
            if callable(value) and key.startswith('on_'):
                event_name = key[3:]  # Remove 'on_' prefix
                handlers[event_name] = value

        # Add the registry to the class
        namespace['_event_handlers'] = handlers

        return super().__new__(mcs, name, bases, namespace)

class EventSystem(metaclass=RegisterMethods):
    def on_click(self):
        print("Click event handler")

    def on_hover(self):
        print("Hover event handler")

    def trigger(self, event_name):
        handler = self._event_handlers.get(event_name)
        if handler:
            handler(self)
        else:
            print(f"No handler for {event_name}")

es = EventSystem()
es.trigger('click')  # Click event handler
es.trigger('hover')  # Hover event handler
```

---

## Practical Metaclass Uses: Attribute Validation

- Enforce constraints on class attributes
- Type checking class variables
- Format validation
- Consistency checks
- Prevent common mistakes

```python
class ValidateAttributes(type):
    def __new__(mcs, name, bases, namespace):
        # Validate attribute types
        for key, value in namespace.items():
            if key.startswith('_'):
                continue  # Skip private attributes

            if key.isupper() and not isinstance(value, (int, str, tuple, frozenset)):
                raise TypeError(f"Constant {key} must be immutable")

            if key.startswith('required_') and value is None:
                raise ValueError(f"Required attribute {key} cannot be None")

        return super().__new__(mcs, name, bases, namespace)

class Configuration(metaclass=ValidateAttributes):
    MAX_CONNECTIONS = 100  # OK - int is immutable
    DEFAULT_TIMEOUT = 30   # OK

    # Would raise TypeError - list is mutable
    # ALLOWED_TYPES = ['jpg', 'png']

    # Would raise ValueError - required field is None
    # required_api_key = None
```

---

## Practical Metaclass Uses: Automatic Property Creation

- Generate properties from attributes
- Apply validation to all properties
- Automatic getter/setter logic
- Maintain clean API and encapsulation
- Reduce boilerplate code

```python
class AutoProperties(type):
    def __new__(mcs, name, bases, namespace):
        # Find attributes to convert to properties
        property_attrs = {}
        for key, value in list(namespace.items()):
            if not key.startswith('_') and not callable(value):
                # Remove the original attribute
                del namespace[key]
                # Store for property creation
                property_attrs[key] = value

        # Create the class
        cls = super().__new__(mcs, name, bases, namespace)

        # Add properties for each attribute
        for name, default in property_attrs.items():
            # Create private attribute name
            private_name = f"_{name}"
            setattr(cls, private_name, default)

            # Create property
            setattr(cls, name, property(
                lambda self, n=private_name: getattr(self, n),
                lambda self, value, n=private_name: setattr(self, n, value)
            ))

        return cls
```

---

## Automatic Property Creation: Usage

```python
class Person(metaclass=AutoProperties):
    name = "Anonymous"
    age = 0

p = Person()
print(p.name)  # Anonymous
p.name = "Alice"
print(p.name)  # Alice
# The actual attribute is _name
print(p._name)  # Alice
```

---

## Practical Metaclass Uses: Singleton Pattern

- Ensure only one instance of a class exists
- Return existing instance if already created
- Common design pattern in many applications
- Simple to implement with metaclasses

```python
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            # Create the only instance
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnection(metaclass=Singleton):
    def __init__(self, connection_string=None):
        print(f"Initializing connection with {connection_string}")
        # Connection setup would go here

# Only initializes once
conn1 = DatabaseConnection("postgresql://localhost/db")
# Returns the same instance, doesn't re-initialize
conn2 = DatabaseConnection("other string")

print(conn1 is conn2)  # True
```

---

## Practical Metaclass Uses: Abstract Base Classes

- Enforce implementation of required methods
- Prevent instantiation of incomplete classes
- Provide interface contracts
- The `abc` module uses metaclasses

```python
from abc import ABCMeta, abstractmethod

class Vehicle(metaclass=ABCMeta):
    @abstractmethod
    def start(self):
        """Start the vehicle's engine."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the vehicle's engine."""
        pass

    def drive(self):
        """Drive the vehicle."""
        self.start()
        print("Driving")

# This would raise TypeError - can't instantiate abstract class
# car = Vehicle()

class Car(Vehicle):
    def start(self):
        print("Car engine started")

    def stop(self):
        print("Car engine stopped")

# Can instantiate complete implementation
car = Car()
car.drive()  # Car engine started \n Driving
```

---

## Practical Metaclass Uses: Custom Container Types

- Override container behavior
- Implement specialized collections
- Bridge between Python and other systems
- Add extra functionality to basic types

```python
class ContainerMeta(type):
    def __new__(mcs, name, bases, namespace):
        # Make sure required methods are defined
        if name != 'CustomContainer':  # Skip the base class
            for method in ['__getitem__', '__len__']:
                if method not in namespace:
                    raise TypeError(f"{name} must implement {method}")

        return super().__new__(mcs, name, bases, namespace)

class CustomContainer(metaclass=ContainerMeta):
    """Base class for custom containers."""
    pass

class EvenNumbers(CustomContainer):
    def __getitem__(self, index):
        return index * 2

    def __len__(self):
        return 10**10  # Virtually unlimited

evens = EvenNumbers()
print(evens[5])  # 10
print(len(evens))  # 10000000000

# This would raise TypeError - missing required methods
# class InvalidContainer(CustomContainer):
#     pass
```

---

## Metaclass Mechanisms: The `__prepare__` Method

- Called before class body execution
- Returns a dictionary-like object for namespace
- Can use custom mapping types for namespace
- Receives class name and bases tuple
- Allows ordered attributes, special mapping, etc.

```python
from collections import OrderedDict

class OrderedMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        # Return ordered dictionary to store attributes in order
        return OrderedDict()

    def __new__(mcs, name, bases, namespace):
        # Namespace is an OrderedDict, preserving definition order
        print(f"Attributes in {name} in definition order:")
        for key, value in namespace.items():
            if not key.startswith('__'):
                print(f"  {key}")

        return super().__new__(mcs, name, bases, namespace)

class MyClass(metaclass=OrderedMeta):
    # Attributes will be recorded in this order
    z = 1
    x = 2
    a = 3

    def method1(self):
        pass

    def method2(self):
        pass
```

---

## Metaclass Mechanisms: The `__call__` Method

- Called when the class is "called" to create an instance
- Controls instance creation and initialization
- Can implement special instantiation logic
- Can return completely different objects
- Separates instance creation from `__new__`/`__init__`

```python
class CallMeta(type):
    def __call__(cls, *args, **kwargs):
        print(f"Creating instance of {cls.__name__}")

        # Pre-instantiation processing
        if hasattr(cls, 'pre_instantiate'):
            cls.pre_instantiate(*args, **kwargs)

        # Create and initialize the instance
        instance = super().__call__(*args, **kwargs)

        # Post-instantiation processing
        if hasattr(cls, 'post_instantiate'):
            cls.post_instantiate(instance)

        return instance

class MyClass(metaclass=CallMeta):
    def __init__(self, x):
        self.x = x

    @classmethod
    def pre_instantiate(cls, *args, **kwargs):
        print(f"Pre-instantiation with {args}, {kwargs}")

    @classmethod
    def post_instantiate(cls, instance):
        print(f"Post-instantiation, x = {instance.x}")

obj = MyClass(42)
```

---

## Metaclass Mechanisms: Class Inheritance with Metaclasses

- Metaclasses are inherited by subclasses
- Derived class uses base class's metaclass unless specified
- Metaclass methods apply to the whole hierarchy
- Abstract base classes enforce interface through inheritance
- Enable framework-wide behavior

```python
class BaseMeta(type):
    def __new__(mcs, name, bases, namespace):
        print(f"Creating class {name} with metaclass {mcs.__name__}")

        # Apply to all classes in hierarchy
        namespace['meta_created'] = True
        return super().__new__(mcs, name, bases, namespace)

class Base(metaclass=BaseMeta):
    pass

class Child(Base):  # Inherits BaseMeta
    pass

class GrandChild(Child):  # Still inherits BaseMeta
    pass

print(Base.meta_created)        # True
print(Child.meta_created)       # True
print(GrandChild.meta_created)  # True
```

---

## Metaclass Mechanisms: Multiple Metaclasses

- A class can only have one metaclass
- Multiple inheritance can cause metaclass conflicts
- Needs a compatible metaclass hierarchy
- Custom metaclass can resolve conflicts

```python
class Meta1(type):
    pass

class Meta2(type):
    pass

class Base1(metaclass=Meta1):
    pass

class Base2(metaclass=Meta2):
    pass

# This will raise TypeError: metaclass conflict
# class Conflict(Base1, Base2):
#     pass

# Solution: create a common metaclass
class CombinedMeta(Meta1, Meta2):
    pass

# Now it works
class NoConflict(Base1, Base2, metaclass=CombinedMeta):
    pass

# Alternative: derive one metaclass from the other
class DerivedMeta(Meta1):
    pass

class Base3(metaclass=DerivedMeta):
    pass

# Works because DerivedMeta is derived from Meta1
class NoConflict2(Base1, Base3):
    pass
```

---

## Metaclass Mechanisms: Instance Creation Flow

1. `type.__call__` invokes class's `__new__`
1. `__new__` creates the instance object
1. `__init__` initializes the instance
1. The initialized instance is returned

```python
class TraceMeta(type):
    def __call__(cls, *args, **kwargs):
        print("1. metaclass __call__")
        instance = cls.__new__(cls, *args, **kwargs)

        if isinstance(instance, cls):
            print("3. calling __init__")
            instance.__init__(*args, **kwargs)

        print("4. returning instance")
        return instance

class MyClass(metaclass=TraceMeta):
    def __new__(cls, *args, **kwargs):
        print("2. class __new__")
        return super().__new__(cls)

    def __init__(self, x=None):
        print(f"    __init__ with x={x}")
        self.x = x

obj = MyClass(42)
# 1. metaclass __call__
# 2. class __new__
# 3. calling __init__
#     __init__ with x=42
# 4. returning instance
```

---

## Creating DSLs with Metaclasses: Domain-Specific Languages

- Custom syntax for specific domains
- More readable and expressive than general code
- Built on top of the host language
- Metaclasses can transform declarations into behavior
- Make complex frameworks more user-friendly

```python
# Example goal: create a simple ORM DSL
class User(Model):
    name = String(max_length=100)
    email = String(max_length=100, unique=True)
    age = Integer(min_value=0)

    def __str__(self):
        return self.name

# Metaclass will transform these declarations into
# database fields, validation logic, etc.
```

---

## Creating DSLs with Metaclasses: A Simple ORM Example

- Define fields as class attributes
- Metaclass converts field definitions to properties
- Handles validation, serialization, etc.
- Creates clean, declarative syntax

```python
class Field:
    def __init__(self, **kwargs):
        self.name = None
        self.attributes = kwargs

    def __set__(self, instance, value):
        instance._data[self.name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._data.get(self.name)

class String(Field):
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        max_length = self.attributes.get('max_length')
        if max_length and len(value) > max_length:
            raise ValueError(f"{self.name} cannot exceed {max_length} characters")
        super().__set__(instance, value)

class Integer(Field):
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be an integer")
        min_value = self.attributes.get('min_value')
        if min_value is not None and value < min_value:
            raise ValueError(f"{self.name} must be at least {min_value}")
        super().__set__(instance, value)
```

---

## Creating DSLs with Metaclasses: Model Metaclass

- Collects field definitions
- Sets up field attributes
- Creates database connection
- Handles model operations

```python
class ModelMeta(type):
    def __new__(mcs, name, bases, namespace):
        if name == 'Model':  # Skip the base Model class
            return super().__new__(mcs, name, bases, namespace)

        # Collect fields
        fields = {}
        for key, value in namespace.items():
            if isinstance(value, Field):
                value.name = key
                fields[key] = value

        # Add the fields to a class attribute
        namespace['_fields'] = fields

        # Create the class
        cls = super().__new__(mcs, name, bases, namespace)

        # Generate table name
        cls._table_name = name.lower() + 's'

        return cls
```

---

## Model Metaclass: Base Model Class

```python
class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        self._data = {}

        # Set initial values
        for key, value in kwargs.items():
            if key in self._fields:
                setattr(self, key, value)

    def save(self):
        print(f"Saving {self.__class__.__name__} to table {self._table_name}")
        for name, field in self._fields.items():
            print(f"  {name}: {getattr(self, name)}")
```

---

## Creating DSLs with Metaclasses: Using the ORM

- Clean, declarative syntax
- Strong validation
- Easy to understand structure
- Domain-specific behavior

```python
class User(Model):
    name = String(max_length=100)
    email = String(max_length=100)
    age = Integer(min_value=0)

# Create a user
user = User(name="Alice", email="alice@example.com", age=30)
user.save()
# Output:
# Saving User to table users
#   name: Alice
#   email: alice@example.com
#   age: 30

# Validation in action
try:
    user.age = -5  # Below min_value
except ValueError as e:
    print(f"Validation error: {e}")

try:
    user.name = 123  # Not a string
except TypeError as e:
    print(f"Validation error: {e}")
```

---

## Creating DSLs with Metaclasses: State Machine DSL Example

- Define states and transitions
- Metaclass creates the state behavior
- Clean representation of complex logic
- Self-documenting behavior

```python
class StateMachineMeta(type):
    def __new__(mcs, name, bases, namespace):
        if name == 'StateMachine':  # Skip the base class
            return super().__new__(mcs, name, bases, namespace)

        # Extract states and transitions
        states = {}
        transitions = {}
        for key, value in namespace.items():
            if key.startswith('state_'):
                state_name = key[6:]  # Remove 'state_' prefix
                states[state_name] = value
            elif key.startswith('transition_'):
                transition_name = key[11:]  # Remove 'transition_' prefix
                transitions[transition_name] = value

        # Add to namespace
        namespace['_states'] = states
        namespace['_transitions'] = transitions
        namespace['_current_state'] = list(states.keys())[0]  # Default to first state

        return super().__new__(mcs, name, bases, namespace)
```

---

## State Machine DSL: Base `StateMachine` Class

```python
class StateMachine(metaclass=StateMachineMeta):
    def get_state(self):
        return self._current_state

    def can_transition(self, transition):
        if transition not in self._transitions:
            return False
        return self._transitions[transition](self)

    def transition(self, transition):
        if not self.can_transition(transition):
            raise ValueError(f"Cannot transition '{transition}' from state '{self._current_state}'")

        # Get next state from transition function
        next_state = self._transitions[transition](self)
        print(f"Transitioning from '{self._current_state}' to '{next_state}'")
        self._current_state = next_state

        # Run state entry function
        state_func = self._states.get(self._current_state)
        if state_func:
            state_func(self)
```

---

## Creating DSLs with Metaclasses: Using the State Machine DSL

- Clean representation of states
- Self-enforcing state constraints
- Easy to understand and modify
- Domain-specific language for state flow

```python
class TrafficLight(StateMachine):
    def state_red(self):
        print("Red light - Stop!")

    def state_yellow(self):
        print("Yellow light - Prepare to stop!")

    def state_green(self):
        print("Green light - Go!")

    def transition_change(self):
        # Define state transitions
        if self._current_state == 'red':
            return 'green'
        elif self._current_state == 'green':
            return 'yellow'
        elif self._current_state == 'yellow':
            return 'red'

# Use the state machine
light = TrafficLight()
print(light.get_state())  # red - the first defined state
light.transition('change')  # Transitioning from 'red' to 'green' \n Green light - Go!
light.transition('change')  # Transitioning from 'green' to 'yellow' \n Yellow light - Prepare to stop!
light.transition('change')  # Transitioning from 'yellow' to 'red' \n Red light - Stop!
```

---

## Examples from Third-Party Libraries: Django Models

- One of the most popular Python ORMs
- Uses metaclasses for field registration
- Declarative model definition
- Automatic database handling

```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

# Django's ModelBase metaclass transforms these declarations
# into database operations, validation, and more

# Behind the scenes, this creates a table with columns for
# each field, manages migrations, sets up querysets, etc.
article = Article(title="Metaclasses in Python", content="...")
article.save()  # Inserts into database
```

---

## Examples from Third-Party Libraries: SQLAlchemy Declarative

- Powerful Python ORM
- Uses metaclasses for declarative models
- Maps classes to database tables
- Strong typing and validation

```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///example.db')
Base = declarative_base()  # Returns a class with a metaclass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

# Create tables
Base.metadata.create_all(engine)

# Use the model
Session = sessionmaker(bind=engine)
session = Session()
user = User(name="Alice", email="alice@example.com")
session.add(user)
session.commit()
```

---

## Examples from Third-Party Libraries: Pydantic Models

- Data validation and settings management
- Uses metaclasses for field processing
- Type checking and conversion
- JSON schema generation

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: str
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = None

# Data validation and type conversion happens automatically
user_data = {
    "id": "123",  # Note: string, will be converted to int
    "name": "Alice",
    "email": "alice@example.com",
    "tags": ["admin", "user"]
}

user = User(**user_data)
print(user.id)  # 123 (as int, not string)
print(user.dict())  # Full model as dict
print(user.json())  # JSON representation
```

---

## Examples from Third-Party Libraries: Enum Metaclass

- Python's standard library
- Creates enum classes
- Manages enum member creation
- Restricts instantiation

```python
import enum

# The EnumMeta metaclass handles the enum creation
class Color(enum.Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

    def describe(self):
        return f"This color is {self.name.lower()}"

# Usage
print(Color.RED)           # Color.RED
print(Color.RED.name)      # RED
print(Color.RED.value)     # 1
print(Color.RED.describe())  # This color is red

# Iteration
for color in Color:
    print(color)  # Color.RED, Color.GREEN, Color.BLUE

# Lookup
print(Color(1))      # Color.RED (by value)
print(Color['RED'])  # Color.RED (by name)
```

---

## Examples from Third-Party Libraries: ABCs in Collections

- Python's collections.abc module
- Abstract base classes for containers
- Virtual subclasses with __subclasshook__
- Duck typing with structural interface checks

```python
from collections.abc import Sequence, Mapping

# These are created with metaclasses
print(type(Sequence))  # <class 'abc.ABCMeta'>
print(type(Mapping))   # <class 'abc.ABCMeta'>

# Regular list is a virtual subclass of Sequence
print(isinstance([], Sequence))  # True
print(issubclass(list, Sequence))  # True

# Regular dict is a virtual subclass of Mapping
print(isinstance({}, Mapping))  # True
print(issubclass(dict, Mapping))  # True

# Create a custom sequence
class MySequence:
    def __getitem__(self, index):
        pass
    def __len__(self):
        pass

# Due to __subclasshook__, this is recognized as a sequence
print(isinstance(MySequence(), Sequence))  # True
```

---

## Examples from Third-Party Libraries: Attrs and Dataclasses

- Automated class building
- Metaclass-like functionality
- Field definitions and processing
- Reduces boilerplate

```python
import attr
from dataclasses import dataclass

# Attrs uses class decorators but performs similar tasks to metaclasses
@attr.s
class AttrsPoint:
    x = attr.ib(default=0)
    y = attr.ib(default=0)

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

# Dataclasses use a decorator but transform the class similar to metaclasses
@dataclass
class DataPoint:
    x: float = 0
    y: float = 0

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

p1 = AttrsPoint(3, 4)
p2 = DataPoint(3, 4)
print(p1)  # AttrsPoint(x=3, y=4)
print(p2)  # DataPoint(x=3, y=4)
```

---

## Best Practices: When to Use Metaclasses

- Only when simpler approaches won't work
- For library and framework development
- When you need to control class creation
- For declarative APIs and DSLs
- When behavior needs to apply to all subclasses

```python
"""
Alternative approaches to try before metaclasses:

1. Regular class inheritance
2. Composition (has-a instead of is-a)
3. Class decorators
4. Descriptors
5. Mixins
6. Function decorators

Metaclasses should be your last resort, not your first approach.
"""
```

---

## Best Practices: Common Pitfalls

- Overcomplicating simple problems
- Making code hard to understand
- Creating unexpected behavior
- Breaking standard patterns
- Performance overhead
- Inheritance conflicts

```python
# Pitfall: overly complex solution
class ValidatedMeta(type):
    def __new__(mcs, name, bases, namespace):
        for key, value in namespace.items():
            if key.startswith('validate_'):
                # Setup complex validation
                pass
        return super().__new__(mcs, name, bases, namespace)

# Better solution: descriptors or properties
class BetterSolution:
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value
```

---

## Best Practices: Metaclass Debugging

- Meta-level code is often harder to debug
- Print statements in metaclass methods
- Inspect the class creation process
- Check class attributes after creation
- Use `__prepare__` for diagnostics

```python
class DebugMeta(type):
    @classmethod
    def __prepare__(mcs, name, bases):
        print(f"Preparing namespace for {name}")
        return dict()

    def __new__(mcs, name, bases, namespace):
        print(f"Creating class {name}")
        print(f"Attributes: {list(namespace.keys())}")
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

    def __init__(cls, name, bases, namespace):
        print(f"Initializing class {name}")
        super().__init__(name, bases, namespace)

class MyClass(metaclass=DebugMeta):
    x = 1

    def method(self):
        pass
```

---

## Summary

## Key Takeaways
- Metaclasses are classes that create classes
- They allow customizing class creation and behavior
- Useful for frameworks, DSLs, and declarative APIs
- Many Python libraries use metaclasses under the hood
- Use simpler approaches when possible
- Metaclasses add complexity but enable powerful patterns

---

## Resources

## Further Reading
- Python documentation on metaclasses
- "Python Cookbook" by David Beazley and Brian Jones
- "Fluent Python" by Luciano Ramalho
- "Expert Python Programming" by Michał Jaworski
- Django and SQLAlchemy documentation
- Raymond Hettinger's talks on metaclasses
