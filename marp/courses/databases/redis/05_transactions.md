# Redis Transactions and Scripting

---

## Redis Atomicity

Redis commands are atomic by default:
- Single commands execute without interruption
- No partial execution of a command
- Guarantees consistency for individual operations

Example:
```bash
INCR counter  # Atomic - will never result in a partial increment
HSET user:123 visits 10 name "John"  # Atomic - all fields are set or none
```

---

## Need for Transactions

Single atomic commands aren't always enough:

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd0_04_transactions)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd0_04_transactions)"/>
  <defs>
    <marker id="arrowd0_04_transactions" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## What are Redis Transactions?

Redis transactions allow executing multiple commands as a single atomic operation:

- All commands execute sequentially
- No interruption by other clients
- All-or-nothing execution*
- Isolated from other clients

\* With some caveats we'll discuss

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="30" width="120" height="45" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="57" text-anchor="middle" font-size="11" font-weight="bold">MULTI</text>
  <rect x="30" y="85" width="120" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="90" y="107" text-anchor="middle" font-size="10">CMD 1 (queued)</text>
  <rect x="30" y="125" width="120" height="35" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="90" y="147" text-anchor="middle" font-size="10">CMD 2 (queued)</text>
  <line x1="160" y1="100" x2="220" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_04_transactions)"/>
  <rect x="230" y="60" width="140" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="85" text-anchor="middle" font-size="11" font-weight="bold">EXEC</text>
  <text x="300" y="105" text-anchor="middle" font-size="10">Execute all</text>
  <text x="300" y="120" text-anchor="middle" font-size="10">atomically</text>
  <line x1="380" y1="100" x2="440" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_04_transactions)"/>
  <rect x="450" y="70" width="120" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="95" text-anchor="middle" font-size="11" font-weight="bold">Results</text>
  <text x="510" y="115" text-anchor="middle" font-size="10">[OK, OK, ...]</text>
  <defs>
    <marker id="arrowd1_04_transactions" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Redis Transaction Commands

```bash
# Start a transaction
MULTI

# Queue commands
COMMAND1 arg1 arg2
COMMAND2 arg1 arg2
# ... more commands

# Execute all queued commands
EXEC

# Discard all queued commands
DISCARD
```

---

## Redis Transaction Example

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_04_transactions)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd2_04_transactions)"/>
  <defs>
    <marker id="arrowd2_04_transactions" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Redis Transaction Limitations

Unlike traditional RDBMS transactions:

1. **No rollback on error**:
    - Syntax errors abort the transaction
    - Runtime errors don't stop execution

1. **No nested transactions**:
    - Cannot start a new MULTI inside a transaction

1. **Limited isolation**:
    - No read isolation during transaction
    - Values may change between MULTI and EXEC

---

## Error Handling in Transactions

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd3_04_transactions)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd3_04_transactions)"/>
  <defs>
    <marker id="arrowd3_04_transactions" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Optimistic Locking with WATCH

WATCH provides optimistic locking:
- Monitor keys for changes
- Abort transaction if watched keys change
- Use between WATCH and EXEC

```bash
WATCH key [key ...]   # Watch keys for changes
MULTI                 # Start transaction
# ... commands
EXEC                  # Execute or abort if watched keys changed
UNWATCH               # Cancel watching (also happens after EXEC/DISCARD)
```

---

## WATCH Example

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <line x1="150" y1="50" x2="150" y2="200" stroke="#333" stroke-width="2"/>
  <line x1="450" y1="50" x2="450" y2="200" stroke="#333" stroke-width="2"/>
  <rect x="100" y="30" width="100" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="400" y="30" width="100" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="150" y="55" text-anchor="middle" font-size="12">Actor A</text>
  <text x="450" y="55" text-anchor="middle" font-size="12">Actor B</text>
  <line x1="150" y1="100" x2="450" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_04_transactions)"/>
  <line x1="450" y1="150" x2="150" y2="150" stroke="#333" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#arrowd4_04_transactions)"/>
  <defs>
    <marker id="arrowd4_04_transactions" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Implementing Optimistic Locking

```python
def transfer_funds(redis, from_acct, to_acct, amount):
    while True:
        try:
            # Watch both accounts
            redis.watch(f"account:{from_acct}", f"account:{to_acct}")

            # Get current balances
            from_balance = int(redis.get(f"account:{from_acct}") or 0)
            to_balance = int(redis.get(f"account:{to_acct}") or 0)

            # Validate sufficient funds
            if from_balance < amount:
                redis.unwatch()
                return False, "Insufficient funds"

            # Start transaction
            pipeline = redis.pipeline(transaction=True)
            pipeline.decrby(f"account:{from_acct}", amount)
            pipeline.incrby(f"account:{to_acct}", amount)

            # Execute and check for success
            result = pipeline.execute()
            return True, "Transfer successful"

        except redis.WatchError:
            # Another client modified the watched keys
            continue  # Retry the operation
```

---

## Common Transaction Use Cases

1. **Counter increment with validation**:
    - Ensure counter doesn't exceed limit

1. **Atomic updates to multiple related keys**:
    - Update user data across multiple data structures

1. **Managing inventory**:
    - Check stock and update atomically

1. **Financial operations**:
    - Transfer funds between accounts

1. **Leader election**:
    - Acquire lock with expiration

---

## Redis Scripts: Introduction to Lua

Lua is a lightweight scripting language:

- Embedded in Redis since version 2.6
- Simple syntax, easy to learn
- Preferred for Redis scripting
- Scripts are atomic like transactions
- More powerful than MULTI/EXEC transactions

```lua
-- Basic Lua script example
local value = redis.call('GET', KEYS[1])
if value == false then
    return redis.call('SET', KEYS[1], ARGV[1])
else
    return value
end
```

---

## Why Use Lua Scripts?

Benefits over transactions:

1. **Reduced network overhead**:
    - Single round-trip vs multiple commands

1. **More complex logic**:
    - Conditionals, loops, variables

1. **True atomicity**:
    - Executes as a single atomic operation

1. **Better performance**:
    - Less client-server communication

1. **Reusability**:
    - Scripts can be stored and called by name

---

## EVAL Command

Execute Lua scripts with EVAL:

```bash
EVAL script numkeys key [key ...] arg [arg ...]
```

- `script`: Lua script source code
- `numkeys`: Number of keys passed to the script
- `key [key ...]`: Keys accessed by the script
- `arg [arg ...]`: Additional arguments

Example:
```bash
EVAL "return redis.call('SET', KEYS[1], ARGV[1])" 1 mykey myvalue
```

---

## Redis and Lua: Special Variables

Inside Lua scripts:

- `KEYS`: Table (array) containing keys (indexed from 1)
- `ARGV`: Table containing additional arguments
- `redis.call()`: Execute Redis command and return result
- `redis.pcall()`: Execute command, capture errors as return values

```lua
-- Increment counter only if less than max
local current = redis.call('GET', KEYS[1])
if current == false or tonumber(current) < tonumber(ARGV[1]) then
    return redis.call('INCR', KEYS[1])
else
    return current
end
```

---

## EVALSHA Command

For efficiency with repeated scripts:

```bash
EVALSHA sha1 numkeys key [key ...] arg [arg ...]
```

- Redis caches script by SHA1 hash
- Avoids re-sending the script body
- Useful for large scripts or frequent calls

```bash
# Store script hash
SCRIPT LOAD "return redis.call('GET', KEYS[1])"
# Returns: "a42059b356c875f0717db19a51f6aaca9ae659ea"

# Execute by hash
EVALSHA a42059b356c875f0717db19a51f6aaca9ae659ea 1 mykey
```

---

## Script Management Commands

```bash
# Load script into cache without executing
SCRIPT LOAD script

# Check if scripts exist in cache
SCRIPT EXISTS sha1 [sha1 ...]

# Remove all scripts from cache
SCRIPT FLUSH

# Kill a currently executing script
SCRIPT KILL
```

---

## Basic Script Examples

**Atomic counter with limit**:
```lua
-- KEYS[1]: counter key
-- ARGV[1]: maximum value
local current = redis.call('GET', KEYS[1]) or 0
if tonumber(current) < tonumber(ARGV[1]) then
    return redis.call('INCR', KEYS[1])
else
    return current
end
```

**Get and delete in one operation**:
```lua
-- KEYS[1]: key to get and delete
local value = redis.call('GET', KEYS[1])
redis.call('DEL', KEYS[1])
return value
```

---

## Script Example: Rate Limiter

```lua
-- KEYS[1]: rate limiter key (e.g., "rate:ip:1.2.3.4")
-- ARGV[1]: maximum requests
-- ARGV[2]: window size in seconds

local key = KEYS[1]
local max_requests = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local current_time = redis.call('TIME')[1] -- Current UNIX timestamp

-- Clean old requests
redis.call('ZREMRANGEBYSCORE', key, 0, current_time - window)

-- Count requests in current window
local count = redis.call('ZCARD', key)

-- If under limit, add new request and return count
if count < max_requests then
    redis.call('ZADD', key, current_time, current_time .. '-' .. math.random())
    redis.call('EXPIRE', key, window)
    return count + 1
else
    -- Over limit
    return 0
end
```

---

## Script Example: Atomic List Rotation

```lua
-- KEYS[1]: list key
-- ARGV[1]: maximum list length

local list_key = KEYS[1]
local max_length = tonumber(ARGV[1])

-- Add new item to the beginning
redis.call('LPUSH', list_key, ARGV[2])

-- Trim list to max length
local current_length = redis.call('LLEN', list_key)
if current_length > max_length then
    -- Return the items that were trimmed off
    local removed = redis.call('LRANGE', list_key, max_length, -1)
    redis.call('LTRIM', list_key, 0, max_length - 1)
    return removed
else
    return {}
end
```

---

## Script Security Considerations

Scripts execute with high privileges:

1. **Script timeout**:
    - Default maximum execution time is 5 seconds
    - `lua-time-limit` configuration option
    - Long-running scripts block Redis

1. **Resource consumption**:
    - Scripts can consume significant CPU
    - Use `SCRIPT KILL` for runaway scripts
    - Only works if script hasn't modified data

1. **Avoid non-deterministic operations**:
    - No random functions except `math.random()`
    - No system calls or file access
    - Helps with replication and clustering

---

## Script Replication and Clustering

Scripts work differently in distributed Redis:

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="25" width="160" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="50" text-anchor="middle" font-size="11" font-weight="bold">Master Node</text>
  <text x="110" y="70" text-anchor="middle" font-size="10">Executes script</text>
  <line x1="200" y1="55" x2="260" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_04_transactions)"/>
  <text x="230" y="48" text-anchor="middle" font-size="9">replicates</text>
  <rect x="270" y="15" width="130" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="335" y="40" text-anchor="middle" font-size="10">Replica 1</text>
  <rect x="270" y="65" width="130" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="335" y="90" text-anchor="middle" font-size="10">Replica 2</text>
  <rect x="30" y="120" width="560" height="60" fill="#fff3e0" stroke="#333" stroke-width="1" rx="5"/>
  <text x="310" y="142" text-anchor="middle" font-size="11" font-weight="bold">Deterministic Scripts Required</text>
  <text x="310" y="162" text-anchor="middle" font-size="10">Same script must produce same results on all nodes (no random, no TIME)</text>
  <defs>
    <marker id="arrowd5_04_transactions" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

- Scripts must be deterministic for replication
- In cluster mode, all keys must be in same slot
- Use `EVAL_RO` for read-only scripts (Redis 7.0+)

---

## Scripting Design Patterns

1. **Command augmentation**:
    - Add features to existing commands
    - Example: SET with unique check

1. **Multi-key atomic operations**:
    - Operate on multiple keys atomically
    - Example: Move element between sets

1. **Extended data structures**:
    - Implement custom data structures
    - Example: Priority queue with scores

1. **Business logic validation**:
    - Validate operations server-side
    - Example: Check balance before transfer

---

## Lua Script vs. MULTI/EXEC

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="20" width="170" height="75" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="42" text-anchor="middle" font-size="11" font-weight="bold">MULTI/EXEC</text>
  <text x="105" y="58" text-anchor="middle" font-size="10">Simple queuing</text>
  <text x="105" y="73" text-anchor="middle" font-size="10">No conditionals</text>
  <text x="105" y="88" text-anchor="middle" font-size="10">Multiple round-trips</text>
  <text x="300" y="60" text-anchor="middle" font-size="12" font-weight="bold">vs</text>
  <rect x="410" y="20" width="170" height="75" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="42" text-anchor="middle" font-size="11" font-weight="bold">Lua Script</text>
  <text x="495" y="58" text-anchor="middle" font-size="10">Complex logic</text>
  <text x="495" y="73" text-anchor="middle" font-size="10">Conditionals/loops</text>
  <text x="495" y="88" text-anchor="middle" font-size="10">Single round-trip</text>
  <rect x="120" y="120" width="360" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="142" text-anchor="middle" font-size="11" font-weight="bold">Both are Atomic</text>
  <text x="300" y="162" text-anchor="middle" font-size="10">No other client can interrupt execution</text>
</svg>

---

## Lua Script vs. MULTI/EXEC: When to Use Each

**Use MULTI/EXEC when**:
- Simple operations (few commands)
- No conditional logic needed
- Optimistic locking with WATCH is sufficient
- Client already has all needed data

**Use Lua scripts when**:
- Complex logic with conditionals
- Need to make decisions based on data values
- Multiple operations on the same keys
- Performance is critical (reduce round trips)
- Implementing custom commands or data structures

---

## Debugging Redis Scripts

Since Redis has no debugging tools for Lua:

1. **Incremental development**:
    - Start with simple scripts
    - Add complexity gradually

1. **Local testing**:
    - Test with Lua interpreter first
    - Mock Redis commands for testing

1. **Use return values**:
    - Return intermediate values for debugging
    - Remove in production

1. **Error handling**:
    - Use `pcall()` to catch errors
    - Return descriptive error messages

---

## Script Error Handling

```lua
-- Example with error handling
local function process_data()
    local value = redis.call('GET', KEYS[1])
    -- Some processing that might fail
    return value
end

-- Call the function with error handling
local ok, result = pcall(process_data)
if not ok then
    -- Handle the error
    return {err = "Error: " .. result}
else
    return result
end
```

---

## Function Commands (Redis 7.0+)

Redis 7.0 introduced function commands:

```bash
# Load a library of functions
FUNCTION LOAD '
#!lua name=mylib
redis.register_function("myfunc", function(keys, args)
    return redis.call("GET", keys[1])
end)
'

# Call a function
FCALL myfunc 1 mykey arg1 arg2

# List loaded functions
FUNCTION LIST
```

Benefits:
- Better organization of scripts
- Proper namespacing
- Improved script management

---

## Advanced Script: Distributed Lock

```lua
-- KEYS[1]: lock name
-- ARGV[1]: lock value (unique identifier)
-- ARGV[2]: lock TTL in milliseconds

-- Try to acquire lock
local acquired = redis.call('SET', KEYS[1], ARGV[1], 'NX', 'PX', ARGV[2])

if acquired then
    return 1  -- Lock acquired
else
    -- Check if we already own the lock
    if redis.call('GET', KEYS[1]) == ARGV[1] then
        -- Extend the lock TTL
        redis.call('PEXPIRE', KEYS[1], ARGV[2])
        return 1  -- Lock extended
    else
        return 0  -- Lock not acquired
    end
end
```

---

## Advanced Script: Releasing a Distributed Lock

```lua
-- KEYS[1]: lock name
-- ARGV[1]: lock value (unique identifier)

-- Get the current lock value
local current_value = redis.call('GET', KEYS[1])

-- Check if we own the lock before releasing
if current_value == ARGV[1] then
    redis.call('DEL', KEYS[1])
    return 1  -- Lock released
else
    -- We don't own the lock
    return 0  -- Could not release
end
```

---

## Advanced Script: Leaderboard with Time Decay

```lua
-- KEYS[1]: leaderboard key
-- ARGV[1]: member ID
-- ARGV[2]: score increment
-- ARGV[3]: decay factor (0-1)
-- ARGV[4]: current time

-- Apply decay to all scores
local members = redis.call('ZRANGE', KEYS[1], 0, -1, 'WITHSCORES')
for i = 1, #members, 2 do
    local member = members[i]
    local score = tonumber(members[i+1])

    -- Skip current member as we'll update it separately
    if member ~= ARGV[1] then
        local time_diff = tonumber(ARGV[4]) - redis.call('HGET', KEYS[1]..':last_update', member)
        local decay = math.pow(tonumber(ARGV[3]), time_diff / 86400) -- Decay per day
        redis.call('ZADD', KEYS[1], score * decay, member)
    end

    -- Update last update time
    redis.call('HSET', KEYS[1]..':last_update', member, ARGV[4])
end

-- Update the current member's score
local current_score = redis.call('ZSCORE', KEYS[1], ARGV[1]) or 0
redis.call('ZADD', KEYS[1], current_score + tonumber(ARGV[2]), ARGV[1])
redis.call('HSET', KEYS[1]..':last_update', ARGV[1], ARGV[4])

return redis.call('ZREVRANGE', KEYS[1], 0, 9, 'WITHSCORES') -- Top 10
```

---

## Lab: Redis Transactions and Scripting

1. **Exercise 1**: Implement a bank transfer using MULTI/EXEC/WATCH
1. **Exercise 2**: Create a script for a rate limiter
1. **Exercise 3**: Implement an atomic counter with a maximum value
1. **Exercise 4**: Build a distributed lock mechanism
1. **Exercise 5**: Create a time-based leaderboard
1. **Exercise 6**: Implement a unique ID generator
1. **Exercise 7**: Build a delayed job queue with priority

---

## Summary

- Redis transactions (MULTI/EXEC) provide atomic execution
- WATCH enables optimistic locking for consistency
- Lua scripting offers more powerful transaction capabilities
- Scripts execute atomically and reduce network overhead
- Use transactions for simple operations
- Use scripts for complex logic and performance
- Redis 7.0+ offers improved Function commands
- Both features enable building complex, atomic operations

Next chapter: Redis Persistence
