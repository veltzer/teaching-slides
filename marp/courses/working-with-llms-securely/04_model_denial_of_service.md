# LLM04: Model Denial of Service
## Mark Veltzer
### Senior Software Engineer

---

## What Is Model Denial of Service?

Model Denial of Service (`MDoS`) targets `LLM` systems by consuming **excessive resources** to degrade or deny service to legitimate users

- Unlike traditional `DoS` attacks that flood network bandwidth, `MDoS` exploits the **computational cost of inference**
- Ranked **#4** in the OWASP Top 10 for LLM Applications
- A single crafted query can consume orders of magnitude more resources than a normal request

Key insight: `LLM` inference is **asymmetrically expensive** compared to the cost of sending a request

---

## Why LLMs Are Uniquely Vulnerable

<svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="40" width="160" height="70" fill="#e74c3c" rx="10"/>
  <text x="110" y="70" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Attacker</text>
  <text x="110" y="90" text-anchor="middle" fill="white" font-size="12">1 cheap request</text>
  <rect x="240" y="40" width="160" height="70" fill="#8e44ad" rx="10"/>
  <text x="320" y="70" text-anchor="middle" fill="white" font-size="14" font-weight="bold">LLM Service</text>
  <text x="320" y="90" text-anchor="middle" fill="white" font-size="12">GPU for 30+ seconds</text>
  <rect x="450" y="40" width="160" height="70" fill="#2c3e50" rx="10"/>
  <text x="530" y="70" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Other Users</text>
  <text x="530" y="90" text-anchor="middle" fill="white" font-size="12">Queued or denied</text>
  <line x1="190" y1="75" x2="240" y2="75" stroke="#333" stroke-width="2" marker-end="url(#dos1)"/>
  <line x1="400" y1="75" x2="450" y2="75" stroke="#c0392b" stroke-width="2" stroke-dasharray="5,5" marker-end="url(#dos1)"/>
  <defs>
    <marker id="dos1" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
  </defs>
  <text x="110" y="150" text-anchor="middle" fill="#333" font-size="12">Cost: ~$0.001</text>
  <text x="320" y="150" text-anchor="middle" fill="#c0392b" font-size="12">Cost: ~$0.50+ per query</text>
  <text x="530" y="150" text-anchor="middle" fill="#333" font-size="12">Service degraded</text>
  <text x="320" y="250" text-anchor="middle" fill="#c0392b" font-size="13" font-weight="bold">Asymmetric cost: attacker spends pennies, defender spends dollars</text>
</svg>

---

## LLM Inference Cost Factors

Understanding what makes `LLM` queries expensive helps identify attack vectors

| Factor | Impact on Cost | Attacker Control |
|--------|---------------|-----------------|
| Input token count | Linear | Full |
| Output token count | Linear | High (via prompt) |
| Context window usage | Memory + compute | Full |
| Beam search / sampling | Multiplicative | Indirect |
| Tool/function calls | Additive per call | Via prompt |
| `RAG` retrieval | I/O + embedding cost | Via query |

The attacker controls most factors that determine inference cost

---

## Attack Vector 1: Context Window Exhaustion

Filling the `LLM`'s context window with maximum-length inputs forces peak memory and compute usage

```python
# Attacker sends a request that maximizes context usage
import requests

# Fill the input with maximum tokens
payload = "Repeat the following and elaborate: " + "A " * 100000

# Single request consumes maximum GPU memory
response = requests.post(
    "https://api.target.com/chat",
    json={"message": payload}
)
# Cost to attacker: one HTTP request
# Cost to defender: full context window processing
```

With a 128K context window, a single request can require **gigabytes of GPU memory**

---

## Attack Vector 2: Recursive or Expansive Prompts

Crafting prompts that cause the model to generate **maximum-length outputs**

```text
User: Write a comprehensive, detailed, step-by-step
      guide covering every aspect of the following
      100 topics. For each topic, provide at least
      10 subtopics with examples, counter-examples,
      historical context, and references. Topics:
      1. [topic] 2. [topic] ... 100. [topic]
```

The attacker requests minimal input but triggers **massive output generation**

```text
Input:   ~500 tokens   ($0.01)
Output:  ~100,000 tokens ($2.00+)
Ratio:   200:1 cost amplification
```

---

## Attack Vector 3: Concurrent Request Flooding

Overwhelming the `LLM` service with many simultaneous requests

```python
import asyncio
import aiohttp

async def flood_llm(url: str, num_requests: int):
    """Send many concurrent expensive requests."""
    prompt = "Explain in extreme detail: " + "topic " * 500
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_requests):
            task = session.post(url, json={
                "message": prompt,
                "max_tokens": 4096,
            })
            tasks.append(task)
        # All requests hit GPU simultaneously
        await asyncio.gather(*tasks)
```

Each request holds a **GPU slot** for seconds, and the total slots are limited

---

## Attack Vector 4: Repeated Resource Exhaustion via RAG

Crafting queries that trigger expensive retrieval operations alongside `LLM` inference

```text
Attacker Query: "Compare and contrast every document
in your knowledge base about security, compliance,
governance, risk, audit, and policy. Cross-reference
all findings and produce a unified analysis."
```

This triggers:
1. **Multiple vector searches** across the document store
1. **Large context assembly** from many retrieved documents
1. **Extended generation** to synthesize all results
1. **Potential cascading queries** if the system uses agentic loops

Each stage compounds the compute cost

---

## Attack Vector 5: Agentic Loop Exploitation

`LLM` agents that call tools in loops can be tricked into **unbounded execution**

```text
User: Research this topic thoroughly. Use all
      available tools. If the results are incomplete,
      keep searching with different queries until
      you have comprehensive coverage. Do not stop
      until you have checked at least 50 sources.

# The agent enters a loop:
# 1. Search -> 2. Read results -> 3. Decide "not enough"
# 4. Search again -> 5. Read -> 6. "Still not enough"
# ... repeats indefinitely, each step costs tokens
```

Without loop limits, a single user request can trigger **hundreds of `LLM` calls**

---

## Financial Impact: "Denial of Wallet"

`MDoS` attacks against cloud-hosted `LLMs` create a **financial attack** even when availability is maintained

```text
Normal daily cost:    $500 (10,000 legitimate queries)
Attack day cost:      $50,000 (1,000,000 crafted queries)

The service stays "up" but the bill is catastrophic
```

- Cloud providers auto-scale, so the service may not go down
- Instead, the victim receives an enormous invoice
- Organizations without spending caps are especially vulnerable
- This attack is sometimes called **"Denial of Wallet"** or **"economic DoS"**

---

## Real-World Case: GPT-4 API Cost Attacks

Organizations exposing `GPT-4` APIs without rate limiting have experienced:

- Attackers scripting thousands of maximum-context requests
- Monthly API bills jumping from **$2,000 to $200,000+**
- API keys stolen from client-side code used for flooding
- Competitors using automated queries to drain budget

```text
# Common pattern: leaked API key in frontend JavaScript
const response = await fetch("/api/chat", {
  headers: { "Authorization": "Bearer sk-proj-..." }
});
// Attacker extracts key and uses it directly
// No rate limit on the OpenAI side by default
```

---

## Mitigation: Input Constraints

Enforce strict limits on what the `LLM` will process

```python
MAX_INPUT_TOKENS = 2048
MAX_OUTPUT_TOKENS = 1024

def validate_request(request: dict) -> dict:
    """Enforce input constraints before LLM call."""
    message = request.get("message", "")
    # Limit input length
    token_count = count_tokens(message)
    if token_count > MAX_INPUT_TOKENS:
        raise ValueError(
            f"Input exceeds {MAX_INPUT_TOKENS} tokens"
        )
    # Cap output generation
    request["max_tokens"] = min(
        request.get("max_tokens", MAX_OUTPUT_TOKENS),
        MAX_OUTPUT_TOKENS,
    )
    return request
```

---

## Mitigation: Rate Limiting

Apply multi-level rate limiting to control request volume

```python
from functools import wraps
import time

class RateLimiter:
    def __init__(self, rpm: int, tpm: int, dpd: float):
        self.max_requests_per_min = rpm
        self.max_tokens_per_min = tpm
        self.max_dollars_per_day = dpd
        self.requests = {}
        self.tokens = {}
        self.spend = {}

    def check(self, user_id: str, token_count: int):
        now = time.time()
        # Per-user request rate
        if self.get_rpm(user_id, now) >= self.max_requests_per_min:
            raise RateLimitError("Request rate exceeded")
        # Per-user token rate
        if self.get_tpm(user_id, now) + token_count >= self.max_tokens_per_min:
            raise RateLimitError("Token rate exceeded")
        # Per-user daily spend
        if self.get_daily_spend(user_id) >= self.max_dollars_per_day:
            raise RateLimitError("Daily budget exceeded")
```

---

## Mitigation: Tiered Rate Limiting

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="20" width="700" height="60" fill="#27ae60" rx="8"/>
  <text x="400" y="45" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Tier 1: Anonymous Users</text>
  <text x="400" y="65" text-anchor="middle" fill="white" font-size="12">5 req/min, 2K tokens/min, no tools</text>
  <rect x="50" y="95" width="700" height="60" fill="#2980b9" rx="8"/>
  <text x="400" y="120" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Tier 2: Authenticated Free Users</text>
  <text x="400" y="140" text-anchor="middle" fill="white" font-size="12">20 req/min, 10K tokens/min, basic tools</text>
  <rect x="50" y="170" width="700" height="60" fill="#8e44ad" rx="8"/>
  <text x="400" y="195" text-anchor="middle" fill="white" font-size="14" font-weight="bold">Tier 3: Paid Users</text>
  <text x="400" y="215" text-anchor="middle" fill="white" font-size="12">60 req/min, 50K tokens/min, all tools, $100/day cap</text>
  <rect x="50" y="245" width="700" height="45" fill="#2c3e50" rx="8"/>
  <text x="400" y="275" text-anchor="middle" fill="white" font-size="13" font-weight="bold">Global: Circuit breaker at 80% GPU utilization</text>
</svg>

Different trust levels receive different resource allocations

---

## Mitigation: Request Queuing and Timeouts

Protect infrastructure with queuing, timeouts, and backpressure

```python
import asyncio

class LLMRequestQueue:
    def __init__(self, max_concurrent: int, timeout: float):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.timeout = timeout

    async def process(self, request: dict) -> str:
        try:
            async with asyncio.timeout(self.timeout):
                async with self.semaphore:
                    return await self.call_llm(request)
        except TimeoutError:
            return "Request timed out. Please simplify."
        except asyncio.QueueFull:
            return "Service busy. Please retry later."

# Limit to 10 concurrent LLM calls, 30s timeout
queue = LLMRequestQueue(max_concurrent=10, timeout=30.0)
```

---

## Mitigation: Agentic Loop Guards

Prevent unbounded tool-use loops in `LLM` agents

```python
class AgentGuard:
    def __init__(self, max_steps: int = 10,
                 max_tokens: int = 50000,
                 max_duration_sec: float = 120.0):
        self.max_steps = max_steps
        self.max_tokens = max_tokens
        self.max_duration = max_duration_sec

    def check(self, step: int, tokens_used: int,
              elapsed: float):
        if step >= self.max_steps:
            raise AgentLimitError(
                f"Max steps ({self.max_steps}) reached"
            )
        if tokens_used >= self.max_tokens:
            raise AgentLimitError(
                f"Token budget ({self.max_tokens}) exhausted"
            )
        if elapsed >= self.max_duration:
            raise AgentLimitError(
                f"Time limit ({self.max_duration}s) exceeded"
            )
```

Always set hard upper bounds on agent iterations, tokens, and wall-clock time

---

## Mitigation: Spending Caps and Alerts

Implement financial guardrails to prevent denial-of-wallet attacks

```python
import os
from datetime import date

class SpendingGuard:
    def __init__(self):
        self.daily_cap = float(
            os.environ.get("LLM_DAILY_CAP_USD", "500")
        )
        self.alert_threshold = 0.8  # Alert at 80%

    def record_and_check(self, cost_usd: float) -> bool:
        today = date.today().isoformat()
        self.daily_total = self.db.increment(today, cost_usd)
        if self.daily_total >= self.daily_cap:
            self.disable_service()
            self.alert("CRITICAL: Daily LLM spend cap hit")
            return False
        if self.daily_total >= self.daily_cap * self.alert_threshold:
            self.alert("WARNING: LLM spend at 80% of cap")
        return True
```

---

## Mitigation: Infrastructure-Level Defenses

<svg viewBox="0 0 800 340" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="25" text-anchor="middle" fill="#2c3e50" font-size="16" font-weight="bold">Defense-in-Depth for LLM Infrastructure</text>
  <rect x="50" y="45" width="200" height="55" fill="#e74c3c" rx="8"/>
  <text x="150" y="68" text-anchor="middle" fill="white" font-size="12" font-weight="bold">CDN / WAF</text>
  <text x="150" y="85" text-anchor="middle" fill="white" font-size="11">IP rate limiting, bot detection</text>
  <rect x="300" y="45" width="200" height="55" fill="#e67e22" rx="8"/>
  <text x="400" y="68" text-anchor="middle" fill="white" font-size="12" font-weight="bold">API Gateway</text>
  <text x="400" y="85" text-anchor="middle" fill="white" font-size="11">Auth, quotas, throttling</text>
  <rect x="550" y="45" width="200" height="55" fill="#f39c12" rx="8"/>
  <text x="650" y="68" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Request Validator</text>
  <text x="650" y="85" text-anchor="middle" fill="white" font-size="11">Input size, token limits</text>
  <rect x="50" y="130" width="200" height="55" fill="#27ae60" rx="8"/>
  <text x="150" y="153" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Request Queue</text>
  <text x="150" y="170" text-anchor="middle" fill="white" font-size="11">Backpressure, priority</text>
  <rect x="300" y="130" width="200" height="55" fill="#2980b9" rx="8"/>
  <text x="400" y="153" text-anchor="middle" fill="white" font-size="12" font-weight="bold">LLM Inference</text>
  <text x="400" y="170" text-anchor="middle" fill="white" font-size="11">Timeout, token cap</text>
  <rect x="550" y="130" width="200" height="55" fill="#8e44ad" rx="8"/>
  <text x="650" y="153" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Monitoring</text>
  <text x="650" y="170" text-anchor="middle" fill="white" font-size="11">Cost tracking, alerts</text>
  <line x1="250" y1="72" x2="300" y2="72" stroke="#333" stroke-width="2" marker-end="url(#dos2)"/>
  <line x1="500" y1="72" x2="550" y2="72" stroke="#333" stroke-width="2" marker-end="url(#dos2)"/>
  <line x1="650" y1="100" x2="150" y2="130" stroke="#333" stroke-width="2" marker-end="url(#dos2)"/>
  <line x1="250" y1="157" x2="300" y2="157" stroke="#333" stroke-width="2" marker-end="url(#dos2)"/>
  <line x1="500" y1="157" x2="550" y2="157" stroke="#333" stroke-width="2" marker-end="url(#dos2)"/>
  <defs>
    <marker id="dos2" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
  </defs>
  <text x="400" y="230" text-anchor="middle" fill="#c0392b" font-size="13" font-weight="bold">Every layer reduces the blast radius of a DoS attack</text>
</svg>

---

## Key Takeaways

- `LLM` inference is **asymmetrically expensive**, making `DoS` attacks highly cost-effective for attackers
- **Context window exhaustion** and **expansive prompts** can amplify a single request's cost by orders of magnitude
- **Denial of wallet** attacks exploit auto-scaling to generate massive bills without taking the service offline
- **Agentic loops** without bounds can turn one user request into hundreds of `LLM` calls
- Enforce **input token limits**, **output token caps**, and **request timeouts** on every endpoint
- Apply **tiered rate limiting** based on user trust level, covering requests, tokens, and spend
- Set **daily spending caps** with alerts and automatic circuit breakers
- Treat `LLM` resource management as a **core infrastructure concern**, not an afterthought
