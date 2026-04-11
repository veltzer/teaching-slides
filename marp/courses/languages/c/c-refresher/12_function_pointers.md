---
tags:
  - languages:c
  - concepts:programming
  - concepts:memory-management
  - concepts:pointers
level: intermediate
category: language
audience:
  - audiences:developers

---
# Function Pointers in C

---

## What is a Function Pointer?

- A variable that stores the address of a function
- Functions have addresses in memory, just like data
- Enables callbacks, dispatch tables, and plugin architectures

```c
#include <stdio.h>

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int main(void) {
    /* Declare a function pointer */
    int (*op)(int, int);

    op = add;
    printf("add(3, 4) = %d\n", op(3, 4));  /* 7 */

    op = sub;
    printf("sub(3, 4) = %d\n", op(3, 4));  /* -1 */

    return 0;
}
```

---

## Function Pointer Memory Model

![Function pointer memory model: stack variable, code segment, dispatch table](svg/courses/languages/c/c-refresher/12_function_pointers/function_pointer_memory_model.svg)

---

## Function Pointer Syntax

```misc
Return type    Pointer name    Parameters
     |              |              |
     v              v              v
   int          (*op)          (int, int)
```

Reading the declaration:
- `op` is a pointer to a function that takes two `int` parameters and returns `int`

Without parentheses: `int *op(int, int)` means a function returning `int *` -- very different!

---

## Simplifying with typedef

```c
#include <stdio.h>

/* Define a type alias for a binary operation */
typedef int (*BinaryOp)(int, int);

int add(int a, int b) { return a + b; }
int mul(int a, int b) { return a * b; }

/* Function that takes a function pointer as parameter */
int apply(BinaryOp op, int a, int b) {
    return op(a, b);
}

int main(void) {
    BinaryOp operations[] = {add, mul};
    const char *names[] = {"add", "mul"};

    for (int i = 0; i < 2; i++) {
        printf("%s(5, 3) = %d\n", names[i], apply(operations[i], 5, 3));
    }

    return 0;
}
```

---

## Callbacks: A Core Pattern

```c
#include <stdio.h>

typedef void (*EventCallback)(const char *event, void *user_data);

struct EventSystem {
    EventCallback callbacks[10];
    void *user_data[10];
    int count;
};

void event_register(struct EventSystem *sys, EventCallback cb, void *data) {
    if (sys->count < 10) {
        sys->callbacks[sys->count] = cb;
        sys->user_data[sys->count] = data;
        sys->count++;
    }
}

void event_fire(struct EventSystem *sys, const char *event) {
    for (int i = 0; i < sys->count; i++) {
        sys->callbacks[i](event, sys->user_data[i]);
    }
}

void logger(const char *event, void *data) {
    const char *prefix = (const char *)data;
    printf("[%s] Event: %s\n", prefix, event);
}

void counter(const char *event, void *data) {
    int *count = (int *)data;
    (*count)++;
    printf("Event count: %d (%s)\n", *count, event);
}

int main(void) {
    struct EventSystem sys = {.count = 0};
    int event_count = 0;

    event_register(&sys, logger, "LOG");
    event_register(&sys, counter, &event_count);

    event_fire(&sys, "startup");
    event_fire(&sys, "data_received");
    event_fire(&sys, "shutdown");

    return 0;
}
```

---

## qsort with Function Pointers

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Employee {
    char name[32];
    int salary;
    int age;
};

/* Sort by salary (descending) */
int cmp_by_salary(const void *a, const void *b) {
    const struct Employee *ea = (const struct Employee *)a;
    const struct Employee *eb = (const struct Employee *)b;
    return (eb->salary > ea->salary) - (eb->salary < ea->salary);
}

/* Sort by name (alphabetical) */
int cmp_by_name(const void *a, const void *b) {
    const struct Employee *ea = (const struct Employee *)a;
    const struct Employee *eb = (const struct Employee *)b;
    return strcmp(ea->name, eb->name);
}

/* Sort by age (ascending) */
int cmp_by_age(const void *a, const void *b) {
    const struct Employee *ea = (const struct Employee *)a;
    const struct Employee *eb = (const struct Employee *)b;
    return (ea->age > eb->age) - (ea->age < eb->age);
}

void print_employees(const struct Employee *emps, int n, const char *label) {
    printf("\n--- %s ---\n", label);
    printf("%-20s %8s %5s\n", "Name", "Salary", "Age");
    for (int i = 0; i < n; i++) {
        printf("%-20s %8d %5d\n", emps[i].name, emps[i].salary, emps[i].age);
    }
}

int main(void) {
    struct Employee team[] = {
        {"Alice",   95000, 34},
        {"Bob",     72000, 28},
        {"Charlie", 88000, 45},
        {"Diana",   105000, 31},
        {"Eve",     72000, 39},
    };
    int n = sizeof(team) / sizeof(team[0]);

    qsort(team, n, sizeof(struct Employee), cmp_by_salary);
    print_employees(team, n, "By Salary (desc)");

    qsort(team, n, sizeof(struct Employee), cmp_by_name);
    print_employees(team, n, "By Name (alpha)");

    qsort(team, n, sizeof(struct Employee), cmp_by_age);
    print_employees(team, n, "By Age (asc)");

    return 0;
}
```

---

## Dispatch Table: Replace Switch Statements

```c
#include <stdio.h>
#include <stdlib.h>

typedef double (*MathFunc)(double, double);

double op_add(double a, double b) { return a + b; }
double op_sub(double a, double b) { return a - b; }
double op_mul(double a, double b) { return a * b; }
double op_div(double a, double b) {
    if (b == 0.0) { fprintf(stderr, "Division by zero\n"); return 0.0; }
    return a / b;
}

int main(void) {
    /* Dispatch table: maps operator character to function */
    struct {
        char symbol;
        MathFunc func;
    } dispatch[] = {
        {'+', op_add},
        {'-', op_sub},
        {'*', op_mul},
        {'/', op_div},
    };
    int n = sizeof(dispatch) / sizeof(dispatch[0]);

    double a = 10.0, b = 3.0;

    for (int i = 0; i < n; i++) {
        double result = dispatch[i].func(a, b);
        printf("%.1f %c %.1f = %.4f\n", a, dispatch[i].symbol, b, result);
    }

    /* vs. the switch approach: */
    /* switch (op) {                     */
    /*     case '+': result = a + b; ... */
    /*     case '-': result = a - b; ... */
    /* }                                 */
    /* Dispatch table is more extensible */

    return 0;
}
```

---

## Signal Handlers

```c
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>

volatile sig_atomic_t running = 1;

void handle_sigint(int sig) {
    (void)sig;  /* suppress unused warning */
    running = 0;
    /* Note: only async-signal-safe functions are allowed here */
    /* printf is NOT safe, write() is */
    const char msg[] = "\nCaught SIGINT, shutting down...\n";
    write(STDOUT_FILENO, msg, sizeof(msg) - 1);
}

void handle_sigterm(int sig) {
    (void)sig;
    running = 0;
}

int main(void) {
    /* Register signal handlers using function pointers */
    struct sigaction sa;
    sa.sa_handler = handle_sigint;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGINT, &sa, NULL);

    signal(SIGTERM, handle_sigterm);

    printf("Running... Press Ctrl+C to stop.\n");
    while (running) {
        printf(".");
        fflush(stdout);
        sleep(1);
    }

    printf("Cleanup complete.\n");
    return 0;
}
```

---

## Generic Map/Filter/Reduce with Function Pointers

```c
#include <stdio.h>
#include <stdlib.h>

typedef int (*MapFunc)(int);
typedef int (*FilterFunc)(int);
typedef int (*ReduceFunc)(int, int);

void array_map(int *arr, int n, MapFunc f) {
    for (int i = 0; i < n; i++) {
        arr[i] = f(arr[i]);
    }
}

int array_filter(int *arr, int n, FilterFunc pred) {
    int j = 0;
    for (int i = 0; i < n; i++) {
        if (pred(arr[i])) {
            arr[j++] = arr[i];
        }
    }
    return j;  /* new size */
}

int array_reduce(const int *arr, int n, ReduceFunc f, int initial) {
    int acc = initial;
    for (int i = 0; i < n; i++) {
        acc = f(acc, arr[i]);
    }
    return acc;
}

int square(int x) { return x * x; }
int is_even(int x) { return x % 2 == 0; }
int sum(int a, int b) { return a + b; }

int main(void) {
    int data[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int n = sizeof(data) / sizeof(data[0]);

    /* Filter: keep only even numbers */
    n = array_filter(data, n, is_even);
    printf("Even: ");
    for (int i = 0; i < n; i++) printf("%d ", data[i]);
    printf("\n");

    /* Map: square each element */
    array_map(data, n, square);
    printf("Squared: ");
    for (int i = 0; i < n; i++) printf("%d ", data[i]);
    printf("\n");

    /* Reduce: sum all elements */
    int total = array_reduce(data, n, sum, 0);
    printf("Sum: %d\n", total);

    return 0;
}
```

---

## A Simple Plugin System

```c
#include <stdio.h>
#include <string.h>

#define MAX_PLUGINS 16

typedef struct {
    const char *name;
    int (*init)(void);
    void (*process)(const char *data);
    void (*shutdown)(void);
} Plugin;

static Plugin plugins[MAX_PLUGINS];
static int plugin_count = 0;

void register_plugin(Plugin p) {
    if (plugin_count < MAX_PLUGINS) {
        plugins[plugin_count++] = p;
    }
}

/* --- Logger Plugin --- */
int logger_init(void) { printf("[Logger] Initialized\n"); return 0; }
void logger_process(const char *data) { printf("[Logger] %s\n", data); }
void logger_shutdown(void) { printf("[Logger] Shut down\n"); }

/* --- Counter Plugin --- */
static int total = 0;
int counter_init(void) { total = 0; printf("[Counter] Initialized\n"); return 0; }
void counter_process(const char *data) {
    total++;
    printf("[Counter] Message #%d: %s\n", total, data);
}
void counter_shutdown(void) { printf("[Counter] Total: %d messages\n", total); }

int main(void) {
    /* Register plugins */
    register_plugin((Plugin){"Logger", logger_init, logger_process, logger_shutdown});
    register_plugin((Plugin){"Counter", counter_init, counter_process, counter_shutdown});

    /* Initialize all plugins */
    for (int i = 0; i < plugin_count; i++) {
        plugins[i].init();
    }

    /* Process data through all plugins */
    const char *messages[] = {"Hello", "World", "Test"};
    for (int m = 0; m < 3; m++) {
        for (int i = 0; i < plugin_count; i++) {
            plugins[i].process(messages[m]);
        }
    }

    /* Shutdown all plugins */
    for (int i = 0; i < plugin_count; i++) {
        plugins[i].shutdown();
    }

    return 0;
}
```

---

## State Machines with Function Pointers

```c
#include <stdio.h>

typedef enum { STATE_IDLE, STATE_RUNNING, STATE_ERROR, STATE_COUNT } State;

typedef State (*StateHandler)(const char *input);

State handle_idle(const char *input) {
    printf("[IDLE] Received: %s\n", input);
    if (input[0] == 's') return STATE_RUNNING;
    if (input[0] == 'e') return STATE_ERROR;
    return STATE_IDLE;
}

State handle_running(const char *input) {
    printf("[RUNNING] Processing: %s\n", input);
    if (input[0] == 'p') return STATE_IDLE;
    if (input[0] == 'e') return STATE_ERROR;
    return STATE_RUNNING;
}

State handle_error(const char *input) {
    printf("[ERROR] Recovery attempt: %s\n", input);
    if (input[0] == 'r') return STATE_IDLE;
    return STATE_ERROR;
}

int main(void) {
    StateHandler handlers[STATE_COUNT] = {
        [STATE_IDLE]    = handle_idle,
        [STATE_RUNNING] = handle_running,
        [STATE_ERROR]   = handle_error,
    };

    State current = STATE_IDLE;
    const char *inputs[] = {"wait", "start", "data", "error", "reset", "start"};
    int n = sizeof(inputs) / sizeof(inputs[0]);

    for (int i = 0; i < n; i++) {
        current = handlers[current](inputs[i]);
    }

    return 0;
}
```

---

## Returning Function Pointers

```c
#include <stdio.h>

typedef double (*MathOp)(double, double);

double add(double a, double b) { return a + b; }
double sub(double a, double b) { return a - b; }
double mul(double a, double b) { return a * b; }

/* Function that returns a function pointer */
MathOp get_operation(char op) {
    switch (op) {
        case '+': return add;
        case '-': return sub;
        case '*': return mul;
        default:  return NULL;
    }
}

/* Without typedef, the signature would be: */
/* double (*get_operation(char op))(double, double); */
/* Extremely hard to read! Always use typedef. */

int main(void) {
    char ops[] = {'+', '-', '*', '?'};

    for (int i = 0; i < 4; i++) {
        MathOp fn = get_operation(ops[i]);
        if (fn != NULL) {
            printf("%.1f %c %.1f = %.1f\n", 10.0, ops[i], 3.0, fn(10.0, 3.0));
        } else {
            printf("Unknown operator: '%c'\n", ops[i]);
        }
    }

    return 0;
}
```

---

## Array of Function Pointers

```c
#include <stdio.h>

void cmd_help(void)    { printf("Available commands: help, status, quit\n"); }
void cmd_status(void)  { printf("System status: OK\n"); }
void cmd_quit(void)    { printf("Goodbye!\n"); }

typedef void (*CommandFunc)(void);

struct Command {
    const char *name;
    CommandFunc func;
    const char *description;
};

int main(void) {
    struct Command commands[] = {
        {"help",   cmd_help,   "Show available commands"},
        {"status", cmd_status, "Show system status"},
        {"quit",   cmd_quit,   "Exit the program"},
    };
    int n = sizeof(commands) / sizeof(commands[0]);

    /* Print help */
    printf("Commands:\n");
    for (int i = 0; i < n; i++) {
        printf("  %-10s - %s\n", commands[i].name, commands[i].description);
    }

    /* Execute a command by name */
    const char *input = "status";
    for (int i = 0; i < n; i++) {
        if (strcmp(input, commands[i].name) == 0) {
            commands[i].func();
            break;
        }
    }

    return 0;
}
```

---

## Function Pointers vs Switch: Comparison

| Aspect | Switch Statement | Function Pointer Table |
|--------|-----------------|----------------------|
| Adding cases | Modify switch code | Add entry to table |
| Runtime selection | Compile-time paths | Fully dynamic |
| Open/Closed | Closed (modify source) | Open (extensible) |
| Performance | Branch prediction | Indirect call |
| Readability | Simple cases | Complex dispatch |
| Plugin support | No | Yes |

Use switch for:
- Small, fixed set of cases
- Performance-critical inner loops

Use function pointers for:
- Extensible systems (plugins, callbacks)
- Strategy pattern
- State machines
- Event-driven architectures

---

## Summary

- Function pointers store addresses of functions and enable dynamic dispatch
- Use `typedef` to make function pointer declarations readable
- Callbacks are the most common use case: `qsort`, event systems, signal handlers
- Dispatch tables replace complex switch statements with extensible arrays
- Function pointers enable plugin systems without modifying core code
- State machines map states to handler functions for clean transitions
- Always check for `NULL` before calling through a function pointer
