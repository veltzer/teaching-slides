# Test Harnesses
---
## Why Test Bash Scripts?
- Scripts grow complex over time
- Manual testing misses edge cases
- Regression testing catches breakage
- Tests serve as documentation
- Same reasons as any other language

```bash
# A function we want to test
is_valid_ip() {
    local ip=$1
    [[ $ip =~ ^([0-9]{1,3}\.){3}[0-9]{1,3}$ ]] || return 1
    local IFS='.'
    read -ra octets <<< "$ip"
    for octet in "${octets[@]}"; do
        (( octet > 255 )) && return 1
    done
    return 0
}
```
---
## Simple Test Framework
```bash
#!/bin/bash

# Minimal test framework
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

assert_equals() {
    local expected=$1 actual=$2 message=${3:-""}
    ((TESTS_RUN++))
    if [[ "$expected" == "$actual" ]]; then
        ((TESTS_PASSED++))
        echo "  PASS: $message"
    else
        ((TESTS_FAILED++))
        echo "  FAIL: $message"
        echo "    Expected: $expected"
        echo "    Actual:   $actual"
    fi
}

assert_true() {
    local message=${1:-""}
    ((TESTS_RUN++))
    if eval "${@:2}"; then
        ((TESTS_PASSED++))
        echo "  PASS: $message"
    else
        ((TESTS_FAILED++))
        echo "  FAIL: $message"
    fi
}

test_summary() {
    echo ""
    echo "=========================="
    echo "Tests run:    $TESTS_RUN"
    echo "Tests passed: $TESTS_PASSED"
    echo "Tests failed: $TESTS_FAILED"
    echo "=========================="
    (( TESTS_FAILED > 0 )) && return 1
    return 0
}
```
---
## Using the Test Framework
```bash
#!/bin/bash
source test_framework.sh
source my_functions.sh

echo "Testing is_valid_ip..."
assert_true "valid IP 192.168.1.1" is_valid_ip "192.168.1.1"
assert_true "valid IP 0.0.0.0" is_valid_ip "0.0.0.0"
assert_true "valid IP 255.255.255.255" is_valid_ip "255.255.255.255"

echo ""
echo "Testing invalid IPs..."
assert_true "reject 256.1.1.1" ! is_valid_ip "256.1.1.1"
assert_true "reject abc.1.1.1" ! is_valid_ip "abc.1.1.1"
assert_true "reject 1.1.1" ! is_valid_ip "1.1.1"
assert_true "reject empty" ! is_valid_ip ""

test_summary
```
---
## Test Patterns
```bash
# Setup and teardown
setup() {
    TEST_DIR=$(mktemp -d)
    echo "test data" > "$TEST_DIR/input.txt"
}

teardown() {
    rm -rf "$TEST_DIR"
}

run_test() {
    local test_name=$1
    setup
    "$test_name"
    local rc=$?
    teardown
    return $rc
}

# Test function
test_file_processing() {
    local output
    output=$(process_file "$TEST_DIR/input.txt")
    assert_equals "expected output" "$output" "file processing"
}

run_test test_file_processing
```
---
## Testing stdout and stderr
```bash
# Capture and test output
test_output() {
    local stdout stderr rc

    # Capture both stdout and stderr
    stdout=$(my_command 2>/tmp/test_stderr)
    rc=$?
    stderr=$(cat /tmp/test_stderr)

    assert_equals 0 "$rc" "exit code should be 0"
    assert_equals "expected output" "$stdout" "stdout check"
    assert_equals "" "$stderr" "no stderr expected"
}

# More robust capture
capture() {
    local stdout_var=$1 stderr_var=$2 rc_var=$3
    shift 3
    local tmpfile
    tmpfile=$(mktemp)
    eval "$stdout_var"'=$("$@" 2>"$tmpfile")'
    eval "$rc_var"'=$?'
    eval "$stderr_var"'=$(cat "$tmpfile")'
    rm -f "$tmpfile"
}
```
---
## Existing Test Frameworks
```bash
# BATS (Bash Automated Testing System)
# Install: npm install -g bats / brew install bats-core

# test_example.bats:
@test "addition" {
    result="$(echo "2 + 2" | bc)"
    [ "$result" -eq 4 ]
}

@test "file exists" {
    run ls /etc/passwd
    [ "$status" -eq 0 ]
}

@test "script output" {
    run ./myscript.sh --version
    [ "$output" = "1.0.0" ]
}

# Run: bats test_example.bats
```
---
## BATS Helpers
```bash
# Setup and teardown in BATS
setup() {
    TEST_DIR="$(mktemp -d)"
    echo "data" > "$TEST_DIR/test.txt"
}

teardown() {
    rm -rf "$TEST_DIR"
}

@test "process file" {
    run process_file "$TEST_DIR/test.txt"
    [ "$status" -eq 0 ]
    [ "${lines[0]}" = "Processing: test.txt" ]
}

# Load helpers
load 'test_helper/bats-support/load'
load 'test_helper/bats-assert/load'

@test "with assertions" {
    run my_command
    assert_success
    assert_output --partial "expected"
}
```
---
## Testing Best Practices
```
1. Test the interface, not the implementation
2. Each test should be independent
3. Use setup/teardown for common state
4. Test both success and failure cases
5. Test edge cases (empty input, special chars)
6. Use temp directories, never hardcode paths
7. Clean up after tests (trap EXIT)
8. Run tests in CI/CD pipeline
9. Keep tests fast (mock slow operations)
10. Name tests descriptively
```
---
## Mocking Commands
```bash
# Override commands with functions for testing
# Functions take precedence over external commands

# Mock curl for offline testing
curl() {
    case "$*" in
        *"api/users"*)
            echo '{"users": [{"name": "Alice"}]}'
            return 0
            ;;
        *"api/error"*)
            echo "Internal Server Error" >&2
            return 1
            ;;
    esac
}

# Now your script's calls to curl use the mock
source my_api_script.sh
# test functions that call curl...

# Remove mock
unset -f curl
```
---
## Integration Testing
```bash
#!/bin/bash
# Integration test: test the full script

readonly SCRIPT="./deploy.sh"

test_deploy_dry_run() {
    local output
    output=$($SCRIPT --dry-run --target staging 2>&1)
    local rc=$?

    assert_equals 0 "$rc" "dry run should succeed"
    [[ "$output" == *"Would deploy to staging"* ]] || {
        echo "FAIL: missing expected output"
        echo "Got: $output"
        return 1
    }
    echo "PASS: dry run output correct"
}

test_deploy_missing_target() {
    local output
    output=$($SCRIPT 2>&1)
    local rc=$?

    assert_equals 1 "$rc" "missing target should fail"
}
```
