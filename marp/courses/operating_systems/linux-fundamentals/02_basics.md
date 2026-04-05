# UNIX Basics
## Getting Started with the Command Line
---
## Logging In and Out

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="15" width="140" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="120" y="35" text-anchor="middle" font-size="11" font-weight="bold">User Terminal</text>
  <text x="120" y="50" text-anchor="middle" font-size="10">username + password</text>
  <rect x="410" y="15" width="140" height="45" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="480" y="35" text-anchor="middle" font-size="11" font-weight="bold">Login Shell</text>
  <text x="480" y="50" text-anchor="middle" font-size="10">/bin/bash</text>
  <line x1="190" y1="37" x2="410" y2="37" stroke="#333" stroke-width="2" marker-end="url(#arr_login)"/>
  <text x="300" y="30" text-anchor="middle" font-size="10">login credentials</text>
  <rect x="140" y="80" width="320" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="102" text-anchor="middle" font-size="10">/etc/passwd validates user, loads shell and HOME</text>
  <rect x="100" y="130" width="130" height="55" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="165" y="150" text-anchor="middle" font-size="10" font-weight="bold">Exit Methods</text>
  <text x="165" y="170" text-anchor="middle" font-size="10">logout | exit | Ctrl+D</text>
  <rect x="370" y="130" width="180" height="55" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="460" y="150" text-anchor="middle" font-size="10" font-weight="bold">Session Types</text>
  <text x="460" y="170" text-anchor="middle" font-size="10">console / SSH / GUI terminal</text>
  <defs>
    <marker id="arr_login" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
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
  <rect x="50" y="15" width="150" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="125" y="40" text-anchor="middle" font-size="11" font-weight="bold">/etc/passwd</text>
  <rect x="225" y="15" width="150" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="40" text-anchor="middle" font-size="11" font-weight="bold">/etc/shadow</text>
  <rect x="400" y="15" width="150" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="475" y="40" text-anchor="middle" font-size="11" font-weight="bold">PAM</text>
  <line x1="200" y1="35" x2="225" y2="35" stroke="#333" stroke-width="2" marker-end="url(#arr_pw)"/>
  <line x1="375" y1="35" x2="400" y2="35" stroke="#333" stroke-width="2" marker-end="url(#arr_pw)"/>
  <rect x="100" y="75" width="400" height="50" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="95" text-anchor="middle" font-size="10" font-weight="bold">Password Storage Flow</text>
  <text x="300" y="113" text-anchor="middle" font-size="10">passwd cmd -> PAM -> hash in /etc/shadow -> chage policy</text>
  <rect x="150" y="145" width="300" height="40" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="162" text-anchor="middle" font-size="10">Hash algorithms: $6$ (SHA-512), $5$ (SHA-256)</text>
  <text x="300" y="178" text-anchor="middle" font-size="10" fill="#666">passwd -S shows password status</text>
  <defs>
    <marker id="arr_pw" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
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
  <rect x="50" y="15" width="500" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="11" font-weight="bold">Command Anatomy</text>
  <text x="300" y="55" text-anchor="middle" font-family="monospace" font-size="13">ls    -l    -a    /home</text>
  <line x1="165" y1="65" x2="165" y2="90" stroke="#e3f2fd" stroke-width="2"/>
  <line x1="240" y1="65" x2="240" y2="120" stroke="#f3e5f5" stroke-width="2"/>
  <line x1="300" y1="65" x2="300" y2="120" stroke="#f3e5f5" stroke-width="2"/>
  <line x1="395" y1="65" x2="395" y2="150" stroke="#e8f5e9" stroke-width="2"/>
  <rect x="100" y="90" width="130" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="165" y="107" text-anchor="middle" font-size="10">command name</text>
  <rect x="175" y="120" width="190" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="270" y="137" text-anchor="middle" font-size="10">options (flags/switches)</text>
  <rect x="320" y="150" width="150" height="25" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="395" y="167" text-anchor="middle" font-size="10">argument (operand)</text>
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
  <rect x="50" y="10" width="150" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="125" y="30" text-anchor="middle" font-size="11" font-weight="bold">man command</text>
  <text x="125" y="48" text-anchor="middle" font-size="10">Detailed manual</text>
  <rect x="225" y="10" width="150" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="11" font-weight="bold">--help flag</text>
  <text x="300" y="48" text-anchor="middle" font-size="10">Quick summary</text>
  <rect x="400" y="10" width="150" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="475" y="30" text-anchor="middle" font-size="11" font-weight="bold">apropos keyword</text>
  <text x="475" y="48" text-anchor="middle" font-size="10">Search man pages</text>
  <rect x="50" y="80" width="500" height="45" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="97" text-anchor="middle" font-size="10" font-weight="bold">Man Page Sections</text>
  <text x="300" y="115" text-anchor="middle" font-size="10">1:Commands  2:Syscalls  3:Library  4:Devices  5:Formats  7:Misc  8:Admin</text>
  <rect x="100" y="140" width="400" height="45" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="157" text-anchor="middle" font-size="10" font-weight="bold">Other Help: info, whatis, type</text>
  <text x="300" y="175" text-anchor="middle" font-size="10">info coreutils | whatis ls | type cd (builtin vs external)</text>
</svg>

---
## Control Characters

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="10" width="100" height="40" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="35" text-anchor="middle" font-size="11" font-weight="bold">Ctrl+C</text>
  <rect x="170" y="10" width="100" height="40" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="220" y="35" text-anchor="middle" font-size="11" font-weight="bold">Ctrl+Z</text>
  <rect x="290" y="10" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="340" y="35" text-anchor="middle" font-size="11" font-weight="bold">Ctrl+D</text>
  <rect x="410" y="10" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="460" y="35" text-anchor="middle" font-size="11" font-weight="bold">Ctrl+L</text>
  <text x="100" y="70" text-anchor="middle" font-size="10">SIGINT</text>
  <text x="100" y="83" text-anchor="middle" font-size="10" fill="#666">Kill process</text>
  <text x="220" y="70" text-anchor="middle" font-size="10">SIGTSTP</text>
  <text x="220" y="83" text-anchor="middle" font-size="10" fill="#666">Suspend</text>
  <text x="340" y="70" text-anchor="middle" font-size="10">EOF</text>
  <text x="340" y="83" text-anchor="middle" font-size="10" fill="#666">End input</text>
  <text x="460" y="70" text-anchor="middle" font-size="10">Clear</text>
  <text x="460" y="83" text-anchor="middle" font-size="10" fill="#666">Redraw screen</text>
  <rect x="50" y="100" width="460" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="280" y="118" text-anchor="middle" font-size="10" font-weight="bold">Signal Flow: Keyboard -> Terminal Driver -> Kernel -> Process</text>
  <text x="280" y="133" text-anchor="middle" font-size="10" fill="#666">Ctrl+R: reverse history search  |  Ctrl+\: SIGQUIT (core dump)</text>
  <rect x="50" y="155" width="230" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="165" y="177" text-anchor="middle" font-size="10">stty -a : view terminal settings</text>
  <rect x="300" y="155" width="210" height="35" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="405" y="177" text-anchor="middle" font-size="10">stty intr ^X : remap Ctrl+X</text>
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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="10" width="500" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="33" text-anchor="middle" font-family="monospace" font-size="12">$ echo "hello world" | grep "hello"_</text>
  <text x="50" y="67" font-size="10" fill="#666">Cursor movement:</text>
  <rect x="50" y="75" width="80" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="90" y="94" text-anchor="middle" font-size="10">Ctrl+A</text>
  <rect x="140" y="75" width="80" height="28" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="180" y="94" text-anchor="middle" font-size="10">Ctrl+E</text>
  <rect x="230" y="75" width="80" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="270" y="94" text-anchor="middle" font-size="10">Alt+B</text>
  <rect x="320" y="75" width="80" height="28" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="94" text-anchor="middle" font-size="10">Alt+F</text>
  <text x="50" y="125" font-size="10" fill="#666">Editing:</text>
  <rect x="50" y="133" width="80" height="28" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="90" y="152" text-anchor="middle" font-size="10">Ctrl+U</text>
  <rect x="140" y="133" width="80" height="28" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="180" y="152" text-anchor="middle" font-size="10">Ctrl+K</text>
  <rect x="230" y="133" width="80" height="28" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="270" y="152" text-anchor="middle" font-size="10">Ctrl+W</text>
  <rect x="320" y="133" width="80" height="28" fill="#ffebee" stroke="#333" stroke-width="1" rx="3"/>
  <text x="360" y="152" text-anchor="middle" font-size="10">Ctrl+Y</text>
  <text x="90" y="176" text-anchor="middle" font-size="9" fill="#666">start of line</text>
  <text x="180" y="176" text-anchor="middle" font-size="9" fill="#666">end of line</text>
  <text x="270" y="176" text-anchor="middle" font-size="9" fill="#666">back word</text>
  <text x="360" y="176" text-anchor="middle" font-size="9" fill="#666">fwd word</text>
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
  <rect x="50" y="10" width="160" height="55" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="130" y="30" text-anchor="middle" font-size="10" font-weight="bold">Permission denied</text>
  <text x="130" y="50" text-anchor="middle" font-size="10" fill="#666">sudo command</text>
  <rect x="220" y="10" width="160" height="55" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="30" text-anchor="middle" font-size="10" font-weight="bold">Command not found</text>
  <text x="300" y="50" text-anchor="middle" font-size="10" fill="#666">check $PATH</text>
  <rect x="390" y="10" width="160" height="55" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="470" y="30" text-anchor="middle" font-size="10" font-weight="bold">File not found</text>
  <text x="470" y="50" text-anchor="middle" font-size="10" fill="#666">check pwd, ls -la</text>
  <rect x="50" y="80" width="500" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="100" text-anchor="middle" font-size="11" font-weight="bold">Debugging Approach</text>
  <text x="300" y="118" text-anchor="middle" font-size="10">1. Read the error  2. Check path/perms  3. Use which/type  4. Check man page</text>
  <rect x="50" y="145" width="500" height="40" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="162" text-anchor="middle" font-size="10">Tip: use Tab completion to avoid typos, up-arrow for history</text>
  <text x="300" y="178" text-anchor="middle" font-size="10" fill="#666">echo $? shows exit code of last command (0=success)</text>
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
