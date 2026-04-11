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

![bit_manipulation](svg/courses/embedded/effective-real-time-embedded-c-and-c++/02_embedded_c/bit_manipulation.svg)

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
uart_puts("Hello\n");    // Direct UART
static uint8_t buf[100]; // Static allocation
int32_t x = 314;        // Fixed-point
// Direct hardware control
```

---

## Startup Code

```c
// Reset handler - first code executed
void Reset_Handler(void) {
    // Copy initialized data from flash to RAM
    uint32_t *src = &_sidata;
    uint32_t *dst = &_sdata;
    while (dst < &_edata) {
        *dst++ = *src++;
    }

    // Zero-initialize BSS
    dst = &_sbss;
    while (dst < &_ebss) {
        *dst++ = 0;
    }

    // Call main
    main();
}
```

---

## Vector Table

```c
// Interrupt vector table
__attribute__((section(".vectors")))
const void* vector_table[] = {
    &_estack,           // Initial stack pointer
    Reset_Handler,      // Reset handler
    NMI_Handler,        // NMI handler
    HardFault_Handler,  // Hard fault handler
    // ... more handlers
};
```

---

## Hardware Abstraction

```c
// Low-level hardware access
typedef struct {
    uint32_t CR1;
    uint32_t CR2;
    uint32_t SR;
    uint32_t DR;
} UART_TypeDef;

// High-level abstraction
void uart_init(UART_TypeDef* uart, uint32_t baud) {
    uart->CR1 = 0;  // Disable UART
    uart->CR2 = calculate_baud(baud);
    uart->CR1 = UART_ENABLE | UART_TX_EN | UART_RX_EN;
}
```

---

## Embedded C Best Practices

1. Minimize stack usage
1. Use const for ROM data
1. Avoid recursion
1. Prefer static allocation
1. Use appropriate data types

---

## Stack Usage Optimization

```c
// Bad - large stack usage
void process_data(void) {
    uint8_t buffer[1024];  // 1KB on stack!
    // ...
}

// Good - static allocation
void process_data(void) {
    static uint8_t buffer[1024];  // In .bss
    // ...
}
```

---

## Const Correctness

```c
// String literals in ROM
const char* const messages[] = {
    "Error",
    "Warning",
    "Info"
};

// Lookup table in ROM
const uint16_t sine_table[256] = {
    0, 402, 804, 1206, // ...
};
```

---

## Data Type Selection

```c
// Use exact-width types
uint8_t byte_value;    // Exactly 8 bits
uint16_t word_value;   // Exactly 16 bits
uint32_t dword_value;  // Exactly 32 bits

// Use fast types for loops
uint_fast8_t i;        // Fastest 8-bit type

// Use size_t for sizes
size_t buffer_size;    // Platform-appropriate
```

---

## Power Management

```c
// Enter low-power mode
void enter_sleep_mode(void) {
    // Disable unused peripherals
    disable_uart();
    disable_spi();

    // Configure wake-up sources
    enable_wakeup_pin();

    // Enter sleep
    __WFI();  // Wait for interrupt
}
```

---

## Watchdog Timer

```c
// Initialize watchdog
void watchdog_init(uint32_t timeout_ms) {
    IWDG->KR = 0x5555;  // Enable access
    IWDG->PR = 4;       // Prescaler /64
    IWDG->RLR = timeout_ms * 40;  // Reload value
    IWDG->KR = 0xCCCC;  // Start watchdog
}

// Feed watchdog
void watchdog_feed(void) {
    IWDG->KR = 0xAAAA;  // Reset counter
}
```

---

## Error Handling

```c
// Error codes
typedef enum {
    ERR_OK = 0,
    ERR_TIMEOUT,
    ERR_INVALID_PARAM,
    ERR_BUSY,
    ERR_HARDWARE
} error_t;

// Return error codes
error_t uart_send(const uint8_t* data, size_t len) {
    if (!data || len == 0) {
        return ERR_INVALID_PARAM;
    }
    // ... implementation
    return ERR_OK;
}
```

---

## Debug Support

```c
// Debug macros
#ifdef DEBUG
    #define DBG_PRINT(fmt, ...) \
        debug_printf(fmt, ##__VA_ARGS__)
    #define DBG_ASSERT(cond) \
        if (!(cond)) { debug_break(); }
#else
    #define DBG_PRINT(fmt, ...)
    #define DBG_ASSERT(cond)
#endif
```

---

## Performance Measurement

```c
// Simple profiling
static uint32_t start_time;

void profile_start(void) {
    start_time = get_tick_count();
}

uint32_t profile_end(void) {
    return get_tick_count() - start_time;
}

// Usage
profile_start();
critical_function();
uint32_t cycles = profile_end();
```

---

## Code Size Optimization

```c
// Function inlining control
__attribute__((always_inline))
static inline void critical_function(void) {
    // Always inlined
}

__attribute__((noinline))
void debug_function(void) {
    // Never inlined
}

// Optimize for size
__attribute__((optimize("Os")))
void large_function(void) {
    // Size-optimized
}
```

---

## Summary

1. Real-time C requires deterministic behavior
1. Avoid dynamic memory allocation
1. Use volatile for hardware and shared data
1. Understand platform-specific extensions
1. Optimize for embedded constraints

---

## Key Takeaways

1. **Predictability** over performance
1. **Static** allocation over dynamic
1. **Direct** hardware control
1. **Minimal** resource usage
1. **Robust** error handling
