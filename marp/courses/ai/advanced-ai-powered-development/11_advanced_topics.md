---
tags:
  - data-and-ai:ai
  - data-and-ai:agents
  - data-and-ai:mcp
  - data-and-ai:rag
  - practices:tools
  - practices:large-codebases
  - data-and-ai:prompt-engineering
  - practices:productivity
level: advanced
category: ai
audience:
  - audiences:developers

---
# Advanced Topics

## Overview
- Multi-model strategies and cost optimization
- Fine-tuning vs prompt engineering for development
- Running local models for privacy and offline work
- AI governance, compliance, and code ownership
- Scaling AI-powered development across teams

---

## Multi-Model Strategies: Why Multiple Models?

- Different models excel at different tasks
- Cost varies dramatically across providers
- Latency requirements differ by use case

| Task | Recommended Tier | Example |
|------|-----------------|---------|
| Code completion | Fast, cheap | `GPT-4o-mini`, `Claude Haiku` |
| Architecture review | High reasoning | `Claude Opus`, `GPT-4o` |
| Test generation | Mid-tier | `Claude Sonnet`, `GPT-4o` |
| Documentation | Mid-tier | `Claude Sonnet`, `Gemini Pro` |

---

## Model Routing and Fallback

- Route requests based on task complexity and latency needs
- Implement fallback chains for reliability

```python
MODEL_ROUTES = {
    "autocomplete": ["claude-haiku", "gpt-4o-mini"],
    "review": ["claude-opus", "gpt-4o", "claude-sonnet"],
    "explain": ["claude-sonnet", "gpt-4o-mini"],
}

async def route_request(task: str, prompt: str) -> str:
    for model in MODEL_ROUTES[task]:
        try:
            return await call_model(model, prompt)
        except (RateLimitError, TimeoutError):
            continue
    raise AllModelsFailedError(task)
```

---

## Cost Optimization Across Models

- Track token usage per task type and model
- Use cheaper models for first-pass, expensive for validation

```yaml
# cost-policy.yaml
policies:
  - task: inline_completion
    max_cost_per_request: 0.002
    model_preference: [haiku, gpt-4o-mini]
  - task: code_review
    max_cost_per_request: 0.05
    model_preference: [sonnet, gpt-4o]
  - task: architecture_analysis
    max_cost_per_request: 0.15
    model_preference: [opus, gpt-4o]
monthly_budget: 500
alert_threshold: 0.8
```

---

## Benchmarking Local vs Cloud Models

- Run identical tasks on local and cloud models to compare
- Measure quality, latency, and cost per task type

```python
import time

TASKS = [
    {"name": "docstring", "prompt": "Write a docstring for: def merge_sort(arr):"},
    {"name": "review", "prompt": "Review this code for bugs: ..."},
    {"name": "test", "prompt": "Write unit tests for a stack class"},
]

async def benchmark(models: list[str], tasks: list[dict]) -> list[dict]:
    results = []
    for model in models:
        for task in tasks:
            start = time.perf_counter()
            output = await call_model(model, task["prompt"])
            elapsed = time.perf_counter() - start
            results.append({
                "model": model, "task": task["name"],
                "latency_s": round(elapsed, 2),
                "output_tokens": count_tokens(output),
                "quality": await score_output(output, task),
            })
    return results
```

**Exercise:** run this against `ollama/codellama:13b` and `claude-sonnet` and compare.

---

## Hands-On: Build a Cost Dashboard

- Wrap every LLM call with a logging decorator
- Aggregate costs per model, task, and team

```python
import functools, datetime, json

COST_LOG: list[dict] = []

def track_cost(model: str, cost_per_1k: float):
    def decorator(fn):
        @functools.wraps(fn)
        async def wrapper(prompt: str, **kw):
            result = await fn(prompt, **kw)
            tokens = count_tokens(result)
            COST_LOG.append({
                "ts": datetime.datetime.utcnow().isoformat(),
                "model": model,
                "tokens": tokens,
                "cost_usd": round(tokens / 1000 * cost_per_1k, 6),
            })
            return result
        return wrapper
    return decorator

def daily_summary() -> dict:
    by_model: dict[str, float] = {}
    for entry in COST_LOG:
        by_model.setdefault(entry["model"], 0.0)
        by_model[entry["model"]] += entry["cost_usd"]
    return by_model
```

Feed `COST_LOG` into Grafana or a simple HTML chart for visibility.

---

## Fine-Tuning vs Prompt Engineering

- Prompt engineering is the default starting point
- Fine-tuning is warranted when prompts become unwieldy

| Criteria | Prompt Engineering | Fine-Tuning |
|----------|-------------------|-------------|
| Setup cost | Low | High |
| Iteration speed | Minutes | Hours/days |
| Domain adaptation | Moderate | Strong |
| Maintenance burden | Low | Medium |
| Data requirement | Few examples | Hundreds+ |

**Rule of thumb:** if your system prompt exceeds 2000 tokens of examples, consider fine-tuning.

---

## Creating Training Datasets from Codebases

- Extract high-quality input/output pairs from real work
- Use git history, code reviews, and documentation as sources

```python
import subprocess, json

def extract_training_pairs(repo_path: str) -> list[dict]:
    """Extract commit message + diff pairs for fine-tuning."""
    log = subprocess.run(
        ["git", "log", "--format=%H", "-100"],
        capture_output=True, text=True, cwd=repo_path
    )
    pairs = []
    for sha in log.stdout.strip().split("\n"):
        msg = get_commit_message(sha, repo_path)
        diff = get_commit_diff(sha, repo_path)
        if len(diff) < 4000:  # Keep examples concise
            pairs.append({"input": diff, "output": msg})
    return pairs
```

---

## Evaluating Fine-Tuned Models

- Always compare against the base model with good prompts
- Use domain-specific benchmarks, not generic ones

```python
EVAL_SUITE = [
    {"input": "def fib(n):", "expected_pattern": r"fibonacci|recursive|memoiz"},
    {"input": "// TODO: add error handling", "check": has_try_catch},
    {"input": "SELECT * FROM users", "check": uses_parameterized_query},
]

def evaluate_model(model_id: str) -> dict:
    results = {"pass": 0, "fail": 0}
    for case in EVAL_SUITE:
        output = generate(model_id, case["input"])
        passed = case["check"](output)
        results["pass" if passed else "fail"] += 1
    results["score"] = results["pass"] / len(EVAL_SUITE)
    return results
```

---

## Fine-Tuning Walkthrough: LoRA on a Code Model

- `LoRA` (Low-Rank Adaptation) fine-tunes a fraction of weights
- Use `peft` + `transformers` for quick setup on a single GPU

```python
from peft import LoraConfig, get_peft_model, TaskType
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer

base_model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-7b-hf")
tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-hf")

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16, lora_alpha=32, lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],
)
model = get_peft_model(base_model, lora_config)

training_args = TrainingArguments(
    output_dir="./lora-codellama",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-4,
)
trainer = Trainer(model=model, args=training_args, train_dataset=dataset)
trainer.train()
model.save_pretrained("./lora-codellama-final")
```

Trainable parameters drop from billions to ~10M with LoRA.

---

## Local Models: Tools and Ecosystem

- `Ollama` -- simplest setup, good model library
- `LM Studio` -- GUI-based, easy model management
- `llama.cpp` -- maximum control, lowest overhead

```bash
# Ollama: pull and run a coding model
ollama pull codellama:13b
ollama run codellama:13b "Write a Python decorator for retry logic"

# llama.cpp: run with specific parameters
./llama-server \
    --model codellama-13b-instruct.Q4_K_M.gguf \
    --ctx-size 4096 \
    --port 8080 \
    --n-gpu-layers 35
```

Both expose an OpenAI-compatible API for tool integration.

---

## Privacy-Sensitive Workflows: The Need

- Some codebases cannot leave the corporate network
- Local models enable AI assistance without data exfiltration

---

## Privacy-Sensitive Development Workflows

![privacy_sensitive_development_workflows](svg/courses/ai/advanced-ai-powered-development/11_advanced_topics/privacy_sensitive_development_workflows.svg)

---

## Offline Development with AI

- Configure IDE extensions to use local endpoints
- Pre-download models before going offline

```json
// VS Code settings for local model fallback
{
    "continue.models": [
        {
            "title": "Local CodeLlama",
            "provider": "ollama",
            "model": "codellama:13b",
            "apiBase": "http://localhost:11434"
        }
    ],
    "github.copilot.advanced": {
        "debug.useElectronFetcher": true,
        "debug.useNodeFetcher": false
    }
}
```

---

## Hardware Requirements and Performance

- VRAM is the primary bottleneck for local inference
- Quantization trades accuracy for speed and memory

| Model Size | Quantization | VRAM Required | Tokens/sec (RTX 4090) |
|-----------|-------------|---------------|----------------------|
| 7B | Q4_K_M | ~4 GB | ~80 |
| 13B | Q4_K_M | ~8 GB | ~45 |
| 34B | Q4_K_M | ~20 GB | ~20 |
| 70B | Q4_K_M | ~40 GB | ~10 |

- For CPU-only: expect 5-10x slower inference
- Apple Silicon M-series: unified memory helps with larger models
- Minimum practical setup: 16 GB RAM, 8 GB VRAM for 7B-13B models

---

## Quantization and Model Optimization

- Quantization reduces model precision to shrink size and increase speed
- Multiple formats target different hardware and workflows

| Format | Approach | Best For |
|--------|----------|----------|
| `GGUF` | CPU + GPU split inference | `llama.cpp`, `Ollama` |
| `GPTQ` | GPU-only, post-training quantization | `vLLM`, `AutoGPTQ` |
| `AWQ` | Activation-aware, preserves salient weights | `vLLM`, `TGI` |

Quality tradeoffs by bit-width:
1. **Q8** -- near-lossless, ~50% size reduction
1. **Q4_K_M** -- good balance, ~75% size reduction
1. **Q2** -- noticeable degradation, only for constrained environments

```bash
# Convert a model to GGUF Q4_K_M using llama.cpp
python convert_hf_to_gguf.py ./codellama-7b --outtype q4_k_m
```

---

## Code Ownership and AI-Generated Code

- Who owns code generated by an AI model?
- Legal landscape is still evolving

Key considerations:
1. Training data provenance matters for license compliance
1. Most jurisdictions: AI output is not independently copyrightable
1. The developer who reviews and integrates the code bears responsibility
1. Company policies should explicitly address AI-generated code

```misc
# Example policy header for AI-assisted files
# AI-ASSISTED: Portions of this file were generated with AI tools.
# Reviewed by: developer@company.com
# Date: 2025-09-15
# Model: claude-sonnet-4-20250514
```

---

## License Implications and Audit Trails

- AI models trained on open-source code may produce license-encumbered output
- Track AI usage for compliance audits

```yaml
# .ai-audit.yaml -- track AI-assisted development
entries:
  - file: src/auth/oauth.py
    model: claude-sonnet
    date: 2025-09-10
    developer: jdoe
    prompt_summary: "Generate OAuth2 PKCE flow"
    review_status: approved
  - file: src/db/migrations/005.sql
    model: gpt-4o
    date: 2025-09-12
    developer: asmith
    prompt_summary: "Migration for user roles table"
    review_status: approved
```

Run license scanners (`scancode`, `FOSSA`, `Snyk`) on AI-generated code.

---

## Organizational Policies for AI Development

- Establish clear guardrails before broad adoption
- Balance productivity gains with risk management

Essential policy areas:
1. **Approved models and providers** -- maintain an allow-list
1. **Data classification** -- which code can be sent to cloud APIs
1. **Review requirements** -- AI-generated code must pass standard review
1. **Prohibited uses** -- security-critical crypto, compliance logic
1. **Incident response** -- what to do when AI introduces a vulnerability

```misc
# .ai-policy.json (enforced by pre-commit hook)
{
    "allowed_providers": ["anthropic", "openai"],
    "blocked_paths": ["src/crypto/**", "src/compliance/**"],
    "require_human_review": true,
    "max_ai_contribution_pct": 70
}
```

---

## AI Governance: Building a Review Board

- A cross-functional board evaluates AI tool adoption and usage
- Provides oversight without blocking developer productivity

Board composition:
1. **Engineering lead** -- technical feasibility and integration
1. **Security representative** -- risk assessment and threat modeling
1. **Legal/compliance** -- licensing, data privacy, regulatory
1. **Product owner** -- business value and roadmap alignment

Evaluation criteria for new AI tools:
1. Data handling and privacy guarantees
1. Model transparency and audit capabilities
1. Cost projections at team and org scale
1. Integration with existing CI/CD and review workflows
1. Vendor lock-in and exit strategy

Meet monthly; publish decisions in an internal decision log.

---

## Security Risks of AI in Development

- AI tools introduce novel attack surfaces in the development pipeline
- Threat model must extend to prompts, models, and outputs

Key risk areas:
1. **Prompt injection in CI** -- malicious code comments that manipulate AI review bots
1. **Model poisoning** -- tampered fine-tuning data introduces backdoors
1. **Data exfiltration** -- sensitive code sent to external APIs without controls
1. **Dependency confusion** -- AI suggests packages that do not exist (typosquatting)

```yaml
# CI safeguard: scan AI-generated suggestions before merge
- name: ai-security-scan
  run: |
    # Verify suggested packages actually exist in registry
    python scripts/verify_imports.py --diff ${{ github.event.pull_request.diff_url }}
    # Check for known prompt injection patterns
    python scripts/scan_prompt_injection.py --path src/
```

---

## Team Onboarding and Training

- AI tools have a learning curve despite apparent simplicity
- Structured onboarding accelerates effective adoption

Recommended onboarding path:
1. **Week 1:** Prompt engineering fundamentals
    - Writing effective system prompts
    - Understanding context windows and token limits
1. **Week 2:** Tool-specific workflows
    - IDE integration, CLI tools, code review assistants
1. **Week 3:** Advanced patterns
    - Multi-step generation, chain-of-thought for debugging
1. **Week 4:** Best practices and pitfalls
    - When not to use AI, reviewing AI output critically

---

## Change Management for AI Adoption

- Technology adoption fails without addressing the human side
- Developers may resist AI tools for valid reasons

Common resistance patterns and responses:
1. **"AI will replace me"** -- reframe as augmentation, show productivity data
1. **"I don't trust the output"** -- teach verification workflows, share error rates
1. **"It slows me down"** -- provide structured training, pair with power users

Practical training program:
1. Lunch-and-learn sessions with live demos
1. Curated prompt libraries for common team tasks
1. Buddy system pairing skeptics with early adopters
1. Monthly retrospectives on AI-assisted work outcomes

---

## Building Internal AI Champions

- Champions accelerate adoption beyond what top-down mandates achieve
- They bridge the gap between tooling teams and daily practitioners

Identifying advocates:
1. Developers who naturally experiment with new tools
1. Team leads who track productivity improvements
1. Engineers who contribute to internal documentation

Building a community of practice:
1. Create a dedicated Slack/Teams channel for AI tips
1. Host bi-weekly show-and-tell sessions for prompt techniques
1. Maintain a shared wiki of effective patterns and anti-patterns
1. Recognize contributions through internal tech talks or blog posts

Champions should have direct access to the governance board for fast feedback loops.

---

## Standardizing Tool Configurations

- Shared configs prevent drift and ensure consistency
- Version-control AI tool settings alongside the codebase

```jsonc
// .ai-config.json (committed to repo)
{
    "default_model": "claude-sonnet",
    "temperature": 0.2,
    "max_tokens": 4096,
    "system_prompt_path": ".prompts/system.md",
    "code_style": {
        "language": "typescript",
        "formatter": "prettier",
        "lint_command": "npm run lint"
    },
    "context_files": [
        "ARCHITECTURE.md",
        "docs/coding-standards.md"
    ]
}
```

---

## Measuring and Improving AI Adoption

- Track metrics to justify investment and guide improvement
- Combine quantitative data with developer surveys

Key metrics to track:
1. **Acceptance rate** -- % of AI suggestions accepted
1. **Time to completion** -- task duration with/without AI
1. **Code quality** -- defect rate in AI-assisted vs manual code
1. **Developer satisfaction** -- quarterly survey scores

```python
# Example: extracting acceptance rate from tool logs
def compute_acceptance_rate(logs: list[dict]) -> float:
    accepted = sum(1 for l in logs if l["action"] == "accepted")
    total = sum(1 for l in logs if l["action"] in ("accepted", "rejected"))
    return accepted / total if total > 0 else 0.0
```

---

## Building a Model Evaluation Pipeline

- Automate quality comparisons across models on every update
- Catch regressions before rolling out new model versions

```python
MODELS = ["claude-sonnet", "gpt-4o", "codellama:13b"]
TEST_CASES = load_test_suite("eval/code_tasks.json")

async def evaluate_all() -> dict:
    scores: dict[str, list[float]] = {}
    for model in MODELS:
        scores[model] = []
        for case in TEST_CASES:
            output = await call_model(model, case["prompt"])
            score = grade(output, case["expected"], case["rubric"])
            scores[model].append(score)
    return {m: sum(s) / len(s) for m, s in scores.items()}
```

Integrate into CI to run weekly; alert when scores drop below threshold.

---

## Maturity Model: Why Stages Matter

- Organizations progress through predictable stages of AI adoption
- Knowing your stage helps prioritize the right investments

---

## AI Development Maturity Model

![ai_development_maturity_model](svg/courses/ai/advanced-ai-powered-development/11_advanced_topics/ai_development_maturity_model.svg)

---

## Maturity Model: Building on Foundations

Each level requires the foundations of the previous one.

---

## Ethical Considerations in AI Development

- AI code generation can perpetuate biases from training data
- Teams must actively address fairness and accessibility

Key concerns:
1. **Bias in suggestions** -- models may default to non-inclusive variable names, culturally biased examples, or inaccessible patterns
1. **Accessibility gaps** -- AI-generated UIs often omit ARIA labels, keyboard navigation, and screen reader support
1. **Environmental cost** -- large model inference has a measurable carbon footprint

Mitigations:
1. Include accessibility linting (`axe`, `pa11y`) in AI-assisted pipelines
1. Add inclusive language checks to code review checklists
1. Track per-team inference carbon estimates using tools like `codecarbon`
1. Review AI suggestions through the lens of diverse end-users

---

## Internal AI Platforms: Core Services

- Centralize model access, prompt management, and observability
- Provide guardrails as a service rather than per-team enforcement

---

## Building Internal AI Development Platforms

![building_internal_ai_development_platforms](svg/courses/ai/advanced-ai-powered-development/11_advanced_topics/building_internal_ai_development_platforms.svg)

---

## Agentic Tool Comparison Matrix

- The agentic coding tool landscape is evolving rapidly
- Each tool makes different tradeoffs in autonomy and integration

| Feature | `Cursor` | `Claude Code` | `Windsurf` | `Copilot Workspace` |
|---------|----------|---------------|------------|---------------------|
| Autonomy level | Medium | High | Medium | High |
| Terminal access | Limited | Full | Limited | Sandboxed |
| Multi-file edits | Yes | Yes | Yes | Yes |
| Custom tools/MCP | No | Yes | No | No |
| Offline/local | No | No | No | No |
| Pricing model | Subscription | Token-based | Subscription | Subscription |

Selection criteria:
1. Does your workflow require terminal and shell access?
1. How important is custom tool integration (`MCP`, plugins)?
1. What level of autonomy is acceptable given your codebase sensitivity?

---

## Future Directions

- The AI-assisted development landscape is shifting toward deeper integration

Emerging trends:
1. **Longer context windows** -- million-token contexts enable whole-repo understanding
    - Reduces need for retrieval and chunking strategies
1. **Multi-modal development** -- diagrams, screenshots, and voice as input
    - Design-to-code workflows become more natural
1. **Collaborative agents** -- multiple specialized agents working in concert
    - One agent writes code, another reviews, a third writes tests
1. **Model distillation** -- compress large model capabilities into smaller, faster models
    - Custom small models that match large model quality on specific domains

The long-term trajectory: AI as a persistent development partner, not a tool you invoke.

---

## Summary

- **Multi-model strategies** reduce cost and improve reliability
    - Route by task complexity, implement fallback chains
- **Fine-tuning** is powerful but only when prompt engineering falls short
    - Build evaluation suites before investing in training
- **Local models** enable private and offline AI development
    - Practical for 7B-13B models on modern hardware
- **Governance** must be proactive, not reactive
    - Audit trails, license scanning, clear ownership policies
- **Scaling** requires standardization and measurement
    - Shared configs, onboarding programs, internal platforms
