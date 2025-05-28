# Memory Management Architecture

---

## Chapter Overview

1. Caching mechanisms
1. Hardware memory management
1. Program sections
1. Memory mapping
1. Dynamic allocation strategies

---

## Memory Hierarchy

<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  <text x="200" y="30" text-anchor="middle" font-size="18" font-weight="bold">Memory Hierarchy</text>
  <polygon points="200,50 100,100 300,100" fill="#ffcccc" stroke="#333" stroke-width="2"/>
  <text x="200" y="80" text-anchor="middle" font-size="14">CPU Registers</text>
  <polygon points="200,100 80,150 320,150" fill="#ffddcc" stroke="#333" stroke-width="2"/>
  <text x="200" y="130" text-anchor="middle" font-size="14">L1 Cache</text>
  <polygon points="200,150 60,200 340,200" fill="#ffeedd" stroke="#333" stroke-width="2"/>
  <text x="200" y="180" text-anchor="middle" font-size="14">L2/L3 Cache</text>
  <polygon points="200,200 40,250 360,250" fill="#ffffcc" stroke="#333" stroke-width="2"/>
  <text x="200" y="230" text-anchor="middle" font-size="14">RAM</text>
  <polygon points="200,250 20,300 380,300" fill="#eeffcc" stroke="#333" stroke-width="2"/>
  <text x="200" y="280" text-anchor="middle" font-size="14">Storage</text>
</svg>

---

## Cache Fundamentals

1. **Temporal Locality**: Recently accessed data likely accessed again
1. **Spatial Locality**: Nearby data likely accessed soon
1. **Cache Line**: Basic unit of cache (typically 32-64 bytes)

---

## Cache Architecture

```c
// Cache-friendly access pattern
void process_matrix_row_major(int matrix[N][M]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < M; j++) {
            matrix[i][j]++;  // Sequential access
        }
    }
}

// Cache-unfriendly pattern
void process_matrix_col_major(int matrix[N][M]) {
    for (int j = 0; j < M; j++) {
        for (int i = 0; i < N; i++) {
            matrix[i][j]++;  // Strided access
        }
    }
}
```

---

## Cache Line Effects

<svg width="400" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="200" y="30" text-anchor="middle" font-size="16" font-weight="bold">64-byte Cache Line</text>
  <rect x="50" y="60" width="300" height="40" fill="#f0f0f0" stroke="#333"/>
  <line x1="50" y1="60" x2="50" y2="100" stroke="#333" stroke-width="2"/>
  <line x1="125" y1="60" x2="125" y2="100" stroke="#333" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="200" y1="60" x2="200" y2="100" stroke="#333" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="275" y1="60" x2="275" y2="100" stroke="#333" stroke-width="1" stroke-dasharray="2,2"/>
  <line x1="350" y1="60" x2="350" y2="100" stroke="#333" stroke-width="2"/>
  <text x="87.5" y="85" text-anchor="middle" font-size="12">16 bytes</text>
  <text x="162.5" y="85" text-anchor="middle" font-size="12">16 bytes</text>
  <text x="237.5" y="85" text-anchor="middle" font-size="12">16 bytes</text>
  <text x="312.5" y="85" text-anchor="middle" font-size="12">16 bytes</text>
  <text x="200" y="130" text-anchor="middle" font-size="14">One cache line fetch</text>
</svg>

---

## Cache Optimization Techniques

```c
// Structure padding for cache alignment
typedef struct {
    uint32_t frequently_used;
    uint32_t also_frequent;
    // Ensure next member starts on cache line
    uint8_t padding[56];
    uint32_t rarely_used;
} cache_aligned_t __attribute__((aligned(64)));
```

---

## False Sharing

```c
// BAD: False sharing between threads
struct {
    int thread1_counter;  // Same cache line!
    int thread2_counter;
} shared;

// GOOD: Avoid false sharing
struct {
    int thread1_counter;
    char padding[60];     // Force different cache lines
    int thread2_counter;
} shared_better;
```

---

## Data Cache vs Instruction Cache

```c
// Keep hot code together
__attribute__((hot))
void frequently_called() {
    // Performance critical
}

__attribute__((cold))
void error_handler() {
    // Rarely executed
}

// Group related functions
__attribute__((section(".fastcode")))
void time_critical_function() {
    // In fast memory
}
```

---

## Hardware Memory Management

1. **MMU** (Memory Management Unit)
1. **MPU** (Memory Protection Unit)
1. **DMA** (Direct Memory Access)
1. **Cache Controllers**

---

## Memory Protection Unit (MPU)

```c
// Configure MPU region
typedef struct {
    uint32_t base_addr;
    uint32_t size;
    uint32_t access_permission;
    uint32_t attributes;
} mpu_region_t;

void configure_mpu_region(uint8_t region_num,
                         const mpu_region_t* config) {
    MPU->RNR = region_num;
    MPU->RBAR = config->base_addr;
    MPU->RASR = config->size |
                config->access_permission |
                config->attributes |
                MPU_RASR_ENABLE;
}
```

---

## Memory Regions

<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  <text x="200" y="30" text-anchor="middle" font-size="16" font-weight="bold">Typical Memory Map</text>
  <rect x="100" y="50" width="200" height="40" fill="#ffcccc" stroke="#333"/>
  <text x="200" y="75" text-anchor="middle" font-size="14">0xFFFFFFFF - System</text>
  <rect x="100" y="90" width="200" height="40" fill="#ccffcc" stroke="#333"/>
  <text x="200" y="115" text-anchor="middle" font-size="14">0xE0000000 - Peripherals</text>
  <rect x="100" y="130" width="200" height="40" fill="#ccccff" stroke="#333"/>
  <text x="200" y="155" text-anchor="middle" font-size="14">0x20000000 - SRAM</text>
  <rect x="100" y="170" width="200" height="40" fill="#ffffcc" stroke="#333"/>
  <text x="200" y="195" text-anchor="middle" font-size="14">0x08000000 - Flash</text>
  <rect x="100" y="210" width="200" height="40" fill="#ffccff" stroke="#333"/>
  <text x="200" y="235" text-anchor="middle" font-size="14">0x00000000 - Aliased</text>
</svg>

---

## Program Sections

```c
// Different sections in memory
const char rodata[] = "String literal";     // .rodata
int initialized = 42;                        // .data
int uninitialized;                          // .bss
const int flash_const = 100;                // .rodata

void function(void) {                       // .text
    static int static_var = 10;             // .data
    int local_var;                          // stack
    int* dynamic = malloc(100);             // heap
}
```

---

## Linker Script Sections

```ld
MEMORY {
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 256K
    RAM (rwx)   : ORIGIN = 0x20000000, LENGTH = 64K
}

SECTIONS {
    .text : {
        *(.vectors)
        *(.text*)
        *(.rodata*)
    } > FLASH

    .data : {
        *(.data*)
    } > RAM AT > FLASH

    .bss : {
        *(.bss*)
        *(COMMON)
    } > RAM
}
```

---

## Section Attributes

```c
// Place variable in specific section
__attribute__((section(".ccmram")))
uint8_t fast_buffer[1024];

// Keep in RAM for fast execution
__attribute__((section(".ramfunc")))
void critical_isr(void) {
    // Runs from RAM
}

// Constant data in flash
__attribute__((section(".rodata")))
const uint16_t lookup_table[256] = { /* ... */ };
```

---

## Memory Mapping in Detail

<svg width="400" height="250" xmlns="http://www.w3.org/2000/svg">
  <text x="200" y="30" text-anchor="middle" font-size="16" font-weight="bold">Program Memory Layout</text>
  <rect x="100" y="50" width="200" height="30" fill="#ffcccc" stroke="#333"/>
  <text x="200" y="70" text-anchor="middle" font-size="12">Stack ↓</text>
  <rect x="100" y="80" width="200" height="40" fill="#ffffff" stroke="#333"/>
  <text x="200" y="105" text-anchor="middle" font-size="12">Free Space</text>
  <rect x="100" y="120" width="200" height="30" fill="#ccffcc" stroke="#333"/>
  <text x="200" y="140" text-anchor="middle" font-size="12">Heap ↑</text>
  <rect x="100" y="150" width="200" height="30" fill="#ccccff" stroke="#333"/>
  <text x="200" y="170" text-anchor="middle" font-size="12">.bss (zeroed)</text>
  <rect x="100" y="180" width="200" height="30" fill="#ffffcc" stroke="#333"/>
  <text x="200" y="200" text-anchor="middle" font-size="12">.data (initialized)</text>
  <rect x="100" y="210" width="200" height="30" fill="#ffccff" stroke="#333"/>
  <text x="200" y="230" text-anchor="middle" font-size="12">.text (code)</text>
</svg>

---

## Stack Management

```c
// Check stack usage
#define STACK_CANARY 0xDEADBEEF

void init_stack_monitor(uint32_t* stack_bottom) {
    // Fill stack with pattern
    uint32_t* ptr = stack_bottom;
    while (ptr < &_estack) {
        *ptr++ = STACK_CANARY;
    }
}

size_t check_stack_usage(uint32_t* stack_bottom) {
    uint32_t* ptr = stack_bottom;
    while (*ptr == STACK_CANARY && ptr < &_estack) {
        ptr++;
    }
    return (uint8_t*)&_estack - (uint8_t*)ptr;
}
```

---

## Heap Implementation

```c
typedef struct block {
    size_t size;
    struct block* next;
    bool free;
} block_t;

static block_t* heap_start = NULL;

void* my_malloc(size_t size) {
    block_t* current = heap_start;

    // First-fit algorithm
    while (current) {
        if (current->free && current->size >= size) {
            current->free = false;
            return (uint8_t*)current + sizeof(block_t);
        }
        current = current->next;
    }
    return NULL;
}
```

---

## Memory Pool Allocator

```c
typedef struct {
    uint8_t* pool;
    size_t block_size;
    size_t num_blocks;
    uint32_t free_map;  // Bitmap for 32 blocks
} memory_pool_t;

void* pool_alloc(memory_pool_t* pool) {
    int idx = __builtin_ffs(pool->free_map) - 1;
    if (idx >= 0) {
        pool->free_map &= ~(1U << idx);
        return pool->pool + (idx * pool->block_size);
    }
    return NULL;
}
```

---

## Fixed Block Allocator

```c
#define BLOCK_SIZE 64
#define NUM_BLOCKS 100

typedef struct free_block {
    struct free_block* next;
} free_block_t;

static uint8_t memory_pool[BLOCK_SIZE * NUM_BLOCKS];
static free_block_t* free_list;

void init_allocator(void) {
    free_list = (free_block_t*)memory_pool;

    for (int i = 0; i < NUM_BLOCKS - 1; i++) {
        free_block_t* block = (free_block_t*)
                              (memory_pool + i * BLOCK_SIZE);
        block->next = (free_block_t*)
                      (memory_pool + (i + 1) * BLOCK_SIZE);
    }
}
```

---

## DMA Operations

```c
// Configure DMA for memory-to-memory transfer
void configure_dma(uint32_t* src, uint32_t* dst,
                   size_t count) {
    DMA1_Channel1->CCR &= ~DMA_CCR_EN;  // Disable

    DMA1_Channel1->CPAR = (uint32_t)src;
    DMA1_Channel1->CMAR = (uint32_t)dst;
    DMA1_Channel1->CNDTR = count;

    DMA1_Channel1->CCR = DMA_CCR_MEM2MEM |  // Mem to mem
                         DMA_CCR_PINC |      // Increment
                         DMA_CCR_MINC |
                         DMA_CCR_PL_HIGH |   // Priority
                         DMA_CCR_TCIE;       // Complete IRQ

    DMA1_Channel1->CCR |= DMA_CCR_EN;       // Start
}
```

---

## Memory Barriers

```c
// Ensure memory operations complete
#define DMB() __asm__ volatile ("dmb" ::: "memory")
#define DSB() __asm__ volatile ("dsb" ::: "memory")
#define ISB() __asm__ volatile ("isb" ::: "memory")

void write_peripheral(volatile uint32_t* reg,
                      uint32_t value) {
    *reg = value;
    DSB();  // Ensure write completes
}
```

---

## Memory-Mapped I/O

```c
// Define peripheral registers
typedef struct {
    volatile uint32_t CR;
    volatile uint32_t SR;
    volatile uint32_t DR;
} UART_TypeDef;

#define UART1_BASE 0x40011000
#define UART1 ((UART_TypeDef*)UART1_BASE)

// Access registers
void uart_send(uint8_t data) {
    while (!(UART1->SR & UART_SR_TXE));
    UART1->DR = data;
}
```

---

## Alignment Requirements

```c
// Natural alignment
typedef struct {
    uint8_t  a;  // offset 0
    uint16_t b;  // offset 2 (aligned)
    uint32_t c;  // offset 4 (aligned)
} aligned_struct_t;

// Force alignment
typedef struct {
    uint8_t data[128];
} __attribute__((aligned(16))) aligned_buffer_t;

// Check alignment
#define IS_ALIGNED(ptr, align) \
    (((uintptr_t)(ptr) & ((align) - 1)) == 0)
```

---

## Memory Access Patterns

```c
// Sequential access - cache friendly
void sequential_sum(const int* arr, size_t n) {
    int sum = 0;
    for (size_t i = 0; i < n; i++) {
        sum += arr[i];  // Predictable pattern
    }
}

// Random access - cache unfriendly
void random_sum(const int* arr, const size_t* indices,
                size_t n) {
    int sum = 0;
    for (size_t i = 0; i < n; i++) {
        sum += arr[indices[i]];  // Unpredictable
    }
}
```

---

## Memory Bandwidth Optimization

```c
// Unroll loops for better throughput
void memcpy_optimized(void* dst, const void* src,
                      size_t n) {
    uint32_t* d = (uint32_t*)dst;
    const uint32_t* s = (const uint32_t*)src;

    // Copy 32 bytes at a time
    while (n >= 32) {
        *d++ = *s++; *d++ = *s++;
        *d++ = *s++; *d++ = *s++;
        *d++ = *s++; *d++ = *s++;
        *d++ = *s++; *d++ = *s++;
        n -= 32;
    }

    // Handle remainder
    uint8_t* d8 = (uint8_t*)d;
    const uint8_t* s8 = (const uint8_t*)s;
    while (n--) *d8++ = *s8++;
}
```

---

## Memory Profiling

```c
typedef struct {
    size_t total_allocated;
    size_t current_usage;
    size_t peak_usage;
    size_t allocation_count;
} memory_stats_t;

static memory_stats_t stats;

void* tracked_malloc(size_t size) {
    void* ptr = malloc(size + sizeof(size_t));
    if (ptr) {
        *(size_t*)ptr = size;
        stats.total_allocated += size;
        stats.current_usage += size;
        if (stats.current_usage > stats.peak_usage) {
            stats.peak_usage = stats.current_usage;
        }
        stats.allocation_count++;
        return (uint8_t*)ptr + sizeof(size_t);
    }
    return NULL;
}
```

---

## Summary

1. Understand cache behavior for performance
1. Use hardware memory protection features
1. Organize code and data in appropriate sections
1. Implement efficient allocation strategies
1. Profile and optimize memory usage

---

## Key Takeaways

1. **Cache** awareness is critical for performance
1. **Memory layout** affects execution speed
1. **Static allocation** preferred in embedded
1. **DMA** offloads CPU for transfers
1. **Alignment** matters for correctness and speed

Next: Intertask Communication
