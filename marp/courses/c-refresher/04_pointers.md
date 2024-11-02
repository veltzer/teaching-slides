# Pointers in C: A Refresher

**C Programming Refresher Course**

---

## What is a Pointer?

- A **pointer** is a variable that stores the **memory address** of another variable.
- In C, pointers are a powerful tool for dynamic memory allocation, array manipulation, and efficient data handling.

### Example:

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

### Key Points:
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

### Example:

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

## Quiz Time!

1. What does the `&` operator do?
1. How do you dereference a pointer?
1. What's the difference between `ptr++` and `(*ptr)++`?
