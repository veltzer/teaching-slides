# C Programming Review

---

## Introduction to C

- Developed by Dennis Ritchie at Bell Labs in 1972
- Widely used in embedded systems, operating systems, and application development
- Known for efficiency and low-level control

---

## C Standards

- C89/C90: First standardized version
- C99: Added new features like inline functions, variable-length arrays
- C11: Added multi-threading support, anonymous structures
- C17: Bug fixes and clarifications

---

## Basic C Program Structure

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("Hello, World!\n");
    return EXIT_SUCCESS;
}
```

Compile and run:
```
gcc hello.c -o hello
./hello
```

---

## Comments in C

```c
// This is a single-line comment

/*
   This is a
   multi-line comment
*/
```

---

## Variables and Data Types

```c
int age = 30;
float height = 1.75;
char grade = 'A';
double pi = 3.14159265359;
```

Size of types is architecture dependent.

---

## Integer Types

```c
#include <stdio.h>
#include <limits.h>

int main() {
    printf("Size of int: %zu bytes\n", sizeof(int));
    printf("Range of int: %d to %d\n", INT_MIN, INT_MAX);
    return 0;
}
```

---

## Floating-Point Types

```c
#include <stdio.h>
#include <float.h>

int main() {
    printf("Size of float: %zu bytes\n", sizeof(float));
    printf("Size of double: %zu bytes\n", sizeof(double));
    printf("Float precision: %d decimal places\n", FLT_DIG);
    printf("Double precision: %d decimal places\n", DBL_DIG);
    return 0;
}
```

---

## Character Type

```c
#include <stdio.h>

int main() {
    char c = 'A';
    printf("Character: %c, ASCII value: %d\n", c, c);
    return 0;
}
```

---

## Boolean Type in C99

```c
#include <stdio.h>
#include <stdbool.h>

int main() {
    bool is_valid = true;
    printf("is_valid: %d\n", is_valid);
    return 0;
}
```

This is part of the C99 standard which today is automatic in most compilers.

---

## Constant Variables

```c
#include <stdio.h>

#define PI 3.14159

int main() {
    const int MAX_SIZE = 100;
    printf("PI: %f\n", PI);
    printf("MAX_SIZE: %d\n", MAX_SIZE);
    return 0;
}
```

---

## Operators: Arithmetic

```c
#include <stdio.h>

int main() {
    int a = 10, b = 3;
    printf("a + b = %d\n", a + b);
    printf("a - b = %d\n", a - b);
    printf("a * b = %d\n", a * b);
    printf("a / b = %d\n", a / b);
    printf("a %% b = %d\n", a % b);
    return 0;
}
```

---

## Operators: Increment and Decrement

```c
#include <stdio.h>

int main() {
    int x = 5;
    printf("x: %d\n", x);
    printf("++x: %d\n", ++x);
    printf("x++: %d\n", x++);
    printf("x: %d\n", x);
    return 0;
}
```

---

## Operators: Relational

```c
#include <stdio.h>

int main() {
    int a = 5, b = 10;
    printf("a < b: %d\n", a < b);
    printf("a > b: %d\n", a > b);
    printf("a <= b: %d\n", a <= b);
    printf("a >= b: %d\n", a >= b);
    printf("a == b: %d\n", a == b);
    printf("a != b: %d\n", a != b);
    return 0;
}
```

---

## Operators: Logical

```c
#include <stdio.h>
#include <stdbool.h>

int main() {
    bool a = true, b = false;
    printf("a && b: %d\n", a && b);
    printf("a || b: %d\n", a || b);
    printf("!a: %d\n", !a);
    return 0;
}
```

---

## Operators: Bitwise

```c
#include <stdio.h>

int main() {
    unsigned int a = 60;  // 0011 1100
    unsigned int b = 13;  // 0000 1101
    printf("a & b = %u\n", a & b);
    printf("a | b = %u\n", a | b);
    printf("a ^ b = %u\n", a ^ b);
    printf("~a = %u\n", ~a);
    printf("a << 2 = %u\n", a << 2);
    printf("a >> 2 = %u\n", a >> 2);
    return 0;
}
```

---

## Operators: Assignment

```c
#include <stdio.h>

int main() {
    int x = 10;
    x += 5;  // x = x + 5
    printf("x after x += 5: %d\n", x);
    x -= 3;  // x = x - 3
    printf("x after x -= 3: %d\n", x);
    x *= 2;  // x = x * 2
    printf("x after x *= 2: %d\n", x);
    x /= 4;  // x = x / 4
    printf("x after x /= 4: %d\n", x);
    x %= 3;  // x = x % 3
    printf("x after x %%= 3: %d\n", x);
    return 0;
}
```

---

## Type Casting

```c
#include <stdio.h>

int main() {
    int i = 10;
    float f = 3.14;
    printf("i as float: %f\n", (float)i);
    printf("f as int: %d\n", (int)f);
    return 0;
}
```

---

## Control Flow: if-else

```c
#include <stdio.h>

int main() {
    int age = 18;
    if (age >= 18) {
        printf("You are an adult.\n");
    } else {
        printf("You are a minor.\n");
    }
    return 0;
}
```

---

## Control Flow: switch

```c
#include <stdio.h>

int main() {
    char grade = 'B';
    switch (grade) {
        case 'A':
            printf("Excellent!\n");
            break;
        case 'B':
            printf("Good job!\n");
            break;
        case 'C':
            printf("Average performance.\n");
            break;
        default:
            printf("Need improvement.\n");
    }
    return 0;
}
```

---

## Loops: while

```c
#include <stdio.h>

int main() {
    int count = 0;
    while (count < 5) {
        printf("%d ", count);
        count++;
    }
    printf("\n");
    return 0;
}
```

---

## Loops: do-while

```c
#include <stdio.h>

int main() {
    int num;
    do {
        printf("Enter a positive number: ");
        scanf("%d", &num);
    } while (num <= 0);
    printf("You entered: %d\n", num);
    return 0;
}
```

---

## Loops: for

```c
#include <stdio.h>

int main() {
    for (int i = 0; i < 5; i++) {
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}
```

---

## Loop Control: break and continue

```c
#include <stdio.h>

int main() {
    for (int i = 0; i < 10; i++) {
        if (i == 5) {
            continue;  // Skip 5
        }
        if (i == 8) {
            break;  // Stop at 8
        }
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}
```

---

## Arrays: Declaration and Initialization

```c
#include <stdio.h>

int main() {
    int numbers[5] = {1, 2, 3, 4, 5};
    for (int i = 0; i < 5; i++) {
        printf("%d ", numbers[i]);
    }
    printf("\n");
    return 0;
}
```

---

## Arrays: Multi-dimensional

```c
#include <stdio.h>

int main() {
    int matrix[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
    return 0;
}
```

---

## Strings in C

```c
#include <stdio.h>
#include <string.h>

int main() {
    char greeting[] = "Hello, World!";
    printf("Greeting: %s\n", greeting);
    printf("Length: %zu\n", strlen(greeting));
    return 0;
}
```

---

## String Functions

```c
#include <stdio.h>
#include <string.h>

int main() {
    char str1[20] = "Hello";
    char str2[] = ", World!";
    strcat(str1, str2);
    printf("Concatenated: %s\n", str1);
    
    char str3[] = "Hello";
    if (strcmp(str1, str3) == 0) {
        printf("Strings are equal\n");
    } else {
        printf("Strings are not equal\n");
    }
    return 0;
}
```

---

## Introduction to Pointers

```c
#include <stdio.h>

int main() {
    int x = 10;
    int *ptr = &x;
    printf("Value of x: %d\n", x);
    printf("Address of x: %p\n", (void*)&x);
    printf("Value of ptr: %p\n", (void*)ptr);
    printf("Value pointed by ptr: %d\n", *ptr);
    return 0;
}
```

---

## Pointer Arithmetic

```c
#include <stdio.h>

int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int *p = arr;
    for (int i = 0; i < 5; i++) {
        printf("%d ", *p);
        p++;
    }
    printf("\n");
    return 0;
}
```

---

## Pointers and Arrays

```c
#include <stdio.h>

int main() {
    int arr[] = {10, 20, 30, 40, 50};
    int *p = arr;
    for (int i = 0; i < 5; i++) {
        printf("arr[%d] = %d, *(p+%d) = %d\n", i, arr[i], i, *(p+i));
    }
    return 0;
}
```

---

## Pointers to Pointers

```c
#include <stdio.h>

int main() {
    int x = 10;
    int *p = &x;
    int **pp = &p;
    printf("x = %d\n", x);
    printf("*p = %d\n", *p);
    printf("**pp = %d\n", **pp);
    return 0;
}
```

---

## Dynamic Memory Allocation

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *arr = (int*)malloc(5 * sizeof(int));
    if (arr == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }
    for (int i = 0; i < 5; i++) {
        arr[i] = i * 10;
        printf("%d ", arr[i]);
    }
    printf("\n");
    free(arr);
    return 0;
}
```

---

## Functions: Basics

```c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int result = add(5, 3);
    printf("5 + 3 = %d\n", result);
    return 0;
}
```

---

## Function Parameters

```c
#include <stdio.h>

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int main() {
    int x = 5, y = 10;
    printf("Before swap: x = %d, y = %d\n", x, y);
    swap(&x, &y);
    printf("After swap: x = %d, y = %d\n", x, y);
    return 0;
}
```

---

## Recursive Functions

```c
#include <stdio.h>

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int main() {
    int n = 5;
    printf("Factorial of %d is %d\n", n, factorial(n));
    return 0;
}
```

---

## Function Pointers

```c
#include <stdio.h>

int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }

int main() {
    int (*operation)(int, int);
    operation = add;
    printf("10 + 5 = %d\n", operation(10, 5));
    operation = subtract;
    printf("10
```
