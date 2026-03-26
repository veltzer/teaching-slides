# The Standard Template Library

---

## Chapter Overview

1. STL components overview
1. Containers and their trade-offs
1. Iterators and ranges
1. Algorithms and their usage
1. Extending and customizing STL

---

## STL Architecture

<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
  <text x="200" y="30" text-anchor="middle" font-size="18" font-weight="bold">STL Components</text>
  <rect x="50" y="60" width="120" height="50" fill="#ffcccc" stroke="#333"/>
  <text x="110" y="90" text-anchor="middle" font-size="14">Containers</text>
  <rect x="230" y="60" width="120" height="50" fill="#ccffcc" stroke="#333"/>
  <text x="290" y="90" text-anchor="middle" font-size="14">Algorithms</text>
  <rect x="140" y="140" width="120" height="50" fill="#ccccff" stroke="#333"/>
  <text x="200" y="170" text-anchor="middle" font-size="14">Iterators</text>
  <rect x="50" y="220" width="120" height="50" fill="#ffffcc" stroke="#333"/>
  <text x="110" y="250" text-anchor="middle" font-size="14">Allocators</text>
  <rect x="230" y="220" width="120" height="50" fill="#ffccff" stroke="#333"/>
  <text x="290" y="250" text-anchor="middle" font-size="14">Functors</text>
  <line x1="110" y1="110" x2="200" y2="140" stroke="#333" stroke-width="2"/>
  <line x1="290" y1="110" x2="200" y2="140" stroke="#333" stroke-width="2"/>
</svg>

---

## Container Categories

```cpp
// Sequence containers - ordered by position
std::vector<int> vec;         // Dynamic array
std::deque<int> deq;          // Double-ended queue
std::list<int> lst;           // Doubly-linked list
std::forward_list<int> flst;  // Singly-linked list
std::array<int, 10> arr;      // Fixed-size array

// Associative containers - ordered by key
std::set<int> s;              // Unique keys
std::multiset<int> ms;        // Duplicate keys allowed
std::map<int, string> m;      // Key-value pairs
std::multimap<int, string> mm; // Duplicate keys allowed

// Unordered containers - hash tables
std::unordered_set<int> us;
std::unordered_multiset<int> ums;
std::unordered_map<int, string> um;
std::unordered_multimap<int, string> umm;

// Container adapters
std::stack<int> stk;          // LIFO
std::queue<int> que;          // FIFO
std::priority_queue<int> pq;  // Heap
```

---

## Vector Deep Dive

```cpp
// Vector growth and capacity
std::vector<int> vec;
vec.reserve(100);  // Allocate space for 100 elements

std::cout << "Size: " << vec.size() << '\n';         // 0
std::cout << "Capacity: " << vec.capacity() << '\n'; // 100

// Efficient insertion
vec.push_back(42);           // Amortized O(1)
vec.emplace_back(43);        // Construct in-place

// Bulk operations
vec.resize(50);              // Size = 50, default construct
vec.resize(60, -1);          // Size = 60, new elements = -1

// Memory management
vec.shrink_to_fit();         // Release unused memory
vec.clear();                 // Remove all elements (capacity unchanged)

// Direct access
int* data = vec.data();      // Pointer to underlying array
```

---

## Deque Internals

```cpp
// Deque - chunks of contiguous memory
std::deque<int> deq;

// Efficient at both ends
deq.push_front(10);  // O(1)
deq.push_back(20);   // O(1)
deq.pop_front();     // O(1)
deq.pop_back();      // O(1)

// Random access still O(1)
int val = deq[5];    // But slower than vector

// No capacity() or reserve()
// Memory in chunks, not contiguous

// When to use deque:
// 1. Need insertion/removal at both ends
// 2. Don't need pointer stability
// 3. Don't need contiguous memory
```

---

## List Operations

```cpp
// List - node-based container
std::list<int> lst = {1, 2, 3, 4, 5};

// No random access
// int val = lst[2];  // Error!

// Iterator-based access
auto it = lst.begin();
std::advance(it, 2);  // O(n)
int val = *it;        // val = 3

// Efficient insertion/removal anywhere
lst.insert(it, 10);   // O(1) with iterator
lst.erase(it);        // O(1) with iterator

// Splice operations - O(1)
std::list<int> other = {6, 7, 8};
lst.splice(lst.end(), other);  // Move all elements

// Unique list operations
lst.sort();           // Member function, not std::sort
lst.unique();         // Remove consecutive duplicates
lst.reverse();        // Reverse list
```

---

## Associative Containers

```cpp
// Set - unique sorted elements
std::set<int> s = {3, 1, 4, 1, 5};  // {1, 3, 4, 5}

// Insertion returns pair<iterator, bool>
auto [it, inserted] = s.insert(2);
if (inserted) {
    std::cout << "Inserted " << *it << '\n';
}

// Efficient lookups - O(log n)
if (s.find(3) != s.end()) {
    std::cout << "Found 3\n";
}

// Range operations
auto lower = s.lower_bound(2);  // First >= 2
auto upper = s.upper_bound(4);  // First > 4
auto range = s.equal_range(3);  // [lower, upper)

// Custom comparator
std::set<int, std::greater<int>> descending;
descending.insert({3, 1, 4, 1, 5});  // {5, 4, 3, 1}

---

## Map Usage

```cpp
// Map - key-value pairs
std::map<std::string, int> ages;

// Insert methods
ages["Alice"] = 30;                    // Operator[]
ages.insert({"Bob", 25});              // Insert pair
ages.emplace("Charlie", 35);           // Construct in-place

// Access with bounds checking
try {
    int age = ages.at("David");        // Throws if not found
} catch (const std::out_of_range& e) {
    std::cout << "Not found\n";
}

// Safe access with default
int age = ages["Eve"];  // Creates entry with value 0

// Iterate over pairs
for (const auto& [name, age] : ages) {
    std::cout << name << ": " << age << '\n';
}

// Structured bindings with insert
auto [it, success] = ages.insert({"Frank", 40});
```

---

## Unordered Containers

```cpp
// Hash table implementation
std::unordered_map<std::string, int> hash_map;

// Average O(1) operations
hash_map["key"] = 42;
auto it = hash_map.find("key");  // O(1) average

// Hash table statistics
std::cout << "Bucket count: " << hash_map.bucket_count() << '\n';
std::cout << "Load factor: " << hash_map.load_factor() << '\n';
std::cout << "Max load factor: " << hash_map.max_load_factor() << '\n';

// Control rehashing
hash_map.reserve(1000);  // Reserve buckets
hash_map.rehash(100);    // Set bucket count

// Custom hash function
struct Point {
    int x, y;
};

struct PointHash {
    size_t operator()(const Point& p) const {
        return std::hash<int>{}(p.x) ^ (std::hash<int>{}(p.y) << 1);
    }
};

std::unordered_set<Point, PointHash> points;
```

---

## Container Adapters

```cpp
// Stack - LIFO adapter
std::stack<int> stk;  // Default: deque
std::stack<int, std::vector<int>> vec_stack;

stk.push(10);
stk.push(20);
int top = stk.top();  // 20
stk.pop();            // Remove 20

// Queue - FIFO adapter
std::queue<int> que;
que.push(10);         // Add to back
que.push(20);
int front = que.front();  // 10
que.pop();            // Remove from front

// Priority Queue - heap adapter
std::priority_queue<int> max_heap;  // Default: max heap
std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;

max_heap.push(3);
max_heap.push(1);
max_heap.push(4);
int largest = max_heap.top();  // 4
```

---

## Iterator Categories

```cpp
// Iterator hierarchy
struct input_iterator_tag {};
struct output_iterator_tag {};
struct forward_iterator_tag : input_iterator_tag {};
struct bidirectional_iterator_tag : forward_iterator_tag {};
struct random_access_iterator_tag : bidirectional_iterator_tag {};

// Input iterator - single pass, read only
std::istream_iterator<int> input(std::cin);

// Output iterator - single pass, write only
std::ostream_iterator<int> output(std::cout, " ");

// Forward iterator - multiple pass, read/write
std::forward_list<int>::iterator fwd;

// Bidirectional iterator - can go backwards
std::list<int>::iterator bidir;

// Random access iterator - arithmetic operations
std::vector<int>::iterator random;
random += 5;  // Jump 5 positions
```

---

## Iterator Operations

```cpp
// Iterator utilities
std::vector<int> vec = {1, 2, 3, 4, 5};
auto it = vec.begin();

// Advance iterator
std::advance(it, 3);  // it points to 4

// Distance between iterators
auto dist = std::distance(vec.begin(), it);  // 3

// Next/prev (C++11)
auto next_it = std::next(it);     // Points to 5
auto prev_it = std::prev(it, 2);  // Points to 2

// Iterator traits
using traits = std::iterator_traits<decltype(it)>;
using value_type = traits::value_type;        // int
using category = traits::iterator_category;   // random_access_iterator_tag

// Reverse iterators
for (auto rit = vec.rbegin(); rit != vec.rend(); ++rit) {
    std::cout << *rit << ' ';  // 5 4 3 2 1
}
```

---

## Common Algorithms

```cpp
std::vector<int> vec = {3, 1, 4, 1, 5, 9, 2, 6};

// Non-modifying algorithms
auto it = std::find(vec.begin(), vec.end(), 5);
int count = std::count(vec.begin(), vec.end(), 1);  // 2
bool has_nine = std::any_of(vec.begin(), vec.end(),
                           [](int x) { return x == 9; });

// Modifying algorithms
std::sort(vec.begin(), vec.end());
std::reverse(vec.begin(), vec.end());
std::rotate(vec.begin(), vec.begin() + 3, vec.end());

// Partitioning
auto pivot = std::partition(vec.begin(), vec.end(),
                           [](int x) { return x < 5; });

// Numeric algorithms
int sum = std::accumulate(vec.begin(), vec.end(), 0);
std::partial_sum(vec.begin(), vec.end(), vec.begin());
```

---

## Algorithm Complexity

```cpp
// O(n) algorithms
std::find, std::count, std::copy, std::fill
std::generate, std::transform, std::for_each

// O(n log n) algorithms
std::sort, std::stable_sort, std::partial_sort
std::nth_element (average O(n))

// O(n²) worst case
std::unique (with unsorted range)

// O(log n) - on sorted ranges
std::binary_search, std::lower_bound, std::upper_bound

// O(1)
std::swap, std::iter_swap

// Know your complexity!
std::vector<int> vec(1000000);
// This is O(n²) - very slow!
for (auto it = vec.begin(); it != vec.end(); ++it) {
    vec.erase(it);  // O(n) operation in loop
}
```

---

## Lambda with Algorithms

```cpp
std::vector<int> vec = {1, 2, 3, 4, 5};

// Transform with lambda
std::transform(vec.begin(), vec.end(), vec.begin(),
               [](int x) { return x * x; });

// Find with lambda
auto it = std::find_if(vec.begin(), vec.end(),
                      [](int x) { return x > 10; });

// Capture in lambdas
int threshold = 10;
auto count = std::count_if(vec.begin(), vec.end(), [threshold](int x) { return x > threshold; });

// Mutable lambda
int sum = 0;
std::for_each(vec.begin(), vec.end(), [&sum](int x) { sum += x; });

// Generic lambda (C++14)
auto print = [](const auto& x) { std::cout << x << ' '; };
std::for_each(vec.begin(), vec.end(), print);
```

---

## Emplace Operations

```cpp
// Construct in-place to avoid copies
struct Widget {
    std::string name;
    int value;

    Widget(std::string n, int v) : name(std::move(n)), value(v) {
        std::cout << "Constructor\n";
    }

    Widget(const Widget&) {
        std::cout << "Copy constructor\n";
    }

    Widget(Widget&&) {
        std::cout << "Move constructor\n";
    }
};

std::vector<Widget> vec;

// Traditional push_back - constructs then moves
vec.push_back(Widget("A", 1));  // Constructor + Move

// Emplace - constructs in-place
vec.emplace_back("B", 2);  // Constructor only

// Works with all containers
std::map<int, Widget> m;
m.emplace(1, Widget("C", 3));  // Construct pair in-place
m.emplace(std::piecewise_construct,
          std::forward_as_tuple(2),
          std::forward_as_tuple("D", 4));
```

---

## Custom Allocators

```cpp
// Simple pool allocator
template<typename T, size_t PoolSize = 1024>
class PoolAllocator {
private:
    static uint8_t pool[PoolSize];
    static size_t offset;

public:
    using value_type = T;

    T* allocate(size_t n) {
        if (offset + n * sizeof(T) > PoolSize) {
            throw std::bad_alloc();
        }
        T* result = reinterpret_cast<T*>(pool + offset);
        offset += n * sizeof(T);
        return result;
    }

    void deallocate(T* p, size_t n) {
        // Simple allocator - no deallocation
    }

    template<typename U>
    struct rebind {
        using other = PoolAllocator<U, PoolSize>;
    };
};

// Usage
std::vector<int, PoolAllocator<int>> vec;
```

---

## Manipulating Algorithms

```cpp
// Copy algorithms
std::vector<int> src = {1, 2, 3, 4, 5};
std::vector<int> dst(5);

std::copy(src.begin(), src.end(), dst.begin());
std::copy_if(src.begin(), src.end(), dst.begin(),
             [](int x) { return x % 2 == 0; });
std::copy_n(src.begin(), 3, dst.begin());
std::copy_backward(src.begin(), src.end(), dst.end());

// Move algorithms
std::vector<std::string> v1 = {"a", "b", "c"};
std::vector<std::string> v2(3);
std::move(v1.begin(), v1.end(), v2.begin());

// Fill algorithms
std::fill(vec.begin(), vec.end(), 42);
std::fill_n(vec.begin(), 5, 0);
std::generate(vec.begin(), vec.end(), rand);
std::generate_n(vec.begin(), 5, [n=0]() mutable { return n++; });

// Remove algorithms (erase-remove idiom)
vec.erase(std::remove(vec.begin(), vec.end(), 3), vec.end());
vec.erase(std::remove_if(vec.begin(), vec.end(),
                         [](int x) { return x < 0; }), vec.end());
```

---

## Set Algorithms

```cpp
// Requires sorted ranges!
std::vector<int> v1 = {1, 2, 3, 4, 5};
std::vector<int> v2 = {3, 4, 5, 6, 7};
std::vector<int> result;

// Set intersection
std::set_intersection(v1.begin(), v1.end(),
                     v2.begin(), v2.end(),
                     std::back_inserter(result));  // {3, 4, 5}

result.clear();
// Set union
std::set_union(v1.begin(), v1.end(),
               v2.begin(), v2.end(),
               std::back_inserter(result));  // {1, 2, 3, 4, 5, 6, 7}

result.clear();
// Set difference
std::set_difference(v1.begin(), v1.end(),
                   v2.begin(), v2.end(),
                   std::back_inserter(result));  // {1, 2}

// Merge sorted ranges
std::vector<int> merged;
std::merge(v1.begin(), v1.end(),
           v2.begin(), v2.end(),
           std::back_inserter(merged));
```

---

## Heap Algorithms

```cpp
std::vector<int> vec = {3, 1, 4, 1, 5, 9, 2, 6};

// Make heap - O(n)
std::make_heap(vec.begin(), vec.end());  // Max heap

// Heap operations
vec.push_back(8);
std::push_heap(vec.begin(), vec.end());  // O(log n)

std::pop_heap(vec.begin(), vec.end());   // O(log n)
vec.pop_back();  // Remove largest

// Heap sort - O(n log n)
std::sort_heap(vec.begin(), vec.end());

// Custom comparator for min heap
std::make_heap(vec.begin(), vec.end(), std::greater<int>());

// Priority queue uses heap algorithms internally
std::priority_queue<int> pq(vec.begin(), vec.end());
```

---

## Permutation Algorithms

```cpp
std::vector<int> vec = {1, 2, 3};

// Generate all permutations
do {
    for (int x : vec) std::cout << x << ' ';
    std::cout << '\n';
} while (std::next_permutation(vec.begin(), vec.end()));
// Output: 1 2 3, 1 3 2, 2 1 3, 2 3 1, 3 1 2, 3 2 1

// Previous permutation
std::prev_permutation(vec.begin(), vec.end());

// Check if permutation
std::vector<int> v1 = {1, 2, 3, 4};
std::vector<int> v2 = {3, 1, 4, 2};
bool is_perm = std::is_permutation(v1.begin(), v1.end(),
                                   v2.begin());  // true

// Rotate as permutation
std::rotate(vec.begin(), vec.begin() + 1, vec.end());
```

---

## Numeric Algorithms

```cpp
#include <numeric>

std::vector<int> vec = {1, 2, 3, 4, 5};

// Accumulate with initial value
int sum = std::accumulate(vec.begin(), vec.end(), 0);
int product = std::accumulate(vec.begin(), vec.end(), 1,
                             std::multiplies<int>());

// Inner product
std::vector<int> v2 = {10, 20, 30, 40, 50};
int dot_product = std::inner_product(vec.begin(), vec.end(),
                                    v2.begin(), 0);

// Partial sum
std::vector<int> partial(5);
std::partial_sum(vec.begin(), vec.end(), partial.begin());
// partial = {1, 3, 6, 10, 15}

// Adjacent difference
std::vector<int> diff(5);
std::adjacent_difference(vec.begin(), vec.end(), diff.begin());
// diff = {1, 1, 1, 1, 1}

// Iota - fill with increasing values
std::iota(vec.begin(), vec.end(), 10);  // {10, 11, 12, 13, 14}
```

---

## Execution Policies (C++17)

```cpp
#include <execution>

std::vector<int> vec(1000000);
std::iota(vec.begin(), vec.end(), 0);

// Sequential execution (default)
std::sort(vec.begin(), vec.end());

// Parallel execution
std::sort(std::execution::par, vec.begin(), vec.end());

// Parallel unsequenced execution
std::sort(std::execution::par_unseq, vec.begin(), vec.end());

// Unsequenced execution
std::transform(std::execution::unseq,
               vec.begin(), vec.end(), vec.begin(),
               [](int x) { return x * 2; });

// Not all algorithms support execution policies
// Check documentation before using
```

---

## Custom Comparators

```cpp
// Function object
struct CompareLength {
    bool operator()(const std::string& a, const std::string& b) const {
        return a.length() < b.length();
    }
};

std::set<std::string, CompareLength> words;

// Lambda as comparator
auto cmp = [](const auto& a, const auto& b) {
    return a.second < b.second;  // Compare by value
};
std::map<int, int, decltype(cmp)> m(cmp);

// For algorithms
std::sort(vec.begin(), vec.end(),
          [](const auto& a, const auto& b) {
              return std::abs(a) < std::abs(b);  // Sort by absolute value
          });

// Binary predicate
auto equal_ignore_case = [](char a, char b) {
    return std::tolower(a) == std::tolower(b);
};
bool same = std::equal(s1.begin(), s1.end(),
                      s2.begin(), equal_ignore_case);
```

---

## Iterator Adapters

```cpp
// Back inserter - appends to container
std::vector<int> vec;
std::copy(src.begin(), src.end(), std::back_inserter(vec));

// Front inserter - prepends (for deque, list)
std::list<int> lst;
std::copy(src.begin(), src.end(), std::front_inserter(lst));

// Insert iterator - inserts at position
std::set<int> s;
std::copy(src.begin(), src.end(), std::inserter(s, s.begin()));

// Stream iterators
std::copy(vec.begin(), vec.end(),
          std::ostream_iterator<int>(std::cout, " "));

std::vector<int> input_vec;
std::copy(std::istream_iterator<int>(std::cin),
          std::istream_iterator<int>(),
          std::back_inserter(input_vec));

// Move iterator
std::vector<std::string> v1 = {"a", "b", "c"};
std::vector<std::string> v2;
std::copy(std::make_move_iterator(v1.begin()),
          std::make_move_iterator(v1.end()),
          std::back_inserter(v2));
```

---

## Extending STL

```cpp
// Custom container requirements
template<typename T>
class MyContainer {
public:
    using value_type = T;
    using iterator = T*;
    using const_iterator = const T*;
    using size_type = size_t;

    iterator begin() { return data; }
    iterator end() { return data + size; }
    const_iterator begin() const { return data; }
    const_iterator end() const { return data + size; }

    size_type size() const { return size_; }
    bool empty() const { return size_ == 0; }

private:
    T* data;
    size_t size_;
};

// Now works with STL algorithms
MyContainer<int> mc;
std::sort(mc.begin(), mc.end());
auto it = std::find(mc.begin(), mc.end(), 42);
```

---

## Function Objects

```cpp
// Standard function objects
std::plus<int> add;
int sum = add(3, 4);  // 7

std::vector<int> vec = {1, 2, 3, 4, 5};
std::transform(vec.begin(), vec.end(), vec.begin(),
               std::negate<int>());  // {-1, -2, -3, -4, -5}

// Bind function arguments
auto add5 = std::bind(std::plus<int>(), std::placeholders::_1, 5);
int result = add5(10);  // 15

// Member function pointers
struct Widget {
    int value;
    int getValue() const { return value; }
};

std::vector<Widget> widgets = {{1}, {2}, {3}};
std::vector<int> values;
std::transform(widgets.begin(), widgets.end(),
               std::back_inserter(values),
               std::mem_fn(&Widget::getValue));
```

---

## Performance Tips

```cpp
// Reserve capacity
std::vector<int> vec;
vec.reserve(1000);  // Avoid reallocations

// Use emplace
vec.emplace_back(args...);  // Construct in-place

// Choose right container
// Random access → vector
// Frequent insert/remove → list/deque
// Sorted unique → set
// Key-value → map/unordered_map

// Avoid unnecessary copies
const auto& elem = vec[i];  // Reference
for (const auto& item : container) { }  // Range-for with reference

// Use move semantics
vec.push_back(std::move(expensive_object));

// Know algorithm complexity
// std::find → O(n)
// std::binary_search → O(log n) but needs sorted range
```

---

## Common Pitfalls

```cpp
// Iterator invalidation
std::vector<int> vec = {1, 2, 3, 4, 5};
for (auto it = vec.begin(); it != vec.end(); ++it) {
    if (*it == 3) {
        vec.erase(it);  // it now invalid!
    }
}

// Correct approach
vec.erase(std::remove(vec.begin(), vec.end(), 3), vec.end());

// Sorting with invalid comparator
std::sort(vec.begin(), vec.end(),
          [](int a, int b) { return a <= b; });  // Not strict weak ordering!

// Forgetting to sort before set operations
std::set_intersection(v1.begin(), v1.end(),
                     v2.begin(), v2.end(),  // Must be sorted!
                     std::back_inserter(result));
```

---

## Summary

1. STL provides powerful abstractions
1. Choose containers based on requirements
1. Understand iterator categories
1. Know algorithm complexities
1. Use modern features (emplace, move)

---

## Key Takeaways

1. **Containers** have different trade-offs
1. **Iterators** connect containers and algorithms
1. **Algorithms** are generic and reusable
1. **Complexity** matters for performance
1. **Modern STL** features improve efficiency
