# Allocating Memory in Linux

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

<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="50" width="400" height="400" fill="#ECF0F1" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Virtual Address Space (x86_64)</text>

  <rect x="200" y="50" width="400" height="50" fill="#E74C3C" stroke="#333" stroke-width="2"/>
  <text x="400" y="80" text-anchor="middle" fill="white" font-size="12">Kernel Space (0xFFFF...)</text>

  <rect x="200" y="100" width="400" height="60" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="400" y="135" text-anchor="middle" fill="white" font-size="12">Stack (grows ↓)</text>
  <text x="620" y="135" font-size="10">~0x7FFF...</text>

  <rect x="200" y="160" width="400" height="40" fill="#95A5A6" stroke="#333" stroke-width="2"/>
  <text x="400" y="185" text-anchor="middle" fill="white" font-size="12">Memory Mapped Region</text>

  <rect x="200" y="200" width="400" height="40" fill="#9B59B6" stroke="#333" stroke-width="2"/>
  <text x="400" y="225" text-anchor="middle" fill="white" font-size="12">Shared Libraries</text>

  <rect x="200" y="240" width="400" height="80" fill="#2ECC71" stroke="#333" stroke-width="2"/>
  <text x="400" y="285" text-anchor="middle" fill="white" font-size="12">Heap (grows ↑)</text>
  <text x="620" y="285" font-size="10">brk</text>

  <rect x="200" y="320" width="400" height="40" fill="#F39C12" stroke="#333" stroke-width="2"/>
  <text x="400" y="345" text-anchor="middle" fill="black" font-size="12">BSS (uninitialized)</text>

  <rect x="200" y="360" width="400" height="40" fill="#E67E22" stroke="#333" stroke-width="2"/>
  <text x="400" y="385" text-anchor="middle" fill="white" font-size="12">Data (initialized)</text>

  <rect x="200" y="400" width="400" height="50" fill="#34495E" stroke="#333" stroke-width="2"/>
  <text x="400" y="430" text-anchor="middle" fill="white" font-size="12">Text (code) - 0x400000</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Heap Organization</text>

  <rect x="100" y="60" width="600" height="60" fill="#2ECC71" stroke="#333" stroke-width="2"/>
  <text x="400" y="95" text-anchor="middle" fill="white" font-size="12">Heap Segment</text>

  <rect x="120" y="140" width="100" height="40" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="170" y="165" text-anchor="middle" fill="white" font-size="10">Chunk 1</text>

  <rect x="120" y="180" width="100" height="20" fill="#E74C3C" stroke="#333" stroke-width="1"/>
  <text x="170" y="195" text-anchor="middle" fill="white" font-size="9">metadata</text>

  <rect x="240" y="140" width="150" height="40" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="315" y="165" text-anchor="middle" fill="white" font-size="10">Chunk 2</text>

  <rect x="240" y="180" width="150" height="20" fill="#E74C3C" stroke="#333" stroke-width="1"/>
  <text x="315" y="195" text-anchor="middle" fill="white" font-size="9">metadata</text>

  <rect x="410" y="140" width="80" height="40" fill="#95A5A6" stroke="#333" stroke-width="2"/>
  <text x="450" y="165" text-anchor="middle" fill="white" font-size="10">Free</text>

  <rect x="410" y="180" width="80" height="20" fill="#7F8C8D" stroke="#333" stroke-width="1"/>
  <text x="450" y="195" text-anchor="middle" fill="white" font-size="9">metadata</text>

  <rect x="510" y="140" width="120" height="40" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="570" y="165" text-anchor="middle" fill="white" font-size="10">Chunk 3</text>

  <rect x="510" y="180" width="120" height="20" fill="#E74C3C" stroke="#333" stroke-width="1"/>
  <text x="570" y="195" text-anchor="middle" fill="white" font-size="9">metadata</text>

  <text x="400" y="250" text-anchor="middle" font-size="11">Each chunk has metadata: size, flags, pointers</text>
  <text x="400" y="270" text-anchor="middle" font-size="11">Free chunks linked in bins by size</text>
</svg>

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

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="14" font-weight="bold">External Fragmentation</text>

  <rect x="100" y="60" width="600" height="40" fill="#ECF0F1" stroke="#333" stroke-width="2"/>

  <rect x="100" y="60" width="80" height="40" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="140" y="85" text-anchor="middle" fill="white" font-size="10">Used</text>

  <rect x="180" y="60" width="40" height="40" fill="#E74C3C" stroke="#333" stroke-width="2"/>
  <text x="200" y="85" text-anchor="middle" fill="white" font-size="10">Free</text>

  <rect x="220" y="60" width="100" height="40" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="270" y="85" text-anchor="middle" fill="white" font-size="10">Used</text>

  <rect x="320" y="60" width="60" height="40" fill="#E74C3C" stroke="#333" stroke-width="2"/>
  <text x="350" y="85" text-anchor="middle" fill="white" font-size="10">Free</text>

  <rect x="380" y="60" width="120" height="40" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="440" y="85" text-anchor="middle" fill="white" font-size="10">Used</text>

  <rect x="500" y="60" width="50" height="40" fill="#E74C3C" stroke="#333" stroke-width="2"/>
  <text x="525" y="85" text-anchor="middle" fill="white" font-size="10">Free</text>

  <rect x="550" y="60" width="150" height="40" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="625" y="85" text-anchor="middle" fill="white" font-size="10">Used</text>

  <text x="400" y="130" text-anchor="middle" font-size="12">Total free: 150 bytes, but largest contiguous: 60 bytes</text>
  <text x="400" y="150" text-anchor="middle" font-size="12">Cannot allocate 100 bytes despite having space!</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Thread Local Storage</text>

  <rect x="50" y="60" width="200" height="300" fill="#3498DB" stroke="#333" stroke-width="2"/>
  <text x="150" y="50" text-anchor="middle" font-size="12">Thread 1</text>
  <rect x="70" y="80" width="160" height="40" fill="#2980B9"/>
  <text x="150" y="105" text-anchor="middle" fill="white" font-size="10">Stack</text>
  <rect x="70" y="130" width="160" height="40" fill="#2471A3"/>
  <text x="150" y="155" text-anchor="middle" fill="white" font-size="10">TLS Block</text>
  <rect x="80" y="140" width="140" height="20" fill="#1F618D"/>
  <text x="150" y="155" text-anchor="middle" fill="white" font-size="9">tls_counter = 5</text>

  <rect x="300" y="60" width="200" height="300" fill="#E74C3C" stroke="#333" stroke-width="2"/>
  <text x="400" y="50" text-anchor="middle" font-size="12">Thread 2</text>
  <rect x="320" y="80" width="160" height="40" fill="#C0392B"/>
  <text x="400" y="105" text-anchor="middle" fill="white" font-size="10">Stack</text>
  <rect x="320" y="130" width="160" height="40" fill="#A93226"/>
  <text x="400" y="155" text-anchor="middle" fill="white" font-size="10">TLS Block</text>
  <rect x="330" y="140" width="140" height="20" fill="#922B21"/>
  <text x="400" y="155" text-anchor="middle" fill="white" font-size="9">tls_counter = 10</text>

  <rect x="550" y="60" width="200" height="300" fill="#2ECC71" stroke="#333" stroke-width="2"/>
  <text x="650" y="50" text-anchor="middle" font-size="12">Thread 3</text>
  <rect x="570" y="80" width="160" height="40" fill="#27AE60"/>
  <text x="650" y="105" text-anchor="middle" fill="white" font-size="10">Stack</text>
  <rect x="570" y="130" width="160" height="40" fill="#229954"/>
  <text x="650" y="155" text-anchor="middle" fill="white" font-size="10">TLS Block</text>
  <rect x="580" y="140" width="140" height="20" fill="#1E8449"/>
  <text x="650" y="155" text-anchor="middle" fill="white" font-size="9">tls_counter = 3</text>

  <text x="400" y="250" text-anchor="middle" font-size="11">Each thread has independent copy</text>
  <text x="400" y="270" text-anchor="middle" font-size="11">No synchronization needed</text>
</svg>

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

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Allocator Performance</text>

  <line x1="100" y1="320" x2="700" y2="320" stroke="#333" stroke-width="2"/>
  <line x1="100" y1="320" x2="100" y2="80" stroke="#333" stroke-width="2"/>

  <rect x="150" y="200" width="60" height="120" fill="#3498DB"/>
  <text x="180" y="340" text-anchor="middle" font-size="10">ptmalloc</text>

  <rect x="250" y="150" width="60" height="170" fill="#E74C3C"/>
  <text x="280" y="340" text-anchor="middle" font-size="10">tcmalloc</text>

  <rect x="350" y="140" width="60" height="180" fill="#2ECC71"/>
  <text x="380" y="340" text-anchor="middle" font-size="10">jemalloc</text>

  <rect x="450" y="120" width="60" height="200" fill="#F39C12"/>
  <text x="480" y="340" text-anchor="middle" font-size="10">mimalloc</text>

  <rect x="550" y="250" width="60" height="70" fill="#9B59B6"/>
  <text x="580" y="340" text-anchor="middle" font-size="10">custom</text>

  <text x="50" y="200" font-size="10">Speed</text>
  <text x="400" y="380" text-anchor="middle" font-size="11">Higher is better (relative performance)</text>
</svg>

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
