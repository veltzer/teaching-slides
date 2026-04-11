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
# Testing with CTest

---

## Why Test Integration Matters

- Automated testing catches regressions early
- Build system integration ensures tests stay in sync with code
- Consistent test execution across platforms and CI environments
- Reduces friction between writing code and validating it

---

## What is CTest?

- CMake's built-in test runner and orchestrator
- Discovers and executes tests registered via `CMakeLists.txt`
- Reports pass/fail status based on return codes and output
- Supports parallel execution, timeouts, labels, and fixtures
- Works with any testing framework or standalone executables

---

## Enabling Testing

```cmake
cmake_minimum_required(VERSION 3.20)
project(MyProject LANGUAGES CXX)

enable_testing()
```

- `enable_testing()` activates CTest support in the project
- Must appear in the top-level `CMakeLists.txt`
- Without it, `add_test()` calls are silently ignored

---

## The add_test() Command

```cmake
add_executable(math_test test_math.cpp)

add_test(
    NAME math_test
    COMMAND math_test
)
```

- `NAME` - unique identifier for the test
- `COMMAND` - the executable to run, optionally with arguments
- A return code of 0 means pass, non-zero means fail

---

## add_test() with Arguments

```cmake
add_executable(solver solver_test.cpp)

add_test(NAME solver_add
    COMMAND solver --op add --a 2 --b 3)
add_test(NAME solver_mul
    COMMAND solver --op mul --a 4 --b 5)
add_test(NAME solver_div
    COMMAND solver --op div --a 10 --b 2)
```

- Same executable with different arguments creates separate tests
- Each test runs independently and reports its own result

---

## Running Tests with ctest

```bash
cmake -S . -B build
cmake --build build
ctest --test-dir build
```

```output
Test project /home/user/project/build
    Start 1: solver_add
1/3 Test #1: solver_add .............   Passed    0.01 sec
    Start 2: solver_mul
2/3 Test #2: solver_mul .............   Passed    0.01 sec
    Start 3: solver_div
3/3 Test #3: solver_div .............   Passed    0.01 sec

100% tests passed, 0 tests failed out of 3
```

---

## CTest Options - Verbosity and Listing

```bash
ctest -N                   # List tests without running them
ctest -V                   # Verbose output
ctest -VV                  # Extra verbose output
ctest --output-on-failure  # Show output only when a test fails
```

- `-N` is useful for verifying test discovery
- `--output-on-failure` is the most common CI setting

---

## CTest Options - Filtering and Parallelism

```bash
ctest -R "solver_"         # Run tests matching regex
ctest -E "slow"            # Exclude tests matching regex
ctest -R "unit_" -E "deprecated"  # Combine include and exclude
ctest -j4                  # Run 4 tests in parallel
ctest -j0                  # Use all available CPU cores
```

- `-R` and `-E` accept regular expressions
- `-j` speeds up large test suites significantly

---

## set_tests_properties() Usage

```cmake
add_test(NAME my_test COMMAND my_test)

set_tests_properties(my_test PROPERTIES
    TIMEOUT 30
    LABELS "unit"
)
```

- Applies properties to one or more tests
- Must be called after the corresponding `add_test()`
- Multiple properties can be set in a single call

---

## TIMEOUT Property

```cmake
add_test(NAME network_test COMMAND network_test)
set_tests_properties(network_test PROPERTIES
    TIMEOUT 10
)

add_test(NAME stress_test COMMAND stress_test)
set_tests_properties(stress_test PROPERTIES
    TIMEOUT 300
)
```

- Kills the test process after the specified number of seconds
- Prevents hanging tests from blocking the entire suite
- A timed-out test is reported as failed

---

## WILL_FAIL Property

```cmake
add_test(NAME test_invalid_input COMMAND validator "")
set_tests_properties(test_invalid_input PROPERTIES
    WILL_FAIL TRUE
)
```

- Inverts the pass/fail logic
- Test passes when the command returns non-zero
- Test fails when the command returns zero
- Useful for verifying that error conditions are caught

---

## PASS_REGULAR_EXPRESSION and FAIL_REGULAR_EXPRESSION

```cmake
add_test(NAME output_check COMMAND my_app --self-test)

set_tests_properties(output_check PROPERTIES
    PASS_REGULAR_EXPRESSION "ALL CHECKS PASSED"
)

add_test(NAME crash_check COMMAND my_app --run)
set_tests_properties(crash_check PROPERTIES
    FAIL_REGULAR_EXPRESSION "SEGFAULT;FATAL ERROR;ABORT"
)
```

- `PASS_REGULAR_EXPRESSION` - pass only if stdout matches
- `FAIL_REGULAR_EXPRESSION` - fail if stdout matches any pattern
- Semicolons separate multiple patterns (any match triggers)

---

## Test Labels

```cmake
add_test(NAME test_add COMMAND test_add)
add_test(NAME test_mul COMMAND test_mul)
add_test(NAME test_db_insert COMMAND test_db_insert)

set_tests_properties(test_add test_mul PROPERTIES
    LABELS "unit;fast")
set_tests_properties(test_db_insert PROPERTIES
    LABELS "integration;slow")
```

- Labels are semicolon-separated strings
- A single test can have multiple labels

---

## Filtering by Label

```bash
ctest -L unit              # Run tests with label matching "unit"
ctest -L "fast"            # Run tests labeled "fast"
ctest -LE "slow"           # Exclude tests labeled "slow"
ctest -L unit -LE legacy   # Combine include and exclude
```

- `-L` includes tests whose labels match the regex
- `-LE` excludes tests whose labels match the regex
- Labels provide a higher-level grouping than name filtering

---

## Test Environment Variables

```cmake
add_test(NAME db_test COMMAND db_test)
set_tests_properties(db_test PROPERTIES
    ENVIRONMENT "DB_HOST=localhost;DB_PORT=5432;DB_NAME=test"
)

add_test(NAME api_test COMMAND api_test)
set_tests_properties(api_test PROPERTIES
    ENVIRONMENT_MODIFICATION "PATH=path_list_prepend:/opt/bin"
)
```

- `ENVIRONMENT` sets variables for the test process
- `ENVIRONMENT_MODIFICATION` modifies existing variables
- Each entry is a `KEY=VALUE` pair, separated by semicolons

---

## WORKING_DIRECTORY Property

```cmake
add_test(NAME config_test COMMAND config_test)
set_tests_properties(config_test PROPERTIES
    WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}/test_data"
)
```

- Sets the current directory when the test runs
- Defaults to `CMAKE_CURRENT_BINARY_DIR`
- Useful when tests depend on relative file paths

---

## Test Fixtures - Setup and Cleanup

```cmake
add_test(NAME setup_db COMMAND init_database)
add_test(NAME cleanup_db COMMAND drop_database)
add_test(NAME test_query COMMAND test_query)

set_tests_properties(setup_db PROPERTIES
    FIXTURES_SETUP Database)
set_tests_properties(cleanup_db PROPERTIES
    FIXTURES_CLEANUP Database)
set_tests_properties(test_query PROPERTIES
    FIXTURES_REQUIRED Database)
```

- `FIXTURES_SETUP` runs before any test requiring the fixture
- `FIXTURES_CLEANUP` runs after all tests requiring the fixture

---

## Fixtures - Multiple Tests Sharing a Fixture

```cmake
set_tests_properties(setup_db PROPERTIES
    FIXTURES_SETUP Database)
set_tests_properties(cleanup_db PROPERTIES
    FIXTURES_CLEANUP Database)

set_tests_properties(
    test_insert test_query test_delete
    PROPERTIES FIXTURES_REQUIRED Database
)
```

---

## Fixtures - Multiple Tests Sharing a Fixture

![fixtures_multiple_tests_sharing_a_fixture](svg/courses/build_systems/cmake/07_testing_with_ctest/fixtures_multiple_tests_sharing_a_fixture.svg)

---

## Fixtures - Execution Order

- Setup runs once before the group, cleanup once after

---

## Google Test Integration

```cmake
include(FetchContent)
FetchContent_Declare(googletest
    GIT_REPOSITORY https://github.com/google/googletest
    GIT_TAG v1.14.0)
FetchContent_MakeAvailable(googletest)

add_executable(my_tests tests/test_main.cpp)
target_link_libraries(my_tests PRIVATE GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(my_tests)
```

- `gtest_discover_tests()` finds all `TEST()` and `TEST_F()` macros
- Each test case becomes a separate CTest entry automatically

---

## Google Test - Example

```cpp
#include <gtest/gtest.h>
#include "calc.h"

TEST(CalcTest, Addition) {
    EXPECT_EQ(add(2, 3), 5);
    EXPECT_EQ(add(-1, 1), 0);
}

TEST(CalcTest, Division) {
    EXPECT_DOUBLE_EQ(divide(10.0, 3.0), 10.0 / 3.0);
    EXPECT_THROW(divide(1.0, 0.0), std::runtime_error);
}
```

- No `main()` needed when linking `GTest::gtest_main`
- Each `TEST()` is discovered and run separately by CTest

---

## Catch2 Integration

```cmake
include(FetchContent)
FetchContent_Declare(Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2
    GIT_TAG v3.5.0)
FetchContent_MakeAvailable(Catch2)

add_executable(tests tests/test_main.cpp)
target_link_libraries(tests PRIVATE Catch2::Catch2WithMain)

include(Catch)
catch_discover_tests(tests)
```

- `catch_discover_tests()` works like `gtest_discover_tests()`
- Automatically discovers `TEST_CASE` macros

---

## Generic Framework Integration

```cmake
add_executable(custom_tests tests/runner.cpp)
target_link_libraries(custom_tests PRIVATE my_test_framework)

add_test(NAME custom_tests COMMAND custom_tests)
set_tests_properties(custom_tests PROPERTIES
    PASS_REGULAR_EXPRESSION "All tests passed"
    FAIL_REGULAR_EXPRESSION "FAILED;ASSERTION"
    TIMEOUT 60
)
```

- Any framework that returns 0 on success works out of the box
- Use regex properties for frameworks with non-standard exit codes
- Wrap scripts or interpreters as test commands when needed

---

## CDash Overview

- Web-based dashboard for collecting build and test results
- Tracks test history and highlights regressions
- Supports multiple platforms, compilers, and configurations
- Available at `https://my.cdash.org` or self-hosted

| Build Name    | Configure | Build | Test | Cover |
|---------------|-----------|-------|------|-------|
| Linux-GCC-13  |    OK     |  OK   | 98%  |  85%  |
| macOS-Clang   |    OK     | 1 err | 95%  |  82%  |

---

## Submitting Results to CDash

```cmake
# CTestConfig.cmake (place in source root)
set(CTEST_PROJECT_NAME "MyProject")
set(CTEST_NIGHTLY_START_TIME "01:00:00 UTC")
set(CTEST_DROP_METHOD "https")
set(CTEST_DROP_SITE "my.cdash.org")
set(CTEST_DROP_LOCATION "/submit.php?project=MyProject")
set(CTEST_DROP_SITE_CDASH TRUE)
```

- Create `CTestConfig.cmake` alongside the top-level `CMakeLists.txt`
- Tells CTest where and how to submit results

---

## CDash Submission Modes

```bash
ctest -D Experimental    # Ad-hoc developer builds
ctest -D Nightly         # Scheduled nightly builds
ctest -D Continuous      # Triggered by source changes
```

- Each mode runs configure, build, test, and submit steps
- Individual steps can be run separately:

```bash
ctest -D ExperimentalStart
ctest -D ExperimentalConfigure
ctest -D ExperimentalBuild
ctest -D ExperimentalTest
ctest -D ExperimentalSubmit
```

---

## Complete Testing Example

```cmake
cmake_minimum_required(VERSION 3.20)
project(Calculator VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
add_library(calc src/calc.cpp)
target_include_directories(calc PUBLIC include/)

enable_testing()
include(FetchContent)
FetchContent_Declare(googletest
    GIT_REPOSITORY https://github.com/google/googletest
    GIT_TAG v1.14.0)
FetchContent_MakeAvailable(googletest)

add_executable(calc_tests tests/test_calc.cpp)
target_link_libraries(calc_tests PRIVATE
    calc GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(calc_tests
    PROPERTIES LABELS "unit"
    DISCOVERY_TIMEOUT 10)
```
