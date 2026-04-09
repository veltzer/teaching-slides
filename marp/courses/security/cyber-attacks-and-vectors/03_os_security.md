# Basic OS Security

---
## OS Security Fundamentals

- Access Controls
- Authentication and Authorization
- Secure Configuration
- Patching and Updates
- Data Protection

---

## Access Controls

- User Account Management
- Password Policies
- Principle of Least Privilege
- File System Permissions

---

## Linux File Permissions Deep Dive

```bash
# Understanding permission bits
# rwxrwxrwx = owner/group/others
# r=4, w=2, x=1

# List file permissions
ls -la /etc/shadow
# -rw-r----- 1 root shadow 1234 Jan 1 00:00 /etc/shadow

# Set restrictive permissions on sensitive files
chmod 600 ~/.ssh/id_rsa       # Only owner can read/write
chmod 700 ~/.ssh              # Only owner can access directory
chmod 644 /etc/passwd         # Owner write, everyone read

# Find world-writable files (security risk)
find / -perm -o+w -type f 2>/dev/null

# Find SUID binaries (potential privilege escalation)
find / -perm -4000 -type f 2>/dev/null

# Find files with no owner (orphaned files)
find / -nouser -o -nogroup 2>/dev/null
```

---

## Access Control Lists (ACLs)

ACLs provide finer-grained access control beyond traditional permissions:

```bash
# View ACLs on a file
getfacl /var/log/application.log

# Grant specific user read access without changing group
setfacl -m u:auditor:r /var/log/application.log

# Grant group write access
setfacl -m g:developers:rw /opt/app/config.yml

# Set default ACL on directory (inherited by new files)
setfacl -d -m g:developers:rw /opt/app/

# Remove all ACLs
setfacl -b /var/log/application.log
```

---

## Authentication and Authorization

- Strong Password Policies
- Multi-Factor Authentication
- Secure User Onboarding and Offboarding
- Privilege Escalation Prevention

---

## PAM (Pluggable Authentication Modules)

PAM controls authentication on Linux systems:
```bash
# /etc/pam.d/common-password - Password policy configuration
# Require minimum length 12, complexity rules
password requisite pam_pwquality.so retry=3 \
    minlen=12 dcredit=-1 ucredit=-1 \
    ocredit=-1 lcredit=-1
# /etc/pam.d/common-auth - Account lockout after failed attempts
auth required pam_faillock.so preauth deny=5 \
    unlock_time=900 audit
auth required pam_faillock.so authfail deny=5 \
    unlock_time=900 audit
# Check PAM configuration for a service
cat /etc/pam.d/sshd
```

---

## PAM (Pluggable Authentication Modules)

![check_pam_configuration_for_a_service](svg/courses/security/cyber-attacks-and-vectors/03_os_security/check_pam_configuration_for_a_service.svg)

---

## Secure Configuration

- Hardening the OS
- Disabling Unnecessary Services
- Secure Network Configuration
- Firewall Rules

---

## Linux Hardening Checklist

```bash
# 1. Disable unnecessary services
systemctl list-unit-files --type=service --state=enabled
systemctl disable cups.service        # Disable printing if not needed
systemctl disable avahi-daemon.service # Disable mDNS

# 2. Configure firewall (UFW example)
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 443/tcp
ufw enable
ufw status verbose

# 3. Secure SSH configuration (/etc/ssh/sshd_config)
# PermitRootLogin no
# PasswordAuthentication no
# MaxAuthTries 3
# AllowUsers admin deploy
# Protocol 2

# 4. Set kernel security parameters (/etc/sysctl.conf)
# net.ipv4.conf.all.rp_filter = 1
# net.ipv4.icmp_echo_ignore_broadcasts = 1
# kernel.randomize_va_space = 2
# net.ipv4.conf.all.accept_redirects = 0
sysctl -p
```

---

## CIS Benchmarks

The Center for Internet Security provides hardening baselines:

---

## CIS Benchmarks

![cis_benchmarks](svg/courses/security/cyber-attacks-and-vectors/03_os_security/cis_benchmarks.svg)

---

## CIS Benchmarks

Tools for automated compliance checking:
- **OpenSCAP**: Open-source compliance scanner
- **Lynis**: Security auditing tool for Unix/Linux
- **InSpec**: Infrastructure testing framework
```bash
# Run Lynis security audit
sudo lynis audit system
# Run OpenSCAP with CIS profile
oscap xccdf eval --profile cis \
    --results results.xml \
    /usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml
```

---

## Patching and Updates

- Timely Application of Security Patches
- Automated Patch Management
- Vulnerability Monitoring and Mitigation

---

## Patch Management Strategy

```bash
# Check for available security updates (Debian/Ubuntu)
apt list --upgradable 2>/dev/null | grep -i security

# Automatic security updates configuration
# /etc/apt/apt.conf.d/50unattended-upgrades
# Unattended-Upgrade::Allowed-Origins {
#     "${distro_id}:${distro_codename}-security";
# };

# Check when system was last updated
stat /var/log/apt/history.log

# List installed packages with known vulnerabilities
# Using tools like vulners or debian-security-tracker
apt list --installed 2>/dev/null | wc -l
```

| Patch Priority | Response Time | Example                    |
|---------------|---------------|----------------------------|
| Critical      | 24-48 hours   | Remote code execution      |
| High          | 1 week        | Privilege escalation       |
| Medium        | 30 days       | Information disclosure     |
| Low           | Next cycle    | Minor configuration issue  |

---

## Data Protection

- Encryption at Rest and in Transit
- Data Backup and Recovery
- Data Loss Prevention

---

## Encryption at Rest

```bash
# Full disk encryption with LUKS
cryptsetup luksFormat /dev/sdb1
cryptsetup luksOpen /dev/sdb1 encrypted_vol
mkfs.ext4 /dev/mapper/encrypted_vol
mount /dev/mapper/encrypted_vol /mnt/secure

# Encrypt a file with GPG
gpg --symmetric --cipher-algo AES256 sensitive_data.tar.gz

# Encrypt with OpenSSL
openssl enc -aes-256-cbc -salt \
    -in plaintext.txt -out encrypted.bin

# Check if a partition is encrypted
lsblk -f | grep crypto
```

---

## Breaking OS Security

---

## Weak Access Controls

- Default or Weak Passwords
- Insecure User Account Management
- Misconfigured File System Permissions

---

## Common Misconfigurations Attackers Exploit

```bash
# DANGER: Common misconfigurations found during pentests

# 1. World-readable sensitive files
ls -la /etc/shadow    # Should be 640, root:shadow
ls -la /etc/sudoers   # Should be 440, root:root

# 2. SUID on unexpected binaries
find / -perm -4000 2>/dev/null
# Dangerous if SUID is on: python, perl, vim, find, nmap

# 3. Writable /etc/cron.d or /etc/cron.daily
ls -la /etc/cron.d/

# 4. Sudo without password
sudo -l
# (ALL) NOPASSWD: ALL  <-- Critical misconfiguration

# 5. Docker socket exposed
ls -la /var/run/docker.sock
# If user is in docker group, they can escalate to root
```

---

## Authentication Bypass

- Brute-Force Attacks
- Credential Stuffing
- Exploiting Authentication Flaws

---

## Brute Force and Credential Attacks

```bash
# Detecting brute force attempts in auth logs
grep "Failed password" /var/log/auth.log | tail -20
grep "Failed password" /var/log/auth.log | \
    awk '{print $11}' | sort | uniq -c | sort -rn | head
# Configure fail2ban for automatic blocking
# /etc/fail2ban/jail.local
# [sshd]
# enabled = true
# port = ssh
# filter = sshd
# logpath = /var/log/auth.log
# maxretry = 3
# bantime = 3600
# findtime = 600
sudo fail2ban-client status sshd
```

---

## Brute Force and Credential Attacks

![findtime_600](svg/courses/security/cyber-attacks-and-vectors/03_os_security/findtime_600.svg)

---

## Privilege Escalation

- Exploiting Software Vulnerabilities
- Kernel Exploits
- Improper Access Control Lists (ACLs)

---

## Linux Privilege Escalation Techniques

Common paths attackers use to escalate from low-privilege user to root:

```bash
# 1. Check sudo permissions
sudo -l

# 2. Check for SUID binaries
find / -perm -u=s -type f 2>/dev/null

# 3. Check for writable cron jobs
ls -la /etc/cron*
cat /etc/crontab

# 4. Check for kernel version (kernel exploits)
uname -r
# Compare against known exploit databases

# 5. Check for writable PATH directories
echo $PATH | tr ':' '\n' | xargs ls -ld

# 6. Check for credentials in environment/files
env | grep -i pass
find / -name "*.conf" -exec grep -l "password" {} \; 2>/dev/null

# 7. Check for Docker/LXC group membership
id
groups
```

---

## Real-World Case Study: Dirty COW (CVE-2016-5195)

- Race condition in the Linux kernel memory subsystem
- Allowed unprivileged users to gain write access to read-only memory
- Affected all Linux kernels from 2007 to 2016 (9 years unpatched)
- Exploited in the wild before patch was available
- Name comes from "Copy-On-Write" mechanism

Lesson: Keep kernels updated and monitor for kernel-level CVEs

---

## Unsecured Services and Misconfigurations

- Unpatched Software
- Unnecessary Services Running
- Insecure Network Configuration

---

## Data Exfiltration and Tampering

- Exploiting Encryption Flaws
- Lack of Data Integrity Checks
- Improper Data Sanitization

---

## Detecting Data Exfiltration

```bash
# Monitor outbound connections for suspicious activity
ss -tunap | grep ESTABLISHED | awk '{print $5}' | \
    cut -d: -f1 | sort | uniq -c | sort -rn | head

# Check for large outbound transfers
iftop -i eth0 -f "dst net not 10.0.0.0/8"

# Monitor DNS queries for tunneling
tcpdump -i eth0 -n port 53 | grep -i "TXT\|NULL\|CNAME"

# Audit file access with auditd
auditctl -w /etc/passwd -p rwa -k passwd_changes
auditctl -w /var/lib/sensitive/ -p rwa -k data_access
ausearch -k data_access --start recent
```

---

## Malware and Rootkits

- Backdoors and Trojans
- Rootkits and Persistent Threats
- Exploiting Kernel Vulnerabilities

---

## Rootkit Detection

```bash
# Check for rootkits using rkhunter
sudo rkhunter --check --skip-keypress

# Check for rootkits using chkrootkit
sudo chkrootkit

# Verify system binary integrity
debsums -c  # Debian/Ubuntu - check changed files
rpm -Va     # RHEL/CentOS - verify all packages

# Check for hidden processes
ps auxf > /tmp/ps_output.txt
ls /proc/ | grep -E '^[0-9]+$' | wc -l
# Compare process count from ps vs /proc

# Check loaded kernel modules
lsmod | sort
# Compare against known-good baseline

# Check for LD_PRELOAD hijacking
echo $LD_PRELOAD
cat /etc/ld.so.preload
```

---

## Mitigating OS Security Risks

- Implement Secure Baselines and Hardening
- Apply Security Patches and Updates Promptly
- Conduct Regular Security Audits and Penetration Testing
- Enforce Principle of Least Privilege
- Implement Comprehensive Security Monitoring and Incident Response

---

## Security Monitoring with auditd

```bash
# Install and enable auditd
sudo apt install auditd
sudo systemctl enable auditd

# Key audit rules (/etc/audit/rules.d/audit.rules)

# Monitor authentication events
-w /etc/pam.d/ -p wa -k pam_config
-w /var/log/auth.log -p wa -k auth_log

# Monitor privilege escalation
-w /usr/bin/sudo -p x -k sudo_usage
-w /etc/sudoers -p wa -k sudoers_change

# Monitor network configuration changes
-w /etc/hosts -p wa -k hosts_change
-w /etc/sysctl.conf -p wa -k sysctl_change

# Search audit logs
ausearch -k sudo_usage --start today
aureport --auth --summary
```

---

## Exercise: OS Security Audit

1. Set up a Linux VM with intentional misconfigurations:
   - World-readable /etc/shadow
   - SUID on /usr/bin/python3
   - Weak root password
   - SSH with PasswordAuthentication yes and PermitRootLogin yes
   - No firewall rules
1. Use Lynis to perform an automated audit
1. Manually identify each vulnerability
1. Document the remediation steps for each finding
1. Apply fixes and re-run the audit to verify improvements
