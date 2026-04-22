---
tags:
  - languages:cpp
  - concepts:design-patterns
  - concepts:oop
  - practices:software-design
level: advanced
category: language
audience:
  - audiences:developers

---
# Command Pattern

---

## Intent

- Encapsulate a request as an object
- Parameterize clients with different requests
- Support undo/redo, queuing, and logging of operations

---

## Problem: Direct Method Calls

```cpp
// Without Command — GUI is tightly coupled to business logic
class Button {
    Editor& editor;
public:
    void onClick() {
        editor.copy();  // Button knows about Editor
    }
};
```

The button cannot be reused for different operations

---

## Command Structure

![command_structure](svg/courses/languages/c++/c++-design-patterns/15_command/command_structure.svg)

---

## Command Interface and Concrete Commands

```cpp
class Command {
public:
    virtual ~Command() = default;
    virtual void execute() = 0;
    virtual void undo() = 0;
};

class InsertTextCommand : public Command {
    Document& doc;
    std::string text;
    size_t position;

public:
    InsertTextCommand(Document& d, std::string t, size_t pos)
        : doc(d), text(std::move(t)), position(pos) {}

    void execute() override {
        doc.insertAt(position, text);
    }

    void undo() override {
        doc.deleteAt(position, text.length());
    }
};
```

---

## Command: Delete Text

```cpp
class DeleteTextCommand : public Command {
    Document& doc;
    std::string deletedText;
    size_t position;
    size_t length;

public:
    DeleteTextCommand(Document& d, size_t pos, size_t len)
        : doc(d), position(pos), length(len) {}

    void execute() override {
        deletedText = doc.getTextAt(position, length);
        doc.deleteAt(position, length);
    }

    void undo() override {
        doc.insertAt(position, deletedText);
    }
};
```

---

## Command History (Undo/Redo)

```cpp
class CommandHistory {
    std::vector<std::unique_ptr<Command>> undoStack;
    std::vector<std::unique_ptr<Command>> redoStack;

public:
    void executeCommand(std::unique_ptr<Command> cmd) {
        cmd->execute();
        undoStack.push_back(std::move(cmd));
        redoStack.clear();  // New command invalidates redo history
    }

    void undo() {
        if (undoStack.empty()) return;
        auto cmd = std::move(undoStack.back());
        undoStack.pop_back();
        cmd->undo();
        redoStack.push_back(std::move(cmd));
    }

    void redo() {
        if (redoStack.empty()) return;
        auto cmd = std::move(redoStack.back());
        redoStack.pop_back();
        cmd->execute();
        undoStack.push_back(std::move(cmd));
    }
};
```

---

## Usage

```cpp
Document doc;
CommandHistory history;

// Execute commands
history.executeCommand(
    std::make_unique<InsertTextCommand>(doc, "Hello ", 0));
history.executeCommand(
    std::make_unique<InsertTextCommand>(doc, "World", 6));

std::cout << doc.getText();  // "Hello World"

history.undo();
std::cout << doc.getText();  // "Hello "

history.redo();
std::cout << doc.getText();  // "Hello World"
```

---

## Command with std::function

```cpp
class FunctionalCommand : public Command {
    std::function<void()> doAction;
    std::function<void()> undoAction;

public:
    FunctionalCommand(std::function<void()> exec,
                      std::function<void()> undo)
        : doAction(std::move(exec)), undoAction(std::move(undo)) {}

    void execute() override { doAction(); }
    void undo() override { undoAction(); }
};

// Usage — create commands from lambdas
auto cmd = std::make_unique<FunctionalCommand>(
    [&]{ light.turnOn(); },
    [&]{ light.turnOff(); }
);
```

---

## Macro Command (Composite Command)

```cpp
class MacroCommand : public Command {
    std::vector<std::unique_ptr<Command>> commands;

public:
    void add(std::unique_ptr<Command> cmd) {
        commands.push_back(std::move(cmd));
    }

    void execute() override {
        for (auto& cmd : commands) {
            cmd->execute();
        }
    }

    void undo() override {
        // Undo in reverse order
        for (auto it = commands.rbegin(); it != commands.rend(); ++it) {
            (*it)->undo();
        }
    }
};
```

---

## When to Use Command

**Use when:**

- You want to parameterize objects with operations
- You need to queue, schedule, or log operations
- You need undoable operations
- You want to decouple the object that invokes the operation from the object that performs it

**Common examples:**

- Text editor undo/redo
- Transaction systems
- Task queues and job schedulers
- GUI button/menu actions
- Macro recording
