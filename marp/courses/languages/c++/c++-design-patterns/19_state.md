# State Pattern

---

## Intent

- Allow an object to alter its behavior when its internal state changes
- The object will appear to change its class
- Encapsulate state-specific behavior into separate state objects

---

## Problem: State-Dependent Conditionals

```cpp
class Document {
    enum State { Draft, Review, Published };
    State state = Draft;

public:
    void publish() {
        if (state == Draft) {
            state = Review;
        } else if (state == Review) {
            state = Published;
        } else if (state == Published) {
            // Already published — do nothing
        }
    }

    void render() {
        if (state == Draft) { /* render as editable */ }
        else if (state == Review) { /* render as read-only with comments */ }
        else if (state == Published) { /* render as final */ }
    }
    // Every method has these same conditionals
};
```

---

## State Pattern Structure

![state_pattern_structure](svg/courses/languages/c++/c++-design-patterns/19_state/state_pattern_structure.svg)

---

## State Interface and Concrete States

```cpp
class Document;  // Forward declaration

class DocumentState {
public:
    virtual ~DocumentState() = default;
    virtual void publish(Document& doc) = 0;
    virtual void edit(Document& doc, const std::string& content) = 0;
    virtual std::string render(const Document& doc) const = 0;
};

class DraftState : public DocumentState {
public:
    void publish(Document& doc) override;
    void edit(Document& doc, const std::string& content) override {
        doc.setContent(content);
        std::cout << "Editing draft\n";
    }
    std::string render(const Document& doc) const override {
        return "[DRAFT] " + doc.getContent();
    }
};

class ReviewState : public DocumentState {
public:
    void publish(Document& doc) override;
    void edit(Document& doc, const std::string& content) override {
        std::cout << "Cannot edit during review\n";
    }
    std::string render(const Document& doc) const override {
        return "[IN REVIEW] " + doc.getContent();
    }
};

class PublishedState : public DocumentState {
public:
    void publish(Document& doc) override {
        std::cout << "Already published\n";
    }
    void edit(Document& doc, const std::string& content) override {
        std::cout << "Cannot edit published document\n";
    }
    std::string render(const Document& doc) const override {
        return doc.getContent();
    }
};
```

---

## Context Class

```cpp
class Document {
    std::unique_ptr<DocumentState> state;
    std::string content;

public:
    Document() : state(std::make_unique<DraftState>()) {}

    void setState(std::unique_ptr<DocumentState> newState) {
        state = std::move(newState);
    }

    void publish() { state->publish(*this); }
    void edit(const std::string& text) { state->edit(*this, text); }
    std::string render() const { return state->render(*this); }

    void setContent(const std::string& c) { content = c; }
    const std::string& getContent() const { return content; }
};

// State transitions
void DraftState::publish(Document& doc) {
    std::cout << "Sending for review\n";
    doc.setState(std::make_unique<ReviewState>());
}

void ReviewState::publish(Document& doc) {
    std::cout << "Publishing document\n";
    doc.setState(std::make_unique<PublishedState>());
}
```

---

## State Pattern Usage

```cpp
Document doc;
doc.edit("Hello World");
std::cout << doc.render() << "\n";  // [DRAFT] Hello World

doc.publish();                       // Sending for review
doc.edit("Try to edit");             // Cannot edit during review
std::cout << doc.render() << "\n";  // [IN REVIEW] Hello World

doc.publish();                       // Publishing document
doc.edit("Try again");               // Cannot edit published document
std::cout << doc.render() << "\n";  // Hello World
```

---

## State vs Strategy

| Aspect | State | Strategy |
|--------|-------|----------|
| Purpose | Behavior varies by state | Algorithm selection |
| Transitions | States know about each other | Strategies are independent |
| Who decides | State objects trigger transitions | Client selects strategy |
| Awareness | States know successor states | Strategies are unaware of each other |

---

## When to Use State

**Use when:**

- An object's behavior depends on its state and must change at runtime
- Operations have large multipart conditionals depending on state
- State transitions are complex and need to be made explicit
- You want to avoid duplicating state-checking code across methods
