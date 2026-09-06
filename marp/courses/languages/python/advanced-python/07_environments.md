---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---

# Python Environments

## Overview
- Python package management
- Virtual environments
- Dependency management
- Environment management tools
- Best practices for project organization

---

## Using pip: What is pip?

- Python's official package installer
- Downloads and installs packages from PyPI
- Manages dependencies
- Comes pre-installed with Python (since 3.4)
- Command line interface

```bash
# Install a package
pip install requests

# Install a specific version
pip install requests==2.25.1

# Install with version constraints
pip install 'requests>=2.20.0,<3.0.0'

# Install from requirements file
pip install -r requirements.txt
```

---

## Using pip: Common pip Commands

- `pip install`: Install packages
- `pip uninstall`: Remove packages
- `pip list`: List installed packages
- `pip freeze`: Output installed packages in requirements format
- `pip show`: Show information about installed packages
- `pip search`: Search PyPI for packages (deprecated)

```bash
# List all installed packages
pip list

# Output installed packages in requirements format
pip freeze > requirements.txt

# Get info about a specific package
pip show requests

# Upgrade pip itself
pip install --upgrade pip
```

---

## Using pip: Installing from Different Sources

- Install from PyPI (default)
- Install from local files
- Install from version control systems
- Install from other indexes

```bash
# Install from PyPI
pip install requests

# Install from local file
pip install ./downloads/requests-2.25.1.tar.gz

# Install from GitHub
pip install git+https://github.com/psf/requests.git

# Install from alternative index
pip install --index-url https://my-custom-index.org/simple/ package-name

# Install from wheels
pip install ./package-1.0.0-py3-none-any.whl
```

---

## Using pip: pip Configuration

- Global configuration in pip.conf
- Per-user configuration
- Environment variables
- Command-line options

```bash
# Location of pip.conf on Linux/Mac
# $HOME/.config/pip/pip.conf or $HOME/.pip/pip.conf

# Location on Windows
# %APPDATA%\pip\pip.ini

# Sample pip.conf content
[global]
index-url = https://custom-pypi.org/simple
trusted-host = custom-pypi.org
timeout = 60
```

---

## Using pip: Security Considerations

- Use trusted package sources
- Verify package integrity
- Scan for vulnerabilities
- Pin dependencies for reproducibility
- Use hash verification

```bash
# Install with hash verification
pip install --require-hashes -r requirements.txt

# Generate hashes for requirements file
pip hash downloaded_package.whl

# Sample requirements with hashes
requests==2.25.1 --hash=sha256:27973dd4a904a4f13b263a19c866c13b92a39ed1c964655f025f3f8d3d75b804

# Use safety to check for vulnerabilities
pip install safety
safety check
```

---

## Virtual Environments: What Are Virtual Environments?

- Isolated Python environments
- Separate package sets for different projects
- Avoid conflicts between package versions
- Standard practice for Python development
- Critical for dependency management

---

## Virtual Environments

![what_are_virtual_environments](svg/courses/languages/python/advanced-python/07_environments/what_are_virtual_environments.svg)

---

## Virtual Environment Isolation

![virtual_environment_isolation](svg/courses/languages/python/advanced-python/07_environments/virtual_environment_isolation.svg)

---

## Virtual Environments: Why Use Virtual Environments?

- Isolate project dependencies
- Avoid system-wide package pollution
- Test with different Python versions
- Ensure reproducible builds
- Document exact dependencies
- Simplify deployment

---

## Virtual Environments: How Virtual Environments Work

- Creates a copy of Python interpreter
- Maintains its own site-packages directory
- Uses symbolic links to save disk space
- Modifies PATH environment variable when activated
- Doesn't affect global Python installation

```tree
Virtual Environment Structure:
venv/
├── bin/ (or Scripts/ on Windows)
│   ├── python  # Python interpreter
│   ├── pip     # Pip installer
│   └── activate  # Activation script
├── lib/
│   └── pythonX.Y/
│       └── site-packages/  # Package directory
├── include/  # Header files
└── pyvenv.cfg  # Configuration
```

---

## Virtual Environment Tools: Built-in venv

- Included in Python standard library (3.3+)
- Creates virtual environments
- Lightweight and straightforward
- Available anywhere Python is installed
- Doesn't handle package installation

```bash
# Create a virtual environment
python -m venv myproject_env

# Activate on Linux/Mac
source myproject_env/bin/activate

# Activate on Windows
myproject_env\Scripts\activate

# Deactivate
deactivate
```

---

## Virtual Environment Tools: virtualenv

- Original virtual environment tool
- Supports older Python versions
- More features than venv
- Faster environment creation
- More customization options

```bash
# Install virtualenv
pip install virtualenv

# Create environment
virtualenv myproject_env

# Create with specific Python version
virtualenv -p /usr/bin/python3.8 myproject_env

# Create without site-packages
virtualenv --no-site-packages myproject_env

# Activate (same as venv)
source myproject_env/bin/activate  # Linux/Mac
myproject_env\Scripts\activate  # Windows
```

---

## Dependency Management: Basic Dependency Management

- Capturing dependencies with `pip freeze`
- Storing in requirements.txt
- Installing from requirements.txt
- Simple but limited approach

```bash
# Generate requirements.txt
pip freeze > requirements.txt

# Sample requirements.txt content
requests==2.25.1
Flask==2.0.1
numpy==1.20.3
pandas==1.3.0

# Install from requirements.txt
pip install -r requirements.txt
```

---

## Dependency Management: The Problem with Simple requirements.txt

- Doesn't distinguish between direct and indirect dependencies
- No development vs. production separation
- Can't specify dependency groups (test, docs, etc.)
- No constraint specification
- Limited platform-specific dependencies
- No automatic environment management

---

## Dependency Management: Development vs. Production Dependencies

- Production: Required to run the application
- Development: Testing, linting, documentation
- Separate requirements files
- Use includes for shared dependencies

```config
# requirements.txt (production)
-r requirements-base.txt
gunicorn==20.1.0
psycopg2-binary==2.9.1

# requirements-dev.txt (development)
-r requirements-base.txt
pytest==6.2.5
flake8==3.9.2
sphinx==4.1.2

# requirements-base.txt (shared)
requests==2.25.1
PyYAML==5.4.1
```

---

## Dependency Management: Locking Dependencies

- Pin every dependency (direct and transitive)
- Ensures 100% reproducible environments
- Prevents "works on my machine" problems
- Critical for production deployments
- Can be automated with tools

```bash
# Example of a locked requirements file
certifi==2021.5.30
charset-normalizer==2.0.4
idna==3.2
requests==2.26.0
urllib3==1.26.6
```

---

## Dependency Management: Dividing Project Dependencies

- By environment (dev, test, prod)
- By functionality (core, api, web)
- By optionality (required, optional, extra)
- Helps manage complex projects
- Reduces installation size

```python
# setup.py with dependency groups
setup(
    name="myproject",
    install_requires=[
        "requests>=2.25.0",
        "PyYAML>=5.4.0",
    ],
    extras_require={
        "test": ["pytest>=6.2.0", "pytest-cov>=2.12.0"],
        "docs": ["sphinx>=4.0.0", "sphinx-rtd-theme>=0.5.0"],
        "web": ["flask>=2.0.0", "jinja2>=3.0.0"],
    }
)

# Install with extras
# pip install -e ".[test,docs]"
```

---

## Environment Management Tools: The OS Itself

- Using system Python
- System package managers
- Simple bash scripts
- Environment variables
- Limited isolation and portability

```bash
# Ubuntu/Debian
sudo apt install python3-requests python3-flask

# Fedora/RHEL
sudo dnf install python3-requests python3-flask

# macOS (Homebrew)
brew install python
pip3 install requests flask

# Using environment variables for configuration
export PYTHONPATH=/path/to/my/project
export FLASK_ENV=development
```

---

## Environment Management Tools: venv

- Python's built-in virtual environment module
- Part of standard library (Python 3.3+)
- Simple, reliable, always available
- Less feature-rich than alternatives
- Great for simple projects

```bash
# Create virtual environment
python -m venv env

# Activate
source env/bin/activate  # Linux/Mac
env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Deactivate
deactivate
```

---

## Environment Management Tools: virtualenv

- The original virtual environment tool
- Compatible with older Python versions
- More features than venv
- Popular base for other tools
- Better performance than venv

```bash
# Install
pip install virtualenv

# Create environment with specific Python
virtualenv -p python3.8 env

# Create without system site-packages
virtualenv --no-site-packages env

# Create with system packages
virtualenv --system-site-packages env
```

---

## Environment Management Tools: pipenv

- Combines pip and virtualenv
- Automatic virtual environment management
- Locks all dependencies (Pipfile.lock)
- Deterministic builds
- Modern workflow with Pipfile

```bash
# Install
pip install pipenv

# Install dependencies and create virtualenv
pipenv install

# Install dev dependencies
pipenv install --dev

# Activate virtual environment
pipenv shell

# Run command in virtual environment
pipenv run python script.py

# Generate requirements.txt
pipenv lock -r > requirements.txt
```

---

## Environment Management Tools: Pipfile Example

- Modern replacement for requirements.txt
- Separate sections for packages and dev-packages
- URL, git, and path dependencies
- Package version specifications
- Environment markers

```toml
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
requests = ">=2.25.0"
flask = "*"
numpy = {version=">=1.20.0", markers="platform_machine != 'arm64'"}

[dev-packages]
pytest = ">=6.0.0"
black = "*"
flake8 = "*"

[requires]
python_version = "3.8"
```

---

## Environment Management Tools: poetry

- Modern Python packaging and dependency management
- Separates development and project dependencies
- Lock file for deterministic installs
- Simplified publishing to PyPI
- Intuitive CLI

```bash
# Install
pip install poetry

# Create new project
poetry new my_project

# Add dependencies
poetry add requests
poetry add pytest --dev

# Install dependencies
poetry install

# Update dependencies
poetry update

# Run commands
poetry run python my_script.py

# Activate environment
poetry shell
```

---

## Environment Management Tools: pyproject.toml Example (Poetry)

- Modern Python project configuration
- Standardized by PEP 517/518
- Replaces setup.py, setup.cfg, MANIFEST.in
- Used by poetry, flit, hatch, and others

```toml
[tool.poetry]
name = "my-package"
version = "0.1.0"
description = "My Python package"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
requests = "^2.25.1"
numpy = "^1.20.0"

[tool.poetry.dev-dependencies]
pytest = "^6.2.5"
black = "^21.6b0"
flake8 = "^3.9.2"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

---

## Environment Management Tools: pip-tools

- Lightweight dependency management
- Generates pinned requirements.txt
- Separates input (requirements.in) from output
- Handles constraints well
- Doesn't create virtual environments

```bash
# Install
pip install pip-tools

# Create requirements.in
# requests>=2.25.0
# flask>=2.0.0

# Generate locked requirements.txt
pip-compile requirements.in

# Install dependencies
pip-sync requirements.txt

# Update a specific package
pip-compile --upgrade-package requests requirements.in

# Generate dev requirements
pip-compile requirements-dev.in
```

---

## Environment Management Tools: Hatch

- Modern project management
- Virtual environment management
- Project creation from templates
- Standardized configuration
- Simple publishing workflow

```bash
# Install
pip install hatch

# Create new project
hatch new my_project

# Create environment
hatch env create

# Run in environment
hatch run test:pytest

# Shell in environment
hatch shell

# Build and publish
hatch build
hatch publish
```

---

## Environment Management Tools: conda

- Cross-platform package manager
- Language-agnostic (not just Python)
- Popular in data science
- Handles binary dependencies
- Environment and package management in one

```bash
# Install a package
conda install numpy

# Create environment
conda create --name myenv python=3.8

# Activate environment
conda activate myenv

# Install from requirements
conda install --file requirements.txt

# Create environment from file
conda env create -f environment.yml

# Export environment
conda env export > environment.yml
```

---

## Environment Management Tools: Comparison of Tools

- **venv**: Simple, built-in, minimal
- **virtualenv**: More features, works with older Python
- **pipenv**: Modern workflow, automatic environment, Pipfile
- **poetry**: Complete package management, publishing
- **pip-tools**: Lightweight, focused on locking
- **conda**: Cross-platform, binary packages
- **Hatch**: Simplified project management

---

## Environment Management Tools: Choosing the Right Tool

- **Project size and complexity**
- **Team familiarity**
- **Binary dependencies**
- **Publishing requirements**
- **Development workflow**
- **Platform requirements**

---

## Environment Management Tools

![choosing_the_right_tool](svg/courses/languages/python/advanced-python/07_environments/choosing_the_right_tool.svg)

---

## Version Numbers: Semantic Versioning

- Standard version numbering scheme
- MAJOR.MINOR.PATCH
- Backwards compatibility rules
- Used by most Python packages

```misc
MAJOR: Incompatible API changes
MINOR: Add functionality (backwards-compatible)
PATCH: Bug fixes (backwards-compatible)

Examples:
1.0.0 - Initial release
1.0.1 - Bug fixes
1.1.0 - New features, backwards-compatible
2.0.0 - Breaking changes
```

---

## Version Numbers: Version Specifiers

- `==`: Exact version
- `>=`, `<=`, `>`, `<`: Comparison operators
- `~=`: Compatible release
- `!=`: Excludes version
- Comma for multiple constraints

```config
requests==2.25.1      # Exactly version 2.25.1
requests>=2.25.0      # Version 2.25.0 or higher
requests<3.0.0        # Any version less than 3.0.0
requests>=2.25.0,<3.0.0  # Version between 2.25.0 and 3.0.0
requests~=2.25.0      # Version 2.25.0 or higher, but less than 2.26.0
```

---

## Version Numbers: Version Constraints Best Practices

- Pin versions in deployment requirements
- Use ranges in library dependencies
- Be specific about compatibility
- Consider using compatible release operator (~=)
- Upper bound major versions

```python
# Application requirements.txt - pin exact versions
requests==2.25.1
flask==2.0.1

# Library setup.py - use ranges
install_requires=[
    "requests>=2.25.0,<3.0.0",
    "flask>=2.0.0,<3.0.0",
]

# Alternative using compatible release
install_requires=[
    "requests~=2.25.0",
    "flask~=2.0.0",
]
```

---

## Version Numbers: When to Set Version Numbers

- Always in production code
- Always when deploying applications
- Always when sharing code with others
- Not always during early development
- Consider policy for internal packages

---

## Version Numbers: Version Handling in Different Tools

- **pip**: requirements.txt with == or constraints
- **pipenv**: Uses ^ by default in Pipfile
- **poetry**: Uses ^ by default in pyproject.toml
- **pip-tools**: Direct control in requirements.in
- **conda**: environment.yml with exact or range

```toml
# Poetry default (^): Compatible with 2.x but not 3.x
requests = "^2.25.1"

# Poetry exact (==): Only 2.25.1
requests = "==2.25.1"

# Poetry caret (~): Compatible with 2.25.x but not 2.26.x
requests = "~2.25.1"
```

---

## Practical Workflow: venv

## Step-by-Step Project Setup
- Create project directory
- Create and activate virtual environment
- Install packages
- Save dependencies
- Document the process

```bash
# Create project directory
mkdir myproject
cd myproject

# Create virtual environment
python -m venv venv

# Activate environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install packages
pip install flask requests

# Save dependencies
pip freeze > requirements.txt

# Create .gitignore (exclude venv)
echo "venv/" > .gitignore
```

---

## Practical Workflow: pipenv

## Step-by-Step Project Setup
- Create project directory
- Initialize Pipenv project
- Install dependencies
- Use the environment
- Commit files to version control

```bash
# Create project directory
mkdir myproject
cd myproject

# Initialize project with specific Python
pipenv --python 3.8

# Install packages
pipenv install flask requests

# Install dev packages
pipenv install pytest black --dev

# Run scripts
pipenv run python app.py

# Activate environment
pipenv shell

# Commit Pipfile and Pipfile.lock
git add Pipfile Pipfile.lock
git commit -m "Initialize project with dependencies"
```

---

## Practical Workflow: poetry

## Step-by-Step Project Setup
- Create new poetry project
- Configure project metadata
- Add dependencies
- Use the environment
- Commit files to version control

```bash
# Create new project
poetry new myproject
cd myproject

# Add dependencies
poetry add flask requests

# Add dev dependencies
poetry add pytest black --dev

# Run scripts
poetry run python app.py

# Activate environment
poetry shell

# Update dependencies
poetry update

# Commit pyproject.toml and poetry.lock
git add pyproject.toml poetry.lock
git commit -m "Initialize project with dependencies"
```

---

## Best Practices: Managing Development Environments

- One environment per project
- Document environment creation
- Keep environments updated
- Automate environment setup
- Use consistent tools across team

```bash
# Script to set up dev environment (setup.sh)
#!/bin/bash
set -e

# Create virtual environment
python -m venv venv

# Activate
source venv/bin/activate

# Install dev dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

echo "Development environment ready!"
```

---

## Best Practices: Dependency Management Strategy

- Lock all dependencies for applications
- Use version ranges for libraries
- Regularly update dependencies
- Automate dependency updates
- Keep an eye on security alerts

```misc
# For applications
1. Use pipenv/poetry/pip-tools to lock ALL dependencies
2. Run CI with locked versions
3. Schedule regular updates
4. Use tools like Dependabot or PyUp

# For libraries
1. Define minimum compatible versions
2. Use upper bounds on major versions
3. Test against multiple dependency versions
4. Document compatibility
```

---

## Best Practices: Handling Conflicting Dependencies

- Use newer versions of tools (better resolvers)
- Isolate conflicting packages in different environments
- Consider alternative packages
- Contact package maintainers
- Fork and fix if necessary

```bash
# When encountering conflicts

# 1. Try upgrading the resolver
pip install --upgrade pip

# 2. Try installing dependencies one by one
pip install package1
pip install package2

# 3. Find the specific conflict
pip install package1==1.2.3 package2
# Try different versions to identify conflict

# 4. Sometimes a different installation order helps
pip install conflicting-dependency==1.2.3
pip install main-package
```

---

## Best Practices: Reproducible Environments

- Lock ALL dependencies (including transitive)
- Include Python version
- Document system dependencies
- Version control your dependency files
- Consider containerization

```bash
# Docker approach (Dockerfile)
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]

# Build and run
# docker build -t myapp .
# docker run myapp
```

---

## Best Practices: CI/CD Integration

- Test with exact same dependencies as production
- Install from lock files
- Cache dependencies in CI
- Test in clean environments
- Multiple Python versions if needed

```yaml
# GitHub Actions example
name: Python Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest
```

---

## Best Practices: Private Package Repositories

- Host internal packages
- Mirror of PyPI for airgapped environments
- Scan packages for security issues
- Serve custom packages
- Tools: PyPI-Server, Artifactory, Nexus, DevPi

```bash
# Install pypiserver
pip install pypiserver

# Run private index
pypi-server -p 8080 packages/

# Configure pip to use private index
pip install --index-url http://localhost:8080/simple/ mypackage

# Add to pip.conf
[global]
index-url = http://localhost:8080/simple/
trusted-host = localhost
```

---

## Real-World Scenarios: Managing Multiple Python Versions

- Tool: pyenv
- Install multiple Python versions
- Switch between versions
- Set local/global defaults
- Works with virtual environments

```bash
# Install pyenv (Linux/macOS)
curl https://pyenv.run | bash

# Install Python versions
pyenv install 3.7.12
pyenv install 3.8.12
pyenv install 3.9.7

# Set global Python version
pyenv global 3.8.12

# Set Python version for a directory
cd myproject
pyenv local 3.9.7

# List installed versions
pyenv versions

# Use with virtualenv
pyenv virtualenv 3.8.12 myproject-env
```

---

## Real-World Scenarios: Handling Binary Dependencies

- Some packages require compilation
- Platform-specific packages
- System dependencies (C libraries)
- Consider wheels, conda, or containers

```bash
# Install build tools (Ubuntu)
apt-get install build-essential python3-dev

# Install system libraries for common packages
apt-get install libpq-dev    # for psycopg2
apt-get install libxml2-dev  # for lxml

# Use binary wheels when possible
pip install --only-binary :all: numpy scipy pandas

# Consider conda for complex cases
conda install numpy scipy pandas

# Or use Docker with pre-built images
FROM python:3.8-buster
```

---

## Real-World Scenarios: Enterprise Environments

- Corporate proxies
- Custom package indexes
- Compliance requirements
- Airgapped networks
- License management

```bash
# Configure pip for proxy
pip config set global.proxy http://user:pass@proxy:8080

# Configure for private repo
pip config set global.index-url https://repo.company.com/pypi/simple
pip config set global.trusted-host repo.company.com

# Generate licenses report
pip install pip-licenses
pip-licenses --format=csv > licenses.csv

# For airgapped envs: download packages
pip download -r requirements.txt -d ./packages
# Transfer packages to airgapped env
pip install --no-index --find-links=./packages -r requirements.txt
```

---

## Real-World Scenarios: Monorepo Project Structure

- Multiple related packages in one repo
- Shared dependencies
- Development dependencies
- Testing across package boundaries

```tree
monorepo/
├── pyproject.toml (workspace config)
├── common/
│   ├── pyproject.toml
│   └── src/common/
├── service-a/
│   ├── pyproject.toml
│   └── src/service_a/
├── service-b/
│   ├── pyproject.toml
│   └── src/service_b/
└── tests/
    ├── integration/
    └── e2e/

# Tools that support this workflow:
# - poetry (with workspaces)
# - tox
# - hatch (multi-environment)
```

---

## Summary

## Key Takeaways
- Always use virtual environments
- Choose tools appropriate for your project
- Lock dependencies for applications
- Use version ranges for libraries
- Document your environment setup
- Follow consistent practices across team
- Consider the full lifecycle of dependencies

---

## Resources

## Further Learning
- Python Packaging User Guide: packaging.python.org
- Python Dependency Management Guide: realpython.com
- Tool documentation:
    - pip.pypa.io
    - pipenv.pypa.io
    - python-poetry.org
    - github.com/pypa/pip-tools
    - hatch.pypa.io
    - docs.conda.io

```python
# Remember:
"""Good environment management leads to:
- Reproducible environments
- Easier collaboration
- Faster onboarding
- Fewer "works on my machine" issues
- More reliable deployments
- Happier developers"""
```
