---
tags:
  - hardware-and-embedded:embedded
  - infrastructure:build-systems
level: advanced
category: embedded
audience:
  - audiences:embedded-engineers
  - audiences:developers
---
# The Toolchain

---

## Chapter Overview

1. Preprocessor and compiler directives
1. Cross-compilation concepts
1. Linker and memory sections
1. Runtime initialization
1. Stack analysis and debugging

---

## Toolchain Components

![toolchain_components](svg/courses/embedded/effective-real-time-embedded-c-and-c++/07_toolchain/toolchain_components.svg)

---

## Preprocessor Directives

```c
// Conditional compilation
#ifdef DEBUG
    #define LOG(msg) printf("DEBUG: %s\n", msg)
#else
    #define LOG(msg) ((void)0)
#endif

// Include guards
#ifndef MODULE_H
#define MODULE_H
// ... declarations
#endif

// Pragma directives
#pragma once  // Modern include guard
#pragma pack(1)  // Structure packing
```

---

## Advanced Macros

```c
// Stringification
#define STRINGIFY(x) #x
#define TOSTRING(x) STRINGIFY(x)

// Token pasting
#define CONCAT(a, b) a##b
#define MAKE_FUNC(name) void CONCAT(func_, name)(void)

// Variadic macros
#define DEBUG_PRINT(fmt, ...) \
    printf("[%s:%d] " fmt "\n", __FILE__, __LINE__, ##__VA_ARGS__)

// Usage
DEBUG_PRINT("Value: %d", 42);
// Output: [file.c:10] Value: 42
```

---

## Compiler Built-ins

```c
// Useful predefined macros
void print_build_info(void) {
    printf("Compiled: %s %s\n", __DATE__, __TIME__);
    printf("Compiler: %s\n", __VERSION__);
    printf("File: %s, Line: %d\n", __FILE__, __LINE__);
    printf("Function: %s\n", __func__);
}

// Compiler-specific macros
#ifdef __GNUC__
    #define PACKED __attribute__((packed))
#elif defined(_MSC_VER)
    #define PACKED __pragma(pack(1))
#endif
```

---

## Cross-Compilation

```makefile
# Cross-compiler configuration
CROSS_COMPILE = arm-none-eabi-
CC = $(CROSS_COMPILE)gcc
AS = $(CROSS_COMPILE)as
LD = $(CROSS_COMPILE)ld
OBJCOPY = $(CROSS_COMPILE)objcopy

# Target-specific flags
CFLAGS += -mcpu=cortex-m4
CFLAGS += -mthumb
CFLAGS += -mfloat-abi=hard
CFLAGS += -mfpu=fpv4-sp-d16
```

---

## Compiler Optimization Levels

```makefile
# Optimization flags
CFLAGS_DEBUG = -O0 -g3  # No optimization, full debug
CFLAGS_RELEASE = -O2    # Balanced optimization
CFLAGS_SIZE = -Os       # Optimize for size
CFLAGS_SPEED = -O3      # Maximum optimization

# Link-time optimization
CFLAGS += -flto
LDFLAGS += -flto

# Function-specific optimization
__attribute__((optimize("O3")))
void performance_critical(void) {
    // Always optimized for speed
}
```

---

## Macros vs Functions

```c
// Macro - no function call overhead
#define MAX(a, b) ((a) > (b) ? (a) : (b))

// Problems with macros
int x = 5;
int y = MAX(x++, 10);  // x incremented twice!

// Inline function - type safe
static inline int max(int a, int b) {
    return a > b ? a : b;
}

// Generic macro with type safety
#define GENERIC_MAX(type) \
static inline type max_##type(type a, type b) { \
    return a > b ? a : b; \
}

GENERIC_MAX(int)
GENERIC_MAX(float)
```

---

## Linker Script Basics

```ld
/* Memory regions */
MEMORY
{
    FLASH (rx)  : ORIGIN = 0x08000000, LENGTH = 512K
    RAM (rwx)   : ORIGIN = 0x20000000, LENGTH = 128K
    CCM (rwx)   : ORIGIN = 0x10000000, LENGTH = 64K
}

/* Section definitions */
SECTIONS
{
    .text : {
        KEEP(*(.vectors))  /* Interrupt vectors */
        *(.text*)          /* Code */
        *(.rodata*)        /* Read-only data */
    } > FLASH
}
```

---

## Memory Section Placement

```ld
SECTIONS
{
    /* Initialized data */
    .data : {
        _sdata = .;        /* Start of data */
        *(.data*)
        _edata = .;        /* End of data */
    } > RAM AT > FLASH

    /* Load address */
    _sidata = LOADADDR(.data);

    /* Uninitialized data */
    .bss : {
        _sbss = .;
        *(.bss*)
        *(COMMON)
        _ebss = .;
    } > RAM
}
```

---

## Custom Sections

```c
// Place in specific section
__attribute__((section(".fastcode")))
void critical_function(void) {
    // Runs from RAM
}

// Custom initialized data
__attribute__((section(".config")))
const config_t default_config = {
    .version = 1,
    .flags = 0x1234
};

// Linker script
.fastcode : {
    *(.fastcode*)
} > RAM AT > FLASH

.config : {
    *(.config*)
} > FLASH
```

---

## Stack and Heap Setup

```ld
/* Stack configuration */
_estack = ORIGIN(RAM) + LENGTH(RAM);  /* Top of RAM */
_Min_Stack_Size = 0x400;               /* 1KB minimum */

/* Heap configuration */
_Min_Heap_Size = 0x200;                /* 512B minimum */

/* Check for enough RAM */
ASSERT(_estack - _ebss >= _Min_Stack_Size + _Min_Heap_Size,
       "Not enough RAM for stack and heap")
```

---

## What Happens Before main()

```c
// Reset handler - entry point
void Reset_Handler(void) {
    // 1. Initialize stack pointer (done by hardware)

    // 2. Copy initialized data from Flash to RAM
    uint32_t* src = &_sidata;
    uint32_t* dst = &_sdata;
    while (dst < &_edata) {
        *dst++ = *src++;
    }

    // 3. Zero-initialize BSS
    dst = &_sbss;
    while (dst < &_ebss) {
        *dst++ = 0;
    }

    // 4. Initialize FPU (if present)
    #ifdef __FPU_PRESENT
    SCB->CPACR |= ((3UL << 20) | (3UL << 22));
    #endif

    // 5. Call constructors (C++)
    __libc_init_array();

    // 6. Call main
    main();

    // 7. Hang if main returns
    while (1);
}
```

---

## C++ Static Initialization

```c
// Constructor array
extern void (*__init_array_start[])(void);
extern void (*__init_array_end[])(void);

void __libc_init_array(void) {
    size_t count = __init_array_end - __init_array_start;
    for (size_t i = 0; i < count; i++) {
        __init_array_start[i]();
    }
}

// In C++ code
class Resource {
    Resource() { /* Constructor called before main */ }
};

Resource global_resource;  // Static initialization
```

---

## Runtime Memory Layout

![runtime_memory_layout](svg/courses/embedded/effective-real-time-embedded-c-and-c++/07_toolchain/runtime_memory_layout.svg)

---

## Stack Frame Analysis

```c
// Function with local variables
void function_with_locals(int param) {
    int local1 = 10;          // Stack offset: -4
    int local2 = 20;          // Stack offset: -8
    char buffer[100];         // Stack offset: -108

    another_function(local1);
}

// Stack frame layout:
// [Return address]  <- Previous SP
// [Saved registers]
// [param]          <- Current SP
// [local1]
// [local2]
// [buffer[0..99]]
```

---

## Stack Usage Estimation

```c
// Static stack analysis
#define STACK_USAGE(name, size) \
    __attribute__((section(".stack_usage"))) \
    static const struct { \
        const char* func; \
        size_t bytes; \
    } stack_##name = { #name, size }

// Annotate functions
void process_data(void) {
    uint8_t buffer[1024];
    STACK_USAGE(process_data, 1024 + 16);  // locals + frame
    // ...
}

// Runtime stack checking
size_t get_stack_usage(void) {
    uint32_t sp;
    __asm__ volatile ("mov %0, sp" : "=r" (sp));
    return (uint8_t*)&_estack - (uint8_t*)sp;
}
```

---

## Build System Integration

```makefile
# Generate dependency files
CFLAGS += -MMD -MP

# Build rules
%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@

# Link with map file
$(TARGET).elf: $(OBJS)
    $(CC) $(LDFLAGS) -Wl,-Map=$(TARGET).map $^ -o $@

# Generate binary
$(TARGET).bin: $(TARGET).elf
    $(OBJCOPY) -O binary $< $@

# Include dependencies
-include $(DEPS)
```

---

## Symbol Visibility

```c
// Control symbol visibility
__attribute__((visibility("hidden")))
void internal_function(void) {
    // Not visible outside compilation unit
}

__attribute__((visibility("default")))
void public_api(void) {
    // Exported symbol
}

// Linker script control
SECTIONS {
    .text : {
        *(.text.public_*)  /* Public functions */
        . = ALIGN(4);
        *(.text.internal_*) /* Internal functions */
    } > FLASH
}
```

---

## Debugging Information

```makefile
# Debug flags
CFLAGS_DEBUG += -g3        # Maximum debug info
CFLAGS_DEBUG += -gdwarf-4  # DWARF format
CFLAGS_DEBUG += -fno-omit-frame-pointer

# Separate debug symbols
$(TARGET).debug: $(TARGET).elf
    $(OBJCOPY) --only-keep-debug $< $@
    $(OBJCOPY) --strip-debug $<
    $(OBJCOPY) --add-gnu-debuglink=$@ $<
```

---

## Size Optimization

```bash
# Analyze binary size
arm-none-eabi-size -A firmware.elf

# Output:
# section          size    addr
# .vectors          456    0x8000000
# .text           45672    0x80001c8
# .rodata          2048    0x800b480
# .data             512    0x20000000
# .bss             4096    0x20000200
```

---

## Dead Code Elimination

```makefile
# Compiler flags
CFLAGS += -ffunction-sections  # Each function in own section
CFLAGS += -fdata-sections      # Each data in own section

# Linker flags
LDFLAGS += -Wl,--gc-sections   # Remove unused sections
LDFLAGS += -Wl,--print-gc-sections  # Show what's removed

# Keep specific symbols
__attribute__((used))
const char version[] = "1.0.0";  // Won't be removed
```

---

## Link-Time Optimization (LTO)

```makefile
# Enable LTO
CFLAGS += -flto
LDFLAGS += -flto

# LTO with specific optimization
CFLAGS += -flto=auto  # Parallel LTO
LDFLAGS += -flto=auto

# Fat LTO objects (debugging)
CFLAGS += -ffat-lto-objects
```

---

## Custom Toolchain Rules

```makefile
# Assembly files
%.o: %.S
    $(CC) $(ASFLAGS) -c $< -o $@

# Generate listings
%.lst: %.c
    $(CC) $(CFLAGS) -Wa,-adhln -c $< > $@

# Preprocessor output
%.i: %.c
    $(CC) $(CFLAGS) -E $< -o $@

# Assembly output
%.s: %.c
    $(CC) $(CFLAGS) -S $< -o $@
```

---

## Binary Analysis Tools

```bash
# Disassembly
arm-none-eabi-objdump -d firmware.elf > firmware.dis

# Symbol table
arm-none-eabi-nm firmware.elf | sort

# Section headers
arm-none-eabi-readelf -S firmware.elf

# Find symbol address
arm-none-eabi-nm firmware.elf | grep main
# 08001234 T main
```

---

## Memory Usage Analysis

```c
// Runtime memory statistics
typedef struct {
    size_t heap_used;
    size_t heap_free;
    size_t stack_used;
    size_t stack_free;
} memory_stats_t;

void get_memory_stats(memory_stats_t* stats) {
    extern uint8_t _end;     // End of BSS
    extern uint8_t _estack;  // Top of stack

    uint32_t sp;
    __asm__ volatile ("mov %0, sp" : "=r" (sp));

    stats->stack_used = &_estack - (uint8_t*)sp;
    stats->stack_free = (uint8_t*)sp - &_end;
    // Heap stats from allocator...
}
```

---

## Toolchain Warnings

```makefile
# Essential warnings
CFLAGS += -Wall              # All common warnings
CFLAGS += -Wextra            # Extra warnings
CFLAGS += -Wpedantic         # Strict ISO C
CFLAGS += -Wconversion       # Type conversions
CFLAGS += -Wshadow           # Variable shadowing
CFLAGS += -Wundef            # Undefined macros
CFLAGS += -Wunused           # Unused entities
CFLAGS += -Wcast-align       # Alignment issues
CFLAGS += -Wstrict-prototypes # Function prototypes

# Treat warnings as errors
CFLAGS += -Werror
```

---

## Static Analysis Integration

```makefile
# Clang static analyzer
scan-build:
    scan-build -o analysis make

# Cppcheck
cppcheck:
    cppcheck --enable=all --inconclusive --std=c11 --platform=unix32 src/

# PC-lint
lint:
    pc-lint -i/usr/local/include co-gcc.lnt project.lnt $(SOURCES)
```

---

## Build Reproducibility

```makefile
# Remove timestamps
CFLAGS += -Wno-builtin-macro-redefined
CFLAGS += -D__DATE__=\"redacted\"
CFLAGS += -D__TIME__=\"redacted\"

# Deterministic builds
CFLAGS += -frandom-seed=42
LDFLAGS += -Wl,--build-id=none

# Record build environment
build-info:
    @echo "Compiler: $(CC) $(shell $(CC) --version | head -1)"
    @echo "Build host: $(shell uname -a)"
    @echo "Git commit: $(shell git rev-parse HEAD)"
```

---

## Summary

1. Understand the complete build process
1. Master preprocessor for conditional compilation
1. Use linker scripts for memory control
1. Implement proper initialization
1. Leverage tools for optimization and analysis

---

## Key Takeaways

1. **Toolchain** knowledge enables optimization
1. **Linker scripts** control memory layout
1. **Initialization** happens before main()
1. **Analysis tools** find issues early
1. **Build system** affects final binary
