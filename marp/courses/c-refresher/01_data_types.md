# C Data Types Refresher

---

## Basic Data Types in C

C provides several basic data types:

- Integer types
- Floating-point types
- Character type
- Void type

---

## Integer Types

- Used to store whole numbers
- Various sizes available:
  - `char`: 1 byte
  - `short`: 2 bytes
  - `int`: 2 or 4 bytes (usually 4)
  - `long`: 4 or 8 bytes
  - `long long`: 8 bytes (C99 and later)

```c
int a = 10;
long long big_num = 1234567890123456789LL;
```

---

## Integer Modifiers

- `signed`: Can represent positive and negative numbers (default)
- `unsigned`: Can only represent non-negative numbers

```c
unsigned int positive = 4294967295U;
signed char small = -128;
```

---

## Floating-Point Types

- Used to store decimal numbers
- Three types available:
  - `float`: Single precision (4 bytes)
  - `double`: Double precision (8 bytes)
  - `long double`: Extended precision (at least 10 bytes, often 16)

```c
float pi = 3.14159F;
double e = 2.71828;
long double big_pi = 3.141592653589793238L;
```

---

## Character Type

- Used to store a single character
- Typically 1 byte in size
- Represented by `char`

```c
char grade = 'A';
char newline = '\n';
```

---

## Void Type

- Represents the absence of a value
- Used in three ways:
    1. Function returns nothing
    1. Function takes no parameters
    1. Generic pointer type

```c
void print_hello(void) {
    printf("Hello, World!\n");
}

void *generic_ptr;
```

---

## Derived Data Types

C also provides several derived data types:

- Arrays
- Pointers
- Structures
- Unions
- Enumerations

---

## Arrays

- Collection of elements of the same type
- Index-based access (starting from 0)

```c
int numbers[5] = {1, 2, 3, 4, 5};
char name[] = "John";  // Null-terminated string
```

---

## Pointers

- Store memory addresses of variables
- Declared using the `*` operator

```c
int x = 10;
int *ptr = &x;
printf("Value of x: %d\n", *ptr);  // Dereference
```

---

## Structures

- Group related data of different types
- Defined using the `struct` keyword

```c
struct Point {
    int x;
    int y;
};

struct Point p1 = {10, 20};
```

---

## Unions

- Store different data types in the same memory location
- Only one member can hold a value at a time

```c
union Data {
    int i;
    float f;
    char str[20];
};

union Data data;
data.i = 10;
```

---

## Enumerations

- User-defined type consisting of named integer constants
- Defined using the `enum` keyword

```c
enum Days {MON, TUE, WED, THU, FRI, SAT, SUN};
enum Days today = WED;
```

---

## Type Qualifiers

- `const`: Value cannot be changed after initialization
- `volatile`: Value may change unexpectedly
- `restrict`: Pointer is the only way to access an object (C99)

```c
const int MAX_SIZE = 100;
volatile int sensor_value;
int *restrict ptr = malloc(sizeof(int));
```

---

## Type Conversion

- Implicit conversion: Automatically done by the compiler
- Explicit conversion: Done by the programmer using typecasting

```c
int i = 10;
float f = 3.14;
double d = (double)i + f;  // Explicit conversion of i to double
```

---

## sizeof Operator

- Returns the size of a data type in bytes
- Useful for portable code and dynamic memory allocation

```c
printf("Size of int: %zu bytes\n", sizeof(int));
printf("Size of float: %zu bytes\n", sizeof(float));
```

---

## Summary

- C provides basic types: integers, floating-point, characters, and void
- Derived types include arrays, pointers, structures, unions, and enums
- Use appropriate types based on the data and operations needed
- Be aware of type sizes and conversions for efficient and correct code
