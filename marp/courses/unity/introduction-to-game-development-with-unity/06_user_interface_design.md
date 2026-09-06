---
tags:
  - tools:unity
  - practices:ui
level: beginner
category: game-development
audience:
  - audiences:developers

---

# User Interface Design

---

## What This Chapter Covers

- The UI Canvas, the root of all UGUI elements
- Common widgets: Text, Button, Image, Slider, InputField
- Anchors and positioning across screen sizes
- Layout groups for automatic arrangement
- Wiring buttons to script methods
- Building menus and HUDs

---

## Two UI Systems

- **UGUI** (UnityEngine.UI): the original, GameObject-based, well-documented
- **UI Toolkit**: the newer system based on UXML and USS (HTML/CSS-like)
- This chapter uses UGUI — broader documentation and tutorials
- New projects can pick either; consistent across the project is what matters
- Both systems coexist in modern Unity

---

## The Canvas

- Every UI element lives under a Canvas GameObject
- A Canvas with no parent renders directly to screen
- Three render modes:
    - Screen Space - Overlay (most common, ignores camera)
    - Screen Space - Camera (lives at a distance from a camera)
    - World Space (UI in 3D space, e.g., a sign on a wall)

---

## Adding Your First Button

- GameObject &#8594; UI &#8594; Button
- Unity creates a Canvas (if needed), an EventSystem, and the Button
- The button has a child Text element
- Edit the text in the Inspector
- Press Play, click — the default visuals respond

---

## EventSystem

- A separate GameObject Unity adds when you create UI
- Routes input (mouse, touch, keyboard, gamepad) to UI elements
- Without an EventSystem, no UI is interactive
- Don't delete it accidentally
- One per scene is enough

---

## Anchors and Pivots

- Anchors define how a UI element scales and moves with its parent
- Pivot is the local origin point of the element
- Visualised as the four blue triangles in the Scene view
- Anchor to a corner: element stays in that corner regardless of screen size
- Anchor to all four corners: element stretches to fill the parent

---

## Anchor Diagram

![anchor_diagram](svg/courses/unity/introduction-to-game-development-with-unity/06_user_interface_design/anchor_diagram.svg)

---

## Common UI Widgets

- **Text** (or TextMeshPro Text): styled text
- **Image**: a sprite, optionally tinted
- **Button**: clickable; has built-in normal/hover/pressed states
- **Slider**: drag a handle, get a float value
- **Toggle**: on/off checkbox
- **InputField**: text entry from the user
- **Scroll View**: panel with vertical/horizontal scrolling

---

## Widgets Overview

![ui_widgets](svg/courses/unity/introduction-to-game-development-with-unity/06_user_interface_design/ui_widgets.svg)

---

## TextMeshPro Is the Default Text

- Sharp text at any zoom (signed distance field)
- Rich text tags: `<b>`, `<i>`, `<color=red>`, `<size=20>`
- Supports custom fonts — generate a font asset from any TTF
- Built-in support for outlines, shadows, gradients
- The legacy Text component is still around but TMP is preferred

---

## Layout Groups

- Manual placement is fragile across screen sizes
- Add a Layout Group component to a panel and its children arrange automatically
- **Horizontal** Layout: side by side
- **Vertical** Layout: stacked
- **Grid** Layout: rows and columns
- Use **Layout Element** on children to override sizing

---

## Wiring a Button to a Script

- Select the Button in the Hierarchy
- Inspector &#8594; Button (Script) &#8594; OnClick() &#8594; click `+`
- Drag the GameObject holding the script into the Object slot
- Pick the public method from the dropdown
- Press Play, click — your method runs

---

## Calling From Code Instead

```csharp
[SerializeField] private Button startButton;

void Awake() {
    startButton.onClick.AddListener(OnStartClicked);
}

void OnStartClicked() {
    SceneManager.LoadScene("Game");
}
```

- Better for buttons that change in code
- Cleaner refactoring — the wire-up is in one place
- Always add listeners in `Awake` or `OnEnable`, remove in `OnDisable`

---

## Building a HUD

- Canvas at Screen Space - Overlay
- Anchor health bar to top-left, score to top-right, mini-map to bottom-right
- Each stays put as the screen size changes
- Use a Vertical Layout Group for stacking elements like a menu list
- TextMeshPro for crisp text at any resolution

---

## Building a Menu

- Separate Canvas for the menu (or a child panel that toggles active)
- Buttons: Start, Options, Quit
- Use `Time.timeScale = 0` to pause the game while a pause menu is open
- Restore `Time.timeScale = 1` when resuming
- Don't forget UI animations to make transitions feel intentional

---

## Multiple Resolution Strategy

- Canvas Scaler component on the Canvas
- "Scale With Screen Size" mode + a reference resolution (e.g., 1920x1080)
- Match width / height: pick depending on whether your UI is portrait or landscape
- Test at the smallest target resolution; if it looks ok there, the rest follows
- Do this once at project start — switching later is painful

---

## Common Pitfalls

- Forgetting to add an EventSystem &#8594; UI looks fine, doesn't react
- Hardcoded pixel positions &#8594; broken on every other screen size
- Text rendering through walls because canvas is in World Space without sorting setup
- Adding listeners every frame in `Update` &#8594; multiple identical handlers fire
- Putting too much UI on one Canvas &#8594; rebuilds entire mesh on any change; split into sub-canvases
