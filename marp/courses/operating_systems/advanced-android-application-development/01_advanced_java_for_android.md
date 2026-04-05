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

## Java 8+ Features in Android
### Key Improvements

<svg width="600" height="250" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="100" width="100" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="250" y="100" width="100" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <rect x="200" y="30" width="80" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <rect x="320" y="30" width="100" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <rect x="450" y="30" width="140" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <rect x="200" y="180" width="80" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="130" text-anchor="middle" font-size="14">Java 7</text>
  <text x="300" y="130" text-anchor="middle" font-size="14">Java 8+</text>
  <text x="240" y="55" text-anchor="middle" font-size="12">Lambda</text>
  <text x="370" y="55" text-anchor="middle" font-size="12">Stream API</text>
  <text x="520" y="55" text-anchor="middle" font-size="11">Method References</text>
  <text x="240" y="205" text-anchor="middle" font-size="12">Optional</text>
  <line x1="150" y1="125" x2="250" y2="125" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="300" y1="100" x2="240" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="300" y1="100" x2="370" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="300" y1="100" x2="520" y2="70" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <line x1="300" y1="150" x2="240" y2="180" stroke="#333" stroke-width="2" marker-end="url(#arrow1)"/>
  <defs>
    <marker id="arrow1" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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

## Stream API
### Data Processing Pipeline

<svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="80" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="200" y="50" width="80" height="50" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <rect x="350" y="50" width="80" height="50" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <rect x="500" y="50" width="80" height="50" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="90" y="80" text-anchor="middle" font-size="14">Source</text>
  <text x="240" y="80" text-anchor="middle" font-size="14">Filter</text>
  <text x="390" y="80" text-anchor="middle" font-size="14">Map</text>
  <text x="540" y="80" text-anchor="middle" font-size="14">Collect</text>
  <line x1="130" y1="75" x2="200" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="280" y1="75" x2="350" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <line x1="430" y1="75" x2="500" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arrow2)"/>
  <defs>
    <marker id="arrow2" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

Example:

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

## Threading Fundamentals
### Android Threading Model

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="30" width="120" height="50" fill="#ff6b6b" stroke="#333" stroke-width="2"/>
  <rect x="250" y="120" width="120" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <rect x="100" y="210" width="120" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <rect x="250" y="210" width="120" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <rect x="400" y="210" width="120" height="40" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="310" y="60" text-anchor="middle" font-size="14">Main Thread</text>
  <text x="310" y="150" text-anchor="middle" font-size="14">Background Thread</text>
  <text x="160" y="235" text-anchor="middle" font-size="12">Network Calls</text>
  <text x="310" y="235" text-anchor="middle" font-size="12">Database Operations</text>
  <text x="460" y="235" text-anchor="middle" font-size="12">File I/O</text>
  <text x="450" y="60" text-anchor="middle" font-size="12">UI Operations</text>
  <line x1="370" y1="55" x2="450" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="310" y1="80" x2="310" y2="120" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="310" y1="170" x2="160" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="310" y1="170" x2="310" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <line x1="310" y1="170" x2="460" y2="210" stroke="#333" stroke-width="2" marker-end="url(#arrow3)"/>
  <defs>
    <marker id="arrow3" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
</svg>

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
