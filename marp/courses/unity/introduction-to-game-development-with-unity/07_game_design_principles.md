---
tags:
  - tools:unity
  - practices:game-design
level: beginner
category: game-development
audience:
  - audiences:developers

---
# Game Design Principles

---
## Feedback Loops

![feedback_loops](svg/courses/unity/introduction-to-game-development-with-unity/07_game_design_principles/feedback_loops.svg)

---
## What This Chapter Covers

- The core ingredients of a game
- What "fun" actually means and how to design for it
- Player experience: pacing, feedback, agency
- Level design and world-building
- Balancing challenge and reward
- A short tour of common pitfalls

---
## What Makes a Game

- A **goal** the player is trying to reach
- **Rules** that constrain how they can do it
- A **mechanic** — the core interaction the player performs
- **Feedback** — the world responds visibly to what the player does
- A **conclusion** — win, lose, or some end state worth reaching

---
## The Core Loop

- The smallest repeatable cycle of player activity
- "Move &#8594; aim &#8594; shoot &#8594; pickup &#8594; move" is a shooter loop
- "Plant &#8594; wait &#8594; harvest &#8594; sell &#8594; expand" is a farm loop
- A game lives or dies on whether its core loop is satisfying after the 100th repetition
- Prototype the core loop *first*, before art, story, or systems

---
## Mechanics, Dynamics, Aesthetics

- The **MDA framework**: a way to think about game design
- **Mechanics**: rules and code (you write these)
- **Dynamics**: behaviour that emerges when players use the mechanics
- **Aesthetics**: how the game *feels* — challenge, story, fellowship, discovery
- Designers tweak mechanics; players experience aesthetics

---
## The MDA Loop

![mda_loop](svg/courses/unity/introduction-to-game-development-with-unity/07_game_design_principles/mda_loop.svg)

---
## What "Fun" Means

- Different players want different things — there is no universal "fun"
- Common categories (Bartle's taxonomy): Achievers, Explorers, Socialisers, Killers
- A puzzle game that delights an Achiever might bore a Socialiser
- Knowing your target audience prevents a lot of design grief
- Watching real people play your game is a humbling, indispensable practice

---
## Player Agency

- The player should feel that *their* choices matter
- A "choice" with no consequence is a fake choice — players see through this
- Real agency: the world remembers what you did
- Agency doesn't require huge open worlds — even small choices land if they have weight
- Avoid the illusion of choice; either commit to consequence or remove the choice

---
## Feedback Loops

- Every player action needs a perceptible response
- Visual: animation, particles, screen shake
- Audio: sound effect, music swell
- Haptic: controller rumble (where supported)
- A delay between action and feedback &gt; 100ms feels sluggish

---
## Difficulty Curves

- Players need to *feel* like they're getting better
- Too easy: no satisfaction from progress
- Too hard: frustration, then quitting
- The Flow channel: difficulty rises in step with player skill
- Periodic dips give breathing room before the next climb

---
## Onboarding

- The first 5 minutes determine whether a player keeps playing
- Teach mechanics by *using* them, not by tutorial pop-ups
- Introduce one mechanic at a time
- Reward early experimentation
- "Show, don't tell" — let the level itself train the player

---
## Pacing

- Mix high-intensity sequences with low-intensity ones
- Constant high intensity is exhausting; constant low intensity is boring
- Use level structure (combat &#8594; exploration &#8594; puzzle &#8594; combat) to set rhythm
- Music and lighting reinforce pacing without saying anything
- Every game is, at heart, a controlled emotional journey

---
## Level Design Basics

- Block out levels with primitive shapes first ("greybox")
- Test gameplay in greybox before adding any art
- Sightlines: where can the player see? Where do you draw their eye?
- Affordances: handholds invite climbing, alcoves invite hiding
- Iterate on the layout *first* — once art is in, changes get expensive

---
## World Building

- Setting and tone shape every other design decision
- A single coherent visual language beats a fancy mishmash
- Lighting carries 60%+ of the mood — invest time in it
- Audio (ambient sound, music) is the other 30%
- The world should suggest stories happened here even when you weren't looking

---
## Reward Schedules

- Constant reward &#8594; rewards lose meaning fast
- Variable rewards (sometimes nothing, sometimes a lot) drive engagement
- Beware crossing into manipulative territory (loot boxes, dark patterns)
- Long-term progression: power-ups, unlocks, cosmetics
- Match reward type to player motivation (Achievers want stats; Explorers want lore)

---
## Balancing

- Numbers (damage, health, prices) must support the experience you want
- Spreadsheets are honest about whether your maths works
- Playtest with real players — your intuition lies
- Buff weak options before nerfing strong ones
- A balance pass is never "done"; treat it as continuous

---
## Prototyping

- Build the smallest playable thing as fast as possible
- Use placeholder art and sounds
- The goal is to learn whether the *idea* is fun
- Throw away prototypes that don't work — that's the point of prototyping
- A prototype that ships is rare and lucky

---
## Common Pitfalls

- Designing in your head — playtest *early*, with someone other than yourself
- Adding features to fix a fundamentally broken core loop
- "Fun is in the polish" — no, fun is in the design
- Confusing complexity with depth
- Not finishing — the world is full of unfinished prototypes; finishing is the rarest skill

---
## Course Wrap-Up

- The Unity editor, scenes, and GameObjects: structure
- Models, materials, animations: assets that look like something
- C# scripting: the glue that makes things behave
- UI: the surface the player interacts with
- Game design: making sure that all of the above adds up to *fun*
- Build something small. Ship it. Then build the next one.
