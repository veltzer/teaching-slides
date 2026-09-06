---
tags:
  - concepts:oop
  - concepts:uml
level: beginner
category: design-patterns
audience:
  - audiences:developers

---

# UML Class Diagrams

---

## What This Chapter Covers

- Why UML is useful (and where it's not)
- The class box notation
- Visibility and types
- Associations, aggregation, composition
- Inheritance and interface implementation
- Reading and creating diagrams

---

## Why UML

- A *visual* notation for OO designs
- Lets you talk about a system without dropping into a specific language's syntax
- Great for whiteboard discussions
- Useful as overview documentation
- Less useful as exhaustive code-mirroring documentation (those go stale)

---

## A UML Class

![uml_class](svg/courses/principles/object-oriented-programming/10_uml_class_diagrams/uml_class.svg)

---

## Class Box Layout

- Top compartment: class name (italic if abstract)
- Middle: attributes
- Bottom: methods
- Visibility prefix: `+` public, `-` private, `#` protected
- Underline a member to mark it `static`

---

## Attribute Notation

- `+ name : type = default`
- Visibility, name, type, optional default
- Example: `- balance : double = 0.0`
- Stereotypes in `<<...>>` for special meanings (rare in practice)

---

## Method Notation

- `+ methodName(param: Type, ...) : ReturnType`
- Example: `+ deposit(amount : double) : void`
- Constructor is the same as a method with no return type
- Abstract methods in italic; underline for static

---

## Associations

- A line between two classes means they reference each other
- Multiplicities at the ends: `1`, `0..1`, `*`, `1..*`
- Example: `Order 1 ----- 1..* OrderLine`
- Direction arrows show which class knows about the other
- A bare line implies bidirectional knowledge

---

## Aggregation vs Composition

- **Aggregation** (open diamond): "has-a", but the part can outlive the whole
- **Composition** (filled diamond): "has-a", and the part dies with the whole
- Library has Books (books exist independently) — aggregation
- House has Rooms (rooms make no sense without the house) — composition
- Distinction matters in the design; less in the code

---

## Inheritance Notation

- A line with a hollow triangle pointing to the *base* class
- `Dog ---|> Animal` means "Dog inherits from Animal"
- Multiple inheritance: multiple lines from the subclass
- Abstract base classes: italicise the class name

---

## Interface Implementation

- Dashed line with a hollow triangle pointing to the interface
- Interface is shown with `<<interface>>` stereotype above the name
- A class can implement many interfaces

---

## Dependencies

- Dashed arrow from "uses" to "is used by"
- Less coupling than association — typically a transient use
- Example: `OrderService ---> EmailService` (uses for notification)
- Distinguishes "has a field of" from "calls a method on, occasionally"

---

## A Small Diagram, In Words

- `Customer 1 ---- 0..* Order` (composition: orders die with the customer)
- `Order 1 ---- 1..* OrderLine`
- `OrderLine *---- 1 Product` (aggregation: products outlive lines)
- `Order ---|> Auditable` (interface)
- That's a small e-commerce model in five lines

---

## Tools for UML

- **PlantUML**: text-based, generates diagrams from a DSL — version-controllable
- **Mermaid**: similar idea, popular in markdown
- **draw.io / diagrams.net**: free, web-based
- **Lucidchart, Visio**: commercial, polished
- For team collaboration, text-based tools win — diffs make sense

---

## When to Use UML

- Whiteboard discussions about a new design
- "Here's the lay of the land" overview docs
- Communicating an architecture to non-developers
- Comparing alternative designs side by side
- Avoiding it: trying to capture *every* class in the system in one giant diagram

---

## When Not to Use UML

- As exhaustive documentation that mirrors every class — code is the spec
- For algorithms — use sequence diagrams or pseudocode
- For data flow — different diagram type
- When the team doesn't read the diagrams anyway
- Never — UML *is* the deliverable you're building (Big Up Front Design)

---

## A Few Pragmatic Tips

- Diagram the *interesting* parts; skip the boilerplate
- Update diagrams when you change the design — and only then
- Keep diagrams small enough to fit on a screen / one page
- Annotate sparingly — too much noise, less value
- A diagram with five well-chosen classes beats one with thirty

---

## Common Mistakes

- Drawing *every* class &#8594; unreadable wall of boxes
- Stale diagrams that contradict the code
- Confusing aggregation and composition (mostly harmless)
- Treating the diagram as the source of truth instead of the code
- Forgetting that diagrams age — date them, mark them as design vs as-built
