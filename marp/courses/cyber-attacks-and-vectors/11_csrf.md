# Cross-Site Request Forgery (CSRF)
Understanding the Attack and Defense

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

```JavaScript
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
