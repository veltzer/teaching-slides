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
