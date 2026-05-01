---
tags:
  - tools:unity
  - practices:game-development
level: beginner
category: game-development
audience:
  - audiences:developers

---
# Introduction to Unity

---
## What This Chapter Covers

- What Unity is, and what kinds of games people make in it
- Installing Unity Hub and the editor
- The main editor windows and what each is for
- Creating, opening, and organising a project
- Moving around a 3D scene
- Manipulating GameObjects with the gizmos

---
## What Unity Is

- A cross-platform game engine and editor
- Builds 2D, 3D, AR, and VR games for ~20 platforms from one codebase
- Used for games (Among Us, Hearthstone), training simulators, and animated film
- Free for hobbyists; paid tiers for commercial use
- Scripting language: C# on .NET

---
## Why People Choose Unity

- Easy ramp from "I have an idea" to "something visual is running"
- Asset Store with thousands of ready-made models, scripts, and tools
- Huge community: tutorials, forums, free assets
- One project &#8594; Windows, Mac, Linux, iOS, Android, consoles, WebGL
- Trade-offs exist (Unity is opinionated and changes often) — covered later

---
## Installing Unity

- Download Unity Hub from unity.com
- Hub manages multiple editor versions and projects side-by-side
- Always pick an LTS (Long Term Support) version for learning
- During install, add the modules for the platforms you'll target
- A fresh install is multi-GB; budget time and disk space

---
## Unity Hub Layout

- **Projects**: list of every project you have on disk
- **Installs**: editor versions installed
- **Learn**: starter projects and Unity tutorials
- **Community**: events and forums
- The Hub never opens a project itself — it launches the editor for you

---
## Creating a New Project

- Click "New Project" in the Hub
- Pick a template: 3D, 2D, URP (Universal Render Pipeline), HDRP, etc.
- For learning: 3D (Built-In Render Pipeline) is the simplest
- Name it, choose a folder; Unity creates a multi-folder structure
- First load can take a few minutes — Unity is importing all built-in assets

---
## The Editor at First Glance

![editor_layout](svg/courses/unity/introduction-to-game-development-with-unity/01_introduction_to_unity/editor_layout.svg)

---
## Scene View

- The 3D viewport where you arrange your level
- Click and drag in empty space to look around
- Right-click drag + WASD to fly around (like an FPS camera)
- F to focus on the selected object
- This is *editing*, not playing — what you see here is the design state

---
## Game View

- Shows what the player sees when the game runs
- Drives the active Camera in the scene
- Pick a target resolution from the dropdown
- The Game view is mainly for testing during Play mode
- The Scene view and Game view almost always show different things

---
## Hierarchy Window

- A list of every GameObject in the current scene, in a tree
- Drag to make one object a child of another
- Right-click for create / delete / rename
- Search bar at the top filters by name
- Selecting here highlights in the Scene view, and vice-versa

---
## Inspector Window

- Shows the *components* of the selected object
- Every GameObject has a Transform; most have more
- Add components via the "Add Component" button at the bottom
- Edit fields directly — values update in the running game in Play mode
- This is where 80% of editor work happens

---
## Project Window

- A view of your project's `Assets` folder
- Models, textures, audio, prefabs, scripts — all live here
- Drag from here into the Scene or Hierarchy to add an asset to a scene
- Folders here = folders on disk; rename here, not in Finder/Explorer
- Right-click to create new C# scripts, materials, prefabs

---
## Console Window

- Where Unity prints messages, warnings, and errors
- `Debug.Log("hello")` from a script appears here
- Errors stop scripts from running; clear the console to see fresh output
- Yellow triangle icons = warnings; red circles = errors
- Always check the console when something doesn't work

---
## GameObjects and Components

- A GameObject is a thing in the scene — a player, a tree, a camera
- A GameObject by itself does nothing — it's a container for components
- Components add behaviour: a Mesh Renderer to draw, a Rigidbody to fall, a script to control
- Add and remove components in the Inspector
- The Transform component (position / rotation / scale) is always present

---
## Manipulating Objects

- Move, Rotate, Scale: keys W, E, R; Q is the hand pan tool
- Each tool shows handles in the Scene view — drag the coloured arrows
- Hold Shift to scale uniformly
- Hold Ctrl (Cmd on Mac) to snap to a grid
- Coordinates: red = X, green = Y (up), blue = Z (forward)

---
## Saving Your Work

- Save the scene: File &#8594; Save (Ctrl+S)
- Scenes are `.unity` files in your `Assets/Scenes/` folder
- Save the project: File &#8594; Save Project — saves preferences and meta files
- Scripts are saved by your code editor, not by Unity
- Commit early, commit often — Unity projects benefit from version control

---
## Project Layout on Disk

- `Assets/` — everything you create or import (commit this)
- `ProjectSettings/` — project-wide settings (commit this)
- `Packages/` — package manifest (commit `manifest.json`)
- `Library/`, `Logs/`, `Temp/`, `obj/` — build artifacts (do *not* commit)
- A `.gitignore` template for Unity is one search away

---
## What's Next

- Next chapter: 3D modeling concepts and bringing models into Unity
- After that: writing C# scripts to make objects do things
- The course builds toward shipping a small playable game
- Don't be precious about saving — experimentation is the point
