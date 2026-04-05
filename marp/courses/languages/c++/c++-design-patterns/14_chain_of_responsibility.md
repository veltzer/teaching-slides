# Chain of Responsibility Pattern

---

## Intent

- Avoid coupling the sender of a request to its receiver
- Give more than one object a chance to handle the request
- Chain the receiving objects and pass the request along the chain until one handles it

---

## Problem: Rigid Request Handling

```cpp
// Tightly coupled — every handler must know about every request type
void handleRequest(Request& req) {
    if (req.type == "authentication") {
        authenticateUser(req);
    } else if (req.type == "authorization") {
        checkPermissions(req);
    } else if (req.type == "validation") {
        validateData(req);
    } else if (req.type == "logging") {
        logRequest(req);
    }
    // Adding new handlers means modifying this function
}
```

---

## Chain of Responsibility Structure

<svg width="600" height="150" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="50" width="120" height="50" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="70" y="80" text-anchor="middle" font-size="11">Handler A</text>

  <rect x="170" y="50" width="120" height="50" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="230" y="80" text-anchor="middle" font-size="11">Handler B</text>

  <rect x="330" y="50" width="120" height="50" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="390" y="80" text-anchor="middle" font-size="11">Handler C</text>

  <rect x="490" y="50" width="100" height="50" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="540" y="80" text-anchor="middle" font-size="11">Default</text>

  <line x1="130" y1="75" x2="170" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="290" y1="75" x2="330" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arr)"/>
  <line x1="450" y1="75" x2="490" y2="75" stroke="#333" stroke-width="2" marker-end="url(#arr)"/>

  <text x="300" y="30" text-anchor="middle" font-size="12">Request passes along the chain</text>

  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

Each handler decides whether to process the request or pass it to the next handler

---

## Handler Base Class

```cpp
class SupportHandler {
protected:
    std::unique_ptr<SupportHandler> next;

public:
    virtual ~SupportHandler() = default;

    SupportHandler& setNext(std::unique_ptr<SupportHandler> handler) {
        next = std::move(handler);
        return *next;
    }

    virtual void handle(const SupportTicket& ticket) {
        if (next) {
            next->handle(ticket);
        } else {
            std::cout << "No handler could process ticket: "
                      << ticket.description << "\n";
        }
    }
};
```

---

## Concrete Handlers

```cpp
class BasicSupport : public SupportHandler {
public:
    void handle(const SupportTicket& ticket) override {
        if (ticket.severity == Severity::Low) {
            std::cout << "Basic Support: Resolved - "
                      << ticket.description << "\n";
        } else {
            SupportHandler::handle(ticket);  // Pass to next
        }
    }
};

class TechnicalSupport : public SupportHandler {
public:
    void handle(const SupportTicket& ticket) override {
        if (ticket.severity == Severity::Medium) {
            std::cout << "Technical Support: Resolved - "
                      << ticket.description << "\n";
        } else {
            SupportHandler::handle(ticket);
        }
    }
};

class ManagerSupport : public SupportHandler {
public:
    void handle(const SupportTicket& ticket) override {
        std::cout << "Manager: Handling escalated ticket - "
                  << ticket.description << "\n";
    }
};
```

---

## Chain Assembly and Usage

```cpp
auto basic = std::make_unique<BasicSupport>();
auto tech = std::make_unique<TechnicalSupport>();
auto manager = std::make_unique<ManagerSupport>();

basic->setNext(std::move(tech))
     .setNext(std::move(manager));

SupportTicket t1{"Password reset", Severity::Low};
SupportTicket t2{"Server crash", Severity::Medium};
SupportTicket t3{"Data breach", Severity::High};

basic->handle(t1);  // Basic Support: Resolved
basic->handle(t2);  // Technical Support: Resolved
basic->handle(t3);  // Manager: Handling escalated ticket
```

---

## Middleware Chain Example

```cpp
class Middleware {
    std::unique_ptr<Middleware> next;

public:
    virtual ~Middleware() = default;

    Middleware& linkWith(std::unique_ptr<Middleware> n) {
        next = std::move(n);
        return *next;
    }

    virtual bool check(const Request& req) {
        return next ? next->check(req) : true;
    }
};

class AuthMiddleware : public Middleware {
public:
    bool check(const Request& req) override {
        if (!req.hasValidToken()) {
            std::cout << "Auth failed\n";
            return false;
        }
        return Middleware::check(req);
    }
};

class RateLimitMiddleware : public Middleware {
    int maxRequests;
    std::unordered_map<std::string, int> counts;
public:
    explicit RateLimitMiddleware(int max) : maxRequests(max) {}

    bool check(const Request& req) override {
        if (++counts[req.ip] > maxRequests) {
            std::cout << "Rate limit exceeded\n";
            return false;
        }
        return Middleware::check(req);
    }
};
```

---

## When to Use Chain of Responsibility

**Use when:**

- More than one object may handle a request, and the handler is not known in advance
- You want to issue a request to one of several objects without specifying the receiver explicitly
- The set of handlers should be specified dynamically

**Common examples:**

- Event handling systems
- Middleware pipelines (logging, auth, validation)
- Exception handling chains
- GUI event bubbling
