# Elements of C/C++

---

## Chapter Overview

1. Type specifiers and qualifiers
1. Type conversion and coercion
1. Structures and unions
1. Enums, typedefs, and declarations
1. Number systems and quality

---

## Type Specifiers

Basic type specifiers in C/C++:
1. `char`, `int`, `float`, `double`
1. `short`, `long`, `long long`
1. `signed`, `unsigned`
1. `void`

---

## Type Qualifiers

```c
const int MAX_SIZE = 100;        // Cannot modify
volatile uint32_t* TIMER_REG;    // Can change unexpectedly
restrict int* ptr;               // No aliasing (C99)
_Atomic int counter;             // Atomic operations (C11)
```

---

## Storage Class Specifiers

```c
auto int x;          // Automatic storage (default)
register int y;      // Hint for register storage
static int z;        // Internal linkage/persistent
extern int w;        // External linkage
_Thread_local int t; // Thread-local storage (C11)
```

---

## Type Qualifiers in Embedded

```c
// Hardware register - volatile
volatile uint32_t* const GPIOA_ODR = (uint32_t*)0x40020014;

// ROM constant - const
const uint8_t firmware_version[] = "1.2.3";

// Shared between ISR and main - volatile
volatile bool data_ready = false;
```

---

## Const Volatile Combination

```c
// Read-only hardware register
const volatile uint32_t* STATUS_REG = (uint32_t*)0x40001000;

// Can read but not write
// Hardware can change the value
uint32_t status = *STATUS_REG;  // OK
*STATUS_REG = 0;                // Error!
```

---

## Type Conversion

<svg width="400" height="250" xmlns="http://www.w3.org/2000/svg">
  <text x="200" y="30" text-anchor="middle" font-size="18" font-weight="bold">Type Conversion Hierarchy</text>
  <rect x="150" y="50" width="100" height="30" fill="#ffcccc" stroke="#333"/>
  <text x="200" y="70" text-anchor="middle" font-size="14">long double</text>
  <rect x="150" y="90" width="100" height="30" fill="#ffddcc" stroke="#333"/>
  <text x="200" y="110" text-anchor="middle" font-size="14">double</text>
  <rect x="150" y="130" width="100" height="30" fill="#ffeedd" stroke="#333"/>
  <text x="200" y="150" text-anchor="middle" font-size="14">float</text>
  <rect x="150" y="170" width="100" height="30" fill="#ffffcc" stroke="#333"/>
  <text x="200" y="190" text-anchor="middle" font-size="14">long long</text>
  <rect x="150" y="210" width="100" height="30" fill="#eeffcc" stroke="#333"/>
  <text x="200" y="230" text-anchor="middle" font-size="14">long/int</text>
  <path d="M 200 80 L 200 90" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 200 120 L 200 130" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 200 160 L 200 170" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M 200 200 L 200 210" stroke="#333" stroke-width="2" marker-end="url(#arrowhead)"/>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Implicit Conversions

```c
int i = 42;
float f = 3.14f;
double d;

// Promotion
d = i;    // int to double
d = f;    // float to double

// Arithmetic conversion
d = i + f;  // i promoted to float, result to double

// Dangerous conversions
i = f;      // 3.14 becomes 3 (truncation)
char c = 300;  // Overflow! (300 & 0xFF = 44)
```

---

## Explicit Conversions

```c
// C-style cast
int x = (int)3.14;

// C++ style casts
int* ptr = static_cast<int*>(void_ptr);
const int* cptr = const_cast<const int*>(ptr);
Derived* d = dynamic_cast<Derived*>(base_ptr);
uint32_t addr = reinterpret_cast<uint32_t>(ptr);
```

---

## Type Coercion Pitfalls

```c
// Sign extension problem
int8_t signed_byte = -1;      // 0xFF
uint32_t extended = signed_byte;  // 0xFFFFFFFF!

// Correct way
uint32_t correct = (uint8_t)signed_byte;  // 0x000000FF

// Integer promotion
uint8_t a = 200;
uint8_t b = 100;
uint8_t c = a + b;  // Overflow! Result is 44
```

---

## Structure Layout

```c
struct Example {
    char c;      // 1 byte
    // 3 bytes padding
    int i;       // 4 bytes  
    char d;      // 1 byte
    // 3 bytes padding
};  // Total: 12 bytes
```

<svg width="400" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="40" height="40" fill="#ffcccc" stroke="#333"/>
  <text x="70" y="75" text-anchor="middle" font-size="14">c</text>
  <rect x="90" y="50" width="120" height="40" fill="#e0e0e0" stroke="#333"/>
  <text x="150" y="75" text-anchor="middle" font-size="14">padding</text>
  <rect x="210" y="50" width="80" height="40" fill="#ccffcc" stroke="#333"/>
  <text x="250" y="75" text-anchor="middle" font-size="14">i</text>
  <rect x="290" y="50" width="40" height="40" fill="#ccccff" stroke="#333"/>
  <text x="310" y="75" text-anchor="middle" font-size="14">d</text>
  <rect x="330" y="50" width="70" height="40" fill="#e0e0e0" stroke="#333"/>
  <text x="365" y="75" text-anchor="middle" font-size="14">pad</text>
</svg>

---

## Structure Packing

```c
// Packed structure - no padding
#pragma pack(push, 1)
struct Packed {
    char c;      // 1 byte
    int i;       // 4 bytes  
    char d;      // 1 byte
};  // Total: 6 bytes
#pragma pack(pop)
```
