# Buffer Overflows in C
---
## What is a Buffer Overflow?
- Occurs when a program tries to write data beyond the bounds of a buffer
- Can overwrite adjacent memory locations
- Allows an attacker to gain control of the program flow
- One of the oldest and most dangerous vulnerability classes
- Responsible for major incidents: Morris Worm (1988), Code Red (2001), Heartbleed (2014)
---
## How Buffer Overflows Happen
- Common coding mistakes:
    - Using insecure functions (e.g. `strcpy`, `strcat`, `sprintf`)
    - Off-by-one errors
    - Inadequate bounds checking
---
## Types of Buffer Overflows

| Type              | Location    | Difficulty | Common Target          |
|-------------------|-------------|------------|------------------------|
| Stack overflow    | Stack       | Medium     | Return address         |
| Heap overflow     | Heap        | Hard       | Function pointers      |
| Integer overflow  | Anywhere    | Medium     | Size calculations      |
| Format string     | Stack       | Medium     | Arbitrary read/write   |
| Off-by-one        | Stack/Heap  | Hard       | Frame pointer          |

---
## Stack Layout Diagram

```diagram
┌──────────────────────────────────────────────────────────┐
│                    Stack Layout                           │
│                                                          │
│  High Address                                            │
│  ┌─────────────────────┐                                 │
│  │  Function Arguments  │                                │
│  ├─────────────────────┤                                 │
│  │  Return Address      │  <-- Attacker's target         │
│  ├─────────────────────┤                                 │
│  │  Saved Frame Pointer │  <-- Can be overwritten        │
│  ├─────────────────────┤                                 │
│  │  [Stack Canary]      │  <-- Protection mechanism      │
│  ├─────────────────────┤                                 │
│  │  Local Variables     │                                │
│  ├─────────────────────┤                                 │
│  │  Buffer[64]          │  <-- Overflow starts here      │
│  └─────────────────────┘                                 │
│  Low Address  (stack grows down)                         │
└──────────────────────────────────────────────────────────┘
```

---
## Diagram

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="15" text-anchor="middle" font-size="12" font-weight="bold">Stack Layout During Buffer Overflow</text>
  <rect x="30" y="25" width="230" height="170" fill="#e3f2fd" stroke="#1565c0" stroke-width="2" rx="3"/>
  <text x="145" y="42" text-anchor="middle" font-size="11" font-weight="bold" fill="#1565c0">Normal Stack</text>
  <rect x="55" y="50" width="180" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="145" y="65" text-anchor="middle" font-size="10">Local Variables</text>
  <rect x="55" y="72" width="180" height="22" fill="#e8f5e9" stroke="#333" stroke-width="1"/>
  <text x="145" y="87" text-anchor="middle" font-size="10">Buffer[64]</text>
  <rect x="55" y="94" width="180" height="22" fill="#fff3e0" stroke="#333" stroke-width="1"/>
  <text x="145" y="109" text-anchor="middle" font-size="10">Saved Frame Pointer</text>
  <rect x="55" y="116" width="180" height="22" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
  <text x="145" y="131" text-anchor="middle" font-size="10" font-weight="bold" fill="#c62828">Return Address</text>
  <rect x="55" y="138" width="180" height="22" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="145" y="153" text-anchor="middle" font-size="10">Function Arguments</text>
  <text x="145" y="180" text-anchor="middle" font-size="9" fill="#666">Stack grows downward</text>
  <rect x="320" y="25" width="260" height="170" fill="#ffebee" stroke="#c62828" stroke-width="2" rx="3"/>
  <text x="450" y="42" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">Overflowed Stack</text>
  <rect x="345" y="50" width="210" height="22" fill="#ffcdd2" stroke="#333" stroke-width="1"/>
  <text x="450" y="65" text-anchor="middle" font-size="10" fill="#c62828">AAAA AAAA AAAA...</text>
  <rect x="345" y="72" width="210" height="22" fill="#ffcdd2" stroke="#333" stroke-width="1"/>
  <text x="450" y="87" text-anchor="middle" font-size="10" fill="#c62828">AAAA (overflow)</text>
  <rect x="345" y="94" width="210" height="22" fill="#ffcdd2" stroke="#333" stroke-width="1"/>
  <text x="450" y="109" text-anchor="middle" font-size="10" fill="#c62828">Overwritten!</text>
  <rect x="345" y="116" width="210" height="22" fill="#ff8a80" stroke="#c62828" stroke-width="2"/>
  <text x="450" y="131" text-anchor="middle" font-size="10" font-weight="bold" fill="#c62828">0xDEADBEEF (hijacked)</text>
  <rect x="345" y="138" width="210" height="22" fill="#f3e5f5" stroke="#333" stroke-width="1"/>
  <text x="450" y="153" text-anchor="middle" font-size="10">Function Arguments</text>
  <text x="450" y="180" text-anchor="middle" font-size="9" fill="#c62828">Attacker controls execution</text>
</svg>

---
## Vulnerable Code Example: strcpy

```c
#include <stdio.h>
#include <string.h>

// VULNERABLE: No bounds checking on user input
void vulnerable_function(char *user_input) {
    char buffer[64];
    strcpy(buffer, user_input);  // No length check!
    printf("You entered: %s\n", buffer);
}

int main(int argc, char *argv[]) {
    if (argc > 1) {
        vulnerable_function(argv[1]);
    }
    return 0;
}
```

```bash
# Compile without protections for demonstration
gcc -fno-stack-protector -z execstack -no-pie \
    -o vulnerable vulnerable.c

# Normal usage
./vulnerable "Hello"

# Overflow attempt (sends 100 'A' characters)
./vulnerable $(python3 -c "print('A' * 100)")
# Segmentation fault - return address overwritten!
```

---
## Secure Code Alternative

```c
#include <stdio.h>
#include <string.h>

// SECURE: Proper bounds checking
void secure_function(const char *user_input) {
    char buffer[64];

    // Option 1: Use strncpy with explicit size limit
    strncpy(buffer, user_input, sizeof(buffer) - 1);
    buffer[sizeof(buffer) - 1] = '\0';  // Ensure null termination

    // Option 2: Use snprintf (preferred)
    snprintf(buffer, sizeof(buffer), "%s", user_input);

    printf("You entered: %s\n", buffer);
}

// Even better: dynamic allocation
void dynamic_function(const char *user_input) {
    size_t len = strlen(user_input);
    if (len > MAX_INPUT_LENGTH) {
        fprintf(stderr, "Input too long\n");
        return;
    }
    char *buffer = calloc(len + 1, sizeof(char));
    if (!buffer) {
        perror("Memory allocation failed");
        return;
    }
    memcpy(buffer, user_input, len);
    printf("You entered: %s\n", buffer);
    free(buffer);
}
```

---
## Unsafe vs Safe C Functions

| Unsafe Function | Safe Alternative         | Notes                        |
|-----------------|--------------------------|------------------------------|
| `strcpy`        | `strncpy` / `strlcpy`   | Always specify max length    |
| `strcat`        | `strncat` / `strlcat`   | Track remaining buffer space |
| `sprintf`       | `snprintf`              | Specify buffer size          |
| `gets`          | `fgets`                 | `gets` removed in C11       |
| `scanf("%s")`   | `scanf("%63s")`         | Specify field width          |
| `vsprintf`      | `vsnprintf`             | Specify buffer size          |

---
## Heap Overflow Example

```c
#include <stdlib.h>
#include <string.h>

// VULNERABLE: Heap buffer overflow
typedef struct {
    char name[32];
    int is_admin;    // Adjacent to buffer on heap
} User;

void vulnerable_heap(char *input) {
    User *user = (User *)malloc(sizeof(User));
    user->is_admin = 0;

    // Overflow name buffer to overwrite is_admin
    strcpy(user->name, input);  // No bounds check!

    if (user->is_admin) {
        printf("Admin access granted!\n");  // Attacker wins
    }
    free(user);
}

// SECURE version
void secure_heap(const char *input) {
    User *user = (User *)calloc(1, sizeof(User));
    if (!user) return;
    user->is_admin = 0;
    strncpy(user->name, input, sizeof(user->name) - 1);
    user->name[sizeof(user->name) - 1] = '\0';
    free(user);
}
```

---
## Format String Vulnerability

```c
#include <stdio.h>

// VULNERABLE: User input used as format string
void vulnerable_format(char *user_input) {
    printf(user_input);  // DANGEROUS! User controls format
}
// Attacker input: "%x %x %x %x" leaks stack values
// Attacker input: "%n" writes to memory!

// SECURE: Always use format specifier
void secure_format(const char *user_input) {
    printf("%s", user_input);  // User input is DATA, not format
}
```

```diagram
┌──────────────────────────────────────────────────┐
│         Format String Attack Capabilities        │
├──────────────────────────────────────────────────┤
│  %x   - Read stack memory (hex)                 │
│  %s   - Read string from memory address          │
│  %n   - Write number of bytes printed to address │
│  %p   - Leak pointer values from stack           │
│  Combined: Arbitrary read + write primitives     │
└──────────────────────────────────────────────────┘
```

---
## Integer Overflow Leading to Buffer Overflow

```c
#include <stdlib.h>
#include <string.h>

// VULNERABLE: Integer overflow in size calculation
void vulnerable_integer(int count, int element_size) {
    // If count=1073741824 and element_size=4,
    // product overflows to 0!
    int total_size = count * element_size;
    char *buffer = malloc(total_size);  // Allocates 0 bytes!
    // Any write to buffer causes heap corruption
    memset(buffer, 0, count * element_size);
    free(buffer);
}

// SECURE: Check for overflow before allocation
void secure_integer(size_t count, size_t element_size) {
    // Use calloc which checks for overflow internally
    char *buffer = calloc(count, element_size);
    if (!buffer) {
        // Allocation failed (possibly due to overflow)
        return;
    }
    // Safe to use buffer
    free(buffer);
}
```

---
## Consequences
- Execution of malicious code
- Privilege escalation
- Denial of service
- Information leaks

---
## Real-World Case Studies

| Vulnerability   | Year | Impact                                      |
|----------------|------|----------------------------------------------|
| Morris Worm    | 1988 | First internet worm, fingerd overflow         |
| Code Red       | 2001 | IIS buffer overflow, 359,000 hosts infected   |
| Slammer        | 2003 | SQL Server overflow, infected 75K hosts in 10m|
| Heartbleed     | 2014 | OpenSSL buffer over-read, leaked private keys |
| EternalBlue    | 2017 | SMB overflow, enabled WannaCry ransomware     |

---
## Heartbleed (CVE-2014-0160) Deep Dive

```diagram
┌────────────────────────────────────────────────────────┐
│              Heartbleed Attack Flow                     │
│                                                        │
│  Client                          Server                │
│    │                               │                   │
│    │  Heartbeat Request:           │                   │
│    │  "bird" (length=4)            │                   │
│    │──────────────────────────────>│                   │
│    │                               │                   │
│    │  Heartbeat Response:          │                   │
│    │  "bird"                       │                   │
│    │<──────────────────────────────│   Normal          │
│    │                               │                   │
│    │  MALICIOUS Heartbeat:         │                   │
│    │  "bird" (claimed length=65535)│                   │
│    │──────────────────────────────>│                   │
│    │                               │                   │
│    │  Response: "bird" + 65531     │                   │
│    │  bytes of server memory       │                   │
│    │  (passwords, private keys!)   │                   │
│    │<──────────────────────────────│   ATTACK          │
└────────────────────────────────────────────────────────┘
```

The bug: Server trusts client-specified length without bounds checking.

---
## Defending Against Buffer Overflows
- Use safe functions (`strncpy`, `strncat`) with bounds checking
- Enable compiler warnings and address sanitizers
- Perform input validation and sanitization
- Avoid using unsafe C functions
- Implement DEP, ASLR, stack canaries

---
## Compiler Protections

```bash
# Enable all warnings and treat as errors
gcc -Wall -Wextra -Werror -o program program.c

# Enable stack protector (canary)
gcc -fstack-protector-all -o program program.c

# Enable address sanitizer (development/testing)
gcc -fsanitize=address -g -o program program.c

# Enable undefined behavior sanitizer
gcc -fsanitize=undefined -g -o program program.c

# Full hardened compilation
gcc -Wall -Wextra -Werror \
    -fstack-protector-strong \
    -D_FORTIFY_SOURCE=2 \
    -O2 \
    -Wformat -Wformat-security \
    -fPIE -pie \
    -z relro -z now \
    -o program program.c
```

| Flag                     | Protection                          |
|--------------------------|-------------------------------------|
| `-fstack-protector-all`  | Stack canaries on all functions     |
| `-D_FORTIFY_SOURCE=2`   | Runtime bounds checking for libc    |
| `-fPIE -pie`            | Position independent executable     |
| `-z relro -z now`       | Read-only relocations (GOT protect) |

---
## Mitigation Techniques
- Data Execution Prevention (DEP)
    - Marks memory regions as non-executable
- Address Space Layout Randomization (ASLR)
    - Randomizes memory layout of processes
- Stack Canaries
    - Detects stack buffer overflows
    - Value is placed before return address on stack

---
## How ASLR Works

```bash
# Check ASLR status on Linux
cat /proc/sys/kernel/randomize_va_space
# 0 = disabled, 1 = partial, 2 = full

# Observe ASLR in action
for i in $(seq 1 5); do
    cat /proc/self/maps | grep stack
done
# Each execution shows different stack addresses

# Check if a binary is PIE (required for full ASLR)
file /usr/bin/ls
readelf -h /usr/bin/ls | grep Type
# DYN (Position-Independent Executable)
```

```diagram
┌──────────────────────────────────────────────────────┐
│           Memory Layout: Without vs With ASLR         │
├──────────────────────┬───────────────────────────────┤
│   Without ASLR       │   With ASLR                   │
├──────────────────────┼───────────────────────────────┤
│   Stack: 0x7fff...   │   Stack: 0x7ffd2a...  (random)│
│   Heap:  0x0060...   │   Heap:  0x5617b3...  (random)│
│   Libs:  0x7f00...   │   Libs:  0x7f8c21...  (random)│
│   Code:  0x0040...   │   Code:  0x5617a1...  (random)│
│                      │                               │
│   Predictable!       │   Unpredictable!              │
└──────────────────────┴───────────────────────────────┘
```

---
## Detection Tools

```bash
# Static analysis - find vulnerable function calls
grep -rn "strcpy\|strcat\|sprintf\|gets\|scanf" src/

# Use cppcheck for static analysis
cppcheck --enable=all --inconclusive src/

# Use Flawfinder for security-focused analysis
flawfinder src/

# Valgrind for runtime memory error detection
valgrind --tool=memcheck --leak-check=full ./program

# AddressSanitizer output example:
# ==12345==ERROR: AddressSanitizer: stack-buffer-overflow
# WRITE of size 100 at 0x7ffd12345678
# #0 0x4011a3 in vulnerable_function overflow.c:5
```

---
## Other Best Practices

- Keep software up-to-date
- Apply principle of least privilege
- Conduct security code reviews
- Use safe alternatives (e.g. rust, memory-safe languages)

---
## Modern Language Alternatives

Languages that prevent buffer overflows by design:

```rust
// Rust: Compiler prevents buffer overflows at compile time
fn main() {
    let mut buffer = [0u8; 64];
    let input = "Hello, World!";

    // This would fail to compile if input > buffer:
    // buffer.copy_from_slice(input.as_bytes());

    // Safe: explicit bounds checking
    let bytes = input.as_bytes();
    let len = bytes.len().min(buffer.len());
    buffer[..len].copy_from_slice(&bytes[..len]);
}
```

```go
// Go: Runtime bounds checking with slices
func safeFunction(input string) {
    buffer := make([]byte, 64)
    // copy() automatically limits to smaller of src/dst
    n := copy(buffer, []byte(input))
    fmt.Printf("Copied %d bytes\n", n)
}
```

---
## Exercise: Buffer Overflow Lab

1. Compile the vulnerable `strcpy` example without protections
2. Run it with increasing input lengths to find the crash point
3. Use GDB to examine the stack layout before and after overflow
4. Enable stack canaries and observe the different crash behavior
5. Enable ASLR and verify addresses change between runs
6. Rewrite the vulnerable code using safe alternatives
7. Run static analysis tools on both versions and compare output

```bash
# GDB commands for the lab
gdb ./vulnerable
(gdb) disassemble vulnerable_function
(gdb) break *vulnerable_function+42
(gdb) run $(python3 -c "print('A'*80)")
(gdb) x/20x $rsp
(gdb) info registers
```
