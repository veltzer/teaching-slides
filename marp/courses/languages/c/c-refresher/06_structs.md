# C Structs and Unions Refresher

---

## Structs in C

- A struct is a user-defined data type that groups related variables of different data types
- Syntax: `struct structure_name { /* member declarations */ };`

---

## Struct Example: Student

```c
struct Student {
    char name[50];
    int age;
    float gpa;
};

struct Student alice = {"Alice", 20, 3.8};
```

---

## Accessing Struct Members

- Use the dot (.) operator to access struct members
- For pointers to structs, use the arrow (->) operator

```c
struct Student bob;
strcpy(bob.name, "Bob");
bob.age = 22;
bob.gpa = 3.5;

struct Student *ptr = &bob;
printf("Name: %s, Age: %d", ptr->name, ptr->age);
```

---

## Nested Structs

- Structs can contain other structs as members

```c
struct Date {
    int day;
    int month;
    int year;
};

struct Employee {
    char name[50];
    struct Date birthdate;
    float salary;
};

struct Employee emp = {"John Doe", {15, 8, 1990}, 50000.0};
```

---

## Unions in C

- A union is a special data type that allows storing different data types in the same memory location
- Only one member can hold a value at any given time
- Syntax: `union union_name { /* member declarations */ };`

---

## Union Example: Data

```c
union Data {
    int i;
    float f;
    char str[20];
};

union Data data;
data.i = 10;
printf("Integer: %d\n", data.i);

data.f = 220.5;
printf("Float: %.2f\n", data.f);

strcpy(data.str, "C Programming");
printf("String: %s\n", data.str);
```

---

## Unions vs Structs

- Unions share memory among all members
- The size of a union is the size of its largest member
- Use unions when you need to save memory and only one member will be used at a time

---

## Practical Use of Unions

- Unions are often used with structs to create more complex data structures

```c
enum Type { INT, FLOAT, STRING };

struct Value {
    enum Type type;
    union {
        int i;
        float f;
        char s[20];
    } data;
};

struct Value v;
v.type = FLOAT;
v.data.f = 3.14;
```

---

---

## Struct Memory Layout and Padding

```text
struct Example {
    char  a;    /* 1 byte  */
    int   b;    /* 4 bytes */
    char  c;    /* 1 byte  */
};

Memory layout (with padding on 64-bit):
┌─────┬─────────────┬─────────────────┬─────┬─────────────┐
│  a  │  padding(3) │       b         │  c  │  padding(3) │
│ 1B  │    3B       │      4B         │ 1B  │    3B       │
└─────┴─────────────┴─────────────────┴─────┴─────────────┘
Offset: 0     1         4               8      9
Total size: 12 bytes (not 6!)
```

Reorder fields to minimize padding:

```c
struct BetterLayout {
    int   b;    /* 4 bytes, offset 0 */
    char  a;    /* 1 byte,  offset 4 */
    char  c;    /* 1 byte,  offset 5 */
    /* 2 bytes padding */
};
/* sizeof = 8 instead of 12! */
```

---

## Struct Padding: Complete Example

```c
#include <stdio.h>
#include <stddef.h>

struct Padded {
    char  a;
    int   b;
    char  c;
};

struct Compact {
    int   b;
    char  a;
    char  c;
};

int main(void) {
    printf("Padded: size=%zu\n", sizeof(struct Padded));    /* 12 */
    printf("Compact: size=%zu\n", sizeof(struct Compact));  /*  8 */

    /* Use offsetof to see field positions */
    printf("\nPadded offsets:\n");
    printf("  a: %zu\n", offsetof(struct Padded, a));  /* 0 */
    printf("  b: %zu\n", offsetof(struct Padded, b));  /* 4 */
    printf("  c: %zu\n", offsetof(struct Padded, c));  /* 8 */

    printf("\nCompact offsets:\n");
    printf("  b: %zu\n", offsetof(struct Compact, b));  /* 0 */
    printf("  a: %zu\n", offsetof(struct Compact, a));  /* 4 */
    printf("  c: %zu\n", offsetof(struct Compact, c));  /* 5 */

    return 0;
}
```

---

## Flexible Array Members (C99)

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Message {
    int length;
    char data[];  /* flexible array member -- must be last */
};

struct Message *create_message(const char *text) {
    int len = strlen(text);
    struct Message *msg = malloc(sizeof(struct Message) + len + 1);
    if (msg == NULL) return NULL;
    msg->length = len;
    memcpy(msg->data, text, len + 1);
    return msg;
}

int main(void) {
    struct Message *msg = create_message("Hello, FAM!");
    if (msg) {
        printf("Length: %d, Data: %s\n", msg->length, msg->data);
        free(msg);
    }
    return 0;
}
```

---

## Linked List with Structs

```c
#include <stdio.h>
#include <stdlib.h>

struct Node {
    int data;
    struct Node *next;
};

struct Node *prepend(struct Node *head, int value) {
    struct Node *new_node = malloc(sizeof(struct Node));
    if (new_node == NULL) return head;
    new_node->data = value;
    new_node->next = head;
    return new_node;
}

void print_list(const struct Node *head) {
    for (const struct Node *cur = head; cur != NULL; cur = cur->next) {
        printf("%d -> ", cur->data);
    }
    printf("NULL\n");
}

void free_list(struct Node *head) {
    while (head != NULL) {
        struct Node *tmp = head;
        head = head->next;
        free(tmp);
    }
}

int main(void) {
    struct Node *list = NULL;
    list = prepend(list, 30);
    list = prepend(list, 20);
    list = prepend(list, 10);
    print_list(list);  /* 10 -> 20 -> 30 -> NULL */
    free_list(list);
    return 0;
}
```

---

## Union Size and Type Punning

```c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

/* Inspect float bit pattern using union (technically UB in C99,
   well-defined in C11 with some compilers via type punning) */
union FloatBits {
    float f;
    uint32_t u;
};

/* Safer alternative: use memcpy */
uint32_t float_to_bits(float f) {
    uint32_t bits;
    memcpy(&bits, &f, sizeof(bits));
    return bits;
}

int main(void) {
    union FloatBits fb;
    fb.f = 3.14f;
    printf("float %.2f = 0x%08X\n", fb.f, fb.u);

    /* Safe version */
    uint32_t bits = float_to_bits(3.14f);
    printf("float 3.14 = 0x%08X (via memcpy)\n", bits);

    /* Union size = size of largest member */
    printf("sizeof(union FloatBits) = %zu\n", sizeof(union FloatBits));

    return 0;
}
```

---

## Tagged Unions: A Complete Implementation

```c
#include <stdio.h>
#include <string.h>

enum ValueType { VAL_INT, VAL_DOUBLE, VAL_STRING, VAL_BOOL };

struct Value {
    enum ValueType type;
    union {
        int i;
        double d;
        char s[32];
        int b;  /* C has no bool before C99 */
    } as;
};

void print_value(const struct Value *v) {
    switch (v->type) {
        case VAL_INT:    printf("int: %d\n", v->as.i); break;
        case VAL_DOUBLE: printf("double: %f\n", v->as.d); break;
        case VAL_STRING: printf("string: \"%s\"\n", v->as.s); break;
        case VAL_BOOL:   printf("bool: %s\n", v->as.b ? "true" : "false"); break;
    }
}

int main(void) {
    struct Value values[] = {
        { .type = VAL_INT,    .as.i = 42 },
        { .type = VAL_DOUBLE, .as.d = 3.14 },
        { .type = VAL_STRING, .as.s = "hello" },
        { .type = VAL_BOOL,   .as.b = 1 },
    };

    for (int i = 0; i < 4; i++) {
        print_value(&values[i]);
    }
    return 0;
}
```

---

## Struct Copying and Comparison

```c
#include <stdio.h>
#include <string.h>

struct Point {
    double x;
    double y;
};

int main(void) {
    struct Point a = {3.0, 4.0};

    /* Struct assignment copies all members */
    struct Point b = a;
    printf("b = (%.1f, %.1f)\n", b.x, b.y);

    /* CANNOT use == to compare structs */
    /* if (a == b) { }  <-- COMPILE ERROR */

    /* Use memcmp (works for simple structs without padding issues) */
    if (memcmp(&a, &b, sizeof(struct Point)) == 0) {
        printf("a and b are equal\n");
    }

    /* Better: write a comparison function */
    /* (memcmp may fail due to padding bytes) */
    if (a.x == b.x && a.y == b.y) {
        printf("a and b are equal (field comparison)\n");
    }

    return 0;
}
```

---

## Summary

- Structs group related variables of different types
- Unions allow different data types to share the same memory location
- Be aware of struct padding -- reorder fields largest-to-smallest to minimize waste
- Use `offsetof` to inspect field positions
- Flexible array members allow variable-size structs
- Tagged unions combine an enum type tag with a union for type-safe variant types
- Structs can be assigned but not compared with `==`
- Use structs when you need to store multiple related values simultaneously
- Use unions when you need to save memory and only one value is needed at a time
