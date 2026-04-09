# Tool Use and Function Calling

## Overview
- The tool-use pattern in LLMs
- Designing effective tools for AI agents
- Built-in tools in popular agents
- Building custom tools

---

## The Tool-Use Pattern

## Why Tools?
- LLMs generate text but cannot act on the world directly
- Tools bridge the gap between reasoning and execution
- The model decides **when** and **which** tool to call
- Results feed back into the conversation for further reasoning

---

## The Tool-Use Pattern

## Why Tools?

![why_tools](svg/courses/ai/advanced-ai-powered-development/04_tool_use_and_function_calling/why_tools.svg)

---

## Tool Definitions and Schemas

## Declaring Tools for the Model
- Tools are described as JSON schemas in the system/config layer
- The model never executes code; it emits a structured tool-call message

```json
{
  "name": "get_weather",
  "description": "Get current weather for a city",
  "input_schema": {
    "type": "object",
    "properties": {
      "city": { "type": "string" },
      "units": { "type": "string", "enum": ["celsius", "fahrenheit"] }
    },
    "required": ["city"]
  }
}
```

---

## Steering Tool Selection with Prompts

## Controlling Which Tools Get Called
- The `tool_choice` parameter controls model behavior
    - `"auto"` -- model decides freely (default)
    - `"any"` -- model must call at least one tool
    - `{"type": "tool", "name": "X"}` -- force a specific tool
- High-quality `description` fields drastically improve selection accuracy

## Writing Effective Tool Descriptions
- Be specific: `"Search Git log by author and date range"` beats `"Search logs"`
- Mention constraints: `"Returns max 50 results, sorted by date"`
- Describe when **not** to use the tool to reduce false positives

```json
{
  "tool_choice": {"type": "tool", "name": "search_code"},
  "tools": [{"name": "search_code",
    "description": "Regex search across the codebase. Use for finding definitions, references, or patterns. Do not use for reading full files."}]
}
```

---

## Tool Result Handling

## The Round-Trip
1. Model emits a `tool_use` content block with `name` and `input`
1. Your runtime executes the actual function
1. You return a `tool_result` message back to the model
1. Model incorporates the result into its next response

```json
{ "role": "assistant", "content": [
    { "type": "tool_use", "id": "call_01", "name": "get_weather",
      "input": { "city": "Tel Aviv" } }
]}
```

```json
{ "role": "user", "content": [
    { "type": "tool_result", "tool_use_id": "call_01",
      "content": "28°C, sunny" }
]}
```

---

## Multi-Turn Tool Conversations

## Chaining Multiple Calls
- A single user request may require several tool invocations
- The model decides autonomously which tools to call next
- Each tool result becomes context for subsequent reasoning
- Parallel tool calls are possible when inputs are independent

---

## Multi-Turn Tool Conversations

## Chaining Multiple Calls

![chaining_multiple_calls](svg/courses/ai/advanced-ai-powered-development/04_tool_use_and_function_calling/chaining_multiple_calls.svg)

---

## Parallel Tool Calls

## Fan-Out Execution
- A model can emit multiple `tool_use` blocks in one response
- The runtime executes them concurrently and returns all results at once
- Reduces latency when tool calls are independent of each other

```json
{ "role": "assistant", "content": [
    { "type": "tool_use", "id": "call_01", "name": "read_file",
      "input": { "path": "src/auth.ts" } },
    { "type": "tool_use", "id": "call_02", "name": "read_file",
      "input": { "path": "src/config.ts" } },
    { "type": "tool_use", "id": "call_03", "name": "grep",
      "input": { "pattern": "TODO", "path": "src/" } }
]}
```

## When to Use Parallel Calls
- Reading multiple files that the model needs simultaneously
- Running independent searches or lookups
- Fetching data from unrelated APIs in a single turn

---

## Designing Effective Tools

## Tool Granularity
- **Too coarse**: one tool does everything, hard to compose
- **Too fine**: many tiny tools, wastes context and turns
- Aim for single-responsibility tools that compose well

| Granularity | Example | Tradeoff |
|---|---|---|
| Too coarse | `manage_database(action, ...)` | Ambiguous, error-prone |
| Too fine | `open_file`, `seek_file`, `read_byte` | Too many round-trips |
| Right | `read_file(path, offset?, limit?)` | Clear, composable |

---

## Tool Composition Patterns

## Chaining Tools into Pipelines
- Tools can be composed sequentially: output of one feeds the next
- The model acts as the orchestrator between pipeline stages
- Common patterns: read-transform-write, search-analyze-act

---

## Tool Composition Patterns

## Chaining Tools into Pipelines

![chaining_tools_into_pipelines](svg/courses/ai/advanced-ai-powered-development/04_tool_use_and_function_calling/chaining_tools_into_pipelines.svg)

---

## Tool Composition Patterns

## Orchestration Strategies
- **Sequential**: each step depends on the previous result
- **Fan-out/fan-in**: parallel reads, then aggregate and act
- **Conditional**: branch based on tool output (e.g., skip if tests pass)

---

## Input/Output Schema Design

## Best Practices
- Use descriptive `description` fields on every property
- Prefer enums over free-form strings where possible
- Keep required parameters minimal; use sensible defaults
- Return structured data, not raw dumps

```json
{
  "name": "search_code",
  "description": "Search codebase using regex",
  "input_schema": {
    "type": "object",
    "properties": {
      "pattern": { "type": "string", "description": "Regex pattern" },
      "path": { "type": "string", "description": "Directory scope" },
      "max_results": { "type": "integer", "default": 10 }
    },
    "required": ["pattern"]
  }
}
```

---

## Managing Context Window with Tool Output

## The Problem
- Tool results consume context tokens alongside the conversation
- Large file reads or verbose API responses can exhaust the window
- The model loses access to earlier context as tokens accumulate

## Mitigation Strategies
1. **Truncation**: cap tool output at a fixed token limit
1. **Summarization**: post-process results before returning to the model
1. **Pagination**: return a page of results with a `next_cursor` field
1. **Selective fields**: return only the fields the model requested

```python
def truncate_result(content: str, max_chars: int = 8000) -> str:
    if len(content) <= max_chars:
        return content
    return content[:max_chars] + "\n... [truncated]"
```

---

## Error Handling and Feedback

## Giving the Model Useful Errors
- Return structured errors, not stack traces
- Include actionable hints so the model can self-correct
- Distinguish user errors from system failures

```json
{
  "is_error": true,
  "content": "File not found: src/auth.ts. Did you mean src/lib/auth.ts?"
}
```

## Key Principles
- Never silently swallow failures
- Suggest alternatives when a tool call is invalid
- Rate-limit or reject dangerous operations explicitly

---

## Security, Sandboxing, and Permissions

## Permission Models
- Define an **allow-list** of permitted tools per session or user role
- Sensitive tools (shell, file write) require explicit user approval
- Enforce **least-privilege**: only expose tools the task actually needs

## Sandboxed Execution
- Run shell tools inside containers or VMs with restricted access
- Apply filesystem scoping: tools can only read/write within a project root
- Network policies prevent tools from reaching internal services

---

## Security, Sandboxing, and Permissions

![sandboxed_execution](svg/courses/ai/advanced-ai-powered-development/04_tool_use_and_function_calling/sandboxed_execution.svg)

---

## Idempotency and Safety

## Designing for Repeated Calls
- Tools may be retried on failure or called redundantly
- **Idempotent** tools produce the same result on repeated calls
- Guard destructive operations with confirmation or dry-run modes

```python
def delete_resource(resource_id: str, dry_run: bool = False) -> dict:
    resource = db.find(resource_id)
    if resource is None:
        return {"status": "not_found"}  # idempotent
    if dry_run:
        return {"status": "would_delete", "resource": resource}
    db.delete(resource_id)
    return {"status": "deleted"}
```

- Prefer `edit` (patch) over `write` (full overwrite) for files
- Log every tool invocation for auditability

---

## Built-in Tools: File Operations

## Common File Tools in AI Agents
- `read_file(path, offset?, limit?)` -- read file contents
- `write_file(path, content)` -- create or overwrite a file
- `edit_file(path, old_string, new_string)` -- surgical text replacement
- `glob(pattern)` -- find files by name pattern
- `grep(pattern, path?, type?)` -- search file contents with regex

```python
# Typical edit tool flow
result = edit_file(
    path="/app/server.py",
    old_string="DEBUG = True",
    new_string="DEBUG = False",
)
# Returns confirmation or error if old_string not found
```

---

## Built-in Tools: Shell, Web, LSP

## Shell Execution
- Run arbitrary commands: build, test, deploy
- Capture `stdout`, `stderr`, and exit code
- Apply timeouts and sandboxing for safety

## Web Search and Fetch
- `web_search(query)` -- retrieve search results
- `web_fetch(url)` -- download page content as markdown
- Essential for up-to-date information beyond training data

## LSP Integration
- Go-to-definition, find references, rename symbol
- Gives the agent IDE-level code intelligence
- Reduces hallucination on symbol names and types

---

## Tool Discovery and Registration

## Dynamic Tool Loading
- Tools can be registered at runtime rather than hardcoded at startup
- MCP servers advertise capabilities via `tools/list` endpoint
- Agents discover available tools and adapt their behavior accordingly

## Capability Negotiation
- Agent queries the registry for tools matching the current task
- New tools can be hot-loaded without restarting the agent
- Tool metadata includes version, permissions, and rate limits

```python
# Dynamic tool registration
registry = ToolRegistry()
registry.register(
    name="query_database",
    handler=db_query_handler,
    schema=db_query_schema,
    permissions=["db:read"],
)
# Agent discovers tools at runtime
available = registry.list_tools(role="developer")
```

---

## Building Custom Tools

## Tool Definition Formats
- OpenAI/Anthropic: JSON Schema under `tools[]`
- MCP (Model Context Protocol): standardized tool discovery
- LangChain/LlamaIndex: Python decorators

```python
# MCP-style tool definition (Python SDK)
from mcp.server import Server
app = Server("my-tools")

@app.tool()
async def query_jira(issue_key: str) -> str:
    """Fetch a Jira issue by key."""
    issue = await jira_client.get(issue_key)
    return f"{issue.key}: {issue.summary} [{issue.status}]"
```

---

## Implementing Tool Handlers

## Anatomy of a Handler

```python
async def handle_tool_call(name: str, input: dict) -> dict:
    match name:
        case "query_jira":
            return await query_jira(**input)
        case "create_ticket":
            return await create_ticket(**input)
        case _:
            return {"is_error": True, "content": f"Unknown tool: {name}"}
```

## Guidelines
- Validate inputs before execution
- Wrap external calls in try/except and return structured errors
- Keep handlers stateless when possible
- Add logging and metrics for observability

---

## Debugging Tool Calls

## Inspecting Request and Response
- Log the full `tool_use` block (name, input, id) on every call
- Log the `tool_result` with timing and status
- Use structured logging (JSON) for easy filtering and search

```python
import logging, time
async def debug_wrapper(name: str, input: dict) -> dict:
    start = time.time()
    logging.info({"event": "tool_call", "name": name, "input": input})
    result = await handle_tool_call(name, input)
    elapsed = time.time() - start
    logging.info({"event": "tool_result", "name": name,
                  "elapsed_ms": int(elapsed * 1000),
                  "is_error": result.get("is_error", False)})
    return result
```

## Common Failure Modes
- Schema mismatch: model sends unexpected field types
- Timeout: external API takes too long to respond
- Auth expiry: tokens or keys have expired mid-session

---

## Tool Performance and Caching

## Caching Strategies
- Cache tool results keyed by `(tool_name, input_hash)`
- Use short TTLs for volatile data (API calls) and longer for stable data (file reads)
- Invalidate cache on known mutations (e.g., after `edit_file`)

## Rate Limiting
- Apply per-tool rate limits to protect downstream services
- Return `429`-style errors with retry hints so the model can back off

## Latency Optimization
- Use connection pooling for HTTP-based tools
- Batch multiple small queries into a single tool call where possible
- Set aggressive timeouts and return partial results on expiry

---

## Streaming Tool Results

## Handling Long-Running Tools
- Some tools (builds, deployments, large searches) take minutes
- Stream intermediate output so the model and user see progress
- Use a `status` field to indicate completion state

```python
async def stream_shell(command: str):
    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE)
    async for line in process.stdout:
        yield {"status": "running", "output": line.decode()}
    code = await process.wait()
    yield {"status": "complete", "exit_code": code}
```

## Progress Updates
- Report percentage or stage for multi-step operations
- Allow the model to cancel a tool call if early output shows an error
- Buffer streamed output and return a final summary to the model

---

## Production Architecture for Tool-Use Systems

## System Components

![system_components](svg/courses/ai/advanced-ai-powered-development/04_tool_use_and_function_calling/system_components.svg)

---

## Production Architecture for Tool-Use Systems

## Key Concerns
- **API Gateway**: rate limiting, request validation, routing
- **Registry**: tool catalog with schemas and versioning
- **Auth**: per-tool permission checks and token management
- **Logger**: full audit trail of every tool invocation and result

---

## Testing Tools with AI Agents

## Strategies
1. **Unit tests**: validate handler logic in isolation
1. **Schema validation**: ensure inputs/outputs match declared schemas
1. **Simulation tests**: feed synthetic tool calls and assert results
1. **End-to-end**: run the full agent loop against a staging environment

```python
def test_query_jira_not_found():
    result = await handle_tool_call("query_jira", {"issue_key": "FAKE-999"})
    assert result["is_error"] is True
    assert "not found" in result["content"]

def test_schema_compliance():
    schema = load_tool_schema("query_jira")
    jsonschema.validate({"issue_key": "PROJ-123"}, schema["input_schema"])
```

---

## Tool Versioning Strategies

## Backward Compatibility
- New versions add optional fields; never remove or rename required ones
- Support multiple versions concurrently during migration periods
- Include a `version` field in tool schemas for explicit negotiation

## Deprecation and Migration
1. Mark deprecated tools with a warning in the `description` field
1. Log usage of deprecated tools to track migration progress
1. Set a sunset date and remove after all consumers have migrated

```json
{
  "name": "search_code_v1",
  "description": "[DEPRECATED: use search_code_v2] Regex search across the codebase.",
  "input_schema": { "type": "object", "properties": {
    "pattern": { "type": "string" } }, "required": ["pattern"] }
}
```

---

## Cross-Platform Tool Compatibility

## Making Tools Work Across Different AI Agents
- Each provider has slightly different schema conventions
- Abstract tool definitions into a shared format and generate per-platform schemas
- MCP provides a vendor-neutral protocol for tool interoperability

## Adapter Pattern

```python
class ToolAdapter:
    def to_openai(self, tool_def: dict) -> dict:
        return {"type": "function", "function": {
            "name": tool_def["name"],
            "description": tool_def["description"],
            "parameters": tool_def["input_schema"]}}

    def to_anthropic(self, tool_def: dict) -> dict:
        return {"name": tool_def["name"],
                "description": tool_def["description"],
                "input_schema": tool_def["input_schema"]}
```

- Test each adapter against the target provider's validation endpoint
- Keep a conformance test suite that runs across all supported platforms

---

## Versioning and Maintaining Tools

## Evolution Without Breaking Agents
- Add new optional parameters; never remove required ones
- Use semantic versioning for tool packages
- Deprecate old tools gracefully with warnings in descriptions
- Monitor tool call success rates and latency

---

## Versioning and Maintaining Tools

## Evolution Without Breaking Agents

![evolution_without_breaking_agents](svg/courses/ai/advanced-ai-powered-development/04_tool_use_and_function_calling/evolution_without_breaking_agents.svg)

---

## Hands-On: Building a Custom Tool End-to-End

## Exercise: Build a `query_logs` Tool
1. Define the JSON schema with `service`, `level`, `since`, and `limit` parameters
1. Implement the handler that queries an Elasticsearch backend
1. Add input validation, error handling, and structured output
1. Register the tool and test it with a live agent

```python
LOG_TOOL_SCHEMA = {
    "name": "query_logs",
    "description": "Search application logs by service and severity level",
    "input_schema": {
        "type": "object",
        "properties": {
            "service": {"type": "string", "description": "Service name"},
            "level": {"type": "string", "enum": ["debug", "info", "warn", "error"]},
            "since": {"type": "string", "description": "ISO 8601 timestamp"},
            "limit": {"type": "integer", "default": 20}
        },
        "required": ["service"]
    }
}
```

## Steps
- Write the handler, add caching, then test with unit and integration tests

---

## Key Takeaways

## Summary
- Tool use turns LLMs from text generators into **autonomous agents**
- Good tool design follows single-responsibility, clear schemas, and idempotency
- Built-in tools (file, shell, web, LSP) cover most coding workflows
- Custom tools extend agents into your domain (Jira, DBs, APIs)
- Test tools rigorously and version them like any API contract
