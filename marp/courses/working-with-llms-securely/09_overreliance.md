# LLM09: Overreliance
## Mark Veltzer
### Senior Software Engineer

---

## What Is Overreliance?

Overreliance occurs when users or systems **trust `LLM` output without adequate verification**, leading to the acceptance of incorrect, fabricated, or misleading information

- Ranked **#9** in the OWASP Top 10 for LLM Applications
- `LLMs` produce text that is **fluent and confident** regardless of correctness
- Two core problems:
    - **Hallucination**: the model generates plausible but factually wrong content
    - **Unwarranted trust**: users assume correctness because the output sounds authoritative

The more convincing the output, the more dangerous overreliance becomes.

---

## Why LLMs Hallucinate

`LLMs` are **next-token predictors**, not knowledge databases. They generate text that is statistically likely, not necessarily true.

```text
Common hallucination categories:

1. FACTUAL FABRICATION
   Inventing facts, dates, names, or statistics
   "The Python GIL was removed in version 3.9" (false)

1. CITATION HALLUCINATION
   Generating fake references that look real
   "According to Smith et al. (2021) in Nature..." (paper doesn't exist)

1. CODE HALLUCINATION
   Using non-existent APIs, functions, or parameters
   "Use requests.get(url, verify_ssl=True)" (wrong parameter name)

1. CONFIDENT INCORRECTNESS
   Providing wrong answers with absolute certainty
   "This is O(n) complexity" (actually O(n²))
```

---

## The Danger: Automation of Wrong Answers

<svg viewBox="0 0 800 280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="or1" markerWidth="10" markerHeight="10" refX="10" refY="5" orient="auto">
      <polygon points="0 0, 10 5, 0 10" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="50" width="160" height="60" fill="#3498db" rx="8"/>
  <text x="110" y="75" text-anchor="middle" fill="white" font-size="12" font-weight="bold">User asks LLM</text>
  <text x="110" y="92" text-anchor="middle" fill="white" font-size="11">for code / facts / advice</text>
  <line x1="190" y1="80" x2="260" y2="80" stroke="#333" stroke-width="2" marker-end="url(#or1)"/>
  <rect x="270" y="50" width="160" height="60" fill="#e67e22" rx="8"/>
  <text x="350" y="75" text-anchor="middle" fill="white" font-size="12" font-weight="bold">LLM responds</text>
  <text x="350" y="92" text-anchor="middle" fill="white" font-size="11">confidently but wrong</text>
  <line x1="430" y1="80" x2="500" y2="80" stroke="#333" stroke-width="2" marker-end="url(#or1)"/>
  <rect x="510" y="30" width="160" height="40" fill="#e74c3c" rx="8"/>
  <text x="590" y="55" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Deployed to production</text>
  <rect x="510" y="80" width="160" height="40" fill="#e74c3c" rx="8"/>
  <text x="590" y="105" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Published as fact</text>
  <rect x="510" y="130" width="160" height="40" fill="#e74c3c" rx="8"/>
  <text x="590" y="155" text-anchor="middle" fill="white" font-size="11" font-weight="bold">Used in legal/medical context</text>
  <line x1="430" y1="80" x2="500" y2="50" stroke="#333" stroke-width="1" stroke-dasharray="4,4"/>
  <line x1="430" y1="80" x2="500" y2="150" stroke="#333" stroke-width="1" stroke-dasharray="4,4"/>
  <text x="400" y="230" text-anchor="middle" fill="#c0392b" font-size="13" font-weight="bold">Without verification, hallucinated content enters real-world systems unchecked</text>
</svg>

---

## Real-World Overreliance Failures

- **Legal filings with fake citations** (2023): A lawyer used `ChatGPT` to draft a brief that cited six court cases. None of them existed. The lawyer was sanctioned by the court.
- **Security vulnerabilities from generated code**: `LLM`-generated code frequently contains insecure patterns such as missing input validation, hardcoded credentials, or use of deprecated cryptographic functions
- **Medical misinformation**: `LLMs` have generated plausible but incorrect drug interaction information and dosage recommendations
- **Financial analysis errors**: Hallucinated financial data and statistics used in reports without fact-checking

Each case shares the same root cause: **the output sounded correct, so nobody verified it**.

---

## Overreliance in Software Development

```python
# Developer asks LLM: "Parse this user-provided date string"
# LLM responds with confident but vulnerable code:

from datetime import datetime

def parse_user_date(date_str: str) -> datetime:
    # LLM-generated: no input validation, no error handling,
    # and uses a format string that may not match user input
    return datetime.strptime(date_str, "%Y-%m-%d")

# PROBLEMS the developer might miss if they trust blindly:
# 1. No try/except for malformed input -> unhandled crash
# 2. No length limit on date_str -> potential DoS
# 3. Assumes one specific format -> breaks with other locales
# 4. No timezone awareness -> subtle bugs in production
```

The code compiles and works for the happy path, which makes developers less likely to question it

---

## Verification Strategy 1: Never Trust, Always Verify

Treat every `LLM` output as an **unverified draft** that requires human review

```python
@dataclass
class LLMOutput:
    content: str
    verified: bool = False
    verification_notes: str = ""
    verified_by: str = ""

def process_llm_response(raw_output: str) -> LLMOutput:
    output = LLMOutput(content=raw_output)
    # Flag for mandatory review before use
    if contains_code(raw_output):
        output.verification_notes = "Code: requires review and testing"
    if contains_factual_claims(raw_output):
        output.verification_notes = "Claims: requires fact-checking"
    return output

def use_output(output: LLMOutput):
    if not output.verified:
        raise ValueError(
            "LLM output must be verified before use"
        )
    return output.content
```

---

## Verification Strategy 2: Automated Fact-Checking

Use programmatic checks to validate `LLM` claims against known data sources

```python
def verify_code_output(llm_code: str) -> dict:
    """Automated checks for LLM-generated code."""
    results = {
        "syntax_valid": False,
        "tests_pass": False,
        "linter_clean": False,
        "security_scan_clean": False,
    }
    # 1. Syntax check
    try:
        compile(llm_code, "<llm>", "exec")
        results["syntax_valid"] = True
    except SyntaxError:
        return results
    # 2. Run through linter
    results["linter_clean"] = run_linter(llm_code)
    # 3. Static security analysis
    results["security_scan_clean"] = run_bandit(llm_code)
    # 4. Run against test suite
    results["tests_pass"] = run_tests(llm_code)
    return results
```

Automated checks catch the obvious errors. Human review catches the subtle ones.

---

## Verification Strategy 3: Cross-Referencing

Validate `LLM` outputs by checking them against **multiple independent sources**

```python
def cross_reference_claim(claim: str) -> dict:
    """Verify a factual claim against multiple sources."""
    sources = [
        query_knowledge_base(claim),
        query_official_docs(claim),
        query_second_llm(claim),  # Different model
    ]
    agreement = calculate_agreement(sources)
    return {
        "claim": claim,
        "sources_checked": len(sources),
        "agreement_score": agreement,
        "verified": agreement > 0.8,
        "conflicting_sources": [
            s for s in sources if not s.agrees
        ],
    }
```

If multiple independent sources disagree with the `LLM`, the `LLM` is likely wrong

---

## Verification Strategy 4: Constrained Output Formats

Force `LLM` outputs into **structured formats** that are easier to validate programmatically

```python
from pydantic import BaseModel, validator

class LLMCodeReview(BaseModel):
    """Structured output that can be validated."""
    language: str
    has_input_validation: bool
    has_error_handling: bool
    has_sql_injection_risk: bool
    suggested_fix: str

    @validator("language")
    def valid_language(cls, v):
        allowed = {"python", "javascript", "go", "rust"}
        if v.lower() not in allowed:
            raise ValueError(f"Unknown language: {v}")
        return v.lower()

# Force LLM to return JSON matching the schema
response = client.chat.completions.create(
    model="gpt-4",
    messages=[...],
    response_format={"type": "json_object"},
)
review = LLMCodeReview.parse_raw(response.choices[0].message.content)
```

---

## User Education: Trust Calibration

Users must understand what `LLMs` can and cannot do reliably

```text
WHAT LLMs ARE GOOD AT:          WHAT LLMs ARE BAD AT:
--------------------------       --------------------------
Drafting and brainstorming       Precise factual recall
Summarizing long documents       Mathematical calculations
Explaining concepts              Citing real sources
Code scaffolding                 Knowing current events
Pattern recognition              Consistent logical reasoning
Translation and rephrasing       Counting and exact measurements
```

Key messages for user training:
- An `LLM` is a **writing assistant**, not an oracle
- Confidence in tone does not equal confidence in accuracy
- Always verify claims that will inform decisions
- If you cannot verify it, do not rely on it

---

## Designing UIs That Discourage Overreliance

Applications should **signal uncertainty** rather than present `LLM` output as authoritative fact

```text
BAD UI PATTERN:
  +--------------------------------------+
  | Answer: Python 3.9 removed the GIL   |
  +--------------------------------------+

GOOD UI PATTERN:
  +--------------------------------------+
  | AI-Generated Draft (unverified)      |
  | Python 3.9 removed the GIL           |
  |                                      |
  | ⚠ This response may contain errors. |
  | Please verify before using.          |
  | [Mark as Verified] [Report Error]    |
  +--------------------------------------+
```

UI elements that help:
- Prominent disclaimers on `LLM` output
- Confidence scores where available
- "Verify" and "Report Error" buttons
- Links to authoritative sources for fact-checking

---

## Organizational Policies for LLM Use

Establish clear guidelines for when and how `LLM` output can be used

```text
POLICY EXAMPLE: LLM-Generated Code

1. ALL LLM-generated code MUST go through standard code review
1. LLM-generated code MUST NOT be committed without tests
1. Security-sensitive code (auth, crypto, input validation)
   MUST be written or reviewed by a senior engineer
1. LLM-generated code MUST be attributed in commit messages
1. Developers are responsible for code they submit,
   regardless of whether an LLM generated it

POLICY EXAMPLE: LLM-Generated Content

1. Factual claims MUST be verified against primary sources
1. Legal or compliance text MUST be reviewed by legal counsel
1. Customer-facing content MUST go through editorial review
1. Medical or safety-related content is PROHIBITED
```

---

## Implementing Guardrails in Production

```python
class OverrelianceGuard:
    def __init__(self):
        self.claim_checker = ClaimVerifier()
        self.code_checker = CodeVerifier()

    def process(self, llm_output: str,
                output_type: str) -> dict:
        result = {"content": llm_output, "safe_to_use": False}
        if output_type == "factual":
            claims = extract_claims(llm_output)
            verified = [
                self.claim_checker.verify(c) for c in claims
            ]
            unverified = [c for c, v in zip(claims, verified)
                          if not v]
            result["unverified_claims"] = unverified
            result["safe_to_use"] = len(unverified) == 0
        elif output_type == "code":
            checks = self.code_checker.verify(llm_output)
            result["checks"] = checks
            result["safe_to_use"] = all(checks.values())
        else:
            result["warning"] = "Unverified LLM output"
        return result
```

---

## Key Takeaways

- `LLMs` hallucinate because they are **statistical text generators**, not knowledge systems. Fluent output does not mean correct output.
- Overreliance is an **organizational and human problem**, not just a technical one. Users must be trained to treat `LLM` output as unverified drafts.
- Implement **multiple verification strategies**: automated checks for code, cross-referencing for facts, structured output for validation.
- Design UIs that **signal uncertainty** with disclaimers, confidence scores, and verification buttons rather than presenting output as authoritative.
- Establish **organizational policies** that require review, testing, and attribution for `LLM`-generated code and content.
- The responsibility for correctness lies with the **human who uses the output**, not with the `LLM` that generated it.
