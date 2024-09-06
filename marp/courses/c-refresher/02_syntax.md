# C Syntax Refresher

---

## Basic Program Structure

A simple C program consists of:

```c
#include <stdio.h>

int main() {
    // Your code here
    return 0;
}
```

- `#include`: Preprocessor directive
- `main()`: Entry point of the program
- `{}`: Block of code
- `return 0;`: Indicates successful program execution

---

## Comments

- Single-line comments: `// This is a comment`
- Multi-line comments: `/* This is a multi-line comment */`

```c
// This is a single-line comment

/* This is a
   multi-line comment */
```

---

## Variables and Constants

- Variables: `type name = value;`
- Constants: `const type NAME = value;`

```c
int age = 25;
const float PI = 3.14159;
```

---

## Data Types

Basic data types:
- `int`: Integer
- `float`: Single-precision floating-point
- `double`: Double-precision floating-point
- `char`: Single character

```c
int count = 10;
float price = 9.99;
char grade = 'A';
```

---

## Operators

- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `&&` (AND), `||` (OR), `!` (NOT)
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`

```c
int a = 5, b = 3;
int sum = a + b;
int is_equal = (a == b);
```

---

## Control Structures: if-else

```c
if (condition) {
    // Code to execute if condition is true
} else if (another_condition) {
    // Code to execute if another_condition is true
} else {
    // Code to execute if all conditions are false
}
```

Example:
```c
if (score >= 90) {
    printf("Grade: A");
} else if (score >= 80) {
    printf("Grade: B");
} else {
    printf("Grade: C");
}
```

---

## Control Structures: switch

```c
switch (expression) {
    case constant1:
        // Code to execute for constant1
        break;
    case constant2:
        // Code to execute for constant2
        break;
    default:
        // Code to execute if no match is found
}
```

Example:
```c
switch (day) {
    case 1:
        printf("Monday");
        break;
    case 2:
        printf("Tuesday");
        break;
    default:
        printf("Other day");
}
```

---

## Loops: for

```c
for (initialization; condition; update) {
    // Code to repeat
}
```

Example:
```c
for (int i = 0; i < 5; i++) {
    printf("%d ", i);
}
```

---

## Loops: while and do-while

While loop:
```c
while (condition) {
    // Code to repeat
}
```

Do-while loop:
```c
do {
    // Code to repeat
} while (condition);
```

Example:
```c
int i = 0;
while (i < 5) {
    printf("%d ", i);
    i++;
}
```

---

## Functions

Function declaration and definition:
```c
return_type function_name(parameter_list) {
    // Function body
    return value;
}
```

Example:
```c
int add(int a, int b) {
    return a + b;
}

int result = add(5, 3);
```

---

## Arrays

Declaration and initialization:
```c
type array_name[size];
type array_name[] = {value1, value2, ...};
```

Example:
```c
int numbers[5] = {1, 2, 3, 4, 5};
char name[] = "John";
```

---

## Pointers

Declaration and usage:
```c
type *pointer_name;
pointer_name = &variable;
```

Example:
```c
int x = 10;
int *ptr = &x;
printf("Value of x: %d", *ptr);
```

---

## Structures

Definition and usage:
```c
struct structure_name {
    type member1;
    type member2;
    // ...
};

struct structure_name variable_name;
```

Example:
```c
struct Person {
    char name[50];
    int age;
};

struct Person p1 = {"Alice", 30};
```

---

## Preprocessor Directives

- `#include`: Include header files
- `#define`: Define macros or constants
- `#ifdef`, `#ifndef`, `#endif`: Conditional compilation

Example:
```c
#include <stdio.h>
#define MAX_SIZE 100

#ifdef DEBUG
    printf("Debug mode on");
#endif
```

---

## Summary

- C programs have a specific structure with the `main()` function as the entry point
- Variables and constants store data, with various data types available
- Control structures (`if-else`, `switch`) and loops (`for`, `while`) control program flow
- Functions encapsulate reusable code
- Arrays store collections of data, and pointers handle memory addresses
- Structures group related data of different types
- Preprocessor directives handle file inclusion and macro definitions
