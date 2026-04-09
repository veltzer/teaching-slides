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

---

## Need for Transactions

![need_for_transactions](svg/courses/databases/redis/05_transactions/need_for_transactions.svg)

---

## What are Redis Transactions?

Redis transactions allow executing multiple commands as a single atomic operation:

- All commands execute sequentially
- No interruption by other clients
- All-or-nothing execution*
- Isolated from other clients

\* With some caveats we'll discuss

---

## What are Redis Transactions?

![what_are_redis_transactions](svg/courses/databases/redis/05_transactions/what_are_redis_transactions.svg)

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

![redis_transaction_example](svg/courses/databases/redis/05_transactions/redis_transaction_example.svg)

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

![error_handling_in_transactions](svg/courses/databases/redis/05_transactions/error_handling_in_transactions.svg)

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

![watch_example](svg/courses/databases/redis/05_transactions/watch_example.svg)

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

---

## Script Replication and Clustering

![script_replication_and_clustering](svg/courses/databases/redis/05_transactions/script_replication_and_clustering.svg)

---

## Script Replication Requirements

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

![lua_script_vs_multi_exec](svg/courses/databases/redis/05_transactions/lua_script_vs_multi_exec.svg)

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
