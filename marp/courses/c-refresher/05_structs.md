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

## Summary

- Structs group related variables of different types
- Unions allow different data types to share the same memory location
- Use structs when you need to store multiple related values simultaneously
- Use unions when you need to save memory and only one value is needed at a time
