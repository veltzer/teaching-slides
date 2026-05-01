---
tags:
  - data-and-ai:llm
level: advanced
category: machine-learning
audience:
  - audiences:developers

---
# Tools and Function Calling

---
## What This Chapter Covers

- What tools are
- Defining tools
- JSON schema
- Tool selection
- Error handling

---
## What a Tool Is

- A function the agent can invoke
- Has a name, description, params
- Returns a result
- The model decides when to call it

---
## Why Tools

- LLMs are not databases
- LLMs cannot execute code
- LLMs do not know real-time data
- Tools bridge to the real world

---
## Tool Definition

- Name: short, verb-like
- Description: tells model when to use
- Parameters: JSON schema
- Return type: structured

---
## JSON Schema for Tools

- Type, properties, required fields
- Used by model to format calls
- Strict mode rejects malformed args
- Validate on the server side too

---
## Anatomy of a Tool Call

- Model emits JSON
- Runtime parses
- Function executes
- Result serialized back

---
## Choosing What to Expose

- One tool per coherent action
- Avoid mega-tools with switches
- Avoid duplicate tools
- Keep parameter sets small

---
## Description Quality

- Description is a prompt
- Tells model when to pick it
- Bad description: tool gets ignored or misused
- Test by varying user input

---
## Tool Errors

- Network errors
- Permission denied
- Bad arguments
- Return structured error to model

---
## Letting the Model Recover

- Return error message in result
- Model can retry with fixed args
- Or apologize to user
- Cap retries to avoid loops

---
## Side Effects

- Read-only vs mutating tools
- Confirm before mutations
- Idempotency keys for retries
- Audit log all calls

---
## Schema Validation

- Validate on entry
- Reject malformed args
- Don't trust the model
- Same as any external input

---
## Common Function-Calling Mistakes

- Vague tool descriptions
- No schema validation
- Over-broad tool surface
- No retry strategy
- Missing audit logs
