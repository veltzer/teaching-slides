# Packaging and Delivering Python Modules

## Overview
- Python packaging systems
- Creating distributable packages
- Building source distributions and wheels
- Publishing to PyPI and other repositories
- Creating custom repositories
- Binary distribution strategies
- API design and stability
- Documentation best practices

---

## Python Packaging Evolution

## Historical Timeline
- Pre-2000: Manual module distribution
- 2000: distutils added to standard library
- 2004: setuptools introduced as distutils enhancement
- 2012: wheel format introduced (PEP 427)
- 2016: pip becomes the default installer
- 2018: pyproject.toml standard (PEP 518)
- 2020+: Modern tools like poetry, hatch, flit

---

## Python Packaging Evolution

## Current State
- distutils (deprecated in Python 3.10)
- setuptools (still widely used)
- Modern packaging standards:
    - PEP 517/518: pyproject.toml-based builds
    - PEP 621: Project metadata in pyproject.toml
- Modern tools:
    - poetry, hatch, flit, setuptools_scm

```python
# Evolution of installation
# Old way
python setup.py install

# Current way
pip install .

# Modern way
pip install build twine
python -m build
twine upload dist/*
```

---

## distutils

## Introduction to distutils
- Original Python packaging system
- Part of the standard library
- Basis for many packaging tools
- Simple but limited functionality
- Deprecated as of Python 3.10

```python
# Basic setup.py with distutils
from distutils.core import setup

setup(
    name="mypackage",
    version="0.1",
    description="A simple package example",
    author="Your Name",
    author_email="your.email@example.com",
    py_modules=["mymodule"],
)
```

---

## distutils

## Limitations of distutils
- Limited dependency management
- No automatic dependency installation
- Minimal metadata support
- No binary distribution support
- Limited configuration options
- Deprecated in Python 3.10

```python
# Building with distutils
python setup.py build
python setup.py install
python setup.py sdist
```

---

## setuptools

## Introduction to setuptools
- Enhanced alternative to distutils
- De facto standard for Python packaging
- Rich feature set for package creation
- Extensive configuration options
- Backwards compatible with distutils

```python
# Basic setup.py with setuptools
from setuptools import setup, find_packages

setup(
    name="mypackage",
    version="0.1",
    description="A simple package example",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "numpy>=1.20.0",
    ],
)
```

---

## setuptools

## Key setuptools Features
- Automatic package discovery
- Dependency declaration and installation
- Entry points for plugins/scripts
- Development mode with `pip install -e .`
- Data file inclusion
- Version handling
- Test integration

```python
# More complete setup.py example
setup(
    name="mypackage",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["requests>=2.25.0"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "mycommand=mypackage.cli:main",
        ],
    },
)
```

---

## setuptools

## Project Structure with setuptools
- Standard layout for Python packages
- Source vs. distribution structure
- Package vs. module organization
- Namespace packages

```tree
mypackage/
├── LICENSE
├── README.md
├── setup.py
├── setup.cfg
├── MANIFEST.in
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── module1.py
│       └── subpackage/
│           ├── __init__.py
│           └── module2.py
└── tests/
    ├── __init__.py
    ├── test_module1.py
    └── test_module2.py
```

---

## setuptools

## setup.cfg Configuration
- Move setup.py configuration to setup.cfg
- Declarative configuration
- Cleaner and more maintainable
- Separate configuration from code

```ini
[metadata]
name = mypackage
version = 0.1.0
description = A simple package example
author = Your Name
author_email = your.email@example.com
license = MIT
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License

[options]
package_dir =
    = src
packages = find:
python_requires = >=3.6
install_requires =
    requests>=2.25.0
    numpy>=1.20.0

[options.packages.find]
where = src
```

---

## setuptools

## MANIFEST.in
- Controls which files are included in source distributions
- Not needed for wheels (which use include_package_data)
- Include non-Python files in your package
- Documentation, license, data files, etc.

```config
# MANIFEST.in example
include LICENSE
include README.md
include pyproject.toml
include requirements*.txt

recursive-include src/mypackage/data *
recursive-include docs *.md *.rst
recursive-exclude * __pycache__
recursive-exclude * *.py[co]
```

---

## Modern Packaging

## pyproject.toml
- New standard for Python packaging (PEP 518/621)
- Replaces setup.py, setup.cfg, MANIFEST.in
- Specifies build system requirements
- Configures build tools
- Declares project metadata
- Tool-specific configuration sections

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm>=6.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
description = "A simple package example"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
requires-python = ">=3.7"
dependencies = [
    "requests>=2.25.0",
    "numpy>=1.20.0",
]
```

---

## Modern Packaging

## Modern Packaging Tools

## setuptools + build
- setuptools remains the most common build backend
- build module provides standardized builder
- Simple, standardized approach
- Compatible with existing setups

```bash
# Install build tool
pip install build

# Build package (source and wheel)
python -m build

# Build specific formats
python -m build --sdist
python -m build --wheel
```

---

## Modern Packaging

## Modern Packaging Tools

## poetry
- Complete package management
- Dependency resolution
- Virtual environment management
- Publishing workflow
- Modern, intuitive interface

```bash
# Initialize a new package
poetry new mypackage

# Add dependencies
poetry add requests numpy

# Build package
poetry build

# Publish to PyPI
poetry publish
```

---

## Modern Packaging

## Modern Packaging Tools

## flit
- Simplest way to package Python modules
- Minimal configuration
- Auto-detection of metadata
- Quick publishing workflow
- Great for single-file modules

```bash
# Initialize flit project
flit init

# Build package
flit build

# Publish to PyPI
flit publish
```

---

## Modern Packaging

## Modern Packaging Tools

## hatch
- Modern Python project manager
- Standardized project structure
- Virtual environment management
- Build and publish workflow
- Plugin system for extensibility

```bash
# Create new project
hatch new mypackage

# Build package
hatch build

# Publish to PyPI
hatch publish
```

---

## Package Formats

## Source Distributions (sdist)
- Contains source code and build instructions
- Platform-independent
- Requires build process on installation
- Contains tests, docs, and other development files
- Traditional format for Python distribution

```bash
# Building source distribution
python -m build --sdist

# Result: mypackage-0.1.0.tar.gz
# Contains:
# - All Python source files
# - setup.py, pyproject.toml, etc.
# - Files specified in MANIFEST.in
```

---

## Package Formats

## Wheel Distributions
- Pre-built distribution format
- Faster installation (no build step)
- Platform-specific or pure Python
- Smaller than source distributions
- Standard format since PEP 427

```bash
# Building wheel distribution
python -m build --wheel

# Universal pure Python wheel:
# mypackage-0.1.0-py3-none-any.whl

# Platform-specific wheel:
# mypackage-0.1.0-cp39-cp39-linux_x86_64.whl
```

---

## Package Formats

## Wheel Anatomy
- Wheel file naming convention
- Internal structure
- Metadata format
- Installation process

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="310" font-family="monospace">
  <!-- Wheel filename -->
  <text x="10" y="30" font-size="13" font-weight="bold" fill="#333" font-family="sans-serif">Wheel Filename Anatomy:</text>
  <text x="10" y="55" font-size="14" fill="#222">mypackage-0.1.0-cp39-cp39-linux_x86_64.whl</text>
  <!-- bracket lines -->
  <!-- Distribution name: chars 0-8 "mypackage" -->
  <line x1="10"  y1="60" x2="10"  y2="75" stroke="#555" stroke-width="1"/>
  <line x1="10"  y1="75" x2="120" y2="75" stroke="#555" stroke-width="1"/>
  <text x="125" y="78" font-size="12" fill="#555" font-family="sans-serif">Distribution name</text>
  <!-- Version: 10-14 "0.1.0" -->
  <line x1="122" y1="60" x2="122" y2="90" stroke="#555" stroke-width="1"/>
  <line x1="122" y1="90" x2="168" y2="90" stroke="#555" stroke-width="1"/>
  <text x="173" y="93" font-size="12" fill="#555" font-family="sans-serif">Version</text>
  <!-- Python tag cp39 -->
  <line x1="170" y1="60" x2="170" y2="105" stroke="#555" stroke-width="1"/>
  <line x1="170" y1="105" x2="204" y2="105" stroke="#555" stroke-width="1"/>
  <text x="209" y="108" font-size="12" fill="#555" font-family="sans-serif">Python tag (CPython 3.9)</text>
  <!-- ABI tag cp39 -->
  <line x1="206" y1="60" x2="206" y2="120" stroke="#555" stroke-width="1"/>
  <line x1="206" y1="120" x2="240" y2="120" stroke="#555" stroke-width="1"/>
  <text x="245" y="123" font-size="12" fill="#555" font-family="sans-serif">ABI tag</text>
  <!-- Python impl -->
  <line x1="242" y1="60" x2="242" y2="135" stroke="#555" stroke-width="1"/>
  <line x1="242" y1="135" x2="355" y2="135" stroke="#555" stroke-width="1"/>
  <text x="360" y="138" font-size="12" fill="#555" font-family="sans-serif">Python implementation</text>
  <!-- Platform linux_x86_64 -->
  <line x1="357" y1="60" x2="357" y2="150" stroke="#555" stroke-width="1"/>
  <line x1="357" y1="150" x2="468" y2="150" stroke="#555" stroke-width="1"/>
  <text x="473" y="153" font-size="12" fill="#555" font-family="sans-serif">Platform</text>
  <!-- Internal structure -->
  <text x="10" y="185" font-size="13" font-weight="bold" fill="#333" font-family="sans-serif">Internal Structure:</text>
  <rect x="10" y="195" width="300" height="110" fill="#f0f4f8" stroke="#333" stroke-width="1.5" rx="4"/>
  <text x="20" y="215" font-size="13" fill="#222">mypackage/</text>
  <text x="20" y="233" font-size="13" fill="#222">mypackage-0.1.0.dist-info/</text>
  <text x="30" y="251" font-size="12" fill="#555">  ├── METADATA</text>
  <text x="30" y="267" font-size="12" fill="#555">  ├── WHEEL</text>
  <text x="30" y="283" font-size="12" fill="#555">  ├── RECORD</text>
  <text x="30" y="299" font-size="12" fill="#555">  └── entry_points.txt</text>
</svg>

---

## Package Formats

## When to Use Which Format
- Source distributions:
    - Distribution to other developers
    - When compilation needs local customization
    - When you need to include development files
- Wheel distributions:
    - Distribution to end users
    - Faster, simpler installation
    - Avoiding build-time dependencies
    - Binary extensions

```bash
# Best practice: build and upload both
python -m build  # Builds both sdist and wheel
twine upload dist/*  # Upload both to PyPI
```

---

## Publishing Packages

## PyPI Overview
- Python Package Index (pypi.org)
- Official public repository
- Over 350,000 packages
- Free hosting for open source projects
- Supports multiple release versions
- Supports source and wheel distributions

---

## Publishing Packages

## Preparing for Publication
- Choose appropriate name (check availability)
- Prepare required metadata
- Create README and documentation
- Choose a license
- Create a release on version control system
- Build distributions

```python
# Required metadata for PyPI
name = "mypackage"
version = "0.1.0"
description = "A brief description"
author = "Your Name"
author_email = "your.email@example.com"
url = "https://github.com/yourusername/mypackage"
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
```

---

## Publishing Packages

## Using twine
- Standard tool for uploading to PyPI
- Securely authenticates to PyPI
- Verifies distributions before upload
- Supports TestPyPI for testing
- Works with any packaging system

```bash
# Install twine
pip install twine

# Check distribution files
twine check dist/*

# Upload to TestPyPI first
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Upload to PyPI
twine upload dist/*

# Using stored credentials
twine upload --config-file .pypirc dist/*
```

---

## Publishing Packages

## PyPI Configuration with .pypirc
- Store PyPI credentials
- Configure multiple repositories
- Define upload destinations
- Simplify twine commands

```ini
# ~/.pypirc
[distutils]
index-servers =
    pypi
    testpypi
    private

[pypi]
username = __token__
password = pypi-AgENdGVz...

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-AgENdGVz...

[private]
repository = https://private.company.com/simple
username = your_username
password = your_password
```

---

## Publishing Packages

## Testing Your Published Package
- Install from TestPyPI first
- Verify package structure
- Test functionality
- Check dependencies are correctly specified
- Ensure documentation is correct

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ mypackage

# Test in a fresh environment
python -m venv test_env
source test_env/bin/activate
pip install mypackage
python -c "import mypackage; print(mypackage.__version__)"

# If all looks good, publish to real PyPI
twine upload dist/*
```

---

## Private Package Repositories

## Why Use a Private Repository?
- Host proprietary code
- Control over available packages
- Airgapped/isolated environments
- Custom package governance
- Internal sharing within organization
- Faster installations on local network

---

## Private Package Repositories

## PyPI Server Options

## PyPI-Server
- Simple, lightweight PyPI server
- Easy to set up and use
- Support for package uploads
- Basic authentication

```bash
# Install PyPI-Server
pip install pypiserver

# Run server
pypi-server -p 8080 /path/to/packages

# Upload packages
twine upload --repository-url http://localhost:8080/ dist/*

# Install from private repo
pip install --index-url http://localhost:8080/simple/ mypackage
```

---

## Private Package Repositories

## PyPI Server Options

## Artifactory/Nexus/DevPi
- Enterprise-grade package repositories
- Advanced security features
- Multiple repository types (not just Python)
- Proxying public PyPI
- Fine-grained permissions
- Storage policies and quotas

```bash
# DevPi example
pip install devpi-server devpi-client
devpi-server --init
devpi-server --start
devpi use http://localhost:3141
devpi login root --password=''
devpi index -c dev
devpi use root/dev
devpi upload
```

---

## Private Package Repositories

## Using Private Repositories
- Configure pip to use private repo
- Authenticate with credentials
- Upload packages with twine
- Install packages with pip
- Use in CI/CD pipelines

```ini
# pip.conf or pip.ini
[global]
index-url = https://private.company.com/simple
trusted-host = private.company.com

# requirements.txt with explicit index
--index-url https://private.company.com/simple
--trusted-host private.company.com
mypackage==1.0.0
```

---

## Binary Distributions

## Why Package as Binary?
- End-user simplicity
- Avoid installation issues
- Include non-Python dependencies
- Protect source code
- Provide standalone applications
- Consistent runtime environment

---

## Binary Distributions

## Creating Binary Distributions

## PyInstaller
- Bundles Python app into standalone executable
- Cross-platform support
- Handles dependencies automatically
- No Python installation required for end users
- Support for one-file and one-directory modes

```bash
# Install PyInstaller
pip install pyinstaller

# Create one-file executable
pyinstaller --onefile myscript.py

# Create one-directory bundle
pyinstaller --name myapp myscript.py

# Customize icon, splash screen, etc.
pyinstaller --onefile --windowed --icon=myicon.ico myscript.py
```

---

## Binary Distributions

## Creating Binary Distributions

## cx_Freeze
- Creates standalone executables
- Cross-platform
- More customizable than PyInstaller
- Works well with complex applications
- Better support for Windows services

```python
# setup.py for cx_Freeze
from cx_Freeze import setup, Executable

setup(
    name="myapp",
    version="0.1",
    description="My Application",
    executables=[Executable("myscript.py", base="Win32GUI")],
    options={
        "build_exe": {
            "packages": ["os", "numpy"],
            "include_files": ["data/"]
        }
    }
)

# Build command
# python setup.py build
```

---

## Binary Distributions

## Creating Binary Distributions

## py2exe/py2app
- Windows-specific (py2exe)
- macOS-specific (py2app)
- Mature and well-tested
- Deep integration with target platforms
- Support for platform-specific features

```python
# setup.py for py2exe
from distutils.core import setup
import py2exe

setup(
    name="myapp",
    version="1.0",
    windows=[{"script": "myscript.py"}],
    options={"py2exe": {
        "compressed": 1,
        "bundle_files": 1,
        "includes": ["numpy", "pandas"]
    }}
)

# Build command
# python setup.py py2exe
```

---

## Binary Distributions

## Creating Binary Distributions

## Docker Containers
- Package application with Python runtime
- Consistent environment across systems
- Excellent for web applications and services
- DevOps friendly deployment
- Works with orchestration systems

```dockerfile
# Dockerfile
FROM python:3.9-slim

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

## API Design and Stability

## Principles of Good API Design
- Consistency in naming and behavior
- Simplicity in common cases
- Progressive disclosure of complexity
- Backward compatibility
- Well-defined interfaces
- Comprehensive documentation
- Follow Python's conventions (PEP 8)

---

## API Design and Stability

## API Components
- Public functions and classes
- Parameters and return values
- Exceptions and error handling
- Module structure
- Import paths
- Extension points
- Configuration options

```python
# Good API design example
def process_data(data, normalize=True, output_format="dict"):
    """
    Process input data and return results.

    Args:
        data: Input data to process
        normalize: Whether to normalize values (default: True)
        output_format: Format for output, 'dict' or 'list' (default: 'dict')

    Returns:
        Processed data in requested format

    Raises:
        ValueError: If output_format is invalid
    """
    # Implementation
```

---

## API Design and Stability

## Versioning and Compatibility
- Semantic versioning (MAJOR.MINOR.PATCH)
- Explicit deprecation process
- Transition periods for breaking changes
- Compatibility layers
- Feature flags for new functionality

```python
import warnings

def old_function(arg1, arg2):
    """Deprecated: Use new_function instead."""
    warnings.warn(
        "old_function is deprecated, use new_function instead",
        DeprecationWarning,
        stacklevel=2
    )
    return new_function(arg1, arg2)

def new_function(arg1, arg2, arg3=None):
    # New implementation
    pass
```

---

## API Design and Stability

## Private vs. Public API
- Mark private internals with underscore
- Document what's public and what's private
- Don't rely on implementation details
- Be careful about exposing internal state
- Use `__all__` to define public API

```python
# In __init__.py
__all__ = ["func1", "func2", "Class1"]

# Public API
def func1():
    """Public function, part of stable API."""
    return _internal_helper()

# Private implementation
def _internal_helper():
    """Private function, not part of public API."""
    return "Internal result"
```

---

## API Design and Stability

## Interface Contracts
- Document parameter types and return values
- Define error conditions and exceptions
- Consider using Python type hints
- Document behavior guarantees
- Be explicit about what can change

```python
from typing import List, Dict, Union, Optional

def process_items(
    items: List[Dict[str, Union[str, int]]],
    config: Optional[Dict[str, str]] = None
) -> List[Dict[str, str]]:
    """
    Process a list of items according to configuration.

    The structure of input items must include 'id' and 'value' keys.
    Output items will contain 'id' and 'result' keys.

    Args:
        items: List of items to process
        config: Optional configuration dictionary

    Returns:
        List of processed items

    Raises:
        ValueError: If any item is missing required keys
    """
    # Implementation
```

---

## Documenting Your Module

## Documentation Types
- API reference documentation
- Tutorials and guides
- Examples and recipes
- Architecture overview
- Development and contribution guides
- Change logs and release notes
- FAQ and troubleshooting

---

## Documenting Your Module

## Docstrings
- Document modules, classes, methods, functions
- Follow standard formats (Google, NumPy, reStructuredText)
- Include parameters, return values, exceptions
- Add examples where helpful
- Reference related functionality

```python
def calculate_statistics(values, include_outliers=True):
    """
    Calculate basic statistics for a list of values.

    Args:
        values: List of numeric values
        include_outliers: Whether to include outliers (default: True)

    Returns:
        dict: Dictionary containing 'mean', 'median', and 'std_dev'

    Raises:
        ValueError: If values is empty or contains non-numeric items

    Examples:
        >>> calculate_statistics([1, 2, 3, 4, 5])
        {'mean': 3.0, 'median': 3.0, 'std_dev': 1.58}
    """
    # Implementation
```

---

## Documenting Your Module

## README Files
- First documentation users see
- Quick start guide
- Installation instructions
- Basic usage examples
- Links to full documentation
- License information
- Support information

```markdown
# MyPackage

A Python library for processing data with efficiency and elegance.

## Installation

```bash
pip install mypackage
```

## Quick Start

```python
import mypackage

# Process some data
result = mypackage.process_data([1, 2, 3])
print(result)
```

## Documentation

Full documentation is available at https://mypackage.readthedocs.io

## License

MIT License

---

## Documenting Your Module

## Documentation Tools

## Sphinx
- Standard documentation generator for Python
- reStructuredText format
- Automatic API documentation from docstrings
- Multiple output formats (HTML, PDF, etc.)
- Extensible with plugins

```bash
# Install Sphinx
pip install sphinx

# Initialize documentation
sphinx-quickstart docs

# Build documentation
cd docs
make html
```

---

## Documenting Your Module

## Documentation Tools

## MkDocs
- Simpler alternative to Sphinx
- Markdown format
- Clean, modern themes
- Easy to set up and use
- Popular with modern Python projects

```yaml
# mkdocs.yml
site_name: MyPackage Documentation
theme: material
nav:
  - Home: index.md
  - Installation: installation.md
  - User Guide: user-guide.md
  - API Reference: api.md
  - FAQ: faq.md

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          selection:
            inherited_members: true
```

---

## Documenting Your Module

## Hosting Documentation

## ReadTheDocs
- Free hosting for open source projects
- Automatic builds from GitHub/GitLab
- Versioned documentation
- Search functionality
- PDF/EPUB downloads

```yaml
# .readthedocs.yml
version: 2

build:
  os: ubuntu-20.04
  tools:
    python: "3.9"

python:
  install:
    - method: pip
      path: .
      extra_requirements:
        - docs

sphinx:
  configuration: docs/conf.py
```

---

## Distributing Documentation

## Documentation Distribution
- Include in source distributions
- Host online (ReadTheDocs, GitHub Pages)
- Package with application
- Offline access options
- Versioned documentation

```python
# setup.py
setup(
    # ... other parameters ...
    extras_require={
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "sphinx-autodoc-typehints>=1.12.0",
        ],
    },
)

# Install with docs dependencies
# pip install -e ".[docs]"
```

---

## Practical Example: Complete Package

## Project Structure
```tree
mypackage/
├── LICENSE
├── README.md
├── CHANGELOG.md
├── pyproject.toml
├── docs/
│   ├── conf.py
│   ├── index.rst
│   └── api.rst
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── core.py
│       └── cli.py
└── tests/
    ├── __init__.py
    └── test_core.py
```

---

## Practical Example: Complete Package

## pyproject.toml
```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
dynamic = ["version"]
description = "An example Python package"
readme = "README.md"
authors = [{name = "Your Name", email = "your.email@example.com"}]
license = {text = "MIT"}
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
requires-python = ">=3.7"
dependencies = [
    "requests>=2.25.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = ["pytest", "black", "flake8"]
docs = ["sphinx", "sphinx-rtd-theme"]

[project.scripts]
mypackage-cli = "mypackage.cli:main"

[tool.setuptools_scm]
write_to = "src/mypackage/_version.py"
```

---

## Practical Example: Complete Package

## __init__.py
```python
"""
MyPackage - An example Python package.

This package demonstrates best practices for Python packaging,
documentation, and API design.
"""

from ._version import version as __version__
from .core import process_data, calculate_statistics

__all__ = ["__version__", "process_data", "calculate_statistics"]
```

---

## Practical Example: Complete Package

## Building and Publishing
```bash
# Ensure build tools are installed
pip install build twine

# Build distributions
python -m build

# Check distributions
twine check dist/*

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ mypackage

# Upload to PyPI
twine upload dist/*
```

---

## Summary

## Key Takeaways
- Choose appropriate packaging tools for your project
- Build both source and wheel distributions
- Design stable, well-documented APIs
- Follow versioning best practices
- Document thoroughly with appropriate tools
- Consider binary distribution for end-user applications
- Maintain compatibility through careful design

---

## Resources

## Further Reading
- Python Packaging User Guide: packaging.python.org
- Setuptools Documentation: setuptools.pypa.io
- Python Packaging Authority (PyPA): pypa.io
- Python Enhancement Proposals (PEPs): www.python.org/dev/peps/
- "How to Package Your Python Code" (Real Python)
- "Packaging a python library" (PyOpenSci)
