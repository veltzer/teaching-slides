# Building Custom Agents

## Overview
- Agent design patterns and architectures
- Survey of major agent frameworks
- Implementing specialized development agents
- Managing agent memory and state
- Evaluating and testing agent systems

---

## What Is an Agent?

- An LLM-powered system that can **plan**, **act**, and **observe** in a loop
- Goes beyond single prompt-response: maintains goals across multiple steps
- Core loop: `Observe -> Think -> Act -> Observe ...`

![what_is_an_agent](/svg/courses/ai/advanced-ai-powered-development/09_building_custom_agents/what_is_an_agent.svg)

---

## Single-Turn vs Multi-Turn Agents

## Single-Turn
- One request, one response, no follow-up
- Stateless: each invocation is independent
- Good for: code formatting, linting, simple Q&A

## Multi-Turn
- Maintains conversation context across exchanges
- Tracks progress toward a goal over multiple steps
- Good for: debugging sessions, iterative refactoring, complex migrations

---

## Supervisor and Sub-Agent Architectures

- A **supervisor** agent orchestrates specialized **sub-agents**
- Each sub-agent has a narrow scope and its own tools
- Supervisor decides which sub-agent to delegate to

```python
from agents import Agent, Runner

code_reviewer = Agent(name="reviewer",
    instructions="Review code for bugs and style issues.")
test_writer = Agent(name="tester",
    instructions="Write unit tests for the given code.")

supervisor = Agent(name="supervisor",
    instructions="Delegate tasks to the right sub-agent.",
    handoffs=[code_reviewer, test_writer])

result = Runner.run_sync(supervisor, "Review and test utils.py")
```

---

## Parallel Agent Execution

- Run independent sub-agents concurrently for speed
- Use `asyncio` to fan out and gather results

```python
import asyncio
from agents import Agent, Runner

agents = [
    Agent(name="security", instructions="Check for vulnerabilities."),
    Agent(name="perf", instructions="Identify performance issues."),
    Agent(name="style", instructions="Check code style."),
]

async def parallel_review(code: str):
    tasks = [Runner.run(agent, code) for agent in agents]
    results = await asyncio.gather(*tasks)
    return {r.agent.name: r.final_output for r in results}
```

---

## Multi-Agent Communication Patterns

- Agents can collaborate through different coordination strategies

![multi_agent_communication_patterns](/svg/courses/ai/advanced-ai-powered-development/09_building_custom_agents/multi_agent_communication_patterns.svg)

- **Peer-to-peer**: agents pass messages directly via `handoffs`
- **Shared blackboard**: agents read/write to a common state store
- **Agent debate**: two agents argue opposing positions, a judge decides
    - Effective for code review: one agent defends, one critiques

---

## Agent Orchestration with Queues

- Decouple agent work from request handling with message queues
- Enables async processing, retries, and horizontal scaling

```python
import redis
import json

rq = redis.Redis()

# Producer: enqueue tasks
def submit_task(task: str, priority: int = 1):
    rq.lpush("agent_tasks", json.dumps(
        {"task": task, "priority": priority}))

# Worker: consume and process
def worker_loop(agent):
    while True:
        _, payload = rq.brpop("agent_tasks")
        task = json.loads(payload)
        result = Runner.run_sync(agent, task["task"])
        rq.hset("agent_results", task["task"],
                result.final_output)
```

- Use **dead-letter queues** for tasks that fail repeatedly
- Aggregate results with a collector that polls `agent_results`

---

## Tool Design Best Practices

- Tools are the agent's hands — well-designed tools lead to reliable agents
- Follow these principles for every tool you expose:

1. **Clear naming**: use verb-noun format like `read_file`, `run_tests`
    - Avoid ambiguous names like `process` or `handle`
1. **Right granularity**: one tool per atomic action
    - Prefer `search_code` + `read_file` over `search_and_read`
1. **Structured returns**: return JSON or typed objects, not free text
    - Include status, data, and error fields consistently
1. **Descriptive docstrings**: the LLM reads them to decide when to call

```python
@function_tool
def search_code(query: str, file_glob: str = "**/*.py",
                max_results: int = 10) -> str:
    """Search the codebase for lines matching a regex pattern.
    Returns matching file paths and line numbers.
    Use this before read_file to locate relevant code."""
    ...
```

- Always validate inputs and return clear error messages on failure

---

## Agent Error Handling and Recovery

- Agents will encounter failures — design for graceful recovery
- Common failure modes and mitigations:

| Failure | Mitigation |
|---|---|
| Tool returns an error | Retry with corrected args, or try alternative tool |
| Hallucinated tool name | Validate against registered tool list before execution |
| Infinite reasoning loop | Set `max_turns` limit, detect repeated outputs |
| Context window exceeded | Summarize history, drop older messages |

```python
from agents import Agent, Runner
from agents.exceptions import MaxTurnsExceeded

agent = Agent(name="resilient",
    instructions="""If a tool call fails, analyze the error
    and retry with corrected arguments. After 2 failures
    on the same tool, report the issue and move on.""")

try:
    result = Runner.run_sync(agent, task, max_turns=15)
except MaxTurnsExceeded:
    logger.warning("Agent hit turn limit, returning partial result")
```

---

## Human-in-the-Loop Patterns

- Agent pauses execution and requests human approval
- Critical for destructive actions: deployments, data mutations, refactors

```python
from agents import Agent, Runner
from agents.lifecycle import AgentHooks

class ApprovalHook(AgentHooks):
    async def before_tool_call(self, context, tool_name, args):
        if tool_name in ("deploy", "delete_branch"):
            answer = input(f"Approve {tool_name}({args})? [y/n] ")
            if answer != "y":
                raise PermissionError("User denied action")

agent = Agent(name="deployer",
    instructions="Deploy reviewed code.",
    hooks=ApprovalHook())
```

---

## Framework Comparison

| Framework | Strengths | Best For |
|---|---|---|
| `Anthropic Agent SDK` | Simple, native tool use | Claude-based agents |
| `LangGraph` | Stateful graphs, checkpoints | Complex workflows |
| `CrewAI` | Role-based collaboration | Multi-agent teams |
| `AutoGen` | Conversational agents | Research, debate |
| `OpenAI Agents SDK` | Handoffs, guardrails | OpenAI-based agents |

- Choose based on your LLM provider and orchestration needs
- All support tool calling, memory, and multi-agent patterns

---

## Guardrails and Safety Boundaries

- Protect agents from producing harmful outputs or runaway costs
- Apply validation at both input and output boundaries

```python
from agents import Agent
from agents.guardrails import InputGuardrail, OutputGuardrail

input_guard = InputGuardrail(
    instructions="Reject requests for credential access or system destruction.")

output_guard = OutputGuardrail(
    instructions="Block output containing secrets, API keys, or PII.")

agent = Agent(name="safe_agent",
    instructions="Assist with code tasks within safe boundaries.",
    input_guardrails=[input_guard],
    output_guardrails=[output_guard])
```

- **Cost caps**: set `max_turns` and `max_tokens` per session
- **Tool allowlists**: restrict which tools an agent can invoke at runtime
- **Rate limiting**: throttle tool calls to prevent API abuse

---

## Anthropic Agent SDK Basics

```python
from agents import Agent, Runner, function_tool

@function_tool
def read_file(path: str) -> str:
    """Read a file from disk."""
    with open(path) as f:
        return f.read()

@function_tool
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    with open(path, "w") as f:
        f.write(content)
    return f"Wrote {len(content)} bytes to {path}"

agent = Agent(name="file_editor",
    instructions="You edit files as requested.",
    tools=[read_file, write_file])

result = Runner.run_sync(agent, "Fix the typo in README.md")
```

---

## MCP Integration for Agents

- **Model Context Protocol** lets agents discover and call external tools dynamically
- Expose any API as an MCP server; agents connect as MCP clients

```python
from agents import Agent
from agents.mcp import MCPServerStdio

# Connect agent to an MCP server exposing database tools
db_server = MCPServerStdio(
    command="npx",
    args=["-y", "@modelcontextprotocol/server-postgres",
          "postgresql://localhost/mydb"])

agent = Agent(name="data_analyst",
    instructions="Query the database to answer questions.",
    mcp_servers=[db_server])

# Agent automatically discovers: query, list_tables, describe_table
```

- MCP servers provide tool schemas, so agents know argument types
- Swap backends without changing agent code — just point to a new server
- Combine multiple MCP servers to give agents cross-system capabilities

---

## LangGraph: Stateful Agent Workflows

```python
from langgraph.graph import StateGraph, MessagesState

def reviewer(state: MessagesState):
    # Call LLM to review code
    return {"messages": [review_result]}

def fixer(state: MessagesState):
    # Call LLM to fix issues found
    return {"messages": [fix_result]}

def should_fix(state: MessagesState) -> str:
    last = state["messages"][-1].content
    return "fix" if "ISSUE" in last else "done"

graph = StateGraph(MessagesState)
graph.add_node("review", reviewer)
graph.add_node("fix", fixer)
graph.add_edge("__start__", "review")
graph.add_conditional_edges("review", should_fix,
    {"fix": "fix", "done": "__end__"})
graph.add_edge("fix", "review")
app = graph.compile()
```

---

## Code Review Agent

```python
from agents import Agent, Runner, function_tool

@function_tool
def get_diff(pr_number: int) -> str:
    """Fetch the git diff for a pull request."""
    import subprocess
    return subprocess.check_output(
        ["gh", "pr", "diff", str(pr_number)]).decode()

review_agent = Agent(
    name="code_reviewer",
    instructions="""You are a senior code reviewer.
    Analyze diffs for: bugs, security issues, performance
    problems, and style violations.
    Provide actionable feedback with line references.""",
    tools=[get_diff],
)

result = Runner.run_sync(review_agent, "Review PR #142")
print(result.final_output)
```

---

## Test Generation Agent

```python
from agents import Agent, Runner, function_tool

@function_tool
def read_source(path: str) -> str:
    """Read source file to generate tests for."""
    with open(path) as f:
        return f.read()

@function_tool
def write_test(path: str, content: str) -> str:
    """Write generated test file."""
    with open(path, "w") as f:
        f.write(content)
    return f"Test written to {path}"

test_agent = Agent(
    name="test_generator",
    instructions="""Generate pytest tests with edge cases.
    Aim for high branch coverage. Use mocks for I/O.""",
    tools=[read_source, write_test],
)
```

---

## Hands-On: Build a Debugging Agent

**Exercise**: build an agent that diagnoses and fixes a failing test

1. Give the agent three tools:
    - `run_tests(path)`: executes `pytest` on the given file, returns output
    - `read_file(path)`: reads source or test file contents
    - `write_file(path, content)`: writes a proposed fix
1. Agent workflow:
    - Run the failing test to observe the error message
    - Read the relevant source file to understand the bug
    - Propose a minimal fix and write it to the file
    - Re-run the test to verify the fix passes
1. Add a **max iteration limit** of 5 to prevent infinite loops

```python
debug_agent = Agent(
    name="debugger",
    instructions="""You are a debugging agent.
    1. Run the failing test  2. Read the source
    3. Write a fix  4. Re-run to verify.
    Stop after the test passes or 5 attempts.""",
    tools=[run_tests, read_file, write_file])
```

---

## Documentation and Migration Agents

## Documentation Agent
- Reads source code and existing docs
- Generates or updates docstrings, API references, changelogs
- Validates that docs match current function signatures

## Migration Agent
- Analyzes codebase for deprecated patterns
- Applies transformation rules (e.g., Python 2 to 3, React class to hooks)
- Runs tests after each transformation to verify correctness

Key principle: **small, verifiable steps** with rollback capability

---

## Monitoring and Alerting Agents

- Agents that run continuously or on a schedule
- Watch logs, metrics, deployments for anomalies

```python
from agents import Agent, function_tool

@function_tool
def query_metrics(service: str, window: str) -> str:
    """Query Prometheus metrics for a service."""
    # Returns error rates, latency percentiles, etc.
    ...

@function_tool
def send_alert(channel: str, message: str) -> str:
    """Send alert to Slack channel."""
    ...

monitor = Agent(
    name="monitor",
    instructions="""Check error rates and latency.
    Alert if error rate > 1% or p99 > 500ms.
    Include root cause hypothesis in alerts.""",
    tools=[query_metrics, send_alert],
)
```

---

## Cost Management for Agent Systems

- Agents can consume tokens rapidly across multi-turn loops
- Implement budgets and routing to keep costs predictable

```python
class TokenBudget:
    def __init__(self, max_tokens: int):
        self.max_tokens = max_tokens
        self.used = 0

    def check(self, prompt_tokens: int) -> bool:
        if self.used + prompt_tokens > self.max_tokens:
            raise BudgetExceededError(
                f"Budget {self.max_tokens} exhausted")
        self.used += prompt_tokens
        return True
```

- **Model routing**: use a cheap model for simple tool calls, expensive model for reasoning
- **Early termination**: stop after N turns if no progress is detected
- **Caching**: store tool results to avoid redundant LLM calls
- Track cost per agent, per task type, per user in your observability stack

---

## Short-Term and Long-Term Memory

## Short-Term Memory
- Conversation history within a single session
- Managed automatically by the framework's message list
- Limited by context window size

## Long-Term Memory
- Persisted across sessions in a vector store or database
- Stores past decisions, user preferences, project conventions

```python
from agents import Agent

agent = Agent(
    name="assistant",
    instructions="""Check memory before answering.
    Store important decisions for future reference.""",
    tools=[search_memory, store_memory],
)
# Memory tools backed by a vector DB (e.g., ChromaDB)
```

---

## Project Knowledge Bases

- Agents perform better with project-specific context
- Index codebases, architecture docs, and ADRs into a retrieval system

```python
@function_tool
def search_codebase(query: str, top_k: int = 5) -> str:
    """Search project knowledge base."""
    import chromadb
    client = chromadb.PersistentClient(path="./kb")
    collection = client.get_collection("project_docs")
    results = collection.query(
        query_texts=[query], n_results=top_k)
    return "\n---\n".join(results["documents"][0])
```

- Include: coding standards, past PR reviews, incident reports
- Refresh the index on each merge to `main`

---

## Learning from Corrections

- Store human corrections as labeled training signals
- Use them to refine agent instructions over time

1. Agent produces output
1. Human corrects or rejects the output
1. Store the `(input, wrong_output, correction)` triple
1. Periodically update agent instructions with learned patterns

```python
@function_tool
def log_correction(task: str, agent_output: str,
                   correction: str) -> str:
    """Log a human correction for future learning."""
    db.insert({"task": task,
               "agent_output": agent_output,
               "correction": correction,
               "timestamp": datetime.now().isoformat()})
    return "Correction logged"
```

---

## Benchmarking Agent Performance

- Define a suite of tasks with known-good outputs
- Measure: accuracy, latency, cost, tool-call count

```python
import json

test_cases = [
    {"input": "Review utils.py", "expected_issues": ["null-check"]},
    {"input": "Write tests for auth.py", "expected_coverage": 0.85},
]

results = []
for case in test_cases:
    output = Runner.run_sync(agent, case["input"])
    score = evaluate(output.final_output, case)
    results.append({"case": case["input"], "score": score})

with open("benchmark_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

---

## Regression Testing for Agents

- Treat agent outputs like software: test them in CI
- Snapshot expected outputs, flag regressions on model or prompt changes

```python
# pytest test for agent behavior
def test_review_agent_finds_sql_injection():
    code = 'query = f"SELECT * FROM users WHERE id={user_id}"'
    result = Runner.run_sync(review_agent, f"Review:\n{code}")
    assert "sql injection" in result.final_output.lower()

def test_test_agent_generates_valid_python():
    result = Runner.run_sync(test_agent, "Test math_utils.py")
    # Verify generated code is syntactically valid
    compile(result.final_output, "<test>", "exec")
```

- Run with `pytest` on every PR that modifies agent prompts or tools

---

## Agent Testing Patterns

- Agents are non-deterministic — testing requires specific strategies
- Combine deterministic checks with LLM-as-judge evaluation

```python
import pytest
from unittest.mock import AsyncMock

# 1. Mock tools for isolation
@pytest.fixture
def mock_read_file():
    tool = AsyncMock(return_value="def add(a, b): return a - b")
    return tool

# 2. Use deterministic seeds where supported
agent = Agent(name="tester", model_settings={"seed": 42})

# 3. Golden test suites
GOLDEN = {"input": "Review add()", "must_contain": ["bug", "subtract"]}
def test_golden(mock_read_file):
    result = Runner.run_sync(agent, GOLDEN["input"])
    for keyword in GOLDEN["must_contain"]:
        assert keyword in result.final_output.lower()
```

- Pin model versions in CI to reduce flakiness
- Use `temperature=0` and `seed` for more reproducible outputs

---

## Monitoring Agents in Production

![monitoring_agents_in_production](/svg/courses/ai/advanced-ai-powered-development/09_building_custom_agents/monitoring_agents_in_production.svg)

- **Log every tool call**: inputs, outputs, latency, token usage
- **Trace conversations**: link multi-turn exchanges with a trace ID
- **Track cost**: monitor token spend per agent per task
- **Set guardrails**: max iterations, max tokens, timeout limits
- **Alert on drift**: flag sudden changes in output quality or cost

---

## Agent Observability with Tracing

- Full visibility into agent reasoning and tool calls across turns
- Essential for debugging failures and optimizing performance

```python
from langfuse import Langfuse
from langfuse.decorators import observe

langfuse = Langfuse()

@observe(name="agent-run")
def run_agent(task: str):
    # Each tool call is automatically traced
    result = Runner.run_sync(agent, task)
    langfuse.score(
        trace_id=langfuse.get_trace_id(),
        name="quality", value=evaluate(result))
    return result
```

- **Langfuse**: open-source tracing with scoring and datasets
- **Arize Phoenix**: real-time spans with LLM eval integration
- **OpenTelemetry**: vendor-neutral standard via `openinference`

---

## Deploying Agents to Production

- Agents need the same rigor as any production service
- Package agents as containerized services with health endpoints

```python
# Dockerfile
FROM python:3.12-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY agent_service/ /app/
WORKDIR /app
HEALTHCHECK CMD curl -f http://localhost:8000/health
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

- Use **horizontal scaling** behind a load balancer
- Set `readiness` probes that verify LLM API connectivity
- Store agent state externally (Redis, PostgreSQL) for stateless pods
- Deploy with rolling updates to avoid dropping active sessions

---

## Agent Configuration and Feature Flags

- Decouple agent behavior from deployment cycles
- Use feature flags to control rollout of new tools or prompts

```python
from flagsmith import Flagsmith

flags = Flagsmith(api_key="...")

def get_agent_config(user_id: str) -> dict:
    identity = flags.get_identity(user_id)
    return {
        "model": identity.get_feature_value("agent_model"),
        "max_turns": int(identity.get_feature_value("max_turns")),
        "enable_refactor_tool": identity.has_feature("refactor_tool"),
    }

config = get_agent_config("team-backend")
agent = Agent(name="assistant", model=config["model"],
    tools=base_tools + ([refactor] if config["enable_refactor_tool"] else []))
```

- Gradually roll out prompt changes to a percentage of users
- A/B test different model versions with real workloads

---

## Hands-On: Build a Multi-Agent Code Review System

**Exercise**: build a supervisor that delegates to specialized reviewers

1. Create three reviewer agents:
    - `security_reviewer`: checks for vulnerabilities, injection, secrets
    - `style_reviewer`: checks naming, formatting, complexity
    - `logic_reviewer`: checks correctness, edge cases, error handling
1. Create a `supervisor` agent that:
    - Receives a code diff as input
    - Delegates to all three reviewers in parallel
    - Aggregates findings into a unified review report
1. Add a `priority_classifier` tool that labels each finding as `critical`, `warning`, or `info`

```python
supervisor = Agent(name="review_supervisor",
    instructions="""Fan out the diff to all reviewers.
    Collect findings, classify priority, return a
    unified report sorted by severity.""",
    handoffs=[security_reviewer, style_reviewer, logic_reviewer])
```

- **Bonus**: add a `fix_proposer` agent that suggests patches for critical findings

---

## Key Takeaways

- Start with **single-turn agents**, evolve to multi-turn and multi-agent
- Use **supervisor/sub-agent** patterns for complex workflows
- Choose frameworks based on your LLM provider and orchestration needs
- Equip agents with **project-specific memory** for better outputs
- Treat agents like software: **benchmark, regression test, monitor**
- Always include **human-in-the-loop** for high-stakes actions
