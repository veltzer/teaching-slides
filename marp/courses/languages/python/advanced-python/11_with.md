---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---
# Python's `with` Statement

## Overview
- Understanding the `with` statement
- Context managers in Python
- Creating your own context managers
- Best practices and use cases
- Advanced techniques

---

## The Problem: Resource Management: Resource Management Challenges

- Proper cleanup of resources
- Files need to be closed
- Locks need to be released
- Network connections need to be terminated
- Database transactions need to be committed or rolled back
- Even when exceptions occur

```python
# Traditional approach with try/finally
file = open('data.txt', 'r')
try:
    data = file.read()
    # Process data...
finally:
    file.close()  # Ensure file is closed even if an exception occurs
```

---

## The Problem: Resource Management: Common Resource Management Issues

- Forgetting to release resources
- Resources not released after exceptions
- Nested resource management gets complex
- Code becomes cluttered with cleanup logic
- Error-prone and repetitive patterns

```python
# Nested resources can be unwieldy
connection = create_db_connection()
try:
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        # Process results...
    finally:
        cursor.close()
finally:
    connection.close()
```

---

## Enter the `with` Statement: What is the `with` Statement?

- Introduced in Python 2.5 (PEP 343)
- Simplifies resource management
- Ensures proper setup and cleanup
- Works with context managers
- Makes code cleaner and more readable
- Handles exceptions properly

```python
# Same file operation with 'with'
with open('data.txt', 'r') as file:
    data = file.read()
    # Process data...
# File is automatically closed when the block exits
```

---

## Enter the `with` Statement: How the `with` Statement Works

1. Evaluates the expression after `with`
1. Calls `__enter__()` method on the result
1. Assigns the return value to the variable after `as`
1. Executes the code block
1. Calls `__exit__()` method when the block exits (even if an exception occurs)

```python
# Simplified explanation of what happens
file_obj = open('data.txt', 'r')  # Expression evaluation
file = file_obj.__enter__()       # Call __enter__, assign to 'file'
try:
    data = file.read()            # Execute the code block
finally:
    file_obj.__exit__(None, None, None)  # Call __exit__ when done
```

---

## Context Manager Protocol

![context_manager_protocol](svg/courses/languages/python/advanced-python/11_with/context_manager_protocol.svg)

---

## Context Managers: What are Context Managers?

- Objects that define `__enter__` and `__exit__` methods
- Control entry to and exit from runtime contexts
- Provide resource acquisition and release
- Handle exceptions that occur in the context
- Foundation of the `with` statement

```python
# A simple context manager
class MyContextManager:
    def __enter__(self):
        print("Entering the context")
        return self  # The object to work with in the context

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Exiting the context")
        # Return False to propagate exceptions, True to suppress them
        return False

# Using the context manager
with MyContextManager() as mcm:
    print("Inside the context block")
```

---

## Context Managers: The `__enter__` Method

- Called when entering the context (start of `with` block)
- Takes no arguments besides `self`
- Returns the object to be bound to the `as` variable
- Can return any object, not just `self`
- Sets up resources, opens connections, etc.

```python
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None

    def __enter__(self):
        print(f"Connecting to database: {self.connection_string}")
        self.connection = connect_to_db(self.connection_string)
        return self.connection  # Return the connection, not self
```

---

## Context Managers: The `__exit__` Method

- Called when exiting the context (end of `with` block)
- Takes exception details as arguments
- Always called, even if an exception occurs
- Can handle or suppress exceptions
- Releases resources, closes connections, etc.

```python
class DatabaseConnection:
    # ... __init__ and __enter__ methods ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing database connection")
        if self.connection:
            self.connection.close()

        if exc_type is not None:
            print(f"An exception occurred: {exc_val}")
            # Return False to propagate the exception
            # Return True to suppress it
            return False
```

---

## Context Managers: Using Multiple Context Managers

- Multiple context managers can be nested
- Cleaner with multiple contexts on one line
- Contexts are entered from left to right
- Contexts are exited from right to left
- All `__exit__` methods are called even if one fails

```python
# Nested context managers
with open('input.txt', 'r') as infile:
    with open('output.txt', 'w') as outfile:
        for line in infile:
            outfile.write(line.upper())

# Cleaner syntax for multiple context managers
with open('input.txt', 'r') as infile, open('output.txt', 'w') as outfile:
    for line in infile:
        outfile.write(line.upper())
```

---

## Built-in Context Managers: File Objects

- The most common context manager
- Automatically closes files when the block exits
- Works with all file modes (read, write, append)
- Ensures proper file handling even with exceptions

```python
# Reading a file
with open('data.txt', 'r') as f:
    content = f.read()

# Writing to a file
with open('output.txt', 'w') as f:
    f.write('Hello, world!')

# Appending to a file
with open('log.txt', 'a') as f:
    f.write('New log entry\n')
```

---

## Built-in Context Managers: Threading Locks

- Protect shared resources in threaded code
- Automatically acquire and release locks
- Prevents forgetting to release locks
- Avoids deadlocks from unhandled exceptions

```python
import threading

# Shared resource and lock
counter = 0
counter_lock = threading.Lock()

def increment_counter():
    global counter

    # Use lock as a context manager
    with counter_lock:
        # This section is thread-safe
        temp = counter
        temp = temp + 1
        counter = temp

# Without context manager
def unsafe_increment():
    global counter
    counter_lock.acquire()
    try:
        counter += 1
    finally:
        counter_lock.release()
```

---

## Built-in Context Managers: The contextlib Module

- Standard library module for context managers
- Simplifies creating and working with context managers
- Various helper classes and functions
- `contextmanager` decorator for creating context managers from generators

```python
import contextlib

# Context manager for temporarily changing directories
@contextlib.contextmanager
def change_directory(path):
    import os
    original_dir = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_dir)

# Using the context manager
with change_directory('/tmp'):
    # Code here runs in /tmp
    print(f"Current directory: {os.getcwd()}")
# Back to the original directory
```

---

## Built-in Context Managers: More From contextlib

- `suppress`: Suppress specific exceptions
- `redirect_stdout` and `redirect_stderr`: Redirect output
- `ExitStack`: Dynamically manage multiple context managers
- `nullcontext`: A context manager that does nothing
- `closing`: Ensure an object's `close()` method is called

```python
from contextlib import suppress, redirect_stdout, ExitStack
import io

# Suppress specific exceptions
with suppress(FileNotFoundError):
    open('non-existent-file.txt')  # Error suppressed

# Redirect stdout
f = io.StringIO()
with redirect_stdout(f):
    print("This goes to the StringIO object")
output = f.getvalue()  # Capture the output

# ExitStack for dynamic contexts
with ExitStack() as stack:
    files = [stack.enter_context(open(f, 'r')) for f in filenames]
    # work with multiple open files
```

---

## Creating Context Managers: Class-Based Context Managers

- Define a class with `__enter__` and `__exit__` methods
- Full control over the context
- Stateful context managers
- More flexible but more verbose

```python
class Timer:
    def __init__(self, name=None):
        self.name = name or "Timer"
        self.start_time = None

    def __enter__(self):
        import time
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        elapsed = time.time() - self.start_time
        print(f"{self.name} took {elapsed:.6f} seconds")
        return False  # Don't suppress exceptions

# Using the Timer
with Timer("Database query") as timer:
    # Run some code to time
    import time
    time.sleep(1.5)
```

---

## Creating Context Managers: Generator-Based Context Managers

- Use `@contextmanager` decorator from contextlib
- Create context manager from a generator function
- Code before `yield` is the `__enter__` part
- Code after `yield` is the `__exit__` part
- More concise than class-based approach

```python
from contextlib import contextmanager

@contextmanager
def timer(name=None):
    import time
    name = name or "Timer"
    start_time = time.time()

    try:
        # The yield statement divides the function
        # into __enter__ and __exit__ parts
        yield
    finally:
        elapsed = time.time() - start_time
        print(f"{name} took {elapsed:.6f} seconds")

# Using the timer
with timer("Sorting operation"):
    # Sort a large list
    sorted([5, 3, 2, 4, 1] * 100000)
```

---

## Creating Context Managers: Yielding Values from Generator Context Managers

- The yielded value becomes the context variable
- Can provide useful objects to the `with` block
- Simplifies resource management with returns
- Used in many practical context managers

```python
from contextlib import contextmanager

@contextmanager
def open_db_connection(connection_string):
    print(f"Connecting to: {connection_string}")
    connection = create_connection(connection_string)

    try:
        # Yield the connection object to the with block
        yield connection
    finally:
        print("Closing database connection")
        connection.close()

# Using the context manager with the yielded value
with open_db_connection("postgresql://localhost/mydb") as conn:
    # Use the connection object directly
    results = conn.execute("SELECT * FROM users")
```

---

## Creating Context Managers: Exception Handling in Context Managers

- `__exit__` receives exception information
- Can handle or suppress exceptions
- Great for cleanup and error recovery
- Returning True suppresses the exception

```python
class DatabaseTransaction:
    def __init__(self, connection):
        self.connection = connection

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # No exception, commit the transaction
            print("Committing transaction")
            self.connection.commit()
        else:
            # Exception occurred, rollback
            print(f"Rolling back due to {exc_type.__name__}: {exc_val}")
            self.connection.rollback()

        self.cursor.close()
        # Return False to propagate the exception
        return False
```

---

## Creating Context Managers: Generator-Based Exception Handling

- Exceptions inside the `with` block are raised at the `yield` statement
- Can be caught with try/except around the yield
- More natural error handling flow
- Simplified transaction logic

```python
@contextmanager
def db_transaction(connection):
    cursor = connection.cursor()

    try:
        yield cursor  # Provide cursor to the with block

        # If we get here without an exception, commit
        connection.commit()
        print("Transaction committed")

    except Exception as e:
        # An exception occurred, rollback
        connection.rollback()
        print(f"Transaction rolled back: {e}")
        raise  # Re-raise the exception

    finally:
        # Always close the cursor
        cursor.close()
```

---

## When to Use Context Managers: Resource Management

- File operations
- Network connections
- Database connections
- Locks and semaphores
- Any resource that needs cleanup

```python
# File example
with open('file.txt', 'w') as f:
    f.write('content')

# Socket example
import socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('example.com', 80))
    s.sendall(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
    response = s.recv(4096)

# Database example
with connect_to_database() as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM table")
```

---

## When to Use Context Managers: Temporary State Changes

- Directory changes
- Environment variables
- System settings
- Configuration changes
- Redirecting output

```python
# Temporary directory change
@contextmanager
def working_directory(path):
    current_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(current_dir)

# Temporary environment variable
@contextmanager
def set_env_var(name, value):
    old_value = os.environ.get(name)
    os.environ[name] = value
    try:
        yield
    finally:
        if old_value is None:
            del os.environ[name]
        else:
            os.environ[name] = old_value
```

---

## When to Use Context Managers: Measurement and Profiling

- Timing operations
- Tracking memory usage
- Counting events
- Performance profiling
- Logging activities

```python
# Memory usage tracking
@contextmanager
def track_memory_usage(name):
    import tracemalloc
    import gc

    # Force GC to reduce noise
    gc.collect()
    tracemalloc.start()
    start_snapshot = tracemalloc.take_snapshot()

    try:
        yield
    finally:
        gc.collect()
        end_snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()

        # Get memory differences
        stats = end_snapshot.compare_to(start_snapshot, 'lineno')
        print(f"Memory usage for {name}:")
        for stat in stats[:3]:  # Top 3 allocations
            print(f"{stat.size_diff / 1024:.1f} KB: {stat.traceback.format()[0]}")
```

---

## When to Use Context Managers: Transactions and Atomic Operations

- Database transactions
- File writing transactions
- API operations that need to be atomic
- Operations that require rollback on failure

```python
# Simple database transaction
@contextmanager
def transaction(connection):
    cursor = connection.cursor()
    try:
        yield cursor
        connection.commit()
    except:
        connection.rollback()
        raise
    finally:
        cursor.close()

# Usage
with transaction(db_connection) as cursor:
    cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
    # If any statement fails, the entire transaction is rolled back
```

---

## When to Use Context Managers: Indentation and Readability

- Group related operations visually
- Make dependencies clear
- Indicate resource scope
- Improve code organization
- Express intent clearly

```python
# Without context manager
plt.figure()
plt.plot(x, y)
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('Title')
plt.show()

# With context manager
with plt.figure():
    plt.plot(x, y)
    plt.xlabel('X Label')
    plt.ylabel('Y Label')
    plt.title('Title')
    plt.show()
    # The figure scope is clear from indentation
```

---

## Third-Party Context Managers: Database Context Managers

- SQLAlchemy sessions
- Django database transactions
- MongoDB connections
- Redis connections
- ORM transaction managers

```python
# SQLAlchemy session context manager
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

engine = create_engine('sqlite:///example.db')

with Session(engine) as session:
    # Session is automatically committed or rolled back
    user = session.query(User).filter_by(id=1).first()
    user.name = "New Name"
    # Commit happens automatically on exiting the context
    # Rollback happens on exception
```

---

## Third-Party Context Managers: Networking Context Managers

- Requests sessions
- FTP connections
- SSH connections
- WebSocket connections
- Server contexts

```python
# Requests session
import requests

with requests.Session() as session:
    # Session maintains cookies, connection pooling
    session.auth = ('username', 'password')
    response1 = session.get('https://api.example.com/v1/data')
    response2 = session.post('https://api.example.com/v1/update',
                            json={'key': 'value'})
    # Connection is closed automatically

# Paramiko SSH connection
import paramiko
with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('hostname', username='user', password='pass')
    stdin, stdout, stderr = ssh.exec_command('ls -l')
    # Connection closed automatically
```

---

## Third-Party Context Managers: Testing Context Managers

- pytest fixtures
- unittest.mock patch
- Temporary files and directories
- Test environment settings
- Capture outputs

```python
import pytest
from unittest.mock import patch
import tempfile

# pytest fixture as context manager
@pytest.fixture
def mock_database():
    with patch('myapp.db.Database') as mock_db:
        mock_db.return_value.get_user.return_value = {'id': 1, 'name': 'Test User'}
        yield mock_db

# Temporary directory
with tempfile.TemporaryDirectory() as tmp_dir:
    # Use temporary directory for test files
    with open(f"{tmp_dir}/test.txt", "w") as f:
        f.write("test data")

    # Test that uses the file
    assert os.path.exists(f"{tmp_dir}/test.txt")
# Directory is automatically cleaned up
```

---

## Error Handling with Context Managers: Common Exception Patterns

- Catch exceptions to handle cleanup
- Suppress specific exceptions only
- Re-raise after cleanup
- Log exceptions during cleanup
- Chain or transform exceptions

```python
class FileProcessor:
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        try:
            self.file = open(self.filename, 'r')
            return self
        except FileNotFoundError as e:
            # Transform the exception
            raise ValueError(f"Configuration file {self.filename} not found") from e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()

        if exc_type is not None:
            # Log the exception but don't suppress it
            logger.error(f"Error processing {self.filename}: {exc_val}")

        # Return False to propagate exceptions
        return False
```

---

## Error Handling with Context Managers: Handling Nested Context Managers

- Inner context exceptions propagate to outer contexts
- Outer contexts can handle inner exceptions
- All `__exit__` methods are called, innermost first
- Great for transactional patterns

```python
@contextmanager
def outer_context():
    print("Enter outer context")
    try:
        yield "outer"
        print("Exit outer context normally")
    except Exception as e:
        print(f"Outer context caught: {e}")
        raise  # Re-raise the exception

@contextmanager
def inner_context():
    print("Enter inner context")
    try:
        yield "inner"
        print("Exit inner context normally")
    except Exception as e:
        print(f"Inner context caught: {e}")
        raise  # Re-raise the exception
```

---

## Nested Context Managers: Usage and Output

```python
# Using nested contexts
try:
    with outer_context() as o:
        with inner_context() as i:
            print(f"Inside both contexts: {o}, {i}")
            raise ValueError("Error inside contexts")
except ValueError as e:
    print(f"Main caught: {e}")

# Output:
# Enter outer context
# Enter inner context
# Inside both contexts: outer, inner
# Inner context caught: Error inside contexts
# Outer context caught: Error inside contexts
# Main caught: Error inside contexts
```

---

## Error Handling with Context Managers: Exception Suppression

- Context managers can suppress exceptions
- Returning True from `__exit__` suppresses the exception
- Useful for specific cleanup scenarios
- Can be dangerous if used incorrectly
- Prefer re-raising exceptions in most cases

```python
@contextmanager
def suppress_specific_errors(*exceptions):
    try:
        yield
    except Exception as e:
        # Only suppress specified exceptions
        if isinstance(e, exceptions):
            print(f"Suppressing {type(e).__name__}: {e}")
        else:
            # Re-raise other exceptions
            raise

# Usage
with suppress_specific_errors(ValueError, TypeError):
    # This error will be suppressed
    value = int("not a number")  # Raises ValueError
    print("This won't be executed")

print("Execution continues despite the error")

with suppress_specific_errors(ValueError, TypeError):
    # This error will NOT be suppressed
    open("nonexistent.txt")  # Raises FileNotFoundError
    print("This won't be executed")
```

---

## Advanced Context Managers: Reusable Context Managers

- Create context manager factories
- Parameterized context managers
- Compose multiple context managers
- Hierarchical context managers
- Context manager utilities

```python
def tempdir(suffix=None, prefix=None, dir=None):
    """Context manager factory for temporary directories."""
    import tempfile
    import shutil

    @contextmanager
    def _tempdir_manager():
        path = tempfile.mkdtemp(suffix, prefix, dir)
        try:
            yield path
        finally:
            shutil.rmtree(path)

    return _tempdir_manager()

# Usage with parameters
with tempdir(prefix="test_") as path:
    # Use the temporary directory
    with open(f"{path}/file.txt", "w") as f:
        f.write("test")
```

---

## Advanced Context Managers: Context Manager Composition

- Combine multiple context managers
- Create higher-level abstractions
- Reduce code duplication
- Hide implementation details
- Maintain clean interfaces

```python
@contextmanager
def file_transaction(filename):
    """A transactional file write context manager.

    Changes are only saved if no exceptions occur.
    """
    import os
    temp_filename = f"{filename}.tmp"

    # Create a temp file and provide it
    with open(temp_filename, 'w') as f:
        yield f

    # If we get here without an exception, rename the temp file
    os.rename(temp_filename, filename)

# Usage
try:
    with file_transaction('config.txt') as f:
        f.write('setting1=value1\n')
        f.write('setting2=value2\n')
        # If an error occurs here, original file is untouched
        x = 1 / 0  # This error would prevent the file update
except ZeroDivisionError:
    print("Transaction failed, original file preserved")
```

---

## Advanced Context Managers: Asynchronous Context Managers

- For use with `async with` statements
- Uses `__aenter__` and `__aexit__` methods
- Allows awaiting asynchronous operations
- Perfect for async I/O operations
- Requires Python 3.5+

```python
import asyncio

class AsyncConnection:
    async def __aenter__(self):
        print("Connecting asynchronously...")
        await asyncio.sleep(1)  # Simulate async connection
        print("Connected")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Disconnecting asynchronously...")
        await asyncio.sleep(0.5)  # Simulate async disconnection
        print("Disconnected")
        return False

    async def query(self, query):
        print(f"Executing query: {query}")
        await asyncio.sleep(0.5)  # Simulate query execution
        return ["result1", "result2"]

# Usage with async with
async def main():
    async with AsyncConnection() as conn:
        results = await conn.query("SELECT * FROM users")
        print(f"Got results: {results}")

asyncio.run(main())
```

---

## Advanced Context Managers: Async Generator Context Managers

- Combine async and generator-based context managers
- Use `@asynccontextmanager` decorator
- Allow asynchronous setup and teardown
- Cleaner than class-based approach for async contexts
- Require Python 3.7+

```python
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_db_transaction(connection):
    # Start transaction asynchronously
    print("Starting transaction")
    await connection.execute("BEGIN TRANSACTION")

    try:
        # Provide the connection to the with block
        yield connection

        # If no exception occurred, commit the transaction
        print("Committing transaction")
        await connection.execute("COMMIT")

    except Exception as e:
        # If an exception occurred, rollback
        print(f"Rolling back transaction: {e}")
        await connection.execute("ROLLBACK")
        raise

# Usage
async def main():
    connection = await create_async_db_connection()

    async with async_db_transaction(connection) as conn:
        await conn.execute("INSERT INTO users VALUES (1, 'Alice')")
        await conn.execute("UPDATE accounts SET balance = 1000 WHERE user_id = 1")

asyncio.run(main())
```

---

## Advanced Context Managers: Context Variables

- Thread-local-like storage for asynchronous code
- Maintains context across asynchronous calls
- Created with `contextvars` module (Python 3.7+)
- Perfect for async request context, logging context, etc.
- Can be used with context managers

```python
import asyncio
import contextvars
from contextlib import contextmanager

# Create a context variable
request_id = contextvars.ContextVar('request_id', default=None)

@contextmanager
def request_context(id):
    # Save the previous value and set new value
    token = request_id.set(id)
    try:
        yield
    finally:
        # Restore the previous value
        request_id.reset(token)

async def process_request(task_id):
    # Access the current request ID
    current_id = request_id.get()
    print(f"Task {task_id} processing request {current_id}")
    await asyncio.sleep(0.1)
```

---

## Context Variables: Async Main Runner

```python
async def main():
    # Run with different request contexts
    with request_context("REQ-1"):
        await asyncio.gather(
            process_request(1),
            process_request(2)
        )

    with request_context("REQ-2"):
        await process_request(3)

asyncio.run(main())
```

---

## Advanced Context Managers: ExitStack: Dynamic Context Management

- Dynamically manage multiple context managers
- Add or remove contexts at runtime
- Great for variable numbers of resources
- Proper cleanup in all cases
- From contextlib module

```python
from contextlib import ExitStack

def process_files(file_list):
    with ExitStack() as stack:
        # Open all files dynamically
        files = [stack.enter_context(open(fname)) for fname in file_list]

        # All files are now open and will be closed when exiting the with block

        # Process all files
        for i, file in enumerate(files):
            print(f"File {i+1} first line: {file.readline().strip()}")

        # Optionally add more contexts at runtime
        if condition:
            lock = stack.enter_context(threading.Lock())
            # Do something with the lock

        # Can also register other cleanup callbacks
        stack.callback(cleanup_function)

        # Can pop contexts if needed before the block exits
        if early_exit_needed:
            stack.pop_all()
```

---

## Advanced Context Managers: Extending ExitStack: AsyncExitStack

- Asynchronous version of ExitStack
- For managing async context managers
- Similar API to ExitStack
- Allows dynamic async resource management
- Available in Python 3.7+

```python
import asyncio
from contextlib import AsyncExitStack

async def process_connections(urls):
    async with AsyncExitStack() as stack:
        # Open all connections asynchronously
        conns = [await stack.enter_async_context(connect(url))
                for url in urls]

        # All connections are now established
        # Process them concurrently
        results = await asyncio.gather(
            *[conn.fetch_data() for conn in conns]
        )

        # Register async cleanup callbacks
        stack.push_async_callback(async_cleanup_function)

        return results

async def main():
    urls = ['http://example.com', 'http://example.org', 'http://example.net']
    results = await process_connections(urls)
    print(f"Got {len(results)} results")

asyncio.run(main())
```

---

## Advanced Context Managers: Context Manager Decorators

- Convert a function into a context manager
- Change how a function executes
- Add setup and teardown around functions
- Can be combined with other decorators
- Create reusable context management patterns

```python
import time
from functools import wraps
from contextlib import contextmanager

# Timer context manager
@contextmanager
def timed(name=None):
    start_time = time.time()
    yield
    elapsed = time.time() - start_time
    print(f"{name or 'Operation'} took {elapsed:.6f} seconds")

# Timing decorator using the context manager
def time_this(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with timed(func.__name__):
            return func(*args, **kwargs)
    return wrapper

# Usage as decorator
@time_this
def slow_function():
    time.sleep(0.5)
    return "Result"

# Usage as context manager
with timed("Manual timing"):
    time.sleep(0.3)
```

---

## Practical Examples: File Processing Context Manager

```python
class CSVProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.input_fd = None
        self.output_fd = None
        self.reader = None
        self.writer = None

    def __enter__(self):
        import csv

        # Open input and output files
        self.input_fd = open(self.input_file, 'r', newline='')
        self.output_fd = open(self.output_file, 'w', newline='')

        # Create CSV reader and writer
        self.reader = csv.reader(self.input_fd)
        self.writer = csv.writer(self.output_fd)

        return self
```

---

## File Processing Context Manager: Exit and Usage

```python
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up resources
        if self.input_fd:
            self.input_fd.close()
        if self.output_fd:
            self.output_fd.close()

        # Log any errors
        if exc_type:
            print(f"Error during CSV processing: {exc_val}")

        # Don't suppress exceptions
        return False

    def process(self, transform_func):
        # Process CSV applying the transform function to each row
        for row in self.reader:
            transformed_row = transform_func(row)
            self.writer.writerow(transformed_row)

# Usage
with CSVProcessor('input.csv', 'output.csv') as processor:
    processor.process(lambda row: [cell.upper() for cell in row])
```

---

## Practical Examples: Database Transaction Context Manager

```python
import sqlite3
from contextlib import contextmanager

@contextmanager
def db_transaction(db_path):
    """Database transaction context manager for SQLite."""
    # Connect to the database
    connection = sqlite3.connect(db_path)
    connection.execute("BEGIN TRANSACTION")

    try:
        # Provide a cursor to the context
        cursor = connection.cursor()
        yield cursor

        # If we reach this point without errors, commit the transaction
        connection.commit()
        print("Transaction committed successfully")

    except Exception as e:
        # An exception occurred, roll back the transaction
        connection.rollback()
        print(f"Transaction rolled back: {e}")
        raise  # Re-raise the exception

    finally:
        # Close the connection in all cases
        connection.close()
```

---

## Database Transaction Context Manager: Usage

```python
# Usage
try:
    with db_transaction('example.db') as cursor:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                     ('John', 'john@example.com'))
        cursor.execute("UPDATE accounts SET balance = balance - 100 WHERE user_id = 1")
        cursor.execute("UPDATE accounts SET balance = balance + 100 WHERE user_id = 2")

        # If any statement fails, the entire transaction is rolled back
        # For example, this would cause a rollback if user_id 3 doesn't exist:
        # cursor.execute("UPDATE accounts SET balance = balance - 50 WHERE user_id = 3")
except Exception as e:
    print(f"Error executing transaction: {e}")
```

---

## Practical Examples: Resource Pool Context Manager

```python
import queue
import threading
from contextlib import contextmanager

class ResourcePool:
    def __init__(self, resources, max_count=None):
        self.resources = queue.Queue(maxsize=max_count or len(resources))
        self.lock = threading.RLock()
        self.count = 0

        # Initialize the pool with resources
        for resource in resources:
            self.resources.put(resource)
            self.count += 1

    @contextmanager
    def acquire(self, timeout=None):
        resource = None
        try:
            # Acquire a resource from the pool
            resource = self.resources.get(timeout=timeout)
            print(f"Acquired resource {resource}")
            yield resource
        finally:
            # Return the resource to the pool if it was acquired
            if resource is not None:
                print(f"Releasing resource {resource}")
                self.resources.put(resource)
```

---

## Resource Pool: Worker and Thread Usage

```python
# Usage example
def worker(pool, worker_id):
    try:
        with pool.acquire(timeout=1) as resource:
            # Use the resource
            print(f"Worker {worker_id} using resource {resource}")
            import time
            time.sleep(0.5)  # Simulate work
    except queue.Empty:
        print(f"Worker {worker_id} couldn't acquire a resource")

# Create a pool with 3 database connections
conn_pool = ResourcePool(["conn1", "conn2", "conn3"])

# Use the pool from multiple threads
threads = []
for i in range(5):  # More workers than resources
    t = threading.Thread(target=worker, args=(conn_pool, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

---

## Practical Examples: Web Request Context Manager

```python
import time
import uuid
import threading
from contextlib import contextmanager

# Thread-local storage for request context
_request_context = threading.local()

@contextmanager
def request_context(user_id=None, trace_id=None):
    """Manage web request context information."""
    # Save previous context if exists
    previous_context = getattr(_request_context, 'current', None)

    # Create new context
    _request_context.current = {
        'trace_id': trace_id or str(uuid.uuid4()),
        'user_id': user_id,
        'start_time': time.time(),
        'request_path': None,
    }
```

---

## Web Request Context Manager: Yield and Cleanup

```python
    try:
        yield _request_context.current
    finally:
        # Calculate request duration
        duration = time.time() - _request_context.current['start_time']

        # Log request details
        context = _request_context.current
        print(f"Request {context['trace_id']} for user {context['user_id']} "
              f"to {context['request_path']} took {duration:.3f}s")

        # Restore previous context
        if previous_context is None:
            del _request_context.current
        else:
            _request_context.current = previous_context

# Function to get current request context
def get_current_context():
    return getattr(_request_context, 'current', None)
```

---

## Web Request Context Manager: Request Handlers and Usage

```python
# Example request handlers
def handle_profile_request(user_id):
    ctx = get_current_context()
    if ctx:
        ctx['request_path'] = '/profile'

    # Process request
    time.sleep(0.2)  # Simulate work
    return {"user_id": user_id, "name": "John Doe"}

def handle_settings_request(user_id):
    ctx = get_current_context()
    if ctx:
        ctx['request_path'] = '/settings'

    # Process request
    time.sleep(0.3)  # Simulate work
    return {"user_id": user_id, "theme": "dark"}

# Usage
with request_context(user_id="user123") as ctx:
    result = handle_profile_request(ctx['user_id'])
    print(f"Profile result: {result}")

with request_context(user_id="user456") as ctx:
    result = handle_settings_request(ctx['user_id'])
    print(f"Settings result: {result}")
```

---

## Summary

## Key Takeaways
- The `with` statement simplifies resource management
- Context managers ensure proper cleanup even with exceptions
- Create custom context managers using classes or generators
- Use context managers for resource management, state changes, and transactions
- Advanced use cases include async contexts, nested contexts, and dynamic management
- Better code readability, reliability, and error handling

---

## Resources

## Further Reading
- Python documentation on context managers
- PEP 343: The "with" Statement
- `contextlib` module documentation
- "Python Cookbook" by David Beazley and Brian Jones
- "Fluent Python" by Luciano Ramalho
