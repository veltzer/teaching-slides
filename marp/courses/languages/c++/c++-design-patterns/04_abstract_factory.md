# Abstract Factory Pattern

---

## Intent

- Provide an interface for creating families of related objects
- Ensure that created objects are compatible with each other
- Encapsulate platform-specific or theme-specific creation logic

---

## Problem: Incompatible Object Families

```cpp
// Risk of mixing incompatible UI elements
auto button = new WindowsButton();
auto checkbox = new MacCheckbox();    // Mismatch!
auto textbox = new LinuxTextBox();    // More mismatch!
```

We need a way to ensure that all created objects belong to the same family

---

## Abstract Factory Structure

![abstract_factory_structure](../../../../../svg/courses/languages/c++/c++-design-patterns/04_abstract_factory/abstract_factory_structure.svg)

---

## Product Interfaces

```cpp
class Button {
public:
    virtual void render() = 0;
    virtual void onClick(std::function<void()> handler) = 0;
    virtual ~Button() = default;
};

class Checkbox {
public:
    virtual void render() = 0;
    virtual bool isChecked() const = 0;
    virtual void toggle() = 0;
    virtual ~Checkbox() = default;
};

class TextBox {
public:
    virtual void render() = 0;
    virtual std::string getText() const = 0;
    virtual void setText(const std::string& text) = 0;
    virtual ~TextBox() = default;
};
```

---

## Concrete Products

```cpp
class WindowsButton : public Button {
public:
    void render() override {
        std::cout << "Rendering Windows-style button\n";
    }
    void onClick(std::function<void()> handler) override {
        handler();
    }
};

class MacButton : public Button {
public:
    void render() override {
        std::cout << "Rendering macOS-style button\n";
    }
    void onClick(std::function<void()> handler) override {
        handler();
    }
};
```

---

## Abstract Factory Interface

```cpp
class GUIFactory {
public:
    virtual std::unique_ptr<Button> createButton() = 0;
    virtual std::unique_ptr<Checkbox> createCheckbox() = 0;
    virtual std::unique_ptr<TextBox> createTextBox() = 0;
    virtual ~GUIFactory() = default;
};
```

---

## Concrete Factories

```cpp
class WindowsFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<WindowsButton>();
    }
    std::unique_ptr<Checkbox> createCheckbox() override {
        return std::make_unique<WindowsCheckbox>();
    }
    std::unique_ptr<TextBox> createTextBox() override {
        return std::make_unique<WindowsTextBox>();
    }
};

class MacFactory : public GUIFactory {
public:
    std::unique_ptr<Button> createButton() override {
        return std::make_unique<MacButton>();
    }
    std::unique_ptr<Checkbox> createCheckbox() override {
        return std::make_unique<MacCheckbox>();
    }
    std::unique_ptr<TextBox> createTextBox() override {
        return std::make_unique<MacTextBox>();
    }
};
```

---

## Client Code

```cpp
class Application {
    std::unique_ptr<GUIFactory> factory;

public:
    explicit Application(std::unique_ptr<GUIFactory> f)
        : factory(std::move(f)) {}

    void createUI() {
        auto button = factory->createButton();
        auto checkbox = factory->createCheckbox();
        auto textbox = factory->createTextBox();

        button->render();
        checkbox->render();
        textbox->render();
    }
};

// Select factory based on platform
std::unique_ptr<GUIFactory> createFactory() {
#ifdef _WIN32
    return std::make_unique<WindowsFactory>();
#elif __APPLE__
    return std::make_unique<MacFactory>();
#else
    return std::make_unique<LinuxFactory>();
#endif
}
```

---

## Abstract Factory vs Factory Method

| Aspect | Factory Method | Abstract Factory |
|--------|---------------|-----------------|
| Creates | One product | Family of products |
| Uses | Inheritance | Composition |
| Extension | New creator subclass | New factory subclass |
| Focus | Single product variation | Product family consistency |
| Complexity | Simpler | More complex |

Use Abstract Factory when you need to ensure that related objects are used together
