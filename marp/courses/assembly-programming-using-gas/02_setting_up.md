# Setting Up the Development Environment

---

## Essential Tools for Assembly Programming

1. GNU Assembler (GAS)
2. GNU Compiler Collection (GCC)
3. GNU Debugger (GDB)
4. Text Editor or Integrated Development Environment (IDE)

---

## Installing Tools on Linux

Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install build-essential gdb
```

Fedora/CentOS:
```bash
sudo dnf groupinstall "Development Tools"
sudo dnf install gdb
```

---

## Verifying Installation

Check GCC version:
```bash
gcc --version
```

Check GAS version:
```bash
as --version
```

Check GDB version:
```bash
gdb --version
```

---

## Text Editors for Assembly

Popular choices:
- Vim
- Emacs
- Visual Studio Code
- Sublime Text

---

## Configuring Vim for Assembly

Add to ~/.vimrc:
```vim
syntax on
set syntax=nasm
set tabstop=8
set shiftwidth=8
set autoindent
```

---

## Configuring Visual Studio Code

1. Install "x86 and x86_64 Assembly" extension
2. Configure settings.json:
```json
{
    "files.associations": {
        "*.s": "gas-x86",
        "*.asm": "nasm"
    }
}
```

---

## Creating a Basic Assembly Project

Project structure:
```
my_assembly_project/
+-- src/
|   +-- main.s
+-- Makefile
+-- README.md
```

---

## Sample Makefile

```makefile
AS = as
LD = ld

ASFLAGS = --32
LDFLAGS = -m elf_i386

SOURCES = src/main.s
OBJECTS = $(SOURCES:.s=.o)
EXECUTABLE = my_program

all: $(SOURCES) $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
    $(LD) $(LDFLAGS) $(OBJECTS) -o $@

.s.o:
    $(AS) $(ASFLAGS) $< -o $@

clean:
    rm -f $(OBJECTS) $(EXECUTABLE)
```

---

## Basic Assembly Program

src/main.s:
```gas
.section .text
.globl _start

_start:
    movl $1, %eax    # sys_exit system call
    movl $0, %ebx    # exit status 0
    int $0x80        # interrupt to invoke system call
```

---

## Compiling and Linking

```bash
# Assemble
as --32 -o main.o main.s

# Link
ld -m elf_i386 -o my_program main.o

# Run
./my_program

# Check exit status
echo $?
```

---

## Debugging with GDB

1. Compile with debugging symbols:
   ```bash
   as --32 -g -o main.o main.s
   ld -m elf_i386 -o my_program main.o
   ```

2. Start GDB:
   ```bash
   gdb ./my_program
   ```

3. Basic GDB commands:
   - `break _start`
   - `run`
   - `next`
   - `step`
   - `info registers`
