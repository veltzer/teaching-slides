# Proxy Pattern

---

## Intent

- Provide a surrogate or placeholder for another object
- Control access to the original object
- Add a level of indirection for various purposes

---

## Proxy Structure

![proxy_structure](/svg/courses/languages/c++/c++-design-patterns/13_proxy/proxy_structure.svg)

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
