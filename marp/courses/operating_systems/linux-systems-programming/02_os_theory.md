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

![historical_context](svg/courses/operating_systems/linux-systems-programming/02_os_theory/historical_context.svg)

---

## x86/x64 Protection Rings

![x86_x64_protection_rings](svg/courses/operating_systems/linux-systems-programming/02_os_theory/x86_x64_protection_rings.svg)

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

## Stored in CS register (Code Segment):

![stored_in_cs_register_code_segment](svg/courses/operating_systems/linux-systems-programming/02_os_theory/stored_in_cs_register_code_segment.svg)

---

## Privilege Transitions

![privilege_transitions](svg/courses/operating_systems/linux-systems-programming/02_os_theory/privilege_transitions.svg)

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

![virtual_memory_architecture](svg/courses/operating_systems/linux-systems-programming/02_os_theory/virtual_memory_architecture.svg)

---

## 4-Level Paging (x86_64):

![4_level_paging_x8664](svg/courses/operating_systems/linux-systems-programming/02_os_theory/4_level_paging_x8664.svg)

---

## Protection Bits:

![protection_bits](svg/courses/operating_systems/linux-systems-programming/02_os_theory/protection_bits.svg)

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

![system_call_mechanism](svg/courses/operating_systems/linux-systems-programming/02_os_theory/system_call_mechanism.svg)

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

## Hardware/Software Interrupts:

![hardware_software_interrupts](svg/courses/operating_systems/linux-systems-programming/02_os_theory/hardware_software_interrupts.svg)

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

## Memory Layout:

![memory_layout](svg/courses/operating_systems/linux-systems-programming/02_os_theory/memory_layout.svg)

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
