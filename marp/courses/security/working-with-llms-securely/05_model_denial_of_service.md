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

```output
Attacker sends a very long input:

"Repeat the following word 10000 times: supercalifragil
isticexpialidocious. Then for each repetition, explain
its etymology in detail. Then translate each explanation
into 50 different languages..."

Result: Massive token generation, high compute cost
```

---

## Attack Vector: Recursive Expansion

```output
"Generate a story. For each sentence in the story,
generate a sub-story. For each sentence in each
sub-story, generate another sub-story. Continue
this process 10 levels deep."

Result: Exponential output growth
```

---

## Financial Impact

```output
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

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="230" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555555"/>
    </marker>
  </defs>
  <rect x="10"  y="30" width="155" height="70" fill="#fce4ec" stroke="#c62828" stroke-width="1.5" rx="4"/>
  <text x="87"  y="52" text-anchor="middle" font-size="12" font-weight="bold" fill="#222222">Incoming Requests</text>
  <text x="87"  y="70" text-anchor="middle" font-size="11" fill="#555555">High volume /</text>
  <text x="87"  y="87" text-anchor="middle" font-size="11" fill="#555555">complex prompts</text>
  <line x1="165" y1="65" x2="210" y2="65" stroke="#555555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="212" y="30" width="175" height="70" fill="#e3f2fd" stroke="#333333" stroke-width="1.5" rx="4"/>
  <text x="299" y="52" text-anchor="middle" font-size="12" font-weight="bold" fill="#222222">Queue</text>
  <text x="299" y="70" text-anchor="middle" font-size="11" fill="#333333">Priority + Limit</text>
  <text x="299" y="87" text-anchor="middle" font-size="11" fill="#333333">Max depth + Timeout</text>
  <line x1="387" y1="65" x2="432" y2="65" stroke="#555555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="434" y="30" width="175" height="70" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
  <text x="521" y="52" text-anchor="middle" font-size="12" font-weight="bold" fill="#222222">LLM Workers</text>
  <text x="521" y="70" text-anchor="middle" font-size="11" fill="#333333">Worker pool</text>
  <text x="521" y="87" text-anchor="middle" font-size="11" fill="#333333">Rate-limited</text>
  <rect x="10" y="120" width="600" height="100" fill="#fff9c4" stroke="#f9a825" stroke-width="1.5" rx="4"/>
  <text x="310" y="140" text-anchor="middle" font-size="12" font-weight="bold" fill="#e65100">Mitigations</text>
  <text x="30"  y="160" font-size="12" fill="#333333">• Priority queuing — paying / trusted users served first</text>
  <text x="30"  y="178" font-size="12" fill="#333333">• Maximum queue depth — reject when overloaded</text>
  <text x="30"  y="196" font-size="12" fill="#333333">• Request timeout in queue  • Graceful degradation under load</text>
</svg>

---

## Key Takeaways

- `LLM` `DoS` can cause both **service outages** and **financial damage**
- Implement **rate limiting** at multiple levels
- Set **hard limits** on input and output token counts
- Monitor **costs** with automated alerts and spending caps
- Use **queuing** and **graceful degradation** under load
