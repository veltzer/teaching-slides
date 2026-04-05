# Observer Pattern

---

## Intent

- Define a one-to-many dependency between objects
- When one object changes state, all its dependents are notified automatically
- Promote loose coupling between the subject and its observers

---

## Problem: Tight Coupling to State Changes

```cpp
// Without Observer — tightly coupled notifications
class Store {
    int inventory;
public:
    void setInventory(int count) {
        inventory = count;
        // Must know about every dependent object
        display.update(inventory);
        logger.log(inventory);
        alertSystem.check(inventory);
        // Adding a new listener means modifying Store
    }
};
```

---

## Observer Structure

<svg width="550" height="230" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="20" width="180" height="70" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="120" y="45" text-anchor="middle" font-size="13" font-weight="bold">Subject</text>
  <text x="120" y="63" text-anchor="middle" font-size="10">+ attach(Observer)</text>
  <text x="120" y="78" text-anchor="middle" font-size="10">+ notify()</text>

  <rect x="320" y="20" width="180" height="60" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="410" y="45" text-anchor="middle" font-size="13" font-weight="bold">Observer</text>
  <text x="410" y="65" text-anchor="middle" font-size="11" font-style="italic">+ update()</text>

  <line x1="210" y1="50" x2="320" y2="50" stroke="#333" stroke-width="1.5" marker-end="url(#obArr)"/>
  <text x="265" y="42" text-anchor="middle" font-size="9">notifies</text>

  <rect x="280" y="140" width="130" height="40" fill="#f1f8e9" stroke="#689f38" stroke-width="2"/>
  <text x="345" y="165" text-anchor="middle" font-size="11">ObserverA</text>

  <rect x="430" y="140" width="130" height="40" fill="#f1f8e9" stroke="#689f38" stroke-width="2"/>
  <text x="495" y="165" text-anchor="middle" font-size="11">ObserverB</text>

  <line x1="345" y1="140" x2="390" y2="80" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>
  <line x1="495" y1="140" x2="430" y2="80" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5"/>

  <defs>
    <marker id="obArr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Observer Interface

```cpp
template<typename... Args>
class Observer {
public:
    virtual void update(Args... args) = 0;
    virtual ~Observer() = default;
};

template<typename... Args>
class Subject {
    std::vector<Observer<Args...>*> observers;

public:
    void attach(Observer<Args...>* observer) {
        observers.push_back(observer);
    }

    void detach(Observer<Args...>* observer) {
        observers.erase(
            std::remove(observers.begin(), observers.end(), observer),
            observers.end());
    }

protected:
    void notify(Args... args) {
        for (auto* observer : observers) {
            observer->update(args...);
        }
    }
};
```

---

## Concrete Subject and Observers

```cpp
class WeatherStation : public Subject<float, float, float> {
    float temperature = 0;
    float humidity = 0;
    float pressure = 0;

public:
    void setMeasurements(float temp, float hum, float pres) {
        temperature = temp;
        humidity = hum;
        pressure = pres;
        notify(temperature, humidity, pressure);
    }
};

class DisplayBoard : public Observer<float, float, float> {
public:
    void update(float temp, float humidity, float pressure) override {
        std::cout << "Display: " << temp << "°C, "
                  << humidity << "% humidity, "
                  << pressure << " hPa\n";
    }
};

class AlertSystem : public Observer<float, float, float> {
public:
    void update(float temp, float humidity, float pressure) override {
        if (temp > 40.0f) {
            std::cout << "ALERT: High temperature! " << temp << "°C\n";
        }
    }
};
```

---

## Observer Usage

```cpp
WeatherStation station;
DisplayBoard display;
AlertSystem alerts;

station.attach(&display);
station.attach(&alerts);

station.setMeasurements(25.0f, 60.0f, 1013.0f);
// Display: 25°C, 60% humidity, 1013 hPa

station.setMeasurements(42.0f, 80.0f, 1008.0f);
// Display: 42°C, 80% humidity, 1008 hPa
// ALERT: High temperature! 42°C

station.detach(&alerts);
station.setMeasurements(45.0f, 85.0f, 1005.0f);
// Display: 45°C, 85% humidity, 1005 hPa
// (no alert — detached)
```

---

## Modern C++ Observer with std::function

```cpp
class EventEmitter {
    using Callback = std::function<void(const std::string&)>;
    std::unordered_map<std::string, std::vector<Callback>> listeners;

public:
    void on(const std::string& event, Callback callback) {
        listeners[event].push_back(std::move(callback));
    }

    void emit(const std::string& event, const std::string& data) {
        auto it = listeners.find(event);
        if (it != listeners.end()) {
            for (auto& cb : it->second) {
                cb(data);
            }
        }
    }
};

// Usage
EventEmitter emitter;
emitter.on("click", [](const std::string& data) {
    std::cout << "Button clicked: " << data << "\n";
});
emitter.on("click", [](const std::string& data) {
    std::cout << "Logging click: " << data << "\n";
});
emitter.emit("click", "submit-button");
```

---

## Thread-Safe Observer

```cpp
template<typename... Args>
class ThreadSafeSubject {
    std::vector<std::function<void(Args...)>> observers;
    mutable std::shared_mutex mtx;

public:
    size_t subscribe(std::function<void(Args...)> callback) {
        std::unique_lock lock(mtx);
        observers.push_back(std::move(callback));
        return observers.size() - 1;
    }

    void notify(Args... args) {
        std::shared_lock lock(mtx);
        for (auto& observer : observers) {
            observer(args...);
        }
    }
};
```

---

## When to Use Observer

**Use when:**

- A change to one object requires changing others, and you do not know how many objects need to change
- An object should notify other objects without making assumptions about who those objects are
- You need a publish-subscribe mechanism

**Watch out for:**

- Memory leaks from forgotten subscriptions (use RAII for unsubscription)
- Update order dependencies
- Performance with many observers
- Cascading updates (observer triggers another notification)
