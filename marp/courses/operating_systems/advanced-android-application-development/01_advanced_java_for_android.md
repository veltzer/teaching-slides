---
tags:
  - infrastructure:android
  - languages:java
  - concepts:mobile-development
level: advanced
category: mobile
audience:
  - audiences:developers

---

# Advanced Java for Android
## Advanced Features and Modern Patterns

---

## Course Overview
- Java 8+ features in Android
- Lambda expressions
- Stream API
- Threading fundamentals
- Exception handling

---

## Key Improvements

![key_improvements](svg/courses/operating_systems/advanced-android-application-development/01_advanced_java_for_android/key_improvements.svg)

---

## Lambda Expressions
### Simplified Anonymous Functions

Before:

```java
button.setOnClickListener(new View.OnClickListener() {
    @Override
    public void onClick(View v) {
        performAction();
    }
});
```

After:

```java
button.setOnClickListener(v -> performAction());
```

---

## Common Lambda Use Cases

| Scenario | Traditional | Lambda |
|----------|-------------|---------|
| Click Listener | `new OnClickListener() {...}` | `v -> handleClick()` |
| Runnable | `new Runnable() {...}` | `() -> performTask()` |
| Comparator | `new Comparator<T>() {...}` | `(a, b) -> a.compareTo(b)` |

---

## Method References
### Four Types of Method References

```java
// Static method reference
List<String> numbers = Arrays.asList("1", "2", "3");
numbers.forEach(System.out::println);

// Instance method reference
String prefix = "User_";
numbers.forEach(prefix::concat);

// Constructor reference
Stream<User> users = names.stream().map(User::new);

// Instance method of arbitrary object
List<String> sorted = names.stream()
    .sorted(String::compareToIgnoreCase)
    .collect(Collectors.toList());
```

---

## Stream API - Data Processing Pipeline

![data_processing_pipeline](svg/courses/operating_systems/advanced-android-application-development/01_advanced_java_for_android/data_processing_pipeline.svg)

---

## Stream API Example
```java
List<User> activeAdmins = users.stream()
    .filter(User::isActive)
    .filter(User::isAdmin)
    .collect(Collectors.toList());
```

---

## Stream Operations Example

```java
public class UserProcessor {
    public List<String> processUsers(List<User> users) {
        return users.stream()
            .filter(user -> user.getAge() > 18)
            .map(User::getUsername)
            .sorted()
            .distinct()
            .collect(Collectors.toList());
    }
}
```

---

## Android Threading Model

![android_threading_model](svg/courses/operating_systems/advanced-android-application-development/01_advanced_java_for_android/android_threading_model.svg)

---

## Thread Implementation

```java
public class DataLoader {
    public void loadData() {
        new Thread(() -> {
            // Background work
            try {
                // Simulate network call
                Thread.sleep(2000);

                // Update UI on main thread
                activity.runOnUiThread(() -> {
                    updateUI();
                });
            } catch (InterruptedException e) {
                handleError(e);
            }
        }).start();
    }
}
```

---

## Exception Handling Best Practices

```java
public class SafeOperation {
    public void performOperation() {
        try {
            riskyOperation();
        } catch (IOException e) {
            Log.e(TAG, "IO Error", e);
            showError("Failed to read data");
        } catch (JSONException e) {
            Log.e(TAG, "JSON Error", e);
            showError("Failed to parse data");
        } finally {
            cleanup();
        }
    }
}
```

---

## Custom Exception Handling

```java
public class AppException extends Exception {
    private final ErrorType type;

    public AppException(ErrorType type, String message) {
        super(message);
        this.type = type;
    }

    public ErrorType getType() {
        return type;
    }
}
```

---

## Practice Exercise
### Lambda and Streams

```java
public class Exercise {
    public static void main(String[] args) {
        List<String> names = Arrays.asList(
            "Alice", "Bob", "Charlie", "David"
        );

        // TODO: Use streams to:
        // 1. Filter names longer than 4 characters
        // 2. Convert to uppercase
        // 3. Sort alphabetically
        // 4. Collect to a new list
    }
}
```

---

## Key Takeaways

- Lambda expressions simplify anonymous functions
- Stream API enables functional programming
- Method references improve code readability
- Proper threading is crucial for Android apps
- Exception handling ensures app stability

---

## Assignment Preview
### Build a Utility Library

Create a utility library that implements:
- Custom stream operations
- Thread-safe data structures
- Error handling framework
- Lambda-based event system

---

## Additional Resources

- Oracle Java 8 Documentation
- Android Developers Guide
- StackOverflow Java 8 Documentation
- GitHub Sample Code Repository
