# Bit Manipulation in C

---

## Why Bit Manipulation?

- Direct hardware register access (embedded systems)
- Compact data storage (flags, permissions)
- High-performance algorithms
- Network protocols (headers, checksums)
- Graphics and image processing
- Cryptography

---

## Bitwise Operators

| Operator | Name | Description |
|----------|------|-------------|
| `&` | AND | 1 if both bits are 1 |
| `\|` | OR | 1 if either bit is 1 |
| `^` | XOR | 1 if bits differ |
| `~` | NOT | Inverts all bits |
| `<<` | Left shift | Shifts bits left (multiply by 2) |
| `>>` | Right shift | Shifts bits right (divide by 2) |

---

## Bitwise AND, OR, XOR

```c
#include <stdio.h>
#include <stdint.h>

void print_bits(uint8_t val) {
    for (int i = 7; i >= 0; i--) {
        putchar((val & (1 << i)) ? '1' : '0');
        if (i == 4) putchar(' ');
    }
}

int main(void) {
    uint8_t a = 0b11001010;  /* 0xCA = 202 */
    uint8_t b = 0b10110110;  /* 0xB6 = 182 */

    printf("a     = "); print_bits(a); printf("  (0x%02X)\n", a);
    printf("b     = "); print_bits(b); printf("  (0x%02X)\n", b);
    printf("a & b = "); print_bits(a & b); printf("  (AND)\n");
    printf("a | b = "); print_bits(a | b); printf("  (OR)\n");
    printf("a ^ b = "); print_bits(a ^ b); printf("  (XOR)\n");
    printf("~a    = "); print_bits(~a); printf("  (NOT)\n");

    return 0;
}
```

```misc
a     = 1100 1010  (0xCA)
b     = 1011 0110  (0xB6)
a & b = 1000 0010  (AND)
a | b = 1111 1110  (OR)
a ^ b = 0111 1100  (XOR)
~a    = 0011 0101  (NOT)
```

---

## Shift Operators

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint8_t val = 0b00001101;  /* 13 */

    printf("val      = %3d = 0b", val);
    for (int i = 7; i >= 0; i--) putchar((val >> i & 1) + '0');
    printf("\n");

    printf("val << 1 = %3d  (multiply by 2)\n", val << 1);   /* 26 */
    printf("val << 2 = %3d  (multiply by 4)\n", val << 2);   /* 52 */
    printf("val >> 1 = %3d  (divide by 2)\n",   val >> 1);   /*  6 */
    printf("val >> 2 = %3d  (divide by 4)\n",   val >> 2);   /*  3 */

    /* WARNING: right shift on signed integers is implementation-defined */
    int8_t neg = -8;
    printf("\nSigned right shift: %d >> 1 = %d\n", neg, neg >> 1);
    /* Usually arithmetic shift: -8 >> 1 = -4 (preserves sign) */

    /* WARNING: shifting by >= bit width is undefined behavior */
    /* uint32_t x = 1; x << 32;  UB! */

    return 0;
}
```

---

## Setting, Clearing, Toggling Bits

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint8_t flags = 0;

    /* Set bit n: use OR with mask */
    flags |= (1 << 3);  /* set bit 3 */
    printf("After set bit 3:    0x%02X\n", flags);  /* 0x08 */

    flags |= (1 << 5);  /* set bit 5 */
    printf("After set bit 5:    0x%02X\n", flags);  /* 0x28 */

    /* Clear bit n: use AND with inverted mask */
    flags &= ~(1 << 3);  /* clear bit 3 */
    printf("After clear bit 3:  0x%02X\n", flags);  /* 0x20 */

    /* Toggle bit n: use XOR with mask */
    flags ^= (1 << 5);  /* toggle bit 5 (was 1, now 0) */
    printf("After toggle bit 5: 0x%02X\n", flags);  /* 0x00 */

    flags ^= (1 << 5);  /* toggle bit 5 (was 0, now 1) */
    printf("After toggle bit 5: 0x%02X\n", flags);  /* 0x20 */

    /* Check if bit n is set */
    if (flags & (1 << 5)) {
        printf("Bit 5 is set\n");
    }

    return 0;
}
```

---

## Bit Manipulation Macros

```c
#include <stdio.h>
#include <stdint.h>

#define BIT_SET(val, bit)     ((val) |=  (1U << (bit)))
#define BIT_CLEAR(val, bit)   ((val) &= ~(1U << (bit)))
#define BIT_TOGGLE(val, bit)  ((val) ^=  (1U << (bit)))
#define BIT_CHECK(val, bit)   (((val) >> (bit)) & 1U)

/* Multi-bit masks */
#define MASK_SET(val, mask)    ((val) |=  (mask))
#define MASK_CLEAR(val, mask)  ((val) &= ~(mask))
#define MASK_CHECK(val, mask)  (((val) & (mask)) == (mask))

int main(void) {
    uint8_t reg = 0;

    BIT_SET(reg, 0);
    BIT_SET(reg, 3);
    BIT_SET(reg, 7);
    printf("reg = 0x%02X\n", reg);  /* 0x89 */

    printf("Bit 3 set? %d\n", BIT_CHECK(reg, 3));  /* 1 */
    printf("Bit 4 set? %d\n", BIT_CHECK(reg, 4));  /* 0 */

    BIT_CLEAR(reg, 3);
    printf("After clear bit 3: 0x%02X\n", reg);  /* 0x81 */

    return 0;
}
```

---

## Bitmask Flags Pattern

```c
#include <stdio.h>
#include <stdint.h>

/* File permission flags */
#define PERM_READ    (1U << 0)  /* 0x01 */
#define PERM_WRITE   (1U << 1)  /* 0x02 */
#define PERM_EXECUTE (1U << 2)  /* 0x04 */
#define PERM_DELETE  (1U << 3)  /* 0x08 */
#define PERM_ADMIN   (1U << 4)  /* 0x10 */

#define PERM_RW      (PERM_READ | PERM_WRITE)
#define PERM_ALL     (PERM_READ | PERM_WRITE | PERM_EXECUTE | PERM_DELETE | PERM_ADMIN)

void print_permissions(uint32_t perms) {
    printf("Permissions: ");
    if (perms & PERM_READ)    printf("READ ");
    if (perms & PERM_WRITE)   printf("WRITE ");
    if (perms & PERM_EXECUTE) printf("EXEC ");
    if (perms & PERM_DELETE)  printf("DELETE ");
    if (perms & PERM_ADMIN)   printf("ADMIN ");
    printf("(0x%02X)\n", perms);
}

int main(void) {
    uint32_t user_perms = PERM_READ | PERM_WRITE;
    print_permissions(user_perms);

    /* Grant execute permission */
    user_perms |= PERM_EXECUTE;
    print_permissions(user_perms);

    /* Revoke write permission */
    user_perms &= ~PERM_WRITE;
    print_permissions(user_perms);

    /* Check permission before action */
    if (user_perms & PERM_WRITE) {
        printf("Writing file...\n");
    } else {
        printf("Permission denied: no write access\n");
    }

    return 0;
}
```

---

## Common Bit Tricks

```c
#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

/* Check if n is a power of 2 */
bool is_power_of_2(unsigned int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

/* Round up to next power of 2 */
uint32_t next_power_of_2(uint32_t v) {
    v--;
    v |= v >> 1;
    v |= v >> 2;
    v |= v >> 4;
    v |= v >> 8;
    v |= v >> 16;
    v++;
    return v;
}

/* Count number of set bits (population count) */
int popcount(uint32_t x) {
    int count = 0;
    while (x) {
        count += x & 1;
        x >>= 1;
    }
    return count;
}

/* Brian Kernighan's popcount (faster) */
int popcount_fast(uint32_t x) {
    int count = 0;
    while (x) {
        x &= (x - 1);  /* clear lowest set bit */
        count++;
    }
    return count;
}

/* Swap without temporary variable */
void xor_swap(int *a, int *b) {
    if (a != b) {  /* must check: XOR swap with self gives 0 */
        *a ^= *b;
        *b ^= *a;
        *a ^= *b;
    }
}

int main(void) {
    printf("Is 16 power of 2? %s\n", is_power_of_2(16) ? "yes" : "no");
    printf("Is 15 power of 2? %s\n", is_power_of_2(15) ? "yes" : "no");

    printf("Next power of 2 after 100: %u\n", next_power_of_2(100));  /* 128 */
    printf("Next power of 2 after 128: %u\n", next_power_of_2(128));  /* 128 */

    printf("popcount(0xFF) = %d\n", popcount(0xFF));   /* 8 */
    printf("popcount(0xA5) = %d\n", popcount(0xA5));   /* 4 */

    int x = 10, y = 20;
    xor_swap(&x, &y);
    printf("After XOR swap: x=%d, y=%d\n", x, y);

    return 0;
}
```

---

## Bit Fields in Structs

```c
#include <stdio.h>
#include <stdint.h>

/* Bit fields allow sub-byte field sizes */
struct TCPFlags {
    uint8_t fin : 1;
    uint8_t syn : 1;
    uint8_t rst : 1;
    uint8_t psh : 1;
    uint8_t ack : 1;
    uint8_t urg : 1;
    uint8_t ece : 1;
    uint8_t cwr : 1;
};

struct Color565 {
    uint16_t blue  : 5;
    uint16_t green : 6;
    uint16_t red   : 5;
};

int main(void) {
    struct TCPFlags flags = {0};
    flags.syn = 1;
    flags.ack = 1;
    printf("TCP SYN-ACK: syn=%d, ack=%d\n", flags.syn, flags.ack);
    printf("sizeof(TCPFlags) = %zu\n", sizeof(struct TCPFlags));

    /* 16-bit color (RGB 565 format, common in embedded displays) */
    struct Color565 red = {.red = 31, .green = 0, .blue = 0};
    struct Color565 green = {.red = 0, .green = 63, .blue = 0};
    struct Color565 white = {.red = 31, .green = 63, .blue = 31};

    printf("Red:   R=%d G=%d B=%d\n", red.red, red.green, red.blue);
    printf("Green: R=%d G=%d B=%d\n", green.red, green.green, green.blue);
    printf("White: R=%d G=%d B=%d\n", white.red, white.green, white.blue);
    printf("sizeof(Color565) = %zu\n", sizeof(struct Color565));

    return 0;
}
```

Warning: Bit field layout (ordering, padding) is implementation-defined.
Do not use bit fields for portable wire formats.

---

## Endianness

![endianness](svg/courses/languages/c/c-refresher/13_bit_manipulation/endianness.svg)

---

## Detecting and Converting Endianness

```c
#include <stdio.h>
#include <stdint.h>
#include <arpa/inet.h>  /* htonl, ntohl */

int is_little_endian(void) {
    uint32_t x = 1;
    return *(uint8_t *)&x == 1;
}

/* Manual byte swap */
uint32_t swap32(uint32_t val) {
    return ((val & 0xFF000000) >> 24) |
           ((val & 0x00FF0000) >>  8) |
           ((val & 0x0000FF00) <<  8) |
           ((val & 0x000000FF) << 24);
}

uint16_t swap16(uint16_t val) {
    return (val >> 8) | (val << 8);
}

int main(void) {
    printf("System is %s-endian\n",
           is_little_endian() ? "little" : "big");

    uint32_t host_val = 0x12345678;
    uint32_t net_val = htonl(host_val);  /* host to network byte order */

    printf("Host: 0x%08X\n", host_val);
    printf("Network: 0x%08X\n", net_val);
    printf("Manual swap: 0x%08X\n", swap32(host_val));

    /* Convert back */
    printf("Back to host: 0x%08X\n", ntohl(net_val));

    return 0;
}
```

---

## Packed Structs

```c
#include <stdio.h>
#include <stdint.h>

/* Normal struct (with padding) */
struct Normal {
    uint8_t  a;
    uint32_t b;
    uint8_t  c;
};

/* Packed struct (no padding) -- GCC/Clang extension */
struct __attribute__((packed)) Packed {
    uint8_t  a;
    uint32_t b;
    uint8_t  c;
};

/* Portable alternative: use #pragma pack */
#pragma pack(push, 1)
struct PackedPortable {
    uint8_t  a;
    uint32_t b;
    uint8_t  c;
};
#pragma pack(pop)

int main(void) {
    printf("Normal: %zu bytes\n", sizeof(struct Normal));          /* 12 */
    printf("Packed: %zu bytes\n", sizeof(struct Packed));          /*  6 */
    printf("PackedPortable: %zu bytes\n", sizeof(struct PackedPortable)); /* 6 */

    /* WARNING: packed structs may have alignment issues */
    /* On some architectures, unaligned access is slow or causes a trap */
    struct Packed p = {0x11, 0xAABBCCDD, 0x22};
    printf("a=0x%02X, b=0x%08X, c=0x%02X\n", p.a, p.b, p.c);

    return 0;
}
```

---

## Extracting and Inserting Bit Fields Manually

```c
#include <stdio.h>
#include <stdint.h>

/* Extract bits [high:low] from value */
uint32_t extract_bits(uint32_t val, int high, int low) {
    uint32_t mask = ((1U << (high - low + 1)) - 1) << low;
    return (val & mask) >> low;
}

/* Insert bits into value at position [high:low] */
uint32_t insert_bits(uint32_t val, uint32_t bits, int high, int low) {
    uint32_t mask = ((1U << (high - low + 1)) - 1) << low;
    val &= ~mask;           /* clear the field */
    val |= (bits << low) & mask;  /* insert new bits */
    return val;
}

int main(void) {
    /* Example: 32-bit instruction encoding */
    uint32_t instruction = 0;

    /* Insert opcode in bits [31:26] */
    instruction = insert_bits(instruction, 0x23, 31, 26);  /* load word */

    /* Insert register in bits [25:21] */
    instruction = insert_bits(instruction, 8, 25, 21);     /* $t0 */

    /* Insert offset in bits [15:0] */
    instruction = insert_bits(instruction, 0x0040, 15, 0);

    printf("Instruction: 0x%08X\n", instruction);
    printf("Opcode:  0x%02X\n", extract_bits(instruction, 31, 26));
    printf("Register: %u\n",    extract_bits(instruction, 25, 21));
    printf("Offset:  0x%04X\n", extract_bits(instruction, 15, 0));

    return 0;
}
```

---

## Bitmap: Compact Set Representation

```c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#define BITMAP_SIZE 256
#define WORD_BITS   32

struct Bitmap {
    uint32_t words[BITMAP_SIZE / WORD_BITS];
};

void bitmap_init(struct Bitmap *bm) {
    memset(bm->words, 0, sizeof(bm->words));
}

void bitmap_set(struct Bitmap *bm, int bit) {
    bm->words[bit / WORD_BITS] |= (1U << (bit % WORD_BITS));
}

void bitmap_clear(struct Bitmap *bm, int bit) {
    bm->words[bit / WORD_BITS] &= ~(1U << (bit % WORD_BITS));
}

int bitmap_test(const struct Bitmap *bm, int bit) {
    return (bm->words[bit / WORD_BITS] >> (bit % WORD_BITS)) & 1;
}

int bitmap_count(const struct Bitmap *bm) {
    int count = 0;
    for (int i = 0; i < BITMAP_SIZE / WORD_BITS; i++) {
        uint32_t w = bm->words[i];
        while (w) { w &= (w - 1); count++; }
    }
    return count;
}

int main(void) {
    struct Bitmap seen;
    bitmap_init(&seen);

    /* Track which ASCII characters appear in a string */
    const char *text = "Hello, World!";
    for (const char *p = text; *p; p++) {
        bitmap_set(&seen, (unsigned char)*p);
    }

    printf("Unique characters in \"%s\":\n", text);
    for (int i = 0; i < 128; i++) {
        if (bitmap_test(&seen, i)) {
            if (i >= 32) printf("'%c' ", i);
            else printf("0x%02X ", i);
        }
    }
    printf("\nCount: %d\n", bitmap_count(&seen));

    return 0;
}
```

---

## Alignment and Power-of-2 Tricks

```c
#include <stdio.h>
#include <stdint.h>

/* Align value up to alignment (alignment must be power of 2) */
size_t align_up(size_t value, size_t alignment) {
    return (value + alignment - 1) & ~(alignment - 1);
}

/* Align value down to alignment */
size_t align_down(size_t value, size_t alignment) {
    return value & ~(alignment - 1);
}

/* Check if value is aligned */
int is_aligned(size_t value, size_t alignment) {
    return (value & (alignment - 1)) == 0;
}

/* Fast modulo for power-of-2 divisor */
unsigned int fast_mod(unsigned int value, unsigned int pow2) {
    return value & (pow2 - 1);  /* equivalent to value % pow2 */
}

int main(void) {
    printf("align_up(100, 16) = %zu\n", align_up(100, 16));    /* 112 */
    printf("align_up(112, 16) = %zu\n", align_up(112, 16));    /* 112 */
    printf("align_down(100, 16) = %zu\n", align_down(100, 16)); /* 96 */

    printf("is_aligned(64, 16) = %d\n", is_aligned(64, 16));   /* 1 */
    printf("is_aligned(65, 16) = %d\n", is_aligned(65, 16));   /* 0 */

    printf("fast_mod(100, 16) = %u\n", fast_mod(100, 16));      /* 4 */
    printf("100 %% 16         = %u\n", 100 % 16);               /* 4 */

    return 0;
}
```

---

## Compiler Builtins for Bit Operations

```c
#include <stdio.h>
#include <stdint.h>

int main(void) {
    uint32_t val = 0x00A04080;

    /* GCC/Clang builtins (very fast: compile to single instructions) */
    printf("Value: 0x%08X\n", val);
    printf("popcount:         %d\n", __builtin_popcount(val));   /* set bits */
    printf("clz (leading 0s): %d\n", __builtin_clz(val));       /* count leading zeros */
    printf("ctz (trailing 0s):%d\n", __builtin_ctz(val));       /* count trailing zeros */
    printf("ffs (first set):  %d\n", __builtin_ffs(val));       /* 1-indexed */

    /* Log2 using clz */
    int log2_val = 31 - __builtin_clz(val);
    printf("floor(log2(%u)) = %d\n", val, log2_val);

    /* Find lowest set bit */
    uint32_t lowest = val & (-val);
    printf("Lowest set bit: 0x%08X\n", lowest);

    /* Clear lowest set bit */
    uint32_t cleared = val & (val - 1);
    printf("Clear lowest set bit: 0x%08X\n", cleared);

    return 0;
}
```

---

## Summary

- Bitwise operators (`&`, `|`, `^`, `~`, `<<`, `>>`) operate on individual bits
- Use bitmasks and flags for compact state representation
- Common patterns: set/clear/toggle/check individual bits
- Bit tricks enable fast power-of-2 checks, alignment, and population counting
- Bit fields provide named sub-byte fields but are not portable across compilers
- Endianness matters for network protocols and file formats -- use `htonl`/`ntohl`
- Packed structs eliminate padding but may cause alignment issues
- Compiler builtins (`__builtin_popcount`, `__builtin_clz`) map to single CPU instructions
- Use bitmaps for compact set representations
