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
# Secure Development

---

## Security in Systems Programming

1. **Defense in depth** - Multiple layers of security
1. **Principle of least privilege** - Minimal necessary permissions
1. **Input validation** - Never trust external data
1. **Memory safety** - Prevent buffer overflows and corruption
1. **Resource management** - Avoid resource exhaustion attacks
1. **Secure by default** - Safe defaults, explicit unsafe operations

---

## Stack Protection Overview

![stack_protection_overview](svg/courses/operating_systems/linux-systems-programming/23_secure_development/stack_protection_overview.svg)

---

## Stack Separation: Thread Info

```c
#include <pthread.h>
#include <sys/mman.h>

struct thread_info {
    pthread_t thread;
    void *stack_base;
    size_t stack_size;
    void *guard_page;
};
```

---

## Stack Separation: Create Thread

```c
struct thread_info *create_secure_thread(void *(*start_routine)(void *),
                                        void *arg) {
    struct thread_info *info = malloc(sizeof(*info));

    info->stack_size = 2 * 1024 * 1024;
    size_t total_size = info->stack_size + 2 * getpagesize();

    void *memory = mmap(NULL, total_size, PROT_READ | PROT_WRITE,
                       MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    if (memory == MAP_FAILED) {
        free(info);
        return NULL;
    }

    info->guard_page = memory;
    mprotect(memory, getpagesize(), PROT_NONE);
    mprotect(memory + getpagesize() + info->stack_size,
             getpagesize(), PROT_NONE);

    info->stack_base = memory + getpagesize();
```

---

## Stack Separation: Attributes and Cleanup

```c
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    pthread_attr_setstack(&attr, info->stack_base, info->stack_size);

    if (pthread_create(&info->thread, &attr, start_routine, arg) != 0) {
        munmap(memory, total_size);
        free(info);
        return NULL;
    }

    pthread_attr_destroy(&attr);
    return info;
}

void cleanup_secure_thread(struct thread_info *info) {
    pthread_join(info->thread, NULL);
    munmap(info->guard_page, info->stack_size + 2 * getpagesize());
    free(info);
}
```

---

## Stack Canaries: Compiler-Generated

```c
// Compile with: gcc -fstack-protector-strong

void vulnerable_function() {
    char buffer[256];

    printf("Enter data: ");
    gets(buffer);

    printf("You entered: %s\n", buffer);
}
```

---

## Stack Canaries: Manual Implementation

```c
volatile uintptr_t stack_canary = 0;

void init_stack_canary() {
    int fd = open("/dev/urandom", O_RDONLY);
    read(fd, &stack_canary, sizeof(stack_canary));
    close(fd);
}

int secure_function() {
    volatile uintptr_t canary = stack_canary;
    char buffer[256];

    process_buffer(buffer);

    if (canary != stack_canary) {
        abort();
    }

    return 0;
}
```

---

## ASLR: Memory Layout Demo

```c
void show_memory_layout() {
    static int static_var = 42;
    int stack_var = 123;
    void *heap_ptr = malloc(100);

    printf("Code segment (main): %p\n", (void*)main);
    printf("Data segment (static_var): %p\n", (void*)&static_var);
    printf("Stack (stack_var): %p\n", (void*)&stack_var);
    printf("Heap (malloc): %p\n", heap_ptr);
    printf("Library (printf): %p\n", (void*)printf);

    free(heap_ptr);
}

#include <sys/personality.h>

int disable_aslr() {
    if (personality(ADDR_NO_RANDOMIZE) == -1) {
        perror("personality");
        return -1;
    }
    return 0;
}
```

---

## ASLR: System Check

```c
int check_system_aslr() {
    FILE *fp = fopen("/proc/sys/kernel/randomize_va_space", "r");
    if (fp == NULL) {
        return -1;
    }

    int level;
    fscanf(fp, "%d", &level);
    fclose(fp);

    switch (level) {
        case 0:
            printf("ASLR: Disabled\n");
            break;
        case 1:
            printf("ASLR: Conservative (stack and heap)\n");
            break;
        case 2:
            printf("ASLR: Full (stack, heap, and libraries)\n");
            break;
    }

    return level;
}
```

---

## Library Randomization: Address Demo

```c
void show_library_addresses() {
    printf("libc base: %p\n", dlopen("libc.so.6", RTLD_LAZY));
    printf("libpthread: %p\n", dlopen("libpthread.so.0", RTLD_LAZY));

    system("cat /proc/self/maps | grep -E '\\.(so|dylib)'");
}
```

---

## Library Randomization: PIE Check

```c
int check_pie_enabled() {
    FILE *fp = popen("readelf -h /proc/self/exe", "r");
    if (fp == NULL) {
        return -1;
    }

    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        if (strstr(line, "Type:") && strstr(line, "DYN")) {
            printf("PIE enabled: Yes\n");
            pclose(fp);
            return 1;
        }
    }

    printf("PIE enabled: No\n");
    pclose(fp);
    return 0;
}

void debug_with_fixed_addresses() {
    printf("WARNING: ASLR should be re-enabled after debugging\n");
    printf("Run: echo 2 > /proc/sys/kernel/randomize_va_space\n");
}
```

---

## AppArmor vs SELinux

![apparmor_vs_selinux](svg/courses/operating_systems/linux-systems-programming/23_secure_development/apparmor_vs_selinux.svg)

---

## AppArmor: Status and Profile

```c
#include <sys/apparmor.h>

int check_apparmor_status() {
    if (aa_is_enabled()) {
        printf("AppArmor is enabled\n");
        return 1;
    } else {
        printf("AppArmor is disabled\n");
        return 0;
    }
}

int get_apparmor_profile() {
    char *profile = NULL;
    char *mode = NULL;

    if (aa_getcon(&profile, &mode) == 0) {
        printf("AppArmor profile: %s (%s)\n",
               profile ? profile : "unconfined",
               mode ? mode : "unknown");

        if (profile) free(profile);
        if (mode) free(mode);
        return 0;
    }

    return -1;
}
```

---

## AppArmor: Change Profile and Query

```c
int change_apparmor_profile(const char *profile) {
    if (aa_change_profile(profile) == 0) {
        printf("Changed to AppArmor profile: %s\n", profile);
        return 0;
    } else {
        perror("aa_change_profile");
        return -1;
    }
}

void read_proc_apparmor_info(pid_t pid) {
    char path[256];
    snprintf(path, sizeof(path), "/proc/%d/attr/current", pid);

    FILE *fp = fopen(path, "r");
    if (fp) {
        char profile[256];
        if (fgets(profile, sizeof(profile), fp)) {
            printf("PID %d AppArmor: %s", pid, profile);
        }
        fclose(fp);
    }
}
```

---

## SELinux: Status Check

```c
#include <selinux/selinux.h>

int check_selinux_status() {
    if (is_selinux_enabled()) {
        printf("SELinux is enabled\n");

        int mode = security_getenforce();
        switch (mode) {
            case 1:
                printf("SELinux mode: Enforcing\n");
                break;
            case 0:
                printf("SELinux mode: Permissive\n");
                break;
            default:
                printf("SELinux mode: Unknown\n");
                break;
        }
        return 1;
    } else {
        printf("SELinux is disabled\n");
        return 0;
    }
}
```

---

## SELinux: Get Context

```c
int get_selinux_context() {
    char *context = NULL;

    if (getcon(&context) == 0) {
        printf("SELinux context: %s\n", context);
        freecon(context);
        return 0;
    } else {
        perror("getcon");
        return -1;
    }
}

int get_file_selinux_context(const char *path) {
    char *context = NULL;

    if (getfilecon(path, &context) >= 0) {
        printf("File %s SELinux context: %s\n", path, context);
        freecon(context);
        return 0;
    } else {
        perror("getfilecon");
        return -1;
    }
}
```

---

## SELinux: Set Context

```c
int set_selinux_context(const char *context) {
    if (setcon(context) == 0) {
        printf("Set SELinux context to: %s\n", context);
        return 0;
    } else {
        perror("setcon");
        return -1;
    }
}
```

---

## Secure Coding Practices: Strings

```c
void safe_string_operations() {
    char dest[100];
    const char *src = "Hello, World!";

    // WRONG: strcpy, strcat, gets — no bounds checking

    strncpy(dest, src, sizeof(dest) - 1);
    dest[sizeof(dest) - 1] = '\0';

    strncat(dest, src, sizeof(dest) - strlen(dest) - 1);

    snprintf(dest, sizeof(dest), "%s", src);
}
```

---

## Secure Coding Practices: Integer Math

```c
int safe_integer_math(int a, int b) {
    if (a > 0 && b > INT_MAX - a) {
        printf("Addition overflow detected\n");
        return -1;
    }

    if (a < 0 && b < INT_MIN - a) {
        printf("Addition underflow detected\n");
        return -1;
    }

    return a + b;
}

void *safe_malloc(size_t size) {
    if (size == 0 || size > SIZE_MAX / 2) {
        errno = EINVAL;
        return NULL;
    }

    void *ptr = malloc(size);
    if (ptr == NULL) {
        fprintf(stderr, "Memory allocation failed for %zu bytes\n", size);
        return NULL;
    }

    memset(ptr, 0, size);
    return ptr;
}
```

---

## Input Validation: Integers

```c
int validate_integer_input(const char *input, int min, int max, int *result) {
    if (input == NULL) {
        return -1;
    }

    char *endptr;
    errno = 0;
    long val = strtol(input, &endptr, 10);

    if (errno != 0 || endptr == input || *endptr != '\0') {
        printf("Invalid integer format\n");
        return -1;
    }

    if (val < min || val > max) {
        printf("Integer out of range [%d, %d]\n", min, max);
        return -1;
    }

    *result = (int)val;
    return 0;
}
```

---

## Input Validation: File Paths

```c
int sanitize_file_path(const char *path, char *sanitized, size_t size) {
    if (path == NULL || sanitized == NULL || size == 0) {
        return -1;
    }

    if (strstr(path, "..") != NULL) {
        printf("Path traversal attempt detected\n");
        return -1;
    }

    if (path[0] == '/') {
        printf("Absolute path not allowed\n");
        return -1;
    }

    if (strlen(path) != strcspn(path, "\0")) {
        printf("Null byte in path\n");
        return -1;
    }

    strncpy(sanitized, path, size - 1);
    sanitized[size - 1] = '\0';

    return 0;
}
```

---

## Input Validation: Email

```c
int validate_email(const char *email) {
    if (email == NULL) {
        return -1;
    }

    size_t len = strlen(email);
    if (len < 5 || len > 254) {
        return -1;
    }

    char *at = strchr(email, '@');
    if (at == NULL || strchr(at + 1, '@') != NULL) {
        return -1;
    }

    if (at == email || at[1] == '\0') {
        return -1;
    }

    return 0;
}
```

---

## Secure File Operations: Creation

```c
int create_secure_file(const char *filename, mode_t mode) {
    char sanitized_path[PATH_MAX];
    if (sanitize_file_path(filename, sanitized_path, sizeof(sanitized_path)) != 0) {
        return -1;
    }

    int fd = open(sanitized_path, O_CREAT | O_WRONLY | O_EXCL, mode);
    if (fd == -1) {
        perror("open");
        return -1;
    }

    return fd;
}

int create_secure_temp_file(char *template) {
    int fd = mkstemp(template);
    if (fd == -1) {
        perror("mkstemp");
        return -1;
    }

    if (fchmod(fd, S_IRUSR | S_IWUSR) == -1) {
        perror("fchmod");
        close(fd);
        unlink(template);
        return -1;
    }

    return fd;
}
```

---

## Secure File Operations: Safe Read

```c
ssize_t read_file_safely(const char *filename, void *buffer, size_t max_size) {
    char sanitized_path[PATH_MAX];
    if (sanitize_file_path(filename, sanitized_path, sizeof(sanitized_path)) != 0) {
        return -1;
    }

    int fd = open(sanitized_path, O_RDONLY);
    if (fd == -1) {
        return -1;
    }

    struct stat st;
    if (fstat(fd, &st) == -1) {
        close(fd);
        return -1;
    }

    if (st.st_size > max_size) {
        printf("File too large: %ld bytes (max: %zu)\n", st.st_size, max_size);
        close(fd);
        return -1;
    }

    ssize_t bytes_read = read(fd, buffer, max_size);
    close(fd);

    return bytes_read;
}
```

---

## Memory Protection: Zeroing and Locking

```c
void secure_memzero(void *ptr, size_t size) {
    volatile unsigned char *volatile_ptr = (volatile unsigned char *)ptr;

    for (size_t i = 0; i < size; i++) {
        volatile_ptr[i] = 0;
    }
}

#ifdef __STDC_LIB_EXT1__
void clear_sensitive_data(void *data, size_t size) {
    memset_s(data, size, 0, size);
}
#endif

int protect_memory_region(void *addr, size_t size, int protection) {
    if (mprotect(addr, size, protection) == -1) {
        perror("mprotect");
        return -1;
    }

    return 0;
}

int lock_sensitive_memory(void *addr, size_t size) {
    if (mlock(addr, size) == -1) {
        perror("mlock");
        return -1;
    }

    return 0;
}
```

---

## Memory Protection: Guarded Allocation

```c
void *secure_alloc(size_t size) {
    size_t page_size = getpagesize();
    size_t total_size = size + 2 * page_size;

    void *memory = mmap(NULL, total_size, PROT_READ | PROT_WRITE,
                       MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    if (memory == MAP_FAILED) {
        return NULL;
    }

    mprotect(memory, page_size, PROT_NONE);
    mprotect((char*)memory + page_size + size, page_size, PROT_NONE);

    return (char*)memory + page_size;
}

void secure_free(void *ptr, size_t size) {
    if (ptr == NULL) {
        return;
    }

    secure_memzero(ptr, size);

    size_t page_size = getpagesize();
    void *original = (char*)ptr - page_size;
    size_t total_size = size + 2 * page_size;

    munmap(original, total_size);
}
```

---

## Cryptographic Security: Random and Hashing

```c
#include <openssl/evp.h>
#include <openssl/rand.h>

int generate_random_bytes(unsigned char *buffer, int length) {
    if (RAND_bytes(buffer, length) != 1) {
        printf("Failed to generate random bytes\n");
        return -1;
    }
    return 0;
}

int hash_password(const char *password, unsigned char *salt,
                 unsigned char *hash, int hash_len) {
    const int iterations = 10000;

    if (PKCS5_PBKDF2_HMAC(password, strlen(password),
                          salt, 16,
                          iterations,
                          EVP_sha256(),
                          hash_len, hash) != 1) {
        printf("Password hashing failed\n");
        return -1;
    }

    return 0;
}
```

---

## Cryptographic Security: AES-256 Encryption

```c
int encrypt_data(const unsigned char *plaintext, int plaintext_len,
                const unsigned char *key, const unsigned char *iv,
                unsigned char *ciphertext) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (ctx == NULL) {
        return -1;
    }

    if (EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }

    int len;
    int ciphertext_len;

    if (EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }
    ciphertext_len = len;

    if (EVP_EncryptFinal_ex(ctx, ciphertext + len, &len) != 1) {
        EVP_CIPHER_CTX_free(ctx);
        return -1;
    }
    ciphertext_len += len;

    EVP_CIPHER_CTX_free(ctx);
    return ciphertext_len;
}
```

---

## Network Security: SSL Context

```c
#include <openssl/ssl.h>

SSL_CTX *create_ssl_context(int server) {
    const SSL_METHOD *method;
    SSL_CTX *ctx;

    if (server) {
        method = TLS_server_method();
    } else {
        method = TLS_client_method();
    }

    ctx = SSL_CTX_new(method);
    if (ctx == NULL) {
        printf("Unable to create SSL context\n");
        ERR_print_errors_fp(stderr);
        return NULL;
    }

    SSL_CTX_set_min_proto_version(ctx, TLS1_2_VERSION);

    SSL_CTX_set_cipher_list(ctx, "ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20:!aNULL:!MD5:!DSS");

    return ctx;
}
```

---

## Network Security: Secure Sockets

```c
int create_secure_socket(const char *hostname, int port) {
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        return -1;
    }

    int reuse = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse));

    int nodelay = 1;
    setsockopt(sockfd, IPPROTO_TCP, TCP_NODELAY, &nodelay, sizeof(nodelay));

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);

    if (inet_pton(AF_INET, hostname, &addr.sin_addr) <= 0) {
        close(sockfd);
        return -1;
    }

    if (connect(sockfd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
        close(sockfd);
        return -1;
    }

    return sockfd;
}
```

---

## Network Security: Rate Limiting

```c
struct rate_limiter {
    time_t window_start;
    int request_count;
    int max_requests;
    int window_seconds;
};

int check_rate_limit(struct rate_limiter *limiter) {
    time_t now = time(NULL);

    if (now - limiter->window_start >= limiter->window_seconds) {
        limiter->window_start = now;
        limiter->request_count = 1;
        return 0;
    }

    if (limiter->request_count >= limiter->max_requests) {
        return -1;
    }

    limiter->request_count++;
    return 0;
}
```

---

## Process Security: Dropping Privileges

```c
#include <sys/prctl.h>
#include <sys/capability.h>

int drop_privileges(uid_t uid, gid_t gid) {
    if (setgroups(0, NULL) == -1) {
        perror("setgroups");
        return -1;
    }

    if (setgid(gid) == -1) {
        perror("setgid");
        return -1;
    }

    if (setuid(uid) == -1) {
        perror("setuid");
        return -1;
    }

    if (setuid(0) == 0) {
        printf("ERROR: Could regain root privileges\n");
        return -1;
    }

    return 0;
}
```

---

## Process Security: prctl Flags

```c
int set_process_security() {
    if (prctl(PR_SET_DUMPABLE, 0, 0, 0, 0) == -1) {
        perror("prctl PR_SET_DUMPABLE");
        return -1;
    }

    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) == -1) {
        perror("prctl PR_SET_NO_NEW_PRIVS");
        return -1;
    }

    if (prctl(PR_SET_NAME, "secure_daemon", 0, 0, 0) == -1) {
        perror("prctl PR_SET_NAME");
        return -1;
    }

    return 0;
}
```

---

## Process Security: Chroot Jail

```c
int setup_chroot_jail(const char *jail_path) {
    if (chdir(jail_path) == -1) {
        perror("chdir");
        return -1;
    }

    if (chroot(jail_path) == -1) {
        perror("chroot");
        return -1;
    }

    if (chdir("/") == -1) {
        perror("chdir to jail root");
        return -1;
    }

    return 0;
}
```

---

## Secure IPC: Unix Socket Setup

```c
int create_secure_unix_socket(const char *path) {
    int sockfd = socket(AF_UNIX, SOCK_STREAM, 0);
    if (sockfd == -1) {
        return -1;
    }

    struct sockaddr_un addr;
    memset(&addr, 0, sizeof(addr));
    addr.sun_family = AF_UNIX;
    strncpy(addr.sun_path, path, sizeof(addr.sun_path) - 1);

    unlink(path);

    if (bind(sockfd, (struct sockaddr*)&addr, sizeof(addr)) == -1) {
        close(sockfd);
        return -1;
    }

    if (chmod(path, S_IRUSR | S_IWUSR) == -1) {
        perror("chmod");
        close(sockfd);
        unlink(path);
        return -1;
    }

    if (listen(sockfd, 5) == -1) {
        close(sockfd);
        unlink(path);
        return -1;
    }

    return sockfd;
}
```

---

## Secure IPC: Peer Credentials

```c
int verify_peer_credentials(int sockfd, uid_t expected_uid, gid_t expected_gid) {
    struct ucred cred;
    socklen_t len = sizeof(cred);

    if (getsockopt(sockfd, SOL_SOCKET, SO_PEERCRED, &cred, &len) == -1) {
        perror("getsockopt SO_PEERCRED");
        return -1;
    }

    if (cred.uid != expected_uid || cred.gid != expected_gid) {
        printf("Peer credentials mismatch: uid=%d (expected %d), gid=%d (expected %d)\n",
               cred.uid, expected_uid, cred.gid, expected_gid);
        return -1;
    }

    return 0;
}
```

---

## Secure Signal Handling: Handler

```c
volatile sig_atomic_t signal_received = 0;
int signal_pipe[2];

void security_signal_handler(int signum) {
    char byte = (char)signum;
    write(signal_pipe[1], &byte, 1);
    signal_received = 1;
}

int setup_secure_signals() {
    if (pipe(signal_pipe) == -1) {
        perror("pipe");
        return -1;
    }

    int flags = fcntl(signal_pipe[1], F_GETFL);
    fcntl(signal_pipe[1], F_SETFL, flags | O_NONBLOCK);

    struct sigaction sa;
    sa.sa_handler = security_signal_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = SA_RESTART;

    sigaction(SIGTERM, &sa, NULL);
    sigaction(SIGINT, &sa, NULL);

    return 0;
}
```

---

## Secure Signal Handling: Process Signals

```c
void process_pending_signals() {
    char buffer[256];
    ssize_t bytes = read(signal_pipe[0], buffer, sizeof(buffer));

    for (ssize_t i = 0; i < bytes; i++) {
        int signum = (int)buffer[i];

        switch (signum) {
            case SIGTERM:
            case SIGINT:
                printf("Received termination signal, shutting down safely...\n");
                cleanup_and_exit();
                break;

            default:
                printf("Received signal %d\n", signum);
                break;
        }
    }
}
```

---

## Resource Limits: Core/FSIZE/NOFILE

```c
#include <sys/resource.h>

int set_security_limits() {
    struct rlimit limit;

    limit.rlim_cur = 0;
    limit.rlim_max = 0;
    if (setrlimit(RLIMIT_CORE, &limit) == -1) {
        perror("setrlimit RLIMIT_CORE");
        return -1;
    }

    limit.rlim_cur = 100 * 1024 * 1024;
    limit.rlim_max = 100 * 1024 * 1024;
    if (setrlimit(RLIMIT_FSIZE, &limit) == -1) {
        perror("setrlimit RLIMIT_FSIZE");
        return -1;
    }

    limit.rlim_cur = 1024;
    limit.rlim_max = 1024;
    if (setrlimit(RLIMIT_NOFILE, &limit) == -1) {
        perror("setrlimit RLIMIT_NOFILE");
        return -1;
    }
```

---

## Resource Limits: Memory and CPU

```c
    limit.rlim_cur = 512 * 1024 * 1024;
    limit.rlim_max = 512 * 1024 * 1024;
    if (setrlimit(RLIMIT_AS, &limit) == -1) {
        perror("setrlimit RLIMIT_AS");
        return -1;
    }

    limit.rlim_cur = 300;
    limit.rlim_max = 300;
    if (setrlimit(RLIMIT_CPU, &limit) == -1) {
        perror("setrlimit RLIMIT_CPU");
        return -1;
    }

    return 0;
}
```

---

## Resource Limits: Connection Limiter

```c
struct connection_limiter {
    int max_connections;
    int current_connections;
    time_t *connection_times;
    int connections_per_minute;
};

int check_connection_limit(struct connection_limiter *limiter) {
    time_t now = time(NULL);

    if (limiter->current_connections >= limiter->max_connections) {
        return -1;
    }

    int recent_connections = 0;
    for (int i = 0; i < limiter->max_connections; i++) {
        if (now - limiter->connection_times[i] < 60) {
            recent_connections++;
        }
    }

    if (recent_connections >= limiter->connections_per_minute) {
        return -1;
    }

    return 0;
}
```

---

## Audit and Logging: Event Logger

```c
#include <syslog.h>

void log_security_event(int level, const char *event, const char *details) {
    syslog(level, "SECURITY: %s - %s", event, details);

    FILE *fp = fopen("/var/log/security.log", "a");
    if (fp) {
        time_t now = time(NULL);
        char *timestr = ctime(&now);
        timestr[strlen(timestr) - 1] = '\0';

        fprintf(fp, "[%s] %s: %s\n", timestr, event, details);
        fclose(fp);
    }
}

struct auth_tracker {
    char ip_address[INET_ADDRSTRLEN];
    int failed_attempts;
    time_t last_attempt;
    time_t lockout_until;
};
```

---

## Audit and Logging: Auth Tracking

```c
int check_auth_attempts(struct auth_tracker *tracker, const char *ip) {
    time_t now = time(NULL);

    if (strcmp(tracker->ip_address, ip) != 0) {
        strncpy(tracker->ip_address, ip, sizeof(tracker->ip_address) - 1);
        tracker->failed_attempts = 0;
        tracker->lockout_until = 0;
    }

    if (tracker->lockout_until > now) {
        log_security_event(LOG_WARNING, "AUTH_BLOCKED", ip);
        return -1;
    }

    return 0;
}

void record_auth_failure(struct auth_tracker *tracker) {
    time_t now = time(NULL);
    tracker->failed_attempts++;
    tracker->last_attempt = now;

    if (tracker->failed_attempts >= 5) {
        tracker->lockout_until = now + 3600;
        log_security_event(LOG_ERR, "AUTH_LOCKOUT", tracker->ip_address);
    } else {
        log_security_event(LOG_WARNING, "AUTH_FAIL", tracker->ip_address);
    }
}
```

---

## Security Testing: Self-Tests

```c
int run_security_tests() {
    printf("Running security tests...\n");

    if (!test_stack_protection()) {
        printf("FAIL: Stack protection not working\n");
        return -1;
    }

    if (check_system_aslr() < 2) {
        printf("WARN: ASLR not fully enabled\n");
    }

    if (!test_privilege_dropping()) {
        printf("FAIL: Privilege dropping test failed\n");
        return -1;
    }

    if (!test_file_permissions()) {
        printf("FAIL: File permissions test failed\n");
        return -1;
    }

    printf("Security tests passed\n");
    return 0;
}
```

---

## Security Testing: Individual Tests

```c
int test_stack_protection() {
    void *stack_start = __builtin_frame_address(0);
    printf("Stack protection test: frame at %p\n", stack_start);

    return 1;
}

int test_privilege_dropping() {
    uid_t original_uid = getuid();

    if (original_uid == 0) {
        if (setuid(1000) == -1) {
            return 0;
        }

        if (setuid(0) == 0) {
            return 0;
        }

        return 1;
    }

    return 1;
}

int test_file_permissions() {
    struct stat st;

    if (stat("/etc/shadow", &st) == 0) {
        if (st.st_mode & (S_IROTH | S_IWOTH)) {
            return 0;
        }
    }

    return 1;
}
```

---

## Security Checklist

1. **Input Validation** - Validate all external input
1. **Buffer Overflow Protection** - Use safe string functions
1. **Privilege Management** - Drop privileges early, use capabilities
1. **Memory Protection** - Clear sensitive data, use guard pages
1. **File Security** - Proper permissions, avoid race conditions
1. **Network Security** - TLS/SSL, rate limiting, input validation

---

## Common Vulnerabilities to Avoid

1. **Buffer overflows** - Use bounded string functions
1. **Format string attacks** - Never pass user input as format string
1. **Race conditions** - Proper locking, atomic operations
1. **Path traversal** - Validate and sanitize file paths
1. **Integer overflow** - Check arithmetic operations
1. **Information disclosure** - Clear sensitive memory

---

## Defense in Depth Strategy

1. **Perimeter security** - Firewalls, network filtering
1. **Application security** - Input validation, safe coding
1. **System security** - ASLR, stack protection, MAC
1. **Process isolation** - Containers, sandboxing
1. **Monitoring** - Logging, intrusion detection
1. **Recovery** - Backup, incident response

---

## Security Tools and Analysis

1. **Static analysis** - Coverity, Clang Static Analyzer
1. **Dynamic analysis** - Valgrind, AddressSanitizer
1. **Fuzzing** - AFL, LibFuzzer for input testing
1. **Runtime protection** - Stack canaries, FORTIFY_SOURCE
1. **System hardening** - SELinux, AppArmor, grsecurity
1. **Penetration testing** - Regular security assessments

---

## Best Practices Summary

1. **Secure by default** - Safe defaults, explicit unsafe operations
1. **Fail securely** - Errors should not compromise security
1. **Principle of least privilege** - Minimal necessary permissions
1. **Defense in depth** - Multiple security layers
1. **Keep it simple** - Complex code is harder to secure
1. **Regular updates** - Keep systems and libraries current
