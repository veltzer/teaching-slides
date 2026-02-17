# LLM08: Excessive Agency
## Mark Veltzer
### Senior Software Engineer

---

## What Is Excessive Agency?

Excessive agency occurs when an `LLM`-based system is granted **too much autonomy, functionality, or privilege**, allowing it to take harmful actions based on unexpected or malicious outputs

- Ranked **#8** in the OWASP Top 10 for LLM Applications
- Combines three root causes:
    - **Excessive functionality**: the `LLM` has access to tools it does not need
    - **Excessive permissions**: tools operate with more privilege than required
    - **Excessive autonomy**: the `LLM` acts without human oversight

Key insight: even without prompt injection, `LLMs` hallucinate and make mistakes. Excessive agency turns those mistakes into **real-world damage**.

---

## Why Excessive Agency Is Dangerous

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ea1" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
  </defs>
  <rect x="50" y="40" width="200" height="60" fill="#3498db" rx="8"/>
  <text x="150" y="65" text-anchor="middle" fill="white" font-size="12" font-weight="bold">LLM hallucinates</text>
  <text x="150" y="82" text-anchor="middle" fill="white" font-size="11">or is prompt-injected</text>
  <line x1="250" y1="70" x2="340" y2="70" stroke="#333" stroke-width="2" marker-end="url(#ea1)"/>
  <rect x="350" y="40" width="200" height="60" fill="#e67e22" rx="8"/>
  <text x="450" y="65" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Decides to call tool</text>
  <text x="450" y="82" text-anchor="middle" fill="white" font-size="11">No approval needed</text>
  <line x1="550" y1="70" x2="640" y2="70" stroke="#333" stroke-width="2" marker-end="url(#ea1)"/>
  <rect x="650" y="20" width="130" height="45" fill="#e74c3c" rx="8"/>
  <text x="715" y="48" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Deletes data</text>
  <rect x="650" y="75" width="130" height="45" fill="#e74c3c" rx="8"/>
  <text x="715" y="103" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Sends emails</text>
  <rect x="650" y="130" width="130" height="45" fill="#e74c3c" rx="8"/>
  <text x="715" y="158" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Transfers funds</text>
  <line x1="550" y1="70" x2="640" y2="42" stroke="#333" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="550" y1="70" x2="640" y2="152" stroke="#333" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="400" y="230" text-anchor="middle" fill="#c0392b" font-size="13" font-weight="bold">Without human oversight, an incorrect LLM decision causes irreversible harm</text>
</svg>

---

## The Three Dimensions of Excessive Agency

```text
1. EXCESSIVE FUNCTIONALITY
   Agent has tools it doesn't need
   Example: A Q&A bot with access to delete_user()

2. EXCESSIVE PERMISSIONS
   Tools operate with overly broad privileges
   Example: A read-only task using a read-write DB credential

3. EXCESSIVE AUTONOMY
   Actions execute without human confirmation
   Example: Agent sends production emails without approval
```

All three must be addressed. Fixing only one still leaves the system vulnerable.

---

## Real-World Scenario: The Overpowered Assistant

```python
# VULNERABLE: Agent has unnecessary and dangerous tools
agent_tools = [
    search_documents,       # Needed
    summarize_text,         # Needed
    send_email,             # NOT needed for Q&A
    delete_database_record, # NOT needed for Q&A
    execute_shell_command,  # Definitely NOT needed
    modify_user_account,    # NOT needed for Q&A
]

agent = create_agent(
    model="gpt-4",
    tools=agent_tools,   # All tools available!
    system_prompt="You are a document Q&A assistant.",
)
```

The agent only needs `search_documents` and `summarize_text`, but has access to **six tools** including shell execution and database deletion

---

## Principle of Least Functionality

Grant the `LLM` agent access to **only the tools it actually needs**

```python
from dataclasses import dataclass

@dataclass
class AgentProfile:
    name: str
    description: str
    allowed_tools: set[str]

AGENT_PROFILES = {
    "qa-bot": AgentProfile(
        name="Document Q&A",
        description="Answers questions from documents",
        allowed_tools={"search_documents", "summarize_text"},
    ),
    "support-bot": AgentProfile(
        name="Customer Support",
        description="Handles support tickets",
        allowed_tools={
            "search_kb", "get_ticket", "update_ticket",
        },
    ),
}

def build_agent(profile_name: str):
    profile = AGENT_PROFILES[profile_name]
    tools = [TOOL_REGISTRY[t] for t in profile.allowed_tools]
    return create_agent(tools=tools)
```

---

## Principle of Least Privilege for Tools

Even when a tool is needed, it should operate with **minimal permissions**

```python
# BAD: Tool connects with full admin privileges
def search_documents(query: str) -> list[str]:
    db = connect(user="admin", password=ADMIN_PW)
    return db.execute(f"SELECT * FROM docs WHERE ...")

# GOOD: Tool connects with read-only, scoped credentials
def search_documents(query: str) -> list[str]:
    db = connect(
        user="readonly_docs_user",
        password=READONLY_PW,
        database="public_docs",   # Scoped to one DB
        options="--default-transaction-read-only=on",
    )
    return db.execute(
        "SELECT title, snippet FROM docs WHERE ...",
    )
```

If the `LLM` is tricked into generating a `DROP TABLE` statement, the read-only connection will **reject it at the database level**

---

## Human-in-the-Loop: Why It Matters

`LLMs` are **non-deterministic** and can produce unexpected outputs even without adversarial input

- A hallucinated function argument could delete the wrong record
- A misunderstood user request could trigger an irreversible action
- A prompt injection could redirect actions to the attacker's benefit

Human-in-the-loop means requiring a **human to review and approve** actions before they execute, especially for:

- Actions that modify or delete data
- Actions that communicate externally (email, SMS, API calls)
- Actions involving money, credentials, or personal data
- Any action that cannot be easily undone

---

## Implementing Human-in-the-Loop Approval

```python
from enum import Enum

class ActionRisk(Enum):
    LOW = "low"       # Auto-execute
    MEDIUM = "medium" # Log, then execute
    HIGH = "high"     # Require human approval

TOOL_RISK_LEVELS = {
    "search_documents": ActionRisk.LOW,
    "summarize_text": ActionRisk.LOW,
    "update_ticket": ActionRisk.MEDIUM,
    "send_email": ActionRisk.HIGH,
    "delete_record": ActionRisk.HIGH,
    "modify_account": ActionRisk.HIGH,
}

def execute_with_approval(tool_name: str, args: dict):
    risk = TOOL_RISK_LEVELS.get(tool_name, ActionRisk.HIGH)
    if risk == ActionRisk.HIGH:
        approval = request_human_approval(
            tool=tool_name, arguments=args,
        )
        if not approval.granted:
            return f"Action denied: {approval.reason}"
    return TOOL_REGISTRY[tool_name](**args)
```

---

## Approval Workflow Architecture

<svg viewBox="0 0 800 340" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ea2" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
  </defs>
  <rect x="300" y="10" width="200" height="40" fill="#2c3e50" rx="8"/>
  <text x="400" y="35" text-anchor="middle" fill="white" font-size="12" font-weight="bold">LLM proposes action</text>
  <line x1="400" y1="50" x2="400" y2="75" stroke="#333" stroke-width="2" marker-end="url(#ea2)"/>
  <rect x="280" y="80" width="240" height="40" fill="#8e44ad" rx="8"/>
  <text x="400" y="105" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Risk classifier evaluates action</text>
  <line x1="300" y1="120" x2="150" y2="155" stroke="#27ae60" stroke-width="2" marker-end="url(#ea2)"/>
  <line x1="500" y1="120" x2="650" y2="155" stroke="#e74c3c" stroke-width="2" marker-end="url(#ea2)"/>
  <text x="200" y="145" fill="#27ae60" font-size="11" font-weight="bold">LOW risk</text>
  <text x="580" y="145" fill="#e74c3c" font-size="11" font-weight="bold">HIGH risk</text>
  <rect x="50" y="160" width="200" height="40" fill="#27ae60" rx="8"/>
  <text x="150" y="185" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Auto-execute</text>
  <rect x="550" y="160" width="200" height="40" fill="#e67e22" rx="8"/>
  <text x="650" y="185" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Queue for human review</text>
  <line x1="650" y1="200" x2="650" y2="230" stroke="#333" stroke-width="2" marker-end="url(#ea2)"/>
  <rect x="530" y="235" width="100" height="35" fill="#27ae60" rx="8"/>
  <text x="580" y="257" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Approve</text>
  <rect x="660" y="235" width="100" height="35" fill="#e74c3c" rx="8"/>
  <text x="710" y="257" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Deny</text>
  <line x1="580" y1="270" x2="580" y2="295" stroke="#27ae60" stroke-width="2" marker-end="url(#ea2)"/>
  <rect x="480" y="295" width="200" height="35" fill="#2c3e50" rx="8"/>
  <text x="580" y="317" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Execute action</text>
  <line x1="710" y1="270" x2="710" y2="295" stroke="#e74c3c" stroke-width="2" marker-end="url(#ea2)"/>
  <rect x="680" y="295" width="100" height="35" fill="#95a5a6" rx="8"/>
  <text x="730" y="317" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Reject</text>
</svg>

---

## Building an Approval Queue

```python
import uuid
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class PendingAction:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tool_name: str = ""
    arguments: dict = field(default_factory=dict)
    requested_at: datetime = field(default_factory=datetime.utcnow)
    user_context: str = ""
    status: str = "pending"  # pending | approved | denied

class ApprovalQueue:
    def __init__(self):
        self.queue: dict[str, PendingAction] = {}

    def submit(self, tool_name: str, args: dict,
               context: str) -> str:
        action = PendingAction(
            tool_name=tool_name,
            arguments=args,
            user_context=context,
        )
        self.queue[action.id] = action
        notify_reviewer(action)
        return action.id

    def decide(self, action_id: str, approved: bool):
        action = self.queue[action_id]
        action.status = "approved" if approved else "denied"
        if approved:
            TOOL_REGISTRY[action.tool_name](**action.arguments)
```

---

## Rate Limiting and Action Budgets

Even for auto-approved actions, impose **limits** to contain runaway agents

```python
from collections import defaultdict
import time

class ActionBudget:
    def __init__(self, max_actions: int = 20,
                 window_seconds: int = 300):
        self.max_actions = max_actions
        self.window = window_seconds
        self.history: dict[str, list[float]] = defaultdict(list)

    def check(self, session_id: str, tool_name: str):
        now = time.time()
        key = f"{session_id}:{tool_name}"
        recent = [
            t for t in self.history[key]
            if now - t < self.window
        ]
        if len(recent) >= self.max_actions:
            raise RateLimitError(
                f"Budget exceeded: {tool_name} called "
                f"{len(recent)} times in {self.window}s"
            )
        self.history[key] = recent + [now]

budget = ActionBudget(max_actions=10, window_seconds=60)
```

This prevents an `LLM` in a loop from calling the same tool hundreds of times

---

## Scope Boundaries: Limiting What Can Be Affected

Define explicit boundaries for what each action can touch

```python
@dataclass
class ActionScope:
    allowed_tables: set[str] = field(default_factory=set)
    allowed_record_ids: set[str] | None = None
    max_records_affected: int = 1
    allowed_recipients: list[str] = field(
        default_factory=list
    )

TOOL_SCOPES = {
    "update_ticket": ActionScope(
        allowed_tables={"tickets"},
        max_records_affected=1,
    ),
    "send_email": ActionScope(
        allowed_recipients=["*@company.com"],
    ),
}

def enforce_scope(tool_name: str, args: dict):
    scope = TOOL_SCOPES.get(tool_name)
    if scope and scope.max_records_affected:
        affected = estimate_affected_records(tool_name, args)
        if affected > scope.max_records_affected:
            raise ScopeError(
                f"Would affect {affected} records, "
                f"limit is {scope.max_records_affected}"
            )
```

---

## Reversibility: Prefer Undoable Actions

Design tools so that actions can be **rolled back** if they turn out to be wrong

```python
class ReversibleAction:
    def __init__(self, tool_name: str, args: dict):
        self.tool_name = tool_name
        self.args = args
        self.undo_info = None

    def execute(self):
        # Capture state before the action
        self.undo_info = capture_current_state(
            self.tool_name, self.args
        )
        return TOOL_REGISTRY[self.tool_name](**self.args)

    def rollback(self):
        if self.undo_info is None:
            raise ValueError("No undo info captured")
        restore_state(self.undo_info)

# Instead of hard-deleting, use soft delete
def delete_record(record_id: str):
    db.execute(
        "UPDATE records SET deleted_at = NOW() WHERE id = %s",
        (record_id,),
    )  # Can be reversed by setting deleted_at = NULL
```

---

## Audit Logging for Agent Actions

Every action an `LLM` agent takes should be **logged immutably** for forensic analysis

```python
import json
import logging

audit_log = logging.getLogger("agent_audit")

def log_agent_action(session_id: str,
                     tool_name: str,
                     args: dict,
                     result: str,
                     approved_by: str | None = None):
    audit_log.info(json.dumps({
        "session_id": session_id,
        "tool": tool_name,
        "arguments": args,
        "result_summary": result[:500],
        "approved_by": approved_by,
        "auto_approved": approved_by is None,
        "timestamp": datetime.utcnow().isoformat(),
    }))
```

Audit logs answer: **who** authorized the action, **what** the `LLM` intended, and **what** actually happened

---

## Putting It All Together

```python
def agent_execute(session_id: str, tool_name: str,
                  args: dict, agent_profile: str):
    profile = AGENT_PROFILES[agent_profile]
    # 1. Check tool is allowed for this agent
    if tool_name not in profile.allowed_tools:
        raise PermissionError(f"Tool not allowed: {tool_name}")
    # 2. Enforce scope boundaries
    enforce_scope(tool_name, args)
    # 3. Check rate limit / action budget
    budget.check(session_id, tool_name)
    # 4. Determine risk and get approval if needed
    risk = TOOL_RISK_LEVELS.get(tool_name, ActionRisk.HIGH)
    approved_by = None
    if risk == ActionRisk.HIGH:
        approval = request_human_approval(tool_name, args)
        if not approval.granted:
            return f"Denied: {approval.reason}"
        approved_by = approval.reviewer
    # 5. Execute with rollback support
    action = ReversibleAction(tool_name, args)
    result = action.execute()
    # 6. Audit log
    log_agent_action(session_id, tool_name, args,
                     str(result), approved_by)
    return result
```

---

## Key Takeaways

- Excessive agency turns `LLM` mistakes and hallucinations into **real-world damage** by granting too much power without oversight
- Apply **least functionality**: only give the agent access to the tools it genuinely needs for its task
- Apply **least privilege**: each tool should use the minimum permissions required (read-only credentials, scoped access)
- Implement **human-in-the-loop** approval for high-risk actions like data modification, external communication, and financial operations
- Use **action budgets** and rate limits to prevent runaway agents from causing cascading damage
- Define **scope boundaries** to limit the blast radius of any single action
- Prefer **reversible actions** (soft deletes, staged changes) so mistakes can be undone
- Maintain **immutable audit logs** of every action the agent takes, including who approved it
