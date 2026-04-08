# Working with `LLMs` Securely
## OWASP Top 10 for `LLM` Applications

Understanding the most critical security risks in `LLM`-based systems

---

## Why `LLM` Security Matters

- `LLMs` are being integrated into critical business applications
- Traditional security models don't fully apply
- New attack surfaces unique to `LLMs`
- Rapid adoption outpaces security awareness
- A single vulnerability can expose entire systems

---

## The `LLM` Attack Surface

![the_llm_attack_surface](svg/courses/security/working-with-llms-securely/01_introduction/the_llm_attack_surface.svg)

Every input and output channel is a potential attack vector

---

## What is OWASP?

- **Open Worldwide Application Security Project**
- Non-profit foundation focused on software security
- Known for the "OWASP Top 10" web vulnerabilities list
- In 2023, launched the **OWASP Top 10 for `LLM` Applications**
- Community-driven, vendor-neutral guidance

---

## OWASP Top 10 for `LLM` Applications

| #     | Vulnerability                      |
|-------|------------------------------------|
| LLM01 | Prompt Injection                  |
| LLM02 | Insecure Output Handling          |
| LLM03 | Training Data Poisoning           |
| LLM04 | Model Denial of Service           |
| LLM05 | Supply Chain Vulnerabilities      |

---

## OWASP Top 10 for `LLM` Applications (cont.)

| #     | Vulnerability                      |
|-------|------------------------------------|
| LLM06 | Sensitive Information Disclosure  |
| LLM07 | Insecure Plugin Design            |
| LLM08 | Excessive Agency                  |
| LLM09 | Overreliance                      |
| LLM10 | Model Theft                       |

---

## Threat Modeling for `LLM` Applications

Key questions to ask:

- **What data** does the `LLM` have access to?
- **What actions** can the `LLM` perform?
- **Who** can interact with the `LLM`?
- **What external data** feeds into the `LLM`?
- **What trust boundaries** exist?

---

## `LLM` Application Architecture

![llm_application_architecture](svg/courses/security/working-with-llms-securely/01_introduction/llm_application_architecture.svg)

Security must be applied at every layer

---

## Trust Boundaries in `LLM` Systems

- **User ↔ Application**: Never trust user input
- **Application ↔ `LLM`**: The `LLM` is not a trusted component
- **`LLM` ↔ Tools/Plugins**: Outputs must be validated
- **`LLM` ↔ Data Sources**: External data may be adversarial
- **`LLM` ↔ Training Data**: Training data may be poisoned

---

## Key Principle: `LLMs` Are Not Trusted Components

> Treat `LLM` output the same way you treat user input: **never trust it**

- `LLMs` can be manipulated through their inputs
- `LLMs` can hallucinate or produce incorrect output
- `LLMs` have no concept of security boundaries
- The application layer must enforce all security policies

---

## Defense in Depth for `LLM` Applications

1. **Input validation** — sanitize and constrain user inputs
1. **Prompt engineering** — design system prompts defensively
1. **Output validation** — treat `LLM` outputs as untrusted
1. **Least privilege** — minimize what the `LLM` can access
1. **Monitoring** — log and alert on suspicious patterns
1. **Human oversight** — keep humans in the loop for critical actions

---

## Course Roadmap

We will cover each of the OWASP Top 10 `LLM` vulnerabilities:

- **Understanding** the vulnerability
- **Real-world examples** of exploitation
- **Hands-on exercises** to identify and exploit
- **Mitigation strategies** to defend against each
- **Architecture patterns** for secure `LLM` integration
