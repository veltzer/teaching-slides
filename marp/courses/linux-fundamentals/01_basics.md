# UNIX Basics
## Getting Started with the Command Line
---
## Logging In and Out

```mermaid
sequenceDiagram
    participant User
    participant Login
    participant Shell
    participant System
    
    User->>Login: Enter username
    Login->>User: Request password
    User->>Login: Enter password
    Login->>System: Verify credentials
    System->>Shell: Start user session
    Note over Shell: User's environment loaded
    Shell->>User: Display prompt
```

Common commands:
```bash
logout    # Clean shell exit
exit      # Exit current shell
Ctrl+D    # EOF (same as exit)
```

---
## Password Management

```bash
# Change your password
passwd

# View password status
passwd -S

# Force password change on next login (root only)
chage -d 0 username
```

```mermaid
graph TD
    A[passwd command] --> B[/etc/passwd]
    A --> C[/etc/shadow]
    B --> D[User Info]
    C --> E[Encrypted Password]
    style A fill:#f96,stroke:#333
    style B fill:#bbf,stroke:#333
    style C fill:#fdd,stroke:#333
```
---
## Command Structure

Basic syntax:

```bash
command [options] [arguments]
```

Examples:

```bash
ls -l /home
cp -r source_dir destination_dir
find /home -name "*.txt"
```

```mermaid
graph LR
    A[Command] --> B[Options]
    A --> C[Arguments]
    B --> D[Short -a]
    B --> E[Long --all]
    C --> F[Files]
    C --> G[Directories]
    style A fill:#f96,stroke:#333
```
---
## Simple Commands

Common basic commands:

```bash
# Display current directory
pwd

# List files
ls

# Create directory
mkdir new_directory

# Remove file
rm file.txt

# Copy file
cp source.txt destination.txt

# Move/rename file
mv old.txt new.txt
```

---
## Getting Help

```bash
# View manual page
man ls

# Short command help
ls --help

# Search manual pages
apropos "list files"

# View command type
type ls
```

```mermaid
graph TD
    A[Help System] --> B[man pages]
    A --> C[--help option]
    A --> D[apropos]
    A --> E[info pages]
    B --> F[Section 1: Commands]
    B --> G[Section 2: System calls]
    B --> H[Section 5: File formats]
    style A fill:#f96,stroke:#333
```
---
## Control Characters

```mermaid
graph TB
    A[Control Characters] --> B[Ctrl+C]
    A --> C[Ctrl+Z]
    A --> D[Ctrl+D]
    A --> E[Ctrl+L]
    A --> F[Ctrl+R]
    B --> G[Interrupt]
    C --> H[Suspend]
    D --> I[EOF]
    E --> J[Clear screen]
    F --> K[Search history]
    style A fill:#f96,stroke:#333
```

Common control characters:
| Key      | Function          |
|----------|-------------------|
| Ctrl+C   | Interrupt        |
| Ctrl+Z   | Suspend          |
| Ctrl+D   | End of input     |
| Ctrl+L   | Clear screen     |
| Ctrl+R   | Search history   |

---
## Command Line Editing

```mermaid
sequenceDiagram
    participant User
    participant Shell
    participant History
    
    User->>Shell: Type command
    Shell->>User: Display feedback
    User->>Shell: ↑ (Up arrow)
    Shell->>History: Fetch previous
    History->>Shell: Return command
    Shell->>User: Display command
```

Navigation shortcuts:
```bash
Ctrl+A  # Move to beginning of line
Ctrl+E  # Move to end of line
Ctrl+U  # Clear line before cursor
Ctrl+K  # Clear line after cursor
Alt+B   # Move back one word
Alt+F   # Move forward one word
```

---
## Command Examples in Practice

Let's combine what we've learned:
```bash
# Create and navigate directories
mkdir -p projects/unix_basics
cd projects/unix_basics

# Create and edit files
touch notes.txt
echo "UNIX Basics" > notes.txt

# View file contents
cat notes.txt
less notes.txt

# Copy and move files
cp notes.txt backup_notes.txt
mv backup_notes.txt ../notes_backup.txt
```
---
## Common Mistakes and Solutions

```mermaid
graph TD
    A[Common Issues] --> B[Permission denied]
    A --> C[Command not found]
    A --> D[File not found]
    B --> E[Use sudo]
    C --> F[Check PATH]
    D --> G[Check spelling]
    style A fill:#f96,stroke:#333
```

Solutions:
```bash
# Permission denied
sudo command

# Command not found
which command
echo $PATH

# File not found
ls -la
pwd
```
---
## Practice Exercise

Try these commands:
```bash
# 1. Create a new directory
mkdir practice

# 2. Create some files
touch practice/file{1..5}.txt

# 3. List files with details
ls -l practice/

# 4. Copy files to backup
cp -r practice practice_backup

# 5. Clean up
rm -rf practice practice_backup
```
