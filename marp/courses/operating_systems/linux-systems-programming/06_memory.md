---
tags:
  - infrastructure:linux
  - languages:c
  - concepts:systems-programming
level: advanced
category: operating-systems
audience:
  - audiences:developers
  - audiences:devops

---
# Allocating Memory in Linux

---
## Virtual Memory Layout

![virtual_memory](svg/courses/operating_systems/linux-systems-programming/06_memory/virtual_memory.svg)

---

## Chapter Overview

1. **Memory Layout**
1. **malloc() and Friends**
1. **mmap() System Call**
1. **Custom Heap Implementation**
1. **Thread Local Storage**
1. **Obstacks**
1. **Stack Allocation**

---

## Process Memory Layout

![process_memory_layout](svg/courses/operating_systems/linux-systems-programming/06_memory/process_memory_layout.svg)

---

## Memory Segments Explained

## Segments:

1. **Text** - Executable code, read-only
1. **Data** - Initialized globals/statics
1. **BSS** - Zero-initialized globals
1. **Heap** - Dynamic allocation (malloc)
1. **Memory Mapped** - mmap, shared libs
1. **Stack** - Local variables, function calls
1. **Kernel** - Kernel memory (inaccessible)

---

## View Process Memory

```bash
# Check memory map
cat /proc/self/maps

# Example output:
00400000-00401000 r-xp  /bin/cat      # Text
00601000-00602000 rw-p  /bin/cat      # Data
01234000-01255000 rw-p  [heap]        # Heap
7ffff7a00000-7ffff7bcd000 r-xp libc.so # Shared lib
7ffffffde000-7ffffffff000 rw-p [stack] # Stack

# Memory statistics
cat /proc/self/status | grep Vm
```

---

## malloc() Family

```c
#include <stdlib.h>

// Allocate memory
void *malloc(size_t size);

// Allocate and zero
void *calloc(size_t nmemb, size_t size);

// Resize allocation
void *realloc(void *ptr, size_t size);

// Aligned allocation
void *aligned_alloc(size_t alignment, size_t size);

// Free memory
void free(void *ptr);
```

---

## malloc() Internals

![malloc_internals](svg/courses/operating_systems/linux-systems-programming/06_memory/malloc_internals.svg)

---

## malloc() Implementation

## glibc malloc (ptmalloc2):

1. **Small requests** (<= 512 bytes)
    - Fast bins
    - No coalescing

1. **Medium requests** (512B - 128KB)
    - Regular bins
    - Best fit allocation

1. **Large requests** (> 128KB)
    - Direct mmap()
    - Released on free()

---

## malloc() Problems

## Issues:

1. **Fragmentation** - Wasted space
1. **Overhead** - Metadata per chunk
1. **Thread contention** - Global locks
1. **No control** - Can't specify location
1. **Memory leaks** - Forget to free()
1. **Use after free** - Dangling pointers
1. **Double free** - Corruption

---

## Memory Fragmentation

![memory_fragmentation](svg/courses/operating_systems/linux-systems-programming/06_memory/memory_fragmentation.svg)

---

## malloc() Best Practices

```c
// Always check return value
void *ptr = malloc(size);
if (ptr == NULL) {
    // Handle allocation failure
    return -ENOMEM;
}

// Initialize memory
memset(ptr, 0, size);
// Or use calloc()

// Free when done
free(ptr);
ptr = NULL;  // Avoid use-after-free

// Never:
free(ptr);
free(ptr);  // Double free!

// Check for leaks with valgrind
```

---

## Alternative Allocators

| Allocator | Pros | Cons |
|-----------|------|------|
| **ptmalloc** | Default, general | Fragmentation |
| **tcmalloc** | Fast, per-thread | Memory overhead |
| **jemalloc** | Scalable, stats | Complex |
| **mimalloc** | Fast, secure | Newer |
| **Hoard** | Multithread | Patent issues |

```bash
# Use alternative allocator
LD_PRELOAD=/usr/lib/libjemalloc.so ./program
```

---

## mmap() System Call

```c
#include <sys/mman.h>

// Map memory
void *addr = mmap(
    NULL,           // Address hint (NULL = kernel chooses)
    4096,           // Length (must be page aligned)
    PROT_READ | PROT_WRITE,  // Protection
    MAP_PRIVATE | MAP_ANONYMOUS,  // Flags
    -1,             // File descriptor (-1 for anonymous)
    0               // Offset
);

if (addr == MAP_FAILED) {
    perror("mmap");
}

// Use memory...

// Unmap when done
munmap(addr, 4096);
```

---

## mmap() Flags

```c
// Protection flags
PROT_READ    // Can read
PROT_WRITE   // Can write
PROT_EXEC    // Can execute
PROT_NONE    // No access

// Mapping flags
MAP_PRIVATE   // Copy-on-write
MAP_SHARED    // Share changes
MAP_ANONYMOUS // No file backing
MAP_FIXED     // Must use hint address
MAP_POPULATE  // Prefault pages
MAP_HUGETLB   // Use huge pages
MAP_LOCKED    // Lock in RAM
```

---

## mmap() vs malloc()

| Feature | malloc() | mmap() |
|---------|----------|--------|
| **Min size** | 1 byte | Page (4KB) |
| **Zeroed** | No | Yes |
| **Control** | Limited | Full |
| **Release** | To heap | To OS |
| **Large alloc** | Uses mmap | Direct |
| **Overhead** | Metadata | None |

---

## File-Backed mmap()

```c
// Map file into memory
int fd = open("data.bin", O_RDWR);
struct stat st;
fstat(fd, &st);

void *addr = mmap(NULL, st.st_size,
                  PROT_READ | PROT_WRITE,
                  MAP_SHARED,  // Changes written to file
                  fd, 0);

// Access file as memory
char *data = (char *)addr;
data[0] = 'X';  // Modifies file!

// Sync to disk
msync(addr, st.st_size, MS_SYNC);

munmap(addr, st.st_size);
close(fd);
```

---

## Shared Memory with mmap()

```c
// Create shared memory
void *shared = mmap(NULL, 4096,
                    PROT_READ | PROT_WRITE,
                    MAP_SHARED | MAP_ANONYMOUS,
                    -1, 0);

pid_t pid = fork();
if (pid == 0) {
    // Child can access shared memory
    int *counter = (int *)shared;
    (*counter)++;
} else {
    wait(NULL);
    int *counter = (int *)shared;
    printf("Counter: %d\n", *counter);  // Sees child's change
}

munmap(shared, 4096);
```

---

## Writing Custom Heap

```c
// Simple bump allocator
typedef struct {
    void *start;
    void *current;
    size_t size;
} Heap;

Heap *heap_create(size_t size) {
    Heap *heap = malloc(sizeof(Heap));
    heap->start = mmap(NULL, size,
                       PROT_READ | PROT_WRITE,
                       MAP_PRIVATE | MAP_ANONYMOUS,
                       -1, 0);
    heap->current = heap->start;
    heap->size = size;
    return heap;
}

void *heap_alloc(Heap *heap, size_t size) {
    // Align to 8 bytes
    size = (size + 7) & ~7;

    if ((char *)heap->current + size >
        (char *)heap->start + heap->size) {
        return NULL;  // Out of space
    }

    void *ptr = heap->current;
    heap->current = (char *)heap->current + size;
    return ptr;
}
```

---

## Custom Heap with Free List

```c
typedef struct block {
    size_t size;
    struct block *next;
    int free;
} block_t;

void *my_malloc(size_t size) {
    block_t *current = free_list;

    // First fit algorithm
    while (current) {
        if (current->free && current->size >= size) {
            current->free = 0;
            return (char *)current + sizeof(block_t);
        }
        current = current->next;
    }

    // No suitable block, allocate new
    return allocate_new_block(size);
}

void my_free(void *ptr) {
    if (!ptr) return;

    block_t *block = (block_t *)((char *)ptr - sizeof(block_t));
    block->free = 1;

    // Coalesce adjacent free blocks
    coalesce_free_blocks();
}
```

---

## brk() and sbrk()

```c
#include <unistd.h>

// Get current program break
void *current_brk = sbrk(0);

// Extend heap by 4096 bytes
void *old_brk = sbrk(4096);
if (old_brk == (void *)-1) {
    perror("sbrk");
}

// Set absolute break
if (brk(new_address) == -1) {
    perror("brk");
}

// Note: malloc() uses brk() for small allocations
// Don't mix manual brk() with malloc()!
```

---

## Thread Local Storage (TLS)

```c
// Thread-local variable
__thread int tls_counter = 0;

// Each thread has its own copy
void *thread_func(void *arg) {
    tls_counter++;  // Doesn't affect other threads
    printf("Thread %ld: counter = %d\n",
           pthread_self(), tls_counter);
    return NULL;
}

// Dynamic TLS
pthread_key_t key;
pthread_key_create(&key, free);

// Set thread-specific value
void *data = malloc(100);
pthread_setspecific(key, data);

// Get thread-specific value
void *my_data = pthread_getspecific(key);
```

---

## TLS Implementation

![tls_implementation](svg/courses/operating_systems/linux-systems-programming/06_memory/tls_implementation.svg)

---

## Obstacks (Object Stacks)

```c
#include <obstack.h>

// Initialize obstack
struct obstack mystack;
obstack_init(&mystack);

// Allocate objects
char *str1 = obstack_alloc(&mystack, 100);
int *arr = obstack_alloc(&mystack, sizeof(int) * 50);

// Growing object
obstack_grow(&mystack, "Hello ", 6);
obstack_grow(&mystack, "World", 5);
obstack_1grow(&mystack, '\0');
char *result = obstack_finish(&mystack);

// Free everything after a point
obstack_free(&mystack, str1);  // Frees str1 and everything after

// Free entire obstack
obstack_free(&mystack, NULL);
```

---

## Obstack Use Cases

## When to Use:

1. **Temporary allocations** in phases
1. **Compiler/parser** symbol tables
1. **String building**
1. **Stack-like** allocation pattern

## Benefits:
- Fast allocation
- Easy bulk free
- No fragmentation
- Good locality

---

## Stack Allocation - alloca()

```c
#include <alloca.h>

void function() {
    // Allocate on stack
    char *buffer = alloca(1024);

    // No need to free!
    // Automatically freed on function return

    // Use like normal memory
    strcpy(buffer, "Stack allocated");

    // Warning: Can cause stack overflow!
    // char *huge = alloca(10000000);  // Dangerous!
}

// Never return alloca'd memory!
char *bad_function() {
    char *ptr = alloca(100);
    return ptr;  // BUG: Returns stack memory!
}
```

---

## C99 Variable Length Arrays

```c
// C99 VLA - allocated on stack
void process(int n) {
    char buffer[n];  // Variable length array
    int matrix[n][n];  // 2D VLA

    // Use like normal array
    for (int i = 0; i < n; i++) {
        buffer[i] = 'A' + i;
    }

    // Automatically freed on return
}

// Get size of VLA
void print_size(int n, char arr[n]) {
    size_t size = sizeof(char[n]);
    printf("Array size: %zu\n", size);
}
```

---

## Memory Alignment

```c
// Natural alignment
struct aligned {
    char c;      // 1 byte
    // 7 bytes padding
    double d;    // 8 bytes (8-byte aligned)
    short s;     // 2 bytes
    // 6 bytes padding
};  // Total: 24 bytes

// Packed struct
struct __attribute__((packed)) packed {
    char c;      // 1 byte
    double d;    // 8 bytes (unaligned!)
    short s;     // 2 bytes
};  // Total: 11 bytes

// Explicit alignment
void *ptr = aligned_alloc(64, 1024);  // 64-byte aligned

// Check alignment
if ((uintptr_t)ptr % 64 == 0) {
    // Properly aligned
}
```

---

## Huge Pages

```c
// Allocate huge pages (2MB or 1GB)
void *addr = mmap(NULL, 2 * 1024 * 1024,
                  PROT_READ | PROT_WRITE,
                  MAP_PRIVATE | MAP_ANONYMOUS | MAP_HUGETLB,
                  -1, 0);

// Benefits:
// - Fewer TLB misses
// - Better performance for large data

// Check huge page availability
// cat /proc/meminfo | grep HugePages

// Reserve huge pages
// echo 20 > /proc/sys/vm/nr_hugepages
```

---

## Memory Locking

```c
#include <sys/mman.h>

// Lock memory in RAM (no swap)
void *critical_data = malloc(4096);
if (mlock(critical_data, 4096) == -1) {
    perror("mlock");
}

// Lock all current memory
if (mlockall(MCL_CURRENT) == -1) {
    perror("mlockall");
}

// Lock future allocations too
mlockall(MCL_CURRENT | MCL_FUTURE);

// Unlock when done
munlock(critical_data, 4096);
munlockall();

// Needs CAP_IPC_LOCK or root
```

---

## NUMA Awareness

```c
#include <numa.h>

// Check NUMA availability
if (numa_available() == -1) {
    // No NUMA support
}

// Allocate on specific node
void *ptr = numa_alloc_onnode(4096, 0);  // Node 0

// Set memory policy
numa_set_localalloc();  // Prefer local node

// Bind to nodes
struct bitmask *mask = numa_allocate_nodemask();
numa_bitmask_setbit(mask, 0);
numa_bind(mask);

// Check node of address
int node = numa_node_of_mem(ptr);
```

---

## Memory Debugging

```bash
# Valgrind - memory leaks
valgrind --leak-check=full ./program

# AddressSanitizer
gcc -fsanitize=address -g program.c
./program

# Memory usage
cat /proc/self/status | grep Vm
pmap -x $$

# System memory
free -h
cat /proc/meminfo
```

---

## Common Memory Bugs

```c
// Memory leak
void leak() {
    void *ptr = malloc(100);
    // Missing free(ptr);
}

// Use after free
void use_after_free() {
    char *ptr = malloc(100);
    free(ptr);
    ptr[0] = 'X';  // BUG!
}

// Double free
void double_free() {
    void *ptr = malloc(100);
    free(ptr);
    free(ptr);  // BUG!
}

// Buffer overflow
void overflow() {
    char *buf = malloc(10);
    strcpy(buf, "This is too long");  // BUG!
}
```

---

## Memory Optimization Techniques

1. **Pool allocators** - Pre-allocate pools
1. **Slab allocators** - Fixed-size objects
1. **Arena allocators** - Thread-local arenas
1. **Memory mapping** - For large files
1. **Lazy allocation** - MAP_NORESERVE
1. **Copy-on-write** - Share until modified

---

## Memory Allocator Comparison

![memory_allocator_comparison](svg/courses/operating_systems/linux-systems-programming/06_memory/memory_allocator_comparison.svg)

---

## Best Practices

1. **Check allocation success**
   ```c
   if (ptr == NULL) handle_error();
   ```

1. **Initialize memory**
   ```c
   memset(ptr, 0, size);
   ```

1. **Free what you allocate**

1. **Set pointers to NULL after free**

1. **Use appropriate allocator**
    - malloc for general use
    - mmap for large allocations
    - alloca for small temporary

1. **Profile memory usage**

---

## Advanced Techniques

```c
// Memory pool with recycling
typedef struct pool {
    void *blocks;
    size_t block_size;
    size_t num_blocks;
    void *free_list;
} pool_t;

// Zero-copy with splice
splice(fd_in, NULL, fd_out, NULL, size, 0);

// Transparent huge pages
madvise(addr, length, MADV_HUGEPAGE);

// Memory prefetching
__builtin_prefetch(addr, 0, 3);
```

---

## Security Considerations

```c
// Clear sensitive data
void secure_free(void *ptr, size_t size) {
    if (ptr) {
        // Overwrite memory
        explicit_bzero(ptr, size);
        free(ptr);
    }
}

// Lock pages with secrets
mlock(password, sizeof(password));

// Disable core dumps
struct rlimit rl = {0, 0};
setrlimit(RLIMIT_CORE, &rl);

// Use MAP_ANONYMOUS for sensitive data
// Never use swap for secrets
```

---

## Performance Tips

1. **Reduce allocations**
    - Reuse buffers
    - Stack allocation when possible

1. **Batch operations**
    - Allocate in chunks

1. **Cache-friendly**
    - Keep hot data together
    - Align to cache lines

1. **NUMA awareness**
    - Allocate near CPU

1. **Huge pages**
    - For large datasets

---

## Memory Profiling

```c
// Manual tracking
size_t allocated = 0;

void *my_malloc(size_t size) {
    void *ptr = malloc(size);
    if (ptr) {
        allocated += size;
        printf("Allocated: %zu bytes (total: %zu)\n",
               size, allocated);
    }
    return ptr;
}

// Use memory profilers:
// - valgrind --tool=massif
// - heaptrack
// - tcmalloc with profiling
```

---

## Real-World Example: Memory Pool

```c
// High-performance memory pool
typedef struct {
    char *memory;
    size_t size;
    size_t used;
    void *free_list;
} Arena;

Arena *arena_create(size_t size) {
    Arena *arena = malloc(sizeof(Arena));
    arena->memory = mmap(NULL, size,
                         PROT_READ | PROT_WRITE,
                         MAP_PRIVATE | MAP_ANONYMOUS,
                         -1, 0);
    arena->size = size;
    arena->used = 0;
    arena->free_list = NULL;
    return arena;
}

void *arena_alloc(Arena *arena, size_t size) {
    // Align to 16 bytes
    size = (size + 15) & ~15;

    if (arena->used + size > arena->size) {
        return NULL;
    }

    void *ptr = arena->memory + arena->used;
    arena->used += size;
    return ptr;
}
```

---

## Memory Pool: Reset and Destroy

```c
void arena_reset(Arena *arena) {
    arena->used = 0;
    arena->free_list = NULL;
    // Memory still mapped, ready for reuse
}

void arena_destroy(Arena *arena) {
    munmap(arena->memory, arena->size);
    free(arena);
}
```

---

## Summary

## Key Takeaways:

- **Memory layout** understanding is crucial
- **malloc()** good for general use
- **mmap()** for large/special allocations
- **Custom allocators** for performance
- **TLS** for thread-local data
- **Stack allocation** for temporary data
- **Profile and debug** memory usage
- **Choose right tool** for the job

Master memory = Build efficient systems!
