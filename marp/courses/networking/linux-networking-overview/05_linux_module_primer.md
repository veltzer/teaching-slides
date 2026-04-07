# Linux Module Primer
## Chapter 5: Kernel Module Development

---

## Chapter Overview

- Module Initialization
- Module Cleanup
- Kernel Module Compilation
- Kernel Logging
- Best Practices

---

## What is a Kernel Module

- Loadable kernel module (LKM)
- Extends kernel functionality
- Dynamically loaded/unloaded
- Runs in kernel space
- Has full kernel privileges

---

## Basic Module Structure

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>

static int __init my_module_init(void)
{
    pr_info("Module initialized\n");
    return 0;
}

static void __exit my_module_exit(void)
{
    pr_info("Module exiting\n");
}

module_init(my_module_init);
module_exit(my_module_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");
MODULE_DESCRIPTION("A simple kernel module");
```

---

## Module Initialization

```c
static int __init my_module_init(void)
{
    int ret;

    // Allocate resources
    ret = resource_allocation();
    if (ret < 0)
        return ret;

    // Initialize data structures
    if (!init_structures()) {
        cleanup_resources();
        return -ENOMEM;
    }

    return 0;
}
```

---

## Module Cleanup

```c
static void __exit my_module_exit(void)
{
    // Free allocated resources
    cleanup_resources();

    // Destroy data structures
    cleanup_structures();

    // Final cleanup
    pr_info("Cleanup complete\n");
}
```

---

## Module Parameters

```c
static int debug = 0;
module_param(debug, int, 0644);
MODULE_PARM_DESC(debug, "Enable debug mode (0/1)");

static char *device_name = "mydev";
module_param(device_name, charp, 0644);
MODULE_PARM_DESC(device_name, "Name of the device");
```

---

## Makefile for Kernel Modules

```makefile
obj-m += mymodule.o

all:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
    make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

---

## Kernel Logging Levels

```c
// Kernel log levels
#define KERN_EMERG    "<0>"  /* system is unusable */
#define KERN_ALERT    "<1>"  /* action must be taken immediately */
#define KERN_CRIT     "<2>"  /* critical conditions */
#define KERN_ERR      "<3>"  /* error conditions */
#define KERN_WARNING  "<4>"  /* warning conditions */
#define KERN_NOTICE   "<5>"  /* normal but significant */
#define KERN_INFO     "<6>"  /* informational */
#define KERN_DEBUG    "<7>"  /* debug-level messages */
```

---

## Logging Functions

```c
// Preferred logging functions
pr_emerg("System is unusable\n");
pr_alert("Action required\n");
pr_crit("Critical error\n");
pr_err("Error occurred\n");
pr_warning("Warning message\n");
pr_notice("Normal but significant\n");
pr_info("Information message\n");
pr_debug("Debug message\n");
```

---

## Loading and Unloading Modules

```bash
# Load module
insmod mymodule.ko
# or
modprobe mymodule

# Unload module
rmmod mymodule
# or
modprobe -r mymodule

# List loaded modules
lsmod

# Module information
modinfo mymodule.ko
```

---

## Module Dependencies

```c
// Module dependencies
#include <linux/module.h>

MODULE_DEPEND(mymodule, dependency, 1, 1, 2);
MODULE_SOFTDEPEND("pre: dependency");
MODULE_SOFTDEPEND("post: dependency");
```

---

## Error Handling

```c
static int __init my_module_init(void)
{
    int ret;

    ret = do_something();
    if (ret) {
        pr_err("Failed to do something: %d\n", ret);
        return ret;
    }

    if (!alloc_resource()) {
        pr_err("Failed to allocate resource\n");
        return -ENOMEM;
    }

    return 0;
}
```

---

## Resource Management

![resource_management](svg/courses/networking/linux-networking-overview/05_linux_module_primer/resource_management.svg)

---

## Memory Allocation

```c
// Kernel memory allocation
void *buf = kmalloc(size, GFP_KERNEL);
if (!buf)
    return -ENOMEM;

// Zeroed memory
void *buf = kzalloc(size, GFP_KERNEL);
if (!buf)
    return -ENOMEM;

// Free memory
kfree(buf);
```

---

## Kernel Symbols

```c
// Export symbol for other modules
EXPORT_SYMBOL(my_function);
EXPORT_SYMBOL_GPL(my_function);

// Symbol declaration
extern void external_function(void);

// Version dependency
MODULE_VERSION("1.0");
```

---

## Module Information

```c
// Module metadata
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Author Name");
MODULE_DESCRIPTION("Module description");
MODULE_VERSION("1.0");
MODULE_ALIAS("my-module");
```

---

## Debug Features

```c
#if defined(DEBUG)
    pr_debug("Debug: value = %d\n", value);
#endif

// Dynamic debug
#define DEBUG
#define pr_fmt(fmt) KBUILD_MODNAME ": " fmt
```

---

## Common Kernel APIs

```c
// Time functions
jiffies         // System uptime in ticks
get_jiffies_64()// 64-bit jiffies
msecs_to_jiffies(ms)  // Convert ms to jiffies

// Memory barriers
mb();           // Full memory barrier
rmb();          // Read memory barrier
wmb();          // Write memory barrier
```

---

## Synchronization

```c
// Spinlock
DEFINE_SPINLOCK(my_lock);
spin_lock(&my_lock);
// Critical section
spin_unlock(&my_lock);

// Mutex
DEFINE_MUTEX(my_mutex);
mutex_lock(&my_mutex);
// Critical section
mutex_unlock(&my_mutex);
```

---

## Module Testing

```bash
# Check module status
dmesg | tail

# Monitor kernel messages
tail -f /var/log/kern.log

# Debug module loading
modprobe -v mymodule

# Check module dependencies
modprobe --show-depends mymodule
```

---

## Best Practices

1. Error handling
1. Resource cleanup
1. Proper logging
1. Documentation
1. Version control
1. Testing
1. Security considerations

---

## Common Pitfalls

1. Memory leaks
1. Race conditions
1. Deadlocks
1. Stack overflow
1. Uninitialized data
1. Missing error checks
1. Improper cleanup

---

## Debugging Tools

![debugging_tools](svg/courses/networking/linux-networking-overview/05_linux_module_primer/debugging_tools.svg)

---

## Module Lifecycle

![module_lifecycle](svg/courses/networking/linux-networking-overview/05_linux_module_primer/module_lifecycle.svg)

---

## Summary

- Module structure
- Initialization/cleanup
- Resource management
- Error handling
- Debugging
- Best practices
