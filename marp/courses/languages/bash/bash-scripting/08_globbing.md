---
tags:
  - languages:bash
  - practices:scripting
  - infrastructure:linux
  - practices:automation
level: intermediate
category: language
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---
# Globbing

---

## Glob Pattern Overview

![Glob Pattern Overview](svg/courses/languages/bash/bash-scripting/08_globbing/glob_pattern_overview.svg)

---
## What is Globbing?
- Pattern matching for filenames
- Performed by the **shell**, not by commands
- Happens before the command sees its arguments
- Also called "pathname expansion" or "filename generation"

```bash
# The shell expands *.txt BEFORE echo sees it
echo *.txt
# echo receives: file1.txt file2.txt file3.txt
```

---
## The Asterisk `*`

```bash
# * matches zero or more characters (except /)
ls *.txt          # all .txt files
ls file*          # files starting with "file"
ls *data*         # files containing "data"
ls *              # all non-hidden files

# * does NOT match hidden files (starting with .)
ls *              # skips .bashrc, .profile, etc.
ls .*             # only hidden files (plus . and ..)
ls .* *           # all files, hidden and non-hidden
```

---
## The Question Mark `?`

```bash
# ? matches exactly one character
ls file?.txt      # file1.txt, fileA.txt, but not file10.txt
ls ???            # all three-character filenames
ls ?.?            # a.b, x.y, etc.

# Combine with *
ls file?.*        # file1.txt, fileA.md, etc.
```

---
## Character Classes `[...]`

```bash
# Match any single character in the set
ls file[123].txt        # file1.txt, file2.txt, file3.txt
ls file[abc].txt        # filea.txt, fileb.txt, filec.txt

# Ranges
ls file[0-9].txt        # file0.txt through file9.txt
ls file[a-z].txt        # filea.txt through filez.txt
ls file[A-Z].txt        # fileA.txt through fileZ.txt
ls file[a-zA-Z].txt     # any single letter

# Multiple ranges
ls file[0-9a-f].txt     # hexadecimal single digit
```

---
## Negation `[!...]` and `[^...]`

```bash
# Match any character NOT in the set
ls file[!0-9].txt       # files NOT ending in a digit
ls file[^abc].txt       # files NOT ending in a, b, or c

# Both ! and ^ work as negation
ls [!.]*                # non-hidden files
ls [^.]*                # same thing

# POSIX specifies !, bash also accepts ^
```

---
## POSIX Character Classes

```bash
# Named classes inside [: :]
ls file[[:digit:]].txt     # file0.txt ... file9.txt
ls file[[:alpha:]].txt     # filea.txt ... fileZ.txt
ls file[[:alnum:]].txt     # digits and letters
ls [[:upper:]]*            # files starting with uppercase

# Available classes:
# [:alpha:] [:digit:] [:alnum:] [:space:]
# [:upper:] [:lower:] [:punct:] [:print:]
# [:cntrl:] [:graph:] [:xdigit:]

# Note: double brackets!
ls [[:digit:]]    # RIGHT
ls [:digit:]       # WRONG (matches :, d, i, g, t)
```

---
## When Globs Don't Match

```bash
# By default, if no files match, the pattern is kept literally
echo /nonexistent/*.xyz
# prints: /nonexistent/*.xyz

# This can cause bugs:
for f in /empty_dir/*; do
    echo "Processing: $f"
done
# prints: Processing: /empty_dir/*

# Fix with nullglob:
shopt -s nullglob
echo /nonexistent/*.xyz
# prints nothing (pattern expands to empty)

# Or use failglob to cause an error:
shopt -s failglob
echo /nonexistent/*.xyz
# bash: no match: /nonexistent/*.xyz
```

---
## The `dotglob` Option

```bash
# By default, * does not match hidden files
ls *           # skips .bashrc, .profile

# Enable dotglob to include hidden files
shopt -s dotglob
ls *           # now includes .bashrc, .profile
               # but still skips . and ..

# Turn it off
shopt -u dotglob
```

---
## Extended Globbing

```bash
# Enable extended globbing
shopt -s extglob

# ?(pattern) - zero or one occurrence
ls file?(s).txt          # file.txt, files.txt

# *(pattern) - zero or more occurrences
ls file*(s).txt          # file.txt, files.txt, filess.txt

# +(pattern) - one or more occurrences
ls file+(s).txt          # files.txt, filess.txt (not file.txt)

# @(pattern) - exactly one occurrence
ls file@(1|2|3).txt      # file1.txt, file2.txt, file3.txt

# !(pattern) - anything except the pattern
ls !(*.txt)               # all files except .txt files
```

---
## Globbing vs Regular Expressions
| Glob | Regex | Meaning |
|------|-------|---------|
| `*` | `.*` | Any characters |
| `?` | `.` | One character |
| `[abc]` | `[abc]` | Character class |
| `[!abc]` | `[^abc]` | Negated class |
| `{a,b}` | `(a\|b)` | Alternatives |

```bash
# IMPORTANT: do not confuse them!
# ls uses globs:
ls *.txt        # correct
ls .*\.txt      # WRONG! (regex syntax)
```

---
## Globbing Safety

```bash
# Problem: what if a filename starts with -
touch -- -rf
ls *
# This passes -rf as a flag to ls!

# Solution: use -- to signal end of options
rm -- -rf       # removes file named "-rf"

# Or use ./ prefix
rm ./-rf

# General rule: when glob results feed into commands,
# consider filenames with special characters
```
