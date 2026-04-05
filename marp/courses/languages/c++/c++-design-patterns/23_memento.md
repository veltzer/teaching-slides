# Memento Pattern

---

## Intent

- Capture an object's internal state so it can be restored later
- Do so without violating encapsulation
- Support undo mechanisms without exposing implementation details

---

## Problem: Exposing State for Undo

```cpp
// To support undo, we need to save state — but this breaks encapsulation
class Editor {
public:
    // Exposing internals just for undo
    std::string content;
    int cursorPos;
    std::string selection;
    // Now anyone can mess with these fields
};
```

---

## Memento Structure Diagram

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="50" width="150" height="70" fill="#fff3e0" stroke="#f57c00" stroke-width="2"/>
  <text x="95" y="75" text-anchor="middle" font-size="13" font-weight="bold">Caretaker</text>
  <text x="95" y="95" text-anchor="middle" font-size="10">history: Memento[]</text>

  <rect x="220" y="50" width="150" height="70" fill="#e3f2fd" stroke="#1976d2" stroke-width="2"/>
  <text x="295" y="75" text-anchor="middle" font-size="13" font-weight="bold">Originator</text>
  <text x="295" y="95" text-anchor="middle" font-size="10">+ save(): Memento</text>

  <rect x="420" y="50" width="150" height="70" fill="#e8f5e8" stroke="#388e3c" stroke-width="2"/>
  <text x="495" y="75" text-anchor="middle" font-size="13" font-weight="bold">Memento</text>
  <text x="495" y="95" text-anchor="middle" font-size="10">state (private)</text>

  <line x1="170" y1="85" x2="220" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#mmArr)"/>
  <line x1="370" y1="85" x2="420" y2="85" stroke="#333" stroke-width="1.5" marker-end="url(#mmArr)"/>
  <text x="195" y="78" text-anchor="middle" font-size="9">uses</text>
  <text x="395" y="78" text-anchor="middle" font-size="9">creates</text>

  <defs>
    <marker id="mmArr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333"/>
    </marker>
  </defs>
</svg>

---

## Memento Structure

```cpp
class EditorMemento {
    friend class Editor;  // Only Editor can access internals
    std::string content;
    int cursorPos;
    std::string selection;

    EditorMemento(std::string c, int pos, std::string sel)
        : content(std::move(c)), cursorPos(pos),
          selection(std::move(sel)) {}

public:
    // Public interface reveals nothing about the state
    std::string getName() const {
        return "Snapshot at cursor " + std::to_string(cursorPos);
    }
};
```

---

## Originator (Editor)

```cpp
class Editor {
    std::string content;
    int cursorPos = 0;
    std::string selection;

public:
    void type(const std::string& text) {
        content.insert(cursorPos, text);
        cursorPos += text.length();
    }

    void moveCursor(int pos) { cursorPos = pos; }

    void select(int start, int end) {
        selection = content.substr(start, end - start);
    }

    // Create a memento
    EditorMemento save() const {
        return EditorMemento(content, cursorPos, selection);
    }

    // Restore from memento
    void restore(const EditorMemento& memento) {
        content = memento.content;
        cursorPos = memento.cursorPos;
        selection = memento.selection;
    }

    std::string getContent() const { return content; }
};
```

---

## Caretaker (History Manager)

```cpp
class History {
    std::vector<EditorMemento> snapshots;
    Editor& editor;

public:
    explicit History(Editor& e) : editor(e) {}

    void save() {
        snapshots.push_back(editor.save());
    }

    void undo() {
        if (snapshots.empty()) return;
        auto memento = snapshots.back();
        snapshots.pop_back();
        editor.restore(memento);
    }

    size_t size() const { return snapshots.size(); }
};

// Usage
Editor editor;
History history(editor);

history.save();
editor.type("Hello ");
history.save();
editor.type("World");

std::cout << editor.getContent();  // "Hello World"
history.undo();
std::cout << editor.getContent();  // "Hello "
history.undo();
std::cout << editor.getContent();  // ""
```

---

## Memento with Limited History

```cpp
class BoundedHistory {
    std::deque<EditorMemento> snapshots;
    Editor& editor;
    size_t maxSize;

public:
    BoundedHistory(Editor& e, size_t max) : editor(e), maxSize(max) {}

    void save() {
        if (snapshots.size() >= maxSize) {
            snapshots.pop_front();  // Remove oldest
        }
        snapshots.push_back(editor.save());
    }

    void undo() {
        if (snapshots.empty()) return;
        editor.restore(snapshots.back());
        snapshots.pop_back();
    }
};
```

---

## When to Use Memento

**Use when:**

- You need to save and restore an object's state (undo/redo)
- Direct access to the object's fields would violate encapsulation
- You need snapshots of an object's state

**Watch out for:**

- Memory consumption if mementos are large or frequent
- Consider incremental mementos (diffs) for large objects
- The `friend` keyword in C++ makes this pattern natural to implement
