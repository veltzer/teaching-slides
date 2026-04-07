# Mediator Pattern

---

## Intent

- Define an object that encapsulates how a set of objects interact
- Promote loose coupling by keeping objects from referring to each other explicitly
- Centralize complex communication and control logic

---

## Problem: Many-to-Many Dependencies

```cpp
// Without Mediator — every component knows about every other
class TextBox {
    Button& submitBtn;
    Checkbox& agreeBox;
    Label& statusLabel;
public:
    void onChange() {
        submitBtn.setEnabled(!text.empty() && agreeBox.isChecked());
        statusLabel.setText("Modified");
    }
};
// Every new component must update all related components
```

---

## Mediator Structure

![mediator_structure](svg/courses/languages/c++/c++-design-patterns/22_mediator/mediator_structure.svg)

---

## Mediator Interface

```cpp
class Component;

class DialogMediator {
public:
    virtual void notify(Component* sender,
                        const std::string& event) = 0;
    virtual ~DialogMediator() = default;
};
```

---

## Components

```cpp
class Component {
protected:
    DialogMediator* mediator;
public:
    explicit Component(DialogMediator* m = nullptr) : mediator(m) {}
    void setMediator(DialogMediator* m) { mediator = m; }
    virtual ~Component() = default;
};

class TextBox : public Component {
    std::string text;
public:
    using Component::Component;
    void setText(const std::string& t) {
        text = t;
        if (mediator) mediator->notify(this, "textChanged");
    }
    const std::string& getText() const { return text; }
};

class Button : public Component {
    bool enabled = true;
public:
    using Component::Component;
    void click() {
        if (enabled && mediator) mediator->notify(this, "click");
    }
    void setEnabled(bool e) { enabled = e; }
    bool isEnabled() const { return enabled; }
};

class Checkbox : public Component {
    bool checked = false;
public:
    using Component::Component;
    void toggle() {
        checked = !checked;
        if (mediator) mediator->notify(this, "toggled");
    }
    bool isChecked() const { return checked; }
};
```

---

## Concrete Mediator

```cpp
class RegistrationDialog : public DialogMediator {
    TextBox username;
    TextBox password;
    Checkbox agreeTerms;
    Button submitBtn;

public:
    RegistrationDialog() {
        username.setMediator(this);
        password.setMediator(this);
        agreeTerms.setMediator(this);
        submitBtn.setMediator(this);
    }

    void notify(Component* sender, const std::string& event) override {
        if (event == "textChanged" || event == "toggled") {
            bool valid = !username.getText().empty()
                      && !password.getText().empty()
                      && agreeTerms.isChecked();
            submitBtn.setEnabled(valid);
        }
        else if (sender == &submitBtn && event == "click") {
            std::cout << "Submitting registration for: "
                      << username.getText() << "\n";
        }
    }
};
```

All interaction logic lives in one place

---

## When to Use Mediator

**Use when:**

- A set of objects communicate in complex but well-defined ways
- Reusing an object is difficult because it refers to many other objects
- Behavior distributed between many classes should be customizable without subclassing

**Mediator vs Observer:**

- **Observer** is one-to-many, unidirectional
- **Mediator** is many-to-many, bidirectional with centralized control

**Watch out for**: God Object anti-pattern — if the mediator grows too large, consider splitting it
