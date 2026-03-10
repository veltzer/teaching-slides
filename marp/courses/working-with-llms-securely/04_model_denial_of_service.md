# LLM04: Model Denial of Service
## Exhausting `LLM` Resources

---

## What is Model Denial of Service?

- Attacker crafts inputs that consume **excessive resources**
- Causes the `LLM` service to become **slow or unavailable**
- Exploits the **computational cost** of `LLM` inference
- Can lead to massive **financial costs** for pay-per-token services

---

## Why `LLMs` Are Vulnerable to `DoS`

- `LLM` inference is **computationally expensive**
- Cost scales with **input and output token count**
- No natural **upper bound** on processing complexity
- A single request can trigger **billions of operations**
- Unlike traditional `DoS`, even a **single request** can be devastating

---

## Attack Vector: Token Flooding

```text
Attacker sends a very long input:

"Repeat the following word 10000 times: supercalifragil
isticexpialidocious. Then for each repetition, explain
its etymology in detail. Then translate each explanation
into 50 different languages..."

Result: Massive token generation, high compute cost
```

---

## Attack Vector: Recursive Expansion

```text
"Generate a story. For each sentence in the story,
generate a sub-story. For each sentence in each
sub-story, generate another sub-story. Continue
this process 10 levels deep."

Result: Exponential output growth
```

---

## Financial Impact

```text
Pay-per-token pricing example:

Normal request:   500 tokens  = $0.01
Attack request: 100,000 tokens = $2.00

1000 attack requests/hour = $2,000/hour

Automated attack over a weekend = $96,000+
```

Even without bringing the service down, costs can be ruinous

---

## Real-World Impact

- **Service degradation** for all users
- **Increased latency** across the platform
- **Cloud cost spikes** that blow through budgets
- **Cascading failures** in dependent systems
- **SLA violations** affecting business commitments

---

## Mitigation: Rate Limiting

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route("/api/chat")
@limiter.limit("10 per minute")  # Per-user rate limit
def chat():
    # Also limit by API key for authenticated users
    check_api_key_rate_limit(request.headers["X-API-Key"])
    return process_chat(request.json)
```

Apply rate limits per user, per `API` key, and globally

---

## Mitigation: Input Constraints

```python
MAX_INPUT_TOKENS = 4096
MAX_OUTPUT_TOKENS = 2048

def validate_request(request):
    input_text = request.json.get("message", "")
    token_count = tokenizer.count_tokens(input_text)

    if token_count > MAX_INPUT_TOKENS:
        return error("Input exceeds maximum token limit")

    if len(input_text) > 50000:  # Character limit
        return error("Input exceeds maximum length")

    return None  # Valid
```

---

## Mitigation: Output Constraints

```python
def generate_response(prompt):
    response = llm.generate(
        prompt,
        max_tokens=MAX_OUTPUT_TOKENS,
        stop_sequences=["\n\n\n"],  # Stop on excessive newlines
        timeout=30,  # 30-second timeout
    )
    return response
```

Always set **maximum output tokens** and **timeouts**

---

## Mitigation: Cost Monitoring and Alerts

```python
# Track costs per user
def track_usage(user_id, input_tokens, output_tokens):
    cost = calculate_cost(input_tokens, output_tokens)
    daily_total = redis.incrbyfloat(
        f"usage:{user_id}:{today()}", cost
    )

    if daily_total > DAILY_LIMIT:
        disable_user_access(user_id)
        alert_ops_team(f"User {user_id} exceeded daily limit")
```

Set per-user and global spending caps

---

## Mitigation: Request Queuing

```text
┌──────────┐     ┌─────────┐     ┌─────────┐
│ Incoming  │────►│  Queue   │────►│  LLM    │
│ Requests  │     │ (Priority│     │ Workers │
│           │     │  + Limit)│     │ (Pool)  │
└──────────┘     └─────────┘     └─────────┘

- Priority queuing (paying users first)
- Maximum queue depth
- Request timeout in queue
- Graceful degradation under load
```

---

## Key Takeaways

- `LLM` `DoS` can cause both **service outages** and **financial damage**
- Implement **rate limiting** at multiple levels
- Set **hard limits** on input and output token counts
- Monitor **costs** with automated alerts and spending caps
- Use **queuing** and **graceful degradation** under load
