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

<svg width="650" height="320" xmlns="http://www.w3.org/2000/svg">
  <rect x="225" y="10" width="200" height="70" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="325" y="35" text-anchor="middle" font-size="13" font-weight="bold">AbstractFactory</text>
  <text x="325" y="52" text-anchor="middle" font-size="10" font-style="italic">+ createButton()</text>
  <text x="325" y="67" text-anchor="middle" font-size="10" font-style="italic">+ createCheckbox()</text>

  <rect x="50" y="130" width="180" height="60" fill="#e1f5fe" stroke="#0277bd" stroke-width="2"/>
  <text x="140" y="155" text-anchor="middle" font-size="12">WindowsFactory</text>
  <text x="140" y="175" text-anchor="middle" font-size="10">+ createButton()</text>

  <rect x="420" y="130" width="180" height="60" fill="#f1f8e9" stroke="#689f38" stroke-width="2"/>
  <text x="510" y="155" text-anchor="middle" font-size="12">MacFactory</text>
  <text x="510" y="175" text-anchor="middle" font-size="10">+ createButton()</text>

  <rect x="50" y="240" width="80" height="40" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="90" y="265" text-anchor="middle" font-size="10">WinButton</text>

  <rect x="150" y="240" width="80" height="40" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="190" y="265" text-anchor="middle" font-size="10">WinCheckbox</text>

  <rect x="420" y="240" width="80" height="40" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="460" y="265" text-anchor="middle" font-size="10">MacButton</text>

  <rect x="520" y="240" width="80" height="40" fill="#fce4ec" stroke="#c2185b" stroke-width="2"/>
  <text x="560" y="265" text-anchor="middle" font-size="10">MacCheckbox</text>

  <line x1="140" y1="130" x2="280" y2="80" stroke="#333" stroke-width="1.5"/>
  <line x1="510" y1="130" x2="370" y2="80" stroke="#333" stroke-width="1.5"/>
</svg>

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
