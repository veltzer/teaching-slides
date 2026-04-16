---
tags:
  - security:security
  - data-and-ai:ai
  - data-and-ai:llm
  - security:owasp
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals

---

# LLM10: Model Theft
## Protecting Your `LLM` Intellectual Property

---

## LLM Model Theft Attack Vectors

![LLM Model Theft Attack Vectors](svg/courses/security/working-with-llms-securely/11_model_theft/model_theft_attacks.svg)

---

## What is Model Theft?

- Unauthorized **copying, extraction, or replication** of an `LLM`
- Attacker gains a functional equivalent of the model **without authorization**
- Threatens the **intellectual property** and **competitive advantage** of model owners
- Can be achieved through `API` access alone — no need to steal model weights

---

## Why Model Theft Matters

- Training an `LLM` costs **millions of dollars**
- Models represent significant **R&D investment**
- Stolen models can be used to:
    - Create **competing products** at no training cost
    - Study the model to find **vulnerabilities**
    - **Fine-tune** for malicious purposes
    - **Bypass safety guardrails**

---

## Attack: Model Weight Theft

```misc
Direct access to model files:

1. Exploit infrastructure vulnerability
2. Access model storage (S3 bucket, file share)
3. Download model weights and configuration
4. Deploy identical model locally

Risk factors:
- Misconfigured cloud storage
- Insider threats
- Compromised CI/CD pipelines
- Weak access controls on model registries
```

---

## Attack: Model Extraction via `API`

```python
# Model extraction through systematic querying
def extract_model(target_api, num_queries=100000):
    training_data = []

    for prompt in generate_diverse_prompts(num_queries):
        response = target_api.query(prompt)
        training_data.append({
            "input": prompt,
            "output": response,
            "logprobs": response.logprobs  # If available
        })

    # Train a clone model on the extracted data
    clone = train_model(training_data)
    return clone
```

---

## Model Extraction: How It Works

```misc
Step 1: Query the target model with diverse inputs
        (thousands to millions of queries)

Step 2: Collect input-output pairs
        (and logprobs/confidence scores if available)

Step 3: Train a "student" model on these pairs
        (knowledge distillation)

Step 4: The student model approximates the
        target model's behavior

Result: A functional copy without the original weights
```

---

## Real-World Incidents

- **Meta's LLaMA** weights leaked within days of restricted release (2023)
- Researchers demonstrated extraction of OpenAI model **embeddings** via API
- Multiple incidents of model weights found on **unsecured cloud storage**
- Insider theft at AI companies leading to **competitive model releases**

---

## Mitigation: Access Controls

```python
# Multi-layer access control for model assets
class ModelAccessControl:
    def check_access(self, user, action, resource):
        checks = [
            self.verify_authentication(user),
            self.verify_authorization(user, action),
            self.verify_ip_allowlist(user),
            self.verify_mfa(user),
            self.check_time_restrictions(user),
        ]
        if not all(checks):
            self.alert_security(user, action, resource)
            raise AccessDenied()

        self.audit_log(user, action, resource)
```

---

## Mitigation: `API` Rate Limiting and Monitoring

```python
class AntiExtractionMonitor:
    def analyze_usage(self, user_id):
        metrics = get_user_metrics(user_id)

        suspicious = (
            metrics.queries_per_hour > 1000 or
            metrics.unique_prompts_ratio > 0.95 or
            metrics.avg_prompt_diversity > 0.9 or
            metrics.logprob_requests_ratio > 0.5 or
            metrics.systematic_input_pattern_detected
        )

        if suspicious:
            throttle_user(user_id)
            alert_security(
                f"Possible extraction: {user_id}")
```

---

## Mitigation: Output Perturbation

```python
import random

def add_output_perturbation(logprobs, epsilon=0.01):
    """Add small random noise to logprobs to hinder
    model extraction while preserving usability."""
    perturbed = {}
    for token, prob in logprobs.items():
        noise = random.gauss(0, epsilon)
        perturbed[token] = max(0, prob + noise)
    # Renormalize
    total = sum(perturbed.values())
    return {k: v/total for k, v in perturbed.items()}
```

Perturbed outputs make extraction less accurate

---

## Mitigation: Watermarking

```misc
Model watermarking techniques:

1. Embed unique patterns in model outputs
2. These patterns are statistically detectable
3. Can prove a model was derived from yours

Types:
- Output watermarking: Patterns in generated text
- Weight watermarking: Markers in model parameters
- Fingerprinting: Unique responses to specific queries
```

---

## Mitigation: Infrastructure Security

- **Encrypt** model weights at rest and in transit
- Use **hardware security modules** (`HSMs`) for key management
- Implement **network segmentation** around model infrastructure
- Use **confidential computing** (encrypted memory) for inference
- Regular **security audits** of model hosting infrastructure

---

## Key Takeaways

- Model theft can occur through **infrastructure compromise** or **`API` extraction**
- Implement **strong access controls** and **multi-factor authentication**
- Monitor `API` usage for **extraction patterns**
- Use **output perturbation** and **watermarking** to hinder extraction
- **Encrypt** model weights and secure hosting infrastructure
- Combine **technical** and **legal** protections
