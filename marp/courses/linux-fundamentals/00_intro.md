---
marp: true
theme: default
paginate: true
header: "Introduction to UNIX"
footer: "Linux Fundamentals Course"
style: |
  .columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
  }
---

# Introduction to UNIX
## Understanding the Fundamentals

---

# What is UNIX?

- Multi-user operating system
- Built in the 1970s at AT&T Bell Labs
- Key characteristics:
  - Modularity
  - Simple tools that do one thing well
  - Text-based configuration
  - Everything is a file philosophy

---

# History of UNIX

```mermaid
timeline
    title UNIX Evolution
    1969 : UNIX Development Begins
    1971 : First Edition
    1973 : Rewritten in C
    1977 : BSD Unix
    1983 : System V
    1991 : Linux Created
    1992 : First Linux Distribution
```

---

# Operating System Core Structure

```mermaid
graph TD
    A[User Applications] --> B[Shell]
    B --> C[System Calls]
    C --> D[Kernel]
    D --> E[Hardware]
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#ddf,stroke:#333
    style D fill:#fdd,stroke:#333
    style E fill:#dfd,stroke:#333
```

---

# The Process Tree

```mermaid
graph TD
    A[init/systemd PID 1] --> B[System Services]
    A --> C[User Sessions]
    B --> D[Network]
    B --> E[Logging]
    C --> F[Shell]
    F --> G[User Programs]
    style A fill:#f96,stroke:#333
```

## Why is it important?
- Process management
- Resource tracking
- System organization
- Parent-child relationships

---

# Process Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Created
    Created --> Running
    Running --> Waiting
    Waiting --> Running
    Running --> Terminated
    Terminated --> Zombie
    Zombie --> [*]
```

## Zombie Processes
- Terminated but not yet cleaned up
- Parent must read exit status
- Adopted by init if parent dies

---

# System Calls

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

# Basic Security Model

```mermaid
graph LR
    A[Process] -->|restricted by| B[File Permissions]
    A -->|confined to| C[Memory Space]
    A -->|controlled by| D[User Privileges]
    style A fill:#f9f,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#ddf,stroke:#333
    style D fill:#fdd,stroke:#333
```

## Key Security Features:
- File system permissions
- Process isolation
- User/group-based access control

---

# The Root User

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

# File System Security

```mermaid
graph TD
    A[File Access Control] --> B[Owner]
    A --> C[Group]
    A --> D[Others]
    B --> E[Read]
    B --> F[Write]
    B --> G[Execute]
    C --> H[Read]
    C --> I[Write]
    C --> J[Execute]
    D --> K[Read]
    D --> L[Write]
    D --> M[Execute]
```

Example permission setting:
```bash
# Setting permissions
chmod 755 file.txt  # rwxr-xr-x
chown user:group file.txt
```

---

# Process Isolation

```mermaid
graph TD
    subgraph "Process A"
    A1[Memory Space A]
    A2[File Descriptors A]
    end
    subgraph "Process B"
    B1[Memory Space B]
    B2[File Descriptors B]
    end
    C[Kernel] --> A1
    C --> B1
    style C fill:#f96,stroke:#333
```

- Each process has its own:
  - Memory space
  - File descriptors
  - Security context
  - Resource limits
