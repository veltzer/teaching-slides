# Memory Mappings

---

## What Are Memory Mappings?

- Memory mapping is a mechanism that maps a file or device into memory
- Provides a way to access files as if they were in memory
- Core technique in modern operating systems
- Enables efficient I/O and inter-process communication

---

## Virtual Memory Fundamentals

- Abstraction that provides each process with its own address space
- Decouples logical addresses from physical addresses
- Enables memory protection between processes
- Allows programs to use more memory than physically available

<svg viewBox="0 0 500 200">
  <rect x="50" y="40" width="180" height="120" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="270" y="40" width="180" height="120" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="140" y="25" text-anchor="middle" font-family="sans-serif">Virtual Memory</text>
  <text x="360" y="25" text-anchor="middle" font-family="sans-serif">Physical Memory</text>
  <path d="M230,80 L270,80" stroke="#000" stroke-width="2" marker-end="url(#arrowhead)"/>
  <path d="M230,120 L270,120" stroke="#000" stroke-width="2" marker-end="url(#arrowhead)"/>
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Memory Mapping Mechanism

- Creates a region in virtual address space
- Links this region to a file or device
- Allows file access through memory operations
- The kernel handles the actual I/O operations

---

## Key Components

- Virtual Memory Manager (VMM)
- Memory Management Unit (MMU)
- Page Tables
- Translation Lookaside Buffer (TLB)
- Page faults and handlers

---

## Page Tables

- Data structures that map virtual addresses to physical addresses
- Organized hierarchically in modern systems
- Each process has its own page table structure
- Managed by the operating system kernel

<svg viewBox="0 0 500 220">
  <rect x="50" y="40" width="180" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <text x="140" y="60" text-anchor="middle" font-family="sans-serif">Virtual Page Number</text>
  <rect x="230" y="40" width="180" height="30" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="320" y="60" text-anchor="middle" font-family="sans-serif">Offset</text>
  <rect x="100" y="120" width="250" height="40" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <text x="225" y="145" text-anchor="middle" font-family="sans-serif">Page Table</text>
  <rect x="100" y="180" width="250" height="30" fill="#fff0e0" stroke="#000" stroke-width="2"/>
  <text x="225" y="200" text-anchor="middle" font-family="sans-serif">Physical Memory Frame</text>
  <path d="M140,70 L140,120" stroke="#000" stroke-width="2" marker-end="url(#arrowhead2)"/>
  <path d="M225,160 L225,180" stroke="#000" stroke-width="2" marker-end="url(#arrowhead2)"/>
  <defs>
    <marker id="arrowhead2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## mmap() System Call

- Primary interface for memory mapping in UNIX-like systems
- Prototype: `void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset)`
- Maps a file or device into memory
- Returns a pointer to the mapped region

---

## mmap() Parameters

- `addr`: Suggested address for mapping (or NULL)
- `length`: Size of the mapping in bytes
- `prot`: Memory protection flags (READ, WRITE, EXEC)
- `flags`: Mapping flags (SHARED, PRIVATE, etc.)
- `fd`: File descriptor for file to map
- `offset`: Offset within the file

---

## Types of Memory Mappings

- File-backed mappings
  1. Map a file into memory
  1. Changes may be written back to the file
- Anonymous mappings
  1. No backing file
  1. Used for program data (heap, stack)
- Shared vs. Private mappings

---

## File-Backed Mappings

- Maps a file directly into memory
- Reads happen on demand (page faults)
- Writes may be cached and flushed later
- Enables efficient file I/O without explicit read/write calls

<svg viewBox="0 0 500 200">
  <rect x="50" y="40" width="150" height="120" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <rect x="300" y="40" width="150" height="120" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="125" y="25" text-anchor="middle" font-family="sans-serif">Memory</text>
  <text x="375" y="25" text-anchor="middle" font-family="sans-serif">File on Disk</text>
  <path d="M200,80 L300,80" stroke="#000" stroke-width="2" marker-end="url(#arrowhead3)"/>
  <path d="M300,120 L200,120" stroke="#000" stroke-width="2" marker-end="url(#arrowhead3)"/>
  <text x="250" y="70" text-anchor="middle" font-family="sans-serif" font-size="12">Page In</text>
  <text x="250" y="135" text-anchor="middle" font-family="sans-serif" font-size="12">Page Out</text>
  <defs>
    <marker id="arrowhead3" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Anonymous Mappings

- Not backed by any file
- Used for process data structures
- Typically zeroed when created
- Common use cases: malloc implementation, stack growth

---

## Shared vs. Private Mappings

- Shared (MAP_SHARED)
  1. Changes visible to all processes mapping the same file
  1. Updates written back to the backing file
- Private (MAP_PRIVATE)
  1. Copy-on-write semantics
  1. Changes are private to the process
  1. No updates to the backing file

---

## Copy-on-Write (CoW)

- Optimization technique for memory mappings
- Mappings share physical pages until write occurs
- On write, a private copy is created for the process
- Reduces memory consumption and improves performance

<svg viewBox="0 0 500 220">
  <rect x="50" y="40" width="150" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <text x="125" y="60" text-anchor="middle" font-family="sans-serif">Process A</text>
  <rect x="300" y="40" width="150" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <text x="375" y="60" text-anchor="middle" font-family="sans-serif">Process B</text>
  <rect x="175" y="100" width="150" height="30" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="250" y="120" text-anchor="middle" font-family="sans-serif">Shared Page</text>
  <rect x="50" y="170" width="150" height="30" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="125" y="190" text-anchor="middle" font-family="sans-serif">Private Copy</text>
  <rect x="300" y="170" width="150" height="30" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="375" y="190" text-anchor="middle" font-family="sans-serif">Original Page</text>
  <path d="M125,70 L220,100" stroke="#000" stroke-width="2" marker-end="url(#arrowhead4)"/>
  <path d="M375,70 L280,100" stroke="#000" stroke-width="2" marker-end="url(#arrowhead4)"/>
  <path d="M125,130 L125,170" stroke="#000" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowhead4)"/>
  <path d="M375,130 L375,170" stroke="#000" stroke-width="2" marker-end="url(#arrowhead4)"/>
  <text x="100" y="150" text-anchor="middle" font-family="sans-serif" font-size="12">Write</text>
  <defs>
    <marker id="arrowhead4" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#000"/>
    </marker>
  </defs>
</svg>

---

## Benefits of Memory Mappings

- Reduced CPU usage (no explicit read/write system calls)
- Potential for zero-copy I/O
- Lazy loading of file contents
- Simplified programming model for file access
- Efficient sharing of memory between processes

---

## Performance Considerations

- Page size affects granularity and overhead
- Large mappings may cause thrashing
- Fragmentation can reduce efficiency
- Proper alignment can improve performance
- TLB misses can be costly

---

## Memory-Mapped Files Use Cases

- Databases (for data files and indexes)
- High-performance I/O operations
- Inter-process communication
- Loading executable files and libraries
- Real-time data processing

---

## Implementation in Linux

- VMA (Virtual Memory Area) structures
- Page fault handler
- Support for huge pages
- Kernel functions: do_mmap(), handle_mm_fault()
- File system integration

<svg viewBox="0 0 500 220">
  <rect x="50" y="40" width="400" height="30" fill="#e0e0ff" stroke="#000" stroke-width="2"/>
  <text x="250" y="60" text-anchor="middle" font-family="sans-serif">Process Virtual Memory Space</text>
  <rect x="75" y="90" width="100" height="25" fill="#ffe0e0" stroke="#000" stroke-width="2"/>
  <text x="125" y="107" text-anchor="middle" font-family="sans-serif" font-size="12">Code Segment</text>
  <rect x="185" y="90" width="100" height="25" fill="#e0ffe0" stroke="#000" stroke-width="2"/>
  <text x="235" y="107" text-anchor="middle" font-family="sans-serif" font-size="12">Data Segment</text>
  <rect x="325" y="90" width="100" height="25" fill="#fff0e0" stroke="#000" stroke-width="2"/>
  <text x="375" y="107" text-anchor="middle" font-family="sans-serif" font-size="12">Mapped Region</text>
  <rect x="50" y="140" width="400" height="30" fill="#f0f0f0" stroke="#000" stroke-width="2"/>
  <text x="250" y="160" text-anchor="middle" font-family="sans-serif">Linux Kernel</text>
  <rect x="75" y="180" width="100" height="25" fill="#f0f0f0" stroke="#000" stroke-width="2"/>
  <text x="125" y="197" text-anchor="middle" font-family="sans-serif" font-size="12">Page Tables</text>
  <rect x="185" y="180" width="100" height="25" fill="#f0f0f0" stroke="#000" stroke-width="2"/>
  <text x="235" y="197" text-anchor="middle" font-family="sans-serif" font-size="12">VMA Structures</text>
  <rect x="325" y="180" width="100" height="25" fill="#f0f0f0" stroke="#000" stroke-width="2"/>
  <text x="375" y="197" text-anchor="middle" font-family="sans-serif" font-size="12">Page Cache</text>
</svg>

---

## Memory Mapping Security Implications

- Possible data leakage through improper unmapping
- Race conditions in shared mappings
- Careful permission management required
- Side-channel attacks via timing analysis
- Protection against unauthorized access

---

## Advanced Features

- MAP_HUGETLB for huge pages
- Kernel samepage merging (KSM)
- Non-uniform memory access (NUMA) awareness
- Direct I/O mappings
- Remote memory mappings (RDMA)

---

## Debugging Memory Mappings

- /proc/[pid]/maps file shows process mappings
- Tools: pmap, cat /proc/[pid]/smaps
- GDB commands for memory inspection
- Valgrind for tracking memory issues
- Memory mapping core dumps

---

## Memory Mappings vs. Read/Write

- Memory mappings:
  1. Better for random access patterns
  1. Lower overhead for multiple accesses
  1. More complex API
- Traditional read/write:
  1. Better for sequential access
  1. Simpler programming model
  1. Works for non-seekable files

---

## Summary

- Memory mappings provide a powerful I/O mechanism
- Enable efficient memory sharing between processes
- Support various use cases from databases to IPC
- Performance benefits for certain access patterns
- Require careful management for optimal performance
