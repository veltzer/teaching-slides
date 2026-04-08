# Strings in C Refresher

---

## What are Strings in C

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

## String Memory Layout

![string_memory_layout_1](svg/courses/languages/c/c-refresher/04_strings/string_memory_layout_1.svg)

![string_memory_layout_2](svg/courses/languages/c/c-refresher/04_strings/string_memory_layout_2.svg)

---

## Array vs Pointer Strings: Critical Difference

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    /* Array: string is modifiable, lives on the stack */
    char arr[] = "Hello";
    arr[0] = 'J';  /* OK: arr is now "Jello" */
    printf("arr = %s\n", arr);

    /* Pointer: points to read-only string literal */
    char *ptr = "Hello";
    /* ptr[0] = 'J';  <-- UNDEFINED BEHAVIOR! Crash likely */

    /* Array: sizeof gives full array size */
    printf("sizeof(arr) = %zu\n", sizeof(arr));  /* 6 */

    /* Pointer: sizeof gives pointer size */
    printf("sizeof(ptr) = %zu\n", sizeof(ptr));  /* 8 on 64-bit */

    /* Best practice: use const for string literal pointers */
    const char *safe_ptr = "Hello";

    return 0;
}
```

---

## Building Strings Safely: A Complete Example

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

char *build_greeting(const char *first, const char *last) {
    /* Calculate needed size: first + " " + last + "\0" */
    size_t len = strlen(first) + 1 + strlen(last) + 1;
    char *result = malloc(len);
    if (result == NULL) return NULL;

    /* Build the string safely */
    snprintf(result, len, "%s %s", first, last);
    return result;
}

int main(void) {
    char *name = build_greeting("John", "Doe");
    if (name != NULL) {
        printf("Hello, %s!\n", name);
        free(name);
    }
    return 0;
}
```

---

## String Conversion with strtol/strtod

`atoi` has no error checking. Prefer `strtol` and `strtod`:

```c
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>

int main(void) {
    const char *input = "42abc";
    char *endptr;

    errno = 0;
    long val = strtol(input, &endptr, 10);

    if (errno != 0) {
        perror("strtol");
    } else if (endptr == input) {
        printf("No digits found\n");
    } else if (*endptr != '\0') {
        printf("Parsed %ld, trailing garbage: '%s'\n", val, endptr);
    } else {
        printf("Parsed %ld successfully\n", val);
    }

    /* Parse hex */
    long hex = strtol("0xFF", NULL, 16);
    printf("0xFF = %ld\n", hex);

    /* Parse binary (C99 strtol base 2) */
    long bin = strtol("1010", NULL, 2);
    printf("1010 (binary) = %ld\n", bin);

    return 0;
}
```

---

## Character Classification Functions

```c
#include <stdio.h>
#include <ctype.h>

int main(void) {
    const char *test = "Hello, World! 123";

    for (const char *p = test; *p; p++) {
        char c = *p;
        printf("'%c': alpha=%d digit=%d upper=%d lower=%d space=%d\n",
               c,
               isalpha((unsigned char)c),
               isdigit((unsigned char)c),
               isupper((unsigned char)c),
               islower((unsigned char)c),
               isspace((unsigned char)c));
    }

    /* Convert to uppercase */
    char buf[] = "hello world";
    for (int i = 0; buf[i]; i++) {
        buf[i] = toupper((unsigned char)buf[i]);
    }
    printf("Uppercase: %s\n", buf);  /* HELLO WORLD */

    return 0;
}
```

Note: Always cast to `unsigned char` when passing to `ctype.h` functions.

---

## Implementing Common String Functions

```c
#include <stdio.h>
#include <stddef.h>

/* strlen implementation */
size_t my_strlen(const char *s) {
    size_t len = 0;
    while (s[len] != '\0') {
        len++;
    }
    return len;
}

/* strcpy implementation */
char *my_strcpy(char *dest, const char *src) {
    char *ret = dest;
    while ((*dest++ = *src++) != '\0')
        ;
    return ret;
}

/* strcmp implementation */
int my_strcmp(const char *s1, const char *s2) {
    while (*s1 && (*s1 == *s2)) {
        s1++;
        s2++;
    }
    return (unsigned char)*s1 - (unsigned char)*s2;
}

int main(void) {
    const char *hello = "Hello";
    printf("my_strlen(\"%s\") = %zu\n", hello, my_strlen(hello));

    char buf[20];
    my_strcpy(buf, hello);
    printf("my_strcpy result: %s\n", buf);

    printf("my_strcmp(\"abc\",\"abd\") = %d\n",
           my_strcmp("abc", "abd"));
    return 0;
}
```

---

## Multi-Byte and Wide Characters

```c
#include <stdio.h>
#include <wchar.h>
#include <locale.h>

int main(void) {
    setlocale(LC_ALL, "");

    /* Wide string */
    wchar_t wide[] = L"Hello \u00E9\u00E8\u00EA";
    wprintf(L"Wide: %ls\n", wide);
    wprintf(L"Wide strlen: %zu\n", wcslen(wide));

    /* Multi-byte string (UTF-8) */
    const char *utf8 = "cafe\xCC\x81";  /* cafe + combining accent */
    printf("UTF-8: %s\n", utf8);
    printf("Byte length: %zu\n", strlen(utf8));

    return 0;
}
```

---

## Buffer Overflow: A Security Vulnerability

```c
#include <stdio.h>
#include <string.h>

/* DANGEROUS: classic buffer overflow */
void vulnerable(const char *input) {
    char buffer[16];
    strcpy(buffer, input);  /* No bounds checking! */
    printf("buffer: %s\n", buffer);
}

/* SAFE: bounds-checked version */
void safe(const char *input) {
    char buffer[16];
    strncpy(buffer, input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';
    printf("buffer: %s\n", buffer);
}

/* BEST: use snprintf */
void best(const char *input) {
    char buffer[16];
    snprintf(buffer, sizeof(buffer), "%s", input);
    printf("buffer: %s\n", buffer);
}

int main(void) {
    const char *long_input = "This string is way too long for a 16-byte buffer";
    /* vulnerable(long_input);  <-- undefined behavior, possible crash */
    safe(long_input);
    best(long_input);
    return 0;
}
```

---

## Summary

- Strings in C are null-terminated character arrays
- Many string operations are provided by `<string.h>` library
- Be aware of buffer overflows and always ensure null-termination
- Use safer alternatives to standard functions when possible
- Remember that string literals are read-only -- use `const char *`
- Prefer `strtol`/`strtod` over `atoi`/`atof` for error detection
- Cast to `unsigned char` before calling `ctype.h` functions
- Use `snprintf` as the safest way to build formatted strings
