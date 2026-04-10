# In-Depth CMake Syntax

---

## CMake Variables and Control Flow

![CMake variables, control flow, macros and functions](svg/courses/build_systems/cmake/03_in_depth_syntax/cmake_variables_and_flow.svg)

---

## Chapter Overview

- Variables: normal, cache, and environment
- Variable expansion and lists
- String operations
- Control flow: `if`, `foreach`, `while`
- Truthiness rules
- Generator expressions
- Macros and functions
- Argument parsing with `cmake_parse_arguments`

---

## Setting Normal Variables with set()

```cmake
set(MY_VAR "Hello")
set(SRC_FILES main.cpp utils.cpp parser.cpp)

message(STATUS "Value: ${MY_VAR}")
message(STATUS "Files: ${SRC_FILES}")
```

```output
-- Value: Hello
-- Files: main.cpp;utils.cpp;parser.cpp
```

- `set()` creates a variable in the current scope
- Multiple values form a semicolon-separated list

---

## Variable Scope Rules

```cmake
set(X "global")

function(my_func)
    message(STATUS "${X}")       # "global" (inherited)
    set(X "local")
    message(STATUS "${X}")       # "local"
endfunction()

my_func()
message(STATUS "${X}")           # "global" (unchanged)
```

- Functions create a new scope with a copy of parent variables
- Changes inside functions do not propagate back

---

## PARENT_SCOPE for Returning Values

```cmake
function(get_version result_var)
    set(${result_var} "2.5.1" PARENT_SCOPE)
endfunction()

get_version(MY_VERSION)
message(STATUS "${MY_VERSION}")  # 2.5.1
```

- `PARENT_SCOPE` writes the variable to the calling scope
- The variable is not set in the function itself when using `PARENT_SCOPE`

---

## Subdirectory Scope

```cmake
# Top-level CMakeLists.txt
set(MY_VAR "top")
add_subdirectory(sub)
message(STATUS "${MY_VAR}")  # still "top"
```

```cmake
# sub/CMakeLists.txt
message(STATUS "${MY_VAR}")  # "top" (inherited)
set(MY_VAR "sub")            # only changes locally
```

- `add_subdirectory()` creates a child scope
- Child inherits parent variables but cannot modify them

---

## Cache Variables with set(... CACHE ...)

```cmake
set(MY_OPT "default" CACHE STRING "A description")
set(ENABLE_TESTS ON CACHE BOOL "Enable testing")
```

- Stored persistently in `CMakeCache.txt`
- Survive across CMake re-runs
- Set from the command line with `-D`:

```cmake
cmake -DENABLE_TESTS=OFF ..
```

---

## Cache Variable Types

| Type | Description | GUI Widget |
|------|-------------|------------|
| `BOOL` | `ON`/`OFF` toggle | Checkbox |
| `STRING` | Arbitrary text | Text field |
| `PATH` | Directory path | Dir chooser |
| `FILEPATH` | File path | File chooser |
| `INTERNAL` | Hidden from GUI | None |

```cmake
set(MY_BOOL ON CACHE BOOL "Enable feature")
set(MY_PATH "/usr/local" CACHE PATH "Install prefix")
set(MY_FILE "config.txt" CACHE FILEPATH "Config file")
```

---

## The FORCE Keyword

```cmake
# Without FORCE: sets only if not already in cache
set(MY_VAR "value" CACHE STRING "desc")

# With FORCE: always overwrites
set(MY_VAR "new_value" CACHE STRING "desc" FORCE)
```

- Without `FORCE`, user-supplied values are preserved
- Use `FORCE` sparingly as it overrides user choices
- `INTERNAL` cache variables always behave as if `FORCE` is set

---

## Environment Variables

```cmake
# Reading environment variables
message(STATUS "Home: $ENV{HOME}")
message(STATUS "Path: $ENV{PATH}")

# Setting environment variables (current process only)
set(ENV{CXX} "/usr/bin/g++-12")
message(STATUS "CXX: $ENV{CXX}")
```

- Use `$ENV{VAR}` to access environment variables
- Changes only affect the running CMake process
- Build tools will not see `set(ENV{...})` changes

---

## Variable Expansion

```cmake
set(MY_VAR "world")
message("Hello ${MY_VAR}")          # Hello world
message("Escaped \${MY_VAR}")       # ${MY_VAR}
message("Undefined: ${NO_SUCH}")    # empty string
```

- `${VAR}` expands a variable
- Undefined variables expand to an empty string
- Use backslash to escape literal `${}`

---

## Nested Variable Expansion

```cmake
set(lang "CXX")
set(CMAKE_CXX_COMPILER "/usr/bin/g++")

# Nested expansion: inner ${lang} resolves first
message(STATUS "${CMAKE_${lang}_COMPILER}")
```

```output
-- /usr/bin/g++
```

- CMake resolves from the inside out
- Useful for writing generic code over multiple languages

---

## Lists in CMake

```cmake
set(MY_LIST a b c)         # creates a;b;c
set(MY_LIST "a;b;c")       # equivalent

list(LENGTH MY_LIST len)    # len = 3
list(GET MY_LIST 0 first)  # first = a
list(APPEND MY_LIST d)     # a;b;c;d
list(REMOVE_ITEM MY_LIST b) # a;c;d
```

- Lists are semicolon-separated strings internally
- The `list()` command provides list operations
- Quoting preserves a string as a single element

---

## Common list() Operations

| Operation | Example | Description |
|-----------|---------|-------------|
| `LENGTH` | `list(LENGTH L n)` | Element count |
| `GET` | `list(GET L 0 val)` | Element at index |
| `APPEND` | `list(APPEND L x)` | Add to end |
| `PREPEND` | `list(PREPEND L x)` | Add to front |
| `REMOVE_ITEM` | `list(REMOVE_ITEM L x)` | Remove by value |
| `REMOVE_AT` | `list(REMOVE_AT L 0)` | Remove by index |
| `FIND` | `list(FIND L x idx)` | Find index |
| `SORT` | `list(SORT L)` | Sort in place |
| `JOIN` | `list(JOIN L "," out)` | Join with separator |

---

## String Operations: FIND and REPLACE

```cmake
set(MY_STR "Hello World")

string(FIND "${MY_STR}" "World" pos)
message(STATUS "Found at: ${pos}")  # 6

string(REPLACE "World" "CMake" result "${MY_STR}")
message(STATUS "${result}")         # Hello CMake
```

- `string(FIND)` returns the index or `-1` if not found
- `string(REPLACE)` replaces all occurrences

---

## String Operations: REGEX

```cmake
set(version_str "version 3.20.5")

string(REGEX MATCH "[0-9]+\\.[0-9]+" ver "${version_str}")
message(STATUS "Version: ${ver}")  # 3.20

string(REGEX REPLACE "([0-9]+)\\.([0-9]+)" "\\1_\\2"
    result "${ver}")
message(STATUS "Result: ${result}")  # 3_20
```

- `REGEX MATCH` extracts the first match
- `REGEX MATCHALL` extracts all matches into a list
- `REGEX REPLACE` substitutes matches

---

## More String Operations

```cmake
set(s "Hello World")

string(LENGTH "${s}" len)         # 11
string(TOUPPER "${s}" upper)      # HELLO WORLD
string(TOLOWER "${s}" lower)      # hello world
string(SUBSTRING "${s}" 0 5 sub)  # Hello
string(STRIP "  hi  " stripped)   # hi
string(CONCAT out "a" "b" "c")   # abc
```

- CMake provides a rich set of string manipulation tools
- All results are stored in an output variable

---

## if() Statements

```cmake
if(MY_VAR)
    message("MY_VAR is truthy")
elseif(MY_VAR STREQUAL "specific")
    message("MY_VAR is 'specific'")
else()
    message("Fallback")
endif()
```

- `if()` evaluates a condition
- `elseif()` and `else()` are optional
- Always close with `endif()`

---

## Truthiness in CMake

Truthy values:

```misc
1, ON, YES, TRUE, Y, any non-zero number
```

Falsy values:

```misc
0, OFF, NO, FALSE, N, IGNORE, NOTFOUND,
empty string, string ending in -NOTFOUND
```

- These are case-insensitive
- An undefined variable evaluates as falsy

---

## Comparison Operators

```cmake
if(x EQUAL 5)               # Numeric equality
if(x LESS 10)               # Numeric less than
if(x GREATER 3)             # Numeric greater than
if(x LESS_EQUAL 10)         # Numeric <=
if(x GREATER_EQUAL 3)       # Numeric >=
if(x STREQUAL "hello")      # String equality
if(x STRLESS "b")           # String less than
if(x MATCHES "^[0-9]+$")    # Regex match
```

- Numeric operators work on integers
- String operators compare lexicographically

---

## EXISTS, DEFINED, AND/OR/NOT

```cmake
if(EXISTS "/path/to/file.txt")
    message("File exists")
endif()

if(DEFINED MY_VAR)
    message("MY_VAR is defined")
endif()

if(DEFINED ENV{HOME})
    message("HOME env var is set")
endif()

if(A AND NOT B)
    message("A is true and B is false")
endif()
```

---

## foreach() Loops: Basic Forms

```cmake
# Iterate over explicit items
foreach(item apple banana cherry)
    message(STATUS "${item}")
endforeach()

# Iterate over a list variable
set(FRUITS apple banana cherry)
foreach(fruit IN LISTS FRUITS)
    message(STATUS "${fruit}")
endforeach()
```

- `IN LISTS` iterates over one or more list variables
- `IN ITEMS` iterates over literal values

---

## foreach() with RANGE

```cmake
# 0 to 5 inclusive
foreach(i RANGE 5)
    message(STATUS "i = ${i}")
endforeach()

# Start, stop, step
foreach(i RANGE 0 10 2)
    message(STATUS "i = ${i}")
endforeach()
```

```output
-- i = 0
-- i = 2
-- i = 4
-- i = 6
-- i = 8
-- i = 10
```

- `RANGE stop` includes both 0 and stop
- `RANGE start stop step` provides full control

---

## foreach() with IN ITEMS and IN LISTS

```cmake
set(LIST_A x y)
set(LIST_B 1 2)

foreach(val IN LISTS LIST_A LIST_B)
    message(STATUS "${val}")
endforeach()
# x, y, 1, 2

foreach(val IN ITEMS a b c)
    message(STATUS "${val}")
endforeach()
# a, b, c
```

- `IN LISTS` takes variable names (without `${}`)
- `IN ITEMS` takes literal values

---

## while() Loops

```cmake
set(counter 0)
while(counter LESS 5)
    message(STATUS "counter = ${counter}")
    math(EXPR counter "${counter} + 1")
endwhile()
```

```output
-- counter = 0
-- counter = 1
-- counter = 2
-- counter = 3
-- counter = 4
```

- Less common than `foreach()`
- Useful for iterative algorithms in CMake scripts

---

## Generator Expressions Introduction

- Evaluated at **build system generation time**, not configure time
- Syntax: `$<EXPRESSION>` or `$<EXPRESSION:value>`
- Used in target properties and certain commands
- Essential for multi-config generators (Visual Studio, Xcode)

```cmake
# Regular variable: evaluated at configure time
# Generator expression: evaluated at generation time
target_compile_definitions(app PRIVATE
    $<$<CONFIG:Debug>:DEBUG_MODE>
)
```

---

## Common Generator Expressions

| Expression | Description |
|------------|-------------|
| `$<CONFIG:cfg>` | 1 if config matches |
| `$<BOOL:val>` | 1 if truthy |
| `$<AND:a,b>` | Logical AND |
| `$<OR:a,b>` | Logical OR |
| `$<NOT:a>` | Logical NOT |
| `$<IF:cond,t,f>` | Conditional value |
| `$<TARGET_FILE:tgt>` | Full path to target file |
| `$<TARGET_FILE_DIR:tgt>` | Directory of target file |
| `$<BUILD_INTERFACE:...>` | Value when building |
| `$<INSTALL_INTERFACE:...>` | Value when installed |
| `$<CXX_COMPILER_ID:id>` | 1 if compiler matches |

---

## Using $<TARGET_FILE:tgt>

```cmake
add_library(mylib SHARED mylib.cpp)
add_executable(app main.cpp)
target_link_libraries(app PRIVATE mylib)

add_custom_command(TARGET app POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:mylib>
        $<TARGET_FILE_DIR:app>
)
```

- `$<TARGET_FILE:tgt>` resolves to the full path of the built binary
- Works correctly across all platforms and configurations

---

## Using $<BUILD_INTERFACE:...>

```cmake
target_include_directories(mylib PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
```

- `BUILD_INTERFACE` applies when building the project
- `INSTALL_INTERFACE` applies when consuming the installed package
- Essential for writing reusable CMake packages

---

## When to Use Generator Expressions vs Variables

Use **regular variables** when:

- The value is known at configure time
- You need the value in `if()` or `message()`
- You are setting paths or options for single-config builds

Use **generator expressions** when:

- The value depends on the build configuration
- You need per-config compile definitions or flags
- You are writing portable packages (build vs install paths)
- You are working with multi-config generators

---

## Macros: macro() / endmacro()

```cmake
macro(print_banner msg)
    message(STATUS "===========================")
    message(STATUS "  ${msg}")
    message(STATUS "===========================")
endmacro()

print_banner("Build Started")
```

```output
-- ===========================
-- Build Started
-- ===========================
```

- Macros execute in the caller's scope (text substitution)

---

## Macro Variable Scope Behavior

```cmake
set(X "original")

macro(change_x)
    set(X "modified by macro")
endmacro()

change_x()
message(STATUS "${X}")  # "modified by macro"
```

- Macros do **not** create a new scope
- Any `set()` inside a macro modifies the caller's variables
- Similar to C preprocessor macros in this regard

---

## Functions: function() / endfunction()

```cmake
function(setup_target target_name)
    target_compile_features(${target_name} PRIVATE cxx_std_17)
    target_compile_options(${target_name} PRIVATE -Wall -Wextra)
endfunction()

add_executable(app main.cpp)
setup_target(app)
```

- Functions create a new variable scope
- Parameters are positional

---

## Function Special Variables: ARGC, ARGV, ARGN

```cmake
function(my_func required_arg)
    message(STATUS "ARGC: ${ARGC}")
    message(STATUS "ARGV: ${ARGV}")
    message(STATUS "ARGN: ${ARGN}")
    message(STATUS "Required: ${required_arg}")
endfunction()

my_func(hello extra1 extra2)
```

```output
-- ARGC: 3
-- ARGV: hello;extra1;extra2
-- ARGN: extra1;extra2
-- Required: hello
```

- `ARGC` is the total argument count
- `ARGV` is all arguments as a list
- `ARGN` is the extra (unnamed) arguments

---

## Difference Between Macros and Functions

```cmake
macro(test_macro)
    set(VAR "macro")
endmacro()

function(test_func)
    set(VAR "function")
endfunction()

set(VAR "original")
test_macro()
message(STATUS "${VAR}")  # "macro" (scope modified)

set(VAR "original")
test_func()
message(STATUS "${VAR}")  # "original" (scope intact)
```

- **Macros**: no new scope, modifies caller directly
- **Functions**: new scope, caller is protected

---

## cmake_parse_arguments for Complex Parsing

```cmake
function(add_my_library)
    cmake_parse_arguments(ARG
        "STATIC;SHARED"            # Boolean options
        "NAME;STANDARD"            # Single-value keywords
        "SOURCES;DEPENDS"          # Multi-value keywords
        ${ARGN}
    )

    if(ARG_STATIC)
        add_library(${ARG_NAME} STATIC ${ARG_SOURCES})
    else()
        add_library(${ARG_NAME} SHARED ${ARG_SOURCES})
    endif()

    target_link_libraries(${ARG_NAME} PRIVATE ${ARG_DEPENDS})
endfunction()
```

---

## Using cmake_parse_arguments in Practice

```cmake
add_my_library(
    NAME mylib
    STATIC
    STANDARD 17
    SOURCES
        src/core.cpp
        src/utils.cpp
    DEPENDS
        pthread
        Boost::filesystem
)
```

- Boolean options are `TRUE` if present, `FALSE` if absent
- `ARG_UNPARSED_ARGUMENTS` holds any unrecognized arguments
- `ARG_KEYWORDS_MISSING_VALUES` holds keywords with no values
- The recommended approach for reusable CMake functions
