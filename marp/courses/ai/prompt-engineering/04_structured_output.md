---
tags:
  - data-and-ai:llm
level: intermediate
category: machine-learning
audience:
  - audiences:developers

---

# Structured Output

---

## What This Chapter Covers

- Why structured output
- JSON mode
- Function calling
- Schema enforcement
- Parsing
- Failure handling

---

## Why Structured Output

- Software needs to consume model output
- Free text is hard to parse
- Models can produce JSON, XML, etc.
- Bridge between LLM and code

---

## Three Modes

![structured_modes](svg/courses/ai/prompt-engineering/04_structured_output/structured_modes.svg)

---

## Format Choices

![format_choices](svg/courses/ai/prompt-engineering/04_structured_output/format_choices.svg)

---

## JSON Mode

- Model outputs valid JSON
- Many APIs support this directly
- Specify the schema in prompt
- Validate after

---

## Sample JSON Prompt

- "Extract: name, email, age. Return JSON."
- Schema in prompt or via API option
- Reliable on modern models

---

## Function Calling

- Define functions with schemas
- Model picks one and supplies args
- Standardised in OpenAI, Anthropic, etc.
- Better than free-text JSON

---

## Sample Function Schema

- name: get_weather
- params: city (string), units (enum)
- description: "Returns current weather"
- Model emits: name + args

---

## JSON Schema

- Standard schema language
- Types, enums, required fields
- Provide to API; backend enforces
- Best practice today

---

## Strict Mode

- Some APIs guarantee schema conformance
- No invalid JSON returned
- Use when available

---

## Validation

- Always validate output server-side
- Models can drift
- Reject and retry on schema fail
- Don't trust the API alone

---

## Parsing

- Most standard libraries handle JSON fine
- Complex nested: write a Pydantic / TypeScript model
- Reuse for type safety

---

## Failure Modes

- Truncated JSON (context limit)
- Trailing prose
- Wrong types
- Hallucinated fields

---

## Recovering

- Detect parse errors
- Retry with stricter prompt
- Add "JSON only, no commentary"
- Eventually fall back to error

---

## Streaming Structured Output

- Partial JSON arrives over time
- Parse as incremental
- Useful for UIs
- Library support varies

---

## Common Structured-Output Mistakes

- Free-text + regex parsing
- No schema validation; trusting model
- Embedding instructions inside data fields
- One huge object instead of multiple calls
- Ignoring streamed partial-output edge cases
