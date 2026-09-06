---
tags:
  - languages:python
level: advanced
category: language
audience:
  - audiences:developers

---

# C and Python Integration

## Overview
- Bridging Python and C code
- Python's C API
- Building C extensions
- Alternative methods for C integration
- Performance considerations
- Real-world applications and examples

---

## Python-C Integration Methods

![Python C integration methods overview](svg/courses/languages/python/advanced-python/15_c_integration/python_c_extension.svg)

---

## Why Integrate C with Python?: Common Motivations

- Performance optimization for bottlenecks
- Access to C libraries and system features
- Memory management control
- Real-time requirements and latency reduction
- Specialized hardware access
- Legacy code integration

```python
# Python code with performance bottleneck
def compute_intensive_function(data, iterations):
    result = 0
    for i in range(iterations):
        for item in data:
            result += process(item)
    return result

# Could be replaced with C implementation for speed
```

---

## Why Integrate C with Python?: Performance Comparison

- Python: High-level, easy to write, slower execution
- C: Low-level, more complex, faster execution
- Integration combines the best of both worlds
- Potential speedups of 10-100x for CPU-bound code
- Minimal benefit for I/O-bound operations

```misc
Task: Sum of squares of 10 million integers

Python:
sum(x*x for x in range(10000000))  # ~1.2 seconds

C equivalent:
// C implementation        # ~0.02 seconds

Potential speedup: ~60x
```

---

## Why Integrate C with Python?: When C Integration Makes Sense

- CPU-bound bottlenecks identified through profiling
- Algorithms with heavy numerical computation
- Bit-level operations and manipulations
- Direct hardware interaction
- Hard real-time requirements
- Memory-intensive operations

---

## Why Integrate C with Python?: When C Integration Doesn't Make Sense

- I/O-bound tasks (network, disk)
- Simple algorithms with low computational intensity
- Where code readability and maintenance is critical
- Early development and prototyping
- When numpy/pandas/scipy already solves the problem
- Tasks without clear performance bottlenecks

---

## Integration Methods Overview

## Main Approaches to C/Python Integration
1. **Python C API**: Direct C extensions using Python's C API
1. **ctypes**: Python standard library for calling C functions
1. **CFFI**: C Foreign Function Interface for Python
1. **Cython**: Python-like language compiled to C
1. **SWIG**: Simplified Wrapper and Interface Generator
1. **pybind11**: C++11 header-only library

| Method | Complexity | Performance | Flexibility |
|--------|-----------|-------------|-------------|
| Python C API | High | High | High |
| ctypes | Low | Medium | Medium |
| CFFI | Medium | High | High |
| Cython | Low | High | High |
| SWIG | Medium | High | Medium |
| pybind11 | Medium | High | High (C++) |

---

## The Python C API: What is the Python C API?

- Low-level interface to Python interpreter
- Allows C code to interact with Python objects
- Provides functions for creating and manipulating Python objects
- Creates extension modules loadable by Python
- Requires understanding Python's internals
- Offers maximum performance and flexibility

```c
// Simplified C API example
#include <Python.h>

static PyObject* c_function(PyObject* self, PyObject* args) {
    int input;
    if (!PyArg_ParseTuple(args, "i", &input))
        return NULL;

    int result = input * 2;
    return Py_BuildValue("i", result);
}

// Function definition and module initialization code...
```

---

## The Python C API: Python C API Core Components

- Python Objects (`PyObject*`)
- Reference counting
- Type system and conversion functions
- Module creation and initialization
- Error handling mechanisms
- Python interpreter interaction

```c
// Core Python C API patterns
PyObject* py_list = PyList_New(3);                 // Create objects
PyList_SetItem(py_list, 0, PyLong_FromLong(1));    // Modify objects

long value = PyLong_AsLong(PyList_GetItem(py_list, 0));  // Extract data

Py_INCREF(py_list);  // Reference counting
Py_DECREF(py_list);  // Must be balanced to avoid memory leaks
```

---

## Creating a C Extension: Basic Extension Module Structure

- Header includes
- Function implementations
- Method table
- Module definition
- Module initialization

```c
#include <Python.h>

// Function implementation
static PyObject* hello_world(PyObject* self, PyObject* args) {
    printf("Hello from C!\n");
    Py_RETURN_NONE;
}

// Method table
static PyMethodDef HelloMethods[] = {
    {"hello", hello_world, METH_NOARGS, "Print hello from C."},
    {NULL, NULL, 0, NULL}  // Sentinel
};

// Module definition (Python 3)
static struct PyModuleDef hellomodule = {
    PyModuleDef_HEAD_INIT,
    "hello",      // Module name
    "Hello module documentation", // Module docstring
    -1,           // Module state
    HelloMethods  // Method table
};

// Module initialization function
PyMODINIT_FUNC PyInit_hello(void) {
    return PyModule_Create(&hellomodule);
}
```

---

## Creating a C Extension: Extension with Parameters

- Parse arguments with `PyArg_ParseTuple`
- Process data in C
- Return Python objects
- Handle errors properly

```c
// Function that accepts and returns values
static PyObject* add_integers(PyObject* self, PyObject* args) {
    int a, b;

    // Parse arguments ("ii" means two integers)
    if (!PyArg_ParseTuple(args, "ii", &a, &b)) {
        return NULL;  // Error already set by PyArg_ParseTuple
    }

    // Perform calculation
    long sum = (long)a + (long)b;

    // Return result as Python object
    return PyLong_FromLong(sum);
}

// Method table entry
{"add", add_integers, METH_VARARGS, "Add two integers."}
```

---

## Creating a C Extension: Building Extensions with setup.py

- Uses distutils or setuptools
- Defines C source files
- Handles compilation details
- Creates installable package
- Cross-platform approach

```python
# setup.py
from setuptools import setup, Extension

module = Extension('hello',
                   sources=['hellomodule.c'])

setup(name='HelloModule',
      version='1.0',
      description='Simple C extension example',
      ext_modules=[module])
```

```bash
# Build and install
python setup.py build
python setup.py install

# Or develop mode
pip install -e .
```

---

## Creating a C Extension: Extension Module Layout

- Single C file for simple modules
- Multiple C files for complex modules
- Header files for shared declarations
- Include files for common functions
- Initialization file containing module definition

```tree
mymodule/
├── setup.py           # Build script
├── mymodule.c         # Main module implementation
├── mymodule_utils.c   # Utility functions
├── mymodule_utils.h   # Shared declarations
└── README.md          # Documentation
```

---

## Working with Python Objects: PyObject and Reference Counting

- All Python objects are represented as `PyObject*`
- Reference counting manages memory
- Must increment/decrement reference counts
- Improper handling leads to leaks or crashes
- Macros for reference count management

```c
// Reference counting basics
PyObject* list = PyList_New(0);  // New reference (refcount = 1)

// Incrementing reference count
Py_INCREF(list);                 // Now refcount = 2

// Decrementing reference count
Py_DECREF(list);                 // Now refcount = 1

// When refcount reaches 0, object is deallocated
Py_DECREF(list);                 // Object is freed

// Common functions that affect reference counts:
// PyObject_GetAttr() -> New reference
// PyList_GetItem()   -> Borrowed reference
// PyTuple_GetItem()  -> Borrowed reference
// PyDict_GetItem()   -> Borrowed reference
```

---

## Working with Python Objects: Borrowed vs. New References

- **Borrowed reference**: Pointer to an object you don't own
- **New reference**: Pointer to an object you own (must Py_DECREF)
- API functions may return either type
- Documentation specifies reference type
- Critical for memory management

```c
// New reference - you must DECREF when done
PyObject* new_ref = PyLong_FromLong(42);
// ... use new_ref ...
Py_DECREF(new_ref);

// Borrowed reference - do not DECREF
PyObject* list = PyList_New(1);
PyList_SetItem(list, 0, PyLong_FromLong(42));  // Steals reference
PyObject* borrowed = PyList_GetItem(list, 0);  // Borrowed

// If you need to keep a borrowed reference:
Py_INCREF(borrowed);
// ... use borrowed ...
Py_DECREF(borrowed);
Py_DECREF(list);
```

---

## Working with Python Objects: Converting Python to C Types

- Each Python type has conversion functions
- Extract C values from Python objects
- Check for errors during conversion
- Handle type mismatches gracefully

```c
// Extract integers
long c_long = PyLong_AsLong(py_int);
if (c_long == -1 && PyErr_Occurred()) {
    // Handle error
}

// Extract floats
double c_double = PyFloat_AsDouble(py_float);

// Extract strings (Python 3)
const char* c_str = PyUnicode_AsUTF8(py_unicode);
if (c_str == NULL) {
    // Handle error
}

// Extract booleans
int c_bool = PyObject_IsTrue(py_bool);
```

---

## Working with Python Objects: Creating Python Objects from C Types

- Build Python objects from C values
- Create complex structures (lists, tuples, dicts)
- Check for allocation failures
- Manage references correctly

```c
// Create Python objects
PyObject* py_long = PyLong_FromLong(42);
PyObject* py_float = PyFloat_FromDouble(3.14159);
PyObject* py_str = PyUnicode_FromString("hello");

// Create a list
PyObject* py_list = PyList_New(3);
PyList_SetItem(py_list, 0, PyLong_FromLong(1));      // Steals reference
PyList_SetItem(py_list, 1, PyLong_FromLong(2));
PyList_SetItem(py_list, 2, PyLong_FromLong(3));

// Create a dictionary
PyObject* py_dict = PyDict_New();
PyDict_SetItemString(py_dict, "key", PyLong_FromLong(42));  // Increments reference
```

---

## Working with Python Objects: PyArg_ParseTuple Format Codes

- `i` - int
- `l` - long
- `d` - double
- `s` - string (char*)
- `O` - PyObject*
- `|` - Optional arguments start
- `$` - Keyword-only arguments start (Python 3)
- Many other specialized codes

```c
static PyObject* example_function(PyObject* self, PyObject* args) {
    int required1;
    const char* required2;
    PyObject* required3;
    int optional1 = 0;
    const char* optional2 = "default";

    // Format: "isO|is" - int, string, object, optional int, optional string
    if (!PyArg_ParseTuple(args, "isO|is",
                          &required1, &required2, &required3,
                          &optional1, &optional2)) {
        return NULL;  // Exception already set
    }

    // Use the parameters...
    Py_RETURN_NONE;
}
```

---

## Working with Python Objects: Py_BuildValue Format Codes

- Similar to PyArg_ParseTuple, but for returning values
- Creates Python objects from C values
- Builds tuples for multi-value returns
- Handles reference counting automatically

```c
// Return a single integer
return Py_BuildValue("i", 42);

// Return a string
return Py_BuildValue("s", "hello");

// Return a tuple (i, s)
return Py_BuildValue("is", 42, "hello");

// Return a list [1, 2, 3]
return Py_BuildValue("[iii]", 1, 2, 3);

// Return a dictionary {"key": "value"}
return Py_BuildValue("{ss}", "key", "value");

// Return None
return Py_BuildValue("");  // or Py_RETURN_NONE;
```

---

## Error Handling in C Extensions: Setting and Checking Errors

- Set exceptions with PyErr_SetString/PyErr_SetObject
- Check for errors with PyErr_Occurred
- Return NULL from functions when errors occur
- Clear errors with PyErr_Clear
- Propagate errors up the call stack

```c
// Setting an error
PyErr_SetString(PyExc_ValueError, "Invalid input value");
return NULL;

// Setting a more detailed error
PyObject* error_value = Py_BuildValue("(is)", 42, "error details");
PyErr_SetObject(PyExc_ValueError, error_value);
Py_DECREF(error_value);
return NULL;

// Checking for errors
if (PyErr_Occurred()) {
    // Handle or propagate the error
    return NULL;
}

// Clearing errors
PyErr_Clear();
```

---

## Error Handling in C Extensions: Common Exception Types

- `PyExc_Exception`: Base exception
- `PyExc_ValueError`: Invalid argument value
- `PyExc_TypeError`: Invalid argument type
- `PyExc_IndexError`: Index out of range
- `PyExc_KeyError`: Key not found
- `PyExc_MemoryError`: Memory allocation failed
- `PyExc_RuntimeError`: Generic runtime error

```c
// Type error
if (!PyLong_Check(arg)) {
    PyErr_SetString(PyExc_TypeError, "Expected an integer");
    return NULL;
}

// Value error
if (value < 0) {
    PyErr_SetString(PyExc_ValueError, "Value must be non-negative");
    return NULL;
}

// Index error
if (index >= size) {
    PyErr_SetString(PyExc_IndexError, "Index out of range");
    return NULL;
}
```

---

## Error Handling in C Extensions: Exception Handling in C

- C doesn't have built-in exceptions
- Use error status codes and NULL returns
- Check errors after each API call
- Properly clean up resources on error paths
- Ensure consistent error propagation

```c
static PyObject* error_handling_example(PyObject* self, PyObject* args) {
    PyObject *list, *item, *result = NULL;

    // Parse arguments
    if (!PyArg_ParseTuple(args, "O", &list))
        return NULL;  // Exception already set

    // Verify object type
    if (!PyList_Check(list)) {
        PyErr_SetString(PyExc_TypeError, "Expected a list");
        return NULL;
    }

    // Allocate resources
    result = PyList_New(0);
    if (result == NULL)
        return NULL;  // Memory error already set

    // Process data with error handling
    for (Py_ssize_t i = 0; i < PyList_Size(list); i++) {
        item = PyList_GetItem(list, i);  // Borrowed reference

        // Process item...
        if (error_occurred) {
            Py_DECREF(result);  // Clean up
            return NULL;        // Propagate error
        }
    }

    return result;
}
```

---

## Building and Installing Extensions: Setuptools Configuration

- More advanced than distutils
- Better dependency handling
- Development mode with `pip install -e .`
- Handles compiler flags and linking
- Cross-platform compatibility features

```python
# setup.py with advanced configuration
from setuptools import setup, Extension
import numpy as np

module = Extension('mymodule',
                  sources=['src/mymodule.c', 'src/utilities.c'],
                  include_dirs=[np.get_include(), 'include'],
                  libraries=['m'],  # Link with math library
                  extra_compile_args=['-O3', '-march=native'],
                  extra_link_args=[],
                  define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')])

setup(
    name='MyModule',
    version='1.0',
    description='Advanced C extension example',
    ext_modules=[module],
    install_requires=['numpy'],
    python_requires='>=3.6',
)
```

---

## Building and Installing Extensions: Cross-Platform Considerations

- Different compilers (MSVC on Windows, GCC/Clang on Unix)
- Platform-specific headers and libraries
- Conditional compilation for OS-specific code
- Binary wheel distribution vs. source distribution
- Continuous integration setups

```python
# Cross-platform setup.py
import platform
from setuptools import setup, Extension

sources = ['common.c', 'module.c']
compile_args = []
link_args = []
libraries = []

if platform.system() == 'Windows':
    compile_args.append('/O2')
    # Windows-specific settings
elif platform.system() == 'Linux':
    compile_args.extend(['-O3', '-march=native'])
    libraries.append('rt')  # Linux-specific library
elif platform.system() == 'Darwin':  # macOS
    compile_args.extend(['-O3', '-march=native'])
    # macOS-specific settings

module = Extension('mymodule',
                  sources=sources,
                  extra_compile_args=compile_args,
                  extra_link_args=link_args,
                  libraries=libraries)

setup(name='MyModule', ext_modules=[module])
```

---

## Building and Installing Extensions: Using a C Compiler on Different Platforms

- Windows: Visual C++ (MSVC) - version must match Python's compiler
- Linux: GCC or Clang
- macOS: Clang (usually via XCode tools)
- Ensure all build dependencies are installed
- May need specific environment variables set

```bash
# Linux/macOS build
pip install -e .

# Windows build with specific compiler
set VS90COMNTOOLS=C:\Program Files\Microsoft Visual Studio 9.0\Common7\Tools\
pip install -e .

# Explicit Python build command
python setup.py build_ext --inplace

# Cross-platform compilation (Linux)
CC=x86_64-w64-mingw32-gcc python setup.py build_ext
```

---

## Alternative Approach: ctypes: What is ctypes?

- Standard library module for calling C functions
- No compilation needed for Python side
- Loads existing shared libraries (.dll, .so, .dylib)
- Creates Python interfaces to C functions
- Less overhead than C API for simple cases
- Easier to use but less flexible

```python
# Basic ctypes example
import ctypes

# Load the C library
libc = ctypes.CDLL('libc.so.6')  # Linux
# libc = ctypes.CDLL('msvcrt.dll')  # Windows

# Call a C function
libc.printf(b"Hello, %s!\n", b"world")

# Call with automatic type conversion
libc.time(None)  # Call time(NULL)

# Define specific argument and return types
libc.strlen.argtypes = [ctypes.c_char_p]
libc.strlen.restype = ctypes.c_size_t
length = libc.strlen(b"Python")
print(f"Length: {length}")  # 6
```

---

## Alternative Approach: ctypes: Data Types in ctypes

- Primitives: c_int, c_double, c_char, c_bool, etc.
- Pointers: POINTER(type), c_char_p, c_void_p
- Arrays: (c_int * 10)(), create_string_buffer()
- Structures: Structure, Union
- Function pointers: CFUNCTYPE

```python
import ctypes

# Basic types
i = ctypes.c_int(42)
f = ctypes.c_float(3.14)
s = ctypes.create_string_buffer(b"hello")

# Arrays
int_array = (ctypes.c_int * 5)(1, 2, 3, 4, 5)
print(int_array[2])  # 3

# Structures
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]

p = Point(10, 20)
print(f"Point: ({p.x}, {p.y})")
```

---

## Alternative Approach: ctypes: Creating Your Own Shared Library

- Write C functions with proper exports
- Compile as shared library (.so, .dll, .dylib)
- Load and use with ctypes in Python
- Easier integration for existing C code

```c
// mylib.c
#include <stdio.h>

// For Windows
#ifdef _WIN32
#define EXPORT __declspec(dllexport)
#else
#define EXPORT
#endif

EXPORT int add(int a, int b) {
    return a + b;
}

EXPORT double multiply(double a, double b) {
    return a * b;
}

// Compile (Linux): gcc -shared -fPIC -o mylib.so mylib.c
// Compile (Windows): gcc -shared -o mylib.dll mylib.c
```

---

## Creating Your Own Shared Library: Loading from Python

```python
# Using the compiled library
import ctypes
import os

# Load library from current directory
libpath = os.path.join(os.path.dirname(__file__), "mylib")
if os.name == 'nt':  # Windows
    lib = ctypes.CDLL(libpath + ".dll")
else:  # Linux/Mac
    lib = ctypes.CDLL(libpath + ".so")

result = lib.add(5, 3)
print(f"5 + 3 = {result}")  # 8
```

---

## Alternative Approach: ctypes: Callbacks with ctypes

- Pass Python functions to C code
- Define function prototype with CFUNCTYPE
- Enables bidirectional integration
- Manage GIL for threaded applications
- Useful for libraries with callback patterns

```python
import ctypes

# Define callback type: int func(int, int)
CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)

# Python function to use as callback
def py_compare(a, b):
    return a - b

# Create callback object from Python function
compare_callback = CMPFUNC(py_compare)

# Load C library with qsort
libc = ctypes.CDLL('libc.so.6')  # Linux

# Create array to sort
arr = (ctypes.c_int * 5)(5, 1, 3, 2, 4)

# Call qsort with our callback
libc.qsort(arr,                                   # array
           ctypes.c_size_t(len(arr)),            # array size
           ctypes.sizeof(ctypes.c_int),          # element size
           compare_callback)                      # comparison function

# Print sorted array
print([arr[i] for i in range(5)])  # [1, 2, 3, 4, 5]
```

---

## Alternative Approach: CFFI: What is CFFI?

- C Foreign Function Interface for Python
- Simpler API than ctypes in many cases
- Supports both API and ABI compatibility modes
- Can generate Python modules from C headers
- Works well with PyPy (faster alternative Python implementation)
- Maintained by PyPy developers

```python
# Basic CFFI example
from cffi import FFI

ffi = FFI()

# Declare the C function signature
ffi.cdef("""
    int printf(const char *format, ...);
    int add(int a, int b);
""")

# Load the C library
lib = ffi.dlopen(None)  # Use standard library

# Call a C standard library function
lib.printf(b"Hello, %s!\n", b"world")

# Define our own C function inline
ffi.cdef("int add(int a, int b);")
lib = ffi.verify("""
    int add(int a, int b) {
        return a + b;
    }
""")

result = lib.add(3, 4)
print(f"3 + 4 = {result}")  # 7
```

---

## Alternative Approach: CFFI: CFFI API Mode

- Compiles C extension module at build time
- Can include and process header files
- Higher performance than ABI mode
- Better for distribution and larger projects
- More similar to writing a C extension

```python
# CFFI API mode example
# build_module.py
from cffi import FFI

ffi = FFI()

# Declare the C types and functions
ffi.cdef("""
    double calculate_distance(double x1, double y1, double x2, double y2);
""")

# Provide implementation
ffi.set_source("_geometry",  # Output module name
    """
    #include <math.h>

    double calculate_distance(double x1, double y1, double x2, double y2) {
        return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2));
    }
    """,
    libraries=['m'])  # Link with math library

if __name__ == "__main__":
    ffi.compile()  # Create the C extension module

# After running: python build_module.py
# Use the compiled module:
from _geometry import lib, ffi
dist = lib.calculate_distance(0, 0, 3, 4)
print(f"Distance: {dist}")  # 5.0
```

---

## Alternative Approach: CFFI: Working with Structures in CFFI

- Define structure layouts in C syntax
- Access fields naturally in Python
- Convert between Python objects and C structures
- Work with arrays of structures
- Handle pointers and memory allocation

```python
from cffi import FFI

ffi = FFI()

# Define a C structure
ffi.cdef("""
    typedef struct {
        char name[64];
        int age;
        double height;
    } Person;

    void print_person(Person *p);
    Person *create_person(const char *name, int age, double height);
    void free_person(Person *p);
""")
```

---

## Working with Structures in CFFI: C Implementation

```python
# Implementation
lib = ffi.verify("""
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    typedef struct {
        char name[64];
        int age;
        double height;
    } Person;

    void print_person(Person *p) {
        printf("Name: %s, Age: %d, Height: %.2f\\n",
               p->name, p->age, p->height);
    }

    Person *create_person(const char *name, int age, double height) {
        Person *p = (Person*)malloc(sizeof(Person));
        strncpy(p->name, name, 63);
        p->name[63] = '\\0';
        p->age = age;
        p->height = height;
        return p;
    }

    void free_person(Person *p) {
        free(p);
    }
""")
```

---

## Working with Structures in CFFI: Usage

```python
# Create and use a Person
person = lib.create_person(b"Alice", 30, 1.75)
lib.print_person(person)

# Access structure fields
print(f"Name: {ffi.string(person.name).decode('utf-8')}")
print(f"Age: {person.age}")
print(f"Height: {person.height}")

# Clean up
lib.free_person(person)
```

---

## Alternative Approach: Cython: What is Cython?

- Programming language combining Python and C
- Python syntax with optional static typing
- Compiles to efficient C code
- Can call C functions and use C types directly
- Easier than pure C extensions
- Significant performance improvements possible

```python
# Python version (slow)
def fibonacci_py(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a
```

```cython
# Cython version (fast)
# fibonacci.pyx
def fibonacci_cy(int n):
    cdef int i
    cdef long a = 0, b = 1
    for i in range(n):
        a, b = b, a + b
    return a
```

```python
# setup.py
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("fibonacci.pyx")
)
```

---

## Alternative Approach: Cython: Cython Type Declarations

- `cdef` declares C variables and functions
- `cpdef` creates functions callable from both Python and C
- Type declarations improve performance
- C types: int, long, float, double, etc.
- Use Python objects when needed

```cython
# Type declarations in Cython
cdef int i, j
cdef double x = 0.0
cdef float y = 0.0
cdef char* s = "hello"
cdef int* ptr
cdef int arr[10]

# Function with C types
cdef int add(int a, int b):
    return a + b

# Function callable from Python
cpdef double calculate(double x, double y):
    cdef double result
    result = add(<int>x, <int>y)  # Type casting
    return result
```

---

## Alternative Approach: Cython: Calling C Functions from Cython

- External C functions must be declared with `cdef extern`
- Can include C header files
- Call C functions directly with native types
- Access C libraries seamlessly
- Expose C functions to Python

```cython
# Calling C functions from Cython
# math_wrapper.pyx

# Include C libraries
cdef extern from "math.h":
    double sin(double x)
    double cos(double x)
    double sqrt(double x)

# Cython function using C functions
def calculate_distance(double x1, double y1, double x2, double y2):
    cdef double dx = x2 - x1
    cdef double dy = y2 - y1
    return sqrt(dx*dx + dy*dy)

# Compute vector angle using C math functions
def vector_angle(double x, double y):
    return atan2(y, x)
```

---

## Alternative Approach: Cython: Using NumPy with Cython

- Efficient array operations
- Access NumPy arrays directly from C
- Avoid Python overhead for loops
- Common pattern for numerical computing
- Optimize bottlenecks in NumPy code

```cython
# Example using NumPy arrays with Cython
# array_ops.pyx
import numpy as np
cimport numpy as np

# Tell Cython that our function works with np.ndarray objects
def fast_multiply(np.ndarray[np.float64_t, ndim=2] a,
                 np.ndarray[np.float64_t, ndim=2] b):
    cdef int i, j
    cdef int rows = a.shape[0]
    cdef int cols = a.shape[1]

    # Create result array
    cdef np.ndarray[np.float64_t, ndim=2] result = np.zeros((rows, cols), dtype=np.float64)

    # Fast C-level loop
    for i in range(rows):
        for j in range(cols):
            result[i, j] = a[i, j] * b[i, j]

    return result
```

---

## Alternative Approach: pybind11

## What is pybind11?
- Header-only C++11 library for creating Python extensions
- Modern, lightweight alternative to SWIG
- Exposes C++ classes, functions, and types to Python
- Automatic type conversion between C++ and Python
- Ideal for C++ projects
- Easier to use than raw Python C API

```cpp
// example.cpp
#include <pybind11/pybind11.h>
namespace py = pybind11;

// A simple C++ function
int add(int a, int b) {
    return a + b;
}

// A simple C++ class
class Pet {
public:
    Pet(const std::string &name) : name(name) { }
    void setName(const std::string &name_) { name = name_; }
    const std::string &getName() const { return name; }
private:
    std::string name;
};

// Create Python module
PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example module";

    // Expose function
    m.def("add", &add, "Add two numbers");

    // Expose class
    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string &>())
        .def("setName", &Pet::setName)
        .def("getName", &Pet::getName);
}
```

---

## Alternative Approach: SWIG

## What is SWIG?
- Simplified Wrapper and Interface Generator
- Generates bindings for many languages, not just Python
- Processes interface files to create wrappers
- Can wrap entire C/C++ libraries with minimal effort
- More complex setup than other methods
- Good for large-scale integration

```c
// example.c
int add(int a, int b) {
    return a + b;
}

double multiply(double a, double b) {
    return a * b;
}
```

```config
// example.i (SWIG interface file)
%module example

%{
#include "example.h"
%}

// Functions to wrap
int add(int a, int b);
double multiply(double a, double b);
```

```bash
# Generate wrapper
swig -python example.i

# Compile
gcc -shared -fPIC -o _example.so example.c example_wrap.c -I/usr/include/python3.8

# Then in Python
import example
result = example.add(3, 4)  # 7
```

---

## Performance Considerations: The Global Interpreter Lock (GIL)

- Python allows only one thread to execute Python code at a time
- C extensions can release the GIL during computation
- Critical for true multi-threaded performance
- Python C API provides macros to manage the GIL
- Important for CPU-bound extensions

```c
// Example of releasing the GIL for a long computation
static PyObject* intensive_calculation(PyObject* self, PyObject* args) {
    int input;
    if (!PyArg_ParseTuple(args, "i", &input))
        return NULL;

    // Release the GIL for the intensive work
    Py_BEGIN_ALLOW_THREADS

    // This code can run in parallel with other Python threads
    // Don't touch Python objects while GIL is released
    long result = do_intensive_calculation(input);

    // Reacquire the GIL before touching Python objects
    Py_END_ALLOW_THREADS

    return PyLong_FromLong(result);
}
```

---

## Performance Considerations: Memory Management Strategies

- Balance between Python and C memory management
- Use Python's memory allocators for consistent behavior
- Consider specialized allocators for performance-critical sections
- Reduce copying between Python and C representations
- Be careful with reference cycles

```c
// Using Python's memory allocator
void* buffer = PyMem_Malloc(size);
if (buffer == NULL) {
    PyErr_NoMemory();
    return NULL;
}

// Process data in buffer...

// Clean up
PyMem_Free(buffer);

// Variants for different purposes
// PyMem_RawMalloc/PyMem_RawFree - no Python state required
// PyMem_Calloc - clears memory
// PyObject_Malloc - for objects
```

---

## Performance Considerations: Profiling C Extensions

- Identify bottlenecks in both Python and C code
- Use specific profiling tools for C code (e.g., valgrind)
- Check reference counting and memory leaks
- Profile Python interface overhead
- Incremental optimization approach

```python
# Python-level profiling with cProfile
import cProfile

def test_extension():
    # Call C extension functions here
    for i in range(1000000):
        my_extension.intensive_function(i)

cProfile.run('test_extension()')

# Python-level memory profiling
from memory_profiler import profile

@profile
def memory_test():
    result = my_extension.create_large_array(1000000)
    # Process result...
    return result

memory_test()
```

```bash
# C-level profiling with valgrind
valgrind --tool=callgrind python -c "import my_extension; my_extension.test()"

# Memory checking
valgrind --tool=memcheck python -c "import my_extension; my_extension.test()"
```

---

## Practical Example: Image Processing: `Grayscale` Function Signature

```c
// image_processing.c
#include <Python.h>
#include <numpy/arrayobject.h>

// Grayscale conversion: average RGB channels
static PyObject* grayscale(PyObject* self, PyObject* args) {
    PyArrayObject *input_array, *output_array;

    // Parse input array
    if (!PyArg_ParseTuple(args, "O!", &PyArray_Type, &input_array))
        return NULL;

    // Ensure input is 3D (height, width, channels)
    if (PyArray_NDIM(input_array) != 3) {
        PyErr_SetString(PyExc_ValueError, "Input must be a 3D array (H,W,C)");
        return NULL;
    }

    // Get dimensions
    npy_intp *dims = PyArray_DIMS(input_array);
    npy_intp height = dims[0];
    npy_intp width = dims[1];
    npy_intp channels = dims[2];

    if (channels != 3) {
        PyErr_SetString(PyExc_ValueError, "Input must have 3 channels (RGB)");
        return NULL;
    }
```

---

## Image Processing Extension: Conversion Loop

```c
    // Create output array (height, width, 1)
    npy_intp out_dims[3] = {height, width, 1};
    output_array = (PyArrayObject*)PyArray_SimpleNew(3, out_dims, NPY_UINT8);
    if (output_array == NULL)
        return NULL;

    // Process the image: RGB to grayscale
    unsigned char *input_data = (unsigned char*)PyArray_DATA(input_array);
    unsigned char *output_data = (unsigned char*)PyArray_DATA(output_array);

    // Release GIL for processing
    Py_BEGIN_ALLOW_THREADS

    for (npy_intp i = 0; i < height; i++) {
        for (npy_intp j = 0; j < width; j++) {
            // Calculate pixel position
            npy_intp in_pos = (i * width + j) * channels;
            npy_intp out_pos = i * width + j;

            // Average RGB channels
            unsigned int sum = input_data[in_pos] +     // R
                              input_data[in_pos + 1] +  // G
                              input_data[in_pos + 2];   // B

            output_data[out_pos] = sum / 3;
        }
    }

    Py_END_ALLOW_THREADS

    return PyArray_Return(output_array);
}
```

---

## Image Processing Extension: Module Initialization

```c
// Module initialization
static PyMethodDef ImageMethods[] = {
    {"grayscale", grayscale, METH_VARARGS, "Convert RGB image to grayscale"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef imagemodule = {
    PyModuleDef_HEAD_INIT,
    "image_processing",
    "Image processing functions in C",
    -1,
    ImageMethods
};

PyMODINIT_FUNC PyInit_image_processing(void) {
    PyObject *m;
    m = PyModule_Create(&imagemodule);
    if (m == NULL)
        return NULL;

    // Import NumPy
    import_array();

    return m;
}
```

---

## Practical Example: Image Processing: Setup and Usage for Image Extension

```python
# setup.py
from setuptools import setup, Extension
import numpy as np

module = Extension('image_processing',
                  sources=['image_processing.c'],
                  include_dirs=[np.get_include()],
                  extra_compile_args=['-O3'])

setup(
    name='ImageProcessing',
    version='1.0',
    description='Fast image processing with C',
    ext_modules=[module],
    install_requires=['numpy'],
)
```

```python
# Using the module
import numpy as np
from PIL import Image
import image_processing

# Load image
img = np.array(Image.open('image.jpg'))
print(f"Original shape: {img.shape}")

# Process with C extension
gray = image_processing.grayscale(img)
print(f"Grayscale shape: {gray.shape}")

# Save result
Image.fromarray(gray.reshape(gray.shape[0], gray.shape[1])).save('gray.jpg')

# Compare with NumPy version
numpy_gray = np.mean(img, axis=2, keepdims=True).astype(np.uint8)
np.testing.assert_allclose(gray, numpy_gray, atol=1)
print("Results match!")
```

---

## Summary

## Key Takeaways
- Direct C extensions offer maximum flexibility and performance
- Python C API provides full access to Python's internals
- Alternative approaches like ctypes, CFFI, and Cython provide easier integration
- Choose the right integration method based on your needs
- Remember to handle reference counting and errors correctly
- Performance gains can be substantial for CPU-bound tasks
- Real-world examples demonstrate practical integration techniques

---

## Resources

## Further Learning
- [Python/C API Reference Manual](https://docs.python.org/3/c-api/)
- [Extending and Embedding Python](https://docs.python.org/3/extending/index.html)
- [CFFI Documentation](https://cffi.readthedocs.io/)
- [Cython Documentation](https://cython.readthedocs.io/)
- [pybind11 Documentation](https://pybind11.readthedocs.io/)
- [Python Cookbook, Chapter 15: C Extensions](https://www.oreilly.com/library/view/python-cookbook-3rd/9781449357337/)
- [Interfacing with C: Writing Extensions](https://realpython.com/c-for-python-programmers/)
