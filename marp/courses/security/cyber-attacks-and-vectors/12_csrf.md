---
tags:
  - security:security
  - security:cyber-attacks
  - security:penetration-testing
  - security:vulnerabilities
level: intermediate
category: security
audience:
  - audiences:developers
  - audiences:security-professionals

---

# Cross-Site Request Forgery (CSRF)

---
## What is CSRF?

- CSRF stands for Cross-Site Request Forgery
- Also known as XSRF, "Sea Surf", or Session Riding
- A type of web security vulnerability
- Allows an attacker to induce users to perform actions they do not intend to do

---
## How CSRF Works

1. Attacker creates a malicious website or email
1. Victim is authenticated on a target site
1. Victim visits the malicious site or opens the email
1. Malicious content triggers an unwanted action on the target site
1. Action is performed with the victim's privileges

---
## CSRF Attack Example

```html
<img src="http://bank.com/transfer?amount=1000&to=attacker"/>
```

- Hidden in a seemingly innocent page
- When loaded, it triggers a fund transfer
- Uses the victim's active session on bank.com

---
## Why CSRF is Dangerous

- Exploits the trust a website has in a user's browser
- Can perform any action the user is authorized to do
- Often targets high-privilege users (e.g., admins)
- Can lead to:
    - Unauthorized transactions
    - Data theft
    - Account compromise

---
## Defending Against CSRF

1. CSRF Tokens
1. Same-Site Cookies
1. Custom Request Headers
1. Double Submit Cookies
1. User Interaction demands

---
## CSRF Tokens

- Unique, unpredictable token for each session
- Server generates and sends token with each form
- Client must include valid token with each request
- Server verifies the token before processing the request

Example:

```html
<form action="/transfer" method="POST">
  <input type="hidden" name="csrf_token" value="randomtoken123">
  <!-- other form fields -->
</form>
```

---
## Same-Site Cookies
- Set the `SameSite` attribute on cookies
- Prevents the browser from sending cookies in cross-site requests
- Options:
    - `Strict`: Never send cookies for cross-site requests
    - `Lax`: Send cookies for top-level GET requests

Example:

```http
Set-Cookie: session=abc123; SameSite=Strict; Secure
```

---
## Custom Request Headers
- Leverage the Same-Origin Policy for custom headers
- Add a custom header to AJAX requests
- Server verifies the presence of this header

Example:

```javascript
fetch('/api/data', {
  headers: {
    'X-Requested-With': 'XMLHttpRequest'
  }
})
```

---
## Double Submit Cookies
1. Set a random token as a cookie
1. Include the same token as a hidden field in forms
1. Server verifies that both values match

Example:

```http
Set-Cookie: csrf_token=abc123; SameSite=Strict
<form>
  <input type="hidden" name="csrf_token" value="abc123">
</form>
```

---
## User Interaction Requirements

- Require user interaction for sensitive actions
- Examples:
    - Re-authentication
    - CAPTCHA
    - Confirmation dialogs

- Makes it harder for attackers to automate CSRF attacks

---

## Best Practices

- Implement multiple layers of protection
- Use HTTPS to prevent token theft
- Avoid using GET requests for state-changing operations
- Keep software and frameworks up-to-date
- Educate users about safe browsing habits

---

## CSRF Attack Flow Diagram

![csrf_attack_flow_diagram](svg/courses/security/cyber-attacks-and-vectors/12_csrf/csrf_attack_flow_diagram.svg)

---

## Advanced CSRF Attack Techniques

```html
<!-- Auto-submitting form (POST-based CSRF) -->
<html>
<body onload="document.forms[0].submit()">
<form action="https://bank.com/transfer" method="POST">
    <input type="hidden" name="to" value="attacker_account"/>
    <input type="hidden" name="amount" value="10000"/>
</form>
</body>
</html>

<!-- AJAX-based CSRF (if CORS is misconfigured) -->
<script>
fetch('https://bank.com/api/transfer', {
    method: 'POST',
    credentials: 'include',  // Sends cookies
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({to: 'attacker', amount: 10000})
});
</script>

<!-- Image tag CSRF (GET-based) -->
<img src="https://bank.com/transfer?to=attacker&amount=10000"
     style="display:none"/>
<!-- Browser sends GET with cookies automatically -->
```

---

## CSRF Token Implementation: Python Flask

```python
from flask import Flask, session, request, abort
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Generate CSRF token per session
def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return session['csrf_token']

# Make token available in all templates
app.jinja_env.globals['csrf_token'] = generate_csrf_token

# Validate CSRF token on state-changing requests
@app.before_request
def check_csrf():
    if request.method in ('POST', 'PUT', 'DELETE'):
        token = request.form.get('csrf_token') or \
                request.headers.get('X-CSRF-Token')
        if not token or token != session.get('csrf_token'):
            abort(403, 'CSRF token validation failed')

@app.route('/transfer', methods=['POST'])
def transfer():
    # CSRF token already validated by before_request
    to_account = request.form['to']
    amount = request.form['amount']
    # Process transfer...
    return 'Transfer complete'
```

```html
<!-- Template with CSRF token -->
<form action="/transfer" method="POST">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    To: <input name="to">
    Amount: <input name="amount">
    <button type="submit">Transfer</button>
</form>
```

---

## SameSite Cookie Comparison

| SameSite Value | Cross-site POST | Cross-site GET (top-level) | Same-site |
|----------------|----------------|---------------------------|-----------|
| `Strict`       | Blocked        | Blocked                   | Sent      |
| `Lax`          | Blocked        | Sent                      | Sent      |
| `None`         | Sent           | Sent                      | Sent      |

```python
# Flask: Set SameSite cookies
from flask import make_response

@app.route('/login', methods=['POST'])
def login():
    resp = make_response(redirect('/dashboard'))
    resp.set_cookie(
        'session_id',
        value=session_token,
        secure=True,       # HTTPS only
        httponly=True,      # Not accessible via JS
        samesite='Lax'     # Blocks cross-site POST
    )
    return resp
```

---

## Real-World CSRF Case Studies

| Incident                | Year | Impact                                  |
|------------------------|------|-----------------------------------------|
| Netflix CSRF           | 2006 | Change account email, enable DVD ship   |
| Gmail filter injection | 2007 | Create email forwarding rules silently   |
| ING Direct             | 2008 | Transfer funds between accounts          |
| YouTube CSRF           | 2008 | Subscribe, add favorites as victim       |
| WordPress              | 2015 | Multiple CSRF vulnerabilities in admin   |

---

## Exercise: CSRF Lab

1. Build a simple banking application with Flask:
   - Login page with session management
   - Transfer money endpoint (POST-based)
   - Account balance display
1. Create an attacker page that performs CSRF:
   - Auto-submitting hidden form
   - Image-based GET request
1. Verify the attack works (money transferred without user consent)
1. Implement defenses one by one and test each:
   - CSRF tokens in all forms
   - SameSite=Lax cookies
   - Custom header validation (X-Requested-With)
1. Verify each defense blocks the CSRF attack
1. Test edge cases: What about JSON API endpoints?
