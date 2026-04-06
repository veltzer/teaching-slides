# Pointers in C: A Refresher

## C Programming Refresher Course

---

## What is a Pointer

- A **pointer** is a variable that stores the **memory address** of another variable.
- In C, pointers are a powerful tool for dynamic memory allocation, array manipulation, and efficient data handling.

### Example

```c
int a = 10;
int *p = &a; // p holds the address of a
```

- `p` is a pointer to `int`, storing the address of `a`.
- `*p` dereferences the pointer to access the value stored at that address.

---

## Declaring and Initializing Pointers

```c
int x = 5;
int *ptr = &x; // ptr is a pointer to an int, initialized with the address of x
```

### Key Points
- `*` indicates that the variable is a pointer.
- The `&` operator is used to get the address of a variable.
- Pointers must be initialized before use to avoid undefined behavior.

---

## Dereferencing Pointers

- Dereferencing a pointer means accessing the value stored at the memory address the pointer holds.

```c
int y = 20;
int *ptr = &y;
printf("%d", *ptr); // Outputs: 20
```

- `*ptr` accesses the value of `y` through the pointer.

---

## Pointer Arithmetic

- Pointers support arithmetic operations like addition and subtraction.
- The operations depend on the data type size.

### Example

```c
int arr[3] = {10, 20, 30};
int *ptr = arr; // points to arr[0]

ptr++; // now points to arr[1]
printf("%d", *ptr); // Outputs: 20
```

- `ptr++` advances the pointer to the next `int` in memory.

---

## Pointers and Arrays

- The name of an array is a pointer to its first element.

```c
int arr[3] = {1, 2, 3};
int *ptr = arr; // ptr points to arr[0]
```

- `ptr` and `arr` can be used interchangeably to access array elements:

```c
printf("%d", *(ptr + 1)); // Outputs: 2
```

---

## Pointers and Functions

- Pointers can be passed to functions to modify the original data.

### Example:

```c
void increment(int *p) {
    (*p)++;
}

int main() {
    int a = 10;
    increment(&a);
    printf("%d", a); // Outputs: 11
}
```

- Passing `&a` allows the function to modify `a` directly.

---

## Dynamic Memory Allocation

- Pointers are essential for managing dynamic memory in C.
- Functions like `malloc`, `calloc`, `realloc`, and `free` manage heap memory.

### Example:

```c
int *ptr = (int *)malloc(sizeof(int) * 10); // Allocate space for 10 ints
```

- `free(ptr)` deallocates the memory.

---

## Common Pointer Pitfalls

1. **Uninitialized Pointers**:
    - Using pointers before they are initialized leads to undefined behavior.
1. **Dangling Pointers**:
    - After freeing memory, the pointer still holds the address. Always set pointers to `NULL` after freeing them.
1. **Pointer Arithmetic Misuse**:
    - Ensure correct data type alignment when performing arithmetic operations.

---

## Pointer Memory Visualization

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="310" font-family="monospace">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <!-- Code block -->
  <rect x="10" y="10" width="300" height="70" fill="#f5f5f5" stroke="#999" stroke-width="1" rx="4"/>
  <text x="20" y="30" font-size="13" fill="#222">int x = 42;</text>
  <text x="20" y="48" font-size="13" fill="#222">int *p = &amp;x;</text>
  <text x="20" y="66" font-size="13" fill="#222">int **pp = &amp;p;</text>
  <!-- Stack Memory label -->
  <text x="10" y="105" font-size="13" font-weight="bold" fill="#333" font-family="sans-serif">Stack Memory:</text>
  <!-- pp row -->
  <rect x="10" y="115" width="200" height="36" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="20" y="138" font-size="13" fill="#222">pp: 0x7FF008</text>
  <!-- p row -->
  <rect x="10" y="151" width="200" height="36" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="20" y="174" font-size="13" fill="#222">p:  0x7FF010</text>
  <!-- x row -->
  <rect x="10" y="187" width="200" height="36" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="20" y="206" font-size="13" fill="#222">x:  42</text>
  <text x="20" y="220" font-size="12" fill="#777">    0x7FF018</text>
  <!-- pp -> p arrow -->
  <line x1="210" y1="133" x2="260" y2="133" stroke="#555" stroke-width="1.5"/>
  <line x1="260" y1="133" x2="260" y2="169" stroke="#555" stroke-width="1.5"/>
  <line x1="210" y1="169" x2="256" y2="169" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- p -> x arrow -->
  <line x1="210" y1="169" x2="280" y2="169" stroke="transparent"/>
  <line x1="210" y1="205" x2="270" y2="205" stroke="#555" stroke-width="1.5"/>
  <line x1="270" y1="169" x2="270" y2="205" stroke="#555" stroke-width="1.5"/>
  <line x1="210" y1="169" x2="266" y2="169" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- equivalences -->
  <text x="10" y="255" font-size="13" fill="#222">**pp == *p == x == 42</text>
  <text x="10" y="275" font-size="13" fill="#222"> *pp == p  == 0x7FF018</text>
  <text x="10" y="295" font-size="13" fill="#222">  pp       == 0x7FF010</text>
</svg>

---

## Pointer Arithmetic in Detail

```c
#include <stdio.h>

int main(void) {
    int arr[] = {10, 20, 30, 40, 50};
    int *p = arr;

    /* Pointer + integer: advances by (n * sizeof(type)) bytes */
    printf("p     = %p, *p     = %d\n", (void *)p, *p);
    printf("p + 1 = %p, *(p+1) = %d\n", (void *)(p+1), *(p+1));
    printf("p + 4 = %p, *(p+4) = %d\n", (void *)(p+4), *(p+4));

    /* Pointer difference: returns number of elements */
    int *end = &arr[4];
    ptrdiff_t diff = end - p;
    printf("end - p = %td elements\n", diff);  /* 4 */

    /* Comparison */
    if (p < end) {
        printf("p points before end\n");
    }

    /* Iterate using pointers */
    for (int *it = arr; it < arr + 5; it++) {
        printf("%d ", *it);
    }
    printf("\n");

    return 0;
}
```

---

## Pointers to Pointers

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Allocate a string and return via pointer-to-pointer */
int allocate_string(char **out, const char *src) {
    *out = malloc(strlen(src) + 1);
    if (*out == NULL) return -1;
    strcpy(*out, src);
    return 0;
}

int main(void) {
    char *str = NULL;

    if (allocate_string(&str, "Hello, Pointers!") == 0) {
        printf("%s\n", str);
        free(str);
    }

    /* 2D dynamic array using pointer to pointer */
    int rows = 3, cols = 4;
    int **matrix = malloc(rows * sizeof(int *));
    for (int i = 0; i < rows; i++) {
        matrix[i] = malloc(cols * sizeof(int));
        for (int j = 0; j < cols; j++) {
            matrix[i][j] = i * cols + j;
        }
    }

    /* Print matrix */
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%3d ", matrix[i][j]);
        }
        printf("\n");
    }

    /* Free matrix */
    for (int i = 0; i < rows; i++) {
        free(matrix[i]);
    }
    free(matrix);

    return 0;
}
```

---

## Const and Pointers

```c
#include <stdio.h>

int main(void) {
    int x = 10, y = 20;

    /* 1. Pointer to const: can't modify the value */
    const int *p1 = &x;
    /* *p1 = 30;  ERROR: can't modify through p1 */
    p1 = &y;     /* OK: can change what p1 points to */

    /* 2. Const pointer: can't change where it points */
    int *const p2 = &x;
    *p2 = 30;    /* OK: can modify the value */
    /* p2 = &y;  ERROR: can't change p2 itself */

    /* 3. Const pointer to const: can't modify either */
    const int *const p3 = &x;
    /* *p3 = 40;  ERROR */
    /* p3 = &y;   ERROR */

    printf("x=%d, y=%d\n", x, y);
    return 0;
}
```

Read right to left: `const int *p` = "p is a pointer to int const"

---

## Void Pointers: Generic Programming

```c
#include <stdio.h>
#include <string.h>

void print_value(const void *ptr, char type) {
    switch (type) {
        case 'i': printf("%d\n", *(const int *)ptr); break;
        case 'f': printf("%f\n", *(const float *)ptr); break;
        case 'd': printf("%f\n", *(const double *)ptr); break;
        case 's': printf("%s\n", (const char *)ptr); break;
    }
}

/* Generic swap function */
void swap(void *a, void *b, size_t size) {
    char temp[size];  /* VLA as temporary buffer */
    memcpy(temp, a, size);
    memcpy(a, b, size);
    memcpy(b, temp, size);
}

int main(void) {
    int a = 10, b = 20;
    printf("Before: a=%d, b=%d\n", a, b);
    swap(&a, &b, sizeof(int));
    printf("After:  a=%d, b=%d\n", a, b);

    double x = 3.14, y = 2.72;
    printf("Before: x=%f, y=%f\n", x, y);
    swap(&x, &y, sizeof(double));
    printf("After:  x=%f, y=%f\n", x, y);

    return 0;
}
```

---

## Restrict Pointers (C99)

```c
#include <stdio.h>
#include <string.h>

/* Without restrict: compiler assumes a and b might alias */
void add_arrays(int *a, const int *b, int n) {
    for (int i = 0; i < n; i++) {
        a[i] += b[i];  /* compiler must reload b[i] each time */
    }
}

/* With restrict: promise no aliasing, enables optimization */
void add_arrays_fast(int *restrict a, const int *restrict b, int n) {
    for (int i = 0; i < n; i++) {
        a[i] += b[i];  /* compiler can optimize aggressively */
    }
}

int main(void) {
    int a[] = {1, 2, 3, 4, 5};
    int b[] = {10, 20, 30, 40, 50};
    add_arrays_fast(a, b, 5);
    for (int i = 0; i < 5; i++) {
        printf("%d ", a[i]);
    }
    printf("\n");
    return 0;
}
```

---

## Common Pointer Bugs: Complete Examples

```c
#include <stdio.h>
#include <stdlib.h>

/* Bug 1: returning pointer to local variable */
int *bad_function(void) {
    int local = 42;
    return &local;  /* DANGER: local is destroyed on return */
}

/* Bug 2: use after free */
void use_after_free(void) {
    int *p = malloc(sizeof(int));
    *p = 42;
    free(p);
    /* printf("%d\n", *p);  UB: p is dangling */
    p = NULL;  /* best practice: NULL after free */
}

/* Bug 3: off-by-one with pointers */
void off_by_one(void) {
    int arr[5] = {1, 2, 3, 4, 5};
    int *p = arr;
    /* Accessing arr[5] via pointer: UB */
    /* printf("%d\n", *(p + 5));  <-- past the end */
}

int main(void) {
    /* int *bad = bad_function(); */
    /* printf("%d\n", *bad);  <-- UB */
    use_after_free();
    off_by_one();
    printf("No crashes (this time), but bugs lurk!\n");
    return 0;
}
```

---

## Quiz Time!

1. What does the `&` operator do?
1. How do you dereference a pointer?
1. What's the difference between `ptr++` and `(*ptr)++`?
1. What is the difference between `const int *p` and `int *const p`?
1. Why should you set a pointer to `NULL` after calling `free()`?
