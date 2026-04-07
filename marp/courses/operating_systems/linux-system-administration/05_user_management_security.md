# User Management and System Security
## Users, ACLs, PAM, SSH, and Hardening

---
## User and Group Management

```bash
# Create user with options
useradd -m -s /bin/bash -G sudo,docker alice

# Modify user
usermod -aG developers alice
usermod -L alice        # lock account
usermod -U alice        # unlock account

# Delete user
userdel -r alice        # remove with home dir

# Create/manage groups
groupadd developers
groupmod -n devs developers
groupdel devs
```

---
## Important User Files

| File | Purpose |
|------|---------|
| `/etc/passwd` | User account info |
| `/etc/shadow` | Encrypted passwords |
| `/etc/group` | Group definitions |
| `/etc/gshadow` | Group passwords |
| `/etc/login.defs` | Login defaults |
| `/etc/skel/` | New user template |

```bash
# Password aging
chage -l alice              # view policy
chage -M 90 -W 7 alice     # max 90 days, warn 7
```

---
## Understanding /etc/passwd and /etc/shadow

```bash
# /etc/passwd format (colon-separated)
# username:x:UID:GID:comment:home:shell
alice:x:1001:1001:Alice Smith:/home/alice:/bin/bash

# /etc/shadow format
# username:hash:lastchange:min:max:warn:inactive:expire
alice:$6$salt$hash:19723:0:90:7:30::
```

```bash
# Verify file consistency
pwck          # check /etc/passwd
grpck         # check /etc/group

# Convert between shadow formats
pwconv        # create shadow from passwd
pwunconv      # merge shadow back to passwd
```

---
## Password Policies

```bash
# /etc/login.defs - system-wide defaults
PASS_MAX_DAYS   90
PASS_MIN_DAYS   7
PASS_WARN_AGE   14
PASS_MIN_LEN    12
LOGIN_RETRIES   3
LOGIN_TIMEOUT   60
```

```bash
# PAM password quality (install libpam-pwquality)
# /etc/security/pwquality.conf
minlen = 12
dcredit = -1      # require at least 1 digit
ucredit = -1      # require at least 1 uppercase
lcredit = -1      # require at least 1 lowercase
ocredit = -1      # require at least 1 special char
maxrepeat = 3     # max consecutive identical chars
```

---
## Special User Accounts

```bash
# System accounts (no login, for services)
useradd -r -s /usr/sbin/nologin -d /nonexistent myservice

# Disable login for existing user
usermod -s /usr/sbin/nologin alice

# Lock account (prefix ! to password hash)
passwd -l alice
usermod -L alice

# Expire account immediately
chage -E 0 alice

# Check for accounts with no password
awk -F: '($2 == "" || $2 == "!") {print $1}' /etc/shadow

# List users with UID 0 (root equivalent)
awk -F: '$3 == 0 {print $1}' /etc/passwd
```

---
## Linux Permission Model

```bash
# Standard permissions: user, group, other
# r(4) w(2) x(1)
chmod 755 script.sh     # rwxr-xr-x
chmod u+x script.sh     # add execute for owner
chmod o-w file.txt      # remove write for other

# Special permissions
chmod u+s /usr/bin/prog  # SUID - run as owner
chmod g+s /shared/       # SGID - inherit group
chmod +t /tmp/           # sticky bit - only owner deletes

# Numeric special permissions
chmod 4755 prog          # SUID
chmod 2755 dir           # SGID
chmod 1777 /tmp          # sticky
```

---
## Default Permissions: umask

```bash
# View current umask
umask           # shows octal
umask -S        # shows symbolic

# Common umask values
umask 022       # files: 644, dirs: 755 (default)
umask 027       # files: 640, dirs: 750
umask 077       # files: 600, dirs: 700

# Set in /etc/profile or ~/.bashrc for persistence

# How umask works:
# New file:      666 - umask = permission
# New directory:  777 - umask = permission
# umask 022: files=644 (rw-r--r--), dirs=755 (rwxr-xr-x)
```

---
## Access Control Lists (ACLs)

Standard permissions (`rwx`) are limited to owner, group, other. ACLs provide fine-grained control.

```bash
# View ACLs
getfacl /data/shared

# Grant user read/write
setfacl -m u:bob:rw /data/shared

# Grant group read
setfacl -m g:devs:r /data/shared

# Set default ACL for new files
setfacl -d -m g:devs:rw /data/shared

# Remove specific ACL
setfacl -x u:bob /data/shared

# Remove all ACLs
setfacl -b /data/shared
```

---
## ACL Advanced Usage

```bash
# Recursive ACL
setfacl -R -m u:bob:rwx /data/shared

# Copy ACLs from one file to another
getfacl source.txt | setfacl --set-file=- dest.txt

# ACL mask (maximum effective permissions)
setfacl -m m::r /data/shared

# Backup and restore ACLs
getfacl -R /data > acl-backup.txt
setfacl --restore=acl-backup.txt

# Check if file has ACLs (+ in ls output)
ls -la /data/shared
# -rw-rw-r--+ 1 alice devs 0 Jan 15 file.txt
```

---
## PAM (Pluggable Authentication Modules)

![pam_pluggable_authentication_modules](/svg/courses/operating_systems/linux-system-administration/05_user_management_security/pam_pluggable_authentication_modules.svg)

PAM module types: `auth`, `account`, `password`, `session`.

Configuration files in `/etc/pam.d/`.

---
## PAM Configuration Example

```config
# /etc/pam.d/common-auth
auth    required    pam_env.so
auth    required    pam_faildelay.so delay=2000000
auth    sufficient  pam_unix.so nullok try_first_pass
auth    required    pam_deny.so
```

Control flags:
- `required` - must pass, but continues checking
- `requisite` - must pass, fails immediately if not
- `sufficient` - if passes, skip remaining
- `optional` - result ignored unless only module

---
## Common PAM Modules

| Module | Purpose |
|--------|---------|
| `pam_unix.so` | Standard UNIX auth |
| `pam_deny.so` | Always deny access |
| `pam_permit.so` | Always allow access |
| `pam_limits.so` | Set resource limits |
| `pam_access.so` | Host/user-based access control |
| `pam_time.so` | Time-based access control |
| `pam_pwquality.so` | Password quality checks |
| `pam_google_authenticator.so` | TOTP 2FA |

```bash
# Resource limits via /etc/security/limits.conf
# alice  hard  nofile  65536
# @devs  soft  nproc   4096
```

---
## PAM Practical: Login Restrictions

```config
# /etc/security/access.conf
# Deny all except specific users from remote
- : ALL EXCEPT alice bob : ALL

# Allow root only from console
+ : root : LOCAL
- : root : ALL

# /etc/security/time.conf
# Allow login only during business hours
login;*;alice;Wk0800-1800
```

```bash
# Enable access control in PAM
# Add to /etc/pam.d/common-auth or specific service:
account required pam_access.so
```

---
## sudo Configuration

```bash
# Edit sudoers safely
visudo

# /etc/sudoers examples
```

```config
# User privilege specification
alice   ALL=(ALL:ALL) ALL

# Group privilege
%developers ALL=(ALL) /usr/bin/systemctl restart nginx

# No password required
bob     ALL=(ALL) NOPASSWD: /usr/bin/apt update

# Command aliases
Cmnd_Alias SERVICES = /usr/bin/systemctl
alice   ALL=(ALL) SERVICES
```

```bash
# Drop-in files (preferred)
echo "alice ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/alice
```

---
## sudo Advanced Configuration

```bash
# Validate sudoers syntax before saving
visudo -c -f /etc/sudoers.d/alice

# User aliases
User_Alias ADMINS = alice, bob, charlie

# Host aliases
Host_Alias WEBSERVERS = web1, web2, web3

# Command aliases
Cmnd_Alias SHUTDOWN = /sbin/halt, /sbin/reboot, /sbin/poweroff

# Combined rule
ADMINS WEBSERVERS=(ALL) SHUTDOWN
```

```config
# Logging all sudo commands
Defaults  logfile="/var/log/sudo.log"
Defaults  log_input, log_output
Defaults  iolog_dir="/var/log/sudo-io/%{user}"
```

---
## SSH In Depth

```bash
# Generate key pair
ssh-keygen -t ed25519 -C "alice@company.com"

# Copy public key to server
ssh-copy-id user@server

# Use ssh-agent
eval $(ssh-agent)
ssh-add ~/.ssh/id_ed25519

# List loaded keys
ssh-add -l
```

---
## SSH Key Types and Best Practices

| Key Type | Recommended | Notes |
|----------|------------|-------|
| `ed25519` | Yes | Modern, fast, secure |
| `rsa` (4096) | Yes | Wide compatibility |
| `ecdsa` | Acceptable | NIST curves |
| `dsa` | No | Deprecated, weak |
| `rsa` (1024) | No | Too short |

```bash
# Generate with passphrase
ssh-keygen -t ed25519 -a 100 -C "alice@company.com"

# Change passphrase on existing key
ssh-keygen -p -f ~/.ssh/id_ed25519

# View key fingerprint
ssh-keygen -l -f ~/.ssh/id_ed25519.pub

# Convert key formats
ssh-keygen -e -f key.pub -m RFC4716 > key.rfc
```

---
## SSH Config File

```config
# ~/.ssh/config
Host prod-web
    HostName 10.0.1.50
    User deploy
    IdentityFile ~/.ssh/prod_key
    Port 2222

Host bastion
    HostName bastion.example.com
    User admin

Host internal-*
    ProxyJump bastion
    User admin
```

```bash
# Now simply:
ssh prod-web
ssh internal-db
```

---
## SSH Config Advanced Options

```config
# ~/.ssh/config

# Multiplexing (reuse connections)
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600

# Keep connections alive
    ServerAliveInterval 60
    ServerAliveCountMax 3

# Specific host with forwarding
Host dev-server
    HostName dev.example.com
    LocalForward 5432 db-server:5432
    DynamicForward 1080
    ForwardAgent yes
```

```bash
mkdir -p ~/.ssh/sockets
```

---
## SSH Tunneling and Jump Hosts

```bash
# Local port forwarding (access remote service locally)
ssh -L 8080:localhost:80 user@server

# Remote port forwarding (expose local service)
ssh -R 9090:localhost:3000 user@server

# Dynamic SOCKS proxy
ssh -D 1080 user@server

# Jump host (ProxyJump)
ssh -J bastion@jump user@target

# Copy files through jump host
scp -o ProxyJump=bastion file user@target:/path/
```

---
## SSH Tunneling Practical Examples

```bash
# Access remote PostgreSQL locally
ssh -L 5432:db-server:5432 user@bastion
# Then: psql -h localhost -p 5432

# Access remote web UI
ssh -L 9090:prometheus:9090 user@server
# Then: http://localhost:9090

# Multi-hop tunnel
ssh -L 8080:internal:80 \
  -J user@bastion1,user@bastion2 user@target

# Reverse tunnel (expose local dev server)
ssh -R 0.0.0.0:8080:localhost:3000 user@public-server

# SOCKS proxy for browsing
ssh -D 1080 -N -f user@server
# Configure browser to use SOCKS5 localhost:1080
```

---
## SSH Hardening

```config
# /etc/ssh/sshd_config
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers alice bob
ClientAliveInterval 300
ClientAliveCountMax 2
Protocol 2
X11Forwarding no
```

```bash
# Apply changes
systemctl restart sshd
```

---
## SSH Hardening: Advanced Options

```config
# /etc/ssh/sshd_config (continued)
# Restrict key exchange algorithms
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org

# Restrict ciphers
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com

# Restrict MACs
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# Restrict key types
PubkeyAcceptedKeyTypes ssh-ed25519,rsa-sha2-512

# Limit concurrent unauthenticated connections
MaxStartups 10:30:60

# Banner warning
Banner /etc/ssh/banner.txt
```

---
## fail2ban

```bash
# Install
apt install fail2ban

# Create local config
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
```

```ini
# /etc/fail2ban/jail.local
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
findtime = 600
```

```bash
# Check status
fail2ban-client status sshd
```

---
## fail2ban Advanced Configuration

```ini
# /etc/fail2ban/jail.local
[DEFAULT]
banaction = nftables
bantime = 1h
findtime = 10m
maxretry = 3

# Progressive banning
[recidive]
enabled = true
logpath = /var/log/fail2ban.log
bantime = 1w
findtime = 1d
maxretry = 5
```

```bash
# Manual ban/unban
fail2ban-client set sshd banip 10.0.0.5
fail2ban-client set sshd unbanip 10.0.0.5

# List banned IPs
fail2ban-client status sshd

# Test regex against log
fail2ban-regex /var/log/auth.log /etc/fail2ban/filter.d/sshd.conf
```

---
## File Integrity Monitoring

```bash
# AIDE (Advanced Intrusion Detection Environment)
apt install aide

# Initialize database
aideinit

# Run integrity check
aide --check

# Update database after known changes
aide --update
```

```bash
# Tripwire alternative
apt install tripwire
tripwire --init
tripwire --check
```

---
## AIDE Configuration

```config
# /etc/aide/aide.conf
# Define what to monitor
/etc    p+i+u+g+sha256
/bin    p+i+u+g+sha256
/sbin   p+i+u+g+sha256
/usr/bin  p+i+u+g+sha256
/usr/sbin p+i+u+g+sha256

# Exclude noisy directories
!/var/log
!/var/cache
!/tmp
!/proc
!/sys
```

Attributes: `p`=permissions, `i`=inode, `u`=user, `g`=group, `s`=size, `sha256`=checksum.

```bash
# Automate daily checks
# 0 4 * * * /usr/bin/aide --check | mail -s "AIDE Report" admin@example.com
```

---
## Security Auditing with auditd

```bash
# Install
apt install auditd

# Add audit rules
auditctl -w /etc/passwd -p wa -k passwd_changes
auditctl -w /etc/shadow -p wa -k shadow_changes
auditctl -a always,exit -F arch=b64 -S execve -k commands

# Search audit logs
ausearch -k passwd_changes
ausearch -m USER_LOGIN --success no

# Generate audit report
aureport --summary
aureport --login --failed
```

---
## auditd Persistent Rules

```bash
# /etc/audit/rules.d/audit.rules
# Delete all existing rules
-D

# Set buffer size
-b 8192

# Monitor user/group changes
-w /etc/passwd -p wa -k identity
-w /etc/group -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/sudoers -p wa -k sudoers

# Monitor network config changes
-w /etc/hosts -p wa -k network
-w /etc/sysconfig/network -p wa -k network

# Monitor mount operations
-a always,exit -F arch=b64 -S mount -k mounts

# Make rules immutable (requires reboot to change)
-e 2
```

---
## Certificate Management

```bash
# Generate self-signed certificate
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout server.key \
  -out server.crt

# Generate CSR for CA signing
openssl req -new -newkey rsa:2048 \
  -keyout server.key -out server.csr

# View certificate details
openssl x509 -in server.crt -text -noout

# Verify certificate chain
openssl verify -CAfile ca.crt server.crt
```

---
## Let's Encrypt with certbot

```bash
# Install certbot
apt install certbot python3-certbot-nginx

# Obtain certificate (nginx)
certbot --nginx -d example.com -d www.example.com

# Obtain certificate (standalone)
certbot certonly --standalone -d example.com

# Renew certificates
certbot renew --dry-run
certbot renew

# Auto-renewal via systemd timer
systemctl enable --now certbot.timer
systemctl list-timers | grep certbot
```

Certificate files:
- `/etc/letsencrypt/live/example.com/fullchain.pem`
- `/etc/letsencrypt/live/example.com/privkey.pem`

---
## System Logging and Security Monitoring

```bash
# Key log files
/var/log/auth.log       # authentication events
/var/log/syslog         # general system log
/var/log/kern.log       # kernel messages
/var/log/faillog        # failed logins

# Monitor login activity
last                    # recent logins
lastb                   # failed logins
who                     # currently logged in
w                       # logged in users + activity

# Watch logs in real time
tail -f /var/log/auth.log
journalctl -f -u sshd
```

---
## Security Monitoring Checklist

Regular checks for system administrators:

```bash
# 1. Check for unauthorized users
awk -F: '$3 >= 1000 {print $1}' /etc/passwd

# 2. Check for empty passwords
awk -F: '$2 == "" {print $1}' /etc/shadow

# 3. Check for SUID/SGID files
find / -xdev \( -perm -4000 -o -perm -2000 \) -type f

# 4. Check world-writable files
find / -xdev -type f -perm -0002

# 5. Check for unauthorized cron jobs
for u in $(cut -d: -f1 /etc/passwd); do
  crontab -l -u "$u" 2>/dev/null
done

# 6. Check listening services
ss -tlnp
```

---
## LDAP/NSS Overview

![ldap_nss_overview](/svg/courses/operating_systems/linux-system-administration/05_user_management_security/ldap_nss_overview.svg)

`NSS` (Name Service Switch) lets applications resolve users, groups, and hosts from multiple backends.

```bash
# /etc/nsswitch.conf with LDAP
passwd: files ldap
group:  files ldap
shadow: files ldap
```

---
## Configuring LDAP Client (sssd)

```bash
# Install SSSD for LDAP authentication
apt install sssd sssd-ldap ldap-utils
```

```ini
# /etc/sssd/sssd.conf
[sssd]
domains = example.com
services = nss, pam

[domain/example.com]
id_provider = ldap
auth_provider = ldap
ldap_uri = ldaps://ldap.example.com
ldap_search_base = dc=example,dc=com
ldap_tls_reqcert = demand
ldap_tls_cacert = /etc/ssl/certs/ca-certificates.crt
```

```bash
chmod 600 /etc/sssd/sssd.conf
systemctl enable --now sssd
```

---
## Two-Factor Authentication with PAM

```bash
# Install Google Authenticator PAM module
apt install libpam-google-authenticator

# Generate TOTP secret per user
google-authenticator
# Answer prompts: time-based, update .google_authenticator,
# disallow reuse, rate limiting
```

```config
# /etc/pam.d/sshd - add after @include common-auth
auth required pam_google_authenticator.so
```

```config
# /etc/ssh/sshd_config
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
```

```bash
systemctl restart sshd
```

---
## SSH Certificates

SSH certificates are signed keys - no need to distribute `authorized_keys` to every server.

```bash
# 1. Create a Certificate Authority (CA)
ssh-keygen -t ed25519 -f ca_key -C "SSH CA"

# 2. Sign a user key (valid 52 weeks)
ssh-keygen -s ca_key -I alice@company -n alice \
  -V +52w alice_id_ed25519.pub

# 3. Sign a host key
ssh-keygen -s ca_key -I web1.example.com \
  -h -n web1.example.com /etc/ssh/ssh_host_ed25519_key.pub
```

```config
# /etc/ssh/sshd_config - trust the CA
TrustedUserCAKeys /etc/ssh/ca_key.pub
```

```config
# ~/.ssh/known_hosts - trust host CA
@cert-authority *.example.com <ca_public_key>
```

---
## CIS Benchmarks Overview

CIS (Center for Internet Security) benchmarks provide hardening checklists.

Key areas covered:
1. Filesystem configuration (disable `cramfs`, `squashfs`)
1. Software updates and patching
1. Secure boot settings
1. Process hardening (`ASLR`, `core dumps`)
1. Mandatory Access Control (`AppArmor`/`SELinux`)
1. Network configuration (disable IP forwarding, ICMP redirects)
1. Audit and logging (`auditd`, log retention)
1. Authentication (password quality, account lockout)
1. SSH server hardening

```bash
# Example: apply filesystem hardening
echo "install cramfs /bin/true" > /etc/modprobe.d/cramfs.conf
echo "install squashfs /bin/true" > /etc/modprobe.d/squashfs.conf
```

---
## Security Scanning with Lynis

```bash
# Install Lynis
apt install lynis

# Run full audit
lynis audit system

# Run specific test category
lynis audit system --tests-from-group authentication

# View results
cat /var/log/lynis.log
cat /var/log/lynis-report.dat
```

Key output sections:
- **Warnings** - issues requiring immediate attention
- **Suggestions** - recommended improvements
- **Hardening index** - overall score (0-100)

```bash
# Extract actionable suggestions
grep "suggestion\[\]" /var/log/lynis-report.dat
```

---
## Chroot Jails

A `chroot` changes the apparent root directory for a process, isolating it from the rest of the filesystem.

```bash
# Create minimal chroot environment
mkdir -p /srv/jail/{bin,lib,lib64,etc}

# Copy required binaries and libraries
cp /bin/bash /srv/jail/bin/
ldd /bin/bash | grep -o '/lib[^ ]*' | \
  while read lib; do
    cp --parents "$lib" /srv/jail/
  done

# Enter the chroot
chroot /srv/jail /bin/bash

# Chroot for SSH users
# /etc/ssh/sshd_config
# Match User restricted_user
#     ChrootDirectory /srv/jail/%u
#     ForceCommand internal-sftp
```

---
## Linux File Capabilities

File capabilities provide fine-grained alternatives to `SUID` root.

```bash
# View capabilities on a file
getcap /usr/bin/ping
# /usr/bin/ping cap_net_raw=ep

# Set a capability
setcap cap_net_bind_service=+ep /usr/local/bin/myserver
# allows binding to ports < 1024 without root

# Remove capabilities
setcap -r /usr/local/bin/myserver

# List all files with capabilities
getcap -r / 2>/dev/null
```

Common capabilities:
| Capability | Purpose |
|-----------|---------|
| `CAP_NET_BIND_SERVICE` | Bind to ports below 1024 |
| `CAP_NET_RAW` | Use raw sockets (`ping`) |
| `CAP_SYS_PTRACE` | Trace processes (`strace`) |
| `CAP_DAC_OVERRIDE` | Bypass file permission checks |
| `CAP_CHOWN` | Change file ownership |

---
## Exercise: Security Audit Walkthrough

Perform a mini security audit on a test system:

```bash
# 1. Check for users with UID 0
awk -F: '$3 == 0 {print $1}' /etc/passwd

# 2. Find world-writable files outside /tmp
find / -xdev -type f -perm -0002 \
  -not -path "/tmp/*" -not -path "/proc/*"

# 3. List SUID binaries and compare to baseline
find / -xdev -perm -4000 -type f -exec ls -l {} \;

# 4. Check SSH config for weak settings
sshd -T | grep -E "permitrootlogin|passwordauth"

# 5. Verify no empty passwords exist
awk -F: '$2 == "" {print $1}' /etc/shadow

# 6. Review sudo access
cat /etc/sudoers.d/*

# 7. Run Lynis and review hardening index
lynis audit system --quick
```

---
## Troubleshooting: Locked Out Users

Common lockout scenarios and fixes:

```bash
# Account locked via PAM faillock
faillock --user alice             # view failed attempts
faillock --user alice --reset     # unlock

# Account expired
chage -l alice                    # check expiry
chage -E -1 alice                 # remove expiry

# Password expired
chage -d 0 alice                  # force password change

# SSH key rejected - check permissions
ls -la ~/.ssh/
# Must be: ~/.ssh (700), authorized_keys (600)
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys

# SELinux/AppArmor blocking access
restorecon -Rv /home/alice/.ssh   # SELinux
aa-status                          # AppArmor
```

---
## SELinux Quick Overview for Ubuntu

`SELinux` enforces mandatory access control via labels on files, processes, and ports.

```bash
# Install SELinux on Ubuntu (replaces AppArmor)
apt install selinux-basics selinux-policy-default auditd
selinux-activate
# Reboot required after activation

# Check SELinux status
sestatus
getenforce        # Enforcing, Permissive, or Disabled

# Switch modes (runtime)
setenforce 0      # Permissive (log only)
setenforce 1      # Enforcing
```

```bash
# View file labels
ls -Z /etc/passwd
# Restore default labels
restorecon -Rv /var/www/html
# Check for SELinux denials
ausearch -m avc -ts recent
```

---
## Password Hash Algorithms

The hash prefix in `/etc/shadow` identifies the algorithm used.

| Prefix | Algorithm | Strength |
|--------|-----------|----------|
| `$1$` | MD5 | Weak, avoid |
| `$5$` | SHA-256 | Acceptable |
| `$6$` | SHA-512 | Recommended |
| `$y$` | yescrypt | Modern default (Ubuntu 22.04+) |
| `$2b$` | bcrypt | Strong, common in apps |

```bash
# Check current default algorithm
grep ENCRYPT_METHOD /etc/login.defs

# Change default to yescrypt
# /etc/login.defs
# ENCRYPT_METHOD yescrypt

# Rehash a user password with new algorithm
passwd alice
```

---
## nscd Name Service Cache

`nscd` caches results from `NSS` lookups (users, groups, hosts) to reduce LDAP/DNS load.

```bash
# Install and enable nscd
apt install nscd
systemctl enable --now nscd

# View cache statistics
nscd -g

# Invalidate specific cache
nscd -i passwd
nscd -i group
nscd -i hosts
```

```bash
# /etc/nscd.conf - key settings
# enable-cache   passwd   yes
# positive-time-to-live  passwd  600
# negative-time-to-live  passwd  20
# suggested-size  passwd  211
# check-files    passwd   yes
```

Note: on systems with `sssd`, prefer `sssd` caching over `nscd` to avoid conflicts.

---
## Restricted Shells

A restricted shell (`rbash`) prevents users from changing directories, modifying `PATH`, or running commands with `/`.

```bash
# Create user with restricted shell
useradd -m -s /bin/rbash restricted_user

# Set up allowed commands via PATH
mkdir /home/restricted_user/bin
ln -s /usr/bin/ls /home/restricted_user/bin/
ln -s /usr/bin/cat /home/restricted_user/bin/

# Lock down the profile
cat > /home/restricted_user/.bash_profile << 'PROF'
PATH=$HOME/bin
export PATH
PROF
chown root:root /home/restricted_user/.bash_profile
chmod 644 /home/restricted_user/.bash_profile
```

Restrictions enforced by `rbash`:
- Cannot `cd` to another directory
- Cannot change `PATH`, `SHELL`, or `ENV`
- Cannot run commands containing `/`
- Cannot redirect output with `>` or `>>`

---
## ulimits Deep Dive

Resource limits are enforced per-process via `pam_limits` and the `ulimit` built-in.

```bash
# View all current limits
ulimit -a

# Key limits
ulimit -n          # max open files (nofile)
ulimit -u          # max user processes (nproc)
ulimit -v          # max virtual memory (kB)
ulimit -l          # max locked memory (kB)
ulimit -c          # core dump size (0 = disabled)
```

```bash
# /etc/security/limits.conf
# <domain>  <type>  <item>   <value>
*            soft    nofile   4096
*            hard    nofile   65536
@developers  soft    nproc    4096
@developers  hard    nproc    8192
alice        hard    as       4194304
# 'as' = address space in kB (4 GB above)

# Systemd services use LimitNOFILE= in unit files
# [Service]
# LimitNOFILE=65536
# LimitNPROC=4096
```

---
## /etc/securetty and Console Access

`/etc/securetty` lists terminals where `root` can log in directly (used by `pam_securetty`).

```bash
# View allowed root login terminals
cat /etc/securetty
# Typical entries: tty1, tty2, ... tty6

# Disable root login on all consoles
# Remove or empty the file
> /etc/securetty

# Verify pam_securetty is active
grep securetty /etc/pam.d/login
# auth required pam_securetty.so
```

Additional console access controls:

```bash
# Disable Ctrl+Alt+Del reboot
systemctl mask ctrl-alt-del.target

# Restrict virtual console access
# /etc/systemd/logind.conf
# NAutoVTs=2          # only 2 virtual terminals
# ReserveVT=1         # reserve VT1 for rescue

# Restrict single-user mode to require root password
# Ensure /etc/shadow has a root password set
passwd root
```

---
## Security Incident Response: Compromised Account

When a user account is suspected to be compromised, act immediately.

```bash
# 1. Lock the account and kill sessions
passwd -l compromised_user
pkill -KILL -u compromised_user

# 2. Preserve evidence before cleanup
tar czf /root/evidence-$(date +%s).tar.gz \
  /home/compromised_user/.bash_history \
  /home/compromised_user/.ssh/ \
  /var/log/auth.log

# 3. Audit recent activity
lastlog -u compromised_user
ausearch -ua compromised_user --start recent
last compromised_user

# 4. Check for persistence mechanisms
crontab -l -u compromised_user
ls -la /home/compromised_user/.ssh/authorized_keys
find /tmp /var/tmp -user compromised_user

# 5. Rotate all credentials the user had access to
# 6. Notify stakeholders and document timeline
```

---
## Exercise: Harden a Fresh Server

Apply these hardening steps to a new Ubuntu server:

```bash
# 1. Set strong password policies
# Edit /etc/login.defs: PASS_MAX_DAYS=90, PASS_MIN_LEN=12
# Install and configure libpam-pwquality

# 2. Lock down SSH
# /etc/ssh/sshd_config:
#   PermitRootLogin no
#   PasswordAuthentication no
#   MaxAuthTries 3

# 3. Configure ulimits for all users
# /etc/security/limits.conf:
#   * hard nofile 65536
#   * hard nproc 4096

# 4. Enable and configure fail2ban
apt install fail2ban
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# 5. Install and initialize AIDE
apt install aide && aideinit

# 6. Enable auditd with key file watches
apt install auditd
auditctl -w /etc/passwd -p wa -k identity
auditctl -w /etc/shadow -p wa -k identity

# 7. Run Lynis and address findings
lynis audit system
```

---
## Kernel Hardening: sysctl Security

```bash
# /etc/sysctl.d/99-security.conf

# Enable ASLR (Address Space Layout Randomization)
kernel.randomize_va_space = 2

# Restrict dmesg to root only
kernel.dmesg_restrict = 1

# Hide kernel pointer addresses from non-root
kernel.kptr_restrict = 2

# Yama ptrace scope (restrict process tracing)
# 0=classic, 1=parent-only, 2=admin-only, 3=disabled
kernel.yama.ptrace_scope = 1

# Restrict access to kernel logs
kernel.printk = 3 3 3 3

# Disable SysRq key (or restrict to safe functions)
kernel.sysrq = 0
```

```bash
# Apply all sysctl settings
sysctl --system

# Verify specific settings
sysctl kernel.randomize_va_space
sysctl kernel.dmesg_restrict
```

---
## Immutable and Append-Only Files

`chattr` sets extended file attributes that even `root` must explicitly remove.

```bash
# Make a file immutable (cannot be modified, deleted,
# renamed, or linked - even by root)
chattr +i /etc/resolv.conf

# Make a file append-only (can add data, cannot
# modify or delete existing content)
chattr +a /var/log/audit/audit.log

# View extended attributes
lsattr /etc/resolv.conf
# ----i--------e-- /etc/resolv.conf

# Remove the immutable attribute
chattr -i /etc/resolv.conf
```

Use cases:
- Protect `/etc/resolv.conf` from being overwritten by `DHCP`
- Protect critical config files from accidental changes
- Ensure log files can only be appended to (tamper resistance)
- Protect `/etc/passwd` and `/etc/shadow` during maintenance

---
## systemd Service Security Features

Harden services using `systemd` built-in sandboxing directives:

```ini
# /etc/systemd/system/myapp.service
[Service]
# Isolate /tmp per service
PrivateTmp=yes

# Make system directories read-only or inaccessible
ProtectSystem=strict
ProtectHome=yes

# Restrict system calls to a whitelist
SystemCallFilter=@system-service
SystemCallFilter=~@privileged @resources

# Drop all capabilities except what is needed
CapabilityBoundingSet=CAP_NET_BIND_SERVICE

# Prevent gaining new privileges
NoNewPrivileges=yes

# Private /dev with only pseudo-devices
PrivateDevices=yes
```

```bash
# Analyze security score of a service
systemd-analyze security nginx.service
# Shows a rating from 0.0 (safest) to 10.0 (exposed)
```

---
## Security Compliance Frameworks

Overview of major compliance frameworks relevant to `Linux` administrators:

| Framework | Focus | Scope |
|-----------|-------|-------|
| CIS Benchmarks | System hardening | Per-OS checklists |
| DISA STIG | Government security | DoD systems |
| PCI-DSS | Payment card data | Cardholder environments |
| SOC 2 | Service organization controls | SaaS, cloud providers |

```bash
# Automated CIS compliance scanning
apt install openscap-scanner
oscap xccdf eval --profile cis \
  /usr/share/xml/scap/ssg/content/ssg-ubuntu2404-ds.xml

# STIG compliance with SCAP
oscap xccdf eval --profile stig \
  /path/to/stig-content.xml
```

Key practices across all frameworks:
1. Maintain patch management and system hardening
1. Enable logging and audit trails (`auditd`, `journald`)
1. Enforce least privilege and access controls
1. Document and review security configurations regularly
