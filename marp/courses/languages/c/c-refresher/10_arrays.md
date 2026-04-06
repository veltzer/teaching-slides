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

## The ARRAY_SIZE Macro

```c
#include <stdio.h>

/* Classic approach: sizeof trick */
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))

int main(void) {
    int nums[] = {10, 20, 30, 40, 50};
    printf("Array has %zu elements\n", ARRAY_SIZE(nums));

    /* WARNING: does NOT work with pointers! */
    int *ptr = nums;
    /* ARRAY_SIZE(ptr) gives sizeof(int*)/sizeof(int) = 2 on 64-bit */
    /* This is a silent bug! */

    /* Iterate using ARRAY_SIZE */
    for (size_t i = 0; i < ARRAY_SIZE(nums); i++) {
        printf("nums[%zu] = %d\n", i, nums[i]);
    }

    return 0;
}
```

---

## Array Memory Layout

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="340" font-family="monospace">
  <!-- Code -->
  <text x="10" y="20" font-size="13" fill="#222">int arr[5] = &#123;10, 20, 30, 40, 50&#125;;</text>
  <text x="10" y="40" font-size="13" fill="#555" font-family="sans-serif">Contiguous memory (4 bytes per int):</text>
  <!-- 1D array cells -->
  <rect x="10"  y="50" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <rect x="130" y="50" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <rect x="250" y="50" width="120" height="40" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <rect x="370" y="50" width="120" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <rect x="490" y="50" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="70"  y="68" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">10</text>
  <text x="190" y="68" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">20</text>
  <text x="310" y="68" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">30</text>
  <text x="430" y="68" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">40</text>
  <text x="550" y="68" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">50</text>
  <text x="70"  y="84" font-size="12" fill="#555" text-anchor="middle">arr[0]</text>
  <text x="190" y="84" font-size="12" fill="#555" text-anchor="middle">arr[1]</text>
  <text x="310" y="84" font-size="12" fill="#555" text-anchor="middle">arr[2]</text>
  <text x="430" y="84" font-size="12" fill="#555" text-anchor="middle">arr[3]</text>
  <text x="550" y="84" font-size="12" fill="#555" text-anchor="middle">arr[4]</text>
  <!-- addresses -->
  <text x="10"  y="104" font-size="11" fill="#777">0x1000</text>
  <text x="130" y="104" font-size="11" fill="#777">0x1004</text>
  <text x="250" y="104" font-size="11" fill="#777">0x1008</text>
  <text x="370" y="104" font-size="11" fill="#777">0x100C</text>
  <text x="490" y="104" font-size="11" fill="#777">0x1010</text>
  <!-- notes -->
  <text x="10" y="125" font-size="13" fill="#222">arr      == &amp;arr[0] == 0x1000</text>
  <text x="10" y="143" font-size="13" fill="#222">arr + 1  == &amp;arr[1] == 0x1004  (advances by sizeof(int))</text>
  <text x="10" y="161" font-size="13" fill="#222">*(arr+i) == arr[i]             (pointer arithmetic identity)</text>
  <!-- 2D -->
  <text x="10" y="188" font-size="13" fill="#555" font-family="sans-serif">2D array: int matrix[2][3] = &#123;&#123;1,2,3&#125;,&#123;4,5,6&#125;&#125;;</text>
  <text x="10" y="210" font-size="13" fill="#555" font-family="sans-serif">Row-major layout in memory:</text>
  <rect x="10"  y="218" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <rect x="110" y="218" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <rect x="210" y="218" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <rect x="310" y="218" width="100" height="40" fill="#fce4ec" stroke="#333" stroke-width="1.5"/>
  <rect x="410" y="218" width="100" height="40" fill="#ede7f6" stroke="#333" stroke-width="1.5"/>
  <rect x="510" y="218" width="100" height="40" fill="#e0f7fa" stroke="#333" stroke-width="1.5"/>
  <text x="60"  y="236" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">1</text>
  <text x="160" y="236" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">2</text>
  <text x="260" y="236" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">3</text>
  <text x="360" y="236" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">4</text>
  <text x="460" y="236" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">5</text>
  <text x="560" y="236" font-size="14" font-weight="bold" fill="#222" text-anchor="middle">6</text>
  <text x="60"  y="252" font-size="11" fill="#555" text-anchor="middle">[0][0]</text>
  <text x="160" y="252" font-size="11" fill="#555" text-anchor="middle">[0][1]</text>
  <text x="260" y="252" font-size="11" fill="#555" text-anchor="middle">[0][2]</text>
  <text x="360" y="252" font-size="11" fill="#555" text-anchor="middle">[1][0]</text>
  <text x="460" y="252" font-size="11" fill="#555" text-anchor="middle">[1][1]</text>
  <text x="560" y="252" font-size="11" fill="#555" text-anchor="middle">[1][2]</text>
  <text x="10" y="278" font-size="13" fill="#222">matrix[i][j] is at offset (i * 3 + j) * sizeof(int)</text>
</svg>

---

## Variable-Length Arrays (C99)

```c
#include <stdio.h>

void print_matrix(int rows, int cols, int mat[rows][cols]) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%4d ", mat[i][j]);
        }
        printf("\n");
    }
}

int main(void) {
    int n = 4;
    int vla[n];  /* VLA: size determined at runtime */

    for (int i = 0; i < n; i++) {
        vla[i] = i * i;
    }

    /* 2D VLA */
    int rows = 3, cols = 4;
    int matrix[rows][cols];
    for (int i = 0; i < rows; i++)
        for (int j = 0; j < cols; j++)
            matrix[i][j] = i * cols + j;

    print_matrix(rows, cols, matrix);
    return 0;
}
```

Caution: VLAs are allocated on the stack. Large VLAs can cause stack overflow.
VLAs are optional in C11 and later (`__STDC_NO_VLA__`).

---

## Sorting with qsort: Complete Example

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Comparator for integers (ascending) */
int cmp_int_asc(const void *a, const void *b) {
    int ia = *(const int *)a;
    int ib = *(const int *)b;
    return (ia > ib) - (ia < ib);  /* safe: no overflow */
}

/* Comparator for strings */
int cmp_str(const void *a, const void *b) {
    const char *sa = *(const char **)a;
    const char *sb = *(const char **)b;
    return strcmp(sa, sb);
}

int main(void) {
    /* Sort integers */
    int nums[] = {42, 17, 93, 5, 28, 61};
    int n = sizeof(nums) / sizeof(nums[0]);
    qsort(nums, n, sizeof(int), cmp_int_asc);

    printf("Sorted ints: ");
    for (int i = 0; i < n; i++) printf("%d ", nums[i]);
    printf("\n");

    /* Sort strings */
    const char *words[] = {"banana", "apple", "cherry", "date"};
    int nw = sizeof(words) / sizeof(words[0]);
    qsort(words, nw, sizeof(char *), cmp_str);

    printf("Sorted strings: ");
    for (int i = 0; i < nw; i++) printf("%s ", words[i]);
    printf("\n");

    return 0;
}
```

---

## Binary Search with bsearch

```c
#include <stdio.h>
#include <stdlib.h>

int cmp_int(const void *a, const void *b) {
    int ia = *(const int *)a;
    int ib = *(const int *)b;
    return (ia > ib) - (ia < ib);
}

int main(void) {
    int sorted[] = {5, 12, 17, 28, 42, 61, 93};
    int n = sizeof(sorted) / sizeof(sorted[0]);

    int key = 28;
    int *found = bsearch(&key, sorted, n, sizeof(int), cmp_int);

    if (found) {
        printf("Found %d at index %td\n", *found, found - sorted);
    } else {
        printf("%d not found\n", key);
    }

    key = 99;
    found = bsearch(&key, sorted, n, sizeof(int), cmp_int);
    printf("%d: %s\n", key, found ? "found" : "not found");

    return 0;
}
```

---

## Best Practices
1. Always initialize arrays when declared, if possible
1. Use const for arrays that shouldn't be modified
1. Use sizeof() carefully with arrays (doesn't work as expected when arrays decay to pointers)
1. Consider using dynamic allocation for large or variably-sized arrays
1. Be cautious with multidimensional arrays and their memory usage
1. Always free dynamically allocated arrays when no longer needed
1. Use `ARRAY_SIZE` macro instead of hardcoding array lengths
1. Prefer `qsort` and `bsearch` over hand-rolled algorithms

---

## Summary
- Arrays in C are fixed-size collections of elements of the same type
- They are closely related to pointers and are passed by reference to functions
- Multidimensional arrays and arrays of pointers provide more complex data structures
- Dynamic arrays allow for runtime size determination
- Use standard library functions (`qsort`, `bsearch`, `memcpy`) for common operations
- VLAs provide runtime-sized arrays but come with stack overflow risks
- Understanding array limitations and following best practices is crucial for effective C programming
