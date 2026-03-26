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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_00_intro)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_00_intro)"/>
  <defs>
    <marker id="arrowd1_00_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---
## The Process Tree

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_00_intro)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_00_intro)"/>
  <defs>
    <marker id="arrowd2_00_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_00_intro)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_00_intro)"/>
  <defs>
    <marker id="arrowd4_00_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_00_intro)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_00_intro)"/>
  <defs>
    <marker id="arrowd5_00_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
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
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_00_intro)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_00_intro)"/>
  <defs>
    <marker id="arrowd6_00_intro" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

- Each process has its own:
    - Memory space
    - File descriptors
    - Security context
    - Resource limits
