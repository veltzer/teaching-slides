# LLM08: Excessive Agency
## When `LLMs` Do Too Much

---

## What is Excessive Agency?

- `LLM` is granted **too many capabilities** or **too much autonomy**
- The model takes **actions** beyond what is necessary or intended
- Insufficient **human oversight** over `LLM`-driven actions
- Amplifies the impact of other vulnerabilities like prompt injection

---

## Why Excessive Agency is Dangerous

```output
Prompt Injection alone:
  → LLM says something wrong

Prompt Injection + Excessive Agency:
  → LLM deletes your database
  → LLM sends emails on your behalf
  → LLM transfers money from your account
  → LLM modifies production configuration
```

Agency turns language manipulation into **real-world damage**

---

## Three Dimensions of Excessive Agency

![three_dimensions](svg/courses/security/working-with-llms-securely/09_excessive_agency/three_dimensions.svg)

---

## Three Dimensions of Excessive Agency Detail

| Dimension           | Description                          |
|---------------------|--------------------------------------|
| **Excessive Functionality** | Too many plugins/tools available |
| **Excessive Permissions**   | Tools have more access than needed |
| **Excessive Autonomy**      | Actions taken without human approval |

---

## Excessive Functionality

```python
# Too many tools available to the LLM
tools = [
    read_database,
    write_database,
    delete_database,      # Does the LLM need this?
    send_email,
    read_filesystem,
    write_filesystem,
    execute_shell_command, # Extremely dangerous!
    manage_users,          # Does the LLM need this?
    modify_permissions,    # Does the LLM need this?
]
```

Every available tool is a potential attack surface

---

## Excessive Permissions

```python
# LLM's database connection has full admin access
db_connection = connect(
    host="db.internal",
    user="admin",          # Full admin privileges!
    password="admin_pass",
    database="production"  # Direct production access!
)

# LLM only needs to READ product information
# but has permissions to DROP tables, DELETE data, etc.
```

---

## Excessive Autonomy

```python
# Dangerous: LLM acts without human approval
def handle_customer_request(message):
    action = llm.decide_action(message)

    if action.type == "refund":
        # Automatically processes refund!
        payment_api.refund(action.amount, action.customer_id)

    elif action.type == "delete_account":
        # Automatically deletes account!
        user_api.delete(action.customer_id)

    return action.response
```

No human reviews the `LLM`'s decision before execution

---

## Real-World Scenario: Auto-GPT Risks

```output
User: "Help me organize my files"

Auto-GPT chain of actions:
1. Reads all files in home directory ✓
2. Categorizes files ✓
3. Creates new folder structure ✓
4. Moves files to new locations ✓
5. Deletes "duplicate" files ✗ (data loss!)
6. Modifies system config "for optimization" ✗
7. Installs packages it "needs" ✗
```

Autonomous agents can escalate beyond intended scope

---

## Mitigation: Principle of Least Privilege

```python
# BEFORE: One connection with full access
tools = get_all_tools()

# AFTER: Only necessary tools with minimal permissions
tools = [
    ReadOnlyDatabaseTool(
        tables=["products", "faq"],
        max_rows=100
    ),
    CustomerResponseTool(
        max_length=500,
        templates_only=True
    ),
]
```

Grant only the **minimum capabilities** needed for the task

---

## Mitigation: Permission Boundaries

```python
def create_llm_db_connection(user_role: str):
    """Create a database connection with permissions
    matching the user's role, not the application's."""
    permissions = {
        "customer": {"tables": ["products", "faq"],
                     "operations": ["SELECT"]},
        "support":  {"tables": ["products", "orders"],
                     "operations": ["SELECT"]},
        "admin":    {"tables": ["*"],
                     "operations": ["SELECT", "UPDATE"]},
    }
    role_perms = permissions.get(user_role, {})
    return RestrictedDBConnection(**role_perms)
```

---

## Mitigation: Human-in-the-Loop

```python
def execute_action(action, user_session):
    # Classify action risk level
    risk = assess_risk(action)

    if risk == "low":
        # Auto-execute read-only actions
        return execute(action)

    elif risk == "medium":
        # Log and execute with notification
        log_action(action)
        notify_user(user_session, action)
        return execute(action)

    elif risk == "high":
        # Require explicit human approval
        approval = request_approval(user_session, action)
        if approval.granted:
            return execute(action)
        return "Action requires approval"
```

---

## Mitigation: Action Classification

| Risk Level | Examples                    | Control          |
|------------|-----------------------------|------------------|
| **Low**    | Read data, search, summarize | Auto-execute     |
| **Medium** | Send message, create record  | Log + notify     |
| **High**   | Delete data, send payment    | Human approval   |
| **Critical** | Modify permissions, admin ops | Block entirely |

---

## Mitigation: Audit Trail

```python
def log_llm_action(action):
    audit_entry = {
        "timestamp": datetime.utcnow(),
        "user_id": action.user_id,
        "session_id": action.session_id,
        "action_type": action.type,
        "parameters": action.params,
        "llm_reasoning": action.reasoning,
        "risk_level": action.risk,
        "outcome": action.result,
        "approved_by": action.approver,
    }
    audit_log.write(audit_entry)
```

Every `LLM`-initiated action should be logged for review

---

## Key Takeaways

- Excessive agency **amplifies** all other `LLM` vulnerabilities
- Apply the **principle of least privilege** to tools, data, and actions
- Implement **human-in-the-loop** controls for high-risk actions
- **Classify actions** by risk level and apply proportional controls
- Maintain a complete **audit trail** of all `LLM`-initiated actions
- The `LLM` should **never** have more permissions than the user
