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
# Time in Linux

---

## Chapter Overview

1. **Time Concepts and Representations**
1. **System Clocks**
1. **Getting and Setting Time**
1. **Sleeping and Timers**
1. **High-Resolution Timing**
1. **Time Measurement**
1. **Best Practices**

---

## What is Time in Computing?

## Multiple Concepts:

- **Wall Clock Time** - Real-world time (can change)
- **Monotonic Time** - Always increases (never jumps)
- **CPU Time** - Processing time consumed
- **Boot Time** - Since system started
- **Process Time** - Since process started

Time is surprisingly complex in computing!

---

## Time Representations in Linux

![time_representations_in_linux](svg/courses/operating_systems/linux-systems-programming/15_time/time_representations_in_linux.svg)

---

## What is the Current Time?

```c
#include <time.h>
#include <sys/time.h>
#include <stdio.h>

void show_all_time_formats() {
    // Method 1: time() - Second precision
    time_t now = time(NULL);
    printf("Epoch seconds: %ld\n", now);

    // Method 2: gettimeofday() - Microsecond precision
    struct timeval tv;
    gettimeofday(&tv, NULL);  // Second arg was timezone (obsolete)
    printf("Seconds: %ld, Microseconds: %ld\n",
           tv.tv_sec, tv.tv_usec);

    // Method 3: clock_gettime() - Nanosecond precision (BEST)
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    printf("Seconds: %ld, Nanoseconds: %ld\n",
           ts.tv_sec, ts.tv_nsec);

    // Convert to human readable
    struct tm *tm_info = localtime(&now);
    printf("Local time: %s", asctime(tm_info));

    // Better formatting
    char buffer[100];
    strftime(buffer, sizeof(buffer),
             "%Y-%m-%d %H:%M:%S %Z", tm_info);
    printf("Formatted: %s\n", buffer);
}
```

---

## How Long Does Getting Time Take?

```c
#include <time.h>
#include <stdio.h>

void benchmark_time_functions() {
    struct timespec start, end;
    const int iterations = 10000000;

    // Benchmark time()
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < iterations; i++) {
        time_t t = time(NULL);
        (void)t;  // Avoid optimization
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    long ns = (end.tv_sec - start.tv_sec) * 1000000000L +
              (end.tv_nsec - start.tv_nsec);
    printf("time(): %ld ns/call\n", ns/iterations);

    // Benchmark gettimeofday()
    clock_gettime(CLOCK_MONOTONIC, &start);
    for (int i = 0; i < iterations; i++) {
        struct timeval tv;
        gettimeofday(&tv, NULL);
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    ns = (end.tv_sec - start.tv_sec) * 1000000000L +
         (end.tv_nsec - start.tv_nsec);
    printf("gettimeofday(): %ld ns/call\n", ns/iterations);

    // Typical results:
    // time(): ~15 ns (vDSO optimized)
    // gettimeofday(): ~20 ns (vDSO optimized)
    // clock_gettime(): ~25 ns (vDSO optimized)
}
```

---

## The Various Clocks Under the OS

```c
#include <time.h>

void show_all_clocks() {
    struct timespec ts;

    // System-wide real time clock (wall clock)
    clock_gettime(CLOCK_REALTIME, &ts);
    printf("CLOCK_REALTIME: %ld.%09ld\n", ts.tv_sec, ts.tv_nsec);

    // Monotonic clock - never goes backward
    clock_gettime(CLOCK_MONOTONIC, &ts);
    printf("CLOCK_MONOTONIC: %ld.%09ld\n", ts.tv_sec, ts.tv_nsec);

    // Raw hardware time (not adjusted by NTP)
    clock_gettime(CLOCK_MONOTONIC_RAW, &ts);
    printf("CLOCK_MONOTONIC_RAW: %ld.%09ld\n", ts.tv_sec, ts.tv_nsec);

    // Time since boot (includes suspend time)
    clock_gettime(CLOCK_BOOTTIME, &ts);
    printf("CLOCK_BOOTTIME: %ld.%09ld\n", ts.tv_sec, ts.tv_nsec);

    // Process CPU time
    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts);
    printf("CLOCK_PROCESS_CPUTIME_ID: %ld.%09ld\n", ts.tv_sec, ts.tv_nsec);

    // Thread CPU time
    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &ts);
    printf("CLOCK_THREAD_CPUTIME_ID: %ld.%09ld\n", ts.tv_sec, ts.tv_nsec);

    // Coarse versions - faster but less precise
    clock_gettime(CLOCK_REALTIME_COARSE, &ts);
    printf("CLOCK_REALTIME_COARSE: %ld.%09ld\n", ts.tv_sec, ts.tv_nsec);

    clock_gettime(CLOCK_MONOTONIC_COARSE, &ts);
    printf("CLOCK_MONOTONIC_COARSE: %ld.%09ld\n", ts.tv_sec, ts.tv_nsec);
}
```

---

## Clock Properties Comparison

| Clock | Affected by NTP | Monotonic | Suspend | Resolution | Use Case |
|-------|-----------------|-----------|---------|------------|----------|
| **REALTIME** | Yes | No | Continues | ~1ns | Wall clock |
| **REALTIME_COARSE** | Yes | No | Continues | ~1-4ms | Fast wall clock |
| **MONOTONIC** | Rate only | Yes | Stops | ~1ns | Intervals |
| **MONOTONIC_COARSE** | Rate only | Yes | Stops | ~1-4ms | Fast intervals |
| **MONOTONIC_RAW** | No | Yes | Stops | ~1ns | Hardware time |
| **BOOTTIME** | Rate only | Yes | Continues | ~1ns | Uptime |
| **PROCESS_CPUTIME** | No | Yes | N/A | ~1ns | CPU profiling |
| **THREAD_CPUTIME** | No | Yes | N/A | ~1ns | Thread profiling |

---

## Clock Resolution and Precision

```c
#include <time.h>
#include <stdio.h>

void check_clock_resolution() {
    struct timespec res;

    // Get resolution of various clocks
    clock_getres(CLOCK_REALTIME, &res);
    printf("CLOCK_REALTIME resolution: %ld ns\n", res.tv_nsec);

    clock_getres(CLOCK_MONOTONIC, &res);
    printf("CLOCK_MONOTONIC resolution: %ld ns\n", res.tv_nsec);

    clock_getres(CLOCK_REALTIME_COARSE, &res);
    printf("CLOCK_REALTIME_COARSE resolution: %ld ns\n", res.tv_nsec);

    clock_getres(CLOCK_PROCESS_CPUTIME_ID, &res);
    printf("CLOCK_PROCESS_CPUTIME_ID resolution: %ld ns\n", res.tv_nsec);

    // Typical output:
    // CLOCK_REALTIME resolution: 1 ns
    // CLOCK_MONOTONIC resolution: 1 ns
    // CLOCK_REALTIME_COARSE resolution: 4000000 ns (4ms)
    // CLOCK_PROCESS_CPUTIME_ID resolution: 1 ns

    // Note: Resolution != Accuracy!
    // Resolution is smallest measurable unit
    // Accuracy depends on hardware and NTP sync
}
```

---

## vDSO - Virtual Dynamic Shared Object

![vdso_virtual_dynamic_shared_object](svg/courses/operating_systems/linux-systems-programming/15_time/vdso_virtual_dynamic_shared_object.svg)

---

## Sleeping Precisely

```c
#include <time.h>
#include <unistd.h>
#include <errno.h>

// Various sleep functions comparison
void sleep_examples() {
    // sleep() - Seconds only, can be interrupted
    unsigned int unslept = sleep(5);
    if (unslept > 0) {
        printf("Sleep interrupted, %u seconds unslept\n", unslept);
    }

    // usleep() - Microseconds (OBSOLETE, don't use)
    usleep(500000);  // 500ms - may sleep longer!

    // nanosleep() - Nanoseconds, handles interrupts
    struct timespec req = {.tv_sec = 1, .tv_nsec = 500000000};  // 1.5s
    struct timespec rem;

    while (nanosleep(&req, &rem) == -1) {
        if (errno == EINTR) {
            // Interrupted, sleep remaining time
            req = rem;
            continue;
        }
        perror("nanosleep");
        break;
    }

    // clock_nanosleep() - Best option, can use any clock
    struct timespec ts = {.tv_sec = 2, .tv_nsec = 0};
    clock_nanosleep(CLOCK_MONOTONIC, 0, &ts, NULL);

    // Absolute time sleep (wake at specific time)
    clock_gettime(CLOCK_MONOTONIC, &ts);
    ts.tv_sec += 5;  // Wake up 5 seconds from now
    clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &ts, NULL);
}
```

---

## Working with the Right Clock

```c
// Example: Measuring elapsed time correctly

// WRONG - Wall clock can jump!
void measure_wrong() {
    time_t start = time(NULL);
    do_work();
    time_t elapsed = time(NULL) - start;
    // Problem: User or NTP can change clock!
    // Could even be negative!
}

// RIGHT - Monotonic clock always increases
void measure_right() {
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    do_work();

    clock_gettime(CLOCK_MONOTONIC, &end);

    // Calculate elapsed time
    long seconds = end.tv_sec - start.tv_sec;
    long nanoseconds = end.tv_nsec - start.tv_nsec;
    if (nanoseconds < 0) {
        seconds--;
        nanoseconds += 1000000000L;
    }

    double elapsed = seconds + nanoseconds / 1e9;
    printf("Elapsed: %.9f seconds\n", elapsed);
}
```

---

## timerfd - File Descriptor for Timers: Create

```c
#include <sys/timerfd.h>
#include <unistd.h>

void timerfd_example() {
    int tfd = timerfd_create(CLOCK_MONOTONIC, TFD_CLOEXEC);
    if (tfd == -1) {
        perror("timerfd_create");
        return;
    }

    struct itimerspec its = {
        .it_value = {.tv_sec = 2, .tv_nsec = 0},
        .it_interval = {.tv_sec = 1, .tv_nsec = 0}
    };

    if (timerfd_settime(tfd, 0, &its, NULL) == -1) {
        perror("timerfd_settime");
        return;
    }
```

---

## timerfd - File Descriptor for Timers: Read

```c
    uint64_t expirations;
    ssize_t s;

    printf("Timer starting...\n");
    for (int i = 0; i < 5; i++) {
        s = read(tfd, &expirations, sizeof(expirations));
        if (s != sizeof(expirations)) {
            perror("read");
            break;
        }
        printf("Timer expired %llu times\n", expirations);
    }

    close(tfd);
}
```

---

## Using timerfd with epoll: Setup

```c
#include <sys/epoll.h>
#include <sys/timerfd.h>

void timerfd_epoll_example() {
    int epfd = epoll_create1(EPOLL_CLOEXEC);

    int tfd1 = timerfd_create(CLOCK_MONOTONIC, TFD_CLOEXEC);
    int tfd2 = timerfd_create(CLOCK_MONOTONIC, TFD_CLOEXEC);

    struct itimerspec its1 = {
        .it_value = {1, 0},
        .it_interval = {1, 0}
    };
    struct itimerspec its2 = {
        .it_value = {2, 0},
        .it_interval = {3, 0}
    };

    timerfd_settime(tfd1, 0, &its1, NULL);
    timerfd_settime(tfd2, 0, &its2, NULL);
```

---

## Using timerfd with epoll: Event Loop

```c
    struct epoll_event ev;
    ev.events = EPOLLIN;
    ev.data.fd = tfd1;
    epoll_ctl(epfd, EPOLL_CTL_ADD, tfd1, &ev);

    ev.data.fd = tfd2;
    epoll_ctl(epfd, EPOLL_CTL_ADD, tfd2, &ev);

    struct epoll_event events[10];
    while (1) {
        int nfds = epoll_wait(epfd, events, 10, -1);
        for (int i = 0; i < nfds; i++) {
            uint64_t exp;
            read(events[i].data.fd, &exp, sizeof(exp));
            printf("Timer %d expired\n", events[i].data.fd);
        }
    }
}
```

---

## Measuring Very Short Functions

```c
// Using CPU timestamp counter for high precision
static inline uint64_t rdtsc() {
    unsigned int lo, hi;
    __asm__ __volatile__ ("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}

// More accurate with serialization
static inline uint64_t rdtscp() {
    unsigned int lo, hi, aux;
    __asm__ __volatile__ ("rdtscp" : "=a"(lo), "=d"(hi), "=c"(aux));
    // The 'aux' contains CPU ID - useful for affinity checking
    return ((uint64_t)hi << 32) | lo;
}

void measure_short_operation() {
    // Method 1: Using TSC directly (cycles)
    uint64_t start = rdtscp();
    __asm__ __volatile__ ("" ::: "memory");  // Compiler barrier

    // Very short operation to measure
    int sum = 0;
    for (int i = 0; i < 100; i++) {
        sum += i;
    }

    __asm__ __volatile__ ("" ::: "memory");  // Compiler barrier
    uint64_t end = rdtscp();

    printf("Operation took %lu CPU cycles\n", end - start);

    // Convert to nanoseconds (need CPU frequency)
    double cpu_ghz = 3.5;  // Example: 3.5 GHz
    double nanoseconds = (end - start) / cpu_ghz;
    printf("Approximately %.2f nanoseconds\n", nanoseconds);
}
```

---

## Benchmarking Best Practices: Measurement

```c
#include <time.h>
#include <stdint.h>
#include <string.h>

void benchmark_function(void (*func)(void), const char *name, int iterations) {
    for (int i = 0; i < 1000; i++) {
        func();
    }

    double times[100];

    for (int run = 0; run < 100; run++) {
        struct timespec start, end;

        clock_gettime(CLOCK_MONOTONIC, &start);

        for (int i = 0; i < iterations; i++) {
            func();
            __asm__ __volatile__ ("" ::: "memory");
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        double elapsed = (end.tv_sec - start.tv_sec) +
                        (end.tv_nsec - start.tv_nsec) / 1e9;
        times[run] = elapsed / iterations;
    }
```

---

## Benchmarking Best Practices: Statistics

```c
    double min = times[0], max = times[0], sum = 0;
    for (int i = 0; i < 100; i++) {
        if (times[i] < min) min = times[i];
        if (times[i] > max) max = times[i];
        sum += times[i];
    }
    double avg = sum / 100;

    printf("%s: avg=%.3f ns, min=%.3f ns, max=%.3f ns\n",
           name, avg * 1e9, min * 1e9, max * 1e9);
}
```

---

## Process and Thread CPU Time: clock() and getrusage()

```c
#include <time.h>
#include <sys/resource.h>
#include <unistd.h>

void measure_cpu_time() {
    clock_t start = clock();

    for (volatile int i = 0; i < 100000000; i++);

    clock_t end = clock();
    double cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("CPU time used: %f seconds\n", cpu_time_used);

    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);

    printf("User CPU time: %ld.%06ld seconds\n",
           usage.ru_utime.tv_sec, usage.ru_utime.tv_usec);
    printf("System CPU time: %ld.%06ld seconds\n",
           usage.ru_stime.tv_sec, usage.ru_stime.tv_usec);
    printf("Max RSS: %ld KB\n", usage.ru_maxrss);
```

---

## Process and Thread CPU Time: clock_gettime

```c
    struct timespec ts;

    clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &ts);
    printf("Process CPU: %ld.%09ld seconds\n", ts.tv_sec, ts.tv_nsec);

    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &ts);
    printf("Thread CPU: %ld.%09ld seconds\n", ts.tv_sec, ts.tv_nsec);

    pthread_t thread;
    clockid_t clock_id;
    pthread_getcpuclockid(thread, &clock_id);
    clock_gettime(clock_id, &ts);
}
```

---

## Timer Implementation Comparison

![timer_implementation_comparison](svg/courses/operating_systems/linux-systems-programming/15_time/timer_implementation_comparison.svg)

---

## POSIX Timers: Signal Handler

```c
#include <signal.h>
#include <time.h>

void timer_handler(int sig, siginfo_t *si, void *uc) {
    timer_t *tidp = si->si_value.sival_ptr;
    printf("Timer %p expired\n", tidp);
}

void posix_timer_example() {
    timer_t timerid;
    struct sigevent sev;
    struct itimerspec its;
    struct sigaction sa;

    sa.sa_flags = SA_SIGINFO;
    sa.sa_sigaction = timer_handler;
    sigemptyset(&sa.sa_mask);
    sigaction(SIGUSR1, &sa, NULL);

    sev.sigev_notify = SIGEV_SIGNAL;
    sev.sigev_signo = SIGUSR1;
    sev.sigev_value.sival_ptr = &timerid;
```

---

## POSIX Timers: Create and Wait

```c
    if (timer_create(CLOCK_REALTIME, &sev, &timerid) == -1) {
        perror("timer_create");
        return;
    }

    its.it_value.tv_sec = 2;
    its.it_value.tv_nsec = 0;
    its.it_interval.tv_sec = 1;
    its.it_interval.tv_nsec = 0;

    if (timer_settime(timerid, 0, &its, NULL) == -1) {
        perror("timer_settime");
        return;
    }

    sleep(5);

    timer_delete(timerid);
}
```

---

## Calendar Time Functions: Convert

```c
#include <time.h>
#include <stdio.h>

void calendar_time_examples() {
    time_t rawtime;
    struct tm *timeinfo;
    struct tm result;
    char buffer[80];

    time(&rawtime);

    timeinfo = localtime(&rawtime);
    printf("Local time: %s", asctime(timeinfo));

    localtime_r(&rawtime, &result);

    timeinfo = gmtime(&rawtime);
    printf("UTC time: %s", asctime(timeinfo));

    gmtime_r(&rawtime, &result);
```

---

## Calendar Time Functions: Format/Parse

```c
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &result);
    printf("Formatted: %s\n", buffer);

    struct tm parsed;
    strptime("2024-12-25 15:30:00", "%Y-%m-%d %H:%M:%S", &parsed);

    time_guessed = mktime(&parsed);

    result.tm_hour += 24;
    mktime(&result);

    printf("Day of week: %d (0=Sunday)\n", result.tm_wday);
    printf("Day of year: %d\n", result.tm_yday);
}
```

---

## Timezone Handling: Set Timezones

```c
#include <time.h>
#include <stdlib.h>
#include <stdio.h>

void timezone_examples() {
    setenv("TZ", "America/New_York", 1);
    tzset();

    time_t now = time(NULL);
    printf("New York: %s", ctime(&now));

    setenv("TZ", "Europe/London", 1);
    tzset();
    printf("London: %s", ctime(&now));

    setenv("TZ", "Asia/Tokyo", 1);
    tzset();
    printf("Tokyo: %s", ctime(&now));
```

---

## Timezone Handling: Info and Format

```c
    extern char *tzname[2];
    extern long timezone;
    extern int daylight;

    printf("Timezone names: %s / %s\n", tzname[0], tzname[1]);
    printf("UTC offset: %ld seconds\n", timezone);
    printf("DST active: %s\n", daylight ? "yes" : "no");

    time_t utc_time = time(NULL);
    struct tm *tokyo_time;

    setenv("TZ", "Asia/Tokyo", 1);
    tzset();
    tokyo_time = localtime(&utc_time);

    char buffer[100];
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S %Z", tokyo_time);
    printf("Tokyo time: %s\n", buffer);
}
```

---

## Monotonic vs Real Time Clocks

![monotonic_vs_real_time_clocks](svg/courses/operating_systems/linux-systems-programming/15_time/monotonic_vs_real_time_clocks.svg)

---

## Deadline Management: Calculate and Check

```c
#include <time.h>
#include <errno.h>

struct timespec calculate_deadline(int timeout_ms) {
    struct timespec deadline;
    clock_gettime(CLOCK_MONOTONIC, &deadline);

    deadline.tv_sec += timeout_ms / 1000;
    deadline.tv_nsec += (timeout_ms % 1000) * 1000000L;

    if (deadline.tv_nsec >= 1000000000L) {
        deadline.tv_sec++;
        deadline.tv_nsec -= 1000000000L;
    }

    return deadline;
}

int deadline_expired(const struct timespec *deadline) {
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);

    return (now.tv_sec > deadline->tv_sec) ||
           (now.tv_sec == deadline->tv_sec &&
            now.tv_nsec >= deadline->tv_nsec);
}
```

---

## Deadline Management: Operation Loop

```c
int do_operation_with_timeout(int timeout_ms) {
    struct timespec deadline = calculate_deadline(timeout_ms);

    while (!deadline_expired(&deadline)) {
        if (try_operation() == SUCCESS) {
            return 0;
        }

        struct timespec now, remaining;
        clock_gettime(CLOCK_MONOTONIC, &now);

        remaining.tv_sec = deadline.tv_sec - now.tv_sec;
        remaining.tv_nsec = deadline.tv_nsec - now.tv_nsec;
        if (remaining.tv_nsec < 0) {
            remaining.tv_sec--;
            remaining.tv_nsec += 1000000000L;
        }

        struct timespec sleep_time = {0, 10000000};
        if (remaining.tv_sec == 0 && remaining.tv_nsec < 10000000) {
            sleep_time = remaining;
        }
        nanosleep(&sleep_time, NULL);
    }

    return -ETIMEDOUT;
}
```

---

## Rate Limiting: Token Bucket

```c
#include <time.h>
#include <stdbool.h>

typedef struct {
    double tokens;
    double max_tokens;
    double tokens_per_second;
    struct timespec last_update;
} RateLimiter;

void rate_limiter_init(RateLimiter *rl, double rate, double burst) {
    rl->tokens = burst;
    rl->max_tokens = burst;
    rl->tokens_per_second = rate;
    clock_gettime(CLOCK_MONOTONIC, &rl->last_update);
}
```

---

## Rate Limiting: Allow Check

```c
bool rate_limiter_allow(RateLimiter *rl, double tokens_needed) {
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);

    double elapsed = (now.tv_sec - rl->last_update.tv_sec) +
                    (now.tv_nsec - rl->last_update.tv_nsec) / 1e9;

    rl->tokens += elapsed * rl->tokens_per_second;
    if (rl->tokens > rl->max_tokens) {
        rl->tokens = rl->max_tokens;
    }

    rl->last_update = now;

    if (rl->tokens >= tokens_needed) {
        rl->tokens -= tokens_needed;
        return true;
    }

    return false;
}
```

---

## Rate Limiting: Usage

```c
void rate_limited_operation() {
    RateLimiter rl;
    rate_limiter_init(&rl, 10.0, 20.0);

    for (int i = 0; i < 100; i++) {
        if (rate_limiter_allow(&rl, 1.0)) {
            printf("Request %d allowed\n", i);
            do_operation();
        } else {
            printf("Request %d rate limited\n", i);
            usleep(10000);
        }
    }
}
```

---

## High-Resolution Profiling: Types

```c
#include <time.h>
#include <stdio.h>
#include <string.h>

typedef struct {
    const char *name;
    struct timespec total_time;
    struct timespec min_time;
    struct timespec max_time;
    long count;
} ProfileEntry;

#define MAX_PROFILES 100
ProfileEntry profiles[MAX_PROFILES];
int profile_count = 0;

typedef struct {
    int index;
    struct timespec start;
} ProfileHandle;
```

---

## High-Resolution Profiling: Begin

```c
ProfileHandle profile_begin(const char *name) {
    ProfileHandle handle;

    handle.index = -1;
    for (int i = 0; i < profile_count; i++) {
        if (strcmp(profiles[i].name, name) == 0) {
            handle.index = i;
            break;
        }
    }

    if (handle.index == -1 && profile_count < MAX_PROFILES) {
        handle.index = profile_count++;
        profiles[handle.index].name = name;
        profiles[handle.index].total_time = (struct timespec){0, 0};
        profiles[handle.index].min_time = (struct timespec){999999, 0};
        profiles[handle.index].max_time = (struct timespec){0, 0};
        profiles[handle.index].count = 0;
    }

    clock_gettime(CLOCK_MONOTONIC, &handle.start);
    return handle;
}
```

---

## High-Resolution Profiling: End

```c
void profile_end(ProfileHandle handle) {
    if (handle.index < 0) return;

    struct timespec end;
    clock_gettime(CLOCK_MONOTONIC, &end);

    struct timespec elapsed;
    elapsed.tv_sec = end.tv_sec - handle.start.tv_sec;
    elapsed.tv_nsec = end.tv_nsec - handle.start.tv_nsec;
    if (elapsed.tv_nsec < 0) {
        elapsed.tv_sec--;
        elapsed.tv_nsec += 1000000000L;
    }

    ProfileEntry *p = &profiles[handle.index];

    p->total_time.tv_sec += elapsed.tv_sec;
    p->total_time.tv_nsec += elapsed.tv_nsec;
    if (p->total_time.tv_nsec >= 1000000000L) {
        p->total_time.tv_sec++;
        p->total_time.tv_nsec -= 1000000000L;
    }
```

---

## High-Resolution Profiling: Min/Max

```c
    if (elapsed.tv_sec < p->min_time.tv_sec ||
        (elapsed.tv_sec == p->min_time.tv_sec &&
         elapsed.tv_nsec < p->min_time.tv_nsec)) {
        p->min_time = elapsed;
    }

    if (elapsed.tv_sec > p->max_time.tv_sec ||
        (elapsed.tv_sec == p->max_time.tv_sec &&
         elapsed.tv_nsec > p->max_time.tv_nsec)) {
        p->max_time = elapsed;
    }

    p->count++;
}
```

---

## High-Resolution Profiling: Report

```c
void profile_report() {
    printf("\nProfile Report:\n");
    printf("%-30s %10s %12s %12s %12s\n",
           "Function", "Calls", "Total (ms)", "Avg (μs)", "Min/Max (μs)");
    printf("%s\n", "—————————————————————————————————————————————————————————————————————————");

    for (int i = 0; i < profile_count; i++) {
        ProfileEntry *p = &profiles[i];
        double total_ms = p->total_time.tv_sec * 1000.0 +
                         p->total_time.tv_nsec / 1e6;
        double avg_us = (p->total_time.tv_sec * 1e6 +
                        p->total_time.tv_nsec / 1e3) / p->count;
        double min_us = p->min_time.tv_sec * 1e6 +
                       p->min_time.tv_nsec / 1e3;
        double max_us = p->max_time.tv_sec * 1e6 +
                       p->max_time.tv_nsec / 1e3;

        printf("%-30s %10ld %12.2f %12.2f %6.1f/%.1f\n",
               p->name, p->count, total_ms, avg_us, min_us, max_us);
    }
}
```

---

## Leap Seconds: Status Check

```c
#include <time.h>
#include <sys/timex.h>

void check_time_status() {
    struct timex tx;
    memset(&tx, 0, sizeof(tx));

    int status = adjtimex(&tx);

    printf("Clock status: ");
    switch (status) {
        case TIME_OK:
            printf("Synchronized, no leap second\n");
            break;
        case TIME_INS:
            printf("Leap second will be inserted\n");
            break;
        case TIME_DEL:
            printf("Leap second will be deleted\n");
            break;
        case TIME_OOP:
            printf("Leap second in progress\n");
            break;
        case TIME_WAIT:
            printf("Leap second occurred\n");
            break;
        case TIME_ERROR:
            printf("Clock not synchronized\n");
            break;
    }
```

---

## Leap Seconds: Offset and Warnings

```c
    printf("Time offset: %ld μs\n", tx.offset);
    printf("Frequency offset: %ld ppm\n", tx.freq / 65536);
    printf("Maximum error: %ld μs\n", tx.maxerror);
    printf("Estimated error: %ld μs\n", tx.esterror);

    if (status == TIME_INS || status == TIME_DEL) {
        printf("Warning: Leap second approaching!\n");
        printf("Use CLOCK_MONOTONIC for intervals\n");
    }
}

int safe_time_compare(time_t t1, time_t t2) {
    struct tm *tm = gmtime(&t1);
    int risky = ((tm->tm_mon == 5 && tm->tm_mday == 30) ||
                 (tm->tm_mon == 11 && tm->tm_mday == 31)) &&
                tm->tm_hour == 23 && tm->tm_min == 59;

    if (risky) {
        return -2;
    }

    return (t1 < t2) ? -1 : (t1 > t2) ? 1 : 0;
}
```

---

## Y2038 Problem: Overflow Demo

```c
#include <time.h>
#include <stdio.h>
#include <limits.h>

void test_y2038_problem() {
    printf("sizeof(time_t) = %zu bytes\n", sizeof(time_t));
    printf("TIME_T_MAX = %ld\n", (long)((time_t)-1 > 0 ?
           (time_t)((1UL << (sizeof(time_t) * 8 - 1)) - 1) :
           (time_t)-1));

    time_t overflow_32bit = 2147483647;
    printf("32-bit overflow: %s", ctime(&overflow_32bit));

    overflow_32bit++;
    if (sizeof(time_t) == 4) {
        printf("After overflow: %ld (negative!)\n", (long)overflow_32bit);
    }

    if (sizeof(time_t) == 8) {
        time_t far_future = 253402300799;
        printf("64-bit can handle: %s", ctime(&far_future));

        time_t max_time = 9223372036854775807LL;
    }
}
```

---

## Y2038 Problem: Future-Proof

```c
typedef int64_t time64_t;

time64_t get_time64() {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME, &ts);
    return (time64_t)ts.tv_sec;
}
```

---

## Thread-Safe Time Functions: Safe vs Unsafe

```c
#include <time.h>
#include <pthread.h>

void thread_safe_time_operations() {
    time_t rawtime;
    time(&rawtime);

    // NOT thread-safe: localtime, asctime, ctime

    struct tm result;
    localtime_r(&rawtime, &result);

    char buffer[26];
    asctime_r(&result, buffer);
    ctime_r(&rawtime, buffer);
```

---

## Thread-Safe Time Functions: Thread CPU Time

```c
    struct timespec thread_time;
    clock_gettime(CLOCK_THREAD_CPUTIME_ID, &thread_time);
    printf("Thread CPU time: %ld.%09ld\n",
           thread_time.tv_sec, thread_time.tv_nsec);

    pthread_t other_thread;
    clockid_t clock_id;
    if (pthread_getcpuclockid(other_thread, &clock_id) == 0) {
        clock_gettime(clock_id, &thread_time);
    }
}

void format_time_threadsafe(time_t t, char *buf, size_t bufsize) {
    struct tm tm_result;
    localtime_r(&t, &tm_result);
    strftime(buf, bufsize, "%Y-%m-%d %H:%M:%S", &tm_result);
}
```

---

## Common Time Bugs: Wall Clock vs Monotonic

```c
void bug1_wrong() {
    time_t start = time(NULL);
    do_work();
    time_t elapsed = time(NULL) - start;
}

void bug1_correct() {
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    do_work();
    clock_gettime(CLOCK_MONOTONIC, &end);
}

void bug2_wrong() {
    int elapsed_ns = end_ns - start_ns;
}

void bug2_correct() {
    int64_t elapsed_ns = end_ns - start_ns;
}
```

---

## Common Time Bugs: EINTR and Comparison

```c
void bug3_wrong() {
    struct timespec req = {5, 0};
    nanosleep(&req, NULL);
}

void bug3_correct() {
    struct timespec req = {5, 0}, rem;
    while (nanosleep(&req, &rem) == -1 && errno == EINTR) {
        req = rem;
    }
}

int bug4_wrong(struct timespec *a, struct timespec *b) {
    return a->tv_sec == b->tv_sec && a->tv_nsec == b->tv_nsec;
}

int timespec_cmp(struct timespec *a, struct timespec *b) {
    if (a->tv_sec < b->tv_sec) return -1;
    if (a->tv_sec > b->tv_sec) return 1;
    if (a->tv_nsec < b->tv_nsec) return -1;
    if (a->tv_nsec > b->tv_nsec) return 1;
    return 0;
}
```

---

## Performance: Caching and Coarse Clocks

```c
void process_events(Event *events, int count) {
    struct timespec now;
    clock_gettime(CLOCK_MONOTONIC, &now);

    for (int i = 0; i < count; i++) {
        if (event_expired(&events[i], &now)) {
            handle_event(&events[i]);
        }
    }
}

void log_message(const char *msg) {
    struct timespec ts;
    clock_gettime(CLOCK_REALTIME_COARSE, &ts);
    printf("[%ld.%03ld] %s\n", ts.tv_sec, ts.tv_nsec / 1000000, msg);
}

typedef struct {
    int nfds;
    int timerfd[MAX_TIMERS];
    struct timespec next_expiry[MAX_TIMERS];
} TimerManager;
```

---

## Performance: Appropriate Precision

```c
void appropriate_precision() {
    time_t t = time(NULL);

    struct timeval tv;
    gettimeofday(&tv, NULL);

    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
}
```

---

## Real-Time System: Periodic Loop

```c
#include <sched.h>
#include <time.h>

void realtime_timing() {
    struct sched_param param = {.sched_priority = 50};
    sched_setscheduler(0, SCHED_FIFO, &param);

    struct timespec next_run, period = {0, 10000000};
    clock_gettime(CLOCK_MONOTONIC, &next_run);

    while (1) {
        do_realtime_work();

        next_run.tv_nsec += period.tv_nsec;
        if (next_run.tv_nsec >= 1000000000L) {
            next_run.tv_sec++;
            next_run.tv_nsec -= 1000000000L;
        }

        clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next_run, NULL);
    }
}
```

---

## Real-Time System: Jitter Measurement

```c
void measure_jitter() {
    struct timespec times[1000];
    struct timespec period = {0, 1000000};

    for (int i = 0; i < 1000; i++) {
        clock_gettime(CLOCK_MONOTONIC, &times[i]);
        clock_nanosleep(CLOCK_MONOTONIC, 0, &period, NULL);
    }

    long min_delta = LONG_MAX, max_delta = 0;
    for (int i = 1; i < 1000; i++) {
        long delta = (times[i].tv_sec - times[i-1].tv_sec) * 1000000000L +
                    (times[i].tv_nsec - times[i-1].tv_nsec);
        if (delta < min_delta) min_delta = delta;
        if (delta > max_delta) max_delta = delta;
    }

    printf("Jitter: %ld ns\n", max_delta - min_delta);
}
```

---

## Debugging Time Issues

```bash
# System time information
timedatectl status
date
hwclock --show

# Check NTP synchronization
ntpq -p
chronyc sources
systemctl status ntp

# Monitor system time changes
dmesg | grep -i clock
journalctl -u systemd-timesyncd

# Check process time usage
ps -o pid,etime,time,pcpu -p PID
cat /proc/PID/stat  # Fields 14-17 are times

# Trace time-related system calls
strace -e clock_gettime,gettimeofday,nanosleep ./program
strace -T ./program  # Show time spent in each syscall

# Profile with time
time ./program
/usr/bin/time -v ./program  # Detailed statistics

# Check timer interrupts
cat /proc/interrupts | grep -i timer
cat /proc/timer_list

# Monitor clock source
cat /sys/devices/system/clocksource/clocksource0/current_clocksource
cat /sys/devices/system/clocksource/clocksource0/available_clocksource
```

---

## Best Practices Summary

1. **Use CLOCK_MONOTONIC** for measuring intervals

1. **Use CLOCK_REALTIME** only for wall clock display

1. **Handle EINTR** in sleep/wait functions

1. **Use thread-safe** _r versions of time functions

1. **Cache time** when using multiple times

1. **Use appropriate precision** (don't over-engineer)

1. **Test for Y2038** on 32-bit systems

1. **Consider timerfd** for event-driven programs

1. **Profile hot paths** with high-resolution timers

1. **Document clock choice** in code comments

---

## Summary

## Key Takeaways:

- **Multiple clocks** serve different purposes
- **vDSO** makes time access fast (~25ns)
- **Monotonic clocks** prevent time-travel bugs
- **timerfd** integrates timers with event loops
- **Resolution ≠ Accuracy** - hardware matters
- **Thread-safety** requires _r functions
- **Y2038** affects 32-bit systems
- **Measure correctly** for reliable benchmarks

Master time = Build robust, efficient systems!
