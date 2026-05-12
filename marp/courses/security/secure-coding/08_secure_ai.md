---
tags:
  - security:secure-coding
  - data-and-ai:ai
  - data-and-ai:machine-learning
  - security:owasp
  - security:compliance
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:devops
  - audiences:security-professionals
---
# Secure AI Development

---

## What This Chapter Covers

- Security risks in `AI`/`ML` pipelines
- Training data integrity and poisoning
- Model security and intellectual property protection
- Adversarial attacks and defenses
- Secure deployment of `AI` models
- `NIST` SP 800-218A — secure development for generative `AI`
- `OWASP` guidelines for `AI`/`ML` security

---

## Why AI Changes The Threat Model

- The classic supply chain now includes **datasets** and **pre-trained models** — both can be poisoned
- The system's behavior is **learned, not coded** — you cannot fully audit it by reading source
- New trust boundary: the **prompt / input** is attacker-controlled and gets *interpreted*, not just processed
- The model itself is valuable IP and may have *memorized* sensitive training data
- Everything from the earlier chapters still applies — `AI` adds risks, it does not replace the old ones

---

## Security Risks Across The AI Pipeline

- **Data collection** — poisoned, biased, or copyright-tainted training data; PII you should not have ingested
- **Training** — compromised training code, malicious dependencies, unverified base models
- **Model artifacts** — pickled model files that execute code on load; tampered weights
- **Serving** — prompt injection, jailbreaks, model extraction via the API, denial-of-wallet
- **Outputs** — the model emits secrets, malware, or hallucinated facts that downstream code trusts
- **Agents/tools** — an LLM wired to tools can be steered, via injection, to *do* things

---

## AI Pipeline Threat Surface

![ai pipeline](svg/courses/security/secure-coding/08_secure_ai/ai_pipeline.svg)

---

## Training Data Integrity And Poisoning

- **Data poisoning** — attacker injects crafted samples so the model learns the wrong thing
    - Availability attack: degrade accuracy broadly
    - **Backdoor / trojan**: model behaves normally except on a secret trigger pattern
- Web-scraped corpora are easy to poison — you do not control what is on the internet
- Defenses: vet and document data **provenance**; deduplicate; anomaly-detect outliers; hold out clean eval sets; checksum and version datasets like any other artifact
- Fine-tuning data is a smaller, higher-leverage target — review it carefully
- Treat "where did this data come from?" as a first-class supply-chain question

---

## Model Security And IP Protection

- The trained model is expensive IP — and an asset others want to steal or clone
- **Model extraction** — querying the API enough to train a functional copy; rate-limit, monitor query patterns, watermark outputs
- **Membership inference / memorization** — probing whether a specific record was in the training set; mitigate with deduplication, differential privacy, and not training on data you cannot expose
- **Unsafe model formats** — `pickle`-based checkpoints execute arbitrary code on load; prefer `safetensors`; scan model files; only load models from sources you trust
- Protect weights at rest like any crown-jewel secret: encryption, access control, signed releases

---

## Adversarial Attacks And Defenses

- **Evasion / adversarial examples** — small, often imperceptible input perturbations that flip the prediction (the classic "panda → gibbon" image)
- **Prompt injection** (the LLM version) — attacker text in the input (or in a fetched web page / document) overrides your instructions; **indirect** injection through retrieved content is the nasty case
- **Jailbreaks** — coax the model past its safety alignment
- Defenses: input validation and sanitization; **never trust model output** — treat it as untrusted data, sandbox any tool calls, require human approval for sensitive actions; least privilege for the model's tools; adversarial testing / red-teaming; output filtering; defense in depth (no single guardrail is enough)
- Reference: `OWASP` `Top` 10 for LLM Applications, `OWASP` ML Security `Top` 10, `MITRE` ATLAS

---

## Secure Deployment Of AI Models

- **Isolate inference** — sandbox it; if it calls tools, scope each tool to least privilege
- **Validate inputs, filter outputs** — at both ends of the model
- **Rate-limit and monitor** — for extraction attempts, abuse, cost spikes ("denial of wallet")
- **Log** prompts and responses (mind the PII) so you can investigate incidents
- **Version and sign** model artifacts; track which model version served which request
- **Human in the loop** for high-impact decisions — do not let a probabilistic system act unchecked
- **Have a rollback** — a bad model deploy is an incident; treat it like one

---

## NIST SP 800-218A — Secure Development For Generative AI

- A companion profile to the `SSDF` (SP 800-218) for generative `AI` and dual-use foundation models
- Extends the same four practice groups (PO, PS, PW, RV) with `AI`-specific tasks:
    - **Data**: govern provenance, integrity, and appropriateness of training and fine-tuning data
    - **Model supply chain**: vet third-party models and components; protect model artifacts from tampering
    - **Evaluation**: red-team for misuse, harmful outputs, and emergent behavior before release
    - **Disclosure**: document model limitations, intended use, and known risks; handle reported issues
- It is the federal-procurement-facing baseline for secure `AI` development — read it alongside the `OWASP` `AI`/`ML` `Top` 10 lists

---

## Takeaways

- `AI` adds risks on top of everything else — datasets and models are now part of your supply chain
- Poisoning and backdoors come in through training data — demand and document data provenance
- Treat model output as **untrusted input**: sandbox tools, validate, filter, keep a human in the loop
- Use safe model formats (`safetensors`), scan and sign model artifacts, rate-limit and monitor the API
- Follow `NIST` SP 800-218A and the `OWASP` `AI`/`ML` `Top` 10 — and remember the earlier chapters still apply
