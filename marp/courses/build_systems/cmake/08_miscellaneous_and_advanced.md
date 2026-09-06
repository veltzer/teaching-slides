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

# Miscellaneous and Advanced Topics

---

## Chapter Overview

- Generating files with `configure_file()`
- Custom targets and custom commands
- Executing processes during configuration
- Cross-compilation with toolchain files
- CMake presets
- Modern CMake best practices and anti-patterns

---

## configure_file() - Overview

- Copies a file and substitutes variable values
- Used to generate headers, config files, and scripts
- Runs at **configure time** (when `cmake` is invoked)
- Supports two substitution syntaxes: `@VAR@` and `${VAR}`

---

## configure_file() - Basic Usage

Template file `config.h.in`:

```cmake
#define PROJECT_NAME "@PROJECT_NAME@"
#define PROJECT_VERSION "@PROJECT_VERSION@"
#define ENABLE_FEATURE @ENABLE_FEATURE@
```

In `CMakeLists.txt`:

```cmake
set(ENABLE_FEATURE 1)
configure_file(config.h.in config.h)
```

---

## Template Substitution Syntax

- `@VAR@` replaces with the value of CMake variable `VAR`
- `${VAR}` also replaces, but can conflict with shell or C++ code
- Use `@ONLY` to restrict substitution to `@VAR@` only

```cmake
configure_file(config.h.in
    ${CMAKE_CURRENT_BINARY_DIR}/config.h
    @ONLY
)
```

- `@ONLY` is the recommended approach for safety
- `COPYONLY` copies without any substitution at all

---

## Generating Version Headers

```cmake
project(MyApp VERSION 2.3.1)

configure_file(version.h.in
    ${CMAKE_CURRENT_BINARY_DIR}/version.h
    @ONLY
)

target_include_directories(myapp PRIVATE
    ${CMAKE_CURRENT_BINARY_DIR}
)
```

Template `version.h.in`:

```cmake
#define MYAPP_VERSION_MAJOR @PROJECT_VERSION_MAJOR@
#define MYAPP_VERSION_MINOR @PROJECT_VERSION_MINOR@
#define MYAPP_VERSION_PATCH @PROJECT_VERSION_PATCH@
#define MYAPP_VERSION "@PROJECT_VERSION@"
```

---

## configure_file() with #cmakedefine

Template:

```cmake
#cmakedefine USE_SSL
#cmakedefine01 HAVE_THREADS
```

If `USE_SSL` is defined and truthy:

```cmake
#define USE_SSL
#define HAVE_THREADS 1
```

If `USE_SSL` is not defined or falsy:

```cmake
/* #undef USE_SSL */
#define HAVE_THREADS 0
```

---

## Custom Targets with add_custom_target()

```cmake
add_custom_target(format
    COMMAND clang-format -i
        ${CMAKE_SOURCE_DIR}/src/*.cpp
        ${CMAKE_SOURCE_DIR}/include/*.h
    COMMENT "Formatting source files"
)
```

```console
cmake --build . --target format
```

- Custom targets are **always** considered out of date
- They run every time they are invoked
- Not part of the default `all` target unless `ALL` is specified

---

## Custom Targets with Dependencies

```cmake
add_custom_target(docs
    COMMAND doxygen ${CMAKE_SOURCE_DIR}/Doxyfile
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Generating documentation"
)

add_dependencies(docs mylib)
```

- `add_dependencies()` ensures `mylib` is built before `docs`
- The `DEPENDS` keyword specifies file-level dependencies
- The `WORKING_DIRECTORY` sets where the command runs

---

## Custom Commands - OUTPUT Form

```cmake
add_custom_command(
    OUTPUT ${CMAKE_BINARY_DIR}/generated.cpp
    COMMAND python3 ${CMAKE_SOURCE_DIR}/gen.py
        -o ${CMAKE_BINARY_DIR}/generated.cpp
    DEPENDS ${CMAKE_SOURCE_DIR}/gen.py
    COMMENT "Generating source file"
)

add_executable(app main.cpp
    ${CMAKE_BINARY_DIR}/generated.cpp)
```

- Produces output files consumed by other targets
- Only runs when outputs are needed and inputs change

---

## Custom Commands - TARGET Form

```cmake
add_custom_command(TARGET myapp POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:myapp>
        ${CMAKE_SOURCE_DIR}/deploy/
    COMMENT "Copying to deploy directory"
)
```

- `PRE_BUILD` - before building (Visual Studio only)
- `PRE_LINK` - after compiling, before linking
- `POST_BUILD` - after building the target

---

## OUTPUT vs TARGET Forms Compared

| Aspect | OUTPUT form | TARGET form |
|--------|-------------|-------------|
| Trigger | When output file is needed | When target is built |
| Rerun | When dependencies change | Every build of target |
| Use case | Code generation | Post-build steps |
| Keyword | `OUTPUT` | `TARGET` |

- OUTPUT form creates a file dependency in the build graph
- TARGET form attaches to an existing build target

---

## Generating Source Files at Build Time

```cmake
add_custom_command(
    OUTPUT ${CMAKE_BINARY_DIR}/version_info.cpp
    COMMAND ${CMAKE_COMMAND}
        -DSRC=${CMAKE_SOURCE_DIR}/version_info.cpp.in
        -DDST=${CMAKE_BINARY_DIR}/version_info.cpp
        -P ${CMAKE_SOURCE_DIR}/gen_version.cmake
    DEPENDS ${CMAKE_SOURCE_DIR}/version_info.cpp.in
)

add_executable(app
    main.cpp
    ${CMAKE_BINARY_DIR}/version_info.cpp
)
```

- Generated files must be listed as sources for a target
- The build system tracks the dependency automatically

---

## execute_process() - Overview

```cmake
execute_process(
    COMMAND git rev-parse HEAD
    OUTPUT_VARIABLE GIT_HASH
    OUTPUT_STRIP_TRAILING_WHITESPACE
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)

message(STATUS "Git hash: ${GIT_HASH}")
```

- Runs during `cmake` configuration, not during build
- Captures stdout, stderr, and return code
- `OUTPUT_STRIP_TRAILING_WHITESPACE` removes trailing newline

---

## Capturing Output from execute_process()

```cmake
execute_process(
    COMMAND pkg-config --modversion libcurl
    RESULT_VARIABLE result
    OUTPUT_VARIABLE curl_version
    ERROR_VARIABLE error_msg
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

if(NOT result EQUAL 0)
    message(WARNING "pkg-config failed: ${error_msg}")
endif()
```

- `RESULT_VARIABLE` holds the exit code (0 on success)
- `ERROR_VARIABLE` captures stderr output
- Multiple `COMMAND` arguments create a pipeline

---

## execute_process() - Piping Commands

```cmake
execute_process(
    COMMAND cat /proc/cpuinfo
    COMMAND grep "model name"
    COMMAND head -1
    OUTPUT_VARIABLE CPU_MODEL
    OUTPUT_STRIP_TRAILING_WHITESPACE
)
```

- Each `COMMAND` creates a stage in the pipeline
- stdout of each feeds into stdin of the next
- Only the last command's stdout is captured

---

## Cross-Compilation Overview

![cross_compilation_overview](svg/courses/build_systems/cmake/08_miscellaneous_and_advanced/cross_compilation_overview.svg)

---

## Cross-Compilation Key Points

- Build on one platform, run on another
- Requires a cross-compiler toolchain
- CMake uses **toolchain files** to configure cross-compilation
- Invoked via `CMAKE_TOOLCHAIN_FILE`

---

## Toolchain File Anatomy

![toolchain_files](svg/courses/build_systems/cmake/08_miscellaneous_and_advanced/toolchain_files.svg)

---

## Toolchain File Variables

| Variable | Description |
|----------|-------------|
| `CMAKE_SYSTEM_NAME` | Target OS (Linux, Windows, etc.) |
| `CMAKE_SYSTEM_PROCESSOR` | Target CPU (arm, aarch64, etc.) |
| `CMAKE_C_COMPILER` | C compiler path |
| `CMAKE_CXX_COMPILER` | C++ compiler path |
| `CMAKE_SYSROOT` | Target sysroot path |
| `CMAKE_FIND_ROOT_PATH` | Root path for find commands |

- Setting `CMAKE_SYSTEM_NAME` triggers cross-compilation mode

---

## Toolchain File Example for ARM

```cmake
# arm-toolchain.cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_C_COMPILER arm-linux-gnueabihf-gcc)
set(CMAKE_CXX_COMPILER arm-linux-gnueabihf-g++)

set(CMAKE_FIND_ROOT_PATH /opt/arm-sysroot)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
```

```console
cmake -DCMAKE_TOOLCHAIN_FILE=arm-toolchain.cmake ..
cmake --build .
```

---

## CMake Presets Overview

- Standardized way to configure common settings
- Stored in `CMakePresets.json` or `CMakeUserPresets.json`
- Replaces long command-line flags
- Supported by IDEs (CLion, VS Code, Visual Studio)
- Introduced in CMake 3.19

---

## Configure Presets

```json
{
    "version": 6,
    "configurePresets": [
        {
            "name": "debug",
            "binaryDir": "build/debug",
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Debug",
                "BUILD_TESTS": "ON"
            }
        },
        {
            "name": "release",
            "binaryDir": "build/release",
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Release"
            }
        }
    ]
}
```

---

## Build and Test Presets

```json
{
    "version": 6,
    "buildPresets": [
        {
            "name": "debug",
            "configurePreset": "debug",
            "jobs": 8
        }
    ],
    "testPresets": [
        {
            "name": "debug",
            "configurePreset": "debug",
            "output": {"outputOnFailure": true}
        }
    ]
}
```

```console
cmake --preset debug
cmake --build --preset debug
ctest --preset debug
```

---

## Preset Inheritance and Conditions

```json
{
    "version": 6,
    "configurePresets": [
        {
            "name": "base",
            "hidden": true,
            "cacheVariables": {
                "CMAKE_EXPORT_COMPILE_COMMANDS": "ON"
            }
        },
        {
            "name": "linux-debug",
            "inherits": "base",
            "binaryDir": "build/debug",
            "condition": {
                "type": "equals",
                "lhs": "${hostSystemName}",
                "rhs": "Linux"
            },
            "cacheVariables": {
                "CMAKE_BUILD_TYPE": "Debug"
            }
        }
    ]
}
```

---

## Modern CMake: Target-Based Approach

```cmake
# Old directory-based style (avoid)
include_directories(include/)
add_definitions(-DFOO)
link_libraries(mylib)

# Modern target-based style (prefer)
target_include_directories(app PRIVATE include/)
target_compile_definitions(app PRIVATE FOO)
target_link_libraries(app PRIVATE mylib)
```

- Per-target commands give precise control
- Properties propagate correctly through dependencies
- Makes the project composable and reusable

---

## Anti-Patterns to Avoid

```cmake
# AVOID global state:
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")
include_directories(${CMAKE_SOURCE_DIR}/include)
add_definitions(-DUSE_FEATURE)
link_directories(/opt/lib)

# AVOID GLOB for sources:
file(GLOB SOURCES "src/*.cpp")

# AVOID hardcoded paths:
target_include_directories(app PRIVATE
    /home/user/mylibs/include)
```

- Global commands affect all targets in the project
- `GLOB` does not detect added or removed files
- Hardcoded paths break on other machines

---

## Summary of Modern CMake Best Practices

- Always specify `cmake_minimum_required(VERSION ...)`
- Use `target_*` commands instead of global equivalents
- Prefer `PRIVATE`, `PUBLIC`, `INTERFACE` visibility specifiers
- List source files explicitly instead of using `GLOB`
- Use out-of-source builds with `cmake -B build`
- Use `find_package()` instead of hardcoded paths
- Use presets to share configurations across a team
- Use toolchain files for cross-compilation
- Keep `CMakeLists.txt` files minimal and readable
