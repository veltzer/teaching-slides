# Async Python

## Overview
- Understanding generators and iterators
- Coroutines and how they work
- Asynchronous programming concepts
- Python's asyncio library
- Alternative async frameworks
- Best practices for async code

---

## What are Generators?

## Generators Fundamentals
- Special type of iterator
- Created with functions using `yield`
- Generate values on-demand
- Maintain internal state between calls
- Memory efficient for large sequences

```python
# A simple generator function
def count_up_to(max):
    count = 1
    while count <= max:
        yield count
        count += 1

# Using the generator
counter = count_up_to(5)
print(next(counter))  # 1
print(next(counter))  # 2
print(next(counter))  # 3
print(next(counter))  # 4
print(next(counter))  # 5
# next(counter) would raise StopIteration
```

---

## What are Generators?

## How Generators Work
- `yield` pauses function execution
- Function state is saved
- Execution resumes from where it left off when next() is called
- Automatic implementation of iterator protocol
- Each call returns the next yielded value

```python
def demonstrate_state():
    x = 1
    print(f"First value: {x}")
    yield x

    x += 1
    print(f"Second value: {x}")
    yield x

    x += 1
    print(f"Third value: {x}")
    yield x

    print("Generator exhausted")

gen = demonstrate_state()
val1 = next(gen)  # Prints "First value: 1", returns 1
val2 = next(gen)  # Prints "Second value: 2", returns 2
val3 = next(gen)  # Prints "Third value: 3", returns 3
# next(gen) would print "Generator exhausted" and raise StopIteration
```

---

## What are Generators?

## Generator Expressions
- Concise syntax similar to list comprehensions
- Creates a generator object instead of a list
- Memory efficient for large datasets
- Lazy evaluation (values calculated on-demand)
- Uses parentheses instead of square brackets

```python
# List comprehension (creates entire list in memory)
squares_list = [x**2 for x in range(1000000)]

# Generator expression (creates values on demand)
squares_gen = (x**2 for x in range(1000000))

# Memory usage comparison
import sys
print(f"List size: {sys.getsizeof(squares_list)} bytes")
print(f"Generator size: {sys.getsizeof(squares_gen)} bytes")

# Using the generator
for i, square in enumerate(squares_gen):
    if i < 5:
        print(square)
    else:
        break
```

---

## What are Generators?

## Generator Benefits
- Memory efficiency for large datasets
- Lazy evaluation (compute values as needed)
- Representing infinite sequences
- Expressing data pipelines
- Building data processing chains
- Simplifying stateful processes

```python
# Processing a large file with generators
def read_large_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()

def grep(pattern, lines):
    for line in lines:
        if pattern in line:
            yield line

# Process 10GB log file without loading into memory
log_lines = read_large_file("huge_log.txt")
error_lines = grep("ERROR", log_lines)
warning_lines = grep("WARNING", log_lines)

# Process only the first 10 errors and warnings
for i, line in enumerate(error_lines):
    if i >= 10:
        break
    print(f"Error {i+1}: {line}")

for i, line in enumerate(warning_lines):
    if i >= 10:
        break
    print(f"Warning {i+1}: {line}")
```

---

## Writing Your Own Generators

## Basic Generator Functions
- Use `yield` statement to return values
- Function body runs on each call to `next()`
- Execution continues after the last `yield` point
- Returns multiple values over time
- Automatically handles iteration protocol

```python
def fibonacci(limit):
    """Generate Fibonacci numbers up to limit."""
    a, b = 0, 1
    while a < limit:
        yield a
        a, b = b, a + b

# Using the generator
for num in fibonacci(100):
    print(num, end=" ")
# Output: 0 1 1 2 3 5 8 13 21 34 55 89

# Can also use next() directly
fib = fibonacci(10)
print(next(fib))  # 0
print(next(fib))  # 1
print(next(fib))  # 1
```

---

## Writing Your Own Generators

## Generator Methods: send()
- Send values back into the generator
- Value becomes the result of the yield expression
- Must call next() first, or send(None)
- Enables two-way communication
- Basis for coroutine development

```python
def counter():
    count = 0
    while True:
        # yield is an expression that can receive a value
        increment = yield count
        # If a value is sent, use it; otherwise default to 1
        count += increment if increment is not None else 1

# Using send with the generator
c = counter()
print(next(c))    # 0 (must call next first)
print(c.send(2))  # 2 (count is now 2)
print(c.send(3))  # 5 (count is now 5)
print(next(c))    # 6 (using default increment of 1)
print(c.send(10)) # 16 (count is now 16)
```

---

## Writing Your Own Generators

## Generator Methods: throw() and close()
- `throw()`: Raise an exception inside the generator
- `close()`: Terminate generator execution
- Exception handling within generators
- Proper cleanup for generator resources
- Complete control over generator lifecycle

```python
def resource_generator():
    try:
        print("Resource opened")
        for i in range(3):
            try:
                value = yield i
                print(f"Got value: {value}")
            except ValueError:
                print("Caught ValueError, continuing")
        print("Generator completed normally")
    finally:
        print("Resource closed")

gen = resource_generator()
print(next(gen))           # Resource opened, returns 0
print(gen.send("hello"))   # Got value: hello, returns 1
print(gen.throw(ValueError))  # Caught ValueError, continuing, returns 2
gen.close()                # Resource closed
```

---

## Writing Your Own Generators

## Yielding From Other Generators
- `yield from`: Delegate to another generator
- Forward values both ways
- Connect generators into pipelines
- Simplify nested yields
- Properly handles return values from subgenerators

```python
def subgenerator():
    yield 1
    yield 2
    return "Finished"  # Return value for yield from

def delegating_generator():
    # Yield from delegates to subgenerator
    result = yield from subgenerator()
    print(f"Subgenerator returned: {result}")
    yield 3
    yield 4

# Using the combined generator
g = delegating_generator()
print(next(g))  # 1 (from subgenerator)
print(next(g))  # 2 (from subgenerator)
print(next(g))  # Prints "Subgenerator returned: Finished", returns 3
print(next(g))  # 4
```

---

## Writing Your Own Generators

## Advanced Generator Patterns
- Pipeline processing
- Data transformation chains
- Producer-consumer pipelines
- Interleaving sequences
- Hierarchical sequence generation

```python
def integers():
    """Generate infinite integers."""
    i = 0
    while True:
        yield i
        i += 1

def take(n, iterable):
    """Take the first n items from iterable."""
    for i, item in enumerate(iterable):
        if i < n:
            yield item
        else:
            break

def map_generator(func, iterable):
    """Apply func to each item in iterable."""
    for item in iterable:
        yield func(item)

# Compose generators into a pipeline
numbers = take(10, integers())
squares = map_generator(lambda x: x**2, numbers)
for square in squares:
    print(square)
```

---

## What are Coroutines?

## From Generators to Coroutines
- Generators: produce data (yield values out)
- Coroutines: consume data (receive values in)
- Evolution of `yield` from statement to expression
- Basis for asynchronous programming
- Two-way communication channel

```python
# Generator (produces values)
def count_generator():
    for i in range(3):
        yield i  # Produces values

# Coroutine (consumes values)
def echo_coroutine():
    while True:
        value = yield  # Consumes values
        print(f"Got: {value}")

# Using both
gen = count_generator()
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2

coro = echo_coroutine()
next(coro)  # Prime the coroutine
coro.send("Hello")  # Got: Hello
coro.send(42)       # Got: 42
```

---

## What are Coroutines?

## Coroutines vs. Generators
- Generators: primarily yield values out
- Coroutines: primarily receive values in
- Generators: iterate over a sequence
- Coroutines: provide a processing step
- Both use `yield` but with different purposes
- Coroutines need to be "primed" with next()

```python
# Pure generator (only yields values)
def pure_generator():
    yield 1
    yield 2
    yield 3

# Pure coroutine (only receives values)
def pure_coroutine():
    while True:
        value = yield
        print(f"Received: {value}")

# Hybrid (both yields and receives values)
def hybrid():
    value = 0
    while True:
        received = yield value
        if received is not None:
            value = received
        else:
            value += 1
```

---

## Writing Your Own Coroutines

## Basic Coroutine Pattern
- Call next() or send(None) to prime coroutine
- Send values with send() method
- Use `yield` as an expression to receive values
- Often wrapped in infinite loop
- Initial yield is typically None

```python
def basic_coroutine():
    print("Coroutine started")

    while True:
        # Receive value from send()
        received = yield
        print(f"Received: {received}")

# Using the coroutine
coro = basic_coroutine()
# Prime the coroutine
next(coro)  # Coroutine started
# Send values
coro.send("Hello")  # Received: Hello
coro.send(42)       # Received: 42
coro.close()
```

---

## Writing Your Own Coroutines

## Coroutine for Data Processing
- Initialize with next() or send(None)
- Process incoming data
- Maintain state between sends
- Close when done

```python
def running_average():
    """Compute running average of values."""
    total = 0
    count = 0
    average = 0

    # First yield is None, returns the first average
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

# Using the coroutine
avg = running_average()
next(avg)  # Prime the coroutine, returns 0
print(avg.send(10))  # 10.0
print(avg.send(20))  # 15.0
print(avg.send(30))  # 20.0
```

---

## Writing Your Own Coroutines

## Coroutine Priming Decorator
- Initialize coroutine automatically
- Avoid explicit calls to next()
- Ensure proper coroutine startup
- Common pattern in coroutine libraries

```python
def coroutine(func):
    """Decorator to prime a coroutine."""
    @functools.wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer

@coroutine
def filtered_data(pattern):
    """Filter data based on pattern."""
    while True:
        data = yield
        if pattern in data:
            print(f"Found pattern in: {data}")

# No need to call next() first
filter_coroutine = filtered_data("error")
filter_coroutine.send("normal message")     # No output
filter_coroutine.send("error in system")    # Found pattern in: error in system
```

---

## Writing Your Own Coroutines

## Coroutine Pipelines
- Connect coroutines in series
- Create data processing pipelines
- First coroutine feeds second, etc.
- Direction of data flow is clear
- Modular, reusable components

```python
@coroutine
def grep(pattern, target):
    """Filter lines containing pattern and send to target."""
    while True:
        line = yield
        if pattern in line:
            target.send(line)

@coroutine
def printer():
    """Print lines received."""
    while True:
        line = yield
        print(line)

# Create pipeline
output = printer()
filter_error = grep("ERROR", output)
filter_warning = grep("WARNING", output)

# Send data through pipeline
for line in log_file:
    filter_error.send(line)
    filter_warning.send(line)
```

---

## Writing Your Own Coroutines

## Coroutine Exception Handling
- Handle exceptions in the coroutine
- Use throw() to inject exceptions
- Important for proper resource cleanup
- Control coroutine execution flow
- Recover from error conditions

```python
@coroutine
def safe_coroutine():
    """Coroutine with exception handling."""
    try:
        while True:
            try:
                value = yield
                print(f"Processing: {value}")
            except ValueError as e:
                print(f"ValueError handled: {e}")
    finally:
        print("Coroutine closing, cleanup complete")

coro = safe_coroutine()
coro.send("normal data")     # Processing: normal data
coro.throw(ValueError, "Bad input")  # ValueError handled: Bad input
coro.send("more data")       # Processing: more data
coro.close()                 # Coroutine closing, cleanup complete
```

---

## What is Asynchronous Programming?

## Understanding Async Programming
- Non-blocking execution model
- Cooperative multitasking
- Handle many operations concurrently
- Maximize I/O efficiency
- Different from parallelism (multi-threading/processing)

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="280" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <!-- Synchronous -->
  <text x="10" y="20" font-size="14" font-weight="bold" fill="#222">Synchronous (Blocking):</text>
  <rect x="10"  y="30" width="150" height="36" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="85"  y="53" font-size="13" fill="#222" text-anchor="middle">Start Task A</text>
  <line x1="85" y1="66" x2="85" y2="72" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="10"  y="74" width="150" height="36" fill="#ffccbc" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="85"  y="97" font-size="13" fill="#222" text-anchor="middle">Wait for A ⏳</text>
  <line x1="85" y1="110" x2="85" y2="116" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="10"  y="118" width="150" height="36" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="85"  y="141" font-size="13" fill="#222" text-anchor="middle">Start Task B</text>
  <line x1="85" y1="154" x2="85" y2="160" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="10"  y="162" width="150" height="36" fill="#ffccbc" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="85"  y="185" font-size="13" fill="#222" text-anchor="middle">Wait for B ⏳</text>
  <text x="10"  y="218" font-size="12" fill="#c62828" font-weight="bold">Total: Time A + Time B</text>
  <!-- Asynchronous -->
  <text x="350" y="20" font-size="14" font-weight="bold" fill="#222">Asynchronous (Non-blocking):</text>
  <rect x="350" y="30" width="150" height="36" fill="#e3f2fd" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="425" y="53" font-size="13" fill="#222" text-anchor="middle">Start Task A</text>
  <line x1="425" y1="66" x2="425" y2="72" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="350" y="74" width="150" height="36" fill="#e8f5e9" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="425" y="97" font-size="13" fill="#222" text-anchor="middle">Start Task B</text>
  <line x1="425" y1="110" x2="425" y2="116" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="350" y="118" width="150" height="36" fill="#fff3e0" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="425" y="141" font-size="13" fill="#222" text-anchor="middle">React on complete</text>
  <text x="350" y="180" font-size="12" fill="#2e7d32" font-weight="bold">Total: Max(Time A, Time B)</text>
  <!-- Divider -->
  <line x1="330" y1="10" x2="330" y2="230" stroke="#ccc" stroke-width="1" stroke-dasharray="4,4"/>
</svg>

---

## What is Asynchronous Programming?

## When to Use Async
- I/O-bound operations
    - Network requests
    - File operations
    - Database queries
- High-concurrency applications
- User interfaces with background operations
- Event-driven systems
- Not ideal for CPU-bound tasks

```misc
Good Async Use Cases:
- Web servers handling many connections
- API clients making multiple requests
- Web scrapers and crawlers
- Chat applications
- Real-time dashboards
- Database connection pools

Less Suitable:
- Intensive data processing
- Mathematical computations
- Image/video processing
- Machine learning algorithms
```

---

## What is Asynchronous Programming?

## Async vs. Multi-threading vs. Multi-processing
- Async: Single thread, cooperative task switching
- Threading: Multiple threads, preemptive multitasking
- Multiprocessing: Multiple processes, true parallelism

| Characteristic | Async | Threading | Multiprocessing |
|---------------|-------|-----------|-----------------|
| Concurrency | Yes | Yes | Yes |
| Parallelism | No | Limited by GIL | Yes |
| Switching | Cooperative | Preemptive | Process-based |
| Memory | Shared | Shared | Separate |
| Complexity | Medium | High | High |
| Best for | I/O-bound tasks | Mixed workloads | CPU-bound tasks |
| Communication | Direct | Locks, queues | Pipes, queues |
| Overhead | Low | Medium | High |

---

## What is Asynchronous Programming?

## The Python Async Landscape
- Initial approaches: callbacks, generators
- Python 3.4: asyncio library introduced
- Python 3.5: async/await syntax
- Python 3.6+: Improved async features
- Ecosystem: asyncio, trio, curio, twisted, tornado

```misc
Timeline of Python Async Evolution:
- Pre-3.4: Generator-based coroutines, third-party libraries
- Python 3.4: asyncio introduced with @asyncio.coroutine
- Python 3.5: async/await syntax (PEP 492)
- Python 3.6: Asynchronous generators, comprehensions
- Python 3.7: Better performance, context variables
- Python 3.8: Asyncio REPL, improved debugging
- Python 3.9: Improved type hints for coroutines
- Python 3.10: Better asyncio task cancellation
```

---

## The Python asyncio Module

## Introduction to asyncio
- Standard library for asynchronous programming
- Event loop driven architecture
- Coroutines with async/await syntax
- Tasks, Futures, and other primitives
- Built-in protocols and transports
- Tools for synchronization

```python
import asyncio

async def hello_world():
    print("Hello")
    await asyncio.sleep(1)  # Non-blocking sleep
    print("World")

# Run the coroutine in an event loop
asyncio.run(hello_world())
```

---

## The Python asyncio Module

## Async and Await Syntax
- `async def`: Define a coroutine function
- `await`: Pause execution until awaitable completes
- Awaitables: coroutines, tasks, futures
- Only valid inside async functions
- Replaced generator-based coroutines

```python
import asyncio

async def fetch_data():
    print("Fetching data...")
    await asyncio.sleep(2)  # Simulating network delay
    return {"data": "Here's your data"}

async def process_data():
    print("Starting data processing")
    data = await fetch_data()  # Await the coroutine
    print(f"Processing {data}")
    await asyncio.sleep(1)
    print("Processing complete")
    return "Processed result"

# Run everything
asyncio.run(process_data())
```

---

## The Python asyncio Module

## Running Coroutines
- asyncio.run(): Main entry point (Python 3.7+)
- Create and get event loop
- Submit coroutines to run
- Handle completion and exceptions
- Clean up after execution

```python
import asyncio

# Python 3.7+ approach
async def main():
    result1 = await task1()
    result2 = await task2()
    return result1, result2

asyncio.run(main())

# Pre-3.7 approach
loop = asyncio.get_event_loop()
try:
    results = loop.run_until_complete(main())
finally:
    loop.close()
```

---

## The Python asyncio Module

## Concurrent Execution with gather()
- Run multiple coroutines concurrently
- Collect results in order
- Single awaitable for multiple operations
- Much more efficient than sequential execution
- Fundamental for async performance benefits

```python
import asyncio
import time

async def fetch(url):
    print(f"Fetching {url}")
    await asyncio.sleep(1)  # Simulate network delay
    return f"Result from {url}"

async def concurrent_example():
    # Start time
    start = time.time()

    # Run concurrently and collect results
    urls = ['url1', 'url2', 'url3', 'url4']
    results = await asyncio.gather(
        *[fetch(url) for url in urls]
    )

    # Print results and timing
    print(f"Results: {results}")
    print(f"Took {time.time() - start:.2f} seconds")  # ~1 second

# Sequential would take ~4 seconds
asyncio.run(concurrent_example())
```

---

## The Python asyncio Module

## Working with Tasks
- Tasks wrap coroutines
- Run concurrently in the event loop
- Can be created, cancelled, and monitored
- More control than gather()
- Allow background execution

```python
import asyncio

async def background_task(name):
    try:
        for i in range(5):
            print(f"Task {name}: step {i}")
            await asyncio.sleep(0.5)
        return f"Task {name} completed"
    except asyncio.CancelledError:
        print(f"Task {name} was cancelled")
        raise

async def main():
    # Create tasks
    task1 = asyncio.create_task(background_task("A"))
    task2 = asyncio.create_task(background_task("B"))

    # Let tasks run for 2 seconds
    await asyncio.sleep(2)

    # Cancel task2
    task2.cancel()

    # Wait for task results, handling cancellations
    try:
        result1 = await task1
        print(f"Result 1: {result1}")
    except asyncio.CancelledError:
        print("Task 1 cancelled")

    try:
        result2 = await task2
        print(f"Result 2: {result2}")
    except asyncio.CancelledError:
        print("Task 2 cancelled")

asyncio.run(main())
```

---

## The Python asyncio Module

## Timeouts and Cancellation
- Set timeouts for operations
- Cancel tasks gracefully
- Handle cancellation in coroutines
- Avoid resource leaks
- Ensure responsive applications

```python
import asyncio

async def long_running_task():
    try:
        print("Long task started")
        await asyncio.sleep(10)
        print("Long task completed")
        return "Task result"
    except asyncio.CancelledError:
        print("Long task was cancelled")
        # Cleanup code here...
        raise  # Re-raise to properly propagate cancellation

async def main():
    try:
        # Run with timeout
        result = await asyncio.wait_for(long_running_task(), timeout=2)
        print(f"Got result: {result}")
    except asyncio.TimeoutError:
        print("Task timed out")

    print("Moving on...")

asyncio.run(main())
```

---

## The Python asyncio Module

## Asynchronous Context Managers
- `async with` statement
- Asynchronous resource management
- For resources that require async setup/teardown
- Defined with `__aenter__` and `__aexit__`
- Often used with connection pools, file operations

```python
import asyncio

class AsyncResource:
    async def __aenter__(self):
        print("Acquiring resource asynchronously")
        await asyncio.sleep(1)  # Simulate async acquisition
        print("Resource acquired")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource asynchronously")
        await asyncio.sleep(0.5)  # Simulate async release
        print("Resource released")

    async def use(self):
        print("Using resource")
        await asyncio.sleep(0.5)

async def main():
    async with AsyncResource() as resource:
        await resource.use()
    print("Done")

asyncio.run(main())
```

---

## The Python asyncio Module

## Asynchronous Iteration
- `async for` statement
- Iterate over asynchronous sequences
- For data sources requiring async operations
- Defined with `__aiter__` and `__anext__`
- Often used for streaming data

```python
import asyncio

class AsyncCounter:
    def __init__(self, limit):
        self.limit = limit
        self.count = 0

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.count >= self.limit:
            raise StopAsyncIteration
        self.count += 1
        await asyncio.sleep(0.1)  # Simulate async work
        return self.count - 1

async def main():
    async for number in AsyncCounter(5):
        print(f"Got number: {number}")
    print("Iteration complete")

asyncio.run(main())
```

---

## The Python asyncio Module

## Creating Asynchronous Generators
- `async def` with `yield`
- Combines generator and coroutine features
- Can use await inside the generator
- Iterated with `async for`
- For producing async sequences

```python
import asyncio

async def async_range(start, stop):
    for i in range(start, stop):
        await asyncio.sleep(0.1)  # Simulate async work
        yield i

async def main():
    # Using async generator with async for
    print("Counting slowly:")
    async for i in async_range(1, 5):
        print(i)

    # Collecting all values
    values = [i async for i in async_range(5, 10)]
    print(f"Collected values: {values}")

asyncio.run(main())
```

---

## The Python asyncio Module

## Handling Synchronous Code
- Use executors for blocking operations
- ThreadPoolExecutor for I/O-bound operations
- ProcessPoolExecutor for CPU-bound operations
- Prevents event loop blocking
- Integrates sync code with async

```python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

def blocking_io():
    # This is a blocking function
    print("Starting blocking I/O operation")
    time.sleep(1)  # Simulates file I/O, database query, etc.
    print("Blocking I/O complete")
    return "Result from blocking operation"

async def main():
    # Create an executor
    executor = ThreadPoolExecutor(max_workers=5)

    # Run blocking function in the executor
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(executor, blocking_io)

    print(f"Got result: {result}")

    # Run multiple blocking operations concurrently
    blocking_tasks = [
        loop.run_in_executor(executor, blocking_io)
        for _ in range(3)
    ]

    # Wait for all to complete
    await asyncio.gather(*blocking_tasks)

asyncio.run(main())
```

---

## The Python asyncio Module

## Streams API
- High-level API for network operations
- Asynchronous TCP connections
- Straightforward reading and writing
- Error handling and connection management
- Built on lower-level transports and protocols

```python
import asyncio

async def tcp_echo_client():
    # Connect to server
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    # Send data
    message = 'Hello, server!'
    print(f'Sending: {message}')
    writer.write(message.encode())
    await writer.drain()

    # Receive response
    data = await reader.read(100)
    print(f'Received: {data.decode()}')

    # Close connection
    writer.close()
    await writer.wait_closed()

async def tcp_echo_server():
    async def handle_client(reader, writer):
        # Read data
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print(f"Received {message} from {addr}")

        # Send response
        writer.write(f"Echo: {message}".encode())
        await writer.drain()

        # Close connection
        writer.close()

    # Start server
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)
    async with server:
        await server.serve_forever()

# Run client and server
asyncio.run(tcp_echo_client())
```

---

## The Python asyncio Module

## Synchronization Primitives
- Lock: Mutual exclusion
- Event: Signal between tasks
- Condition: Wait for a condition to be true
- Semaphore: Control access to a resource
- Handles concurrency issues

```python
import asyncio

async def worker(lock, worker_id):
    print(f"Worker {worker_id} waiting for lock")
    async with lock:
        print(f"Worker {worker_id} acquired lock")
        await asyncio.sleep(1)  # Simulate work
        print(f"Worker {worker_id} releasing lock")

async def event_example():
    # Create an event
    event = asyncio.Event()

    # Waiting task
    async def waiter():
        print("Waiter: Waiting for event...")
        await event.wait()
        print("Waiter: Event received, proceeding!")

    # Signal task
    async def setter():
        print("Setter: Working...")
        await asyncio.sleep(2)
        print("Setter: Setting event")
        event.set()

    # Run both tasks
    await asyncio.gather(waiter(), setter())

async def main():
    # Lock example
    lock = asyncio.Lock()
    await asyncio.gather(*(worker(lock, i) for i in range(3)))

    # Event example
    await event_example()

asyncio.run(main())
```

---

## Alternative Async Frameworks

## The Twisted Framework
- One of the oldest Python async frameworks
- Event-driven networking engine
- Callback-based programming style
- Rich protocol implementations
- Used in many production systems

```python
from twisted.internet import reactor, protocol
from twisted.web.client import Agent, readBody
from twisted.internet.defer import inlineCallbacks

# Simple HTTP client
@inlineCallbacks
def fetch_page(url):
    agent = Agent(reactor)
    response = yield agent.request(b'GET', url.encode())
    body = yield readBody(response)
    print(f"Response from {url}: {len(body)} bytes")
    reactor.stop()

# TCP Echo Server
class EchoProtocol(protocol.Protocol):
    def dataReceived(self, data):
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return EchoProtocol()

# Run the client
fetch_page('http://example.com')
# Or run the server
# reactor.listenTCP(8000, EchoFactory())

# Start the event loop
reactor.run()
```

---

## Alternative Async Frameworks

## Trio
- Modern async framework
- Focus on usability and correctness
- Nurseries for structured concurrency
- Robust cancellation
- Clear error handling

```python
import trio

async def child_task(nursery, i):
    print(f"Task {i} starting")
    await trio.sleep(1)
    print(f"Task {i} finished")

async def parent_task():
    print("Parent task starting")
    async with trio.open_nursery() as nursery:
        # Start three child tasks
        for i in range(3):
            nursery.start_soon(child_task, nursery, i)
        # Parent task continues while children run
        print("Parent task waiting for children")
    # Nursery block exits when all children are done
    print("All tasks completed")

# Run the parent task
trio.run(parent_task)
```

---

## Integrating Different Async Frameworks

## Working with Multiple Frameworks
- Challenges in compatibility
- Adapter patterns
- Bridging between frameworks
- Hybrid systems approach
- Each framework has unique strengths

```python
# Combining asyncio and Twisted (example pattern)

import asyncio
from twisted.internet import asyncioreactor
from twisted.web.client import Agent, readBody

# Set up Twisted to use asyncio's event loop
asyncioreactor.install()
from twisted.internet import reactor

# Bridge function: Twisted Deferred to asyncio Future
def deferred_to_future(deferred):
    future = asyncio.Future()

    def on_success(result):
        if not future.done():
            future.set_result(result)

    def on_failure(failure):
        if not future.done():
            future.set_exception(failure.value)

    deferred.addCallbacks(on_success, on_failure)
    return future

# Use Twisted from asyncio
async def fetch_with_twisted(url):
    agent = Agent(reactor)
    response = await deferred_to_future(agent.request(b'GET', url.encode()))
    body = await deferred_to_future(readBody(response))
    return body.decode()

# Main asyncio function
async def main():
    result = await fetch_with_twisted(b'http://example.com')
    print(f"Got response: {len(result)} bytes")

# Run with asyncio
asyncio.run(main())
```

---

## Best Practices for Async Code

## Async Code Organization
- Keep coroutines focused on a single responsibility
- Use clear naming conventions for async functions
- Structure code for easy error handling
- Separate I/O operations from pure computation
- Group related operations in modules

```python
# Good async organization example

# In db.py
async def get_user(user_id):
    """Get user by ID from database."""
    # ...

async def update_user(user_id, data):
    """Update user in database."""
    # ...

# In api.py
async def fetch_remote_data(url):
    """Fetch data from remote API."""
    # ...

# In service.py
async def process_user_data(user_id):
    """Process user data with remote enrichment."""
    # Load user
    user = await db.get_user(user_id)

    # Enrich with remote data
    remote_data = await api.fetch_remote_data(f"/user/{user_id}/details")

    # Merge and update
    updated_user = {**user, **remote_data}
    await db.update_user(user_id, updated_user)

    return updated_user
```

---

## Best Practices for Async Code

## Error Handling in Async Code
- Use try/except inside coroutines
- Propagate errors with proper context
- Handle task cancellation cleanly
- Set appropriate timeouts
- Avoid swallowing exceptions

```python
import asyncio

async def fetch_with_retry(url, max_retries=3):
    """Fetch URL with retry logic and proper error handling."""
    for attempt in range(1, max_retries + 1):
        try:
            # Set a timeout for the request
            async with asyncio.timeout(10):
                return await make_request(url)

        except asyncio.TimeoutError:
            print(f"Request timed out (attempt {attempt}/{max_retries})")

        except ConnectionError as e:
            print(f"Connection error: {e} (attempt {attempt}/{max_retries})")

        except Exception as e:
            # Log unexpected errors but don't retry them
            print(f"Unexpected error: {e}")
            raise

        # Exponential backoff
        await asyncio.sleep(2 ** (attempt - 1))

    # If we get here, all retries failed
    raise RuntimeError(f"Failed to fetch {url} after {max_retries} attempts")
```

---

## Best Practices for Async Code

## Debugging Async Code
- Use logging extensively
- Enable asyncio debug mode
- Set descriptive task names
- Visual traceback for coroutines
- Async-aware debuggers

```python
import asyncio
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create named tasks
async def worker(name):
    logger = logging.getLogger(f"worker.{name}")
    logger.info(f"Starting work")
    await asyncio.sleep(1)
    logger.info(f"Work completed")

async def main():
    # Enable asyncio debug mode
    asyncio.get_event_loop().set_debug(True)

    # Create tasks with names
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(f"worker-{i}"))
        task.set_name(f"WorkerTask-{i}")  # Set descriptive name
        tasks.append(task)

    # Wait for all tasks
    await asyncio.gather(*tasks)

# Run with a task factory that logs task creation/destruction
asyncio.run(main(), debug=True)
```

---

## Best Practices for Async Code

## Testing Async Code
- Use pytest-asyncio for async tests
- Mock async calls appropriately
- Write tests for error conditions
- Test concurrency behavior
- Test timeouts and cancellation

```python
# Install pytest-asyncio first
# pip install pytest-asyncio

import pytest
import asyncio

# Function to test
async def fetch_data(url):
    if not url.startswith('http'):
        raise ValueError("Invalid URL")
    # Simulate network delay
    await asyncio.sleep(0.1)
    return f"Data from {url}"

# Test basic functionality
@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data("http://example.com")
    assert result == "Data from http://example.com"

# Test error condition
@pytest.mark.asyncio
async def test_fetch_data_invalid_url():
    with pytest.raises(ValueError):
        await fetch_data("invalid-url")

# Test concurrent execution
@pytest.mark.asyncio
async def test_concurrent_fetch():
    urls = [f"http://example.com/{i}" for i in range(3)]
    results = await asyncio.gather(*[fetch_data(url) for url in urls])
    assert len(results) == 3
    assert all(r.startswith("Data from http://") for r in results)

# Test timeout
@pytest.mark.asyncio
async def test_fetch_with_timeout():
    with pytest.raises(asyncio.TimeoutError):
        async with asyncio.timeout(0.05):  # Shorter than the sleep in fetch_data
            await fetch_data("http://example.com")
```

---

## Practical Example

## Complete Async Web API Client
```python
import asyncio
import aiohttp
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self._get_headers())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def _get_headers(self) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers

    async def get(self, endpoint: str) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"GET request to {url}")

        async with self.session.get(url) as response:
            response.raise_for_status()
            return await response.json()

    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"POST request to {url}")

        async with self.session.post(url, json=data) as response:
            response.raise_for_status()
            return await response.json()

    async def fetch_users(self) -> List[Dict[str, Any]]:
        return await self.get("users")

    async def fetch_user(self, user_id: int) -> Dict[str, Any]:
        return await self.get(f"users/{user_id}")

    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.post("users", user_data)

async def main():
    async with APIClient("https://api.example.com", api_key="your_api_key") as client:
        # Fetch all users
        users = await client.fetch_users()
        print(f"Found {len(users)} users")

        # Fetch specific users concurrently
        user_ids = [1, 2, 3]
        user_tasks = [client.fetch_user(uid) for uid in user_ids]
        users = await asyncio.gather(*user_tasks)

        # Process users
        for user in users:
            print(f"User: {user['name']} - {user['email']}")

        # Create a new user
        new_user = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        created = await client.create_user(new_user)
        print(f"Created user with ID: {created['id']}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
```

---

## Summary

## Key Takeaways
- Generators yield values and maintain state
- Coroutines are the foundation of async Python
- asyncio provides a standard async framework
- async/await simplifies asynchronous code
- Different async patterns for different problems
- Careful error handling is crucial in async code
- Test and debug async code thoroughly
- Async excels at I/O-bound operations

---

## Resources

## Further Learning
- Python asyncio documentation
- "Python Concurrency with asyncio" by Matthew Fowler
- Trio documentation
- Twisted documentation
- "Fluent Python" by Luciano Ramalho (chapters on async)
- Real Python tutorials on async programming
- PEP 492: Coroutines with async and await syntax
