# Introduction to UNIX
## Understanding the Fundamentals

![h:500](../../../raw/unix.svg) ![h:500,width:50%](../../../raw/ken_thompson.jpg)

---
## What is UNIX?

- Multi-user operating system
- Built in the 1970s at AT&T Bell Labs
- Key characteristics:
    - Modularity
    - Simple tools that do one thing well
    - Text-based configuration
    - Everything is a file philosophy
---
## History of UNIX

![0](../../../out/mermaid/marp/courses/linux-fundamentals/00_intro.md/0.png)

---
## Operating System Core Structure

![1](../../../out/mermaid/marp/courses/linux-fundamentals/00_intro.md/1.png)

---
## The Process Tree

![2](../../../out/mermaid/marp/courses/linux-fundamentals/00_intro.md/2.png)

## Why is it important?
- Process management
- Resource tracking
- System organization
- Parent-child relationships

---

## Process Lifecycle

![3](../../../out/mermaid/marp/courses/linux-fundamentals/00_intro.md/3.png)

### Zombie Processes
- Terminated but not yet cleaned up
- Parent must read exit status
- Adopted by init if parent dies

---
## System Calls

Example of a simple system call in C:
```c
#include <unistd.h>
#include <fcntl.h>

int main() {
    // Open system call
    int fd = open("file.txt", O_RDONLY);
    
    // Read system call
    char buffer[100];
    read(fd, buffer, 100);
    
    // Close system call
    close(fd);
    return 0;
}
```

---
## Basic Security Model

![4](../../../out/mermaid/marp/courses/linux-fundamentals/00_intro.md/4.png)

### Key Security Features:
- File system permissions
- Process isolation
- User/group-based access control
---
## The Root User

- UID 0
- Special characteristics:
    - Bypasses permission checks
    - Can access all files
    - Can manipulate all processes
  
```bash
# Example of root privileges
sudo su -
whoami  # Returns "root"
touch /root/test_file  # Succeeds
chmod 777 /some/system/file  # Succeeds
```

---
## File System Security

![5](../../../out/mermaid/marp/courses/linux-fundamentals/00_intro.md/5.png)

Example permission setting:
```bash
# Setting permissions
chmod 755 file.txt  # rwxr-xr-x
chown user:group file.txt
```
---
## Process Isolation

![6](../../../out/mermaid/marp/courses/linux-fundamentals/00_intro.md/6.png)

- Each process has its own:
    - Memory space
    - File descriptors
    - Security context
    - Resource limits
