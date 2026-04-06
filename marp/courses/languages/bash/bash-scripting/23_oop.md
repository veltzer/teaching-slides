# Object Oriented Programming with Associative Arrays
---
## OOP in `bash`? Really?
- `bash` is not an OOP language
- But we can simulate some OOP patterns
- Associative arrays can act as "objects"
- Functions can act as "methods"
- Useful for complex scripts that need structure
- Not recommended for production — consider `Python` instead
---
## A Simple Object

```bash
# Create an "object" using an associative array
declare -A person=(
    [name]="Alice"
    [age]=30
    [email]="alice@example.com"
)

# "Method" that operates on the object
person_greet() {
    local -n self=$1
    echo "Hi, I'm ${self[name]}, age ${self[age]}"
}

person_greet person
# Hi, I'm Alice, age 30
```
---
## Constructor Pattern

```bash
# "Constructor" function
new_person() {
    local -n obj=$1
    obj=()    # clear the array
    obj[name]="${2:?Name required}"
    obj[age]="${3:?Age required}"
    obj[email]="${4:-}"
    obj[_type]="person"    # pseudo-type tag
}

# Create instances
declare -A alice
new_person alice "Alice" 30 "alice@example.com"

declare -A bob
new_person bob "Bob" 25

echo "${alice[name]} is ${alice[age]}"
echo "${bob[name]} is ${bob[age]}"
```
---
## Methods as Functions

```bash
# Define methods that take object as first argument
person_to_string() {
    local -n self=$1
    echo "${self[name]} (${self[age]}) <${self[email]:-n/a}>"
}

person_birthday() {
    local -n self=$1
    self[age]=$((self[age] + 1))
    echo "Happy birthday ${self[name]}! Now ${self[age]}"
}

person_set_email() {
    local -n self=$1
    self[email]="$2"
}

# Usage:
person_to_string alice    # Alice (30) <alice@example.com>
person_birthday alice     # Happy birthday Alice! Now 31
```
---
## Dispatch Table Pattern

```bash
# Map method names to functions
declare -A PERSON_METHODS=(
    [greet]="person_greet"
    [to_string]="person_to_string"
    [birthday]="person_birthday"
)

# Dispatcher
call() {
    local obj_name=$1
    local method=$2
    shift 2
    local -n obj=$obj_name
    local type="${obj[_type]}"
    local methods_var="${type^^}_METHODS"
    local -n methods=$methods_var
    local func="${methods[$method]}"
    [[ -z "$func" ]] && { echo "Unknown method: $method" >&2; return 1; }
    "$func" "$obj_name" "$@"
}

# Usage:
call alice greet
call alice birthday
```
---
## Simulating Collections

```bash
# A list of objects using naming convention
declare -a person_list=()

add_person() {
    local name=$1 age=$2 email=$3
    local idx=${#person_list[@]}
    local var="person_${idx}"

    declare -gA "$var"
    local -n obj=$var
    obj[name]="$name"
    obj[age]="$age"
    obj[email]="$email"
    obj[_type]="person"

    person_list+=("$var")
}

list_persons() {
    for var_name in "${person_list[@]}"; do
        person_to_string "$var_name"
    done
}

add_person "Alice" 30 "alice@ex.com"
add_person "Bob" 25 "bob@ex.com"
list_persons
```
---
## Practical Example: Config Manager

```bash
#!/bin/bash

new_config() {
    local -n cfg=$1
    cfg=()
    cfg[_file]="$2"
}

config_load() {
    local -n cfg=$1
    local file="${cfg[_file]}"
    while IFS='=' read -r key value; do
        [[ "$key" =~ ^[[:space:]]*#|^$ ]] && continue
        key="${key// /}"
        cfg[$key]="$value"
    done < "$file"
}

config_get() {
    local -n cfg=$1
    echo "${cfg[$2]:-$3}"    # key, default
}

config_set() {
    local -n cfg=$1
    cfg[$2]="$3"
}

config_save() {
    local -n cfg=$1
    local file="${cfg[_file]}"
    : > "$file"    # truncate
    for key in "${!cfg[@]}"; do
        [[ "$key" == _* ]] && continue
        echo "$key=${cfg[$key]}" >> "$file"
    done
}
```
---
## Limitations of OOP in `bash`

```text
Limitation                   Alternative
---------------------------------------------------
No real inheritance          Use composition
No private/public            Prefix private with _
No polymorphism              Use dispatch tables
No garbage collection        Manual unset
No type checking             Add runtime checks
Performance overhead         Keep it simple
Naming conflicts             Use prefixes/namespaces

Bottom line: if your script needs OOP,
consider switching to Python or another language.
```
