# Protected Operating System Theory

---

## Chapter Overview

1. **Protected OS Definition**
1. **Importance of Protection**
1. **Privilege Mechanisms**
1. **Memory Protection**
1. **System Calls**
1. **Security Rings**

---

## What is a Protected Operating System?

## Definition:
An OS that **isolates** and **controls** access between:
- User processes
- System resources
- Hardware devices
- Memory regions

## Goal:
**Prevent** programs from interfering with each other or the system

---

## Why Protection Matters

1. **Security**: Prevent malicious code
1. **Stability**: Contain crashes
1. **Privacy**: Isolate user data
1. **Resource Management**: Fair sharing
1. **Multi-tenancy**: Multiple users safely

Without protection: DOS, early Windows, embedded systems

---

## Historical Context

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <line x1="100" y1="300" x2="700" y2="300" stroke="#333" stroke-width="2"/>
  <circle cx="150" cy="300" r="5" fill="#E74C3C"/>
  <text x="150" y="280" text-anchor="middle" font-size="12">1960s</text>
  <text x="150" y="330" text-anchor="middle" font-size="11">Mainframes</text>
  <circle cx="300" cy="300" r="5" fill="#3498DB"/>
  <text x="300" y="280" text-anchor="middle" font-size="12">1970s</text>
  <text x="300" y="330" text-anchor="middle" font-size="11">UNIX</text>
  <circle cx="450" cy="300" r="5" fill="#9B59B6"/>
  <text x="450" y="280" text-anchor="middle" font-size="12">1980s</text>
  <text x="450" y="330" text-anchor="middle" font-size="11">Protected Mode</text>
  <circle cx="600" cy="300" r="5" fill="#2ECC71"/>
  <text x="600" y="280" text-anchor="middle" font-size="12">1990s+</text>
  <text x="600" y="330" text-anchor="middle" font-size="11">Modern OS</text>
  <text x="400" y="100" text-anchor="middle" font-size="16" font-weight="bold">Evolution of OS Protection</text>
</svg>

---

## CPU Privilege Levels

## x86/x64 Protection Rings

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <circle cx="400" cy="200" r="180" fill="#E74C3C" opacity="0.3" stroke="#333" stroke-width="2"/>
  <circle cx="400" cy="200" r="140" fill="#F39C12" opacity="0.4" stroke="#333" stroke-width="2"/>
  <circle cx="400" cy="200" r="100" fill="#F1C40F" opacity="0.5" stroke="#333" stroke-width="2"/>
  <circle cx="400" cy="200" r="60" fill="#2ECC71" opacity="0.6" stroke="#333" stroke-width="2"/>
  <text x="400" y="200" text-anchor="middle" font-size="14" font-weight="bold">Ring 0</text>
  <text x="400" y="215" text-anchor="middle" font-size="11">Kernel</text>
  <text x="400" y="125" text-anchor="middle" font-size="12">Ring 1-2</text>
  <text x="400" y="140" text-anchor="middle" font-size="10">Device Drivers</text>
  <text x="400" y="70" text-anchor="middle" font-size="12">Ring 3</text>
  <text x="400" y="85" text-anchor="middle" font-size="10">User Space</text>
</svg>

---

## Modern CPU Modes

## Real Mode vs Protected Mode

| Feature | Real Mode | Protected Mode |
|---------|-----------|----------------|
| **Memory** | 1MB limit | 4GB+ (32-bit) |
| **Protection** | None | Full |
| **Privilege** | Single level | 4 rings |
| **Multitasking** | Cooperative | Preemptive |
| **Used by** | BIOS, DOS | Linux, Windows |

---

## How Privilege Works

## CPU Privilege Checking:

```c
// Every instruction checked by CPU
if (current_privilege_level > required_privilege) {
    generate_exception(GENERAL_PROTECTION_FAULT);
}

// Privileged instructions (Ring 0 only):
// - Load GDT/IDT
// - Modify CR0/CR3
// - IN/OUT port access
// - HLT (halt CPU)
```

---

## Current Privilege Level (CPL)

## Stored in CS register (Code Segment):

```diagram
CS Register: [Selector:16 bits][Hidden Descriptor]
              ├─ Index (13 bits)
              ├─ Table Indicator (1 bit)
              └─ RPL (2 bits) = Current Privilege Level

CPL Values:
- 0 = Kernel mode (highest privilege)
- 3 = User mode (lowest privilege)
```

---

## Privilege Transitions

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="100" width="200" height="80" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="200" y="145" text-anchor="middle" fill="white" font-size="16">User Mode</text>
  <rect x="500" y="100" width="200" height="80" fill="#E74C3C" stroke="#333" stroke-width="2"/>
  <text x="600" y="145" text-anchor="middle" fill="white" font-size="16">Kernel Mode</text>
  <path d="M 300 140 Q 400 90 500 140" stroke="#2ECC71" stroke-width="3" fill="none" marker-end="url(#arrow3)"/>
  <text x="400" y="80" text-anchor="middle" font-size="12">System Call</text>
  <path d="M 500 160 Q 400 210 300 160" stroke="#9B59B6" stroke-width="3" fill="none" marker-end="url(#arrow3)"/>
  <text x="400" y="230" text-anchor="middle" font-size="12">Return</text>
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Memory Protection Overview

## Key Concepts:

1. **Virtual Memory**: Each process sees its own address space
1. **Page Tables**: Map virtual to physical addresses
1. **Protection Bits**: Control access permissions
1. **Segmentation**: Legacy protection mechanism
1. **ASLR**: Address Space Layout Randomization

---

## Virtual Memory Architecture

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="400" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="125" y="30" text-anchor="middle" font-size="14" font-weight="bold">Process A</text>
  <rect x="50" y="50" width="150" height="100" fill="#2980B9"/>
  <text x="125" y="100" text-anchor="middle" fill="white" font-size="12">Stack</text>
  <rect x="50" y="250" width="150" height="100" fill="#3498DB"/>
  <text x="125" y="300" text-anchor="middle" fill="white" font-size="12">Heap</text>
  <rect x="50" y="350" width="150" height="100" fill="#2471A3"/>
  <text x="125" y="400" text-anchor="middle" fill="white" font-size="12">Code</text>

  <rect x="250" y="50" width="150" height="400" fill="#E74C3C" stroke="#333" stroke-width="2"/>
  <text x="325" y="30" text-anchor="middle" font-size="14" font-weight="bold">Process B</text>
  <rect x="250" y="50" width="150" height="100" fill="#C0392B"/>
  <text x="325" y="100" text-anchor="middle" fill="white" font-size="12">Stack</text>
  <rect x="250" y="250" width="150" height="100" fill="#E74C3C"/>
  <text x="325" y="300" text-anchor="middle" fill="white" font-size="12">Heap</text>
  <rect x="250" y="350" width="150" height="100" fill="#A93226"/>
  <text x="325" y="400" text-anchor="middle" fill="white" font-size="12">Code</text>

  <rect x="500" y="50" width="250" height="400" fill="#95A5A6" stroke="#333" stroke-width="2"/>
  <text x="625" y="30" text-anchor="middle" font-size="14" font-weight="bold">Physical Memory</text>
  <rect x="500" y="100" width="250" height="50" fill="#3498DB"/>
  <text x="625" y="130" text-anchor="middle" fill="white" font-size="11">Process A Page</text>
  <rect x="500" y="200" width="250" height="50" fill="#E74C3C"/>
  <text x="625" y="230" text-anchor="middle" fill="white" font-size="11">Process B Page</text>
  <rect x="500" y="300" width="250" height="50" fill="#2ECC71"/>
  <text x="625" y="330" text-anchor="middle" fill="white" font-size="11">Kernel Page</text>
</svg>

---

## Page Table Structure

## 4-Level Paging (x86_64):

```diagram
Virtual Address (48 bits used of 64):
┌────────┬────────┬────────┬────────┬────────┬────────┐
│  PML4  │  PDPT  │   PD   │   PT   │ Offset │ Unused │
│ 9 bits │ 9 bits │ 9 bits │ 9 bits │12 bits │16 bits │
└────────┴────────┴────────┴────────┴────────┴────────┘

CR3 → PML4 → PDPT → PD → PT → Physical Page
```

---

## Page Table Entry (PTE)

## Protection Bits:

```diagram
64-bit PTE Format:
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬──────────────────────────┬─────────┐
│N│G│ │D│A│C│W│U│R│    Physical Page Number  │  Flags  │
│X│ │ │ │ │D│T│/│/│         (40 bits)        │(12 bits)│
└─┴─┴─┴─┴─┴─┴─┴─┴─┴──────────────────────────┴─────────┘

P (Present):     Page in memory
R/W (Read/Write): Write permission
U/S (User/Super): User accessible
PWT (Write-Through): Cache policy
PCD (Cache Disable): No caching
A (Accessed):    Page was read
D (Dirty):       Page was written
G (Global):      Not flushed on context switch
NX (No Execute): Prevent execution
```

---

## Memory Protection in Action

```c
// Kernel sets up page tables
void setup_page_table(struct process *p) {
    // Map kernel space (Ring 0 only)
    map_pages(KERNEL_START, KERNEL_END,
              PAGE_PRESENT | PAGE_RW);

    // Map user code (read-only, executable)
    map_pages(p->code_start, p->code_end,
              PAGE_PRESENT | PAGE_USER);

    // Map user data (read-write, no-execute)
    map_pages(p->data_start, p->data_end,
              PAGE_PRESENT | PAGE_RW | PAGE_USER | PAGE_NX);
}
```

---

## Memory Protection Violations

## Common Faults:

1. **Segmentation Fault**
   ```c
   int *p = NULL;
   *p = 42;  // SIGSEGV
   ```

1. **Stack Overflow**
   ```c
   void recurse() { recurse(); }
   ```

1. **Permission Denied**
   ```c
   char *code = "code";
   ((void(*)())code)();  // NX bit
   ```

---

## How Memory Protection Works

## Hardware + OS Cooperation:

1. **CPU MMU** (Memory Management Unit)
    - Translates virtual → physical
    - Checks permissions
    - Raises exceptions

1. **OS Kernel**
    - Manages page tables
    - Handles page faults
    - Enforces policy

1. **TLB** (Translation Lookaside Buffer)
    - Caches translations
    - Fast path for memory access

---

## System Calls - The Gateway

## Definition:
**Controlled entry points** from user space to kernel space

## Purpose:
- Request kernel services
- Access hardware
- Manage resources
- Inter-process communication

---

## System Call Mechanism

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="300" height="60" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="200" y="85" text-anchor="middle" fill="white" font-size="14">User Program</text>
  <rect x="50" y="150" width="300" height="60" fill="#9B59B6" stroke="#333" stroke-width="2"/>
  <text x="200" y="185" text-anchor="middle" fill="white" font-size="14">C Library (glibc)</text>
  <rect x="50" y="250" width="300" height="60" fill="#E74C3C" stroke="#333" stroke-width="2"/>
  <text x="200" y="285" text-anchor="middle" fill="white" font-size="14">Kernel</text>
  <line x1="200" y1="110" x2="200" y2="150" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <text x="250" y="130" font-size="11">function call</text>
  <line x1="200" y1="210" x2="200" y2="250" stroke="#333" stroke-width="2" marker-end="url(#arrow4)"/>
  <text x="250" y="230" font-size="11">syscall instruction</text>
  <rect x="450" y="100" width="300" height="200" fill="#ECF0F1" stroke="#333" stroke-width="2"/>
  <text x="600" y="130" text-anchor="middle" font-size="12" font-weight="bold">System Call Steps:</text>
  <text x="460" y="160" font-size="11">1. Load syscall number in RAX</text>
  <text x="460" y="180" font-size="11">2. Load arguments in registers</text>
  <text x="460" y="200" font-size="11">3. Execute SYSCALL instruction</text>
  <text x="460" y="220" font-size="11">4. CPU switches to Ring 0</text>
  <text x="460" y="240" font-size="11">5. Kernel handles request</text>
  <text x="460" y="260" font-size="11">6. SYSRET back to Ring 3</text>
  <defs>
    <marker id="arrow4" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## System Call Implementation (x86_64)

## Modern Fast System Call:

```asm
; User space (Ring 3)
mov rax, 1        ; sys_write system call number
mov rdi, 1        ; fd = stdout
mov rsi, buffer   ; buffer pointer
mov rdx, length   ; number of bytes
syscall           ; Fast system call

; Kernel space (Ring 0)
; CPU automatically:
; - Saves RIP to RCX
; - Saves RFLAGS to R11
; - Loads kernel RIP from MSR_LSTAR
; - Switches to Ring 0
```

---

## System Call Numbers

## Common Linux System Calls:

```c
// arch/x86/include/asm/unistd_64.h
#define __NR_read       0
#define __NR_write      1
#define __NR_open       2
#define __NR_close      3
#define __NR_stat       4
#define __NR_fstat      5
#define __NR_mmap       9
#define __NR_brk        12
#define __NR_fork       57
#define __NR_execve     59
#define __NR_exit       60
#define __NR_wait4      61
```

---

## System Call Performance

## Overhead Comparison:

| Method | Cycles | Use Case |
|--------|--------|----------|
| **Function Call** | ~5 | User space only |
| **SYSCALL** | ~150 | Modern Linux |
| **INT 0x80** | ~400 | Legacy Linux |
| **SYSENTER** | ~200 | 32-bit systems |

## Optimization Strategies:
- Batch operations
- Use vDSO for some calls
- Minimize context switches

---

## vDSO - Virtual Dynamic Shared Object

## System Calls Without Kernel Entry:

```c
// Some "system calls" don't enter kernel
// Mapped into every process

// Fast calls via vDSO:
gettimeofday()  // Reads from shared memory
clock_gettime() // No kernel transition
getcpu()        // CPU and NUMA node

// Check vDSO mapping:
// $ cat /proc/self/maps | grep vdso
// 7ffff7ffa000-7ffff7ffc000 r-xp [vdso]
```

---

## System Call Tracing

## Tools for Debugging:

```bash
# strace - trace system calls
strace -e open,read,write ./program

# Output example:
open("/etc/passwd", O_RDONLY) = 3
read(3, "root:x:0:0:root:/root:/bin/bash\n", 4096) = 2145
write(1, "Users found\n", 12) = 12

# perf - performance analysis
perf stat -e syscalls:* ./program

# BPF - advanced tracing
bpftrace -e 'syscall:sys_enter_* { @[probe] = count(); }'
```

---

## Interrupt Descriptor Table (IDT)

## Hardware/Software Interrupts:

```diagram
IDT Entry Structure:
┌──────────────┬──────────────┬──────┬──────┐
│ Offset 31-16 │ Offset 63-32 │ Type │ DPL  │
├──────────────┼──────────────┼──────┼──────┤
│   Selector   │ Offset 15-0  │ IST  │ Resv │
└──────────────┴──────────────┴──────┴──────┘

Important Vectors:
0x00-0x1F: CPU Exceptions
0x20-0x2F: Hardware IRQs
0x30-0xFF: Software Interrupts
0x80:      Legacy System Call
```

---

## Context Switching

## Process State During Switch:

```c
struct context {
    // General Purpose Registers
    uint64_t rax, rbx, rcx, rdx;
    uint64_t rsi, rdi, rbp, rsp;
    uint64_t r8, r9, r10, r11;
    uint64_t r12, r13, r14, r15;

    // Special Registers
    uint64_t rip;      // Instruction pointer
    uint64_t rflags;   // CPU flags
    uint64_t cr3;      // Page table base

    // Segment Registers
    uint16_t cs, ds, es, fs, gs, ss;
};
```

---

## Protection Mechanisms Summary

## Hardware Features:

1. **Privilege Rings**: Isolate kernel/user
1. **Virtual Memory**: Isolate processes
1. **Page Protection**: Control access
1. **NX Bit**: Prevent code injection
1. **SMEP/SMAP**: Supervisor mode protection

## Software Features:
1. **ASLR**: Randomize memory layout
1. **Stack Canaries**: Detect overflow
1. **SELinux/AppArmor**: Mandatory access control

---

## Modern Protection Extensions

## Intel CET (Control-flow Enforcement):

```c
// Shadow Stack - Prevents ROP attacks
call function    // Push return address to both stacks
ret             // Verify shadow stack matches

// Indirect Branch Tracking
jmp rax         // Must land on ENDBR instruction
```

## Intel MPX (Memory Protection Extensions):
- Bounds checking in hardware
- Deprecated but influential

---

## Kernel vs User Space

## Memory Layout:

```diagram
0xFFFFFFFFFFFFFFFF ┌─────────────────┐
                   │  Kernel Space   │
0xFFFF800000000000 ├─────────────────┤ <- Canonical hole
                   │   (Not mapped)  │
0x00007FFFFFFFFFFF ├─────────────────┤
                   │   User Stack    │
                   │       ↓         │
                   │                 │
                   │       ↑         │
                   │   User Heap     │
                   │   User Code     │
0x0000000000000000 └─────────────────┘
```

---

## Protection Domain Transitions

## Types of Transitions:

1. **System Calls**: User → Kernel (voluntary)
1. **Interrupts**: Any → Kernel (hardware)
1. **Exceptions**: Any → Kernel (faults)
1. **Signals**: Kernel → User (async)

## Cost:
- Save/restore context
- TLB flush (sometimes)
- Cache pollution

---

## Security Implications

## Attack Vectors and Mitigations:

| Attack | Protection |
|--------|------------|
| **Buffer Overflow** | NX bit, ASLR, Canaries |
| **Return-to-libc** | ASLR, PIE |
| **ROP/JOP** | CET, CFI |
| **Kernel Exploits** | SMEP, SMAP, KASLR |
| **Side Channels** | Page Table Isolation |

---

## Meltdown and Spectre

## CPU Vulnerabilities:

```c
// Meltdown - Read kernel memory from user space
// Exploits out-of-order execution

// Mitigation: KPTI (Kernel Page Table Isolation)
// Separate page tables for user/kernel

// Spectre - Read process memory
// Exploits speculative execution

// Mitigation: Retpoline, microcode updates
```

---

## Container Security

## Namespaces and cgroups:

```c
// Namespaces - Isolation
CLONE_NEWPID   // Process IDs
CLONE_NEWNET   // Network stack
CLONE_NEWNS    // Mount points
CLONE_NEWIPC   // IPC resources
CLONE_NEWUTS   // Hostname
CLONE_NEWUSER  // User IDs

// cgroups - Resource limits
memory.limit_in_bytes
cpu.shares
blkio.weight
```

---

## Virtualization and Protection

## Hardware Virtualization Extensions:

1. **Intel VT-x / AMD-V**
    - VMX root/non-root modes
    - Extended page tables (EPT)

1. **Protection in VMs**
    - Guest Ring 0 → Host Ring 3
    - Nested page tables
    - VMCS/VMCB structures

---

## System Call Best Practices

## For Developers:

1. **Minimize syscalls** - Batch operations
1. **Use appropriate APIs** - libc vs direct
1. **Handle errors** - Check return values
1. **Understand costs** - Profile performance
1. **Security** - Validate inputs
1. **Portability** - Use POSIX when possible

---

## Debugging Protection Issues

## Common Tools:

```bash
# Check process memory map
cat /proc/<pid>/maps

# View page faults
perf stat -e page-faults ./program

# Check capabilities
getcap /usr/bin/program

# SELinux context
ls -Z file

# AppArmor status
aa-status
```

---

## Future of OS Protection

## Emerging Technologies:

1. **Hardware Security**
    - Intel TDX (Trust Domain Extensions)
    - AMD SEV (Secure Encrypted Virtualization)

1. **Software Approaches**
    - Rust in kernel
    - Formal verification
    - eBPF sandboxing

1. **Quantum Computing**
    - New threat models
    - Post-quantum cryptography

---

## Key Takeaways

1. **Protection is fundamental** to modern OS
1. **Hardware and software** work together
1. **Privilege levels** isolate components
1. **Virtual memory** provides isolation
1. **System calls** bridge user/kernel
1. **Performance vs security** tradeoffs
1. **Continuous evolution** against threats

---

## Summary

## Protected OS Components:

- **CPU Rings**: Hardware privilege levels
- **MMU**: Memory protection unit
- **Page Tables**: Virtual memory mapping
- **System Calls**: Controlled kernel access
- **Context Switching**: Process isolation
- **Security Features**: ASLR, NX, etc.

Understanding these = Better system programming!
