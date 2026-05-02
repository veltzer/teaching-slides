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
# Installing Software

---

## CMake Install Workflow

![cmake_install_workflow](svg/courses/build_systems/cmake/05_installing_software/cmake_install_workflow.svg)

---

## Install Destinations

![install_destinations](svg/courses/build_systems/cmake/05_installing_software/install_destinations.svg)

---

## Chapter Overview

- Why install rules matter
- `CMAKE_INSTALL_PREFIX` and default locations
- Installing targets, files, directories, and scripts
- Component-based installation
- `GNUInstallDirs` module
- Exported targets and package config files

---

## Why Install Rules Matter

- Building produces artifacts scattered in the build tree
- Install rules copy them to a well-known, organized location
- Other projects can then find and link your libraries
- Required for packaging with `CPack`
- Without install rules, your project is not distributable

---

## CMAKE_INSTALL_PREFIX

```cmake
cmake -DCMAKE_INSTALL_PREFIX=/opt/myproject ..
cmake --build .
cmake --install .
```

- Controls the root directory for all installed files
- All `DESTINATION` paths are relative to this prefix
- Can be overridden at install time with `--prefix`

---

## Default Install Locations

| Platform | Default Prefix |
|----------|----------------|
| Linux / macOS | `/usr/local` |
| Windows | `C:\Program Files\<project>` |

- The `--prefix` flag overrides `CMAKE_INSTALL_PREFIX`

```bash
cmake --install . --prefix /tmp/staging
```

---

## DESTDIR for Packaging

```bash
DESTDIR=/tmp/package cmake --install .
```

- Prepends `DESTDIR` to all absolute paths
- Result: `/tmp/package/usr/local/bin/myapp`
- Does not affect the paths stored inside config files
- Commonly used by distro package builders

---

## install(TARGETS) - Executables

```cmake
add_executable(myapp main.cpp)

install(TARGETS myapp
    RUNTIME DESTINATION bin
)
```

- Copies the built executable to `${CMAKE_INSTALL_PREFIX}/bin`
- `RUNTIME` selects executables and DLLs on Windows

---

## install(TARGETS) - Libraries

```cmake
add_library(mylib SHARED src/mylib.cpp)

install(TARGETS mylib
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
)
```

- `LIBRARY` handles shared libraries (`.so`, `.dylib`)
- `ARCHIVE` handles static libraries (`.a`, `.lib`)
- Both can point to the same or different destinations

---

## RUNTIME, LIBRARY, and ARCHIVE

| Component | File Types | Typical Destination |
|-----------|-----------|---------------------|
| `RUNTIME` | `.exe`, `.dll` | `bin/` |
| `LIBRARY` | `.so`, `.dylib` | `lib/` |
| `ARCHIVE` | `.a`, `.lib`, import libs | `lib/` |

- CMake automatically picks the correct component per platform
- You should specify all three for maximum portability

---

## install(TARGETS) - Multiple Targets

```cmake
install(TARGETS mylib myapp
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    INCLUDES DESTINATION include
)
```

- Multiple targets in a single command
- `INCLUDES DESTINATION` sets the interface include directory
- Each target is routed to the matching component

---

## install(FILES)

```cmake
install(FILES
    include/mylib/mylib.h
    include/mylib/utils.h
    DESTINATION include/mylib
)
```

- Copies files without execute permission
- Creates destination directories as needed
- Users can then write `#include <mylib/mylib.h>`

---

## install(DIRECTORY)

```cmake
install(DIRECTORY include/
    DESTINATION include
    FILES_MATCHING PATTERN "*.h"
)
```

- Copies an entire directory tree
- Trailing `/` means copy contents, not the directory itself
- `FILES_MATCHING PATTERN` filters which files are included
- Without the trailing `/`, `include` itself is copied

---

## install(DIRECTORY) - Excluding Files

```cmake
install(DIRECTORY assets/
    DESTINATION share/myapp
    PATTERN ".git" EXCLUDE
    PATTERN "*.bak" EXCLUDE
)
```

- `EXCLUDE` removes matching entries from the install
- Multiple patterns can be combined
- Useful for stripping version control or temporary files

---

## install(PROGRAMS) for Scripts

```cmake
install(PROGRAMS
    scripts/deploy.sh
    scripts/run_tests.sh
    DESTINATION bin
)
```

- Works like `install(FILES)` but sets execute permission
- Use for shell scripts, Python scripts, or other interpreted programs
- The scripts are installed alongside compiled executables

---

## Component-Based Installation

```cmake
install(TARGETS myapp
    RUNTIME DESTINATION bin
    COMPONENT Runtime
)

install(TARGETS mylib
    LIBRARY DESTINATION lib
    COMPONENT Libraries
)

install(FILES include/mylib.h
    DESTINATION include/mylib
    COMPONENT Development
)
```

---

## Installing a Single Component

```bash
cmake --install . --component Runtime
cmake --install . --component Development
```

- Only files tagged with that component are installed
- Useful for separating runtime from development files
- `CPack` can create separate packages per component

---

## GNUInstallDirs Module

```cmake
include(GNUInstallDirs)

install(TARGETS mylib
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

install(FILES include/mylib.h
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/mylib
)
```

- Provides platform-appropriate install directories
- Handles `lib` vs `lib64` on 64-bit Linux automatically

---

## GNUInstallDirs Variables

| Variable | Default Value |
|----------|---------------|
| `CMAKE_INSTALL_BINDIR` | `bin` |
| `CMAKE_INSTALL_LIBDIR` | `lib` or `lib64` |
| `CMAKE_INSTALL_INCLUDEDIR` | `include` |
| `CMAKE_INSTALL_DATADIR` | `share` |
| `CMAKE_INSTALL_MANDIR` | `share/man` |
| `CMAKE_INSTALL_SYSCONFDIR` | `etc` |

- Always prefer these over hardcoded paths

---

## Exported Targets Overview

- Allow other CMake projects to consume your library
- Provide imported targets with all properties set
- Consumers do not need to know compiler flags or paths
- The modern replacement for `FindXxx.cmake` modules

---

## install(EXPORT) - Creating an Export Set

```cmake
install(TARGETS mylib
    EXPORT MyLibTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    INCLUDES DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
```

- `EXPORT MyLibTargets` registers the target for export
- Multiple targets can belong to the same export set

---

## install(EXPORT) - Installing the Export

```cmake
install(EXPORT MyLibTargets
    FILE MyLibTargets.cmake
    NAMESPACE MyLib::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib
)
```

- Generates `MyLibTargets.cmake` at install time
- `NAMESPACE` prefixes all target names with `MyLib::`
- Consumers use `MyLib::mylib` as the target name

---

## Creating a Package Config File

Create `MyLibConfig.cmake.in`:

```cmake
@PACKAGE_INIT@

include("${CMAKE_CURRENT_LIST_DIR}/MyLibTargets.cmake")

check_required_components(MyLib)
```

- `@PACKAGE_INIT@` is replaced with path setup code
- `check_required_components()` validates required components

---

## CMakePackageConfigHelpers Module

```cmake
include(CMakePackageConfigHelpers)

configure_package_config_file(
    MyLibConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake
    INSTALL_DESTINATION
        ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib
)
```

- Handles path relocation between build and install trees
- Ensures the config file works regardless of install prefix

---

## write_basic_package_version_file

```cmake
write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)
```

- Generates a version file for `find_package()` version checks
- `VERSION` defaults to `PROJECT_VERSION` if omitted

---

## VERSION Compatibility Modes

| Mode | Meaning |
|------|---------|
| `AnyNewerVersion` | Any version >= requested |
| `SameMajorVersion` | Same major, any minor/patch |
| `SameMinorVersion` | Same major.minor, any patch |
| `ExactVersion` | Exact match required |

```cmake
# Consumer requests version 1.2
find_package(MyLib 1.2 REQUIRED)
# SameMajorVersion: 1.5.0 matches, 2.0.0 does not
```

---

## Installing Config and Version Files

```cmake
install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib
)
```

- Both files must be in the same directory
- The directory name should match the package name

---

## Complete Install + Export Example

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyLib VERSION 1.0.0 LANGUAGES CXX)
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

add_library(mylib src/mylib.cpp)
target_include_directories(mylib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

install(TARGETS mylib EXPORT MyLibTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
install(DIRECTORY include/
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
```

---

## Complete Example (Continued)

```cmake
install(EXPORT MyLibTargets
    FILE MyLibTargets.cmake
    NAMESPACE MyLib::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)

configure_package_config_file(
    MyLibConfig.cmake.in
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake
    INSTALL_DESTINATION
        ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)

write_basic_package_version_file(
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion)

install(FILES
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfig.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/MyLib)
```

---

## Installed Package Layout

```tree
/usr/local/
    lib/
        libmylib.so
        cmake/
            MyLib/
                MyLibConfig.cmake
                MyLibConfigVersion.cmake
                MyLibTargets.cmake
    include/
        mylib.h
```

---

## Testing the Installation

```bash
cmake -B build -DCMAKE_INSTALL_PREFIX=/tmp/test_install
cmake --build build
cmake --install build
```

```cmake
# In a separate test project:
cmake_minimum_required(VERSION 3.20)
project(consumer LANGUAGES CXX)

find_package(MyLib 1.0 REQUIRED)

add_executable(app main.cpp)
target_link_libraries(app PRIVATE MyLib::mylib)
```

---

## Building Against the Test Install

```bash
cmake -B consumer_build \
    -DCMAKE_PREFIX_PATH=/tmp/test_install \
    consumer/
cmake --build consumer_build
./consumer_build/app
```

- `CMAKE_PREFIX_PATH` tells CMake where to search for packages
- Verifies that install rules and exports work correctly
- Always test installation before releasing your project
