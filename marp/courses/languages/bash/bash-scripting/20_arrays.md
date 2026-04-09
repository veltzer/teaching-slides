# Using Arrays

---
## Creating Arrays

```bash
# Method 1: parentheses
fruits=("apple" "banana" "cherry")

# Method 2: assign individual elements
colors[0]="red"
colors[1]="green"
colors[2]="blue"

# Method 3: from command output
files=($(ls *.txt))      # CAUTION: breaks on spaces

# Method 4: safe from command output
mapfile -t files < <(find . -name "*.txt")

# Method 5: from a string
IFS=',' read -ra items <<< "a,b,c,d"
```

---
## Accessing Array Elements

```bash
arr=("zero" "one" "two" "three" "four")

# Single element
echo "${arr[0]}"     # zero
echo "${arr[2]}"     # two

# Last element
echo "${arr[-1]}"    # four (bash 4.3+)
echo "${arr[-2]}"    # three

# All elements
echo "${arr[@]}"     # zero one two three four

# Number of elements
echo "${#arr[@]}"    # 5

# All indices
echo "${!arr[@]}"    # 0 1 2 3 4
```

---
## `"${arr[@]}"` vs `"${arr[*]}"`

```bash
arr=("hello world" "foo bar" "baz")

# "@" preserves each element as a separate word
for item in "${arr[@]}"; do
    echo "item: [$item]"
done
# item: [hello world]
# item: [foo bar]
# item: [baz]

# "*" joins all elements into one string
for item in "${arr[*]}"; do
    echo "item: [$item]"
done
# item: [hello world foo bar baz]

# ALWAYS use "${arr[@]}" when iterating
```

---
## Adding Elements

```bash
arr=("one" "two")

# Append one element
arr+=("three")
echo "${arr[@]}"    # one two three

# Append multiple elements
arr+=("four" "five")
echo "${arr[@]}"    # one two three four five

# Insert at specific index
arr[10]="ten"
echo "${arr[@]}"    # one two three four five ten
echo "${!arr[@]}"   # 0 1 2 3 4 10 (sparse!)
echo "${#arr[@]}"   # 6

# Prepend (create new array)
arr=("zero" "${arr[@]}")
```

---
## Removing Elements

```bash
arr=("a" "b" "c" "d" "e")

# Remove by index
unset 'arr[2]'
echo "${arr[@]}"    # a b d e
echo "${!arr[@]}"   # 0 1 3 4 (index 2 is gone, NOT shifted)

# Remove last element
unset 'arr[-1]'

# Remove entire array
unset arr

# Remove by value (no built-in way)
remove_value() {
    local -n arr_ref=$1
    local value=$2
    local new_arr=()
    for item in "${arr_ref[@]}"; do
        [[ "$item" != "$value" ]] && new_arr+=("$item")
    done
    arr_ref=("${new_arr[@]}")
}
```

---
## Array Slicing

```bash
arr=("a" "b" "c" "d" "e" "f")

# Slice: ${arr[@]:offset:length}
echo "${arr[@]:1:3}"     # b c d
echo "${arr[@]:2}"       # c d e f (from index 2 to end)
echo "${arr[@]:(-2)}"    # e f (last 2 elements)

# Copy an array
copy=("${arr[@]}")

# Merge arrays
arr1=("a" "b")
arr2=("c" "d")
merged=("${arr1[@]}" "${arr2[@]}")
echo "${merged[@]}"      # a b c d
```

---
## Iterating Over Arrays

```bash
fruits=("apple" "banana" "cherry" "date")

# By value
for fruit in "${fruits[@]}"; do
    echo "Fruit: $fruit"
done

# By index
for i in "${!fruits[@]}"; do
    echo "[$i] = ${fruits[$i]}"
done

# C-style loop
for ((i = 0; i < ${#fruits[@]}; i++)); do
    echo "[$i] = ${fruits[$i]}"
done

# With index and value (bash doesn't have enumerate)
i=0
for fruit in "${fruits[@]}"; do
    echo "[$((i++))]: $fruit"
done
```

---
## Checking If an Element Exists

```bash
# No built-in way to check if a VALUE exists
# Method 1: loop
contains() {
    local value=$1
    shift
    for item in "$@"; do
        [[ "$item" == "$value" ]] && return 0
    done
    return 1
}

arr=("apple" "banana" "cherry")
if contains "banana" "${arr[@]}"; then
    echo "Found banana"
fi

# Method 2: pattern matching
if [[ " ${arr[*]} " == *" banana "* ]]; then
    echo "Found banana"
fi
# WARNING: fails if elements contain spaces
```

---
## Checking If an Index Exists

```bash
arr=("a" "b" "c")
unset 'arr[1]'    # now sparse: indices 0, 2

# Check if index is set
if [[ -v arr[1] ]]; then
    echo "arr[1] is set"
else
    echo "arr[1] is not set"    # this prints
fi

if [[ -v arr[0] ]]; then
    echo "arr[0] is set"        # this prints
fi
```

---
## Sorting Arrays

```bash
# bash has no built-in sort for arrays
# Use process substitution with sort

arr=("banana" "apple" "date" "cherry")

# Sort into new array
mapfile -t sorted < <(printf '%s\n' "${arr[@]}" | sort)
echo "${sorted[@]}"    # apple banana cherry date

# Numeric sort
nums=(42 5 100 23 7)
mapfile -t sorted < <(printf '%s\n' "${nums[@]}" | sort -n)
echo "${sorted[@]}"    # 5 7 23 42 100

# Reverse sort
mapfile -t sorted < <(printf '%s\n' "${arr[@]}" | sort -r)
echo "${sorted[@]}"    # date cherry banana apple
```

---
## Unique Elements

```bash
arr=("apple" "banana" "apple" "cherry" "banana" "date")

# Remove duplicates (sorted)
mapfile -t unique < <(printf '%s\n' "${arr[@]}" | sort -u)
echo "${unique[@]}"    # apple banana cherry date

# Remove duplicates (preserve order) using awk
mapfile -t unique < <(printf '%s\n' "${arr[@]}" | awk '!seen[$0]++')
echo "${unique[@]}"    # apple banana cherry date
```

---
## Arrays as Function Arguments

```bash
# Pass array to function
process_items() {
    local items=("$@")
    for item in "${items[@]}"; do
        echo "Processing: $item"
    done
}

my_array=("one" "two" "three")
process_items "${my_array[@]}"

# Return array from function (via nameref)
generate_list() {
    local -n result=$1
    result=("generated_a" "generated_b" "generated_c")
}

generate_list output_array
echo "${output_array[@]}"
```

---
## `mapfile` / `readarray`

```bash
# Read lines from stdin into an array
mapfile -t lines < file.txt

# readarray is an alias for mapfile
readarray -t lines < file.txt

# Options:
# -t  : strip trailing newlines
# -n N : read at most N lines
# -s N : skip first N lines
# -O N : start at index N

# Read first 10 lines
mapfile -t -n 10 lines < file.txt

# Skip header, read next 5 lines
mapfile -t -s 1 -n 5 lines < file.txt

# From a command
mapfile -t pids < <(pgrep bash)
```

---
## Practical: Stack Implementation

```bash
# Using an array as a stack
declare -a stack=()

push() { stack+=("$1"); }
pop() {
    local -n result=$1
    result="${stack[-1]}"
    unset 'stack[-1]'
}
peek() { echo "${stack[-1]}"; }
is_empty() { (( ${#stack[@]} == 0 )); }
stack_size() { echo "${#stack[@]}"; }

# Usage:
push "first"
push "second"
push "third"
echo "Top: $(peek)"         # third
echo "Size: $(stack_size)"   # 3

pop value
echo "Popped: $value"       # third
echo "Size: $(stack_size)"   # 2
```
