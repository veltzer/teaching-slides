# Proxy Pattern

---

## Intent

- Provide a surrogate or placeholder for another object
- Control access to the original object
- Add a level of indirection for various purposes

---

## Proxy Structure

<svg width="550" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="60" width="120" height="50" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="80" y="90" text-anchor="middle" font-size="12">Client</text>

  <rect x="190" y="20" width="150" height="60" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="265" y="45" text-anchor="middle" font-size="13" font-weight="bold">Subject</text>
  <text x="265" y="65" text-anchor="middle" font-size="11" font-style="italic">+ request()</text>

  <rect x="120" y="130" width="130" height="50" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="185" y="150" text-anchor="middle" font-size="12">Proxy</text>
  <text x="185" y="168" text-anchor="middle" font-size="10">+ request()</text>

  <rect x="310" y="130" width="150" height="50" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="385" y="150" text-anchor="middle" font-size="12">RealSubject</text>
  <text x="385" y="168" text-anchor="middle" font-size="10">+ request()</text>

  <line x1="140" y1="85" x2="190" y2="55" stroke="#333" stroke-width="1.5" marker-end="url(#pxArr)"/>
  <line x1="185" y1="130" x2="240" y2="80" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="385" y1="130" x2="290" y2="80" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="250" y1="155" x2="310" y2="155" stroke="#333" stroke-width="1.5" marker-end="url(#pxArr)"/>
  <text x="280" y="148" font-size="9">delegates</text>

  <defs>
    <marker id="pxArr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Types of Proxies

1. **Virtual Proxy**: Delays creation of expensive objects until needed
1. **Protection Proxy**: Controls access based on permissions
1. **Remote Proxy**: Represents an object in a different address space
1. **Logging Proxy**: Adds logging to method calls
1. **Caching Proxy**: Caches results of expensive operations

---

## Virtual Proxy (Lazy Loading)

```cpp
class Image {
public:
    virtual void display() = 0;
    virtual int getWidth() const = 0;
    virtual int getHeight() const = 0;
    virtual ~Image() = default;
};

class HighResImage : public Image {
    std::string filename;
    std::vector<uint8_t> pixels;  // Expensive to load

public:
    explicit HighResImage(const std::string& file) : filename(file) {
        // Simulate expensive loading
        std::cout << "Loading " << filename << " from disk...\n";
        pixels.resize(1024 * 1024 * 4);  // 4 MB
    }

    void display() override {
        std::cout << "Displaying " << filename << "\n";
    }
    int getWidth() const override { return 1024; }
    int getHeight() const override { return 1024; }
};
```

---

## Virtual Proxy Implementation

```cpp
class ImageProxy : public Image {
    std::string filename;
    mutable std::unique_ptr<HighResImage> realImage;

    void loadIfNeeded() const {
        if (!realImage) {
            realImage = std::make_unique<HighResImage>(filename);
        }
    }

public:
    explicit ImageProxy(const std::string& file) : filename(file) {
        // No loading — just store the filename
    }

    void display() override {
        loadIfNeeded();
        realImage->display();
    }

    int getWidth() const override {
        loadIfNeeded();
        return realImage->getWidth();
    }

    int getHeight() const override {
        loadIfNeeded();
        return realImage->getHeight();
    }
};

// Create 1000 proxies — no disk I/O until display() is called
std::vector<std::unique_ptr<Image>> gallery;
for (const auto& file : imageFiles) {
    gallery.push_back(std::make_unique<ImageProxy>(file));
}
```

---

## Protection Proxy

```cpp
class Document {
public:
    virtual void read() = 0;
    virtual void write(const std::string& content) = 0;
    virtual ~Document() = default;
};

class SecureDocumentProxy : public Document {
    std::unique_ptr<Document> realDocument;
    std::string currentUser;
    std::unordered_set<std::string> writers;

public:
    SecureDocumentProxy(std::unique_ptr<Document> doc,
                        const std::string& user,
                        std::unordered_set<std::string> authorizedWriters)
        : realDocument(std::move(doc)),
          currentUser(user),
          writers(std::move(authorizedWriters)) {}

    void read() override {
        realDocument->read();  // Everyone can read
    }

    void write(const std::string& content) override {
        if (writers.count(currentUser) == 0) {
            throw std::runtime_error("Access denied: " + currentUser);
        }
        realDocument->write(content);
    }
};
```

---

## Caching Proxy

```cpp
class WeatherService {
public:
    virtual std::string getForecast(const std::string& city) = 0;
    virtual ~WeatherService() = default;
};

class CachingWeatherProxy : public WeatherService {
    std::unique_ptr<WeatherService> realService;
    std::unordered_map<std::string, std::string> cache;
    std::unordered_map<std::string, std::chrono::steady_clock::time_point> timestamps;
    std::chrono::seconds ttl;

public:
    CachingWeatherProxy(std::unique_ptr<WeatherService> svc,
                        std::chrono::seconds cacheTTL)
        : realService(std::move(svc)), ttl(cacheTTL) {}

    std::string getForecast(const std::string& city) override {
        auto now = std::chrono::steady_clock::now();
        auto it = cache.find(city);
        if (it != cache.end() && (now - timestamps[city]) < ttl) {
            return it->second;  // Return cached result
        }
        auto result = realService->getForecast(city);
        cache[city] = result;
        timestamps[city] = now;
        return result;
    }
};
```

---

## Proxy vs Decorator vs Adapter

| Pattern | Purpose | Interface |
|---------|---------|-----------|
| Proxy | Controls access | Same as subject |
| Decorator | Adds behavior | Same as component |
| Adapter | Converts interface | Different from adaptee |

- **Proxy** manages the lifecycle or access to the real object
- **Decorator** adds new responsibilities
- **Adapter** translates between interfaces

---

## When to Use Proxy

**Use when:**

- Lazy initialization is needed (virtual proxy)
- Access control is required (protection proxy)
- Remote object access needs local representation (remote proxy)
- Caching of expensive operations is beneficial (caching proxy)
- Logging or auditing of method calls is required (logging proxy)

**C++ specific**: `std::shared_ptr` and `std::unique_ptr` are a form of smart reference proxy that manages object lifetime
