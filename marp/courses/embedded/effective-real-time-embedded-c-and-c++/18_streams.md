# Input/Output Using Stream Classes

---

## Common Background of I/O Streams

C++ provides a comprehensive I/O system based on streams
- Stream: sequence of characters flowing from source to destination
- Type-safe and extensible compared to C's printf/scanf
- Consistent interface for files, strings, and console I/O

![common_background_of_i_o_streams](/svg/courses/embedded/effective-real-time-embedded-c-and-c++/18_streams/common_background_of_i_o_streams.svg)

---

## Stream Hierarchy Overview

All stream classes derive from common base classes
- `ios_base`: platform-independent base functionality
- `ios`: template base class with character type
- Input streams derive from `istream`
- Output streams derive from `ostream`

![stream_hierarchy_overview](/svg/courses/embedded/effective-real-time-embedded-c-and-c++/18_streams/stream_hierarchy_overview.svg)

---

## Fundamental Stream Classes and Objects

Key stream objects available globally:
- `cin`: standard input stream
- `cout`: standard output stream
- `cerr`: unbuffered error stream
- `clog`: buffered error stream

```cpp
#include <iostream>
using namespace std;

int main() {
    int value;
    cout << "Enter a number: ";
    cin >> value;
    cout << "You entered: " << value << endl;
    cerr << "Error logging" << endl;
    return 0;
---

## Best Practices Summary

Key guidelines for effective stream usage:

1. **Always check stream state** after I/O operations
1. **Use RAII** for automatic resource management
1. **Prefer binary I/O** for structured data
1. **Minimize flushing** for better performance
1. **Handle errors gracefully** with proper recovery
1. **Use appropriate stream types** for the task
1. **Consider thread safety** in multi-threaded applications
1. **Leverage manipulators** for consistent formatting

```cpp
// Good practice example
void processFile(const string& filename) {
    ifstream file(filename);
    if (!file.is_open()) {
        throw runtime_error("Cannot open: " + filename);
    }

    string line;
    while (getline(file, line)) {
        if (file.bad()) break;
        // Process line safely
    }
    // File automatically closed
}
```

---

## Common Pitfalls to Avoid

Watch out for these common mistakes:

1. **Forgetting to check file open status**
```cpp
// BAD
ofstream file("data.txt");
file << "data";  // May fail silently

// GOOD
ofstream file("data.txt");
if (!file.is_open()) {
    throw runtime_error("Cannot open file");
}
```

1. **Mixing C and C++ I/O after sync disabled**
1. **Using endl when '\n' suffices** (performance)
1. **Not handling stream errors** properly
1. **Forgetting to flush** when needed

---

## Advanced Stream Techniques

Sophisticated stream manipulation:

```cpp
#include <iostream>
#include <sstream>
#include <iomanip>
using namespace std;

// Custom manipulator
ostream& timestamp(ostream& os) {
    auto now = time(nullptr);
    return os << "[" << put_time(localtime(&now), "%Y-%m-%d %H:%M:%S") << "] ";
}

// Parameterized manipulator
class width_fill {
    int w;
    char c;
public:
    width_fill(int width, char fill = ' ') : w(width), c(fill) {}
    friend ostream& operator<<(ostream& os, const width_fill& wf) {
        return os << setw(wf.w) << setfill(wf.c);
    }
};

int main() {
    cout << timestamp << "Application started" << endl;
    cout << width_fill(20, '*') << "Important" << endl;
    return 0;
}
```

---

## Stream States and Error Handling

Every stream has state flags indicating its condition:
- `good()`: stream is ready for I/O
- `eof()`: end-of-file reached
- `fail()`: I/O operation failed
- `bad()`: stream is corrupted

```cpp
#include <iostream>
#include <fstream>
using namespace std;

void checkStreamState(istream& stream) {
    if (stream.good()) cout << "Stream is good\n";
    if (stream.eof()) cout << "End of file reached\n";
    if (stream.fail()) cout << "I/O operation failed\n";
    if (stream.bad()) cout << "Stream is corrupted\n";
}
```

---

## Standard Stream Operators << and >>

Insertion operator (<<) for output:
- Converts data to character sequence
- Returns reference to stream for chaining

Extraction operator (>>) for input:
- Converts character sequence to data
- Skips whitespace by default

```cpp
int a = 42;
double b = 3.14;
string c = "Hello";

// Output chaining
cout << "Values: " << a << ", " << b << ", " << c << endl;

// Input chaining
cin >> a >> b >> c;
```

---

## Operator Overloading for Custom Types

Define << and >> operators for user-defined types:

```cpp
class Point {
    int x, y;
public:
    Point(int x = 0, int y = 0) : x(x), y(y) {}

    friend ostream& operator<<(ostream& os, const Point& p) {
        return os << "(" << p.x << ", " << p.y << ")";
    }

    friend istream& operator>>(istream& is, Point& p) {
        char dummy;
        return is >> dummy >> p.x >> dummy >> p.y >> dummy;
    }
};

Point p(3, 4);
cout << "Point: " << p << endl;  // Output: Point: (3, 4)
```

---

## Standard Input/Output Functions

Alternative I/O functions for specific needs:
- `get()`: read single character or line
- `getline()`: read entire line including spaces
- `put()`: write single character
- `read()/write()`: binary I/O operations

```cpp
char ch;
string line;

// Read single character
cin.get(ch);

// Read entire line
getline(cin, line);

// Write single character
cout.put('A');
```

---

## Manipulators Overview

Manipulators modify stream behavior:
- **Parameterless**: `endl`, `flush`, `ws`
- **Parameterized**: `setw()`, `setprecision()`, `setfill()`
- **State-changing**: `hex`, `oct`, `dec`, `fixed`, `scientific`

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    double pi = 3.14159265;
    cout << fixed << setprecision(3) << pi << endl;  // 3.142
    cout << scientific << pi << endl;                // 3.142e+00
    return 0;
}
```

---

## Formatting Numbers

Control numeric output format:

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    int num = 255;
    double val = 123.456789;

    // Different number bases
    cout << "Decimal: " << dec << num << endl;      // 255
    cout << "Hexadecimal: " << hex << num << endl;  // ff
    cout << "Octal: " << oct << num << endl;        // 377

    // Floating-point formatting
    cout << fixed << setprecision(2) << val << endl;     // 123.46
    cout << scientific << setprecision(3) << val << endl; // 1.235e+02

    return 0;
}
```

---

## Field Width and Alignment

Control output field width and alignment:

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    cout << setw(10) << "Name" << setw(10) << "Age" << endl;
    cout << setw(10) << "John" << setw(10) << 25 << endl;
    cout << setw(10) << "Alice" << setw(10) << 30 << endl;

    // With fill character
    cout << setfill('*') << setw(15) << "Padded" << endl;

    // Left alignment
    cout << left << setw(10) << "Left" << endl;
    cout << right << setw(10) << "Right" << endl;

    return 0;
}
```

---

## Boolean and Character Formatting

Special formatting for booleans and characters:

```cpp
#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    bool flag = true;
    char ch = 'A';

    // Boolean formatting
    cout << boolalpha << flag << endl;    // true
    cout << noboolalpha << flag << endl;  // 1

    // Character as number
    cout << static_cast<int>(ch) << endl; // 65

    // Show positive sign
    cout << showpos << 42 << endl;        // +42
    cout << noshowpos << 42 << endl;      // 42

    return 0;
}
```

---

## Internationalization Support

C++ streams support locale-specific formatting:

```cpp
#include <iostream>
#include <locale>
#include <iomanip>
using namespace std;

int main() {
    // Set German locale
    locale german("de_DE");
    cout.imbue(german);

    double money = 1234.56;
    cout << "Price: " << fixed << setprecision(2)
         << money << endl;

    // Thousands separator
    cout.imbue(locale(""));  // System default
    cout << "Number: " << 1234567 << endl;

    return 0;
}
```

---

## File Access Basics

File streams provide file I/O capabilities:
- `ifstream`: input file stream
- `ofstream`: output file stream
- `fstream`: bidirectional file stream

```cpp
#include <fstream>
#include <iostream>
using namespace std;

int main() {
    // Output to file
    ofstream outFile("data.txt");
    outFile << "Hello, File!" << endl;
    outFile.close();

    // Input from file
    ifstream inFile("data.txt");
    string line;
    while (getline(inFile, line)) {
        cout << line << endl;
    }
    inFile.close();

    return 0;
}
```

---

## File Opening Modes

Specify how files should be opened:

```cpp
#include <fstream>
using namespace std;

int main() {
    // Different opening modes
    ofstream file1("output.txt", ios::out);           // Write (default)
    ofstream file2("append.txt", ios::app);           // Append
    ofstream file3("binary.dat", ios::binary);        // Binary mode
    ifstream file4("input.txt", ios::in);             // Read (default)

    // Combined modes
    fstream file5("data.txt", ios::in | ios::out);    // Read/Write
    fstream file6("temp.tmp", ios::trunc);            // Truncate

    // Always check if file opened successfully
    if (file1.is_open()) {
        file1 << "Data written successfully" << endl;
        file1.close();
    }

    return 0;
}
```

---

## File Position Control

Control read/write position in files:

```cpp
#include <fstream>
#include <iostream>
using namespace std;

int main() {
    fstream file("positions.txt", ios::in | ios::out | ios::trunc);

    // Write some data
    file << "0123456789" << endl;

    // Get current position
    streampos writePos = file.tellp();
    cout << "Write position: " << writePos << endl;

    // Move to beginning for reading
    file.seekg(0, ios::beg);

    // Read and display position
    char ch;
    while (file.get(ch)) {
        cout << "Read '" << ch << "' at position " << file.tellg() << endl;
    }

    file.close();
    return 0;
}
```

---

## Binary File Operations

Reading and writing binary data:

```cpp
#include <fstream>
#include <iostream>
using namespace std;

struct Record {
    int id;
    char name[20];
    double salary;
};

int main() {
    Record emp = {101, "John Doe", 50000.0};

    // Write binary data
    ofstream binOut("employee.dat", ios::binary);
    binOut.write(reinterpret_cast<char*>(&emp), sizeof(Record));
    binOut.close();

    // Read binary data
    Record readEmp;
    ifstream binIn("employee.dat", ios::binary);
    binIn.read(reinterpret_cast<char*>(&readEmp), sizeof(Record));
    binIn.close();

    cout << "ID: " << readEmp.id << ", Name: " << readEmp.name
         << ", Salary: " << readEmp.salary << endl;

    return 0;
}
```

---

## Connecting Input and Output Streams

Tie streams together for synchronized I/O:

```cpp
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    // cout is tied to cin by default
    cout << "Enter your name: ";  // Automatically flushed
    string name;
    cin >> name;

    // Manual tying
    ofstream logFile("log.txt");
    cin.tie(&logFile);  // Tie cin to log file

    // Untie streams
    cin.tie(nullptr);

    // Check current tie
    ostream* tied = cin.tie();
    if (tied) {
        cout << "cin is tied to a stream" << endl;
    }

    return 0;
}
```

---

## Stream Classes for Strings

String streams allow in-memory string manipulation:
- `istringstream`: read from string
- `ostringstream`: write to string
- `stringstream`: bidirectional string I/O

```cpp
#include <sstream>
#include <iostream>
using namespace std;

int main() {
    // Writing to string
    ostringstream oss;
    oss << "Value: " << 42 << ", PI: " << 3.14;
    string result = oss.str();
    cout << result << endl;

    // Reading from string
    istringstream iss("10 20 30");
    int a, b, c;
    iss >> a >> b >> c;
    cout << "Numbers: " << a << ", " << b << ", " << c << endl;

    return 0;
}
```

---

## String Parsing with String Streams

Powerful parsing capabilities:

```cpp
#include <sstream>
#include <iostream>
#include <vector>
using namespace std;

vector<int> parseNumbers(const string& input) {
    vector<int> numbers;
    istringstream iss(input);
    int num;

    while (iss >> num) {
        numbers.push_back(num);
    }

    return numbers;
}

int main() {
    string data = "1 2 3 4 5 6 7 8 9 10";
    vector<int> nums = parseNumbers(data);

    cout << "Parsed numbers: ";
    for (int n : nums) {
        cout << n << " ";
    }
    cout << endl;

    return 0;
}
```

---

## CSV Parsing Example

Using string streams for CSV data:

```cpp
#include <sstream>
#include <iostream>
#include <vector>
using namespace std;

vector<string> splitCSV(const string& line) {
    vector<string> fields;
    istringstream ss(line);
    string field;

    while (getline(ss, field, ',')) {
        fields.push_back(field);
    }

    return fields;
}

int main() {
    string csvLine = "John,Doe,30,Engineer";
    vector<string> fields = splitCSV(csvLine);

    cout << "CSV Fields:" << endl;
    for (size_t i = 0; i < fields.size(); ++i) {
        cout << "[" << i << "]: " << fields[i] << endl;
    }

    return 0;
}
```

---

## Input/Output Operators for User-Defined Types

Best practices for custom I/O operators:

```cpp
class Complex {
    double real, imag;
public:
    Complex(double r = 0, double i = 0) : real(r), imag(i) {}

    // Output operator
    friend ostream& operator<<(ostream& os, const Complex& c) {
        os << c.real;
        if (c.imag >= 0) os << "+";
        os << c.imag << "i";
        return os;
    }

    // Input operator with error handling
    friend istream& operator>>(istream& is, Complex& c) {
        char plus, i;
        if (!(is >> c.real >> plus >> c.imag >> i)) {
            is.setstate(ios::failbit);
        }
        return is;
    }
};
```

---

## Stream Buffer Classes Overview

Stream buffers manage the actual I/O operations:
- `streambuf`: abstract base class
- `filebuf`: file buffer
- `stringbuf`: string buffer
- Custom buffer classes possible

![stream_buffer_classes_overview](/svg/courses/embedded/effective-real-time-embedded-c-and-c++/18_streams/stream_buffer_classes_overview.svg)

---

## Custom Stream Buffer Example

Creating a custom buffer for logging:

```cpp
#include <iostream>
#include <streambuf>
#include <fstream>
using namespace std;

class LogBuffer : public streambuf {
    ofstream logFile;

protected:
    virtual int overflow(int c) override {
        if (c != EOF) {
            // Write to both console and file
            cout.put(c);
            logFile.put(c);
        }
        return c;
    }

public:
    LogBuffer(const string& filename) : logFile(filename) {}
    ~LogBuffer() { logFile.close(); }
};

int main() {
    LogBuffer logBuf("output.log");
    ostream logStream(&logBuf);

    logStream << "This goes to both console and file!" << endl;

    return 0;
}
```

---

## Performance Considerations - Buffering

Understanding stream buffering for optimal performance:

```cpp
#include <iostream>
#include <fstream>
#include <chrono>
using namespace std;

void testBuffering() {
    auto start = chrono::high_resolution_clock::now();

    ofstream file("test.txt");

    // This is slow - flushes after each write
    for (int i = 0; i < 10000; ++i) {
        file << i << endl;  // endl flushes
    }

    auto mid = chrono::high_resolution_clock::now();

    // This is faster - no automatic flushing
    for (int i = 0; i < 10000; ++i) {
        file << i << '\n';  // Just newline, no flush
    }
    file.flush();  // Manual flush at end

    auto end = chrono::high_resolution_clock::now();

    cout << "With endl: " << chrono::duration_cast<chrono::milliseconds>(mid - start).count() << "ms" << endl;
    cout << "With \\n: " << chrono::duration_cast<chrono::milliseconds>(end - mid).count() << "ms" << endl;
}
```

---

## Performance - Binary vs Text I/O

Binary I/O is typically faster for structured data:

```cpp
#include <fstream>
#include <vector>
#include <chrono>
using namespace std;

void comparePerformance() {
    vector<int> data(100000);
    for (size_t i = 0; i < data.size(); ++i) {
        data[i] = i;
    }

    auto start = chrono::high_resolution_clock::now();

    // Text output
    ofstream textFile("data.txt");
    for (int val : data) {
        textFile << val << '\n';
    }
    textFile.close();

    auto mid = chrono::high_resolution_clock::now();

    // Binary output
    ofstream binFile("data.bin", ios::binary);
    binFile.write(reinterpret_cast<const char*>(data.data()),
                  data.size() * sizeof(int));
    binFile.close();

    auto end = chrono::high_resolution_clock::now();

    cout << "Text I/O: " << chrono::duration_cast<chrono::milliseconds>(mid - start).count() << "ms" << endl;
    cout << "Binary I/O: " << chrono::duration_cast<chrono::milliseconds>(end - mid).count() << "ms" << endl;
}
```

---

## Memory-Mapped Files Alternative

For large files, consider memory-mapped I/O:

```cpp
#include <iostream>
#include <fstream>
#include <memory>
using namespace std;

class MemoryMappedFile {
    char* data;
    size_t size;

public:
    MemoryMappedFile(const string& filename) {
        ifstream file(filename, ios::binary | ios::ate);
        size = file.tellg();
        file.seekg(0);

        data = new char[size];
        file.read(data, size);
    }

    ~MemoryMappedFile() {
        delete[] data;
    }

    const char* getData() const { return data; }
    size_t getSize() const { return size; }

    // Fast access to specific positions
    char operator[](size_t pos) const {
        return (pos < size) ? data[pos] : '\0';
    }
};
```

---

## Stream Synchronization Issues

Be aware of synchronization with C stdio:

```cpp
#include <iostream>
#include <cstdio>
using namespace std;

int main() {
    // By default, C++ streams are synchronized with C stdio
    cout << "C++ output" << endl;
    printf("C output\n");

    // Disable synchronization for better performance
    ios_base::sync_with_stdio(false);

    // WARNING: Don't mix C and C++ I/O after this!
    cout << "Fast C++ output" << endl;
    // printf("Don't do this!"); // Undefined behavior

    return 0;
}
```

---

## Thread Safety Considerations

Stream I/O is generally not thread-safe:

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <vector>
using namespace std;

mutex cout_mutex;

void threadSafeOutput(int id) {
    for (int i = 0; i < 5; ++i) {
        {
            lock_guard<mutex> lock(cout_mutex);
            cout << "Thread " << id << ": " << i << endl;
        }
        // Do other work without holding the lock
    }
}

int main() {
    vector<thread> threads;

    for (int i = 0; i < 3; ++i) {
        threads.emplace_back(threadSafeOutput, i);
    }

    for (auto& t : threads) {
        t.join();
    }

    return 0;
}
```

---

## Error Recovery Strategies

Robust error handling techniques:

```cpp
#include <iostream>
#include <fstream>
#include <limits>
using namespace std;

void robustInput() {
    int number;

    while (true) {
        cout << "Enter a number: ";

        if (cin >> number) {
            cout << "You entered: " << number << endl;
            break;
        } else {
            cout << "Invalid input. Please try again." << endl;

            // Clear error flags
            cin.clear();

            // Skip invalid input
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }
    }
}

bool safeFileOperation(const string& filename) {
    ifstream file(filename);

    if (!file.is_open()) {
        cerr << "Cannot open file: " << filename << endl;
        return false;
    }

    string line;
    while (getline(file, line)) {
        if (file.bad()) {
            cerr << "I/O error occurred" << endl;
            return false;
        }

        // Process line
        cout << line << endl;
    }

    return true;
}
```

---

## RAII for Stream Management

Use RAII principles for automatic resource management:

```cpp
#include <fstream>
#include <iostream>
#include <memory>
using namespace std;

class FileManager {
    unique_ptr<ofstream> file;

public:
    FileManager(const string& filename)
        : file(make_unique<ofstream>(filename)) {
        if (!file->is_open()) {
            throw runtime_error("Cannot open file: " + filename);
        }
    }
    void write(const string& data) {
        if (file && file->is_open()) {
            *file << data << endl;
            if (file->fail()) {
                throw runtime_error("Write operation failed");
            }
        }
    }
    // Destructor automatically closes file
    ~FileManager() = default;  // unique_ptr handles cleanup
};

int main() {
    try {
        FileManager fm("output.txt");
        fm.write("RAII ensures proper cleanup");
        fm.write("Even if exceptions occur");
        // File automatically closed when fm goes out of scope
    } catch (const exception& e) {
        cerr << "Error: " << e.what() << endl;
    }
    return 0;
}
