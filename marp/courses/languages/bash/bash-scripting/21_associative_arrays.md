# Using Associative Arrays
---
## Declaring Associative Arrays

```bash
# MUST declare with -A (unlike indexed arrays)
declare -A config

# Without declare -A, it's an indexed array!
# This is a common mistake

# Declare and initialize
declare -A colors=(
    [red]="#FF0000"
    [green]="#00FF00"
    [blue]="#0000FF"
)
```
---
## Adding Key-Value Pairs

```bash
declare -A user

# Add pairs one at a time
user[name]="Alice"
user[age]="30"
user[email]="alice@example.com"
user[role]="admin"

# Add multiple pairs at once
declare -A settings=(
    [host]="localhost"
    [port]="8080"
    [debug]="true"
    [log_level]="info"
)

# Overwrite existing key
settings[debug]="false"
```
---
## Accessing Values

```bash
declare -A capitals=(
    [France]="Paris"
    [Germany]="Berlin"
    [Japan]="Tokyo"
)

# Access by key
echo "${capitals[France]}"    # Paris

# Default value if key missing
echo "${capitals[Spain]:-Unknown}"    # Unknown

# Store in variable
city="${capitals[Japan]}"
echo "Japan's capital: $city"     # Tokyo
```
---
## Iterating Over Associative Arrays

```bash
declare -A config=(
    [host]="localhost"
    [port]="5432"
    [db]="myapp"
    [user]="admin"
)

# Iterate over keys
for key in "${!config[@]}"; do
    echo "$key = ${config[$key]}"
done

# Iterate over values only
for value in "${config[@]}"; do
    echo "Value: $value"
done

# NOTE: order is NOT guaranteed!
# Associative arrays are hash tables
```
---
## Checking Key Existence

```bash
declare -A data=([x]=1 [y]=2 [z]="")

# Method 1: -v test (bash 4.2+)
if [[ -v data[x] ]]; then
    echo "x exists"
fi

if [[ ! -v data[w] ]]; then
    echo "w does not exist"
fi

# Method 2: check key in list
if [[ " ${!data[*]} " == *" x "* ]]; then
    echo "x exists"
fi

# Important: empty value is different from missing key
[[ -v data[z] ]] && echo "z exists (but is empty)"
```
---
## Removing Keys

```bash
declare -A fruits=(
    [apple]=1
    [banana]=2
    [cherry]=3
)

# Remove a key
unset 'fruits[banana]'
echo "${!fruits[@]}"    # apple cherry

# Clear all entries
declare -A fruits=()
# or
unset fruits
declare -A fruits
```
---
## Size and Membership

```bash
declare -A registry=(
    [service1]="running"
    [service2]="stopped"
    [service3]="running"
)

# Number of entries
echo "Count: ${#registry[@]}"    # 3

# Count running services
running=0
for status in "${registry[@]}"; do
    [[ "$status" == "running" ]] && ((running++))
done
echo "Running: $running"
```
---
## Associative Arrays from Files

```bash
# Load a key=value config file
declare -A config

while IFS='=' read -r key value; do
    # Skip comments and empty lines
    [[ "$key" =~ ^[[:space:]]*# ]] && continue
    [[ -z "$key" ]] && continue
    # Trim whitespace
    key="${key## }"
    key="${key%% }"
    value="${value## }"
    value="${value%% }"
    config["$key"]="$value"
done < config.ini

# Access loaded config
echo "Database: ${config[db_host]}:${config[db_port]}"
```
---
## Associative Array as Counter

```bash
#!/bin/bash
declare -A word_count

# Count word frequencies
while read -r word; do
    word="${word,,}"    # lowercase
    (( word_count[$word]++ ))
done < <(tr ' ' '\n' < document.txt)

# Display results
for word in "${!word_count[@]}"; do
    printf "%-20s %d\n" "$word" "${word_count[$word]}"
done | sort -t' ' -k2 -rn | head -20
```
---
## Nested Structures (Simulated)

```bash
# bash does NOT support nested arrays
# Simulate with naming conventions

declare -A db
db[user.name]="admin"
db[user.password]="secret"
db[user.host]="localhost"
db[server.port]="8080"
db[server.workers]="4"

# Access "nested" values
echo "User: ${db[user.name]}@${db[user.host]}"
echo "Server: port ${db[server.port]}, ${db[server.workers]} workers"

# List all keys in a "namespace"
for key in "${!db[@]}"; do
    [[ $key == user.* ]] && echo "$key = ${db[$key]}"
done
```
---
## Passing Associative Arrays to Functions

```bash
# Method 1: by nameref (bash 4.3+)
print_map() {
    local -n map=$1
    for key in "${!map[@]}"; do
        echo "  $key -> ${map[$key]}"
    done
}

declare -A settings=([a]=1 [b]=2 [c]=3)
print_map settings

# Method 2: serialize and deserialize
serialize_map() {
    local -n map=$1
    for key in "${!map[@]}"; do
        echo "$key=${map[$key]}"
    done
}

deserialize_map() {
    local -n map=$1
    while IFS='=' read -r key value; do
        map[$key]="$value"
    done
}
```
---
## Practical: Simple Key-Value Store

```bash
#!/bin/bash
readonly STORE_FILE="${HOME}/.kvstore"

kv_set() {
    local key=$1 value=$2
    # Remove old entry, add new one
    grep -v "^${key}=" "$STORE_FILE" 2>/dev/null > "${STORE_FILE}.tmp" || true
    echo "${key}=${value}" >> "${STORE_FILE}.tmp"
    mv "${STORE_FILE}.tmp" "$STORE_FILE"
}

kv_get() {
    local key=$1
    grep "^${key}=" "$STORE_FILE" 2>/dev/null | cut -d= -f2-
}

kv_delete() {
    local key=$1
    grep -v "^${key}=" "$STORE_FILE" > "${STORE_FILE}.tmp" 2>/dev/null || true
    mv "${STORE_FILE}.tmp" "$STORE_FILE"
}

kv_list() {
    cat "$STORE_FILE" 2>/dev/null
}
```
