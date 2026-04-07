# Hello World with CMake

---

## Chapter Overview

- Creating a minimal CMake project
- Building executables and libraries
- Setting compiler flags
- User-configured options
- Build types (Debug, Release)
- Property inheritance from dependencies

---

## Minimal CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.20)
project(HelloWorld)

add_executable(hello main.cpp)
```

- `cmake_minimum_required()` sets the minimum CMake version
- `project()` names the project
- `add_executable()` defines a build target

---

## The Source File

```cmake
# This is what main.cpp looks like (shown for context)
```

```cpp
// main.cpp
#include <iostream>

int main() {
    std::cout << "Hello, CMake!" << std::endl;
    return 0;
}
```

---

## Building the Project

```bash
mkdir build
cd build
cmake ..
cmake --build .
./hello
```

```output
Hello, CMake!
```

---

## Project Directory Layout

```tree
hello_project/
    CMakeLists.txt
    main.cpp
    build/
        CMakeCache.txt
        CMakeFiles/
        Makefile
        hello
```

- Source and build directories are separate
- All generated files stay in `build/`

---

## The cmake_minimum_required() Command

```cmake
cmake_minimum_required(VERSION 3.20)
```

- Must be the first command in `CMakeLists.txt`
- Enforces a minimum CMake version for the project
- Controls which policies are active
- If the installed CMake is older, configuration fails with an error

---

## The project() Command

```cmake
project(HelloWorld
    VERSION 1.0.0
    DESCRIPTION "A simple hello world"
    LANGUAGES CXX
)
```

- `VERSION` sets `PROJECT_VERSION` variable
- `DESCRIPTION` provides a human-readable description
- `LANGUAGES` specifies languages used (`C`, `CXX`, `Fortran`, `CUDA`)

---

## Variables Set by project()

| Variable | Value |
|----------|-------|
| `PROJECT_NAME` | HelloWorld |
| `PROJECT_VERSION` | 1.0.0 |
| `PROJECT_VERSION_MAJOR` | 1 |
| `PROJECT_VERSION_MINOR` | 0 |
| `PROJECT_VERSION_PATCH` | 0 |
| `PROJECT_SOURCE_DIR` | /path/to/source |
| `PROJECT_BINARY_DIR` | /path/to/build |

---

## Adding Multiple Source Files

```cmake
add_executable(hello
    main.cpp
    utils.cpp
    parser.cpp
)
```

- List all source files that make up the executable
- Header files are not listed (they are found via `#include`)

---

## Creating a Static Library

```cmake
add_library(mylib STATIC
    mathutil.cpp
    stringutil.cpp
)
```

- `STATIC` creates a `.a` (Linux) or `.lib` (Windows) file
- The library is an archive of object files
- Must be linked to an executable to be useful

---

## Creating a Shared Library

```cmake
add_library(mylib SHARED
    mathutil.cpp
    stringutil.cpp
)
```

- `SHARED` creates a `.so` (Linux) or `.dll` (Windows) file
- Loaded at runtime by the dynamic linker
- Can be shared across multiple executables

---

## Linking a Library to an Executable

```cmake
add_library(mylib STATIC mathutil.cpp)
add_executable(hello main.cpp)
target_link_libraries(hello PRIVATE mylib)
```

- `target_link_libraries()` connects a library to an executable
- `PRIVATE` means the dependency is internal to the target

---

## PRIVATE vs PUBLIC vs INTERFACE

| Keyword | Used by target | Propagated to dependents |
|---------|---------------|------------------------|
| `PRIVATE` | Yes | No |
| `PUBLIC` | Yes | Yes |
| `INTERFACE` | No | Yes |

- `PRIVATE` - only the target itself uses the dependency
- `PUBLIC` - both the target and its consumers use it
- `INTERFACE` - only consumers use it (e.g., header-only libraries)

---

## The set() Command

```cmake
set(MY_SOURCES main.cpp utils.cpp parser.cpp)
add_executable(hello ${MY_SOURCES})

set(MY_VERSION "1.0")
message(STATUS "Version is ${MY_VERSION}")
```

- `set()` creates or modifies a variable
- Variables are referenced with `${VAR_NAME}`
- Scope is the current `CMakeLists.txt` and below

---

## CMAKE_C_FLAGS and CMAKE_CXX_FLAGS

```cmake
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=c11")
```

- Global flags that apply to all targets
- Appending preserves any user-supplied flags
- This is the old-style approach
- Affects every target in the project, which can cause problems

---

## target_compile_options (Modern Approach)

```cmake
target_compile_options(myapp PRIVATE
    -Wall
    -Wextra
    -Wpedantic
)
```

- Adds flags only to the specified target
- `PRIVATE` keeps flags from propagating to dependents
- Preferred over global `CMAKE_CXX_FLAGS`

---

## Setting the C++ Standard

```cmake
target_compile_features(myapp PRIVATE cxx_std_17)
```

Or using target properties:

```cmake
set_target_properties(myapp PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)
```

- `CXX_STANDARD_REQUIRED ON` makes it an error if not supported
- `CXX_EXTENSIONS OFF` disables GNU extensions

---

## User-Configured Options with option()

```cmake
option(ENABLE_TESTS "Build test suite" ON)
option(USE_OPENGL "Enable OpenGL rendering" OFF)

if(ENABLE_TESTS)
    add_subdirectory(tests)
endif()
```

- `option()` creates a boolean cache variable
- Users toggle with `cmake -DENABLE_TESTS=OFF ..`
- Values persist in `CMakeCache.txt`

---

## cmake_dependent_option

```cmake
include(CMakeDependentOption)

option(BUILD_GUI "Build the GUI frontend" ON)
cmake_dependent_option(
    USE_OPENGL "Use OpenGL for rendering" ON
    "BUILD_GUI" OFF
)
```

- `USE_OPENGL` is only available when `BUILD_GUI` is `ON`
- If the condition is false, it defaults to `OFF`
- Useful for hiding irrelevant options from users

---

## Build Types

```bash
cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake -DCMAKE_BUILD_TYPE=Release ..
cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo ..
cmake -DCMAKE_BUILD_TYPE=MinSizeRel ..
```

| Type | Optimization | Debug Info |
|------|-------------|------------|
| `Debug` | `-O0` | Yes (`-g`) |
| `Release` | `-O3` | No |
| `RelWithDebInfo` | `-O2` | Yes (`-g`) |
| `MinSizeRel` | `-Os` | No |

---

## Setting a Default Build Type

```cmake
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release
        CACHE STRING "Build type" FORCE)
endif()
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
```

- Without this, the default is an empty string (no optimization flags)
- Always set a sensible default for your project

---

## Property Inheritance via target_link_libraries

```cmake
add_library(mylib STATIC mylib.cpp)
target_include_directories(mylib PUBLIC include/)
target_compile_definitions(mylib PUBLIC USE_MYLIB)

add_executable(app main.cpp)
target_link_libraries(app PRIVATE mylib)
# app automatically gets include/ and USE_MYLIB
```

- `PUBLIC` properties propagate through `target_link_libraries()`
- This is the core of modern CMake's target-based approach

---

## Visualizing Property Propagation

![visualizing_property_propagation](/svg/courses/build_systems/cmake/02_hello_world/visualizing_property_propagation.svg)

- `PRIVATE` linking stops propagation
- `PUBLIC` linking continues the chain
- `INTERFACE` properties propagate without being used by the owner

---

## Complete Example Walkthrough

```cmake
cmake_minimum_required(VERSION 3.20)
project(Greeter VERSION 1.0 LANGUAGES CXX)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release
        CACHE STRING "Build type" FORCE)
endif()

option(BUILD_TESTS "Build test suite" ON)
```

- Sets up the project with a version and language
- Provides a default build type
- Offers a user-configurable option

---

## Complete Example (Continued)

```cmake
add_library(greet STATIC src/greet.cpp)
target_include_directories(greet PUBLIC include/)
target_compile_features(greet PUBLIC cxx_std_17)
target_compile_options(greet PRIVATE -Wall -Wextra)

add_executable(app src/main.cpp)
target_link_libraries(app PRIVATE greet)
```

- Library with public headers and C++17 requirement
- Executable consuming the library
- C++17 and include paths propagate from library to executable
