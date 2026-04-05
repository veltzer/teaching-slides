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

<svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="40" width="300" height="70" fill="#f0f0f0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="80" text-anchor="middle" font-size="14">Diagram</text>
</svg>

---
## Operating System Core Structure

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="10" width="500" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="12" font-weight="bold">User Space</text>
  <rect x="70" y="60" width="120" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="130" y="82" text-anchor="middle" font-size="10">Applications</text>
  <rect x="210" y="60" width="120" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="270" y="82" text-anchor="middle" font-size="10">Shell (bash)</text>
  <rect x="350" y="60" width="120" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="410" y="82" text-anchor="middle" font-size="10">Libraries (libc)</text>
  <rect x="50" y="110" width="500" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="132" text-anchor="middle" font-size="11" font-weight="bold">System Call Interface</text>
  <rect x="50" y="155" width="500" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="180" text-anchor="middle" font-size="12" font-weight="bold">Kernel (process mgmt, memory, fs, drivers)</text>
</svg>

---
## The Process Tree

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="225" y="10" width="150" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="11" font-weight="bold">init (PID 1)</text>
  <line x1="250" y1="50" x2="130" y2="80" stroke="#333" stroke-width="2"/>
  <line x1="300" y1="50" x2="300" y2="80" stroke="#333" stroke-width="2"/>
  <line x1="350" y1="50" x2="470" y2="80" stroke="#333" stroke-width="2"/>
  <rect x="60" y="80" width="140" height="35" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="130" y="102" text-anchor="middle" font-size="10">sshd (PID 200)</text>
  <rect x="230" y="80" width="140" height="35" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="102" text-anchor="middle" font-size="10">cron (PID 300)</text>
  <rect x="400" y="80" width="140" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="470" y="102" text-anchor="middle" font-size="10">nginx (PID 400)</text>
  <line x1="100" y1="115" x2="100" y2="145" stroke="#333" stroke-width="1"/>
  <line x1="160" y1="115" x2="160" y2="145" stroke="#333" stroke-width="1"/>
  <rect x="40" y="145" width="120" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="100" y="165" text-anchor="middle" font-size="10">bash (PID 501)</text>
  <rect x="180" y="145" width="120" height="30" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="240" y="165" text-anchor="middle" font-size="10">bash (PID 502)</text>
</svg>

## Why is it important
- Process management
- Resource tracking
- System organization
- Parent-child relationships

---

## Process Lifecycle

<svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="150" y="40" width="300" height="70" fill="#f0f0f0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="80" text-anchor="middle" font-size="14">Diagram</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="15" width="150" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="125" y="40" text-anchor="middle" font-size="11" font-weight="bold">User (UID)</text>
  <rect x="225" y="15" width="150" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="40" text-anchor="middle" font-size="11" font-weight="bold">Group (GID)</text>
  <rect x="400" y="15" width="150" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="475" y="40" text-anchor="middle" font-size="11" font-weight="bold">Others</text>
  <rect x="50" y="75" width="500" height="45" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="92" text-anchor="middle" font-size="11">File Permissions: r w x | r w x | r w x</text>
  <text x="300" y="110" text-anchor="middle" font-size="10" fill="#666">owner    group    others</text>
  <rect x="50" y="140" width="500" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="157" text-anchor="middle" font-size="11">Process runs with UID/GID of the user who started it</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#666">Kernel checks permissions on every file access</text>
</svg>

### Key Security Features
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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="10" width="500" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="11" font-weight="bold">Permission Check Flow</text>
  <text x="300" y="50" text-anchor="middle" font-size="10">-rwxr-xr-- 1 alice devs 4096 file.txt</text>
  <rect x="60" y="80" width="130" height="40" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="125" y="95" text-anchor="middle" font-size="10">Owner: alice</text>
  <text x="125" y="110" text-anchor="middle" font-size="10" fill="#666">rwx (7)</text>
  <rect x="235" y="80" width="130" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="95" text-anchor="middle" font-size="10">Group: devs</text>
  <text x="300" y="110" text-anchor="middle" font-size="10" fill="#666">r-x (5)</text>
  <rect x="410" y="80" width="130" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="475" y="95" text-anchor="middle" font-size="10">Others</text>
  <text x="475" y="110" text-anchor="middle" font-size="10" fill="#666">r-- (4)</text>
  <rect x="100" y="140" width="400" height="45" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="158" text-anchor="middle" font-size="10">chmod 754 file.txt   |   chown alice:devs file.txt</text>
  <text x="300" y="175" text-anchor="middle" font-size="10" fill="#666">Numeric (octal) mode   |   Change owner and group</text>
</svg>

Example permission setting:

```bash
# Setting permissions
chmod 755 file.txt  # rwxr-xr-x
chown user:group file.txt
```

---
## Process Isolation

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="100" y="10" width="180" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="190" y="30" text-anchor="middle" font-size="11" font-weight="bold">Process A (PID 100)</text>
  <text x="190" y="48" text-anchor="middle" font-size="10">Virtual Memory: 0x0000...</text>
  <rect x="320" y="10" width="180" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="410" y="30" text-anchor="middle" font-size="11" font-weight="bold">Process B (PID 200)</text>
  <text x="410" y="48" text-anchor="middle" font-size="10">Virtual Memory: 0x0000...</text>
  <rect x="100" y="75" width="400" height="30" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="95" text-anchor="middle" font-size="11">Isolated: separate memory, FDs, security context</text>
  <rect x="100" y="120" width="400" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="133" text-anchor="middle" font-size="10" font-weight="bold">Kernel enforces isolation</text>
  <text x="300" y="148" text-anchor="middle" font-size="10">MMU maps virtual addresses to physical memory</text>
  <rect x="100" y="165" width="400" height="25" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="182" text-anchor="middle" font-size="10">Physical RAM (shared by all processes via kernel)</text>
</svg>

- Each process has its own:
    - Memory space
    - File descriptors
    - Security context
    - Resource limits
