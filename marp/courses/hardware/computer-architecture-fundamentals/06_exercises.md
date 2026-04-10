# Hands-On Exercises

---

## Architecture Exercises Guide

![CPU and memory exercises: lscpu, /proc/cpuinfo, cache performance, memory latency, TLB](svg/courses/hardware/computer-architecture-fundamentals/06_exercises/architecture_exercises_guide.svg)

---

## Table of Contents

1. Reading CPU Information
1. Understanding lscpu Output
1. Exploring /proc/cpuinfo
1. Cache Performance Experiments
1. Sequential vs Random Access
1. Cache Line Effects
1. Measuring Memory Latency
1. Using perf stat
1. TLB and Page Tables
1. Examining /proc/self/maps

---

## Exercise 1: Reading Basic CPU Information with lscpu

Run `lscpu` and study the output. This is the quickest way to understand
the CPU in any Linux system.

```bash
lscpu
```

**Expected output (example):**

```misc
Architecture:             x86_64
CPU(s):                   16
Thread(s) per core:       2
Core(s) per socket:       8
Socket(s):                1
Model name:               AMD Ryzen 7 7800X3D
CPU max MHz:              5050.0000
L1d cache:                256 KiB    (8 instances)
L1i cache:                256 KiB    (8 instances)
L2 cache:                 8 MiB      (8 instances)
L3 cache:                 96 MiB     (1 instance)
NUMA node(s):             1
```

**Questions to answer:**
1. How many physical cores does the system have?
1. Is hyper-threading (SMT) enabled? How can you tell?
1. What is the L3 cache size? Is it shared or per-core?
1. How many NUMA nodes are there?

---

## Exercise 2: Exploring /proc/cpuinfo

`/proc/cpuinfo` provides detailed per-core information directly from
the kernel.

```bash
# View info for the first logical CPU
head -30 /proc/cpuinfo

# Count physical cores
grep "core id" /proc/cpuinfo | sort -u | wc -l

# Count logical CPUs (includes hyper-threads)
grep -c "^processor" /proc/cpuinfo

# List all CPU feature flags
grep "^flags" /proc/cpuinfo | head -1 | tr ' ' '\n' | sort
```

**Check for specific features:**

```bash
# Does the CPU support AVX2?
grep -o 'avx2' /proc/cpuinfo | head -1

# Does the CPU support AES hardware acceleration?
grep -o 'aes' /proc/cpuinfo | head -1

# Check for virtualization support
grep -oE 'vmx|svm' /proc/cpuinfo | head -1
# vmx = Intel VT-x, svm = AMD-V
```

**Exercise**: Write a one-liner that prints "SMT: ON" if hyper-threading
is active, or "SMT: OFF" otherwise.

```bash
[ $(lscpu | awk '/Thread\(s\) per core:/{print $NF}') -gt 1 ] \
    && echo "SMT: ON" || echo "SMT: OFF"
```

---

## Exercise 3: Inspecting Cache Topology

Understand your cache hierarchy from sysfs:

```bash
# List all cache levels for CPU 0
ls /sys/devices/system/cpu/cpu0/cache/

# For each cache level, show type, size, and associativity
for idx in /sys/devices/system/cpu/cpu0/cache/index*; do
    echo "--- $(basename $idx) ---"
    echo "Level: $(cat $idx/level)"
    echo "Type:  $(cat $idx/type)"
    echo "Size:  $(cat $idx/size)"
    echo "Ways:  $(cat $idx/ways_of_associativity)"
    echo "Line:  $(cat $idx/coherency_line_size) bytes"
    echo "Sets:  $(cat $idx/number_of_sets)"
    echo ""
done
```

**Expected output:**

```misc
--- index0 ---
Level: 1
Type:  Data
Size:  32K
Ways:  8
Line:  64 bytes
Sets:  64

--- index1 ---
Level: 1
Type:  Instruction
Size:  32K
Ways:  8
Line:  64 bytes
Sets:  64

--- index2 ---
Level: 2
Type:  Unified
Size:  256K
Ways:  4
Line:  64 bytes
Sets:  1024

--- index3 ---
Level: 3
Type:  Unified
Size:  16384K
Ways:  16
Line:  64 bytes
Sets:  16384
```

---

## Exercise 4: Sequential vs Random Access in C

This experiment demonstrates the dramatic impact of spatial locality
on cache performance.

```c
/* cache_access.c -- sequential vs random array access */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#define ARRAY_SIZE (64 * 1024 * 1024)  /* 64 million ints = 256 MB */
#define ITERATIONS 1

static double time_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

void sequential_access(int *arr, int n) {
    volatile long sum = 0;
    for (int iter = 0; iter < ITERATIONS; iter++) {
        for (int i = 0; i < n; i++) {
            sum += arr[i];
        }
    }
}

void random_access(int *arr, int *indices, int n) {
    volatile long sum = 0;
    for (int iter = 0; iter < ITERATIONS; iter++) {
        for (int i = 0; i < n; i++) {
            sum += arr[indices[i]];
        }
    }
}

int main(void) {
    int *arr = malloc(ARRAY_SIZE * sizeof(int));
    int *indices = malloc(ARRAY_SIZE * sizeof(int));

    if (!arr || !indices) {
        perror("malloc");
        return 1;
    }

    /* Initialize array and random indices */
    for (int i = 0; i < ARRAY_SIZE; i++) {
        arr[i] = i;
        indices[i] = i;
    }

    /* Fisher-Yates shuffle for random indices */
    srand(42);
    for (int i = ARRAY_SIZE - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int tmp = indices[i];
        indices[i] = indices[j];
        indices[j] = tmp;
    }

    double t0, t1;

    t0 = time_seconds();
    sequential_access(arr, ARRAY_SIZE);
    t1 = time_seconds();
    printf("Sequential: %.3f seconds\n", t1 - t0);

    t0 = time_seconds();
    random_access(arr, indices, ARRAY_SIZE);
    t1 = time_seconds();
    printf("Random:     %.3f seconds\n", t1 - t0);

    free(arr);
    free(indices);
    return 0;
}
```

**Build and run:**

```bash
gcc -O2 -o cache_access cache_access.c
./cache_access
```

**Typical output:**

```misc
Sequential: 0.052 seconds
Random:     1.340 seconds     <-- 25x slower!
```

---

## Exercise 5: Cache Line Effects

This experiment shows the effect of the 64-byte cache line size.
Accessing every element vs every 16th element (one per cache line)
takes nearly the same time because the entire line is loaded anyway.

```c
/* cache_line.c -- demonstrate cache line effects */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ARRAY_SIZE (32 * 1024 * 1024)  /* 32M ints = 128 MB */

static double time_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int main(void) {
    int *arr = malloc(ARRAY_SIZE * sizeof(int));
    if (!arr) { perror("malloc"); return 1; }

    /* Initialize to avoid page faults during measurement */
    for (int i = 0; i < ARRAY_SIZE; i++) arr[i] = 1;

    printf("Stride  Elements_Touched  Time(ms)  Throughput(GB/s)\n");
    printf("------  ----------------  --------  ----------------\n");

    int strides[] = {1, 2, 4, 8, 16, 32, 64, 128, 256, 512};
    int num_strides = sizeof(strides) / sizeof(strides[0]);

    for (int s = 0; s < num_strides; s++) {
        int stride = strides[s];
        int count = ARRAY_SIZE / stride;

        volatile long sum = 0;
        double t0 = time_seconds();
        for (int i = 0; i < ARRAY_SIZE; i += stride) {
            sum += arr[i];
        }
        double t1 = time_seconds();

        double elapsed_ms = (t1 - t0) * 1000.0;
        double bytes_touched = (double)count * sizeof(int);
        double gb_per_sec = bytes_touched / (t1 - t0) / 1e9;

        printf("%5d   %16d  %8.2f  %16.2f\n",
               stride, count, elapsed_ms, gb_per_sec);
    }

    free(arr);
    return 0;
}
```

**Build and run:**

```bash
gcc -O2 -o cache_line cache_line.c
./cache_line
```

**Expected pattern:**

```output
Stride  Elements_Touched  Time(ms)  Throughput(GB/s)
------  ----------------  --------  ----------------
    1          33554432     23.45             5.45
    2          16777216     12.10             5.29
    4           8388608      6.30             5.09
    8           4194304      3.40             4.72
   16           2097152      2.80             2.86    <-- cache line boundary
   32           1048576      2.70             1.48
   64            524288      2.65             0.76
  128            262144      2.60             0.38
  256            131072      2.55             0.20
  512             65536      2.50             0.10
```

Note: time stays nearly flat from stride 16 onward because each access
fetches a full 64-byte cache line regardless of stride.

---

## Exercise 6: Measuring Memory Latency by Array Size

This experiment measures effective memory latency as array size grows
past each cache level.

```c
/* mem_latency.c -- pointer-chasing latency measurement */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define CHASE_COUNT (1 << 24)  /* 16M pointer chases */

static double time_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

/* Create a random linked list through the array */
void create_pointer_chase(void **arr, int n) {
    int *order = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) order[i] = i;

    /* Fisher-Yates shuffle */
    srand(42);
    for (int i = n - 1; i > 0; i--) {
        int j = rand() % (i + 1);
        int tmp = order[i];
        order[i] = order[j];
        order[j] = tmp;
    }

    /* Link nodes in shuffled order */
    for (int i = 0; i < n - 1; i++) {
        arr[order[i]] = &arr[order[i + 1]];
    }
    arr[order[n - 1]] = &arr[order[0]];  /* close the loop */
    free(order);
}

int main(void) {
    printf("Array Size    Latency (ns)\n");
    printf("----------    ------------\n");

    /* Test sizes from 4 KB to 256 MB */
    for (int kb = 4; kb <= 256 * 1024; kb *= 2) {
        int n = (kb * 1024) / sizeof(void *);
        void **arr = malloc(n * sizeof(void *));
        if (!arr) { perror("malloc"); return 1; }

        create_pointer_chase(arr, n);

        /* Warm up */
        void **p = arr;
        for (int i = 0; i < n * 2; i++) {
            p = (void **)*p;
        }

        /* Measure */
        p = arr;
        double t0 = time_seconds();
        for (int i = 0; i < CHASE_COUNT; i++) {
            p = (void **)*p;
        }
        double t1 = time_seconds();

        /* Prevent optimization */
        volatile void *sink = p;
        (void)sink;

        double latency_ns = (t1 - t0) / CHASE_COUNT * 1e9;

        if (kb < 1024)
            printf("%6d KB     %8.1f\n", kb, latency_ns);
        else
            printf("%6d MB     %8.1f\n", kb / 1024, latency_ns);

        free(arr);
    }

    return 0;
}
```

**Build and run:**

```bash
gcc -O2 -o mem_latency mem_latency.c
./mem_latency
```

**Expected output (varies by CPU):**

```output
Array Size    Latency (ns)
----------    ------------
     4 KB          1.2       <-- L1 cache
     8 KB          1.2
    16 KB          1.3
    32 KB          1.3
    64 KB          3.8       <-- L2 cache
   128 KB          4.0
   256 KB          4.1
   512 KB          9.5       <-- L3 cache
     1 MB         10.2
     4 MB         12.1
    16 MB         13.5
    32 MB         58.0       <-- Main memory!
    64 MB         72.3
   128 MB         78.5
   256 MB         82.1
```

You can clearly see the step function as data exceeds each cache level.

---

## Exercise 7: Using perf stat for CPU Counters

`perf stat` reads hardware performance counters to measure cache misses,
branch mispredictions, and more.

```bash
# Basic event counting (run as root or set perf_event_paranoid)
sudo perf stat ./cache_access

# Example output:
#  Performance counter stats for './cache_access':
#
#        1,523.45 msec task-clock
#               3      context-switches
#     3,845,012,345      cycles
#     1,234,567,890      instructions     # 0.32 insn per cycle
#       234,567,890      cache-references
#       123,456,789      cache-misses     # 52.6% of all refs
#        12,345,678      branch-misses
```

**Measuring specific cache events:**

```bash
# L1 data cache misses
sudo perf stat -e L1-dcache-loads,L1-dcache-load-misses \
    ./cache_access

# Last-level cache (L3) misses
sudo perf stat -e LLC-loads,LLC-load-misses \
    ./cache_access

# Compare sequential vs random (use the two benchmarks)
echo "=== Sequential ==="
sudo perf stat -e cache-references,cache-misses \
    ./cache_access sequential

echo "=== Random ==="
sudo perf stat -e cache-references,cache-misses \
    ./cache_access random
```

---

## Exercise 8: perf stat -- Branch Prediction

Measure branch prediction accuracy on sorted vs unsorted data:

```c
/* branch_pred.c -- demonstrate branch prediction impact */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N (32 * 1024 * 1024)

static double time_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int main(int argc, char **argv) {
    int sorted = (argc > 1 && argv[1][0] == 's');
    int *data = malloc(N * sizeof(int));

    srand(42);
    for (int i = 0; i < N; i++)
        data[i] = rand() % 256;

    if (sorted)
        qsort(data, N, sizeof(int), (__compar_fn_t)strcmp);
        /* Simple sort -- for proper sorting use a real comparator */

    /* Actually, let's do a proper integer sort: */
    if (sorted) {
        /* Insertion of proper qsort comparator */
        for (int i = 1; i < N; i++) {
            int key = data[i];
            int j = i - 1;
            while (j >= 0 && data[j] > key) {
                data[j + 1] = data[j];
                j--;
            }
            data[j + 1] = key;
        }
    }

    volatile long sum = 0;
    double t0 = time_seconds();
    for (int i = 0; i < N; i++) {
        if (data[i] >= 128)
            sum += data[i];
    }
    double t1 = time_seconds();

    printf("%s: sum=%ld, time=%.3f sec\n",
           sorted ? "Sorted" : "Unsorted", (long)sum, t1 - t0);

    free(data);
    return 0;
}
```

**A better version with proper sorting:**

```c
/* branch_pred2.c -- cleaner version */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N (32 * 1024 * 1024)

int cmp_int(const void *a, const void *b) {
    return (*(int *)a - *(int *)b);
}

int main(int argc, char **argv) {
    int sorted = (argc > 1 && argv[1][0] == 's');
    int *data = malloc(N * sizeof(int));

    srand(42);
    for (int i = 0; i < N; i++)
        data[i] = rand() % 256;

    if (sorted)
        qsort(data, N, sizeof(int), cmp_int);

    volatile long sum = 0;
    struct timespec t0, t1;
    clock_gettime(CLOCK_MONOTONIC, &t0);

    for (int i = 0; i < N; i++) {
        if (data[i] >= 128)
            sum += data[i];
    }

    clock_gettime(CLOCK_MONOTONIC, &t1);
    double elapsed = (t1.tv_sec - t0.tv_sec) +
                     (t1.tv_nsec - t0.tv_nsec) * 1e-9;

    printf("%s: sum=%ld, time=%.3f sec\n",
           sorted ? "Sorted" : "Unsorted", (long)sum, elapsed);

    free(data);
    return 0;
}
```

**Run with perf:**

```bash
gcc -O2 -o branch_pred branch_pred2.c

sudo perf stat -e branches,branch-misses ./branch_pred u
# Unsorted: ~25% branch miss rate

sudo perf stat -e branches,branch-misses ./branch_pred s
# Sorted:   ~0.01% branch miss rate
```

---

## Exercise 9: Viewing TLB Misses

The Translation Lookaside Buffer (TLB) caches virtual-to-physical
address translations. TLB misses trigger expensive page table walks.

```bash
# View TLB-related performance counters
sudo perf stat -e dTLB-loads,dTLB-load-misses,\
iTLB-loads,iTLB-load-misses \
    ./mem_latency

# Example output:
#  1,234,567,890  dTLB-loads
#      2,345,678  dTLB-load-misses   # 0.19% of all dTLB loads
#    567,890,123  iTLB-loads
#          1,234  iTLB-load-misses   # 0.00% of all iTLB loads
```

**Experiment: force TLB pressure with large strides:**

```c
/* tlb_pressure.c -- stride through memory hitting many pages */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE (512 * 1024 * 1024L)  /* 512 MB */

static double time_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int main(void) {
    char *buf = malloc(SIZE);
    if (!buf) { perror("malloc"); return 1; }

    /* Touch all pages to ensure they are mapped */
    for (long i = 0; i < SIZE; i += 4096) buf[i] = 1;

    int strides[] = {64, 512, 4096, 65536, 2*1024*1024};
    char *labels[] = {"64B (cache line)", "512B", "4KB (page)",
                      "64KB", "2MB (huge page)"};

    for (int s = 0; s < 5; s++) {
        long stride = strides[s];
        long count = SIZE / stride;
        volatile long sum = 0;

        double t0 = time_seconds();
        for (long i = 0; i < SIZE; i += stride) {
            sum += buf[i];
        }
        double t1 = time_seconds();

        double ns_per_access = (t1 - t0) * 1e9 / count;
        printf("Stride %-22s: %8.1f ns/access  (%ld accesses)\n",
               labels[s], ns_per_access, count);
    }

    free(buf);
    return 0;
}
```

```bash
gcc -O2 -o tlb_pressure tlb_pressure.c
sudo perf stat -e dTLB-load-misses ./tlb_pressure
```

---

## Exercise 10: Examining Page Tables via /proc/self/maps

Every process has a virtual memory map visible in `/proc/self/maps`.
This exercise explores the memory layout of a running process.

```bash
# View your shell's memory map
cat /proc/self/maps | head -30

# Example output:
# 5574a0200000-5574a0205000 r--p  /usr/bin/cat
# 5574a0205000-5574a020a000 r-xp  /usr/bin/cat    <- code (executable)
# 5574a020a000-5574a020d000 r--p  /usr/bin/cat    <- read-only data
# 5574a020e000-5574a020f000 rw-p  /usr/bin/cat    <- writable data
# 5574a1a34000-5574a1a55000 rw-p  [heap]          <- heap
# 7f1c8a200000-7f1c8a228000 r--p  /lib/libc.so.6  <- shared library
# 7ffd12340000-7ffd12361000 rw-p  [stack]         <- stack
# 7ffd123fe000-7ffd12402000 r--p  [vvar]
# 7ffd12402000-7ffd12404000 r-xp  [vdso]
```

**Understanding the columns:**

```bash
Address Range          Perms  Offset   Dev   Inode  Pathname
─────────────────────  ─────  ───────  ────  ─────  ────────
5574a0205000-5574a020a000  r-xp  00005000  08:02  12345  /usr/bin/cat
│                          │││└─ p=private, s=shared
│                          ││└── x=executable
│                          │└─── w=writable
│                          └──── r=readable
```

---

## Exercise 11: Memory Map from Inside a C Program

Write a program that prints its own memory map and allocates memory
to observe heap growth:

```c
/* show_maps.c -- display own memory layout */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void show_maps(const char *label) {
    char path[64];
    snprintf(path, sizeof(path), "/proc/%d/maps", getpid());

    printf("\n=== %s ===\n", label);
    FILE *f = fopen(path, "r");
    if (!f) { perror("fopen"); return; }

    char line[512];
    while (fgets(line, sizeof(line), f)) {
        /* Show only interesting regions */
        if (strstr(line, "[heap]") || strstr(line, "[stack]") ||
            strstr(line, "show_maps")) {
            printf("  %s", line);
        }
    }
    fclose(f);
}

int main(void) {
    printf("PID: %d\n", getpid());

    show_maps("Before allocation");

    /* Allocate 1 MB */
    void *p1 = malloc(1024 * 1024);
    memset(p1, 'A', 1024 * 1024);  /* force physical mapping */
    show_maps("After 1 MB malloc");

    /* Allocate 100 MB */
    void *p2 = malloc(100 * 1024 * 1024);
    memset(p2, 'B', 100 * 1024 * 1024);
    show_maps("After 100 MB malloc");

    /* Free the memory */
    free(p1);
    free(p2);
    show_maps("After free");

    return 0;
}
```

```bash
gcc -O0 -o show_maps show_maps.c
./show_maps
```

**Observe:**
- Small allocations (< ~128 KB) grow the heap with brk/sbrk
- Large allocations use mmap (appear as anonymous mappings)
- After free, mmap regions may be returned to the OS immediately

---

## Exercise 12: Putting It All Together with perf

A comprehensive perf session to profile a real workload:

```bash
# 1. List all available hardware events
sudo perf list hw

# 2. Run a complete profile of any program
sudo perf stat -d ./cache_access

# The -d flag adds detailed cache and branch counters:
#  task-clock, context-switches, cpu-migrations, page-faults,
#  cycles, instructions, branches, branch-misses,
#  L1-dcache-loads, L1-dcache-load-misses,
#  LLC-loads, LLC-load-misses

# 3. Record and report (sampling-based profiling)
sudo perf record -g ./cache_access
sudo perf report

# 4. Count specific events across all CPUs for 5 seconds
sudo perf stat -a -e cycles,instructions,cache-misses \
    sleep 5

# 5. Compare two runs side by side
sudo perf stat -r 5 ./cache_access sequential 2> seq.txt
sudo perf stat -r 5 ./cache_access random 2> rand.txt
diff seq.txt rand.txt
```

**Key metrics to watch:**

| Metric | Good | Bad |
|--------|------|-----|
| Instructions per cycle (IPC) | > 2.0 | < 0.5 |
| L1 cache miss rate | < 3% | > 10% |
| LLC miss rate | < 5% | > 20% |
| Branch miss rate | < 1% | > 5% |
| dTLB miss rate | < 0.1% | > 1% |

---

## Exercise 13: Huge Pages and TLB Performance

Huge pages (2 MB instead of 4 KB) reduce TLB misses for large
allocations. This experiment measures the impact.

```c
/* huge_pages.c -- compare performance with regular vs huge pages */
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <time.h>

#define SIZE (256 * 1024 * 1024L)  /* 256 MB */
#define STRIDE 4096                /* one access per page */

static double time_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

void benchmark(char *buf, long size, const char *label) {
    long count = size / STRIDE;
    volatile long sum = 0;

    /* Warm up */
    for (long i = 0; i < size; i += STRIDE) sum += buf[i];

    double t0 = time_seconds();
    for (int rep = 0; rep < 10; rep++) {
        for (long i = 0; i < size; i += STRIDE) {
            sum += buf[i];
        }
    }
    double t1 = time_seconds();

    printf("%-20s: %.3f ms per iteration  (%ld pages)\n",
           label, (t1 - t0) / 10.0 * 1000.0, count);
}

int main(void) {
    /* Regular pages (4 KB) */
    char *regular = mmap(NULL, SIZE, PROT_READ | PROT_WRITE,
                         MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);

    /* Huge pages (2 MB) -- requires system configuration */
    char *huge = mmap(NULL, SIZE, PROT_READ | PROT_WRITE,
                      MAP_ANONYMOUS | MAP_PRIVATE | MAP_HUGETLB,
                      -1, 0);

    if (regular == MAP_FAILED) {
        perror("mmap regular");
        return 1;
    }

    /* Touch all pages */
    for (long i = 0; i < SIZE; i += 4096) regular[i] = 1;

    benchmark(regular, SIZE, "Regular (4KB pages)");

    if (huge != MAP_FAILED) {
        for (long i = 0; i < SIZE; i += 4096) huge[i] = 1;
        benchmark(huge, SIZE, "Huge (2MB pages)");
        munmap(huge, SIZE);
    } else {
        printf("Huge pages not available. Enable with:\n");
        printf("  echo 256 | sudo tee "
               "/proc/sys/vm/nr_hugepages\n");
    }

    munmap(regular, SIZE);
    return 0;
}
```

```bash
# Enable huge pages (as root)
echo 256 | sudo tee /proc/sys/vm/nr_hugepages

gcc -O2 -o huge_pages huge_pages.c
./huge_pages

# Expected: 2-5x faster with huge pages for this stride pattern
```

---

## Summary: What We Measured

```bash
┌─────────────────────────────────────────────────────────┐
│              Exercises Summary                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  CPU Inspection:                                        │
│  - lscpu: quick overview (cores, threads, caches)       │
│  - /proc/cpuinfo: detailed per-core features            │
│  - sysfs: exact cache parameters                        │
│                                                         │
│  Performance Experiments:                               │
│  - Sequential vs random: 10-50x difference              │
│  - Cache line stride: flat cost at stride >= 16 ints    │
│  - Pointer chasing: reveals L1/L2/L3/DRAM latency      │
│  - Branch prediction: 3x difference sorted vs unsorted  │
│                                                         │
│  Performance Tools:                                     │
│  - perf stat: hardware counter measurement              │
│  - perf record/report: sampling-based profiling         │
│  - /proc/self/maps: virtual memory layout               │
│  - Huge pages: TLB miss reduction                       │
│                                                         │
│  Key Takeaway: understanding the hardware is essential  │
│  for writing fast software. Measure, don't guess!       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```
