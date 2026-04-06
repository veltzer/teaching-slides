# Using Third Party Modules
---
## What are Third Party Modules?
- Packages not included in Python's standard library
- Published on PyPI (Python Package Index)
- Installed using `pip` (Python's package manager)
- Over 500,000 packages available
- Cover virtually every domain
---
## PyPI - Python Package Index
- https://pypi.org
- The official repository for Python packages
- Anyone can publish packages
- Packages have version numbers, documentation, and metadata
- Each package page shows:
    - Description and README
    - Installation command
    - Version history
    - License information
---
## `pip` - The Package Installer

```bash
# Install a package
pip install requests

# Install specific version
pip install requests==2.31.0

# Install minimum version
pip install "requests>=2.28"

# Install from requirements file
pip install -r requirements.txt
```
---
## `pip` - Common Commands

```bash
# List installed packages
pip list

# Show package details
pip show requests

# Search for packages (use PyPI website instead)
# pip search is disabled

# Upgrade a package
pip install --upgrade requests

# Uninstall a package
pip uninstall requests
```
---
## `pip freeze`

```bash
# Show installed packages in requirements format
pip freeze

# Save to requirements file
pip freeze > requirements.txt

# Install from requirements file
pip install -r requirements.txt
```

- `pip freeze` outputs exact versions
- Use this to recreate environments
---
## `requirements.txt` Format

```config
requests==2.31.0
numpy>=1.24.0
pandas~=2.0
flask>=2.3,<3.0
python-dateutil
pytest>=7.0
```

- `==` exact version
- `>=` minimum version
- `~=` compatible release (same major.minor)
- `>=,<` range of versions
---
## Virtual Environments - Why?
- Different projects may need different package versions
- System Python should not be cluttered
- Reproducible environments across machines
- Isolation prevents conflicts

```diagram
Project A: requests==2.28
Project B: requests==2.31
System: ???
```
---
## Creating Virtual Environments

```bash
# Create a virtual environment
python3 -m venv myenv

# Activate (Linux/macOS)
source myenv/bin/activate

# Activate (Windows)
myenv\Scripts\activate

# Deactivate
deactivate
```
---
## Virtual Environment Workflow

```bash
# 1. Create project directory
mkdir my_project && cd my_project

# 2. Create virtual environment
python3 -m venv .venv

# 3. Activate
source .venv/bin/activate

# 4. Install dependencies
pip install requests flask

# 5. Save requirements
pip freeze > requirements.txt

# 6. Deactivate when done
deactivate
```
---
## Virtual Environment Structure

```tree
.venv/
  bin/           (Scripts/ on Windows)
    activate
    python
    pip
  lib/
    python3.12/
      site-packages/
        requests/
        flask/
  pyvenv.cfg
```
---
## `requests` - HTTP Library

```python
import requests

# GET request
response = requests.get("https://api.github.com")
print(response.status_code)  # 200
print(response.json())       # Parsed JSON
print(response.headers)      # Response headers
```
---
## `requests` - POST and Parameters

```python
import requests

# POST with JSON body
response = requests.post(
    "https://httpbin.org/post",
    json={"name": "Alice", "age": 30},
)
print(response.json())

# GET with query parameters
response = requests.get(
    "https://api.example.com/search",
    params={"q": "python", "page": 1},
)
```
---
## `requests` - Error Handling

```python
import requests

try:
    response = requests.get("https://api.example.com", timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.ConnectionError:
    print("Connection failed")
except requests.Timeout:
    print("Request timed out")
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
```
---
## Popular Third Party Packages
| Package | Purpose |
|---------|---------|
| `requests` | HTTP client |
| `numpy` | Numerical computing |
| `pandas` | Data analysis |
| `flask` | Web framework (lightweight) |
| `django` | Web framework (full-featured) |
| `fastapi` | Modern async web framework |
| `pytest` | Testing framework |
| `sqlalchemy` | Database ORM |
| `pillow` | Image processing |
| `click` | CLI framework |
---
## `numpy` - Quick Overview

```python
import numpy as np

# Create arrays
a = np.array([1, 2, 3, 4, 5])
b = np.arange(0, 10, 2)
c = np.zeros((3, 3))
d = np.ones((2, 4))

# Operations are vectorized
print(a * 2)        # [2, 4, 6, 8, 10]
print(a + b[:5])    # element-wise addition
print(np.mean(a))   # 3.0
print(np.std(a))    # 1.414...
```
---
## `pandas` - Quick Overview

```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [30, 25, 35],
    "city": ["NYC", "LA", "Chicago"],
})

print(df)
print(df["age"].mean())        # 30.0
print(df[df["age"] > 28])      # Filter rows
print(df.sort_values("name"))  # Sort
```
---
## `click` - CLI Framework

```python
import click

@click.command()
@click.option("--name", prompt="Your name", help="Name to greet")
@click.option("--count", default=1, help="Number of greetings")
def hello(name, count):
    """Simple program that greets NAME."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")

if __name__ == "__main__":
    hello()
```

```bash
python3 hello.py --name Alice --count 3
```
---
## `rich` - Rich Text in Terminal

```python
from rich.console import Console
from rich.table import Table

console = Console()

table = Table(title="Students")
table.add_column("Name", style="cyan")
table.add_column("Grade", justify="right", style="green")

table.add_row("Alice", "92")
table.add_row("Bob", "85")

console.print(table)
console.print("[bold red]Error![/bold red] Something went wrong")
```
---
## `python-dotenv` - Environment Configuration

```python
# .env file:
# DATABASE_URL=postgresql://localhost/mydb
# SECRET_KEY=my-secret-key

from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")
secret = os.getenv("SECRET_KEY")
print(db_url)
```

```bash
pip install python-dotenv
```
---
## `tqdm` - Progress Bars

```python
from tqdm import tqdm
import time

# Simple progress bar
for i in tqdm(range(100)):
    time.sleep(0.01)

# With description
for i in tqdm(range(100), desc="Processing"):
    time.sleep(0.01)

# Manual update
with tqdm(total=100) as pbar:
    for i in range(10):
        time.sleep(0.1)
        pbar.update(10)
```
---
## `pydantic` - Data Validation

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    age: int
    email: EmailStr

# Valid data
user = User(name="Alice", age=30, email="alice@example.com")
print(user.model_dump())

# Invalid data raises ValidationError
# User(name="Bob", age="not_a_number", email="invalid")
```

```bash
pip install pydantic[email]
```
---
## Checking Package Security

```bash
# pip-audit: check for known vulnerabilities
pip install pip-audit
pip-audit

# safety: another security checker
pip install safety
safety check
```

- Always review packages before installing
- Check download counts, maintenance status, and license
- Prefer well-known, actively maintained packages
---
## Summary
- PyPI hosts over 500,000 Python packages
- Use `pip` to install and manage packages
- Virtual environments isolate project dependencies
- `requirements.txt` for reproducible installations
- Popular packages: `requests`, `numpy`, `pandas`, `flask`
- Always use virtual environments for projects
- Check package security and maintenance status
