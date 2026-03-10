# Expansion: Brace and Comma
---
## Brace Expansion
- Generates arbitrary strings
- Processed BEFORE variable expansion
- Not a glob: works even if files don't exist
- Two forms: comma-separated list and sequence

```bash
echo {a,b,c}
# a b c

echo file{1,2,3}.txt
# file1.txt file2.txt file3.txt
```
---
## Brace Expansion: Comma Lists

```bash
# Prefix and suffix are attached to each item
echo {cat,dog,bird}
# cat dog bird

echo /home/{alice,bob,charlie}/.bashrc
# /home/alice/.bashrc /home/bob/.bashrc /home/charlie/.bashrc

# Create multiple directories at once
mkdir -p project/{src,lib,bin,doc,test}

# Copy to a backup
cp config.yml{,.backup}
# expands to: cp config.yml config.yml.backup

# Rename pattern
mv file.{txt,md}
# expands to: mv file.txt file.md
```
---
## Brace Expansion: Sequences

```bash
# Integer sequences
echo {1..10}
# 1 2 3 4 5 6 7 8 9 10

# With step
echo {0..20..5}
# 0 5 10 15 20

# Letter sequences
echo {a..z}
# a b c d e f g h i j k l m n o p q r s t u v w x y z

echo {A..Z}
# A B C D E F G H I J K L M N O P Q R S T U V W X Y Z

# Zero-padded numbers
echo {001..010}
# 001 002 003 004 005 006 007 008 009 010
```
---
## Nesting Brace Expansions

```bash
# Braces can be nested
echo {a,b{1,2},c}
# a b1 b2 c

# Create a directory tree
mkdir -p project/{src/{main,test},lib,doc}
# Creates:
# project/src/main
# project/src/test
# project/lib
# project/doc

# Multiple levels
echo {a,b}{1,2}{x,y}
# a1x a1y a2x a2y b1x b1y b2x b2y
```
---
## Brace Expansion is NOT Globbing

```bash
# Key differences:
# 1. Brace expansion generates strings, not matched files
echo {a,b,c}.txt    # ALWAYS produces: a.txt b.txt c.txt
echo *.txt           # only produces existing .txt files

# 2. Brace expansion happens BEFORE variable expansion
x=3
echo {1..$x}        # {1..3} literally! NOT 1 2 3
# Use seq or eval instead:
seq 1 "$x"
eval echo "{1..$x}"

# 3. Braces with a single element are not expanded
echo {solo}          # {solo}
echo {a,b}           # a b
```
---
## Practical Brace Expansion Examples

```bash
# Compare two git branches
diff <(git show main:file.c) <(git show develop:file.c)

# Create date-stamped directories
mkdir logs-{2024,2025}-{01..12}

# Download numbered files
wget https://example.com/page{1..50}.html

# Bulk operations
chmod 644 *.{jpg,png,gif,bmp}

# Create multiple test files
touch test_{pass,fail}_{01..05}.log
```
---
## Tilde Expansion

```bash
# ~ expands to the home directory
echo ~
# /home/mark

# ~user expands to that user's home
echo ~root
# /root

# ~+ is the current directory (same as $PWD)
echo ~+

# ~- is the previous directory (same as $OLDPWD)
echo ~-

# Tilde must be at the start, unquoted
echo "~"      # literal tilde
echo ~/file   # /home/mark/file
```
---
## `$PATH` and Brace Expansion Together

```bash
# Quickly add multiple directories to PATH
export PATH="${HOME}/{bin,scripts,tools}:${PATH}"
# Wait... this does NOT work!
# Brace expansion happens before variable expansion

# Correct approach: spell it out
export PATH="${HOME}/bin:${HOME}/scripts:${HOME}/tools:${PATH}"
```
---
## Expansion Order Summary
```text
1. Brace expansion:       {a,b,c}
2. Tilde expansion:       ~
3. Parameter expansion:   $var, ${var}
4. Command substitution:  $(cmd)
5. Arithmetic expansion:  $((expr))
6. Process substitution:  <(cmd), >(cmd)
7. Word splitting:        (on unquoted results)
8. Filename expansion:    *.txt, file?.log
9. Quote removal:         removes unneeded quotes
```
---
## Day 1 Summary
- The shell is the interface between you and the kernel
- `bash` is the standard scripting shell on `Linux`
- The shell parses commands through multiple expansion stages
- Return codes indicate success (0) or failure (non-zero)
- Variables can be shell-local or environment (exported)
- Redirection controls where input/output flows
- Error handling requires explicit attention (`set -euo pipefail`)
- Globbing matches existing files; brace expansion generates strings
