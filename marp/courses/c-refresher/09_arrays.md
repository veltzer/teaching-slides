# Arrays in C Refresher

---

## What are Arrays in C?

- Collections of elements of the same data type
- Stored in contiguous memory locations
- Fixed size, determined at compile time (for standard arrays)
- Zero-indexed: first element is at index 0

Basic syntax:

```c
data_type array_name[array_size];
```

---

## Declaring and Initializing Arrays

Declaration:

```c
int numbers[5];  // Declares an array of 5 integers
```

Initialization:

```c
int numbers[5] = {1, 2, 3, 4, 5};  // Full initialization
int partial[5] = {1, 2};  // Partial (rest are 0)
int auto_size[] = {1, 2, 3, 4, 5};  // Size determined by initializer
```

---

## Accessing Array Elements

- Use square brackets `[]` with the index
- Remember: arrays are zero-indexed!

```c
int numbers[5] = {10, 20, 30, 40, 50};
printf("%d\n", numbers[2]);  // Prints 30
numbers[4] = 60;  // Modifies the last element
```

Warning: C doesn't perform bounds checking!

---

## Arrays and Memory

- Arrays are stored in contiguous memory
- The array name is a constant pointer to the first element

```c
int arr[3] = {10, 20, 30};
printf("%p\n", arr);      // Address of the first element
printf("%p\n", &arr[0]);  // Same as above
```

---

## Arrays and Pointers

Arrays can be accessed using pointer notation:

```c
int arr[3] = {10, 20, 30};
int *ptr = arr;  // ptr points to the first element

printf("%d\n", *ptr);     // Prints 10
printf("%d\n", *(ptr+1)); // Prints 20
printf("%d\n", ptr[2]);   // Prints 30
```

---

## Passing Arrays to Functions

Arrays are passed by reference (decay to pointers):

```c
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
}

int numbers[5] = {1, 2, 3, 4, 5};
printArray(numbers, 5);
```

Alternative syntax:

```c
void printArray(int *arr, int size) {
    // Function body remains the same
}
```

---

## Multidimensional Arrays

2D array declaration and initialization:

```c
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};
```

Accessing elements:

```c
int element = matrix[1][2];  // element is 7
```

---

## Passing Multidimensional Arrays to Functions

For 2D arrays, specify at least the second dimension:

```c
void print2DArray(int arr[][4], int rows) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < 4; j++) {
            printf("%d ", arr[i][j]);
        }
        printf("\n");
    }
}

int matrix[3][4] = {{1,2,3,4}, {5,6,7,8}, {9,10,11,12}};
print2DArray(matrix, 3);
```

---

## Array of Pointers

Useful for strings or varying-length rows:

```c
char *fruits[] = {
    "apple",
    "banana",
    "cherry"
};

printf("%s\n", fruits[1]);  // Prints "banana"
```

---

## Dynamic Arrays

Use `malloc()` to create arrays at runtime:

```c
#include <stdlib.h>

int size = 5;
int *dynamicArray = (int *)malloc(size * sizeof(int));

if (dynamicArray == NULL) {
    // Handle allocation failure
}

// Use the array
for (int i = 0; i < size; i++) {
    dynamicArray[i] = i * 10;
}

// Don't forget to free when done
free(dynamicArray);
```

---

## Common Array Operations

1. Traversing:

```c
for (int i = 0; i < size; i++) {
   printf("%d ", arr[i]);
}
```

1. Searching:

```c
int search(int arr[], int size, int key) {
   for (int i = 0; i < size; i++) {
       if (arr[i] == key) return i;
   }
   return -1;  // Not found
}
```

1. Sorting (e.g., bubble sort):

```c
void bubbleSort(int arr[], int size) {
   for (int i = 0; i < size-1; i++) {
       for (int j = 0; j < size-i-1; j++) {
           if (arr[j] > arr[j+1]) {
               // Swap arr[j] and arr[j+1]
               int temp = arr[j];
               arr[j] = arr[j+1];
               arr[j+1] = temp;
           }
       }
   }
}
```

---
## Array Limitations and Considerations
1. Fixed size: Cannot be resized after declaration
1. No bounds checking: Accessing out-of-bounds elements can cause undefined behavior
1. No built-in size information: Size must be tracked separately
1. Whole array assignment not possible: Must copy element by element
1. When passed to functions, arrays decay to pointers, losing size information
---
## Best Practices
1. Always initialize arrays when declared, if possible
1. Use const for arrays that shouldn't be modified
1. Use sizeof() carefully with arrays (doesn't work as expected when arrays decay to pointers)
1. Consider using dynamic allocation for large or variably-sized arrays
1. Be cautious with multidimensional arrays and their memory usage
1. Always free dynamically allocated arrays when no longer needed
---
## Summary
- Arrays in C are fixed-size collections of elements of the same type
- They are closely related to pointers and are passed by reference to functions
- Multidimensional arrays and arrays of pointers provide more complex data structures
- Dynamic arrays allow for runtime size determination
- Understanding array limitations and following best practices is crucial for effective C programming
