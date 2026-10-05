---
tags:
  - data-and-ai:ai
  - data-and-ai:generative-ai
  - concepts:code-generation
  - tools:github
  - practices:productivity
level: intermediate
category: ai
audience:
  - audiences:developers
  - audiences:team-leads
  - audiences:devops

---

# Code Completions in Practice

---

## What This Chapter Covers

- Ghost text: accepting, rejecting, partial acceptance, alternatives
- Next edit suggestions: completions that follow your edits
- Steering completions without opening chat
- Turning completions off when they get in the way
- Public code matching, code referencing and content exclusions

---

## The Life of a Suggestion

![ghost_text_lifecycle](svg/courses/ai/github-copilot-in-practice/02_code_completions_in_practice/ghost_text_lifecycle.svg)

---

## Ghost Text Mechanics

- You pause typing, Copilot sends a request in the background
- The answer appears as grey ghost text at the cursor
- Ghost text is not code yet: nothing is in the buffer
- Keep typing and the suggestion adapts or disappears
- Typing the same characters as the suggestion keeps it alive
- One suggestion can be a word, a line or a whole function

---

## Accepting and Rejecting

- `Tab` accepts the whole suggestion
- `Esc` dismisses it
- Simply continuing to type also rejects it
- Partial acceptance is the underused superpower:
    - accept the next word when only the start is right
    - accept the next line of a long multi-line suggestion
- Partial acceptance lets you take the good part and steer the rest

---

## Cycling Through Alternatives

- The first suggestion is not the only one Copilot has
- `Alt+]` / `Alt+[` move to the next and previous alternative
- Hover the ghost text to see the inline toolbar with `1/3` counters
- `Ctrl+Enter` opens the completions panel with several candidates
- Useful when the first suggestion has the right shape but the wrong detail

---

## Keyboard Shortcuts Worth Internalizing

| Action | `VS Code` | `JetBrains` |
| --- | --- | --- |
| Accept suggestion | `Tab` | `Tab` |
| Dismiss | `Esc` | `Esc` |
| Accept next word | `Ctrl+Right` | `Ctrl+Right` |
| Accept next line | unbound by default | `Ctrl+Alt+Right` |
| Next / previous alternative | `Alt+]` / `Alt+[` | `Alt+]` / `Alt+[` |
| Trigger suggestion manually | `Alt+\` | `Alt+\` |

On `macOS` replace `Ctrl` with `Cmd` and `Alt` with `Option`.

---

## Binding Accept Next Line in VS Code

- The command exists, the shortcut does not
- Open Keyboard Shortcuts (`Ctrl+K Ctrl+S`) and search for it
- Or add it to `keybindings.json` directly:

```json
{
    "key": "ctrl+alt+right",
    "command": "editor.action.inlineSuggest.acceptNextLine",
    "when": "inlineSuggestionVisible && !editorReadonly"
}
```

---

## Practice Drill

1. Write a function signature and wait for ghost text
1. Accept only the first word with `Ctrl+Right`
1. Cycle alternatives with `Alt+]` until you see a different approach
1. Dismiss with `Esc` and trigger again with `Alt+\`
1. Repeat until the keys are muscle memory, not menu searches

---

## Next Edit Suggestions

- Classic completions only predict text at the cursor
- Next edit suggestions (`NES`) predict where you will edit next
- Rename a parameter and `NES` proposes the matching change three lines down
- An arrow in the gutter marks the predicted location
- `Tab` jumps to it, `Tab` again accepts the edit
- Enabled with `github.copilot.nextEditSuggestions.enabled`

---

## Completion vs Next Edit Suggestion

![completion_vs_next_edit](svg/courses/ai/github-copilot-in-practice/02_code_completions_in_practice/completion_vs_nes.svg)

---

## Inline Completion vs Next Edit

| Aspect | Inline completion | Next edit suggestion |
| --- | --- | --- |
| Triggered by | Cursor position | A recent edit |
| Location | At the cursor | Anywhere in the file |
| Typical output | New code | Changes to existing code |
| Accept | `Tab` | `Tab` to jump, `Tab` to accept |
| Best for | Writing new lines | Refactors and ripple changes |

---

## Accepting a Chain of Related Edits

- Change a field name, a type or a call signature once
- `NES` proposes the next consistent change
- Accept it and the following prediction appears
- Walk the whole ripple with `Tab`, `Tab`, `Tab`
- Stop and read when a prediction looks wrong: `Esc` breaks the chain
- For edits that span files, use edit or agent mode instead

---

## What Completions Actually See

![completion_context](svg/courses/ai/github-copilot-in-practice/02_code_completions_in_practice/completion_context.svg)

---

## Open Files and Neighboring Tabs

- Completions do not search your repository
- The prompt uses the current file plus snippets from open tabs
- Tabs in the same language are preferred
- Want Copilot to use your `User` model? Open `models/user.py`
- Close unrelated tabs to stop them from polluting the prompt
- A tidy set of tabs is a cheap, effective context strategy

---

## Names, Types and Signatures as Steering Wheels

- The function name is the strongest hint you give
- Typed signatures narrow the space of plausible bodies
- Compare what you get from these two lines:

```python
def process(data):
```

```python
def parse_iso_dates(rows: list[dict[str, str]]) -> list[datetime]:
```

---

## Steering With Doc Comment Types

- Declare the interface first, then let Copilot fill the code
- The type turns a guess into a constrained problem

```javascript
/** @typedef {{id: number, email: string, active: boolean}} User */

/**
 * @param {User[]} users
 * @returns {string[]} emails of active users, sorted
 */
function activeEmails(users) {
```

---

## Comment-Driven Completion

- Write the intent as a comment, then start the next line
- Be specific about inputs, outputs and edge cases

```python
# Read a CSV of orders, skip rows where status == "cancelled",
# return total revenue per customer_id as a dict, rounded to 2 decimals
def revenue_per_customer(path: str) -> dict[str, float]:
```

- Delete or keep the comment depending on whether it documents the code

---

## When Comments Beat Chat

- The change is local: a few lines in the file you are editing
- You already know the shape of the answer
- You want to stay in the editor without switching focus
- The surrounding code already shows the style to follow
- Chat wins when you need to discuss, compare or touch many files

---

## Completion or Chat?

![completion_or_chat](svg/courses/ai/github-copilot-in-practice/02_code_completions_in_practice/completion_or_chat.svg)

---

## Giving Copilot an Example to Imitate

- Copilot is excellent at continuing a pattern
- Write the first case by hand, let it produce the rest

```python
ROUTES = [
    Route("/users", list_users, methods=["GET"]),
    Route("/users/{id}", get_user, methods=["GET"]),
    # Copilot now continues with create, update, delete
]
```

- Works for test cases, enum mappings, switch branches, fixtures

---

## When Completions Get in the Way

- Writing prose, `Markdown` or commit messages
- Typing secrets, configuration or data files
- Thinking hard and the ghost text is a distraction
- Pair programming or live demos where suggestions confuse
- The answer is rarely to uninstall: scope it instead

---

## Disabling Per Language and Per Workspace

- `github.copilot.enable` takes a map of language to boolean
- In user settings it applies everywhere
- In `.vscode/settings.json` it applies to this workspace only

```json
{
    "github.copilot.enable": {
        "*": true,
        "markdown": false,
        "plaintext": false,
        "yaml": false
    }
}
```

---

## Disabling Temporarily and Snoozing

- Click the Copilot icon in the status bar for quick toggles
- Disable completions globally or for the current language
- Snooze hides suggestions for a few minutes and re-enables by itself
- Snoozing is ideal for focused typing: no setting to forget to restore
- Manual trigger (`Alt+\`) still works for on-demand suggestions
- `JetBrains`: the Copilot status bar widget offers the same toggles

---

## The Public Code Matching Filter

![code_matching](svg/courses/ai/github-copilot-in-practice/02_code_completions_in_practice/code_matching.svg)

---

## Code Matching and Code Referencing

- Suggestions are compared to public code on `GitHub`
- Policy "block": matching suggestions are never shown
- Policy "allow": matches are shown together with a code reference
- The reference lists the repository, license and location of the match
- In `VS Code` see the `GitHub Copilot Log (Code References)` output channel
- Your plan or organization decides the policy, not each developer

---

## Content Exclusions From the Developer's Side

- Admins can exclude paths and repositories from Copilot
- In an excluded file completions are simply not offered
- Excluded files are not used as context for other files either
- The status bar icon shows that Copilot is disabled for this file
- Exclusions apply to completions and chat; check the docs for which agent features honor them
- Exclusions can take up to 30 minutes to reach your IDE

---

## What Copilot Will Not See

| Source | Used by completions? |
| --- | --- |
| Current file (above and below cursor) | Yes |
| Open tabs in the editor | Yes, as snippets |
| Closed files in the repository | No |
| Files matched by a content exclusion | No |
| Files listed in `.gitignore` | Yes, if open |
| Terminal output and test results | No |

---

## Key Takeaways

- Partial acceptance and alternatives make ghost text far more useful
- `NES` turns one edit into a guided ripple of related edits
- Steer with open tabs, names, types, comments and examples
- Scope or snooze completions instead of fighting them
- Know your organization's matching policy and exclusions
