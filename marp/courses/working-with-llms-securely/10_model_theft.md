# LLM10: Model Theft
## Mark Veltzer
### Senior Software Engineer

---

## What Is Model Theft?

Model theft refers to the **unauthorized access, copying, or extraction** of proprietary `LLM` models and their components

- Ranked **#10** in the OWASP Top 10 for LLM Applications
- Covers several attack vectors:
    - **Direct exfiltration**: stealing model weights or configuration files from storage
    - **Model extraction**: reconstructing a model by querying its API systematically
    - **Side-channel attacks**: inferring model architecture from timing, outputs, or metadata
- Stolen models can be used to:
    - Launch targeted adversarial attacks
    - Bypass safety guardrails
    - Compete commercially without training costs

---

## Why Model Theft Matters

<svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="mt1" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="50" width="180" height="60" fill="#3498db" rx="8"/>
  <text x="120" y="75" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Proprietary LLM</text>
  <text x="120" y="92" text-anchor="middle" fill="white" font-size="11">$10M+ training cost</text>
  <line x1="210" y1="80" x2="290" y2="80" stroke="#333" stroke-width="2" marker-end="url(#mt1)"/>
  <rect x="300" y="50" width="180" height="60" fill="#e67e22" rx="8"/>
  <text x="390" y="75" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Attacker extracts</text>
  <text x="390" y="92" text-anchor="middle" fill="white" font-size="11">via API or breach</text>
  <line x1="480" y1="80" x2="560" y2="50" stroke="#333" stroke-width="2" marker-end="url(#mt1)"/>
  <line x1="480" y1="80" x2="560" y2="110" stroke="#333" stroke-width="2" marker-end="url(#mt1)"/>
  <rect x="570" y="25" width="200" height="40" fill="#e74c3c" rx="8"/>
  <text x="670" y="50" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Competitor uses clone</text>
  <rect x="570" y="75" width="200" height="40" fill="#e74c3c" rx="8"/>
  <text x="670" y="100" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Adversarial attacks crafted</text>
  <rect x="570" y="125" width="200" height="40" fill="#e74c3c" rx="8"/>
  <text x="670" y="150" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Safety guardrails bypassed</text>
  <text x="400" y="230" text-anchor="middle" fill="#c0392b" font-size="13" font-weight="bold">Model theft turns your investment into the attacker's advantage</text>
</svg>

---

## Model Extraction Attacks

An attacker queries the `LLM` API thousands of times to **build a functionally equivalent clone** without ever accessing the actual weights

```text
MODEL EXTRACTION PROCESS:

1. QUERY COLLECTION
   Attacker sends diverse prompts covering the input space
   Collects input-output pairs: (prompt, response)

1. DISTILLATION
   Uses collected pairs as training data for a smaller model
   Student model learns to mimic the original's behavior

1. REFINEMENT
   Iteratively queries areas where the clone diverges
   Focuses on edge cases to improve fidelity

RESULT: A functional replica trained at a fraction of the cost
        The clone may replicate biases, capabilities, and flaws
```

---

## API Abuse for Model Replication

```python
# How an attacker might systematically extract a model
import itertools

class ModelExtractor:
    def __init__(self, target_api):
        self.api = target_api
        self.training_data = []

    def collect_samples(self, prompts: list[str]):
        for prompt in prompts:
            response = self.api.query(
                prompt=prompt,
                temperature=0,  # Deterministic output
                logprobs=True,  # Request probability data
            )
            self.training_data.append({
                "input": prompt,
                "output": response.text,
                "logprobs": response.logprobs,  # Key signal
            })

    def train_clone(self):
        # Use collected data to fine-tune a base model
        clone = load_base_model("open-source-llm")
        clone.fine_tune(self.training_data)
        return clone
```

Requesting `logprobs` gives the attacker **probability distributions** over the vocabulary, which dramatically accelerates extraction.

---

## Detecting Extraction Attempts

Extraction attacks have distinctive patterns that can be detected with monitoring

```python
from collections import defaultdict
import time

class ExtractionDetector:
    def __init__(self, window_sec: int = 3600):
        self.window = window_sec
        self.request_log: dict[str, list] = defaultdict(list)

    def check_request(self, api_key: str,
                      request: dict) -> list[str]:
        now = time.time()
        alerts = []
        history = self.request_log[api_key]
        # Prune old entries
        history[:] = [r for r in history
                      if now - r["time"] < self.window]
        # High volume in short window
        if len(history) > 500:
            alerts.append("HIGH_VOLUME")
        # Systematic temperature=0 usage
        zero_temp = [r for r in history
                     if r.get("temperature") == 0]
        if len(zero_temp) > len(history) * 0.9:
            alerts.append("DETERMINISTIC_PATTERN")
        # Repeated logprobs requests
        logprob_reqs = [r for r in history
                        if r.get("logprobs")]
        if len(logprob_reqs) > len(history) * 0.8:
            alerts.append("LOGPROBS_ABUSE")
        history.append({"time": now, **request})
        return alerts
```

---

## Access Controls for Model Protection

Protecting `LLM` assets requires **defense in depth** across multiple layers

```text
LAYER 1: NETWORK ACCESS
   - Model endpoints behind VPN or private network
   - No direct internet access to model serving infrastructure
   - API gateway as single entry point

LAYER 2: AUTHENTICATION AND AUTHORIZATION
   - API keys with scoped permissions (read-only, no logprobs)
   - Role-based access: not every developer needs model access
   - Short-lived tokens with automatic rotation

LAYER 3: MODEL ARTIFACT SECURITY
   - Model weights encrypted at rest and in transit
   - Stored in access-controlled registries (not open S3 buckets)
   - Checksums to detect tampering

LAYER 4: OPERATIONAL CONTROLS
   - Rate limiting per API key and per IP
   - Query budgets with hard daily/monthly caps
   - Watermarking model outputs for traceability
```

---

## Rate Limiting and Query Budgets

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class QueryBudget:
    daily_limit: int = 1000
    monthly_limit: int = 10000
    max_logprob_requests: int = 50
    max_batch_size: int = 10

class BudgetEnforcer:
    def __init__(self):
        self.usage: dict[str, dict] = {}

    def check(self, api_key: str, request: dict):
        today = datetime.utcnow().strftime("%Y-%m-%d")
        month = datetime.utcnow().strftime("%Y-%m")
        usage = self.usage.setdefault(api_key, {})
        daily = usage.get(f"daily:{today}", 0)
        monthly = usage.get(f"monthly:{month}", 0)
        budget = self._get_budget(api_key)
        if daily >= budget.daily_limit:
            raise RateLimitError("Daily query limit reached")
        if monthly >= budget.monthly_limit:
            raise RateLimitError("Monthly query limit reached")
        if request.get("logprobs"):
            lp_count = usage.get(f"logprobs:{today}", 0)
            if lp_count >= budget.max_logprob_requests:
                raise RateLimitError("Logprobs limit reached")
            usage[f"logprobs:{today}"] = lp_count + 1
        usage[f"daily:{today}"] = daily + 1
        usage[f"monthly:{month}"] = monthly + 1
```

---

## Output Watermarking

Embed **invisible statistical watermarks** in `LLM` outputs to trace stolen model replicas back to the source

```python
import hashlib

class OutputWatermarker:
    """Embeds a detectable signal in token selection."""
    def __init__(self, secret_key: str):
        self.key = secret_key

    def watermark_logits(self, logits: list[float],
                         context_hash: str) -> list[float]:
        """Bias token probabilities using a keyed hash."""
        seed = hashlib.sha256(
            f"{self.key}:{context_hash}".encode()
        ).digest()
        # Split vocabulary into "green" and "red" tokens
        # Slightly boost green token probabilities
        for i in range(len(logits)):
            if self._is_green_token(i, seed):
                logits[i] += 1.0  # Small bias
        return logits

    def detect_watermark(self, text: str) -> float:
        """Returns confidence that text came from our model."""
        tokens = tokenize(text)
        green_count = sum(
            1 for t in tokens
            if self._is_green_token(t.id, self._get_seed(t))
        )
        return green_count / len(tokens)  # High = watermarked
```

---

## Securing Model Artifacts

```python
import hashlib
from pathlib import Path

class ModelRegistry:
    """Secure storage for model weights and configs."""
    def __init__(self, storage_path: str, encryption_key: str):
        self.path = Path(storage_path)
        self.enc_key = encryption_key
        self.manifest: dict[str, str] = {}

    def register_model(self, model_name: str,
                       weights_path: str):
        checksum = self._compute_checksum(weights_path)
        encrypted_path = self._encrypt_and_store(
            weights_path, model_name
        )
        self.manifest[model_name] = {
            "path": encrypted_path,
            "checksum": checksum,
            "registered_at": datetime.utcnow().isoformat(),
        }
        # Remove unencrypted copy
        Path(weights_path).unlink()

    def load_model(self, model_name: str, requestor: str):
        if not self._is_authorized(requestor, model_name):
            raise PermissionError(
                f"{requestor} not authorized for {model_name}"
            )
        entry = self.manifest[model_name]
        decrypted = self._decrypt(entry["path"])
        if self._compute_checksum(decrypted) != entry["checksum"]:
            raise TamperError("Model checksum mismatch")
        audit_log.info(f"{requestor} loaded {model_name}")
        return decrypted
```

---

## Monitoring and Alerting Strategy

```python
from dataclasses import dataclass

@dataclass
class ModelSecurityAlert:
    severity: str      # low, medium, high, critical
    alert_type: str
    api_key: str
    details: str

class ModelSecurityMonitor:
    def __init__(self):
        self.detector = ExtractionDetector()
        self.budget = BudgetEnforcer()

    def process_request(self, api_key: str,
                        request: dict) -> dict:
        # 1. Enforce budget
        self.budget.check(api_key, request)
        # 2. Check for extraction patterns
        alerts = self.detector.check_request(
            api_key, request
        )
        for alert_type in alerts:
            self._handle_alert(ModelSecurityAlert(
                severity="high",
                alert_type=alert_type,
                api_key=api_key,
                details=f"Suspicious pattern: {alert_type}",
            ))
        # 3. Log the request
        audit_log.info(f"API request from {api_key}")
        return {"allowed": len(alerts) == 0}

    def _handle_alert(self, alert: ModelSecurityAlert):
        if alert.severity == "critical":
            revoke_api_key(alert.api_key)
        notify_security_team(alert)
```

---

## Key Takeaways

- Model theft targets your **intellectual property and competitive advantage**. A stolen model can be used to create competitors, craft adversarial attacks, or bypass safety guardrails.
- **Model extraction attacks** query your API systematically to build functional clones. Features like `logprobs` and deterministic outputs (`temperature=0`) make extraction easier.
- Implement **layered access controls**: network isolation, scoped API keys, encrypted model artifacts, and integrity checksums.
- Use **rate limiting and query budgets** to make large-scale extraction impractical. Monitor for telltale patterns like high volume, deterministic settings, and repeated `logprobs` requests.
- Consider **output watermarking** to trace stolen model replicas back to your system and establish provenance.
- Maintain **comprehensive audit logs** and automated alerting so that extraction attempts are detected early and responded to quickly.
