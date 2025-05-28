# Embedded C

---

## Chapter Overview

1. Real-time C programming
1. Embedded-specific C features
1. Writing code in kernel space
1. Hardware-software interface

---

## Real-Time C Programming

Real-time systems require predictable execution timing and deterministic behavior.

---

## Deterministic Code

```c
// Non-deterministic
void process_data() {
    data = malloc(SIZE);  // Unknown time
    sort(data);          // Variable time
    free(data);          // Unknown time
}

// Deterministic
void process_data() {
    static uint8_t data[SIZE];  // Fixed memory
    bubble_sort(data, SIZE);    // Known time
}
```

---

## Avoiding Dynamic Memory

1. Use static allocation
1. Implement memory pools
1. Fixed-size buffers
1. Stack-based allocation

---

## Memory Pool Example

```c
#define POOL_SIZE 10
#define BLOCK_SIZE 64

typedef struct {
    uint8_t data[BLOCK_SIZE];
    bool in_use;
} block_t;

static block_t pool[POOL_SIZE];

void* pool_alloc(void) {
    for (int i = 0; i < POOL_SIZE; i++) {
        if (!pool[i].in_use) {
            pool[i].in_use = true;
            return pool[i].data;
        }
    }
    return NULL;
}
```

---

## Interrupt-Safe Code

```c
volatile uint32_t counter = 0;

void interrupt_handler(void) {
    counter++;  // Atomic on 32-bit systems
}

void main_loop(void) {
    uint32_t local_counter;

    // Critical section
    __disable_irq();
    local_counter = counter;
    __enable_irq();

    process(local_counter);
}
```

---

## Volatile Keyword

Essential for:
1. Memory-mapped I/O registers
1. Variables modified in ISRs
1. Variables shared between tasks

```c
volatile uint32_t* const UART_STATUS = (uint32_t*)0x40001000;
volatile bool data_ready = false;
```

---

## Embedded C Extensions

1. Interrupt function attributes
1. Inline assembly
1. Pragma directives
1. Memory sections

---

## Interrupt Function Declaration

```c
// GCC ARM Cortex-M
void __attribute__((interrupt)) TIM2_IRQHandler(void) {
    // Handle timer interrupt
}

// IAR
#pragma vector = TIM2_IRQn
__interrupt void TIM2_IRQHandler(void) {
    // Handle timer interrupt
}
```

---

## Inline Assembly

```c
// GCC inline assembly
static inline void nop(void) {
    __asm__ volatile ("nop");
}

// Disable interrupts
static inline uint32_t disable_interrupts(void) {
    uint32_t primask;
    __asm__ volatile (
        "mrs %0, primask\n"
        "cpsid i"
        : "=r" (primask)
    );
    return primask;
}
```

---

## Memory Sections

```c
// Place in specific memory section
__attribute__((section(".fastcode")))
void critical_function(void) {
    // Time-critical code
}

// Place in RAM for faster execution
__attribute__((section(".data")))
const uint8_t lookup_table[256] = { /* ... */ };
```

---

## Bit Manipulation

<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="300" height="40" fill="#f0f0f0" stroke="#333"/>
  <text x="200" y="30" text-anchor="middle" font-size="16">8-bit Register</text>
  <g id="bits">
    <rect x="50" y="50" width="37.5" height="40" fill="#ffcccc" stroke="#333"/>
    <text x="68.75" y="75" text-anchor="middle" font-size="14">7</text>
    <rect x="87.5" y="50" width="37.5" height="40" fill="#ccffcc" stroke="#333"/>
    <text x="106.25" y="75" text-anchor="middle" font-size="14">6</text>
    <rect x="125" y="50" width="37.5" height="40" fill="#ccccff" stroke="#333"/>
    <text x="143.75" y="75" text-anchor="middle" font-size="14">5</text>
    <rect x="162.5" y="50" width="37.5" height="40" fill="#ffffcc" stroke="#333"/>
    <text x="181.25" y="75" text-anchor="middle" font-size="14">4</text>
    <rect x="200" y="50" width="37.5" height="40" fill="#ffccff" stroke="#333"/>
    <text x="218.75" y="75" text-anchor="middle" font-size="14">3</text>
    <rect x="237.5" y="50" width="37.5" height="40" fill="#ccffff" stroke="#333"/>
    <text x="256.25" y="75" text-anchor="middle" font-size="14">2</text>
    <rect x="275" y="50" width="37.5" height="40" fill="#ffcccc" stroke="#333"/>
    <text x="293.75" y="75" text-anchor="middle" font-size="14">1</text>
    <rect x="312.5" y="50" width="37.5" height="40" fill="#ccffcc" stroke="#333"/>
    <text x="331.25" y="75" text-anchor="middle" font-size="14">0</text>
  </g>
  <text x="200" y="120" text-anchor="middle" font-size="14">MSB → LSB</text>
</svg>

---

## Bit Operations

```c
#define BIT(x) (1UL << (x))
#define SET_BIT(reg, bit) ((reg) |= BIT(bit))
#define CLEAR_BIT(reg, bit) ((reg) &= ~BIT(bit))
#define TOGGLE_BIT(reg, bit) ((reg) ^= BIT(bit))
#define READ_BIT(reg, bit) (((reg) >> (bit)) & 1)

// Usage
SET_BIT(PORTA, 5);      // Set bit 5
CLEAR_BIT(PORTB, 3);    // Clear bit 3
if (READ_BIT(PINC, 7))  // Check bit 7
```

---

## Register Access Patterns

```c
// Direct register access
#define GPIOA_BASE 0x40020000
#define GPIOA ((GPIO_TypeDef*)GPIOA_BASE)

// Structured register access
typedef struct {
    volatile uint32_t MODER;
    volatile uint32_t OTYPER;
    volatile uint32_t OSPEEDR;
    volatile uint32_t PUPDR;
    volatile uint32_t IDR;
    volatile uint32_t ODR;
    volatile uint32_t BSRR;
    volatile uint32_t LCKR;
    volatile uint32_t AFR[2];
} GPIO_TypeDef;
```

---

## Writing Code in Kernel Space

1. No standard library
1. Limited stack size
1. No floating-point (usually)
1. Direct hardware access

---

## Kernel Space Restrictions

```c
// Cannot use:
printf("Hello\n");        // No stdio
malloc(100);             // No heap
float x = 3.14;         // No FPU
system("ls");           // No OS calls

// Must use:
```
