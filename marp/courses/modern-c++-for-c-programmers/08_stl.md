# Standard Template Library (STL)

---

## What is the STL?

The Standard Template Library is a collection of C++ template classes and functions that provide:

1. **Containers** - data structures to store objects
1. **Iterators** - objects that point to elements in containers
1. **Algorithms** - functions that perform operations on containers
1. **Function objects** - classes that act like functions
1. **Adaptors** - modify containers or iterators

---

## STL Architecture

<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="150" height="80" fill="#e6f3ff" stroke="#0066cc"/>
  <text x="125" y="75" text-anchor="middle" font-size="14" font-weight="bold">Containers</text>
  <text x="125" y="95" text-anchor="middle" font-size="12">vector, list, map</text>
  <text x="125" y="115" text-anchor="middle" font-size="12">set, queue, stack</text>

  <rect x="250" y="50" width="150" height="80" fill="#ffe6e6" stroke="#cc0000"/>
  <text x="325" y="75" text-anchor="middle" font-size="14" font-weight="bold">Iterators</text>
  <text x="325" y="95" text-anchor="middle" font-size="12">begin(), end()</text>
  <text x="325" y="115" text-anchor="middle" font-size="12">++, *, -></text>

  <rect x="450" y="50" width="150" height="80" fill="#e6ffe6" stroke="#00cc00"/>
  <text x="525" y="75" text-anchor="middle" font-size="14" font-weight="bold">Algorithms</text>
  <text x="525" y="95" text-anchor="middle" font-size="12">sort, find, copy</text>
  <text x="525" y="115" text-anchor="middle" font-size="12">transform, for_each</text>

  <rect x="150" y="180" width="150" height="80" fill="#fff0e6" stroke="#ff6600"/>
  <text x="225" y="205" text-anchor="middle" font-size="14" font-weight="bold">Function Objects</text>
  <text x="225" y="225" text-anchor="middle" font-size="12">less, greater</text>
  <text x="225" y="245" text-anchor="middle" font-size="12">lambdas</text>

  <rect x="350" y="180" width="150" height="80" fill="#f0e6ff" stroke="#6600cc"/>
  <text x="425" y="205" text-anchor="middle" font-size="14" font-weight="bold">Adaptors</text>
  <text x="425" y="225" text-anchor="middle" font-size="12">stack, queue</text>
  <text x="425" y="245" text-anchor="middle" font-size="12">priority_queue</text>

  <line x1="200" y1="90" x2="250" y2="90" stroke="#666" marker-end="url(#arrowhead)"/>
  <line x1="400" y1="90" x2="450" y2="90" stroke="#666" marker-end="url(#arrowhead)"/>
  <line x1="325" y1="130" x2="325" y2="180" stroke="#666" marker-end="url(#arrowhead)"/>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

---

## Why Use the STL?

1. **Efficiency** - optimized implementations
1. **Reliability** - thoroughly tested
1. **Consistency** - uniform interface across containers
1. **Flexibility** - generic algorithms work with any container
1. **Productivity** - focus on problem solving, not data structures

---

## STL Headers

```cpp
#include <vector>       // Dynamic arrays
#include <list>         // Doubly linked lists
#include <deque>        // Double-ended queues
#include <set>          // Ordered sets
#include <map>          // Associative arrays
#include <unordered_map> // Hash tables
#include <stack>        // LIFO containers
#include <queue>        // FIFO containers
#include <algorithm>    // Algorithms
#include <iterator>     // Iterator utilities
#include <functional>   // Function objects
#include <string>       // String class
```

---

## Container Categories

<svg width="600" height="350" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="20" width="180" height="100" fill="#e6f3ff" stroke="#0066cc"/>
  <text x="140" y="40" text-anchor="middle" font-size="14" font-weight="bold">Sequence Containers</text>
  <text x="140" y="60" text-anchor="middle" font-size="12">vector</text>
  <text x="140" y="75" text-anchor="middle" font-size="12">deque</text>
  <text x="140" y="90" text-anchor="middle" font-size="12">list</text>
  <text x="140" y="105" text-anchor="middle" font-size="12">array (C++11)</text>

  <rect x="280" y="20" width="180" height="100" fill="#ffe6e6" stroke="#cc0000"/>
  <text x="370" y="40" text-anchor="middle" font-size="14" font-weight="bold">Associative Containers</text>
  <text x="370" y="60" text-anchor="middle" font-size="12">set, multiset</text>
  <text x="370" y="75" text-anchor="middle" font-size="12">map, multimap</text>
  <text x="370" y="90" text-anchor="middle" font-size="12">Ordered (tree-based)</text>
  <text x="370" y="105" text-anchor="middle" font-size="12">O(log n) operations</text>

  <rect x="50" y="140" width="180" height="100" fill="#e6ffe6" stroke="#00cc00"/>
  <text x="140" y="160" text-anchor="middle" font-size="14" font-weight="bold">Unordered Containers</text>
  <text x="140" y="180" text-anchor="middle" font-size="12">unordered_set</text>
  <text x="140" y="195" text-anchor="middle" font-size="12">unordered_map</text>
  <text x="140" y="210" text-anchor="middle" font-size="12">Hash-based (C++11)</text>
  <text x="140" y="225" text-anchor="middle" font-size="12">O(1) average operations</text>

  <rect x="280" y="140" width="180" height="100" fill="#fff0e6" stroke="#ff6600"/>
  <text x="370" y="160" text-anchor="middle" font-size="14" font-weight="bold">Container Adaptors</text>
  <text x="370" y="180" text-anchor="middle" font-size="12">stack</text>
  <text x="370" y="195" text-anchor="middle" font-size="12">queue</text>
  <text x="370" y="210" text-anchor="middle" font-size="12">priority_queue</text>
  <text x="370" y="225" text-anchor="middle" font-size="12">Wrap other containers</text>
</svg>

---

## Vector - Dynamic Array

```cpp
#include <vector>
#include <iostream>

int main() {
    // Declaration and initialization
    std::vector<int> numbers;
    std::vector<int> numbers2(10);        // 10 elements, default initialized
    std::vector<int> numbers3(10, 5);     // 10 elements, all set to 5
    std::vector<int> numbers4{1, 2, 3, 4, 5}; // Initializer list

    // Adding elements
    numbers.push_back(10);
    numbers.push_back(20);
    numbers.push_back(30);

    // Accessing elements
    std::cout << "First: " << numbers[0] << std::endl;
    std::cout << "Second: " << numbers.at(1) << std::endl;
    std::cout << "Last: " << numbers.back() << std::endl;

---

## Sorting Algorithms

```cpp
#include <algorithm>
#include <vector>

int main() {
    std::vector<int> numbers{9, 3, 7, 1, 5, 2, 8, 4, 6};

    // Basic sort (ascending)
    std::sort(numbers.begin(), numbers.end());

    // Sort with custom comparator (descending)
    std::sort(numbers.begin(), numbers.end(), std::greater<int>());

    // Sort with lambda
    std::sort(numbers.begin(), numbers.end(),
              [](int a, int b) { return a > b; });

    // Stable sort (preserves relative order of equal elements)
    std::stable_sort(numbers.begin(), numbers.end());

    // Partial sort (sort only first n elements)
    std::partial_sort(numbers.begin(), numbers.begin() + 3, numbers.end());

    // nth_element (put nth element in correct position)
    std::nth_element(numbers.begin(), numbers.begin() + 4, numbers.end());

    return 0;
}
```

---

## Numeric Algorithms

```cpp
#include <numeric>
#include <vector>

int main() {
    std::vector<int> numbers{1, 2, 3, 4, 5};

    // Sum all elements
    int sum = std::accumulate(numbers.begin(), numbers.end(), 0);
    std::cout << "Sum: " << sum << std::endl;  // 15

    // Product of all elements
    int product = std::accumulate(numbers.begin(), numbers.end(), 1,
                                  std::multiplies<int>());
    std::cout << "Product: " << product << std::endl;  // 120

    // Custom operation
    int sum_of_squares = std::accumulate(numbers.begin(), numbers.end(), 0,
                                         [](int sum, int n) { return sum + n * n; });

    // Inner product (dot product)
    std::vector<int> other{2, 3, 4, 5, 6};
    int dot_product = std::inner_product(numbers.begin(), numbers.end(),
                                         other.begin(), 0);

    // Partial sum (running totals)
    std::vector<int> partial_sums(5);
    std::partial_sum(numbers.begin(), numbers.end(), partial_sums.begin());
    // partial_sums: {1, 3, 6, 10, 15}

    return 0;
}
```

---

## Function Objects (Functors)

```cpp
#include <functional>
#include <algorithm>
#include <vector>

// Custom functor class
class Multiply {
private:
    int factor;
public:
    Multiply(int f) : factor(f) {}
    int operator()(int x) const { return x * factor; }
};

int main() {
    std::vector<int> numbers{1, 2, 3, 4, 5};

    // Using custom functor
    Multiply times3(3);
    std::transform(numbers.begin(), numbers.end(), numbers.begin(), times3);

    // Standard functors
    std::sort(numbers.begin(), numbers.end(), std::greater<int>());  // Descending

    // Lambda expressions (C++11)
    std::sort(numbers.begin(), numbers.end(),
              [](int a, int b) { return a < b; });  // Ascending

    // std::function wrapper
    std::function<bool(int, int)> comparator = [](int a, int b) { return a > b; };
    std::sort(numbers.begin(), numbers.end(), comparator);

    return 0;
}
```

---

## Lambda Expressions

```cpp
#include <algorithm>
#include <vector>

int main() {
    std::vector<int> numbers{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Basic lambda
    auto is_even = [](int n) { return n % 2 == 0; };

    // Count even numbers
    int even_count = std::count_if(numbers.begin(), numbers.end(), is_even);

    // Lambda with capture
    int threshold = 5;
    auto greater_than_threshold = [threshold](int n) { return n > threshold; };

    // Capture by reference
    int sum = 0;
    std::for_each(numbers.begin(), numbers.end(), [&sum](int n) { sum += n; });

    // Capture by value vs reference
    int multiplier = 2;
    auto by_value = [multiplier](int n) { return n * multiplier; };      // Copy
    auto by_ref = [&multiplier](int n) { return n * multiplier; };       // Reference
    auto by_value_mutable = [multiplier](int n) mutable {
        return n * ++multiplier;
    };

    // Generic lambda (C++14)
    auto generic = [](auto a, auto b) { return a + b; };

    return 0;
}
```

---

## STL Algorithms with Lambdas

```cpp
#include <algorithm>
#include <vector>
#include <string>

int main() {
    std::vector<std::string> words{"hello", "world", "cpp", "programming"};

    // Sort by length
    std::sort(words.begin(), words.end(),
              [](const std::string& a, const std::string& b) {
                  return a.length() < b.length();
              });

    // Find first word longer than 5 characters
    auto it = std::find_if(words.begin(), words.end(),
                           [](const std::string& word) {
                               return word.length() > 5;
                           });

    // Transform to uppercase
    std::transform(words.begin(), words.end(), words.begin(),
                   [](std::string word) {
                       std::transform(word.begin(), word.end(), word.begin(),
                                      ::toupper);
                       return word;
                   });

    // Check if all words have more than 2 characters
    bool all_long = std::all_of(words.begin(), words.end(),
                                [](const std::string& word) {
                                    return word.length() > 2;
                                });

    return 0;
}
```

---

## Iterator Adaptors

```cpp
#include <iterator>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> source{1, 2, 3, 4, 5};
    std::vector<int> dest;

    // Back inserter - automatically calls push_back
    std::copy(source.begin(), source.end(), std::back_inserter(dest));

    // Front inserter - automatically calls push_front (deque, list)
    std::list<int> lst;
    std::copy(source.begin(), source.end(), std::front_inserter(lst));

    // Insert iterator - inserts at specific position
    std::vector<int> target{10, 20, 30};
    std::copy(source.begin(), source.end(),
              std::inserter(target, target.begin() + 1));

    // Reverse iterator
    std::copy(source.rbegin(), source.rend(), std::back_inserter(dest));

    // Move iterator (C++11)
    std::vector<std::string> strings{"hello", "world"};
    std::vector<std::string> moved;
    std::copy(std::make_move_iterator(strings.begin()),
              std::make_move_iterator(strings.end()),
              std::back_inserter(moved));

    return 0;
}
```

---

## Algorithm Complexity

<svg width="600" height="350" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="20" width="150" height="60" fill="#e6f3ff" stroke="#0066cc"/>
  <text x="125" y="40" text-anchor="middle" font-size="12" font-weight="bold">O(1) - Constant</text>
  <text x="125" y="60" text-anchor="middle" font-size="10">vector::at, map::find</text>

  <rect x="220" y="20" width="150" height="60" fill="#ffe6e6" stroke="#cc0000"/>
  <text x="295" y="40" text-anchor="middle" font-size="12" font-weight="bold">O(log n) - Logarithmic</text>
  <text x="295" y="60" text-anchor="middle" font-size="10">binary_search, set ops</text>

  <rect x="390" y="20" width="150" height="60" fill="#e6ffe6" stroke="#00cc00"/>
  <text x="465" y="40" text-anchor="middle" font-size="12" font-weight="bold">O(n) - Linear</text>
  <text x="465" y="60" text-anchor="middle" font-size="10">find, count, copy</text>

  <rect x="135" y="100" width="150" height="60" fill="#fff0e6" stroke="#ff6600"/>
  <text x="210" y="120" text-anchor="middle" font-size="12" font-weight="bold">O(n log n)</text>
  <text x="210" y="140" text-anchor="middle" font-size="10">sort, stable_sort</text>

  <rect x="305" y="100" width="150" height="60" fill="#f0e6ff" stroke="#6600cc"/>
  <text x="380" y="120" text-anchor="middle" font-size="12" font-weight="bold">O(n²) - Quadratic</text>
  <text x="380" y="140" text-anchor="middle" font-size="10">bubble_sort (not in STL)</text>

  <rect x="150" y="200" width="300" height="100" fill="#f9f9f9" stroke="#333"/>
  <text x="300" y="220" text-anchor="middle" font-size="14" font-weight="bold">Performance Tips</text>
  <text x="300" y="240" text-anchor="middle" font-size="12">• Choose right container for your use case</text>
  <text x="300" y="260" text-anchor="middle" font-size="12">• Use algorithms instead of manual loops</text>
  <text x="300" y="280" text-anchor="middle" font-size="12">• Reserve space for vectors when size is known</text>
</svg>

---

## Container Selection Guide

```cpp
// Need random access and frequent insertions at end?
std::vector<int> vec;  // O(1) access, O(1) amortized push_back

// Need frequent insertions/deletions at both ends?
std::deque<int> deq;   // O(1) access, O(1) push_front/push_back

// Need frequent insertions/deletions in middle?
std::list<int> lst;    // O(1) insert/erase with iterator

// Need unique sorted elements?
std::set<int> s;       // O(log n) insert/find/erase

// Need key-value mapping?
std::map<std::string, int> m;  // O(log n) operations

// Need fastest possible lookup?
std::unordered_set<int> us;    // O(1) average insert/find/erase
std::unordered_map<std::string, int> um;  // O(1) average operations

// Need LIFO (stack) behavior?
std::stack<int> stk;   // O(1) push/pop/top

// Need FIFO (queue) behavior?
std::queue<int> que;   // O(1) push/pop/front

// Need priority-based access?
std::priority_queue<int> pq;  // O(log n) push/pop, O(1) top
```

---

## String Class

```cpp
#include <string>
#include <algorithm>

int main() {
    std::string str = "Hello, World!";

    // Basic operations
    std::cout << "Length: " << str.length() << std::endl;
    std::cout << "Character at 7: " << str[7] << std::endl;

    // Substring
    std::string sub = str.substr(7, 5);  // "World"

    // Find operations
    size_t pos = str.find("World");
    if (pos != std::string::npos) {
        std::cout << "Found 'World' at position: " << pos << std::endl;
    }

    // String modification
    str.replace(pos, 5, "C++");  // Replace "World" with "C++"
    str.insert(5, " Beautiful");
    str.erase(5, 10);  // Remove " Beautiful"

    // String algorithms
    std::string text = "hello world";
    std::transform(text.begin(), text.end(), text.begin(), ::toupper);

    // String comparison
    std::string a = "apple", b = "banana";
    if (a < b) {
        std::cout << a << " comes before " << b << std::endl;
    }

    return 0;
}
```

---

## String Operations and Algorithms

```cpp
#include <string>
#include <sstream>
#include <algorithm>

int main() {
    // String stream for parsing
    std::string data = "10 20 30 40 50";
    std::istringstream iss(data);
    std::vector<int> numbers;

    int num;
    while (iss >> num) {
        numbers.push_back(num);
    }

    // Tokenizing strings
    std::string sentence = "The quick brown fox";
    std::istringstream stream(sentence);
    std::string word;
    std::vector<std::string> words;

    while (stream >> word) {
        words.push_back(word);
    }

    // Join strings
    std::ostringstream joined;
    for (size_t i = 0; i < words.size(); ++i) {
        if (i > 0) joined << " ";
        joined << words[i];
    }
    std::string result = joined.str();

    // String algorithms
    std::string text = "programming";
    std::sort(text.begin(), text.end());  // Sort characters

    return 0;
}
```

---

## STL Utilities

```cpp
#include <utility>
#include <tuple>
#include <memory>

int main() {
    // Pair
    std::pair<int, std::string> p1 = std::make_pair(42, "answer");
    std::pair<int, std::string> p2(100, "century");

    std::cout << "First: " << p1.first << ", Second: " << p1.second << std::endl;

    // Tuple (C++11)
    std::tuple<int, double, std::string> t1 = std::make_tuple(1, 2.5, "hello");

    int i;
    double d;
    std::string s;
    std::tie(i, d, s) = t1;  // Unpack tuple

    // Structured bindings (C++17)
    auto [num, val, text] = t1;

    // Smart pointers
    std::unique_ptr<int> ptr1 = std::make_unique<int>(42);
    std::shared_ptr<int> ptr2 = std::make_shared<int>(100);

    // Moving
    auto ptr3 = std::move(ptr1);  // ptr1 is now null

    return 0;
}
```

---

## Error Handling in STL

```cpp
#include <vector>
#include <stdexcept>

int main() {
    std::vector<int> vec{1, 2, 3};

    try {
        // Safe access with bounds checking
        int value = vec.at(10);  // Throws std::out_of_range
    }
    catch (const std::out_of_range& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }

    // Unsafe access (no bounds checking)
    // int value = vec[10];  // Undefined behavior

    // Check before access
    if (10 < vec.size()) {
        int value = vec[10];
    }

    // Iterator safety
    auto it = vec.find(vec.begin(), vec.end(), 5);
    if (it != vec.end()) {
        std::cout << "Found: " << *it << std::endl;
    } else {
        std::cout << "Not found" << std::endl;
    }

    return 0;
}
```

---

## Performance Best Practices

```cpp
#include <vector>
#include <algorithm>

int main() {
    // Reserve space to avoid reallocations
    std::vector<int> vec;
    vec.reserve(1000);  // Reserve space for 1000 elements

    // Use emplace instead of push when constructing objects
    std::vector<std::pair<int, std::string>> pairs;
    pairs.emplace_back(1, "one");     // Construct in place
    // pairs.push_back({1, "one"});   // Create temporary then copy

    // Use const references to avoid copies
    for (const auto& item : vec) {    // No copy
        // Process item
    }

    // Prefer algorithms to manual loops
    // Manual loop:
    // for (auto& item : vec) { item *= 2; }

    // Algorithm:
    std::transform(vec.begin(), vec.end(), vec.begin(),
                   [](int n) { return n * 2; });

    // Use move semantics
    std::vector<std::string> source = {"hello", "world"};
    std::vector<std::string> dest = std::move(source);  // No copy

    return 0;
}
```

---

## STL Debugging Tips

```cpp
#include <vector>
#include <cassert>

int main() {
    std::vector<int> vec{1, 2, 3, 4, 5};

    // Use assertions for debugging
    assert(!vec.empty());
    assert(vec.size() == 5);

    // Check iterator validity
    auto it = vec.begin();
    vec.push_back(6);  // May invalidate iterators in vector
    // Using 'it' here might be undefined behavior

    // Safe approach: refresh iterator after modification
    it = vec.begin();

    // Debug output
    #ifdef DEBUG
    std::cout << "Vector size: " << vec.size() << std::endl;
    std::cout << "Vector capacity: " << vec.capacity() << std::endl;
    for (size_t i = 0; i < vec.size(); ++i) {
        std::cout << "vec[" << i << "] = " << vec[i] << std::endl;
    }
    #endif

    // Use debug versions of containers (implementation-specific)
    // Example: g++ -D_GLIBCXX_DEBUG

    return 0;
}
```

---

## Common STL Pitfalls

1. **Iterator invalidation** after container modifications
1. **Dangling iterators** after container destruction
1. **Using wrong container** for the task
1. **Not checking return values** of find operations
1. **Mixing signed/unsigned** in comparisons
1. **Forgetting to include headers**
1. **Memory leaks** with raw pointers in containers

---

## Real-World Example: Word Counter

```cpp
#include <iostream>
#include <string>
#include <map>
#include <vector>
#include <algorithm>
#include <sstream>

int main() {
    std::string text = "the quick brown fox jumps over the lazy dog the fox is quick";
    std::istringstream iss(text);
    std::string word;
    std::map<std::string, int> word_count;

    // Count words
    while (iss >> word) {
        ++word_count[word];
    }

    // Convert to vector for sorting
    std::vector<std::pair<std::string, int>> sorted_words(
        word_count.begin(), word_count.end());

    // Sort by count (descending)
    std::sort(sorted_words.begin(), sorted_words.end(),
              [](const auto& a, const auto& b) {
                  return a.second > b.second;
              });

    // Display results
    std::cout << "Word frequency:" << std::endl;
    for (const auto& pair : sorted_words) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }

    return 0;
}
```

---

## STL and Modern C++

```cpp
#include <vector>
#include <algorithm>
#include <ranges>  // C++20

int main() {
    std::vector<int> numbers{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // Traditional STL approach
    std::vector<int> evens;
    std::copy_if(numbers.begin(), numbers.end(), std::back_inserter(evens),
                 [](int n) { return n % 2 == 0; });

    std::transform(evens.begin(), evens.end(), evens.begin(),
                   [](int n) { return n * n; });

    // C++20 Ranges approach
    #if __cplusplus >= 202002L
    auto result = numbers
                | std::views::filter([](int n) { return n % 2 == 0; })
                | std::views::transform([](int n) { return n * n; });

    for (int n : result) {
        std::cout << n << " ";
    }
    #endif

    // Auto and range-based for (C++11)
    for (const auto& num : numbers) {
        std::cout << num << " ";
    }

    return 0;
}
```

---

## Summary

The STL provides:

1. **Containers** - efficient data structures for different needs
1. **Iterators** - uniform way to access container elements
1. **Algorithms** - reusable operations on containers
1. **Function objects** - customizable behavior
1. **Utilities** - helper classes and functions

Key benefits: efficiency, reliability, consistency, and productivity. The STL is the foundation of modern C++ programming.

Master the STL to write more efficient, maintainable, and expressive C++ code.

---

## Vector Operations

```cpp
std::vector<int> vec{1, 2, 3, 4, 5};

// Size and capacity
std::cout << "Size: " << vec.size() << std::endl;
std::cout << "Capacity: " << vec.capacity() << std::endl;
std::cout << "Empty: " << vec.empty() << std::endl;

// Modifying
vec.insert(vec.begin() + 2, 99);  // Insert 99 at position 2
vec.erase(vec.begin() + 1);       // Remove element at position 1
vec.pop_back();                   // Remove last element
vec.clear();                      // Remove all elements

// Resizing
vec.resize(10);                   // Resize to 10 elements
vec.reserve(100);                 // Reserve space for 100 elements

// Access to underlying array
int* data = vec.data();           // Get pointer to underlying array
```

---

## Iterating Through Vector

```cpp
std::vector<int> numbers{1, 2, 3, 4, 5};

// Traditional for loop
for (size_t i = 0; i < numbers.size(); ++i) {
    std::cout << numbers[i] << " ";
}

// Range-based for loop (C++11)
for (int num : numbers) {
    std::cout << num << " ";
}

// Range-based for loop with reference
for (int& num : numbers) {
    num *= 2;  // Modify elements
}

// Iterator-based loop
for (auto it = numbers.begin(); it != numbers.end(); ++it) {
    std::cout << *it << " ";
}

// Using algorithms
std::for_each(numbers.begin(), numbers.end(),
              [](int n) { std::cout << n << " "; });
```

---

## List - Doubly Linked List

```cpp
#include <list>

int main() {
    std::list<int> numbers{1, 2, 3, 4, 5};

    // Adding elements
    numbers.push_front(0);    // Add to beginning
    numbers.push_back(6);     // Add to end

    // Inserting
    auto it = numbers.begin();
    std::advance(it, 3);      // Move iterator to position 3
    numbers.insert(it, 99);   // Insert 99 at position 3

    // Removing
    numbers.remove(99);       // Remove all elements with value 99
    numbers.pop_front();      // Remove first element
    numbers.pop_back();       // Remove last element

    // List-specific operations
    std::list<int> other{10, 11, 12};
    numbers.splice(numbers.end(), other);  // Move elements from other
    numbers.sort();           // Sort the list
    numbers.unique();         // Remove consecutive duplicates

    return 0;
}
```

---

## Deque - Double-Ended Queue

```cpp
#include <deque>

int main() {
    std::deque<int> dq;

    // Adding elements at both ends
    dq.push_back(1);     // Add to end: [1]
    dq.push_front(0);    // Add to front: [0, 1]
    dq.push_back(2);     // Add to end: [0, 1, 2]
    dq.push_front(-1);   // Add to front: [-1, 0, 1, 2]

    // Random access (like vector)
    std::cout << "Element at index 2: " << dq[2] << std::endl;

    // Removing from both ends
    dq.pop_front();      // Remove from front: [0, 1, 2]
    dq.pop_back();       // Remove from end: [0, 1]

    // Deque supports most vector operations
    dq.resize(10);
    dq.insert(dq.begin() + 2, 99);

    return 0;
}
```

---

## Set - Ordered Unique Elements

```cpp
#include <set>

int main() {
    std::set<int> numbers{5, 2, 8, 2, 1, 9};  // Duplicates automatically removed

    // Insertion
    numbers.insert(3);
    numbers.insert(2);  // Won't be added (already exists)

    // Finding elements
    auto it = numbers.find(5);
    if (it != numbers.end()) {
        std::cout << "Found: " << *it << std::endl;
    }

    // Check if element exists
    if (numbers.count(8) > 0) {
        std::cout << "8 is in the set" << std::endl;
    }

    // Removing elements
    numbers.erase(2);     // Remove by value
    numbers.erase(it);    // Remove by iterator

    // Iteration (elements are sorted)
    for (int num : numbers) {
        std::cout << num << " ";  // Output: 1 3 8 9 (sorted order)
    }

    return 0;
}
```

---

## Map - Key-Value Pairs

```cpp
#include <map>

int main() {
    std::map<std::string, int> ages;

    // Insertion
    ages["Alice"] = 25;
    ages["Bob"] = 30;
    ages.insert({"Charlie", 35});
    ages.insert(std::make_pair("David", 28));

    // Access
    std::cout << "Alice is " << ages["Alice"] << " years old" << std::endl;
    std::cout << "Bob is " << ages.at("Bob") << " years old" << std::endl;

    // Safe access with find
    auto it = ages.find("Eve");
    if (it != ages.end()) {
        std::cout << "Eve is " << it->second << " years old" << std::endl;
    } else {
        std::cout << "Eve not found" << std::endl;
    }

    // Iteration
    for (const auto& pair : ages) {
        std::cout << pair.first << ": " << pair.second << std::endl;
    }

    return 0;
}
```

---

## Unordered Containers (Hash Tables)

```cpp
#include <unordered_set>
#include <unordered_map>

int main() {
    // Unordered set - O(1) average operations
    std::unordered_set<std::string> words{"hello", "world", "cpp"};
    words.insert("programming");

    if (words.find("hello") != words.end()) {
        std::cout << "Found 'hello'" << std::endl;
    }

    // Unordered map - O(1) average operations
    std::unordered_map<std::string, int> word_count;
    word_count["hello"] = 5;
    word_count["world"] = 3;

    // Hash table performance info
    std::cout << "Bucket count: " << word_count.bucket_count() << std::endl;
    std::cout << "Load factor: " << word_count.load_factor() << std::endl;
    std::cout << "Max load factor: " << word_count.max_load_factor() << std::endl;

    return 0;
}
```

---

## Container Adaptors

```cpp
#include <stack>
#include <queue>

int main() {
    // Stack (LIFO - Last In, First Out)
    std::stack<int> stk;
    stk.push(1);
    stk.push(2);
    stk.push(3);

    while (!stk.empty()) {
        std::cout << stk.top() << " ";  // 3 2 1
        stk.pop();
    }
    std::cout << std::endl;

    // Queue (FIFO - First In, First Out)
    std::queue<int> que;
    que.push(1);
    que.push(2);
    que.push(3);

    while (!que.empty()) {
        std::cout << que.front() << " ";  // 1 2 3
        que.pop();
    }
    std::cout << std::endl;

    return 0;
}
```

---

## Priority Queue

```cpp
#include <queue>
#include <vector>

int main() {
    // Max heap by default (largest element at top)
    std::priority_queue<int> max_heap;
    max_heap.push(3);
    max_heap.push(1);
    max_heap.push(4);
    max_heap.push(2);

    while (!max_heap.empty()) {
        std::cout << max_heap.top() << " ";  // 4 3 2 1
        max_heap.pop();
    }
    std::cout << std::endl;

    // Min heap (smallest element at top)
    std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;
    min_heap.push(3);
    min_heap.push(1);
    min_heap.push(4);
    min_heap.push(2);

    while (!min_heap.empty()) {
        std::cout << min_heap.top() << " ";  // 1 2 3 4
        min_heap.pop();
    }

    return 0;
}
```

---

## Iterators - The Bridge

<svg width="600" height="300" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="120" height="60" fill="#e6f3ff" stroke="#0066cc"/>
  <text x="110" y="75" text-anchor="middle" font-size="12" font-weight="bold">Container</text>
  <text x="110" y="95" text-anchor="middle" font-size="12">vector, list, etc.</text>

  <rect x="240" y="50" width="120" height="60" fill="#ffe6e6" stroke="#cc0000"/>
  <text x="300" y="75" text-anchor="middle" font-size="12" font-weight="bold">Iterator</text>
  <text x="300" y="95" text-anchor="middle" font-size="12">begin(), end()</text>

  <rect x="430" y="50" width="120" height="60" fill="#e6ffe6" stroke="#00cc00"/>
  <text x="490" y="75" text-anchor="middle" font-size="12" font-weight="bold">Algorithm</text>
  <text x="490" y="95" text-anchor="middle" font-size="12">sort, find, etc.</text>

  <line x1="170" y1="80" x2="240" y2="80" stroke="#666" marker-end="url(#arrowhead)"/>
  <line x1="360" y1="80" x2="430" y2="80" stroke="#666" marker-end="url(#arrowhead)"/>

  <rect x="150" y="160" width="300" height="100" fill="#f9f9f9" stroke="#333"/>
  <text x="300" y="180" text-anchor="middle" font-size="14" font-weight="bold">Iterator Types</text>
  <text x="300" y="200" text-anchor="middle" font-size="12">Input → Forward → Bidirectional → Random Access</text>
  <text x="300" y="220" text-anchor="middle" font-size="12">Each type supports more operations</text>
  <text x="300" y="240" text-anchor="middle" font-size="12">Algorithms require minimum iterator category</text>

  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

---

## Iterator Categories

```cpp
#include <vector>
#include <list>
#include <forward_list>

int main() {
    std::vector<int> vec{1, 2, 3, 4, 5};
    std::list<int> lst{1, 2, 3, 4, 5};

    // Random Access Iterator (vector, deque)
    auto vec_it = vec.begin();
    vec_it += 3;           // Jump to position 3
    vec_it -= 1;           // Jump back 1 position
    int diff = vec.end() - vec.begin();  // Calculate distance

    // Bidirectional Iterator (list, set, map)
    auto lst_it = lst.begin();
    ++lst_it;              // Move forward
    --lst_it;              // Move backward
    // lst_it += 3;        // Error! No random access

    // Forward Iterator (forward_list, unordered containers)
    std::forward_list<int> fwd_lst{1, 2, 3};
    auto fwd_it = fwd_lst.begin();
    ++fwd_it;              // Move forward only
    // --fwd_it;           // Error! No backward movement

    return 0;
}
```

---

## Iterator Operations

```cpp
#include <vector>
#include <iterator>

int main() {
    std::vector<int> numbers{1, 2, 3, 4, 5};

    // Basic iterator operations
    auto it = numbers.begin();
    std::cout << *it << std::endl;     // Dereference: 1
    ++it;                              // Pre-increment
    std::cout << *it << std::endl;     // 2

    // Iterator arithmetic (random access)
    it = numbers.begin();
    std::advance(it, 3);               // Move iterator 3 positions
    std::cout << *it << std::endl;     // 4

    // Distance between iterators
    auto distance = std::distance(numbers.begin(), numbers.end());
    std::cout << "Distance: " << distance << std::endl;  // 5

    // Reverse iterators
    for (auto rit = numbers.rbegin(); rit != numbers.rend(); ++rit) {
        std::cout << *rit << " ";      // 5 4 3 2 1
    }

    return 0;
}
```

---

## Common Algorithms

```cpp
#include <algorithm>
#include <vector>
#include <numeric>

int main() {
    std::vector<int> numbers{3, 1, 4, 1, 5, 9, 2, 6};

    // Sorting
    std::sort(numbers.begin(), numbers.end());

    // Searching
    auto it = std::find(numbers.begin(), numbers.end(), 5);
    if (it != numbers.end()) {
        std::cout << "Found 5 at position: "
                  << std::distance(numbers.begin(), it) << std::endl;
    }

    // Binary search (requires sorted container)
    bool found = std::binary_search(numbers.begin(), numbers.end(), 4);

    // Counting
    int count = std::count(numbers.begin(), numbers.end(), 1);
    std::cout << "Number of 1's: " << count << std::endl;

    return 0;
}
```

---

## Algorithm Categories

<svg width="600" height="400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="20" width="160" height="80" fill="#e6f3ff" stroke="#0066cc"/>
  <text x="130" y="40" text-anchor="middle" font-size="12" font-weight="bold">Non-modifying</text>
  <text x="130" y="55" text-anchor="middle" font-size="10">find, count, equal</text>
  <text x="130" y="70" text-anchor="middle" font-size="10">search, for_each</text>
  <text x="130" y="85" text-anchor="middle" font-size="10">all_of, any_of</text>

  <rect x="220" y="20" width="160" height="80" fill="#ffe6e6" stroke="#cc0000"/>
  <text x="300" y="40" text-anchor="middle" font-size="12" font-weight="bold">Modifying</text>
  <text x="300" y="55" text-anchor="middle" font-size="10">copy, move, fill</text>
  <text x="300" y="70" text-anchor="middle" font-size="10">transform, replace</text>
  <text x="300" y="85" text-anchor="middle" font-size="10">remove, unique</text>

  <rect x="390" y="20" width="160" height="80" fill="#e6ffe6" stroke="#00cc00"/>
  <text x="470" y="40" text-anchor="middle" font-size="12" font-weight="bold">Sorting</text>
  <text x="470" y="55" text-anchor="middle" font-size="10">sort, stable_sort</text>
  <text x="470" y="70" text-anchor="middle" font-size="10">partial_sort</text>
  <text x="470" y="85" text-anchor="middle" font-size="10">nth_element</text>

  <rect x="50" y="120" width="160" height="80" fill="#fff0e6" stroke="#ff6600"/>
  <text x="130" y="140" text-anchor="middle" font-size="12" font-weight="bold">Binary Search</text>
  <text x="130" y="155" text-anchor="middle" font-size="10">binary_search</text>
  <text x="130" y="170" text-anchor="middle" font-size="10">lower_bound</text>
  <text x="130" y="185" text-anchor="middle" font-size="10">upper_bound</text>

  <rect x="220" y="120" width="160" height="80" fill="#f0e6ff" stroke="#6600cc"/>
  <text x="300" y="140" text-anchor="middle" font-size="12" font-weight="bold">Set Operations</text>
  <text x="300" y="155" text-anchor="middle" font-size="10">set_union</text>
  <text x="300" y="170" text-anchor="middle" font-size="10">set_intersection</text>
  <text x="300" y="185" text-anchor="middle" font-size="10">set_difference</text>

  <rect x="390" y="120" width="160" height="80" fill="#ffffcc" stroke="#cccc00"/>
  <text x="470" y="140" text-anchor="middle" font-size="12" font-weight="bold">Numeric</text>
  <text x="470" y="155" text-anchor="middle" font-size="10">accumulate</text>
  <text x="470" y="170" text-anchor="middle" font-size="10">inner_product</text>
  <text x="470" y="185" text-anchor="middle" font-size="10">partial_sum</text>

  <rect x="135" y="220" width="160" height="80" fill="#e6f0ff" stroke="#0080ff"/>
  <text x="215" y="240" text-anchor="middle" font-size="12" font-weight="bold">Heap Operations</text>
  <text x="215" y="255" text-anchor="middle" font-size="10">make_heap</text>
  <text x="215" y="270" text-anchor="middle" font-size="10">push_heap</text>
  <text x="215" y="285" text-anchor="middle" font-size="10">pop_heap</text>

  <rect x="305" y="220" width="160" height="80" fill="#ffe0e6" stroke="#ff4080"/>
  <text x="385" y="240" text-anchor="middle" font-size="12" font-weight="bold">Permutation</text>
  <text x="385" y="255" text-anchor="middle" font-size="10">next_permutation</text>
  <text x="385" y="270" text-anchor="middle" font-size="10">prev_permutation</text>
  <text x="385" y="285" text-anchor="middle" font-size="10">shuffle</text>
</svg>

---

## Searching Algorithms

```cpp
#include <algorithm>
#include <vector>

int main() {
    std::vector<int> numbers{1, 2, 3, 4, 5, 6, 7, 8, 9};

    // Linear search
    auto it = std::find(numbers.begin(), numbers.end(), 5);
    if (it != numbers.end()) {
        std::cout << "Found 5" << std::endl;
    }

    // Find with predicate
    auto even_it = std::find_if(numbers.begin(), numbers.end(),
                                [](int n) { return n % 2 == 0; });

    // Binary search (container must be sorted)
    bool found = std::binary_search(numbers.begin(), numbers.end(), 6);

    // Lower bound (first position where element could be inserted)
    auto lower = std::lower_bound(numbers.begin(), numbers.end(), 5);

    // Upper bound (last position where element could be inserted)
    auto upper = std::upper_bound(numbers.begin(), numbers.end(), 5);

    // Equal range (both bounds at once)
    auto range = std::equal_range(numbers.begin(), numbers.end(), 5);

    return 0;
}
```

---

## Modifying Algorithms

```cpp
#include <algorithm>
#include <vector>

int main() {
    std::vector<int> source{1, 2, 3, 4, 5};
    std::vector<int> dest(5);
    // Copy
    std::copy(source.begin(), source.end(), dest.begin());
    // Copy with condition
    std::vector<int> evens;
    std::copy_if(source.begin(), source.end(), std::back_inserter(evens),
                 [](int n) { return n % 2 == 0; });
    // Transform (modify elements while copying)
    std::vector<int> doubled(5);
    std::transform(source.begin(), source.end(), doubled.begin(),
                   [](int n) { return n * 2; });
    // Fill
    std::fill(dest.begin(), dest.end(), 42);
    // Replace
    std::replace(source.begin(), source.end(), 3, 99);  // Replace all 3s with 99
    // Remove (doesn't actually remove, returns new end iterator)
    auto new_end = std::remove(source.begin(), source.end(), 2);
    source.erase(new_end, source.end());  // Actually remove elements
    return 0;
}
