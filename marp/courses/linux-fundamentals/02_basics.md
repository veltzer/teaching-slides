# UNIX Basics
## Getting Started with the Command Line
---
## Logging In and Out

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_01_basics)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd0_01_basics)"/>
  <defs>
    <marker id="arrowd0_01_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_01_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_01_basics)"/>
  <defs>
    <marker id="arrowd1_01_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_01_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_01_basics)"/>
  <defs>
    <marker id="arrowd2_01_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_01_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_01_basics)"/>
  <defs>
    <marker id="arrowd3_01_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---
## Control Characters

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_01_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_01_basics)"/>
  <defs>
    <marker id="arrowd4_01_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_01_basics)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd5_01_basics)"/>
  <defs>
    <marker id="arrowd5_01_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="75" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="250" y="75" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <rect x="450" y="75" width="100" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="105" text-anchor="middle" font-size="12">Node 1</text>
  <text x="300" y="105" text-anchor="middle" font-size="12">Node 2</text>
  <text x="500" y="105" text-anchor="middle" font-size="12">Node 3</text>
  <line x1="150" y1="100" x2="250" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_01_basics)"/>
  <line x1="350" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_01_basics)"/>
  <defs>
    <marker id="arrowd6_01_basics" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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
