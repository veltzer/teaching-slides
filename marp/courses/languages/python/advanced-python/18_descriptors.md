---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---
# Python Descriptors

## Overview
- What are descriptors?
- The descriptor protocol
- Types of descriptors
- Writing your own descriptors
- Real-world applications
- Examples from third-party modules

---

## What Are Descriptors?: Definition

- Objects that implement the descriptor protocol
- A way to customize attribute access in classes
- Enable powerful control over attribute behavior
- Foundation for Python's attribute system
- Core feature for many Python language features

```python
# Many Python features are implemented using descriptors:
# - Properties
# - Methods
# - Class methods
# - Static methods
# - Slots
```

---

## What Are Descriptors?: The Descriptor Protocol

- Implement at least one of these methods:
    - `__get__(self, obj, type=None)`: Called when attribute is accessed
    - `__set__(self, obj, value)`: Called when attribute is assigned
    - `__delete__(self, obj)`: Called when attribute is deleted
- Objects implementing `__get__` and `__set__` are data descriptors
- Objects implementing only `__get__` are non-data descriptors

```python
class MyDescriptor:
    def __get__(self, obj, objtype=None):
        return "Getting attribute"

    def __set__(self, obj, value):
        print(f"Setting attribute to {value}")

    def __delete__(self, obj):
        print("Deleting attribute")
```

---

## What Are Descriptors?: How Descriptors Work

- Descriptors are class attributes
- When accessed through an instance, descriptor protocol is invoked
- Python looks for descriptor methods during attribute access
- Priority chain for attribute lookup:
    1. Data descriptors (with `__set__` and/or `__delete__`)
    1. Instance variables in `__dict__`
    1. Non-data descriptors (only `__get__`)
    1. Class variables

```python
class MyClass:
    descriptor = MyDescriptor()  # Class attribute

obj = MyClass()
obj.descriptor       # Calls MyDescriptor.__get__(descriptor, obj, MyClass)
obj.descriptor = 42  # Calls MyDescriptor.__set__(descriptor, obj, 42)
del obj.descriptor   # Calls MyDescriptor.__delete__(descriptor, obj)
```

---

## Descriptor Protocol: Lookup Chain and Priority

![descriptor_protocol](svg/courses/languages/python/advanced-python/18_descriptors/descriptor_protocol.svg)

---

## Types of Descriptors: Data vs. Non-Data Descriptors

- **Data descriptors**: Implement `__set__` and/or `__delete__`
    - Take precedence over instance attributes
    - Cannot be overridden by instance attributes
    - Examples: properties, slots
- **Non-data descriptors**: Implement only `__get__`
    - Lower priority than instance attributes
    - Can be overridden by instance attributes
    - Examples: methods, classmethods, staticmethods

```python
class NonDataDescriptor:
    def __get__(self, obj, objtype=None):
        return "Non-data descriptor"

class DataDescriptor:
    def __get__(self, obj, objtype=None):
        return "Data descriptor"
    def __set__(self, obj, value):
        print(f"Setting {value}")
```

---

## Types of Descriptors: Descriptor Behaviors

- **Read-Only**: Implement `__get__` but not `__set__`
- **Computed Values**: Generate values dynamically in `__get__`
- **Validated Attributes**: Check values in `__set__`
- **Custom Storage**: Store values outside instance `__dict__`
- **Event Triggers**: Execute code on access or modification
- **Lazy Evaluation**: Compute values only when needed

```python
# Read-Only Descriptor
class Constant:
    def __init__(self, value):
        self.value = value

    def __get__(self, obj, objtype=None):
        return self.value

# In class:
# PI = Constant(3.14159)
```

---

## Methods as Descriptors: Functions as Descriptors

- Regular instance methods are descriptors
- Implement `__get__` method only
- `__get__` returns a bound method when accessed from instance
- `__get__` returns the function itself when accessed from class

```python
# Simplified explanation of how methods work:
class Function:
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self  # Accessed from class
        return BoundMethod(self, obj)  # Accessed from instance

class BoundMethod:
    def __init__(self, function, instance):
        self.function = function
        self.instance = instance

    def __call__(self, *args, **kwargs):
        return self.function(self.instance, *args, **kwargs)
```

---

## Methods as Descriptors: Method Types

- **Instance Methods**: First parameter is `self`
- **Class Methods**: First parameter is `cls`, uses `@classmethod`
- **Static Methods**: No special first parameter, uses `@staticmethod`

```python
class Example:
    # Instance method (non-data descriptor)
    def instance_method(self, arg):
        return f"Instance {self} got {arg}"

    # Class method (non-data descriptor)
    @classmethod
    def class_method(cls, arg):
        return f"Class {cls.__name__} got {arg}"

    # Static method (non-data descriptor)
    @staticmethod
    def static_method(arg):
        return f"Got {arg}"
```

---

## Properties as Descriptors: Property Basics

- Built-in way to create managed attributes
- A data descriptor that calls user-provided functions
- Provides getter, setter, deleter, and doc options
- Allows attribute-like access to computed values

```python
class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        """Name property docstring"""
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value

    @name.deleter
    def name(self):
        del self._name
```

---

## Properties as Descriptors: Property Implementation

- `property` is a class that implements the descriptor protocol
- Creates a descriptor instance with provided functions
- Simplified implementation:

```python
class Property:
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or (fget and fget.__doc__)

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)
```

---

## Writing Your Own Descriptors: Basic Descriptor Structure

- Define a class with descriptor protocol methods
- Store descriptor instances as class variables
- Handle attribute storage and access
- Follow suitable naming conventions

```python
class Validator:
    def __init__(self, name=None):
        self.name = name  # Attribute name

    def __set_name__(self, owner, name):
        # This is called when descriptor is defined in a class
        if self.name is None:
            self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, None)

    def __set__(self, obj, value):
        self.validate(value)
        obj.__dict__[self.name] = value

    def validate(self, value):
        # To be implemented by subclasses
        pass
```

---

## Writing Your Own Descriptors: Attribute Storage Options

- **Instance `__dict__`**: Most common approach
- **Descriptor instance**: Store values in descriptor
- **Separate storage**: Use another object or mapping
- **Weakref dictionary**: Avoid memory leaks
- **Private naming**: Use mangled names to avoid collisions

```python
# Instance dictionary storage
def __set__(self, obj, value):
    obj.__dict__[self.name] = value

# Descriptor instance storage (problematic!)
def __set__(self, obj, value):
    self.value = value  # Shared across all instances!

# Separate storage
def __set__(self, obj, value):
    storage = getattr(obj, '_storage', {})
    storage[self.name] = value
    obj._storage = storage
```

---

## Writing Your Own Descriptors: The `__set_name__` Method

- Introduced in Python 3.6
- Automatically called when descriptor is created in class
- Provides descriptor with its attribute name and owner class
- Eliminates need for explicit name parameter
- Simplifies descriptor usage

```python
class AutoNamed:
    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name, None)

    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)

class Person:
    # Name automatically set by __set_name__
    first_name = AutoNamed()
    last_name = AutoNamed()
```

---

## Writing Your Own Descriptors: Type Validation Descriptor

- Enforce type constraints on attributes
- Raise errors for invalid values
- Provide clear error messages
- Support multiple types

```python
class Typed:
    def __init__(self, *types):
        self.types = types
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, None)

    def __set__(self, obj, value):
        if not isinstance(value, self.types):
            type_names = [t.__name__ for t in self.types]
            raise TypeError(f"{self.name} must be of type: {' or '.join(type_names)}")
        obj.__dict__[self.name] = value

class Person:
    name = Typed(str)
    age = Typed(int)
    height = Typed(int, float)
```

---

## Writing Your Own Descriptors: Range Validation Descriptor

- Enforce value ranges on numeric attributes
- Combine with type validation
- Support minimum and maximum values
- Useful for configuration settings

```python
class Ranged:
    def __init__(self, minimum=None, maximum=None):
        self.minimum = minimum
        self.maximum = maximum
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, None)

    def __set__(self, obj, value):
        if self.minimum is not None and value < self.minimum:
            raise ValueError(f"{self.name} must be at least {self.minimum}")
        if self.maximum is not None and value > self.maximum:
            raise ValueError(f"{self.name} must be at most {self.maximum}")
        obj.__dict__[self.name] = value

class Settings:
    timeout = Ranged(0, 60)
    max_connections = Ranged(1, 100)
    retry_count = Ranged(0, 10)
```

---

## Writing Your Own Descriptors: Combining Descriptors

- Create descriptor factories
- Combine multiple validation rules
- Use composition or inheritance
- Build descriptor toolkits
- Create domain-specific validators

```python
class Field:
    def __init__(self, *validators):
        self.validators = validators
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, None)

    def __set__(self, obj, value):
        for validator in self.validators:
            validator(self.name, value)
        obj.__dict__[self.name] = value

def type_validator(*types):
    def validate(name, value):
        if not isinstance(value, types):
            type_names = [t.__name__ for t in types]
            raise TypeError(f"{name} must be of type: {' or '.join(type_names)}")
    return validate

def range_validator(minimum=None, maximum=None):
    def validate(name, value):
        if minimum is not None and value < minimum:
            raise ValueError(f"{name} must be at least {minimum}")
        if maximum is not None and value > maximum:
            raise ValueError(f"{name} must be at most {maximum}")
    return validate

class Person:
    name = Field(type_validator(str))
    age = Field(type_validator(int), range_validator(0, 120))
```

---

## Writing Your Own Descriptors: Lazy Properties

- Compute values only when needed
- Cache results for future access
- Reset cache when dependencies change
- Save computation time for expensive operations

```python
class LazyProperty:
    def __init__(self, function):
        self.function = function
        self.name = function.__name__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        # Compute value and cache in instance dictionary
        value = self.function(obj)
        obj.__dict__[self.name] = value
        return value

class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    @LazyProperty
    def average(self):
        print("Computing average...")
        return sum(self.data) / len(self.data)

    @LazyProperty
    def maximum(self):
        print("Computing maximum...")
        return max(self.data)
```

---

## Writing Your Own Descriptors: Unit Conversion Descriptor

- Automatic unit conversion
- Store in canonical units
- Present in user-preferred units
- Support multiple unit systems
- Used in scientific computing

```python
class Distance:
    def __init__(self):
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        # Get value in meters
        meters = obj.__dict__.get(self.name, 0)

        # Convert to user's preferred unit
        unit = getattr(obj, 'unit', 'meters')
        if unit == 'meters':
            return meters
        elif unit == 'feet':
            return meters * 3.28084
        elif unit == 'yards':
            return meters * 1.09361
        elif unit == 'miles':
            return meters * 0.000621371

    def __set__(self, obj, value):
        # Convert from user's unit to meters
        unit = getattr(obj, 'unit', 'meters')
        if unit == 'meters':
            meters = value
        elif unit == 'feet':
            meters = value / 3.28084
        elif unit == 'yards':
            meters = value / 1.09361
        elif unit == 'miles':
            meters = value / 0.000621371

        obj.__dict__[self.name] = meters

class Trip:
    distance = Distance()

    def __init__(self, distance=0, unit='meters'):
        self.unit = unit
        self.distance = distance
```

---

## Writing Your Own Descriptors: Log Access Descriptor

- Monitor attribute access
- Record changes to attributes
- Audit sensitive operations
- Debug complex attribute interactions
- Create activity logs

```python
class LoggedAttribute:
    def __init__(self, name=None, logging_function=None):
        self.name = name
        self.logging_function = logging_function or print

    def __set_name__(self, owner, name):
        if self.name is None:
            self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        value = obj.__dict__.get(self.name, None)
        self.logging_function(f"Accessing {self.name}: {value}")
        return value

    def __set__(self, obj, value):
        old_value = obj.__dict__.get(self.name, None)
        self.logging_function(f"Setting {self.name}: {old_value} -> {value}")
        obj.__dict__[self.name] = value

class BankAccount:
    balance = LoggedAttribute()

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount
```

---

## Real-World Applications: Form Validation

- Validate user input in web forms
- Apply multiple validation rules
- Generate appropriate error messages
- Create self-validating models
- Similar to Django's form fields

```python
class FormField:
    def __init__(self, required=True, validators=None):
        self.required = required
        self.validators = validators or []
        self.name = None
        self.errors = []

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, None)

    def __set__(self, obj, value):
        self.errors = []

        # Check if required
        if self.required and (value is None or value == ''):
            self.errors.append(f"{self.name} is required")

        # Run validators
        for validator in self.validators:
            try:
                validator(value)
            except Exception as e:
                self.errors.append(str(e))

        # Only set if valid
        if not self.errors:
            obj.__dict__[self.name] = value

    def is_valid(self, obj):
        return not self.errors

# Example validators
def email_validator(value):
    if '@' not in value:
        raise ValueError("Invalid email format")

def length_validator(min_length, max_length):
    def validate(value):
        if len(value) < min_length:
            raise ValueError(f"Must be at least {min_length} characters")
        if len(value) > max_length:
            raise ValueError(f"Must be at most {max_length} characters")
    return validate

class RegistrationForm:
    username = FormField(validators=[length_validator(3, 20)])
    email = FormField(validators=[email_validator])
    password = FormField(validators=[length_validator(8, 50)])

    def is_valid(self):
        return all(
            field.is_valid(self)
            for name, field in vars(self.__class__).items()
            if isinstance(field, FormField)
        )
```

---

## Real-World Applications: ORM Models

- Object-Relational Mapping systems
- Map class attributes to database columns
- Enforce data types and constraints
- Generate schema and queries
- Used in Django, SQLAlchemy, etc.

```python
class Column:
    def __init__(self, column_type, primary_key=False, nullable=True):
        self.column_type = column_type
        self.primary_key = primary_key
        self.nullable = nullable
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, None)

    def __set__(self, obj, value):
        if value is None and not self.nullable:
            raise ValueError(f"{self.name} cannot be NULL")

        if value is not None and not isinstance(value, self.column_type):
            raise TypeError(f"{self.name} must be of type {self.column_type.__name__}")

        obj.__dict__[self.name] = value

class Model:
    @classmethod
    def columns(cls):
        return {
            name: attr for name, attr in vars(cls).items()
            if isinstance(attr, Column)
        }

class User(Model):
    id = Column(int, primary_key=True)
    username = Column(str, nullable=False)
    email = Column(str, nullable=False)
    age = Column(int)

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
```

---

## Real-World Applications: Configuration Systems

- Define configuration parameters
- Apply validation rules
- Support default values
- Convert string inputs to appropriate types
- Used in settings management

```python
class ConfigParam:
    def __init__(self, type=None, default=None, choices=None, help=""):
        self.type = type
        self.default = default
        self.choices = choices
        self.help = help
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        value = obj.__dict__.get(self.name, self.default)
        return value

    def __set__(self, obj, value):
        # Type conversion if needed
        if self.type and not isinstance(value, self.type):
            try:
                value = self.type(value)
            except Exception:
                raise TypeError(f"{self.name} must be convertible to {self.type.__name__}")

        # Validate choices
        if self.choices and value not in self.choices:
            raise ValueError(f"{self.name} must be one of: {', '.join(str(c) for c in self.choices)}")

        obj.__dict__[self.name] = value

class AppConfig:
    debug = ConfigParam(bool, default=False, help="Enable debug mode")
    log_level = ConfigParam(str, default="INFO",
                          choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                          help="Logging level")
    max_connections = ConfigParam(int, default=10, help="Maximum concurrent connections")

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self.__class__, key):
                setattr(self, key, value)
            else:
                raise AttributeError(f"Unknown configuration parameter: {key}")

    @classmethod
    def from_dict(cls, config_dict):
        return cls(**config_dict)

    @classmethod
    def from_file(cls, filename):
        # Load config from file (e.g., JSON, YAML, INI)
        import json
        with open(filename, 'r') as f:
            config_dict = json.load(f)
        return cls.from_dict(config_dict)
```

---

## Examples from Third-Party Modules: Django Model Fields

- Django ORM uses descriptors for model fields
- Each field type is a descriptor
- Handles database conversion
- Validates input data
- Manages relationships between models

```python
from django.db import models

class Product(models.Model):
    # Each field is a descriptor
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
```

---

## Examples from Third-Party Modules: SQLAlchemy ORM

- Uses descriptors for column definitions
- Manages relationships between tables
- Handles database dialect differences
- Provides query building interface
- One of the most advanced descriptor uses

```python
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    # Each column is a descriptor
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)

    # Relationship is also a descriptor
    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"<User(name='{self.name}', fullname='{self.fullname}', nickname='{self.nickname}')>"

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"<Address(email_address='{self.email_address}')>"
```

---

## Examples from Third-Party Modules: Python-attrs Library

- Uses descriptors for attribute management
- Automatically generates special methods
- Supports validation and conversion
- Type checking and default values
- A cleaner alternative to dataclasses

```python
import attr

@attr.s
class Point:
    # Each attribute is a descriptor
    x = attr.ib(type=float, default=0.0)
    y = attr.ib(type=float, default=0.0)

    @y.validator
    def check_y(self, attribute, value):
        if value < 0:
            raise ValueError("y must be positive")

    def distance_from_origin(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

# Usage
p = Point(3.0, 4.0)
print(p)  # Point(x=3.0, y=4.0)
print(p.distance_from_origin())  # 5.0
```

---

## Examples from Third-Party Modules: Pydantic

- Data validation library using descriptors
- Type annotations as validation rules
- JSON schema generation
- Used in FastAPI and other frameworks
- Modern approach to descriptors

```python
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    signup_ts: Optional[datetime] = None
    friends: List[int] = []

    # Validator for name
    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v:
            raise ValueError('must contain a space')
        return v.title()

    # Validator for friends
    @validator('friends')
    def friends_check(cls, v):
        if len(v) > 100:
            raise ValueError('too many friends')
        return v

# Usage
user = User(id=1, name='john doe', friends=[1, 2, 3])
print(user.dict())
# {'id': 1, 'name': 'John Doe', 'signup_ts': None, 'friends': [1, 2, 3]}
```

---

## Summary

## Key Takeaways
- Descriptors provide a powerful way to customize attribute access
- Foundation for many Python language features
- Useful for validation, computed properties, and more
- Enable clean, declarative programming styles
- Used extensively in ORMs and data validation libraries
- Build reusable, composable attribute behaviors

---

## Further Reading

## Resources
- Python documentation on descriptors
- "Python Cookbook" by David Beazley and Brian Jones
- "Fluent Python" by Luciano Ramalho
- Descriptor HowTo Guide in Python docs
- Source code for Django models, SQLAlchemy ORM
- Raymond Hettinger's talks on descriptors
