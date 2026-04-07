# Framework Issues: Namespaces and Cgroups

---

## Overview

1. **Namespaces** - Process isolation and virtualization
1. **Cgroups** - Resource control and limits
1. **Capabilities** - Fine-grained privilege control
1. **Containers** - Combining namespaces and cgroups
1. **Security implications** - Isolation boundaries
1. **Use cases** - When and how to apply these technologies

---

## Linux Namespaces

![linux_namespaces](/svg/courses/operating_systems/linux-systems-programming/22_framework_issues/linux_namespaces.svg)

---

## Types of Namespaces

```c
// Namespace types (from linux/sched.h)
CLONE_NEWPID    // Process ID namespace
CLONE_NEWNET    // Network namespace
CLONE_NEWNS     // Mount namespace
CLONE_NEWUTS    // UTS (hostname) namespace
CLONE_NEWIPC    // IPC namespace
CLONE_NEWUSER   // User namespace
CLONE_NEWCGROUP // Cgroup namespace (Linux 4.6+)
CLONE_NEWTIME   // Time namespace (Linux 5.6+)

// Example: Create new process with multiple namespaces
int flags = CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWNS;
pid_t pid = clone(child_function, child_stack + STACK_SIZE, flags, NULL);
```

---

## Creating Namespaces

```c
#define _GNU_SOURCE
#include <sched.h>
#include <sys/wait.h>

// Child function that runs in new namespace
int child_function(void *arg) {
    printf("Child PID in namespace: %d\n", getpid()); // Will be 1

    // Child has its own view of the system
    system("ps aux");

    return 0;
}

int create_namespace_example() {
    const int STACK_SIZE = 1024 * 1024;
    char *child_stack = malloc(STACK_SIZE);

    // Create child in new PID namespace
    pid_t pid = clone(child_function, child_stack + STACK_SIZE,
                     CLONE_NEWPID | SIGCHLD, NULL);

    if (pid == -1) {
        perror("clone");
        return -1;
    }

    printf("Parent: child PID is %d\n", pid);
    wait(NULL); // Wait for child

    free(child_stack);
    return 0;
}
```

---

## Entering Existing Namespaces

```c
#include <fcntl.h>

// Enter namespace of another process
int enter_namespace(pid_t target_pid, const char *ns_type) {
    char ns_path[256];
    snprintf(ns_path, sizeof(ns_path), "/proc/%d/ns/%s", target_pid, ns_type);

    int ns_fd = open(ns_path, O_RDONLY);
    if (ns_fd == -1) {
        perror("open namespace");
        return -1;
    }

    // Join the namespace
    if (setns(ns_fd, 0) == -1) {
        perror("setns");
        close(ns_fd);
        return -1;
    }

    close(ns_fd);
    return 0;
}

// Example: Enter network namespace of container
int join_container_network(pid_t container_pid) {
    if (enter_namespace(container_pid, "net") == 0) {
        printf("Joined network namespace of PID %d\n", container_pid);
        return 0;
    }
    return -1;
}
```

---

## Unshare System Call

```c
// Unshare - move calling process to new namespace
int create_isolated_process() {
    // Create new PID and network namespaces for current process
    if (unshare(CLONE_NEWPID | CLONE_NEWNET) == -1) {
        perror("unshare");
        return -1;
    }

    // After unshare, need to fork to see new PID namespace
    pid_t pid = fork();
    if (pid == 0) {
        printf("Child PID after unshare: %d\n", getpid()); // Should be 1
        exec_container_init();
    } else if (pid > 0) {
        wait(NULL);
    }

    return 0;
}

// Unshare specific namespace types
void demonstrate_unshare() {
    // Create new mount namespace
    unshare(CLONE_NEWNS);

    // Create new UTS namespace (hostname)
    unshare(CLONE_NEWUTS);
    sethostname("container", 9);

    // Create new IPC namespace
    unshare(CLONE_NEWIPC);
}
```

---

## PID Namespace Details

```c
// PID namespace demonstration
void pid_namespace_demo() {
    printf("Original PID: %d\n", getpid());

    const int STACK_SIZE = 1024 * 1024;
    char *stack = malloc(STACK_SIZE);

    pid_t child = clone(child_in_pid_ns, stack + STACK_SIZE,
                       CLONE_NEWPID | SIGCHLD, NULL);

    printf("Child PID from parent: %d\n", child);
    wait(NULL);

    free(stack);
}

int child_in_pid_ns(void *arg) {
    printf("Child PID (inside namespace): %d\n", getpid()); // 1
    printf("Parent PID (inside namespace): %d\n", getppid()); // 0

    // Fork another process
    pid_t grandchild = fork();
    if (grandchild == 0) {
        printf("Grandchild PID (inside namespace): %d\n", getpid()); // 2
        exit(0);
    } else {
        wait(NULL);
    }

    return 0;
}
```

---

## Network Namespace

```c
#include <sys/socket.h>
#include <linux/netlink.h>

// Create network namespace and configure interface
int setup_network_namespace() {
    // Create new network namespace
    if (unshare(CLONE_NEWNET) == -1) {
        perror("unshare CLONE_NEWNET");
        return -1;
    }

    // The new namespace starts with only loopback interface
    // and it's down - need to bring it up
    system("ip link set lo up");

    return 0;
}

// Create virtual ethernet pair
int create_veth_pair(const char *veth1, const char *veth2) {
    char cmd[256];

    // Create veth pair
    snprintf(cmd, sizeof(cmd), "ip link add %s type veth peer name %s",
             veth1, veth2);

    if (system(cmd) != 0) {
        return -1;
    }

    return 0;
}

// Move interface to namespace
int move_interface_to_namespace(const char *interface, pid_t target_pid) {
    char cmd[256];
    snprintf(cmd, sizeof(cmd), "ip link set %s netns %d",
             interface, target_pid);

    return system(cmd) == 0 ? 0 : -1;
}
```

---

## Mount Namespace

```c
#include <sys/mount.h>

// Mount namespace demonstration
int mount_namespace_demo() {
    // Create new mount namespace
    if (unshare(CLONE_NEWNS) == -1) {
        perror("unshare CLONE_NEWNS");
        return -1;
    }

    // Make all mounts private (don't propagate)
    if (mount("none", "/", NULL, MS_REC | MS_PRIVATE, NULL) == -1) {
        perror("make mounts private");
        return -1;
    }

    // Create and mount tmpfs
    if (mkdir("/tmp/container_tmp", 0755) == -1 && errno != EEXIST) {
        perror("mkdir");
        return -1;
    }

    if (mount("tmpfs", "/tmp/container_tmp", "tmpfs", 0, "size=100M") == -1) {
        perror("mount tmpfs");
        return -1;
    }

    printf("Mounted tmpfs in isolated namespace\n");

    // Change root filesystem (chroot-like)
    setup_container_rootfs();

    return 0;
}

// Setup minimal container root filesystem
int setup_container_rootfs() {
    const char *container_root = "/tmp/container_root";

    // Create basic directory structure
    mkdir(container_root, 0755);
    mkdir("/tmp/container_root/bin", 0755);
    mkdir("/tmp/container_root/lib", 0755);
    mkdir("/tmp/container_root/proc", 0755);
    mkdir("/tmp/container_root/dev", 0755);
    mkdir("/tmp/container_root/sys", 0755);

    // Bind mount essential directories
    mount("/bin", "/tmp/container_root/bin", NULL, MS_BIND, NULL);
    mount("/lib", "/tmp/container_root/lib", NULL, MS_BIND, NULL);

    // Change root
    if (chroot(container_root) == -1) {
        perror("chroot");
        return -1;
    }

    chdir("/");

    // Mount proc and sys in new root
    mount("proc", "/proc", "proc", 0, NULL);
    mount("sysfs", "/sys", "sysfs", 0, NULL);

    return 0;
}
```

---

## User Namespace

```c
#include <sys/capability.h>

// User namespace provides privilege isolation
int user_namespace_demo() {
    uid_t original_uid = getuid();
    gid_t original_gid = getgid();

    printf("Original UID: %d, GID: %d\n", original_uid, original_gid);

    // Create new user namespace
    if (unshare(CLONE_NEWUSER) == -1) {
        perror("unshare CLONE_NEWUSER");
        return -1;
    }

    printf("After unshare - UID: %d, GID: %d\n", getuid(), getgid());

    // Setup UID/GID mappings
    setup_uid_mapping(getpid(), 0, original_uid, 1);
    setup_gid_mapping(getpid(), 0, original_gid, 1);

    printf("After mapping - UID: %d, GID: %d\n", getuid(), getgid());

    return 0;
}

int setup_uid_mapping(pid_t pid, int inside_uid, int outside_uid, int length) {
    char path[256];
    char mapping[256];

    snprintf(path, sizeof(path), "/proc/%d/uid_map", pid);
    snprintf(mapping, sizeof(mapping), "%d %d %d",
             inside_uid, outside_uid, length);

    int fd = open(path, O_WRONLY);
    if (fd == -1) {
        perror("open uid_map");
        return -1;
    }

    if (write(fd, mapping, strlen(mapping)) == -1) {
        perror("write uid_map");
        close(fd);
        return -1;
    }

    close(fd);
    return 0;
}

int setup_gid_mapping(pid_t pid, int inside_gid, int outside_gid, int length) {
    char path[256];
    char mapping[256];

    // First, deny setgroups to enable gid_map writing
    snprintf(path, sizeof(path), "/proc/%d/setgroups", pid);
    int fd = open(path, O_WRONLY);
    if (fd != -1) {
        write(fd, "deny", 4);
        close(fd);
    }

    snprintf(path, sizeof(path), "/proc/%d/gid_map", pid);
    snprintf(mapping, sizeof(mapping), "%d %d %d",
             inside_gid, outside_gid, length);

    fd = open(path, O_WRONLY);
    if (fd == -1) {
        perror("open gid_map");
        return -1;
    }

    if (write(fd, mapping, strlen(mapping)) == -1) {
        perror("write gid_map");
        close(fd);
        return -1;
    }

    close(fd);
    return 0;
}
```

---

## Cgroups Overview

![cgroups_overview](/svg/courses/operating_systems/linux-systems-programming/22_framework_issues/cgroups_overview.svg)

---

## Cgroups v1 vs v2

```c
// Cgroup paths differ between v1 and v2
#define CGROUP_V1_PATH "/sys/fs/cgroup"
#define CGROUP_V2_PATH "/sys/fs/cgroup"

// Check cgroup version
int get_cgroup_version() {
    struct stat st;

    // Check for cgroup2 filesystem
    if (stat("/sys/fs/cgroup/cgroup.controllers", &st) == 0) {
        return 2; // Cgroups v2
    } else if (stat("/sys/fs/cgroup/memory", &st) == 0) {
        return 1; // Cgroups v1
    }

    return 0; // No cgroups or unknown
}

// Create cgroup (v1)
int create_cgroup_v1(const char *controller, const char *group_name) {
    char path[512];
    snprintf(path, sizeof(path), "/sys/fs/cgroup/%s/%s",
             controller, group_name);

    if (mkdir(path, 0755) == -1 && errno != EEXIST) {
        perror("mkdir cgroup");
        return -1;
    }

    return 0;
}

// Create cgroup (v2)
int create_cgroup_v2(const char *group_name) {
    char path[512];
    snprintf(path, sizeof(path), "/sys/fs/cgroup/%s", group_name);

    if (mkdir(path, 0755) == -1 && errno != EEXIST) {
        perror("mkdir cgroup v2");
        return -1;
    }

    return 0;
}
```

---

## Memory Cgroup Control

```c
// Set memory limit for cgroup
int set_memory_limit(const char *cgroup_name, long long bytes) {
    char path[512];
    char limit_str[64];

    // Cgroups v1
    snprintf(path, sizeof(path),
             "/sys/fs/cgroup/memory/%s/memory.limit_in_bytes", cgroup_name);

    snprintf(limit_str, sizeof(limit_str), "%lld", bytes);

    int fd = open(path, O_WRONLY);
    if (fd == -1) {
        perror("open memory limit");
        return -1;
    }

    if (write(fd, limit_str, strlen(limit_str)) == -1) {
        perror("write memory limit");
        close(fd);
        return -1;
    }

    close(fd);
    return 0;
}

// Add process to memory cgroup
int add_process_to_memory_cgroup(const char *cgroup_name, pid_t pid) {
    char path[512];
    char pid_str[32];

    snprintf(path, sizeof(path),
             "/sys/fs/cgroup/memory/%s/cgroup.procs", cgroup_name);
    snprintf(pid_str, sizeof(pid_str), "%d", pid);

    int fd = open(path, O_WRONLY);
    if (fd == -1) {
        perror("open cgroup.procs");
        return -1;
    }

    if (write(fd, pid_str, strlen(pid_str)) == -1) {
        perror("write cgroup.procs");
        close(fd);
        return -1;
    }

    close(fd);
    return 0;
}

// Read memory usage
long long read_memory_usage(const char *cgroup_name) {
    char path[512];
    char buffer[64];

    snprintf(path, sizeof(path),
             "/sys/fs/cgroup/memory/%s/memory.usage_in_bytes", cgroup_name);

    int fd = open(path, O_RDONLY);
    if (fd == -1) {
        return -1;
    }

    ssize_t bytes = read(fd, buffer, sizeof(buffer) - 1);
    close(fd);

    if (bytes > 0) {
        buffer[bytes] = '\0';
        return strtoll(buffer, NULL, 10);
    }

    return -1;
}
```

---

## CPU Cgroup Control

```c
// Set CPU quota and period
int set_cpu_quota(const char *cgroup_name, int quota_us, int period_us) {
    char path[512];
    char value_str[32];

    // Set CPU period (cgroups v1)
    snprintf(path, sizeof(path),
             "/sys/fs/cgroup/cpu/%s/cpu.cfs_period_us", cgroup_name);
    snprintf(value_str, sizeof(value_str), "%d", period_us);

    int fd = open(path, O_WRONLY);
    if (fd != -1) {
        write(fd, value_str, strlen(value_str));
        close(fd);
    }

    // Set CPU quota
    snprintf(path, sizeof(path),
             "/sys/fs/cgroup/cpu/%s/cpu.cfs_quota_us", cgroup_name);
    snprintf(value_str, sizeof(value_str), "%d", quota_us);

    fd = open(path, O_WRONLY);
    if (fd == -1) {
        return -1;
    }

    if (write(fd, value_str, strlen(value_str)) == -1) {
        perror("write cpu quota");
        close(fd);
        return -1;
    }

    close(fd);
    return 0;
}

// Set CPU shares (relative weight)
int set_cpu_shares(const char *cgroup_name, int shares) {
    char path[512];
    char shares_str[32];

    snprintf(path, sizeof(path),
             "/sys/fs/cgroup/cpu/%s/cpu.shares", cgroup_name);
    snprintf(shares_str, sizeof(shares_str), "%d", shares);

    int fd = open(path, O_WRONLY);
    if (fd == -1) {
        return -1;
    }

    if (write(fd, shares_str, strlen(shares_str)) == -1) {
        perror("write cpu shares");
        close(fd);
        return -1;
    }

    close(fd);
    return 0;
}
```

---

## Block I/O Cgroup Control

```c
// Set I/O bandwidth limits
int set_blkio_bandwidth(const char *cgroup_name, const char *device,
                       long long read_bps, long long write_bps) {
    char path[512];
    char limit_str[128];

    // Set read bandwidth limit
    snprintf(path, sizeof(path),
             "/sys/fs/cgroup/blkio/%s/blkio.throttle.read_bps_device",
             cgroup_name);
    snprintf(limit_str, sizeof(limit_str), "%s %lld", device, read_bps);

    int fd = open(path, O_WRONLY);
    if (fd != -1) {
        write(fd, limit_str, strlen(limit_str));
        close(fd);
    }

    // Set write bandwidth limit
    snprintf(path, sizeof(path),
             "/sys/fs/cgroup/blkio/%s/blkio.throttle.write_bps_device",
             cgroup_name);
    snprintf(limit_str, sizeof(limit_str), "%s %lld", device, write_bps);

    fd = open(path, O_WRONLY);
    if (fd != -1) {
        write(fd, limit_str, strlen(limit_str));
        close(fd);
    }

    return 0;
}

// Set I/O priority (weight)
int set_blkio_weight(const char *cgroup_name, int weight) {
    char path[512];
    char weight_str[32];

    snprintf(path, sizeof(path),
             "/sys/fs/cgroup/blkio/%s/blkio.weight", cgroup_name);
    snprintf(weight_str, sizeof(weight_str), "%d", weight);

    int fd = open(path, O_WRONLY);
    if (fd == -1) {
        return -1;
    }

    if (write(fd, weight_str, strlen(weight_str)) == -1) {
        perror("write blkio weight");
        close(fd);
        return -1;
    }

    close(fd);
    return 0;
}
```

---

## Capabilities System

```c
#include <sys/capability.h>
#include <sys/prctl.h>

// Drop all capabilities except specified ones
int drop_capabilities_except(cap_value_t *keep_caps, int num_caps) {
    cap_t caps = cap_get_proc();
    if (caps == NULL) {
        return -1;
    }

    // Clear all capabilities
    if (cap_clear(caps) == -1) {
        cap_free(caps);
        return -1;
    }

    // Set only the capabilities we want to keep
    if (num_caps > 0) {
        if (cap_set_flag(caps, CAP_EFFECTIVE, num_caps, keep_caps,
                        CAP_SET) == -1 ||
            cap_set_flag(caps, CAP_PERMITTED, num_caps, keep_caps,
                        CAP_SET) == -1) {
            cap_free(caps);
            return -1;
        }
    }

    // Apply the capability set
    if (cap_set_proc(caps) == -1) {
        cap_free(caps);
        return -1;
    }

    cap_free(caps);
    return 0;
}

// Example: Keep only network capabilities
int setup_network_capabilities() {
    cap_value_t caps[] = {
        CAP_NET_BIND_SERVICE,  // Bind to ports < 1024
        CAP_NET_RAW           // Use raw sockets
    };

    return drop_capabilities_except(caps, 2);
}

// Set capability bounding set
int set_capability_bounding_set(cap_value_t *caps, int num_caps) {
    // Drop all capabilities from bounding set first
    for (int i = 0; i <= CAP_LAST_CAP; i++) {
        if (prctl(PR_CAPBSET_DROP, i, 0, 0, 0) == -1) {
            // Some capabilities might not exist
            if (errno != EINVAL) {
                return -1;
            }
        }
    }

    // This doesn't work - bounding set can only be reduced
    // We've already dropped all, so we're done
    return 0;
}
```

---

## Complete Container Creation

```c
// Create a complete container with isolation
struct container_config {
    char *hostname;
    char *root_path;
    long long memory_limit;
    int cpu_shares;
    uid_t uid;
    gid_t gid;
    cap_value_t *capabilities;
    int num_capabilities;
};

int create_container(struct container_config *config) {
    const int STACK_SIZE = 1024 * 1024;
    char *stack = malloc(STACK_SIZE);

    // Create all namespaces
    int flags = CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWNS |
                CLONE_NEWUTS | CLONE_NEWIPC | CLONE_NEWUSER;

    pid_t container_pid = clone(container_init, stack + STACK_SIZE,
                               flags | SIGCHLD, config);

    if (container_pid == -1) {
        perror("clone");
        free(stack);
        return -1;
    }

    // Setup from parent process
    setup_container_cgroups(container_pid, config);
    setup_container_network(container_pid);

    // Wait for container
    int status;
    waitpid(container_pid, &status, 0);

    free(stack);
    return WEXITSTATUS(status);
}

int container_init(void *arg) {
    struct container_config *config = (struct container_config *)arg;

    // Set hostname
    sethostname(config->hostname, strlen(config->hostname));

    // Setup user namespace mappings
    setup_uid_mapping(getpid(), 0, config->uid, 1);
    setup_gid_mapping(getpid(), 0, config->gid, 1);

    // Setup mount namespace
    setup_container_mounts(config->root_path);

    // Drop capabilities
    drop_capabilities_except(config->capabilities, config->num_capabilities);

    // Change to non-root user
    setuid(1000);
    setgid(1000);

    // Execute container process
    execl("/bin/sh", "/bin/sh", NULL);

    return 1; // Should not reach here
}
```

---

## Container Resource Setup

```c
int setup_container_cgroups(pid_t container_pid, struct container_config *config) {
    char cgroup_name[256];
    snprintf(cgroup_name, sizeof(cgroup_name), "container_%d", container_pid);

    // Create cgroups
    create_cgroup_v1("memory", cgroup_name);
    create_cgroup_v1("cpu", cgroup_name);
    create_cgroup_v1("blkio", cgroup_name);

    // Set limits
    set_memory_limit(cgroup_name, config->memory_limit);
    set_cpu_shares(cgroup_name, config->cpu_shares);

    // Add container process to cgroups
    add_process_to_memory_cgroup(cgroup_name, container_pid);
    add_process_to_cpu_cgroup(cgroup_name, container_pid);
    add_process_to_blkio_cgroup(cgroup_name, container_pid);

    return 0;
}

int setup_container_network(pid_t container_pid) {
    // Create veth pair
    create_veth_pair("veth_host", "veth_container");

    // Move container side to container namespace
    move_interface_to_namespace("veth_container", container_pid);

    // Setup host side
    system("ip addr add 192.168.1.1/24 dev veth_host");
    system("ip link set veth_host up");

    return 0;
}

int setup_container_mounts(const char *root_path) {
    // Change root
    if (chroot(root_path) == -1) {
        perror("chroot");
        return -1;
    }

    chdir("/");

    // Mount essential filesystems
    mount("proc", "/proc", "proc", 0, NULL);
    mount("sysfs", "/sys", "sysfs", 0, NULL);
    mount("tmpfs", "/tmp", "tmpfs", 0, "size=100M");
    mount("tmpfs", "/dev/shm", "tmpfs", 0, "size=64M");

    return 0;
}
```

---

## Monitoring and Debugging

```c
// Read cgroup statistics
struct cgroup_stats {
    long long memory_usage;
    long long memory_limit;
    long long cpu_usage;
    long long blkio_read;
    long long blkio_write;
};

int read_cgroup_stats(const char *cgroup_name, struct cgroup_stats *stats) {
    // Memory stats
    stats->memory_usage = read_memory_usage(cgroup_name);
    stats->memory_limit = read_cgroup_value("memory", cgroup_name,
                                           "memory.limit_in_bytes");

    // CPU stats
    stats->cpu_usage = read_cgroup_value("cpuacct", cgroup_name,
                                        "cpuacct.usage");

    // Block I/O stats
    stats->blkio_read = read_blkio_stat(cgroup_name, "Read");
    stats->blkio_write = read_blkio_stat(cgroup_name, "Write");

    return 0;
}

long long read_cgroup_value(const char *controller, const char *cgroup_name,
                           const char *filename) {
    char path[512];
    char buffer[64];

    snprintf(path, sizeof(path), "/sys/fs/cgroup/%s/%s/%s",
             controller, cgroup_name, filename);

    int fd = open(path, O_RDONLY);
    if (fd == -1) {
        return -1;
    }

    ssize_t bytes = read(fd, buffer, sizeof(buffer) - 1);
    close(fd);

    if (bytes > 0) {
        buffer[bytes] = '\0';
        return strtoll(buffer, NULL, 10);
    }

    return -1;
}

// List processes in cgroup
int list_cgroup_processes(const char *cgroup_name) {
    char path[512];
    snprintf(path, sizeof(path), "/sys/fs/cgroup/memory/%s/cgroup.procs",
             cgroup_name);

    FILE *fp = fopen(path, "r");
    if (fp == NULL) {
        return -1;
    }

    pid_t pid;
    printf("Processes in cgroup %s:\n", cgroup_name);
    while (fscanf(fp, "%d", &pid) == 1) {
        printf("  PID: %d\n", pid);
    }

    fclose(fp);
    return 0;
}
```

---

## Security Considerations

```c
// Security best practices for containers
int secure_container_setup() {
    // 1. Use user namespaces
    if (unshare(CLONE_NEWUSER) == -1) {
        perror("unshare user namespace");
        return -1;
    }

    // 2. Drop unnecessary capabilities
    cap_value_t no_caps[] = {
        CAP_SYS_ADMIN,    // System administration
        CAP_SYS_MODULE,   // Load kernel modules
        CAP_SYS_TIME,     // Set system time
        CAP_MKNOD,        // Create device files
    };

    for (int i = 0; i < 4; i++) {
        if (prctl(PR_CAPBSET_DROP, no_caps[i], 0, 0, 0) == -1) {
            perror("drop capability");
        }
    }

    // 3. Set no-new-privs
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) == -1) {
        perror("set no new privs");
        return -1;
    }

    // 4. Set up seccomp filter (simplified)
    setup_seccomp_filter();

    return 0;
}

// Basic seccomp filter
int setup_seccomp_filter() {
    // This is a simplified example
    // Real implementations use libseccomp

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT, 0, 0, 0) == -1) {
        if (errno != EINVAL) { // SECCOMP might not be available
            perror("seccomp");
            return -1;
        }
    }

    return 0;
}
```

---

## Container Runtime Integration

```c
// Simple container runtime interface
struct container_runtime {
    char *name;
    pid_t pid;
    struct container_config config;
    struct cgroup_stats stats;
    enum { CREATED, RUNNING, STOPPED } state;
};

int start_container(struct container_runtime *runtime) {
    runtime->pid = create_container(&runtime->config);
    if (runtime->pid > 0) {
        runtime->state = RUNNING;
        return 0;
    }
    return -1;
}

int stop_container(struct container_runtime *runtime) {
    if (runtime->state == RUNNING) {
        kill(runtime->pid, SIGTERM);

        // Wait for graceful shutdown
        sleep(5);

        // Force kill if still running
        if (kill(runtime->pid, 0) == 0) {
            kill(runtime->pid, SIGKILL);
        }

        waitpid(runtime->pid, NULL, 0);
        runtime->state = STOPPED;

        // Cleanup cgroups
        cleanup_container_cgroups(runtime->name);
    }

    return 0;
}

int cleanup_container_cgroups(const char *container_name) {
    char path[512];

    // Remove cgroup directories
    snprintf(path, sizeof(path), "/sys/fs/cgroup/memory/%s", container_name);
    rmdir(path);

    snprintf(path, sizeof(path), "/sys/fs/cgroup/cpu/%s", container_name);
    rmdir(path);

    snprintf(path, sizeof(path), "/sys/fs/cgroup/blkio/%s", container_name);
    rmdir(path);

    return 0;
}
```

---

## Performance Tuning

```c
// Optimize cgroup performance
int optimize_cgroup_performance(const char *cgroup_name) {
    // Disable swap for memory cgroup
    char path[512];
    snprintf(path, sizeof(path),
             "/sys/fs/cgroup/memory/%s/memory.swappiness", cgroup_name);

    int fd = open(path, O_WRONLY);
    if (fd != -1) {
        write(fd, "0", 1); // Disable swap
        close(fd);
    }

    // Set memory reclaim behavior
    snprintf(path, sizeof(path),
             "/sys/fs/cgroup/memory/%s/memory.oom_control", cgroup_name);

    fd = open(path, O_WRONLY);
    if (fd != -1) {
        write(fd, "1", 1); // Disable OOM killer
        close(fd);
    }

    // Optimize CPU scheduling
    set_cpu_shares(cgroup_name, 1024); // Normal priority

    return 0;
}

// Monitor resource pressure
int monitor_resource_pressure(const char *cgroup_name) {
    // Check memory pressure
    long long usage = read_memory_usage(cgroup_name);
    long long limit = read_cgroup_value("memory", cgroup_name,
                                       "memory.limit_in_bytes");

    if (usage > 0 && limit > 0) {
        double utilization = (double)usage / limit;
        if (utilization > 0.9) {
            printf("WARNING: Memory utilization high: %.1f%%\n",
                   utilization * 100);
        }
    }

    // Check for memory events
    long long oom_kill = read_cgroup_value("memory", cgroup_name,
                                          "memory.oom_control");
    if (oom_kill > 0) {
        printf("WARNING: OOM events detected\n");
    }

    return 0;
}
```

---

## Use Cases and Best Practices

1. **Containers** - Combine namespaces + cgroups + capabilities
1. **Resource isolation** - Prevent resource starvation
1. **Security boundaries** - Limit access to system resources
1. **Development environments** - Isolated build/test environments
1. **Service management** - Control resource usage per service
1. **Multi-tenancy** - Safe resource sharing

---

## When to Use These Technologies

1. **Namespaces** - Process isolation, virtualization
1. **Cgroups** - Resource limits, accounting, prioritization
1. **Capabilities** - Fine-grained privilege control
1. **User namespaces** - Rootless containers
1. **Network namespaces** - Network isolation
1. **Mount namespaces** - Filesystem isolation

---

## Common Pitfalls

1. **Privilege escalation** - Improper capability handling
1. **Resource exhaustion** - Insufficient limits
1. **Namespace pollution** - Unintended sharing
1. **Cgroup hierarchy** - Complex inheritance rules
1. **Mount propagation** - Unexpected filesystem visibility
1. **PID wraparound** - PID namespace limitations

---

## Debugging and Troubleshooting

1. **Check namespace membership** - `/proc/PID/ns/`
1. **Monitor cgroup usage** - `/sys/fs/cgroup/*/cgroup_name/`
1. **Verify capabilities** - `getpcaps`, `/proc/PID/status`
1. **Network debugging** - `ip netns`, `nsenter`
1. **Mount debugging** - `/proc/PID/mounts`
1. **Process tree** - `pstree`, `systemd-cgls`

---

## Future Developments

1. **Cgroups v2** - Unified hierarchy, improved API
1. **Time namespaces** - Virtualize system time
1. **CLONE_NEWTIME** - Per-container time management
1. **Enhanced security** - Better isolation mechanisms
1. **Performance improvements** - Reduced overhead
1. **Better tooling** - Improved debugging and monitoring
