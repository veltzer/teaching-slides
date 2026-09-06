---
tags:
  - tools:unity
  - practices:animation
level: beginner
category: game-development
audience:
  - audiences:developers

---

# Animation

---

## Animation Principles

![animation_principles](svg/courses/unity/introduction-to-game-development-with-unity/05_animation/animation_principles.svg)

---

## What This Chapter Covers

- The principles that make animation feel alive
- How Unity's Animator works
- Creating animation clips inside Unity
- Importing animated characters from external tools
- Blending and transitioning between states
- Driving animations from script

---

## What "Animation" Means Here

- Changing a property over time — position, rotation, colour, anything
- Two big buckets:
    - **Skeletal** animation: a rig of bones drives a mesh (characters)
    - **Property** animation: any field of any component over time
- Both go through the same Animator pipeline in Unity

---

## A Few Animation Principles

- **Squash and stretch**: even rigid things deform under acceleration
- **Anticipation**: a tiny windup before a big move
- **Follow-through**: things keep moving briefly after a stop
- **Easing**: motion isn't linear; ease in and out for natural feel
- These come from Disney's Twelve Principles of Animation

---

## Animation Clip vs Animator

- A **Clip** is a single named animation: "Walk", "Jump", "Idle"
- The **Animator** is a state machine that picks which clip plays
- Clips are reusable across many Animators
- The state machine handles transitions, blending, and conditions
- Both live as assets in your project

---

## Creating a Clip in Unity

- Select a GameObject &#8594; Window &#8594; Animation &#8594; Animation
- Click "Create" — Unity prompts for a clip name and saves it
- Click the red Record button
- Move time forward in the timeline; change properties; Unity records keyframes
- Stop recording, hit Play in the Animation window to preview

---

## Keyframes

- A **keyframe** is "at time t, this property has value v"
- Unity interpolates between keyframes
- Right-click a keyframe to change interpolation: linear, smooth, constant
- Add keyframes for any animatable property — colour, scale, intensity, custom script fields
- Less is more: a few good keyframes beat dozens of redundant ones

---

## The Animator Window

- Window &#8594; Animation &#8594; Animator
- Shows the state machine for the currently selected GameObject's Animator
- States: clips that can play
- Transitions: arrows between states
- Parameters: variables that drive transitions (Bool, Int, Float, Trigger)

---

## Animator State Machine

![state_machine](svg/courses/unity/introduction-to-game-development-with-unity/05_animation/state_machine.svg)

---

## Transitions

- Right-click a state &#8594; Make Transition &#8594; click target
- Set conditions on the transition's Inspector
- Conditions check parameters: e.g., `IsRunning == true`
- Adjust transition duration for smooth blends
- Always provide a way back — a transition graph with no exit is a trap

---

## Parameters

- Bool: on/off (`IsRunning`, `IsGrounded`)
- Int: enum-like states
- Float: continuous values (`Speed`)
- Trigger: like Bool but auto-resets after triggering one transition
- Set from script: `animator.SetBool("IsRunning", true)`

---

## Importing Animated Characters

- FBX from Maya / Blender / Mixamo brings the rig and clips together
- In the Inspector: Rig tab &#8594; Animation Type &#8594; Humanoid (for human characters)
- Humanoid lets Unity retarget animations across different characters
- Animation tab: rename, trim, loop the imported clips
- Drag the result into the Hierarchy and you have an animated character

---

## Mixamo Workflow

- Mixamo (mixamo.com, free): upload a model, get hundreds of mocap animations
- Download as FBX with skin, or as separate animation files
- Drop into Unity, set rig type to Humanoid, ready to use
- Great for prototyping; production usually does custom mocap or hand-animation
- Watch the animation pivot; mismatched pivots look strange

---

## Blend Trees

- A way to interpolate between several clips based on a parameter
- Classic example: 1D blend tree from Idle &#8594; Walk &#8594; Run on a Speed parameter
- 2D blend trees take two parameters (e.g., move-x, move-y)
- Smoother than chained transitions for movement
- Add via Animator window: right-click empty space &#8594; Create State &#8594; From New Blend Tree

---

## Driving Animation From Script

```csharp
private Animator anim;

void Awake() {
    anim = GetComponent<Animator>();
}

void Update() {
    float speed = rb.velocity.magnitude;
    anim.SetFloat("Speed", speed);

    if (Input.GetKeyDown(KeyCode.Space)) {
        anim.SetTrigger("Jump");
    }
}
```

- Set parameters; let the Animator decide what plays
- Avoid driving the Animator directly with `Play("clipname")` — couples logic to clip names

---

## Layers and Avatar Masks

- Animator can have multiple **layers** that play in parallel
- Lower layers blend into upper layers via masks
- Example: base layer plays the locomotion; upper layer plays a "wave hand" only on the upper body
- Masks define which bones a layer affects
- Powerful but adds complexity; ignore until you need it

---

## Tweens for UI and Simple Motion

- Animator is overkill for "fade this button to 50% over 0.3s"
- Use a tweening library (DOTween, LeanTween) or write simple coroutines
- Tweens drive properties from script; no state machine, no clips
- Lighter weight, less ceremony for one-off animations
- Coroutine example: gradual fade with `Mathf.Lerp` and `yield return null`

---

## Common Pitfalls

- Animator state names typo'd in `SetTrigger` calls — silent failure
- Transition durations too long — character feels sluggish
- Forgetting to set a default state — Animator does nothing
- Animating values that another script also writes every frame (script wins, animation looks broken)
- Importing every animation as Generic when you want Humanoid retargeting
