# OS & Server Hardening

## Reducing the Attack Surface at the Infrastructure Level

---

## Why Hardening Matters

```text
Default Installation = Maximum Attack Surface

+--Default Install--+     +--Hardened Install--+
| All services on   |     | Minimal services   |
| Default passwords |     | Strong passwords   |
| Verbose errors    |     | Generic errors     |
| No firewall       |     | Strict firewall    |
| No logging        |     | Full audit logging |
| Root access       |     | Least privilege    |
| No updates        |     | Patch management   |
+-------------------+     +--------------------+
```

---

## Linux Server Hardening Checklist

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Remove unnecessary packages
sudo apt autoremove -y
sudo apt purge telnet ftp rsh-client

# 3. Disable unnecessary services
sudo systemctl disable bluetooth cups avahi-daemon
sudo systemctl list-unit-files --state=enabled

# 4. Configure SSH securely
sudo vi /etc/ssh/sshd_config
# PermitRootLogin no
# PasswordAuthentication no  (use keys only)
# MaxAuthTries 3
# AllowUsers deploy admin
# Port 2222  (change from default)

# 5. Set strong password policy
sudo apt install libpam-pwquality
# /etc/security/pwquality.conf
# minlen = 14
# dcredit = -1
# ucredit = -1
# lcredit = -1
# ocredit = -1
```

---

## File System Hardening

```bash
# Secure /tmp with noexec
# /etc/fstab entry:
tmpfs /tmp tmpfs defaults,noexec,nosuid,nodev 0 0

# Set proper permissions on critical files
chmod 600 /etc/shadow
chmod 644 /etc/passwd
chmod 600 /etc/ssh/sshd_config
chmod 700 /root

# Find world-writable files
find / -xdev -type f -perm -0002 -ls

# Find SUID binaries (potential privilege escalation)
find / -xdev -perm -4000 -type f -ls

# Remove unnecessary SUID bits
chmod u-s /usr/bin/unnecessary_program

# Enable filesystem auditing
auditctl -w /etc/passwd -p wa -k passwd_changes
auditctl -w /etc/shadow -p wa -k shadow_changes
```

---

## Host-Based Firewall (iptables/nftables)

```bash
# Basic iptables rules for a web server

# Flush existing rules
iptables -F

# Default policies: DROP everything
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH (from specific IP)
iptables -A INPUT -p tcp --dport 22 -s 10.0.0.0/24 -j ACCEPT

# Allow HTTP and HTTPS
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Drop everything else (implicit via policy)

# Save rules
iptables-save > /etc/iptables/rules.v4
```

---

## UFW - Simplified Firewall

```bash
# Ubuntu Uncomplicated Firewall

# Enable UFW
sudo ufw enable

# Default deny incoming, allow outgoing
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow specific services
sudo ufw allow 22/tcp     # SSH
sudo ufw allow 80/tcp     # HTTP
sudo ufw allow 443/tcp    # HTTPS

# Allow from specific IP
sudo ufw allow from 10.0.0.0/24 to any port 22

# Rate limiting on SSH
sudo ufw limit ssh

# Check status
sudo ufw status verbose

# Application profiles
sudo ufw app list
sudo ufw allow 'Nginx Full'
```

---

## Logging & Monitoring

```bash
# Essential logs to monitor
/var/log/auth.log        # Authentication attempts
/var/log/syslog          # System events
/var/log/kern.log        # Kernel messages
/var/log/apache2/        # Apache logs
/var/log/nginx/          # Nginx logs
/var/log/mysql/          # MySQL logs
/var/log/fail2ban.log    # Brute-force protection

# Centralized logging with rsyslog
# /etc/rsyslog.conf
*.* @@logserver.internal:514

# Log rotation
# /etc/logrotate.d/custom
/var/log/myapp/*.log {
    daily
    rotate 90
    compress
    missingok
    notifempty
    create 640 www-data adm
}
```

---

## Fail2Ban - Automated Intrusion Prevention

```bash
# Install
sudo apt install fail2ban

# Configuration: /etc/fail2ban/jail.local
[DEFAULT]
bantime = 3600            # Ban for 1 hour
findtime = 600            # Within 10 minutes
maxretry = 5              # After 5 failures
banaction = iptables-multiport

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3

[nginx-http-auth]
enabled = true
port = http,https
filter = nginx-http-auth
logpath = /var/log/nginx/error.log

# Check status
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

---

## Web Server Hardening - Nginx

```nginx
# /etc/nginx/nginx.conf

# Hide version number
server_tokens off;

# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# Disable unnecessary methods
if ($request_method !~ ^(GET|HEAD|POST)$) {
    return 444;
}

# Limit request body size
client_max_body_size 10m;

# Rate limiting
limit_req_zone $binary_remote_addr zone=login:10m rate=5r/m;
location /login {
    limit_req zone=login burst=3 nodelay;
}
```

---

## Web Server Hardening - Apache

```apache
# /etc/apache2/conf-enabled/security.conf

# Hide version
ServerTokens Prod
ServerSignature Off

# Disable directory listing
<Directory /var/www/html>
    Options -Indexes
</Directory>

# Disable TRACE method
TraceEnable Off

# Security headers
Header always set X-Frame-Options "SAMEORIGIN"
Header always set X-Content-Type-Options "nosniff"
Header always set X-XSS-Protection "1; mode=block"
Header always set Strict-Transport-Security "max-age=31536000"
Header always set Content-Security-Policy "default-src 'self'"

# Limit request size
LimitRequestBody 10485760

# Disable unnecessary modules
# a2dismod status info autoindex
```

---

## TLS Configuration Best Practices

```nginx
# Nginx TLS configuration
server {
    listen 443 ssl http2;

    ssl_certificate /etc/ssl/certs/server.crt;
    ssl_certificate_key /etc/ssl/private/server.key;

    # Protocols - TLS 1.2 and 1.3 only
    ssl_protocols TLSv1.2 TLSv1.3;

    # Strong cipher suites
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;

    # OCSP stapling
    ssl_stapling on;
    ssl_stapling_verify on;

    # DH parameters (generate: openssl dhparam -out dhparam.pem 4096)
    ssl_dhparam /etc/ssl/dhparam.pem;

    # Session settings
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;
}
```

---

## Database Hardening

```sql
-- MySQL/MariaDB hardening

-- 1. Run the security script
-- mysql_secure_installation

-- 2. Remove anonymous users
DELETE FROM mysql.user WHERE User='';

-- 3. Remove test database
DROP DATABASE IF EXISTS test;

-- 4. Create application-specific user with minimal privileges
CREATE USER 'webapp'@'localhost' IDENTIFIED BY 'strong_random_password';
GRANT SELECT, INSERT, UPDATE ON webapp_db.* TO 'webapp'@'localhost';
-- NO DELETE, DROP, CREATE, ALTER, FILE, PROCESS, SUPER

-- 5. Disable remote root login
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');

-- 6. Enable logging
-- /etc/mysql/mysql.conf.d/mysqld.cnf
-- general_log = 1
-- log_error = /var/log/mysql/error.log
-- slow_query_log = 1

FLUSH PRIVILEGES;
```

---

## Application-Level Hardening

```python
# Django settings.py - Security configuration
DEBUG = False                          # NEVER True in production
ALLOWED_HOSTS = ['www.example.com']    # Specific hosts only

# Security middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # ...
]

# Cookie settings
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
```

---

## Container Security (Docker)

```dockerfile
# Secure Dockerfile practices

# Use specific version, not 'latest'
FROM node:18-alpine

# Create non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set working directory
WORKDIR /app

# Copy only needed files
COPY package*.json ./
RUN npm ci --only=production

COPY --chown=appuser:appgroup . .

# Run as non-root
USER appuser

# Don't expose unnecessary ports
EXPOSE 3000

# Use exec form for signal handling
CMD ["node", "server.js"]
```

```bash
# Runtime security
docker run --read-only --tmpfs /tmp \
  --security-opt=no-new-privileges \
  --cap-drop=ALL \
  --network=app-network \
  myapp:1.0
```

---

## Vulnerability Scanning

```bash
# Automated vulnerability scanning tools

# OpenVAS/Greenbone - Network vulnerability scanner
# sudo gvm-setup && gvm-start

# Lynis - System auditing
sudo lynis audit system
sudo lynis audit system --pentest

# CIS Benchmarks
# Follow Center for Internet Security configuration guides

# Docker security scanning
docker scan myimage:latest
trivy image myimage:latest

# Web application scanning
nikto -h https://target.com
nuclei -u https://target.com -severity critical,high
```

---

## WAF (Web Application Firewall)

```text
WAF Deployment Modes:
+--Inline (Blocking)-------+
| Request -> WAF -> Server |
| WAF blocks attacks       |
+--------------------------+

+--Out-of-band (Detection)-+
| Request -> Server        |
| Copy -> WAF (alerts)     |
+--------------------------+

Popular WAFs:
  - ModSecurity (open source, Apache/Nginx)
  - AWS WAF (cloud-native)
  - Cloudflare WAF (CDN-integrated)
  - Imperva / Akamai (enterprise)

WAF Limitations:
  - Can be bypassed with encoding tricks
  - May cause false positives
  - Not a substitute for secure code
  - Cannot detect logic flaws
```

---

## ModSecurity Configuration

```apache
# ModSecurity with OWASP Core Rule Set (CRS)

# Enable ModSecurity
SecRuleEngine On

# Set request body limit
SecRequestBodyLimit 13107200
SecRequestBodyNoFilesLimit 131072

# Enable logging
SecAuditEngine RelevantOnly
SecAuditLog /var/log/modsec_audit.log

# OWASP CRS rules
Include /etc/modsecurity/crs/crs-setup.conf
Include /etc/modsecurity/crs/rules/*.conf

# Custom rule example: Block SQL injection patterns
SecRule ARGS "@rx (?i)(union.*select|sleep\s*\(|benchmark\s*\()" \
    "id:1001,phase:2,deny,status:403,msg:'SQL Injection Attempt'"

# Custom rule: Block XSS patterns
SecRule ARGS "@rx <script" \
    "id:1002,phase:2,deny,status:403,msg:'XSS Attempt'"
```

---

## Supply Chain Security

```text
Third-party dependencies are a major attack vector:

Package Manager Risks:
- npm (JavaScript): typosquatting, malicious packages
- pip (Python): dependency confusion
- Maven (Java): compromised libraries
- NuGet (.NET): vulnerable packages

Defense measures:
1. Lock dependency versions (package-lock.json, Pipfile.lock)
2. Audit dependencies regularly:
   npm audit
   pip-audit
   mvn dependency-check:check

3. Use private registries for internal packages
4. Verify package integrity (checksums, signatures)
5. Monitor for new CVEs in dependencies:
   - Dependabot (GitHub)
   - Snyk
   - OWASP Dependency-Check

6. Pin specific versions, don't use ranges
   "lodash": "4.17.21"      (GOOD)
   "lodash": "^4.17.0"      (RISKY)

7. Review new dependencies before adding them
```

---

## Incident Response Preparation

```text
Incident Response Plan for Web Attacks:

1. PREPARATION
   - Define incident response team roles
   - Establish communication channels
   - Prepare forensic tools and runbooks
   - Set up centralized logging

2. IDENTIFICATION
   - Monitor WAF alerts and log anomalies
   - Check for unauthorized access patterns
   - Look for data exfiltration indicators

3. CONTAINMENT
   - Block attacker IP at firewall
   - Disable compromised accounts
   - Isolate affected servers

4. ERADICATION
   - Patch the exploited vulnerability
   - Remove backdoors and web shells
   - Reset all potentially compromised credentials

5. RECOVERY
   - Restore from clean backups
   - Verify system integrity
   - Gradually restore services

6. LESSONS LEARNED
   - Document the incident timeline
   - Update security controls
   - Improve detection capabilities
```

---

## Security Monitoring & Alerting

```bash
# Key events to alert on:

# Failed login attempts (threshold)
grep "Failed password" /var/log/auth.log | \
  awk '{print $11}' | sort | uniq -c | sort -rn

# Web application errors (500s)
awk '$9 ~ /^5/ {print $0}' /var/log/nginx/access.log

# Suspicious user agents
grep -iE "(sqlmap|nikto|nmap|dirbuster|gobuster)" \
  /var/log/nginx/access.log

# Path traversal attempts
grep -iE "(\.\.\/|\.\.\\\\)" /var/log/nginx/access.log

# SQL injection attempts
grep -iE "(union.*select|sleep\(|benchmark\()" \
  /var/log/nginx/access.log

# Large file downloads (data exfiltration)
awk '$10 > 10000000 {print $0}' /var/log/nginx/access.log

# Consider SIEM: ELK Stack, Splunk, Graylog
# For automated alerting and correlation
```

---

## Hardening Assessment Checklist

```text
Operating System:
[ ] System packages updated
[ ] Unnecessary services disabled
[ ] Strong password policy enforced
[ ] SSH hardened (key-only, non-root)
[ ] Filesystem permissions correct
[ ] SUID binaries reviewed

Network:
[ ] Host firewall configured (deny default)
[ ] Only required ports open
[ ] Rate limiting enabled
[ ] Fail2Ban or equivalent active

Web Server:
[ ] Version headers hidden
[ ] Directory listing disabled
[ ] Security headers configured
[ ] TLS properly configured
[ ] Unnecessary modules disabled

Application:
[ ] Debug mode disabled
[ ] Error messages generic
[ ] Session security configured
[ ] CSRF protection enabled
[ ] Input validation in place

Database:
[ ] Default credentials changed
[ ] Least privilege DB users
[ ] Remote access restricted
[ ] Logging enabled
```

---

## Summary

- Default configurations are insecure - always harden
- Least privilege applies at every layer
- Host firewalls are essential even behind network firewalls
- Logging and monitoring detect attacks in progress
- `Fail2Ban` automatically blocks brute-force attacks
- Web server headers are easy wins for security
- TLS 1.2+ with strong ciphers only
- Database users should have minimal required privileges
- Regular scanning verifies hardening effectiveness

> Tomorrow: Boot2Root & CTF
