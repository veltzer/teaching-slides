# Importing Dependencies in CMake

---

## Chapter Overview

- Why dependency management matters
- `find_package()` basics and search modes
- Package search paths and `CMAKE_PREFIX_PATH`
- Variables vs imported targets
- Manual find commands: `find_library()`, `find_path()`, and more
- Writing custom `FindXXX.cmake` modules
- Exported and `IMPORTED` targets
- `FetchContent` module for downloading dependencies
- `pkg-config` integration
- `add_subdirectory()` for local dependencies

---

## Why Dependency Management Matters

- Real projects depend on dozens of external libraries
- Each library may be installed in different locations
- Different platforms use different conventions
- Hard-coded paths break portability

```cmake
# Bad: hard-coded paths
target_include_directories(myapp PRIVATE /usr/local/include/openssl)
target_link_libraries(myapp /usr/local/lib/libssl.so)
```

- CMake provides tools to find and consume dependencies portably

---

## find_package() - Basic Usage

```cmake
find_package(OpenSSL REQUIRED)

target_link_libraries(myapp PRIVATE OpenSSL::SSL OpenSSL::Crypto)
```

- Searches for a package and sets variables and/or imported targets
- `REQUIRED` causes a fatal error if the package is not found
- Without `REQUIRED`, check `OpenSSL_FOUND` manually

```cmake
find_package(OpenSSL)
if(OpenSSL_FOUND)
    target_link_libraries(myapp PRIVATE OpenSSL::SSL)
endif()
```

---

## find_package() - Version Constraints

```cmake
find_package(Boost 1.70 REQUIRED)
find_package(Qt6 6.2 EXACT REQUIRED)
find_package(ZLIB 1.2.11...<1.3 REQUIRED)
```

- Specify a minimum version after the package name
- `EXACT` requires an exact version match
- Version ranges (CMake 3.19+) use `MIN...<MAX` syntax
- The package provides its version; CMake compares automatically

---

## find_package() - Components

```cmake
find_package(Boost 1.70 REQUIRED COMPONENTS filesystem system)
find_package(Qt6 REQUIRED COMPONENTS Widgets Network)
```

- `COMPONENTS` requests specific parts of a package
- `OPTIONAL_COMPONENTS` allows some components to be missing

```cmake
find_package(Qt6 REQUIRED
    COMPONENTS Widgets
    OPTIONAL_COMPONENTS WebEngine
)
if(TARGET Qt6::WebEngine)
    target_link_libraries(myapp PRIVATE Qt6::WebEngine)
endif()
```

---

## CONFIG vs MODULE Mode

- `find_package()` has two search modes:
    - **Module mode**: searches for `FindXXX.cmake` files
    - **Config mode**: searches for `XXXConfig.cmake` or `xxx-config.cmake`
- By default, CMake tries Module mode first, then Config mode

```cmake
# Force a specific mode
find_package(MyLib MODULE REQUIRED)
find_package(MyLib CONFIG REQUIRED)
```

- Module mode: uses `Find` scripts shipped with CMake or your project
- Config mode: uses config files shipped by the library itself

---

## How find_package() Searches - Module Mode

- CMake looks for `FindXXX.cmake` in:
    1. Directories listed in `CMAKE_MODULE_PATH`
    1. CMake's built-in module directory

```cmake
# Add your project's cmake/ folder to the search path
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

# Now CMake can find cmake/FindMyLib.cmake
find_package(MyLib REQUIRED)
```

- CMake ships with many built-in Find modules
- Run `cmake --help-module-list` to see them all

---

## How find_package() Searches - Config Mode

- CMake looks for `XXXConfig.cmake` in platform-specific locations:
    - `<prefix>/lib/cmake/XXX/`
    - `<prefix>/share/XXX/cmake/`
    - `<prefix>/cmake/`
- Prefixes searched include `/usr`, `/usr/local`, and others
- The `XXX_DIR` variable can point directly to the config file location

```cmake
# Hint where to find the config file
set(MyLib_DIR "/opt/mylib/lib/cmake/MyLib")
find_package(MyLib CONFIG REQUIRED)
```

---

## CMAKE_PREFIX_PATH

```cmake
cmake -DCMAKE_PREFIX_PATH="/opt/custom;/home/user/libs" ..
```

- A semicolon-separated list of directories to search
- Each prefix is searched for `include/`, `lib/`, `lib/cmake/`, etc.
- Can be set as a CMake variable or environment variable

```cmake
# In CMakeLists.txt
list(APPEND CMAKE_PREFIX_PATH "/opt/custom")

# Or via environment variable
# export CMAKE_PREFIX_PATH="/opt/custom:/home/user/libs"
```

- Preferred way to point CMake at non-standard install locations

---

## Using Found Packages - Variables

- Older Find modules set variables like:
    - `XXX_FOUND` - whether the package was found
    - `XXX_INCLUDE_DIRS` - header directories
    - `XXX_LIBRARIES` - libraries to link
    - `XXX_VERSION` - package version

```cmake
find_package(ZLIB REQUIRED)

target_include_directories(myapp PRIVATE ${ZLIB_INCLUDE_DIRS})
target_link_libraries(myapp PRIVATE ${ZLIB_LIBRARIES})
```

- This approach is error-prone and does not propagate transitive dependencies

---

## Using Found Packages - Imported Targets

- Modern packages provide imported targets (e.g., `ZLIB::ZLIB`)
- Imported targets carry include dirs, compile flags, and link deps

```cmake
find_package(ZLIB REQUIRED)
target_link_libraries(myapp PRIVATE ZLIB::ZLIB)
```

- One line replaces both `target_include_directories` and `target_link_libraries`
- Transitive dependencies are handled automatically
- Always prefer imported targets over variables when available

---

## find_library() and find_path()

```cmake
find_library(MATH_LIB m)
find_path(MATH_INCLUDE math.h)

if(MATH_LIB AND MATH_INCLUDE)
    target_include_directories(myapp PRIVATE ${MATH_INCLUDE})
    target_link_libraries(myapp PRIVATE ${MATH_LIB})
endif()
```

- `find_library()` searches for a library file by name
- `find_path()` searches for a directory containing a header
- Both accept `HINTS` and `PATHS` to guide the search

```cmake
find_library(MYLIB mylib HINTS /opt/mylib/lib)
find_path(MYLIB_INC mylib.h HINTS /opt/mylib/include)
```

---

## find_program() and find_file()

```cmake
find_program(CLANG_FORMAT clang-format)
if(CLANG_FORMAT)
    add_custom_target(format
        COMMAND ${CLANG_FORMAT} -i ${ALL_SOURCES}
    )
endif()
```

- `find_program()` locates an executable on the system
- `find_file()` locates a specific file by full path

```cmake
find_file(GPL_LICENSE
    NAMES LICENSE.GPL LICENSE.GPL3
    PATHS /usr/share/licenses
)
```

- All four find commands share the same options: `HINTS`, `PATHS`, `PATH_SUFFIXES`

---

## Writing a FindXXX.cmake Module

```cmake
# cmake/FindMyMath.cmake
find_path(MYMATH_INCLUDE_DIR mymath.h
    HINTS ${MYMATH_ROOT}/include
)
find_library(MYMATH_LIBRARY mymath
    HINTS ${MYMATH_ROOT}/lib
)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(MyMath
    REQUIRED_VARS MYMATH_LIBRARY MYMATH_INCLUDE_DIR
)
```

- Use `find_path()` and `find_library()` to locate pieces
- `FindPackageHandleStandardArgs` handles `REQUIRED`, version checks, and messaging

---

## FindXXX.cmake - Creating an Imported Target

```cmake
# Continue from the previous slide
if(MyMath_FOUND AND NOT TARGET MyMath::MyMath)
    add_library(MyMath::MyMath UNKNOWN IMPORTED)
    set_target_properties(MyMath::MyMath PROPERTIES
        IMPORTED_LOCATION "${MYMATH_LIBRARY}"
        INTERFACE_INCLUDE_DIRECTORIES "${MYMATH_INCLUDE_DIR}"
    )
endif()
```

- Create an `IMPORTED` target so consumers use `target_link_libraries`
- Guard with `NOT TARGET` to avoid redefinition
- `UNKNOWN IMPORTED` lets CMake detect the library type

---

## Exported Targets - How Libraries Export Themselves

```cmake
# In the library's CMakeLists.txt
install(TARGETS mylib
    EXPORT MyLibTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    INCLUDES DESTINATION include
)

install(EXPORT MyLibTargets
    NAMESPACE MyLib::
    DESTINATION lib/cmake/MyLib
)
```

- `install(EXPORT)` generates a file with imported target definitions
- Consumers use `find_package(MyLib CONFIG)` to load them
- The `NAMESPACE` prefix avoids name collisions

---

## Generating a Package Config File

```cmake
include(CMakePackageConfigHelpers)

configure_package_config_file(
    cmake/MyLibConfig.cmake.in
    "${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake"
    INSTALL_DESTINATION lib/cmake/MyLib
)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake"
    DESTINATION lib/cmake/MyLib
)
```

---

## Using IMPORTED Targets Directly

```cmake
add_library(vendor::zstd STATIC IMPORTED)
set_target_properties(vendor::zstd PROPERTIES
    IMPORTED_LOCATION "${CMAKE_SOURCE_DIR}/vendor/lib/libzstd.a"
    INTERFACE_INCLUDE_DIRECTORIES "${CMAKE_SOURCE_DIR}/vendor/include"
    INTERFACE_COMPILE_DEFINITIONS "ZSTD_STATIC_LINKING_ONLY"
)

target_link_libraries(myapp PRIVATE vendor::zstd)
```

- You can create `IMPORTED` targets manually without a Find module
- Useful for vendored or pre-built libraries
- `INTERFACE_*` properties propagate to consumers automatically

---

## FetchContent Module (CMake 3.11+)

```cmake
include(FetchContent)

FetchContent_Declare(json
    GIT_REPOSITORY https://github.com/nlohmann/json.git
    GIT_TAG v3.11.2
)

FetchContent_MakeAvailable(json)

target_link_libraries(myapp PRIVATE nlohmann_json::nlohmann_json)
```

- Downloads and builds dependencies at configure time
- The dependency becomes part of your build tree
- No need to pre-install anything

---

## FetchContent_Declare Options

```cmake
FetchContent_Declare(mylib
    GIT_REPOSITORY https://github.com/example/mylib.git
    GIT_TAG main
    GIT_SHALLOW TRUE
)

FetchContent_Declare(data
    URL https://example.com/data-1.0.tar.gz
    URL_HASH SHA256=abc123...
)
```

- `GIT_SHALLOW TRUE` speeds up cloning large repos
- `URL` supports tarballs and zip archives
- `URL_HASH` verifies download integrity
- Always pin `GIT_TAG` to a specific commit or tag for reproducibility

---

## FetchContent_MakeAvailable Internals

```cmake
FetchContent_Declare(dep1 GIT_REPOSITORY ... GIT_TAG ...)

# MakeAvailable is equivalent to:
FetchContent_GetProperties(dep1)
if(NOT dep1_POPULATED)
    FetchContent_Populate(dep1)
    add_subdirectory(${dep1_SOURCE_DIR} ${dep1_BINARY_DIR})
endif()

# But MakeAvailable is simpler:
FetchContent_MakeAvailable(dep1)
```

- `FetchContent_Populate()` downloads the source
- `add_subdirectory()` integrates it into the build
- `MakeAvailable` does both in one call (CMake 3.14+)

---

## FetchContent vs ExternalProject

| Feature | FetchContent | ExternalProject |
|---|---|---|
| When it runs | Configure time | Build time |
| Targets visible | Yes | No |
| Build integration | Full | Separate build |
| Use case | Source deps | Pre-built deps |

- `FetchContent` is preferred for most source-level dependencies
- `ExternalProject` is useful when you need a completely isolated build
- `ExternalProject` targets are not available at configure time

---

## pkg-config Integration

```cmake
find_package(PkgConfig REQUIRED)

pkg_check_modules(LIBCURL REQUIRED IMPORTED_TARGET libcurl)
target_link_libraries(myapp PRIVATE PkgConfig::LIBCURL)
```

- Many Unix libraries ship `.pc` files for `pkg-config`
- `IMPORTED_TARGET` creates a modern imported target (CMake 3.6+)
- Without `IMPORTED_TARGET`, you get variables instead:

```cmake
pkg_check_modules(LIBCURL REQUIRED libcurl)
target_include_directories(myapp PRIVATE ${LIBCURL_INCLUDE_DIRS})
target_link_libraries(myapp PRIVATE ${LIBCURL_LIBRARIES})
```

---

## add_subdirectory() for Local Dependencies

```cmake
# Project layout:
# project/
#   CMakeLists.txt
#   libs/
#     mathlib/
#       CMakeLists.txt
#   apps/
#     myapp/
#       CMakeLists.txt

# Top-level CMakeLists.txt
add_subdirectory(libs/mathlib)
add_subdirectory(apps/myapp)

# apps/myapp/CMakeLists.txt
target_link_libraries(myapp PRIVATE mathlib)
```

- `add_subdirectory()` includes another `CMakeLists.txt` into the build
- Targets defined in subdirectories are visible to the rest of the project

---

## Practical Patterns - Try Config, Then Find

```cmake
# Prefer config mode, fall back to module mode
find_package(MyLib CONFIG QUIET)
if(NOT MyLib_FOUND)
    find_package(MyLib MODULE REQUIRED)
endif()
```

- Config files are more reliable and self-contained
- Fall back to Find modules for packages that do not ship configs
- `QUIET` suppresses messages when the first attempt fails

---

## Practical Patterns - Dependency Options

```cmake
option(USE_SYSTEM_JSON "Use system nlohmann_json" OFF)

if(USE_SYSTEM_JSON)
    find_package(nlohmann_json REQUIRED)
else()
    FetchContent_Declare(json
        GIT_REPOSITORY https://github.com/nlohmann/json.git
        GIT_TAG v3.11.2
    )
    FetchContent_MakeAvailable(json)
endif()

target_link_libraries(myapp PRIVATE nlohmann_json::nlohmann_json)
```

- Let users choose between system and vendored dependencies
- The consuming code stays the same either way

---

## Chapter Summary

- `find_package()` is the primary tool for locating dependencies
    - Config mode loads library-provided config files
    - Module mode runs `FindXXX.cmake` scripts
- Always prefer imported targets over raw variables
- `FetchContent` downloads and builds dependencies at configure time
- `pkg_check_modules()` integrates with `pkg-config` on Unix
- `add_subdirectory()` works for in-tree or local dependencies
- Provide options to let users choose system vs vendored libraries
