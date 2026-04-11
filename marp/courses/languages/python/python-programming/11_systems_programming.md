---
tags:
  - languages:python
level: beginner
category: language
audience:
  - audiences:developers

---
# Systems Programming

---
## Overview
- File I/O and text processing
- Formatted output
- Working with JSON and YAML
- Running external processes
- Multiprocessing and threading
- Environment and system interaction

---
## Standard I/O Streams

```python
import sys

# Standard output
sys.stdout.write("Hello\n")

# Standard error
sys.stderr.write("Error message\n")

# Standard input
line = sys.stdin.readline()
```

- `print()` writes to `sys.stdout` by default
- Use `sys.stderr` for error messages

---
## Reading Input

```python
# Simple input
name = input("Enter your name: ")

# Read until EOF
import sys
for line in sys.stdin:
    print(f"Got: {line.strip()}")
```

```bash
echo "hello" | python3 script.py
cat data.txt | python3 script.py
```

---
## Formatted Printing - f-strings Review

```python
name = "Alice"
balance = 1234567.89

print(f"Name: {name:>20}")
print(f"Balance: ${balance:>15,.2f}")
print(f"{'Item':<15} {'Price':>10}")
print(f"{'-' * 25}")
print(f"{'Apple':<15} {'$1.50':>10}")
print(f"{'Banana':<15} {'$0.75':>10}")
```

```output
Name:                Alice
Balance: $  1,234,567.89
Item                 Price
-------------------------
Apple                $1.50
Banana               $0.75
```

---
## Formatting Tables

```python
data = [
    ("Alice", 30, "Engineer"),
    ("Bob", 25, "Designer"),
    ("Charlie", 35, "Manager"),
]

header = f"{'Name':<12} {'Age':>5} {'Role':<12}"
print(header)
print("-" * len(header))
for name, age, role in data:
    print(f"{name:<12} {age:>5} {role:<12}")
```

```output
Name           Age Role
------------------------------
Alice           30 Engineer
Bob             25 Designer
Charlie         35 Manager
```

---
## Opening Files

```python
# Open for reading (default mode)
f = open("data.txt", "r")
content = f.read()
f.close()

# Open for writing (creates or truncates)
f = open("output.txt", "w")
f.write("Hello\n")
f.close()

# Open for appending
f = open("log.txt", "a")
f.write("New entry\n")
f.close()
```

---
## File Modes
| Mode | Description |
|------|-------------|
| `"r"` | Read (default) |
| `"w"` | Write (truncate) |
| `"a"` | Append |
| `"x"` | Exclusive create (fail if exists) |
| `"b"` | Binary mode |
| `"t"` | Text mode (default) |
| `"+"` | Read and write |

---
## The `with` Statement (Context Manager)

```python
# Recommended: file is automatically closed
with open("data.txt", "r") as f:
    content = f.read()
# f is closed here, even if an exception occurred

# Multiple files
with open("input.txt") as fin, open("output.txt", "w") as fout:
    for line in fin:
        fout.write(line.upper())
```

---
## Reading Files

```python
with open("data.txt") as f:
    # Read entire file as string
    content = f.read()

    # Read one line
    f.seek(0)
    line = f.readline()

    # Read all lines as list
    f.seek(0)
    lines = f.readlines()

    # Iterate line by line (memory efficient)
    f.seek(0)
    for line in f:
        print(line.strip())
```

---
## Reading Large Files Efficiently

```python
# BAD: loads entire file into memory
with open("huge.txt") as f:
    lines = f.readlines()  # All in memory!

# GOOD: iterate line by line
with open("huge.txt") as f:
    for line in f:
        process(line)

# Read in chunks
with open("huge.bin", "rb") as f:
    while chunk := f.read(8192):
        process(chunk)
```

---
## Writing Files

```python
# Write a string
with open("output.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("Second line\n")

# Write multiple lines
lines = ["Line 1\n", "Line 2\n", "Line 3\n"]
with open("output.txt", "w") as f:
    f.writelines(lines)

# print to file
with open("output.txt", "w") as f:
    print("Hello, World!", file=f)
```

---
## File Encoding

```python
# Specify encoding explicitly
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Write with encoding
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("Hello, monde!\n")

# Handle encoding errors
with open("data.txt", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()
```

---
## Binary Files

```python
# Read binary
with open("image.png", "rb") as f:
    data = f.read()
    print(f"Size: {len(data)} bytes")
    print(f"First 4 bytes: {data[:4]}")

# Write binary
with open("output.bin", "wb") as f:
    f.write(b"\x00\x01\x02\x03")
    f.write(bytes([0, 1, 2, 3]))
```

---
## `pathlib` for File Operations

```python
from pathlib import Path

# Read and write
p = Path("data.txt")
content = p.read_text(encoding="utf-8")
p.write_text("New content\n", encoding="utf-8")

# Binary
data = Path("image.png").read_bytes()

# Check existence
if p.exists():
    print(f"Size: {p.stat().st_size}")
```

---
## File System Operations with `pathlib`

```python
from pathlib import Path

# List directory contents
for item in Path(".").iterdir():
    print(item)

# Glob patterns
for py_file in Path(".").glob("**/*.py"):
    print(py_file)

# Create directories
Path("output/data").mkdir(parents=True, exist_ok=True)

# Delete file
Path("temp.txt").unlink(missing_ok=True)
```

---
## File System Operations with `shutil`

```python
import shutil

# Copy file
shutil.copy("src.txt", "dst.txt")
shutil.copy2("src.txt", "dst.txt")  # Preserve metadata

# Copy directory tree
shutil.copytree("src_dir", "dst_dir")

# Remove directory tree
shutil.rmtree("old_dir")

# Move/rename
shutil.move("old.txt", "new.txt")

# Disk usage
usage = shutil.disk_usage("/")
print(f"Free: {usage.free / 1e9:.1f} GB")
```

---
## Temporary Files

```python
import tempfile

# Temporary file (auto-deleted)
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt") as f:
    f.write("Temporary data")
    f.flush()
    print(f.name)  # /tmp/tmpXXXXXX.txt

# Temporary directory
with tempfile.TemporaryDirectory() as tmpdir:
    print(tmpdir)  # /tmp/tmpXXXXXX
    # Directory and contents deleted after with block
```

---
## JSON - Reading and Writing

```python
import json

# Python to JSON string
data = {"name": "Alice", "scores": [90, 85, 92]}
json_str = json.dumps(data, indent=2)
print(json_str)

# JSON string to Python
parsed = json.loads(json_str)
print(parsed["name"])  # Alice

# Write to file
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Read from file
with open("data.json") as f:
    loaded = json.load(f)
```

---
## JSON - Type Mapping
| Python | JSON |
|--------|------|
| `dict` | object |
| `list`, `tuple` | array |
| `str` | string |
| `int`, `float` | number |
| `True` | `true` |
| `False` | `false` |
| `None` | `null` |

---
## JSON - Custom Serialization

```python
import json
from datetime import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

data = {"event": "meeting", "time": datetime.now()}
json_str = json.dumps(data, cls=DateEncoder, indent=2)
print(json_str)
```

---
## YAML with PyYAML

```python
import yaml

# Read YAML
with open("config.yaml") as f:
    config = yaml.safe_load(f)

print(config)

# Write YAML
data = {"name": "Alice", "scores": [90, 85, 92]}
with open("output.yaml", "w") as f:
    yaml.dump(data, f, default_flow_style=False)
```

```bash
pip install pyyaml
```

---
## CSV Files

```python
import csv

# Read CSV
with open("data.csv") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        print(row)

# Read as dictionaries
with open("data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["age"])
```

---
## CSV - Writing

```python
import csv

# Write CSV
data = [
    ["Name", "Age", "City"],
    ["Alice", 30, "NYC"],
    ["Bob", 25, "LA"],
]

with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)

# Write from dicts
with open("output.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerow({"name": "Alice", "age": 30})
```

---
## Environment Variables

```python
import os

# Read environment variable
home = os.environ["HOME"]
user = os.environ.get("USER", "unknown")

# Set environment variable (for current process)
os.environ["MY_VAR"] = "my_value"

# All environment variables
for key, value in os.environ.items():
    print(f"{key}={value}")
```

---
## Running External Commands - `subprocess`

```python
import subprocess

# Simple command
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
print(result.stdout)
print(result.returncode)  # 0 = success
```

---
## `subprocess.run()` Options

```python
import subprocess

# Capture output
result = subprocess.run(
    ["grep", "-r", "TODO", "."],
    capture_output=True,
    text=True,
    timeout=30,
)
print(result.stdout)
print(result.stderr)
print(result.returncode)

# Check for errors
result = subprocess.run(
    ["ls", "nonexistent"],
    capture_output=True,
    text=True,
    check=True,  # Raises CalledProcessError on failure
)
```

---
## `subprocess` - Piping

```python
import subprocess

# Pipe between commands
ps = subprocess.Popen(
    ["ps", "aux"],
    stdout=subprocess.PIPE,
)
grep = subprocess.Popen(
    ["grep", "python"],
    stdin=ps.stdout,
    stdout=subprocess.PIPE,
    text=True,
)
ps.stdout.close()
output = grep.communicate()[0]
print(output)
```

---
## `subprocess` - Shell Commands

```python
import subprocess

# Run shell command (use with caution)
result = subprocess.run(
    "ls -la | wc -l",
    shell=True,
    capture_output=True,
    text=True,
)
print(result.stdout.strip())
```

- `shell=True` is a security risk with user input
- Prefer passing command as a list without `shell=True`

---
## `subprocess` - Input

```python
import subprocess

result = subprocess.run(
    ["python3", "-c", "name = input(); print(f'Hello {name}')"],
    input="Alice\n",
    capture_output=True,
    text=True,
)
print(result.stdout)  # Hello Alice
```

---
## Multiprocessing - Basics

```python
from multiprocessing import Process
import os

def worker(name):
    print(f"Worker {name}, PID: {os.getpid()}")

if __name__ == "__main__":
    processes = []
    for i in range(4):
        p = Process(target=worker, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
```

---
## Multiprocessing - Pool

```python
from multiprocessing import Pool

def square(x):
    return x ** 2

if __name__ == "__main__":
    with Pool(4) as pool:
        results = pool.map(square, range(10))
        print(results)
        # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
```

---
## Multiprocessing - Pool Methods

```python
from multiprocessing import Pool

def process_item(x):
    return x ** 2

if __name__ == "__main__":
    with Pool(4) as pool:
        # map: ordered results
        results = pool.map(process_item, range(10))

        # imap: lazy ordered results
        for result in pool.imap(process_item, range(10)):
            print(result)

        # imap_unordered: lazy, any order (faster)
        for result in pool.imap_unordered(process_item, range(10)):
            print(result)
```

---
## Multiprocessing - Shared State

```python
from multiprocessing import Process, Value, Array

def increment(counter, n):
    for _ in range(n):
        with counter.get_lock():
            counter.value += 1

if __name__ == "__main__":
    counter = Value("i", 0)
    processes = [
        Process(target=increment, args=(counter, 1000))
        for _ in range(4)
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    print(counter.value)  # 4000
```

---
## Threading - Basics

```python
import threading

def worker(name):
    print(f"Thread {name} starting")
    # do some work
    print(f"Thread {name} done")

threads = []
for i in range(4):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

---
## Threading - The GIL

- CPython has the Global Interpreter Lock (GIL)
- Only one thread executes Python bytecode at a time
- Threads are useful for I/O-bound tasks
- For CPU-bound tasks, use `multiprocessing`

---
## Threading - The GIL

![threading_the_gil](svg/courses/languages/python/python-programming/11_systems_programming/threading_the_gil.svg)

---
## Threading - Thread Pool

```python
from concurrent.futures import ThreadPoolExecutor
import urllib.request

def fetch_url(url):
    with urllib.request.urlopen(url) as response:
        return len(response.read())

urls = [
    "https://www.python.org",
    "https://docs.python.org",
    "https://pypi.org",
]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(fetch_url, urls)
    for url, size in zip(urls, results):
        print(f"{url}: {size} bytes")
```

---
## `concurrent.futures` - ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor

def cpu_intensive(n):
    return sum(i * i for i in range(n))

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(cpu_intensive, 10_000_000)
            for _ in range(4)
        ]
        for f in futures:
            print(f.result())
```

---
## `concurrent.futures` - `as_completed`

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def task(n):
    time.sleep(n)
    return f"Task {n} done"

with ThreadPoolExecutor() as executor:
    futures = {executor.submit(task, i): i for i in [3, 1, 2]}

    for future in as_completed(futures):
        result = future.result()
        print(result)
```

```output
Task 1 done
Task 2 done
Task 3 done
```

---
## Threading - Locks

```python
import threading

counter = 0
lock = threading.Lock()

def increment(n):
    global counter
    for _ in range(n):
        with lock:
            counter += 1

threads = [
    threading.Thread(target=increment, args=(100_000,))
    for _ in range(4)
]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)  # 400000
```

---
## Signal Handling

```python
import signal
import sys

def handler(signum, frame):
    print(f"\nReceived signal {signum}")
    sys.exit(0)

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGTERM, handler)

print("Running... Press Ctrl+C to stop")
while True:
    pass
```

---
## Summary
- Use `open()` with `with` statement for file I/O
- `pathlib` for modern file system operations
- `json` for structured data serialization
- `subprocess` for running external commands
- `multiprocessing` for CPU-bound parallel work
- `threading` for I/O-bound concurrent work
- `concurrent.futures` for high-level parallelism
- Be aware of the GIL when choosing between threads and processes
