---
tags:
  - hardware-and-embedded:embedded
  - languages:c
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers

---
# Writing Safer C

---

## Chapter Overview

1. MISRA-C and CWE standards
1. Compiler warnings and static analysis
1. Common pitfalls and vulnerabilities
1. Coding style and banned APIs
1. Debugging preparation techniques

---

## Why Safety Matters

![why_safety_matters](svg/courses/embedded/effective-real-time-embedded-c-and-c++/09_writing_safer_c/why_safety_matters.svg)

---

## MISRA-C Overview

Motor Industry Software Reliability Association

1. Guidelines for critical systems
1. Focus on reliability and portability
1. Mandatory, required, and advisory rules
1. Static analysis friendly

---

## MISRA-C Key Rules

```c
// Rule 14.7: Function shall have single exit
// BAD
int function(int x) {
    if (x < 0) return -1;
    if (x > 100) return -2;
    return x * 2;
}

// GOOD
int function(int x) {
    int result;
    if (x < 0) {
        result = -1;
    } else if (x > 100) {
        result = -2;
    } else {
        result = x * 2;
    }
    return result;
}
```

---

## MISRA Type Safety

```c
// Rule 10.1: Operands shall not be inappropriate types
// BAD
uint8_t a = 5;
int8_t b = -3;
uint8_t c = a + b;  // Mixing signed/unsigned

// GOOD
uint8_t a = 5;
uint8_t b = 3;
uint8_t c = a + b;

// Rule 10.3: Narrow type assignment
// BAD
uint32_t wide = 1000;
uint8_t narrow = wide;  // Implicit narrowing

// GOOD
uint32_t wide = 1000;
uint8_t narrow = (uint8_t)(wide & 0xFF);  // Explicit
```

---

## Control Flow Rules

```c
// Rule 15.5: No more than one break/return per loop
// BAD
for (int i = 0; i < n; i++) {
    if (condition1) break;
    if (condition2) return;
    if (condition3) break;
}

// Rule 16.1: Functions shall not be defined with ellipsis
// BAD
void print_values(int count, ...) { }

// Rule 16.3: Identifiers in prototype and definition must match
// BAD
void func(int x, int y);     // Declaration
void func(int a, int b) { }   // Definition - names differ
```

---

## Pointer Safety

```c
// Rule 18.1: Pointer arithmetic on arrays only
// BAD
int x = 5;
int* p = &x;
p++;  // Undefined!

// GOOD
int arr[10];
int* p = arr;
p++;  // OK - array

// Rule 18.3: Relational operators on pointers to same array
// BAD
int arr1[10], arr2[10];
if (&arr1[5] > &arr2[3]) { }  // Different arrays!

// GOOD
if (&arr1[5] > &arr1[3]) { }  // Same array
```

---

## Common Weakness Enumeration (CWE)

Major vulnerability categories:
1. **CWE-120**: Buffer overflow
1. **CWE-416**: Use after free
1. **CWE-476**: NULL pointer dereference
1. **CWE-190**: Integer overflow
1. **CWE-369**: Divide by zero

---

## Buffer Overflow Prevention

```c
// CWE-120: Classic buffer overflow
// VULNERABLE
void unsafe_copy(char* input) {
    char buffer[32];
    strcpy(buffer, input);  // No bounds check!
}

// SAFE
void safe_copy(const char* input, size_t input_len) {
    char buffer[32];
    if (input_len >= sizeof(buffer)) {
        return;  // Error
    }
    memcpy(buffer, input, input_len);
    buffer[input_len] = '\0';
}

// SAFER - Use strlcpy if available
void safer_copy(const char* input) {
    char buffer[32];
    strlcpy(buffer, input, sizeof(buffer));
}
```

---

## Integer Overflow Protection

```c
// CWE-190: Integer overflow
// VULNERABLE
size_t allocate_array(size_t count, size_t size) {
    void* ptr = malloc(count * size);  // Overflow!
    return ptr;
}

// SAFE
void* safe_allocate(size_t count, size_t size) {
    // Check for overflow
    if (count && size > SIZE_MAX / count) {
        return NULL;
    }
    return malloc(count * size);
}

// Using compiler built-ins
void* safer_allocate(size_t count, size_t size) {
    size_t total;
    if (__builtin_mul_overflow(count, size, &total)) {
        return NULL;
    }
    return malloc(total);
}
```

---

## Null Pointer Checks

```c
// CWE-476: NULL pointer dereference
// VULNERABLE
void process_data(struct data* ptr) {
    ptr->field = 42;  // What if ptr is NULL?
}

// SAFE
void process_data(struct data* ptr) {
    if (!ptr) {
        log_error("NULL pointer");
        return;
    }
    ptr->field = 42;
}

// DEFENSIVE with assertions
void process_data(struct data* ptr) {
    assert(ptr != NULL);  // Debug builds
    if (!ptr) return;     // Release builds
    ptr->field = 42;
}
```

---

## Use After Free Prevention

```c
// CWE-416: Use after free
// VULNERABLE
void vulnerable(void) {
    char* buffer = malloc(SIZE);
    free(buffer);
    buffer[0] = 'A';  // Use after free!
}

// SAFE
void safe(void) {
    char* buffer = malloc(SIZE);
    free(buffer);
    buffer = NULL;  // Defensive nulling
}

// SAFER - Wrapper macro
#define SAFE_FREE(ptr) do { \
    free(ptr); \
    (ptr) = NULL; \
} while(0)
```

---

## Compiler Warning Flags

```makefile
# Essential warnings
CFLAGS += -Wall -Wextra -Wpedantic

# Type safety
CFLAGS += -Wconversion
CFLAGS += -Wsign-conversion
CFLAGS += -Wfloat-equal

# Security
CFLAGS += -Wformat=2
CFLAGS += -Wformat-overflow=2
CFLAGS += -Wformat-truncation=2
CFLAGS += -Wstringop-overflow=4

# Code quality
CFLAGS += -Wshadow
CFLAGS += -Wunused
CFLAGS += -Wuninitialized
CFLAGS += -Wmaybe-uninitialized
```

---

## Additional Safety Warnings

```makefile
# Undefined behavior detection
CFLAGS += -Wstrict-overflow=5
CFLAGS += -Warray-bounds=2
CFLAGS += -Wnull-dereference

# Best practices
CFLAGS += -Wmissing-prototypes
CFLAGS += -Wstrict-prototypes
CFLAGS += -Wold-style-definition
CFLAGS += -Wmissing-include-dirs

# Make warnings errors
CFLAGS += -Werror
```

---

## Static Analysis Tools

```bash
# Clang Static Analyzer
scan-build make

# Cppcheck
cppcheck --enable=all \
         --std=c11 \
         --inline-suppr \
         --quiet \
         src/

# PVS-Studio
pvs-studio-analyzer analyze \
    -o project.log \
    -j4

# PC-lint Plus
pc-lint-plus \
    -i/usr/local/include \
    co-gcc.lnt \
    au-misra3.lnt \
    *.c
```

---

## Runtime Sanitizers

```makefile
# AddressSanitizer - memory errors
CFLAGS_ASAN = -fsanitize=address
CFLAGS_ASAN += -fno-omit-frame-pointer

# UndefinedBehaviorSanitizer
CFLAGS_UBSAN = -fsanitize=undefined

# ThreadSanitizer - race conditions
CFLAGS_TSAN = -fsanitize=thread

# Memory leak detection
CFLAGS_LEAK = -fsanitize=leak

# Combine sanitizers
CFLAGS_DEBUG += $(CFLAGS_ASAN) $(CFLAGS_UBSAN)
```

---

## Defensive Programming

```c
// Range checking
int get_element(const int* array, size_t size, size_t index) {
    if (!array || index >= size) {
        return DEFAULT_VALUE;
    }
    return array[index];
}

// State validation
typedef enum {
    STATE_INIT,
    STATE_READY,
    STATE_BUSY,
    STATE_ERROR
} state_t;

void state_machine(state_t* state, event_t event) {
    // Validate current state
    if (*state < STATE_INIT || *state > STATE_ERROR) {
        *state = STATE_ERROR;
        return;
    }

    // Process event...
}
```

---

## Input Validation

```c
// Validate all external inputs
bool parse_packet(const uint8_t* data, size_t len) {
    if (!data || len < HEADER_SIZE) {
        return false;
    }

    packet_header_t* hdr = (packet_header_t*)data;

    // Check magic number
    if (hdr->magic != PACKET_MAGIC) {
        return false;
    }

    // Check version
    if (hdr->version > MAX_VERSION) {
        return false;
    }

    // Check payload size
    if (hdr->payload_len > len - HEADER_SIZE) {
        return false;
    }

    // Validate CRC
    if (!verify_crc(data, len)) {
        return false;
    }

    return true;
}
```

---

## Banned Functions

```c
// Unsafe string functions - BANNED
strcpy()    // Use strlcpy() or snprintf()
strcat()    // Use strlcat() or snprintf()
sprintf()   // Use snprintf()
gets()      // Use fgets()

// Unsafe memory functions
alloca()    // Stack overflow risk
malloc(0)   // Implementation defined

// Non-reentrant functions
strtok()    // Use strtok_r()
ctime()     // Use ctime_r()
```

---

## Safe Alternatives

```c
// Safe string handling
void safe_string_ops(void) {
    char dest[32];
    const char* src = "Hello, World!";

    // Safe copy
    snprintf(dest, sizeof(dest), "%s", src);

    // Safe concatenation
    char buffer[64] = "Start: ";
    size_t len = strlen(buffer);
    snprintf(buffer + len, sizeof(buffer) - len,
             "%s", src);

    // Safe tokenization
    char* saveptr;
    char* token = strtok_r(buffer, " ", &saveptr);
}
```

---

## Error Handling Patterns

```c
// Error codes enum
typedef enum {
    ERR_OK = 0,
    ERR_NULL_PTR,
    ERR_OUT_OF_RANGE,
    ERR_OVERFLOW,
    ERR_INVALID_STATE,
    ERR_NO_MEMORY
} error_code_t;

// Consistent error handling
error_code_t process_buffer(const uint8_t* buf,
                           size_t len,
                           result_t* result) {
    // Input validation
    if (!buf || !result) {
        return ERR_NULL_PTR;
    }

    if (len > MAX_BUFFER_SIZE) {
        return ERR_OUT_OF_RANGE;
    }

    // Process...

    return ERR_OK;
}
```

---

## Coding Style Guidelines

```c
// Clear naming conventions
typedef struct {
    uint32_t tx_count;      // Transmitted packets
    uint32_t rx_count;      // Received packets
    uint32_t error_count;   // Error counter
} network_stats_t;

// Function naming
bool uart_is_ready(void);        // Query functions
void uart_send_byte(uint8_t b);  // Action functions
error_t uart_init(uint32_t baud); // May fail

// Constants
#define UART_BUFFER_SIZE 256U    // Unsigned suffix
#define UART_TIMEOUT_MS  1000U

// Magic numbers
enum {
    PACKET_HEADER_SIZE = 12,
    PACKET_CRC_SIZE = 4,
    PACKET_MAX_PAYLOAD = 1024
};
```

---

## Assert Usage

```c
// Compile-time assertions
_Static_assert(sizeof(packet_t) == 64,
               "Packet size mismatch");

// Runtime assertions for invariants
void buffer_put(buffer_t* buf, uint8_t data) {
    assert(buf != NULL);
    assert(buf->size > 0);
    assert(buf->count <= buf->size);

    // Defensive check even in release
    if (buf->count >= buf->size) {
        return;  // Buffer full
    }

    buf->data[buf->head] = data;
    buf->head = (buf->head + 1) % buf->size;
    buf->count++;

    // Post-condition
    assert(buf->count <= buf->size);
}
```

---

## Debug Infrastructure

```c
// Debug levels
typedef enum {
    DBG_ERROR = 0,
    DBG_WARN = 1,
    DBG_INFO = 2,
    DBG_DEBUG = 3,
    DBG_TRACE = 4
} debug_level_t;

// Debug macros
#ifdef DEBUG
    #define DBG_PRINT(level, fmt, ...) \
        do { \
            if (level <= g_debug_level) { \
                printf("[%s:%d] " fmt "\n", \
                       __func__, __LINE__, ##__VA_ARGS__); \
            } \
        } while(0)
#else
    #define DBG_PRINT(level, fmt, ...)
#endif

// Usage
DBG_PRINT(DBG_ERROR, "Failed to init: %d", err);
```

---

## Memory Debugging

```c
// Memory tracking
#ifdef DEBUG_MEMORY
typedef struct alloc_info {
    void* ptr;
    size_t size;
    const char* file;
    int line;
    struct alloc_info* next;
} alloc_info_t;

static alloc_info_t* alloc_list = NULL;

void* debug_malloc(size_t size, const char* file, int line) {
    void* ptr = malloc(size);
    if (ptr) {
        alloc_info_t* info = malloc(sizeof(alloc_info_t));
        info->ptr = ptr;
        info->size = size;
        info->file = file;
        info->line = line;
        info->next = alloc_list;
        alloc_list = info;
    }
    return ptr;
}

#define malloc(size) debug_malloc(size, __FILE__, __LINE__)
#endif
```

---

## Unit Testing Support

```c
// Test framework macros
#define TEST_ASSERT(cond) \
    do { \
        if (!(cond)) { \
            printf("FAIL: %s:%d: " #cond "\n", \
                   __FILE__, __LINE__); \
            return false; \
        } \
    } while(0)

#define TEST_ASSERT_EQ(a, b) \
    TEST_ASSERT((a) == (b))

// Test function
bool test_buffer_operations(void) {
    buffer_t buf;
    buffer_init(&buf, 10);

    TEST_ASSERT_EQ(buffer_empty(&buf), true);
    TEST_ASSERT_EQ(buffer_put(&buf, 42), true);
    TEST_ASSERT_EQ(buffer_empty(&buf), false);

    uint8_t value;
    TEST_ASSERT_EQ(buffer_get(&buf, &value), true);
    TEST_ASSERT_EQ(value, 42);

    return true;
}
```

---

## Code Review Checklist

1. **Inputs validated**: All external data checked
1. **Bounds checked**: Array accesses verified
1. **NULL checked**: Pointers validated
1. **Overflow checked**: Integer operations safe
1. **Resources freed**: No memory leaks
1. **Errors handled**: All failures managed

---

## Security Considerations

```c
// Clear sensitive data
void secure_clear(void* ptr, size_t size) {
    volatile uint8_t* p = (volatile uint8_t*)ptr;
    while (size--) {
        *p++ = 0;
    }
}

// Constant-time comparison
bool secure_compare(const uint8_t* a, const uint8_t* b,
                   size_t len) {
    uint8_t result = 0;
    for (size_t i = 0; i < len; i++) {
        result |= a[i] ^ b[i];
    }
    return result == 0;
}

// Stack cleanup
void secure_function(void) {
    uint8_t key[32];
    // Use key...

    // Clear before return
    secure_clear(key, sizeof(key));
}
```

---

## Summary

1. Follow established standards (MISRA-C)
1. Enable all compiler warnings
1. Use static analysis tools
1. Implement defensive programming
1. Prepare comprehensive debugging support

---

## Key Takeaways

1. **Prevention** is cheaper than fixing
1. **Standards** improve reliability
1. **Tools** catch bugs early
1. **Validation** prevents exploits
1. **Testing** ensures correctness
