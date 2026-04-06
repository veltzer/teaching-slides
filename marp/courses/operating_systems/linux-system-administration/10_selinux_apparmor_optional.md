# SELinux and AppArmor (Optional)
## Mandatory Access Control

---
## Mandatory Access Control (MAC) Concepts

- Standard `Linux` uses DAC (Discretionary Access Control)
    - File owners control permissions
- MAC adds a second layer enforced by the kernel
    - Even `root` is restricted by policy
- Two main implementations:
    - `SELinux` - used by RHEL, Fedora, CentOS
    - `AppArmor` - used by Ubuntu, SUSE

---
## DAC vs MAC Comparison

| Feature | DAC | MAC |
|---------|-----|-----|
| Access decisions | File owner | System policy |
| Root bypass | Root can override | Root is restricted |
| Configuration | `chmod`/`chown` | Policy files |
| Complexity | Simple | More complex |
| Protection | Against other users | Against compromised processes |

MAC is essential when:
- A compromised service should not access arbitrary files
- Compliance requires mandatory security controls
- Defense-in-depth is required

---
## SELinux Modes

| Mode | Description |
|------|-------------|
| Enforcing | Policies enforced, violations denied and logged |
| Permissive | Violations logged but not denied |
| Disabled | SELinux completely off |

```bash
# Check current mode
getenforce
sestatus

# Change mode temporarily
setenforce 0        # permissive
setenforce 1        # enforcing

# Change permanently in /etc/selinux/config
# SELINUX=enforcing
```

---
## SELinux Contexts

Every file, process, and port has a security context: `user:role:type:level`

```bash
# View file contexts
ls -Z /var/www/html/

# View process contexts
ps auxZ | grep httpd

# Change file context
chcon -t httpd_sys_content_t /var/www/html/index.html

# Restore default context
restorecon -Rv /var/www/html/
```

---
## SELinux Context Deep Dive

```bash
# Context format: user:role:type:level
# system_u:object_r:httpd_sys_content_t:s0

# Common types for web servers:
# httpd_sys_content_t    - read-only web content
# httpd_sys_rw_content_t - read-write web content
# httpd_log_t            - log files

# View port contexts
semanage port -l | grep http

# Add custom port for httpd
semanage port -a -t http_port_t -p tcp 8080

# Set context for custom web directory
semanage fcontext -a -t httpd_sys_content_t \
  "/srv/www(/.*)?"
restorecon -Rv /srv/www/
```

---
## SELinux Booleans and Policies

```bash
# List all booleans
getsebool -a

# Search for specific booleans
getsebool -a | grep httpd

# Set a boolean
setsebool -P httpd_can_network_connect on

# View policy modules
semodule -l

# Generate policy from denials
audit2allow -a -M mypolicy
semodule -i mypolicy.pp
```

---
## Common SELinux Booleans

| Boolean | Purpose |
|---------|---------|
| `httpd_can_network_connect` | Allow HTTP to connect to network |
| `httpd_can_network_connect_db` | Allow HTTP to connect to DB |
| `httpd_enable_homedirs` | Serve content from home dirs |
| `samba_enable_home_dirs` | Share home directories via Samba |
| `ftp_home_dir` | Allow FTP access to home dirs |
| `ssh_sysadm_login` | Allow SSH login as sysadm_r |

```bash
# Find relevant booleans for a service
getsebool -a | grep -i samba
semanage boolean -l | grep httpd
```

---
## Troubleshooting SELinux Denials

```bash
# View denials in audit log
ausearch -m AVC -ts recent

# Use audit2why for explanations
ausearch -m AVC -ts recent | audit2why

# Use sealert for detailed analysis
sealert -a /var/log/audit/audit.log

# Common fix: restore contexts
restorecon -Rv /path/to/files

# Common fix: enable boolean
setsebool -P <boolean_name> on

# Last resort: create custom policy
audit2allow -a -M custom_policy
```

---
## SELinux Troubleshooting Workflow

- Check if SELinux is the problem:

```bash
# Temporarily switch to permissive
setenforce 0
# Test if the issue goes away
# If yes, SELinux is blocking
setenforce 1
```

- Find the denial:

```bash
ausearch -m AVC -ts recent | audit2why
```

- Fix (in order of preference):
    - `restorecon` - fix file contexts
    - `setsebool` - enable boolean
    - `semanage fcontext` - add context rule
    - `audit2allow` - create custom policy (last resort)

---
## AppArmor Modes

| Mode | Description |
|------|-------------|
| Enforce | Policy enforced, violations denied |
| Complain | Violations logged, not denied |
| Disabled | Profile not loaded |

```bash
# Check AppArmor status
aa-status

# Set profile to complain mode
aa-complain /etc/apparmor.d/usr.sbin.nginx

# Set profile to enforce mode
aa-enforce /etc/apparmor.d/usr.sbin.nginx

# Disable a profile
ln -s /etc/apparmor.d/usr.sbin.nginx \
  /etc/apparmor.d/disable/
apparmor_parser -R /etc/apparmor.d/usr.sbin.nginx
```

---
## AppArmor Profile Structure

```config
# /etc/apparmor.d/usr.sbin.nginx
#include <tunables/global>

/usr/sbin/nginx {
  #include <abstractions/base>
  #include <abstractions/nameservice>

  # Binary
  /usr/sbin/nginx           mr,

  # Configuration
  /etc/nginx/               r,
  /etc/nginx/**             r,

  # Log files
  /var/log/nginx/           rw,
  /var/log/nginx/**         rw,

  # Web content
  /var/www/html/            r,
  /var/www/html/**          r,

  # Network
  network inet tcp,
  network inet6 tcp,

  # PID file
  /run/nginx.pid            rw,
}
```

---
## AppArmor Permission Flags

| Flag | Permission |
|------|-----------|
| `r` | Read |
| `w` | Write |
| `a` | Append |
| `k` | Lock |
| `m` | Memory map executable |
| `x` | Execute |
| `ix` | Inherit execute (same profile) |
| `px` | Profile execute (switch to target profile) |
| `ux` | Unconfined execute |
| `Ux` | Unconfined, scrub environment |

---
## Writing AppArmor Profiles

```config
# /etc/apparmor.d/usr.local.bin.myapp
#include <tunables/global>

/usr/local/bin/myapp {
  #include <abstractions/base>
  #include <abstractions/nameservice>

  /usr/local/bin/myapp    mr,
  /etc/myapp/             r,
  /etc/myapp/**           r,
  /var/log/myapp/         rw,
  /var/log/myapp/**       rw,
  /tmp/myapp.*            rw,
  network tcp,
}
```

```bash
# Generate profile interactively
aa-genprof /usr/local/bin/myapp

# Update profile from logs
aa-logprof
```

---
## AppArmor Troubleshooting

```bash
# Check for denials
journalctl | grep -i apparmor | grep DENIED

# View audit messages
dmesg | grep apparmor

# Parse log for a specific profile
aa-logprof -f /var/log/syslog

# Temporarily switch to complain to diagnose
aa-complain /etc/apparmor.d/usr.local.bin.myapp
# Reproduce the issue
# Review logs
aa-logprof
# Switch back to enforce
aa-enforce /etc/apparmor.d/usr.local.bin.myapp

# Reload all profiles
systemctl reload apparmor
```

---
## SELinux File Context Management

```bash
# View default contexts for a path
semanage fcontext -l | grep /var/www

# Add custom file context rule
semanage fcontext -a -t httpd_sys_rw_content_t \
  "/srv/uploads(/.*)?"

# Apply context rules to filesystem
restorecon -Rv /srv/uploads

# Verify context was applied
ls -Zd /srv/uploads

# Delete a custom context rule
semanage fcontext -d "/srv/uploads(/.*)?"

# Export all local customizations
semanage export > selinux-local.txt

# Import customizations on another machine
semanage import < selinux-local.txt
```

---
## Building Custom SELinux Policy Modules

```bash
# Step 1: trigger the denial (in permissive mode)
setenforce 0
# Run the application that is being blocked
setenforce 1

# Step 2: extract denials from audit log
ausearch -m AVC -ts recent > /tmp/denials.txt

# Step 3: generate a policy module
audit2allow -i /tmp/denials.txt -M myapp_custom

# Step 4: review the generated policy
cat myapp_custom.te
```

```config
# Example generated .te file
module myapp_custom 1.0;
require {
    type httpd_t;
    type user_home_t;
    class file { read open getattr };
}
allow httpd_t user_home_t:file { read open getattr };
```

```bash
# Step 5: install the module
semodule -i myapp_custom.pp

# Verify it is loaded
semodule -l | grep myapp_custom
```

---
## AppArmor Abstractions

```misc
# Abstractions are reusable permission sets
# Located in /etc/apparmor.d/abstractions/

# Common abstractions:
# base          - basic system access (/dev, /proc)
# nameservice   - DNS, NSS, LDAP lookups
# authentication - PAM, shadow, login
# apache2-common - shared Apache paths
# ssl_certs     - read access to SSL certificates
# python        - Python interpreter paths
# bash          - Bash shell access
```

```config
# Using abstractions in a profile
/usr/local/bin/myapp {
  #include <abstractions/base>
  #include <abstractions/nameservice>
  #include <abstractions/ssl_certs>
  #include <abstractions/python>

  /usr/local/bin/myapp    mr,
  /etc/myapp/**           r,
  /var/log/myapp/**       rw,
}
```

Create custom abstractions for shared rules across profiles.

---
## SELinux vs AppArmor Comparison

| Feature | SELinux | AppArmor |
|---------|---------|----------|
| Approach | Labels on all objects | Path-based rules |
| Default distros | RHEL, Fedora, CentOS | Ubuntu, SUSE, Debian |
| Policy scope | System-wide | Per-application |
| Learning curve | Steep | Moderate |
| Granularity | Very fine-grained | Coarser |
| File identification | By inode label | By file path |
| Hardlink safety | Secure (label follows) | Risk (path changes) |
| New file handling | Inherits parent context | Matched by path rule |
| Tool ecosystem | `semanage`, `audit2allow` | `aa-genprof`, `aa-logprof` |
| Network control | Port labeling | Basic network rules |

Choose based on:
- Distribution default (path of least resistance)
- Team familiarity
- Compliance requirements (some mandate `SELinux`)

---
## Exercise: Confining a Web Application

Scenario: confine `/usr/local/bin/webapp` that needs:
- Read config from `/etc/webapp/`
- Write logs to `/var/log/webapp/`
- Listen on port `8080`
- Connect to `PostgreSQL` on port `5432`

```bash
# AppArmor approach
aa-genprof /usr/local/bin/webapp
# Run the application in another terminal
# Press S to scan logs, then F to finish

# SELinux approach
# 1. Run in permissive, exercise all features
setenforce 0
systemctl start webapp
# Exercise all app functionality
setenforce 1

# 2. Build policy from collected denials
ausearch -m AVC -ts recent | audit2allow -M webapp
semodule -i webapp.pp

# 3. Test in enforcing mode
systemctl restart webapp
# Verify all features work
```

---
## SELinux Port Labeling

`SELinux` controls which ports services can bind to:

```bash
# List all port labels
semanage port -l

# Show ports allowed for HTTP
semanage port -l | grep http_port_t
# http_port_t  tcp  80, 443, 488, 8008, ...

# Allow nginx to bind to a custom port
semanage port -a -t http_port_t -p tcp 9090

# Allow a service to use a non-standard port
semanage port -a -t ssh_port_t -p tcp 2222

# Modify an existing port label
semanage port -m -t http_port_t -p tcp 3000

# Delete a custom port label
semanage port -d -t http_port_t -p tcp 9090
```

```bash
# Common port types:
# http_port_t     - web servers
# ssh_port_t      - SSH
# smtp_port_t     - mail servers
# dns_port_t      - DNS servers
# postgresql_port_t - PostgreSQL
```

---
## AppArmor Network Rules

Control network access per application with `AppArmor`:

```config
# /etc/apparmor.d/usr.local.bin.myservice
/usr/local/bin/myservice {
  #include <abstractions/base>

  # Allow TCP on specific ports
  network inet tcp,
  network inet6 tcp,

  # Allow UDP (e.g., for DNS lookups)
  network inet dgram,
  network inet6 dgram,

  # Deny raw sockets (prevent packet sniffing)
  deny network inet raw,

  # Deny all Unix domain sockets
  deny network unix,

  /usr/local/bin/myservice    mr,
  /etc/myservice/**           r,
  /var/log/myservice/**       rw,
}
```

Network rule syntax:
- `network inet tcp` - allow IPv4 TCP
- `network inet6 dgram` - allow IPv6 UDP
- `network unix stream` - allow Unix stream sockets
- Use `deny` for explicit blocks (logged when in `complain` mode)

---
## MAC in Container Environments

Containers benefit from MAC for defense-in-depth:

```bash
# Docker uses AppArmor by default on Ubuntu
# Check the default profile
docker run --rm alpine cat /proc/1/attr/current

# Run with a custom AppArmor profile
docker run --security-opt \
  apparmor=my-container-profile nginx

# Run with no AppArmor (not recommended)
docker run --security-opt apparmor=unconfined nginx
```

```bash
# SELinux with containers (RHEL/Fedora)
# Containers run with svirt_lv_t by default
ps -eZ | grep container

# Allow container to access host files
chcon -Rt svirt_sandbox_file_t /data/shared

# Podman with SELinux volume labels
podman run -v /host/data:/data:Z myapp
# :Z = private label, :z = shared label
```

Key points:
- Default container profiles block `mount`, `ptrace`, and raw sockets
- Custom profiles can restrict filesystem and network access further
- `SELinux` prevents container escapes via `svirt` separation

---
## Exercise: MAC Policy for a Database Server

Scenario: confine `PostgreSQL` running on a non-standard port `5433`:

1. **SELinux approach** (RHEL/Fedora):

```bash
# Allow PostgreSQL on custom port
semanage port -a -t postgresql_port_t -p tcp 5433

# Verify the label
semanage port -l | grep postgresql

# If PostgreSQL reads from /data/pgdata:
semanage fcontext -a -t postgresql_db_t \
  "/data/pgdata(/.*)?"
restorecon -Rv /data/pgdata
```

1. **AppArmor approach** (Ubuntu):
    - Generate a profile with `aa-genprof /usr/lib/postgresql/16/bin/postgres`
    - Exercise all database operations while profiling
    - Review and tighten the generated profile
    - Ensure network rules allow only TCP on port `5433`
    - Deny access to `/home` and `/tmp` beyond the `PostgreSQL` socket

1. Verify the confined service starts correctly and test that access to unauthorized paths is blocked
