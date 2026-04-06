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

## The CMake Pipeline

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="70">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- CMakeLists.txt -->
  <rect x="10" y="15" width="130" height="40" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="75" y="40" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">CMakeLists.txt</text>
  <line x1="140" y1="35" x2="175" y2="35" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- cmake (configure) -->
  <rect x="175" y="15" width="130" height="40" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="240" y="32" font-family="sans-serif" font-size="12" font-weight="bold" fill="#222" text-anchor="middle">cmake</text>
  <text x="240" y="48" font-family="sans-serif" font-size="11" fill="#555" text-anchor="middle">(configure)</text>
  <line x1="305" y1="35" x2="340" y2="35" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Build Files -->
  <rect x="340" y="15" width="110" height="40" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="395" y="40" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Build Files</text>
  <line x1="450" y1="35" x2="485" y2="35" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Build Tool -->
  <rect x="485" y="15" width="100" height="40" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="535" y="40" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Build Tool</text>
  <line x1="585" y1="35" x2="620" y2="35" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <!-- Binaries -->
  <rect x="620" y="15" width="80" height="40" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="660" y="40" font-family="sans-serif" font-size="12" fill="#222" text-anchor="middle">Binaries</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="380" height="220">
  <!-- CMake -->
  <rect x="20" y="10" width="340" height="48" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="120" y="33" font-family="sans-serif" font-size="14" font-weight="bold" fill="#222">CMake</text>
  <text x="230" y="33" font-family="sans-serif" font-size="12" fill="#555">Build system generator</text>
  <!-- CTest -->
  <rect x="20" y="63" width="340" height="48" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="120" y="86" font-family="sans-serif" font-size="14" font-weight="bold" fill="#222">CTest</text>
  <text x="230" y="86" font-family="sans-serif" font-size="12" fill="#555">Test driver</text>
  <!-- CPack -->
  <rect x="20" y="116" width="340" height="48" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="120" y="139" font-family="sans-serif" font-size="14" font-weight="bold" fill="#222">CPack</text>
  <text x="230" y="139" font-family="sans-serif" font-size="12" fill="#555">Packaging tool</text>
  <!-- CDash -->
  <rect x="20" y="169" width="340" height="48" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="120" y="192" font-family="sans-serif" font-size="14" font-weight="bold" fill="#222">CDash</text>
  <text x="230" y="192" font-family="sans-serif" font-size="12" fill="#555">Testing dashboard</text>
</svg>

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
