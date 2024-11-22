# Strings in C Refresher

---

## What are Strings in C?

- In C, strings are arrays of characters
- They are terminated by a null character (`'\0'`)
- Not a built-in data type like in some other languages

```c
char greeting[] = "Hello";
// Equivalent to:
char greeting[] = {'H', 'e', 'l', 'l', 'o', '\0'};
```

---

## Declaring Strings

Two main ways to declare strings:

1. Character array:

```c
char str[6] = "Hello";
```

1. Pointer to char:

```c
char *str = "Hello";
```

Note: The second method creates a read-only string literal.

---

## String Input and Output

Input:

```c
char name[50];
scanf("%s", name);  // Reads until whitespace
fgets(name, sizeof(name), stdin);  // Reads entire line
```

Output:

```c
char *greeting = "Hello, World!";
printf("%s\n", greeting);
puts(greeting);  // Automatically adds newline
```

---

## String Length: strlen()

- `strlen()` returns the length of a string (excluding null terminator)
- Defined in `<string.h>`

```c
#include <string.h>

char str[] = "Hello";
size_t length = strlen(str);  // length is 5
```

---

## String Comparison: strcmp()

- `strcmp()` compares two strings
- Returns 0 if equal, <0 if str1 < str2, >0 if str1 > str2
- Defined in `<string.h>`

```c
#include <string.h>

char *s1 = "apple";
char *s2 = "banana";

if (strcmp(s1, s2) < 0) {
    printf("apple comes before banana\n");
}
```

---

## String Copy: strcpy()

- `strcpy()` copies one string to another
- Dangerous if destination buffer is too small
- `strncpy()` is a safer alternative
- Both defined in `<string.h>`

```c
#include <string.h>

char src[] = "Hello";
char dest[10];

strcpy(dest, src);
// or safer:
strncpy(dest, src, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';  // Ensure null-termination
```

---

## String Concatenation: strcat()

- `strcat()` appends one string to another
- `strncat()` is a safer alternative (limits characters copied)
- Both defined in `<string.h>`

```c
#include <string.h>

char str1[20] = "Hello";
char str2[] = ", World!";

strcat(str1, str2);
// or safer:
strncat(str1, str2, sizeof(str1) - strlen(str1) - 1);
```

---

## String Searching: strchr() and strstr()

- `strchr()`: Find first occurrence of a character
- `strstr()`: Find first occurrence of a substring
- Both defined in `<string.h>`

```c
#include <string.h>

char str[] = "Hello, World!";
char *ch = strchr(str, 'o');  // Points to first 'o'
char *sub = strstr(str, "World");  // Points to "World"
```

---

## String to Number Conversion

- `atoi()`: Convert string to integer
- `atof()`: Convert string to float
- Defined in `<stdlib.h>`

```c
#include <stdlib.h>

char num_str[] = "12345";
int num = atoi(num_str);  // num is 12345

char float_str[] = "3.14159";
float pi = atof(float_str);  // pi is 3.14159
```

---

## String Tokenization: strtok()

- `strtok()` splits a string into tokens
- Defined in `<string.h>`
- Not thread-safe (use `strtok_r()` for thread-safe version)

```c
#include <string.h>

char str[] = "apple,banana,cherry";
char *token = strtok(str, ",");
while (token != NULL) {
    printf("%s\n", token);
    token = strtok(NULL, ",");
}
```

---

## String Formatting: sprintf()

- `sprintf()` writes formatted output to a string
- `snprintf()` is a safer alternative (limits characters written)
- Both defined in `<stdio.h>`

```c
#include <stdio.h>

char buffer[50];
int age = 30;
sprintf(buffer, "I am %d years old", age);
// or safer:
snprintf(buffer, sizeof(buffer), "I am %d years old", age);
```

---

## Common String Pitfalls

1. Forgetting null terminator
1. Buffer overflow
1. Using `scanf()` without limiting input
1. Modifying string literals
1. Not checking return values of string functions

```c
char str[5] = "Hello";  // Buffer overflow!
char *s = "Hello"; s[0] = 'h';  // Undefined behavior!
```

---

## Best Practices

1. Always ensure strings are null-terminated
1. Use safer alternatives like `strncpy()`, `strncat()`, `snprintf()`
1. Check return values of string functions
1. Use `fgets()` instead of `gets()` for string input
1. Be cautious with string literals

---

## Summary

- Strings in C are null-terminated character arrays
- Many string operations are provided by `<string.h>` library
- Be aware of buffer overflows and always ensure null-termination
- Use safer alternatives to standard functions when possible
- Remember that string literals are read-only
