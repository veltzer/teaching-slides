---
tags:
  - tools:unity
  - languages:csharp
level: beginner
category: game-development
audience:
  - audiences:developers

---
# C# Scripting Fundamentals

---
## What This Chapter Covers

- Why Unity uses C#
- Variables, types, and operators
- Control flow: if, switch, loops
- Functions and methods
- Classes and how Unity scripts fit into the type system

---
## Why C#

- Strongly typed, garbage collected, mature ecosystem
- Runs on .NET — Unity ships its own runtime
- Compiles to IL, then to native via Mono or IL2CPP
- Single-file scripts; one class per file by convention
- Modern C# features: properties, async/await, pattern matching, LINQ

---
## A First Script

```csharp
using UnityEngine;

public class HelloWorld : MonoBehaviour
{
    void Start()
    {
        Debug.Log("Hello, Unity!");
    }
}
```

- `using UnityEngine;` brings in Unity's API
- Class name *must* match the file name
- `MonoBehaviour` is Unity's base class for scripts attached to GameObjects
- `Start()` runs once when the GameObject becomes active
- Output appears in the Console window when you press Play

---
## Variables and Types

```csharp
int score = 0;
float health = 100f;
string playerName = "Mark";
bool isAlive = true;
Vector3 position = new Vector3(0, 1, 0);
```

- Common scalar types: `int`, `float`, `double`, `bool`, `char`
- Reference types: `string`, classes, arrays, lists
- `var` lets the compiler infer the type from the right-hand side
- Floats need the `f` suffix; without it the compiler treats `1.0` as `double`

---
## Operators

```csharp
int a = 5 + 3;        // arithmetic
bool b = a > 7;       // comparison
bool c = b && a < 10; // logical
a += 1;               // compound assignment
```

- Arithmetic: `+ - * / %`
- Comparison: `== != < > <= >=`
- Logical: `&& || !`
- Compound: `+= -= *= /= %=`
- Increment / decrement: `++ --`

---
## If / Else

```csharp
if (health <= 0) {
    Die();
} else if (health < 25) {
    PlayLowHealthSound();
} else {
    PlayNormalSound();
}
```

- Conditions go in parentheses
- Bodies in braces — *always* use braces, even for one-liners
- `else if` chains are common; consider `switch` past 3 branches

---
## Switch

```csharp
switch (state) {
    case GameState.Menu:
        ShowMenu();
        break;
    case GameState.Playing:
        UpdatePlayer();
        break;
    case GameState.GameOver:
        ShowScore();
        break;
}
```

- One arm per `case` value, terminated by `break`
- C# 8 introduced `switch` *expressions* — more concise but less common in tutorials
- Forgetting `break` is a compile error in C# (unlike C/C++)

---
## Loops

```csharp
for (int i = 0; i < 10; i++) {
    Debug.Log(i);
}

foreach (var enemy in enemies) {
    enemy.TakeDamage(5);
}

while (timeLeft > 0) {
    Tick();
}
```

- `for`: counter-controlled, common when you need the index
- `foreach`: iterate any collection without indexes
- `while`: condition-controlled
- `do { ... } while (...)`: runs the body at least once

---
## Functions / Methods

```csharp
public int Add(int a, int b)
{
    return a + b;
}

void DoNothing() { }
```

- `public`, `private`, `protected` control visibility
- Return type comes before the name; `void` for "returns nothing"
- Parameters in parentheses
- Methods inside a class are sometimes called "functions" — same thing here

---
## Method Overloading

```csharp
public void Take(int damage) { ... }
public void Take(int damage, string source) { ... }
public void Take(DamageInfo info) { ... }
```

- Same name, different parameter list
- The compiler picks the version that matches at the call site
- Used heavily in Unity APIs (e.g., `Instantiate` has many overloads)

---
## Classes

```csharp
public class Enemy
{
    public int Health = 10;
    private string name = "Goblin";

    public void TakeDamage(int amount)
    {
        Health -= amount;
    }
}
```

- A class bundles state (fields) with behaviour (methods)
- `public` fields show up in the Inspector when on a `MonoBehaviour`
- Prefer `private` fields with public methods (encapsulation)
- Properties (`public int Health { get; set; }`) are common too

---
## Instances

```csharp
Enemy goblin = new Enemy();
goblin.TakeDamage(3);

// On a GameObject:
GetComponent<Enemy>().TakeDamage(3);
```

- `new ClassName()` creates an instance
- For `MonoBehaviour`s, use `AddComponent`/`GetComponent` instead — Unity manages their lifecycle
- Reference vs value semantics matter: classes are references, structs are values

---
## Namespaces

```csharp
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

namespace MyGame
{
    public class Player : MonoBehaviour { }
}
```

- Group related types under a namespace
- Avoid name collisions with the rest of the world
- `using` brings types into scope for a file

---
## Common C# Pitfalls in Unity

- Comparing floats with `==` — they rarely match exactly; use `Mathf.Approximately`
- Allocating in `Update()` — runs 60+ times a second, GC pressure adds up
- Forgetting `f` on float literals: `transform.position = new Vector3(0, 1.5, 0);` won't compile
- Capturing variables in closures — fine, but watch the heap allocation
- `null` reference exceptions on uninitialized `[SerializeField]` references

---
## C# Scripting Lifecycle

![script_lifecycle](svg/courses/unity/introduction-to-game-development-with-unity/03_csharp_scripting_fundamentals/script_lifecycle.svg)
