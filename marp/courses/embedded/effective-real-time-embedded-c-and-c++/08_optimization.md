---
tags:
  - hardware-and-embedded:embedded
  - infrastructure:performance
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers
---
# Optimizations

---

## Chapter Overview

1. Performance optimization strategies
1. Memory optimization techniques
1. Power consumption reduction
1. Code size optimization
1. Compiler optimization insights

---

## Optimization Goals

![optimization_goals](svg/courses/embedded/effective-real-time-embedded-c-and-c++/08_optimization/optimization_goals.svg)

---

## Profiling First

```c
// Simple profiling macro
#define PROFILE_START(name) \
    uint32_t _profile_##name##_start = get_cycle_count()

#define PROFILE_END(name) \
    uint32_t _profile_##name##_cycles = \
        get_cycle_count() - _profile_##name##_start; \
    printf(#name ": %u cycles\n", _profile_##name##_cycles)

// Usage
PROFILE_START(critical_function);
critical_function();
PROFILE_END(critical_function);
```

---

## Cache Optimization

```c
// Poor cache usage - column major
void matrix_multiply_slow(float* C, const float* A,
                         const float* B, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            for (int k = 0; k < n; k++) {
                C[i*n + j] += A[i*n + k] * B[k*n + j];
            }
        }
    }
}

// Better - cache-friendly access
void matrix_multiply_fast(float* C, const float* A,
                         const float* B, int n) {
    for (int i = 0; i < n; i++) {
        for (int k = 0; k < n; k++) {
            float a_ik = A[i*n + k];
            for (int j = 0; j < n; j++) {
                C[i*n + j] += a_ik * B[k*n + j];
            }
        }
    }
}
```

---

## Loop Optimization

```c
// Original loop
for (int i = 0; i < n; i++) {
    sum += array[i];
}

// Loop unrolling
for (int i = 0; i < n - 3; i += 4) {
    sum += array[i] + array[i+1] +
           array[i+2] + array[i+3];
}
// Handle remainder
for (; i < n; i++) {
    sum += array[i];
}

// Software pipelining
int a = array[0];
for (int i = 1; i < n; i++) {
    int b = array[i];
    sum += a;
    a = b;
}
sum += a;
```

---

## Branch Prediction

```c
// Unpredictable branches - slow
for (int i = 0; i < n; i++) {
    if (data[i] >= 128) {  // Random pattern
        sum += data[i];
    }
}

// Sorted data - fast
qsort(data, n, sizeof(int), compare);
for (int i = 0; i < n; i++) {
    if (data[i] >= 128) {  // Predictable
        sum += data[i];
    }
}

// Branchless alternative
for (int i = 0; i < n; i++) {
    sum += (data[i] >= 128) ? data[i] : 0;
    // Or: sum += data[i] & -(data[i] >= 128);
}
```

---

## Lookup Tables

```c
// Slow computation
uint8_t reverse_bits_slow(uint8_t byte) {
    uint8_t result = 0;
    for (int i = 0; i < 8; i++) {
        result <<= 1;
        result |= byte & 1;
        byte >>= 1;
    }
    return result;
}

// Fast lookup
const uint8_t reverse_table[256] = {
    0x00, 0x80, 0x40, 0xC0, 0x20, 0xA0, // ...
};

uint8_t reverse_bits_fast(uint8_t byte) {
    return reverse_table[byte];
}
```

---

## Integer Optimization

```c
// Division by power of 2
int slow_div = value / 16;
int fast_div = value >> 4;  // Only for unsigned!

// Modulo power of 2
int slow_mod = value % 32;
int fast_mod = value & 31;

// Multiply by constant
int slow_mul = value * 10;
int fast_mul = (value << 3) + (value << 1);  // 8x + 2x

// Absolute value without branch
int abs_value = (value ^ (value >> 31)) - (value >> 31);
```

---

## Fixed-Point Arithmetic

```c
// Fixed-point representation (16.16)
typedef int32_t fixed_t;
#define FIXED_SHIFT 16
#define FIXED_ONE (1 << FIXED_SHIFT)

// Conversion
#define FLOAT_TO_FIXED(x) ((fixed_t)((x) * FIXED_ONE))
#define FIXED_TO_FLOAT(x) ((float)(x) / FIXED_ONE)
#define INT_TO_FIXED(x) ((x) << FIXED_SHIFT)

// Operations
fixed_t fixed_mul(fixed_t a, fixed_t b) {
    return ((int64_t)a * b) >> FIXED_SHIFT;
}

fixed_t fixed_div(fixed_t a, fixed_t b) {
    return ((int64_t)a << FIXED_SHIFT) / b;
}
```

---

## SIMD Instructions

```c
// ARM NEON example
#include <arm_neon.h>

void add_arrays_neon(float* dst, const float* a,
                    const float* b, int n) {
    int i;
    for (i = 0; i < n - 3; i += 4) {
        float32x4_t va = vld1q_f32(&a[i]);
        float32x4_t vb = vld1q_f32(&b[i]);
        float32x4_t vr = vaddq_f32(va, vb);
        vst1q_f32(&dst[i], vr);
    }
    // Handle remainder
    for (; i < n; i++) {
        dst[i] = a[i] + b[i];
    }
}
```

---

## Memory Access Patterns

```c
// Structure of Arrays (SoA) - cache friendly
typedef struct {
    float x[1000];
    float y[1000];
    float z[1000];
} vectors_soa_t;

// Array of Structures (AoS) - less cache friendly
typedef struct {
    float x, y, z;
} vector_t;
vector_t vectors_aos[1000];

// Processing SoA - better locality
void process_soa(vectors_soa_t* v) {
    for (int i = 0; i < 1000; i++) {
        v->x[i] *= 2.0f;  // All x's in cache
    }
}
```

---

## Alignment Optimization

```c
// Ensure alignment for SIMD
typedef struct {
    float data[4];
} __attribute__((aligned(16))) aligned_vector_t;

// Aligned allocation
void* aligned_malloc(size_t size, size_t alignment) {
    void* p1;
    void** p2;
    int offset = alignment - 1 + sizeof(void*);

    p1 = malloc(size + offset);
    if (!p1) return NULL;

    p2 = (void**)(((size_t)p1 + offset) & ~(alignment - 1));
    p2[-1] = p1;
    return p2;
}

void aligned_free(void* p) {
    free(((void**)p)[-1]);
}
```

---

## Function Inlining

```c
// Force inline
__attribute__((always_inline))
static inline int max(int a, int b) {
    return a > b ? a : b;
}

// Prevent inline
__attribute__((noinline))
void debug_function(void) {
    // Keep for debugging
}

// Compiler decides
inline int common_function(int x) {
    return x * 2;
}
```

---

## Constant Propagation

```c
// Enable constant folding
#define BUFFER_SIZE 256
#define ELEMENT_SIZE 4
#define TOTAL_SIZE (BUFFER_SIZE * ELEMENT_SIZE)

// Compile-time computation
static const int lookup[] = {
    [0] = 0,
    [1] = 1,
    [2] = 1,
    [3] = 2,
    // ...
};

// Template-like macros
#define MAKE_BUFFER(type, size) \
    static type buffer_##type[size]

MAKE_BUFFER(uint8_t, 256);
MAKE_BUFFER(uint32_t, 64);
```

---

## Power Optimization

```c
// Clock gating
void enter_low_power(void) {
    // Disable unused peripherals
    RCC->APB1ENR &= ~(RCC_APB1ENR_TIM2EN |
                      RCC_APB1ENR_USART2EN);

    // Reduce clock frequency
    set_system_clock(HSI_8MHZ);

    // Enter sleep mode
    __WFI();  // Wait for interrupt
}

// Dynamic voltage/frequency scaling
void adjust_performance(int load) {
    if (load > 80) {
        set_system_clock(HSE_168MHZ);
        set_voltage_scale(SCALE_1);
    } else if (load < 20) {
        set_system_clock(HSI_16MHZ);
        set_voltage_scale(SCALE_3);
    }
}
```

---

## Interrupt Latency

```c
// Fast interrupt handler
__attribute__((interrupt("FIQ")))
void fast_interrupt(void) {
    // Minimal processing
    flag = 1;
    // Defer work to main loop
}

// Zero-latency interrupts (Cortex-M)
void configure_zero_latency_irq(IRQn_Type irq) {
    NVIC_SetPriority(irq, 0);  // Highest priority

    // Configure BASEPRI for critical sections
    // Allows priority 0 interrupts
    __set_BASEPRI(1 << (8 - __NVIC_PRIO_BITS));
}
```

---

## DMA Optimization

```c
// Double buffering with DMA
typedef struct {
    uint8_t buffer0[BUFFER_SIZE];
    uint8_t buffer1[BUFFER_SIZE];
    volatile int active_buffer;
} dma_buffers_t;

void dma_complete_handler(void) {
    static dma_buffers_t* bufs = &dma_buffers;

    // Switch buffers
    bufs->active_buffer ^= 1;

    // Start next transfer immediately
    DMA_SetMemory(bufs->active_buffer ?
                  bufs->buffer1 : bufs->buffer0);
    DMA_Start();

    // Process completed buffer in background
    process_buffer(bufs->active_buffer ?
                   bufs->buffer0 : bufs->buffer1);
}
```

---

## String Optimization

```c
// Optimized string length
size_t strlen_fast(const char* str) {
    const char* s = str;

    // Align to word boundary
    while (((uintptr_t)s & 3) && *s) s++;

    // Check 4 bytes at a time
    const uint32_t* w = (const uint32_t*)s;
    while (!(((*w) - 0x01010101) & ~(*w) & 0x80808080)) {
        w++;
    }

    // Find exact byte
    s = (const char*)w;
    while (*s) s++;

    return s - str;
}
```

---

## Memory Copy Optimization

```c
void* memcpy_optimized(void* dst, const void* src, size_t n) {
    uint8_t* d = (uint8_t*)dst;
    const uint8_t* s = (const uint8_t*)src;

    // Copy bytes until aligned
    while (((uintptr_t)d & 3) && n) {
        *d++ = *s++;
        n--;
    }

    // Copy words
    uint32_t* dw = (uint32_t*)d;
    const uint32_t* sw = (const uint32_t*)s;
    while (n >= 16) {
        *dw++ = *sw++;
        *dw++ = *sw++;
        *dw++ = *sw++;
        *dw++ = *sw++;
        n -= 16;
    }

    // Copy remaining bytes
    d = (uint8_t*)dw;
    s = (const uint8_t*)sw;
    while (n--) {
        *d++ = *s++;
    }

    return dst;
}
```

---

## Compiler Hints

```c
// Branch prediction hints
#define likely(x)   __builtin_expect(!!(x), 1)
#define unlikely(x) __builtin_expect(!!(x), 0)

void process_data(int* data, int n) {
    for (int i = 0; i < n; i++) {
        if (likely(data[i] > 0)) {
            // Common case
            data[i] *= 2;
        } else if (unlikely(data[i] < -1000)) {
            // Rare error case
            handle_error();
        }
    }
}

// Prefetch hints
void process_large_array(int* arr, int n) {
    for (int i = 0; i < n; i++) {
        __builtin_prefetch(&arr[i + 8], 0, 3);
        // Process arr[i]
    }
}
```

---

## Link-Time Optimization

```c
// Whole program optimization
// file1.c
int helper(int x) {
    return x * 2;
}

// file2.c
extern int helper(int x);
int process(int y) {
    return helper(y) + 1;  // Can be inlined with LTO
}

// Build with:
// gcc -flto -c file1.c file2.c
// gcc -flto file1.o file2.o -o program
```

---

## Profile-Guided Optimization

```makefile
# Step 1: Build with profiling
$(TARGET).prof:
    $(CC) $(CFLAGS) -fprofile-generate $(SRCS) -o $@

# Step 2: Run with representative data
profile-run: $(TARGET).prof
    ./$(TARGET).prof < typical_input.dat

# Step 3: Rebuild with profile data
$(TARGET).opt:
    $(CC) $(CFLAGS) -fprofile-use $(SRCS) -o $@
```

---

## Code Size Optimization

```c
// Merge identical code sequences
__attribute__((cold))
void error_handler(const char* msg) {
    // Rarely executed - out of hot path
    log_error(msg);
    reset_system();
}

// Use smaller instructions
// Instead of:
if (x == 0) { y = 0; }
// Use:
y &= -(x != 0);

// Tail call optimization
int recursive(int n) {
    if (n <= 1) return 1;
    return recursive(n - 1);  // Becomes jump, not call
}
```

---

## Space-Time Tradeoffs

```c
// Computing vs storing
// Option 1: Compute on demand (save space)
uint16_t get_crc(const uint8_t* data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc = update_crc(crc, data[i]);
    }
    return crc;
}

// Option 2: Precompute table (save time)
const uint16_t crc_table[256] = { /* ... */ };
uint16_t get_crc_fast(const uint8_t* data, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc = (crc << 8) ^ crc_table[(crc >> 8) ^ data[i]];
    }
    return crc;
}
```

---

## Lazy Evaluation

```c
// Defer computation until needed
typedef struct {
    int (*compute)(void* data);
    void* data;
    int cached_result;
    bool computed;
} lazy_int_t;

int lazy_get(lazy_int_t* lazy) {
    if (!lazy->computed) {
        lazy->cached_result = lazy->compute(lazy->data);
        lazy->computed = true;
    }
    return lazy->cached_result;
}
```

---

## Memory Pool Optimization

```c
// Type-specific pools
#define DECLARE_POOL(type, count) \
    static struct { \
        type items[count]; \
        uint32_t free_map[(count + 31) / 32]; \
    } type##_pool; \
    \
    type* alloc_##type(void) { \
        int idx = __builtin_ffs(type##_pool.free_map[0]); \
        if (idx) { \
            type##_pool.free_map[0] &= ~(1U << (idx-1)); \
            return &type##_pool.items[idx-1]; \
        } \
        return NULL; \
    }

DECLARE_POOL(task_t, 32)
DECLARE_POOL(buffer_t, 16)
```

---

## Optimization Checklist

1. **Profile first** - measure before optimizing
1. **Algorithm first** - O(n) beats optimized O(n²)
1. **Memory patterns** - cache-friendly access
1. **Compiler flags** - appropriate optimization level
1. **Platform specific** - use hardware features

---

## Common Anti-Patterns

```c
// BAD: Premature optimization
register int i;  // Compiler knows better

// BAD: Over-optimization
#define MULTIPLY_BY_2(x) ((x) << 1)  // Compiler does this

// BAD: Assuming optimization
volatile int x = 5;
if (x == 5) {  // May not be true!
    // ...
}

// BAD: Breaking readability
int a=b<<2+c&0xFF^d;  // What does this do?
```

---

## Benchmarking Best Practices

```c
// Proper benchmarking
void benchmark_function(void (*func)(void),
                       const char* name) {
    // Warm up cache
    func();

    // Multiple runs
    uint32_t times[100];
    for (int i = 0; i < 100; i++) {
        uint32_t start = get_cycle_count();
        func();
        times[i] = get_cycle_count() - start;
    }

    // Calculate statistics
    uint32_t min = times[0], max = times[0], sum = 0;
    for (int i = 0; i < 100; i++) {
        if (times[i] < min) min = times[i];
        if (times[i] > max) max = times[i];
        sum += times[i];
    }

    printf("%s: min=%u, max=%u, avg=%u\n",
           name, min, max, sum/100);
}
```

---

## Platform-Specific Features

```c
// ARM Cortex-M bit manipulation
uint32_t bit_reverse(uint32_t value) {
    uint32_t result;
    __asm__("rbit %0, %1" : "=r"(result) : "r"(value));
    return result;
}

// Count leading zeros
int clz(uint32_t value) {
    return __builtin_clz(value);
}

// Saturating arithmetic
int16_t saturate_add(int16_t a, int16_t b) {
    int32_t result = (int32_t)a + b;
    if (result > INT16_MAX) return INT16_MAX;
    if (result < INT16_MIN) return INT16_MIN;
    return result;
}
```

---

## Summary

1. Profile before optimizing
1. Understand hardware capabilities
1. Balance different optimization goals
1. Use appropriate algorithms and data structures
1. Leverage compiler and platform features

---

## Key Takeaways

1. **Measure** performance scientifically
1. **Cache** behavior dominates performance
1. **Algorithm** choice matters most
1. **Trade-offs** exist between goals
1. **Maintainability** matters too
