---
tags:
  - tools:cmake
  - languages:c
  - languages:c++
  - practices:build-systems
level: intermediate
category: build-system
audience:
  - audiences:developers
  - audiences:devops

---
# Introduction to CMake

---

## What is CMake?

- A cross-platform, open-source build system generator
- Does not build software directly - generates native build files
- Supports `Makefiles`, `Ninja`, Visual Studio solutions, Xcode projects, and more
- The de facto standard for C and C++ projects

---

## CMake History

- Created by Bill Hoffman at Kitware in 2000
- Originally developed for the Insight Toolkit (ITK) project
- Funded by the US National Library of Medicine
- Replaced `autotools` as the dominant build system for C/C++

---

## CMake Timeline

| Year | Milestone |
|------|-----------|
| 2000 | Initial release |
| 2006 | CMake 2.4 - widespread adoption begins |
| 2014 | CMake 3.0 - modern CMake paradigm |
| 2017 | CMake 3.9 - improved `find_package` |
| 2020 | CMake 3.19 - presets support |
| 2023 | CMake 3.27 - continued improvements |

---

## Why CMake Became Popular

- Cross-platform support (Linux, macOS, Windows, embedded)
- Handles complex dependency graphs
- Large ecosystem of "Find" modules
- Adopted by major projects: LLVM, Qt, KDE, OpenCV, Boost
- Strong IDE integration (CLion, VS Code, Visual Studio)

---

## CMake Major Features

- Out-of-source builds
- Automatic dependency tracking
- Platform-independent configuration
- Built-in test and packaging support
- Support for multiple languages (C, C++, Fortran, CUDA, ASM)

---

## CMake vs Other Build Systems

| Feature | CMake | Make | Meson | Bazel |
|---------|-------|------|-------|-------|
| Cross-platform | Yes | Limited | Yes | Yes |
| Generator | Yes | No | Yes | No |
| Learning curve | Medium | Low | Low | High |
| Ecosystem | Huge | Huge | Growing | Growing |
| IDE support | Excellent | Basic | Good | Good |

---
## Build Tool Comparison

![cmake_vs_others](svg/courses/build_systems/cmake/01_introduction/cmake_vs_others.svg)

---

## The CMake Pipeline

![the_cmake_pipeline](svg/courses/build_systems/cmake/01_introduction/the_cmake_pipeline.svg)

---

## The CMake Pipeline Steps

- **Configure step**: CMake reads `CMakeLists.txt` and generates build files
- **Build step**: Native tool (`make`, `ninja`, etc.) compiles the code
- **Install step**: Optionally install built artifacts

---

## Configuration Step in Detail

```bash
mkdir build
cd build
cmake ..
```

- CMake detects the compiler, platform, and settings
- Generates a `CMakeCache.txt` with cached variables
- Produces native build system files

---

## Build Step in Detail

```bash
cmake --build .
```

- Invokes the underlying build tool
- Compiles source files
- Links executables and libraries
- Only rebuilds changed files (incremental builds)

---

## Out-of-Source Builds

```tree
my_project/
    CMakeLists.txt
    src/
        main.cpp
    build/          <-- Build artifacts go here
        Makefile
        CMakeCache.txt
        main
```

- Source tree stays clean
- Multiple build directories allowed (Debug, Release)
- Never run `cmake .` in the source directory

---

## Out Of Source Build Wins

![out_of_source_benefits](svg/courses/build_systems/cmake/01_introduction/out_of_source_benefits.svg)

---

## Platform Independence

- CMake abstracts away platform-specific details
- Same `CMakeLists.txt` works on Linux, macOS, and Windows
- Compiler flags are translated automatically
- Path separators handled transparently

---

## Platform Independence - Example

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyApp)

add_executable(myapp src/main.cpp)
target_compile_features(myapp PRIVATE cxx_std_17)
```

- This works on any platform with a C++17 compiler
- No `#ifdef _WIN32` in the build script
- CMake picks the right compiler and flags

---

## CMake Generators

```bash
cmake -G "Unix Makefiles" ..
cmake -G "Ninja" ..
cmake -G "Visual Studio 17 2022" ..
cmake -G "Xcode" ..
```

- Generators determine which build system files to produce
- Default generator is platform-dependent
- `Ninja` is recommended for speed

---

## Listing Available Generators

```bash
cmake --help
```

Output includes:

```output
Generators
  * Unix Makefiles
    Ninja
    Ninja Multi-Config
    Visual Studio 17 2022
    Xcode
```

---

## The CMake Developer

- CMake is developed and maintained by **Kitware**
- Open-source under a permissive BSD license
- Active community on Discourse, GitLab, and Stack Overflow
- Documentation at https://cmake.org/documentation/

---

## CMake Versions and Policies

- Each CMake version introduces new features and policies
- `cmake_minimum_required(VERSION X.Y)` sets the minimum version
- Policies allow backward compatibility
- Always specify the minimum version your project needs

---

## The CMake Family of Tools

![the_cmake_family_of_tools](svg/courses/build_systems/cmake/01_introduction/the_cmake_family_of_tools.svg)

---

## CPack Overview

- Packages built software into distributable formats
- Supports: `.tar.gz`, `.zip`, `.deb`, `.rpm`, `.exe` (NSIS), `.dmg`
- Configured within `CMakeLists.txt`
- Invoked with `cpack` command after building

---

## CTest Overview

- CMake's built-in test runner
- Discovers and runs tests registered with `add_test()`
- Supports test labels, timeouts, and fixtures
- Integrates with GTest, Catch2, and other frameworks

---

## CDash Overview

- Web-based dashboard for collecting test results
- Shows build/test/coverage history over time
- Supports continuous, nightly, and experimental builds
- Hosted at https://my.cdash.org or self-hosted

---

## Installing CMake

On Linux:

```bash
sudo apt install cmake    # Debian/Ubuntu
sudo dnf install cmake    # Fedora
```

On macOS:

```bash
brew install cmake
```

On Windows: download from https://cmake.org/download/

---

## Verifying the Installation

```bash
cmake --version
```

```output
cmake version 3.28.1
CMake suite maintained and supported by Kitware
```

- Ensure your version meets project requirements
- Newer is generally better for modern CMake features
