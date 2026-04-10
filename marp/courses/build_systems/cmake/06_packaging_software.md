# Packaging Software

---

## CPack Packaging Generators

![CPack generators: TGZ, DEB, RPM, NSIS and workflow](svg/courses/build_systems/cmake/06_packaging_software/cpack_generators.svg)

---

## Chapter Overview

- What is `CPack` and why packaging matters
- `CPack` generators overview
- Basic configuration variables
- Archive generators: `TGZ`, `ZIP`, `TXZ`
- `DEB` packaging for Debian/Ubuntu
- `RPM` packaging for Red Hat/Fedora
- `NSIS` packaging for Windows
- Package metadata
- Component-based packaging

---

## Why Packaging Matters

- Users should not need to build from source
- Packages provide a standard installation experience
- Package managers handle dependencies and upgrades
- Distributing raw binaries lacks metadata and uninstall support
- Packaging is the final step in a professional build pipeline

---

## What is CPack

- A packaging tool bundled with CMake
- Reads your `install()` rules and bundles the results
- Supports many package formats through generators
- Configured via `CPACK_*` variables in `CMakeLists.txt`
- Invoked with the `cpack` command-line tool

---

## CPack Generators Overview

| Generator | Format | Platform |
|-----------|--------|----------|
| `TGZ` | `.tar.gz` | All |
| `ZIP` | `.zip` | All |
| `TXZ` | `.tar.xz` | All |
| `DEB` | `.deb` | Debian/Ubuntu |
| `RPM` | `.rpm` | Red Hat/Fedora |
| `NSIS` | `.exe` installer | Windows |
| `DragNDrop` | `.dmg` | macOS |

---

## Basic CPack Configuration

```cmake
set(CPACK_PACKAGE_NAME "myproject")
set(CPACK_PACKAGE_VERSION_MAJOR 1)
set(CPACK_PACKAGE_VERSION_MINOR 0)
set(CPACK_PACKAGE_VERSION_PATCH 0)

include(CPack)
```

- Variables must be set before `include(CPack)`
- `include(CPack)` reads the variables and configures packaging
- The `cpack` command is then available in the build directory

---

## Essential CPACK Variables

| Variable | Purpose |
|----------|---------|
| `CPACK_PACKAGE_NAME` | Package name |
| `CPACK_PACKAGE_VERSION` | Full version string |
| `CPACK_PACKAGE_DESCRIPTION_SUMMARY` | One-line description |
| `CPACK_PACKAGE_VENDOR` | Organization name |
| `CPACK_PACKAGE_CONTACT` | Maintainer email |
| `CPACK_RESOURCE_FILE_LICENSE` | Path to license file |

---

## Package Metadata Example

```cmake
set(CPACK_PACKAGE_NAME "myapp")
set(CPACK_PACKAGE_VERSION "1.2.3")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY
    "A high-performance data processor")
set(CPACK_PACKAGE_VENDOR "Acme Corp")
set(CPACK_PACKAGE_CONTACT "dev@acme.com")
set(CPACK_RESOURCE_FILE_LICENSE
    "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")

include(CPack)
```

---

## Running cpack

```console
cd build
cpack
```

- Runs all generators listed in `CPACK_GENERATOR`
- Produces packages in the build directory
- Uses the install rules to collect files

```console
cpack -G TGZ
cpack -G ZIP
cpack -G DEB
```

- The `-G` flag selects a specific generator

---

## Selecting Default Generators

```cmake
set(CPACK_GENERATOR "TGZ;ZIP")
```

- Semicolon-separated list of generators
- All listed generators run when `cpack` is called without `-G`
- You can override at the command line with `-G`

---

## Archive Generator: TGZ

```cmake
set(CPACK_GENERATOR "TGZ")
set(CPACK_PACKAGE_NAME "myapp")
set(CPACK_PACKAGE_VERSION "1.0.0")

include(CPack)
```

```console
cd build && cpack -G TGZ
```

- Produces `myapp-1.0.0-Linux.tar.gz`
- Contains all files defined by `install()` rules
- Portable across all platforms

---

## Archive Generators: ZIP and TXZ

```cmake
set(CPACK_GENERATOR "ZIP;TXZ")

include(CPack)
```

```console
cpack -G ZIP
cpack -G TXZ
```

- `ZIP` produces `.zip` archives, common on Windows
- `TXZ` produces `.tar.xz` with better compression than `TGZ`
- All archive generators share the same `CPACK_PACKAGE_*` variables

---

## DEB Packaging Basics

```cmake
set(CPACK_GENERATOR "DEB")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "dev@acme.com")

include(CPack)
```

- Produces `.deb` packages for Debian and Ubuntu
- `CPACK_DEBIAN_PACKAGE_MAINTAINER` is required
- CPack generates the `DEBIAN/control` file automatically

---

## DEB Package Dependencies

```cmake
set(CPACK_DEBIAN_PACKAGE_DEPENDS
    "libssl3 (>= 3.0), libcurl4 (>= 7.80)")
set(CPACK_DEBIAN_PACKAGE_RECOMMENDS "python3")
set(CPACK_DEBIAN_PACKAGE_SECTION "utils")
set(CPACK_DEBIAN_PACKAGE_PRIORITY "optional")
```

- `CPACK_DEBIAN_PACKAGE_DEPENDS` lists runtime dependencies
- Version constraints use standard Debian syntax
- `RECOMMENDS` and `SUGGESTS` are optional soft dependencies

---

## DEB Automatic Dependencies

```cmake
set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS ON)
```

- Runs `dpkg-shlibdeps` to detect shared library dependencies
- Automatically populates the `Depends` field
- Requires `dpkg-dev` to be installed on the build machine
- Works well for C and C++ projects

---

## RPM Packaging Basics

```cmake
set(CPACK_GENERATOR "RPM")
set(CPACK_RPM_PACKAGE_LICENSE "MIT")

include(CPack)
```

- Produces `.rpm` packages for Red Hat, Fedora, and SUSE
- CPack generates the spec file automatically
- Requires `rpmbuild` to be installed on the build machine

---

## RPM Package Configuration

```cmake
set(CPACK_RPM_PACKAGE_GROUP "Applications/System")
set(CPACK_RPM_PACKAGE_REQUIRES
    "openssl >= 3.0, libcurl >= 7.80")
set(CPACK_RPM_PACKAGE_DESCRIPTION
    "A high-performance data processing tool.")
set(CPACK_RPM_PACKAGE_URL "https://acme.com/myapp")
```

- `CPACK_RPM_PACKAGE_REQUIRES` lists runtime dependencies
- `CPACK_RPM_PACKAGE_GROUP` categorizes the package
- RPM spec file is generated from these variables

---

## RPM Additional Options

```cmake
set(CPACK_RPM_PACKAGE_AUTOREQ ON)
set(CPACK_RPM_PACKAGE_AUTOPROV ON)
set(CPACK_RPM_PACKAGE_RELOCATABLE ON)
set(CPACK_RPM_POST_INSTALL_SCRIPT_FILE
    "${CMAKE_CURRENT_SOURCE_DIR}/scripts/postinst.sh")
```

- `AUTOREQ` and `AUTOPROV` enable automatic dependency detection
- `RELOCATABLE` allows installation to a non-default prefix
- Post-install scripts run after package installation

---

## NSIS Packaging for Windows

```cmake
set(CPACK_GENERATOR "NSIS")
set(CPACK_NSIS_DISPLAY_NAME "My Application")
set(CPACK_NSIS_PACKAGE_NAME "MyApp")
set(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES64")

include(CPack)
```

- Produces a `.exe` installer for Windows
- `NSIS` (Nullsoft Scriptable Install System) must be installed
- Creates a graphical installation wizard

---

## NSIS Installer Options

```cmake
set(CPACK_NSIS_MUI_ICON
    "${CMAKE_CURRENT_SOURCE_DIR}/icon.ico")
set(CPACK_NSIS_ENABLE_UNINSTALL_BEFORE_INSTALL ON)
set(CPACK_NSIS_MODIFY_PATH ON)
set(CPACK_NSIS_CREATE_ICONS_EXTRA
    "CreateShortCut '$SMPROGRAMS\\\\$STARTMENU_FOLDER\\\\MyApp.lnk' '$INSTDIR\\\\bin\\\\myapp.exe'")
```

- `MODIFY_PATH` adds the install directory to the system `PATH`
- Custom icons and Start Menu shortcuts are supported
- Uninstaller is generated automatically

---

## Component-Based Packaging

```cmake
install(TARGETS myapp
    RUNTIME DESTINATION bin
    COMPONENT Runtime)

install(TARGETS mylib
    LIBRARY DESTINATION lib
    COMPONENT Libraries)

install(FILES include/mylib.h
    DESTINATION include/mylib
    COMPONENT Development)
```

- Each `install()` rule is assigned to a component
- Components can be packaged separately

---

## Declaring Components with CPack

```cmake
include(CPackComponent)

cpack_add_component(Runtime
    DISPLAY_NAME "Application"
    DESCRIPTION "The main executable"
    REQUIRED)

cpack_add_component(Libraries
    DISPLAY_NAME "Shared Libraries"
    DESCRIPTION "Runtime shared libraries")

cpack_add_component(Development
    DISPLAY_NAME "Development Files"
    DESCRIPTION "Headers and CMake config"
    DEPENDS Libraries)
```

---

## Component Groups

```cmake
cpack_add_component_group(Core
    DISPLAY_NAME "Core Components"
    DESCRIPTION "Required runtime files")

cpack_add_component(Runtime
    DISPLAY_NAME "Application"
    GROUP Core)

cpack_add_component(Libraries
    DISPLAY_NAME "Shared Libraries"
    GROUP Core)

cpack_add_component(Development
    DISPLAY_NAME "Development Files"
    GROUP Core
    DEPENDS Libraries)
```

---

## Packaging Components Separately

```cmake
set(CPACK_DEB_COMPONENT_INSTALL ON)
set(CPACK_RPM_COMPONENT_INSTALL ON)
set(CPACK_ARCHIVE_COMPONENT_INSTALL ON)
```

- Produces one package per component
- Without this, all components are merged into a single package
- DEB example output:
    - `myapp-1.0.0-Runtime.deb`
    - `myapp-1.0.0-Libraries.deb`
    - `myapp-1.0.0-Development.deb`

---

## Complete Example: CMakeLists.txt

```cmake
cmake_minimum_required(VERSION 3.20)
project(myapp VERSION 1.0.0 LANGUAGES CXX)
include(GNUInstallDirs)

add_library(mylib SHARED src/mylib.cpp)
add_executable(myapp src/main.cpp)
target_link_libraries(myapp PRIVATE mylib)

install(TARGETS myapp RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    COMPONENT Runtime)
install(TARGETS mylib LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    COMPONENT Libraries)
install(FILES include/mylib.h
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/mylib
    COMPONENT Development)
```

---

## Complete Example: CPack Section

```cmake
set(CPACK_PACKAGE_NAME "myapp")
set(CPACK_PACKAGE_VERSION ${PROJECT_VERSION})
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Data processor")
set(CPACK_PACKAGE_VENDOR "Acme Corp")
set(CPACK_PACKAGE_CONTACT "dev@acme.com")
set(CPACK_RESOURCE_FILE_LICENSE
    "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE")
set(CPACK_GENERATOR "TGZ;DEB;RPM")
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "dev@acme.com")
set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS ON)
set(CPACK_RPM_PACKAGE_LICENSE "MIT")
set(CPACK_DEB_COMPONENT_INSTALL ON)
set(CPACK_RPM_COMPONENT_INSTALL ON)

include(CPack)
```

---

## Building and Packaging

```console
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
cd build
cpack -G TGZ
cpack -G DEB
cpack -G RPM
```

- Always build in `Release` mode for distribution
- Each `cpack -G` call produces the specified format
- Packages appear in the build directory
- Use `cpack --verbose` to debug packaging issues
