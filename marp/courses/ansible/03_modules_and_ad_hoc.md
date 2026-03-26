# Modules and Ad-Hoc Commands

## Topics Covered
- Understanding `Ansible` modules
- Module categories and common modules
- Ad-hoc command patterns
- Working with module documentation
- Return values and output

---

## What Are Modules?

- Modules are the units of work in `Ansible`
- Each module performs a specific task
- Written mostly in `Python`
- Accept arguments and return `JSON`
- Most modules are **idempotent**
- Over 7,000+ modules available in collections

---

## Module Categories

| Category | Examples |
|----------|---------|
| Cloud | `amazon.aws.ec2_instance`, `azure.azcollection.azure_rm_virtualmachine` |
| Files | `copy`, `file`, `template`, `lineinfile`, `blockinfile` |
| Packaging | `apt`, `yum`, `pip`, `npm` |
| System | `service`, `systemd`, `user`, `group`, `cron` |
| Database | `mysql_db`, `postgresql_db`, `mongodb_user` |
| Network | `ios_command`, `nxos_config`, `vyos_system` |
| Source Control | `git`, `subversion` |
| Utilities | `debug`, `assert`, `set_fact`, `pause` |

---

## Finding Module Documentation

```bash
# List all available modules
ansible-doc -l

# Search for modules by keyword
ansible-doc -l | grep -i "firewall"
ansible-doc -l | grep -i "docker"

# Get full documentation for a module
ansible-doc apt
ansible-doc copy
ansible-doc template

# Show only the examples
ansible-doc apt -s

# Show a module's return values
ansible-doc -t module apt
```

---

## File Modules: copy

```yaml
# Copy a file to remote hosts
- name: Copy application config
  copy:
    src: files/app.conf
    dest: /etc/myapp/app.conf
    owner: root
    group: root
    mode: '0644'
    backup: yes

# Copy content directly
- name: Create MOTD
  copy:
    content: |
      Welcome to {{ inventory_hostname }}
      Environment: {{ env }}
      Managed by Ansible - DO NOT EDIT MANUALLY
    dest: /etc/motd
```

---

## File Modules: file

```yaml
# Create a directory
- name: Create application directory
  file:
    path: /opt/myapp
    state: directory
    owner: appuser
    group: appuser
    mode: '0755'

# Create a symbolic link
- name: Create symlink to current release
  file:
    src: /opt/myapp/releases/v2.1.0
    dest: /opt/myapp/current
    state: link

# Delete a file
- name: Remove old config
  file:
    path: /etc/myapp/old.conf
    state: absent

# Set permissions recursively
- name: Fix permissions
  file:
    path: /var/www/html
    owner: www-data
    group: www-data
    recurse: yes
```

---

## File Modules: lineinfile

```yaml
# Ensure a line exists in a file
- name: Set hostname in /etc/hosts
  lineinfile:
    path: /etc/hosts
    line: "192.168.1.10 myapp.example.com"
    state: present

# Replace a line matching a regex
- name: Set max open files
  lineinfile:
    path: /etc/security/limits.conf
    regexp: '^appuser\s+soft\s+nofile'
    line: 'appuser soft nofile 65536'

# Remove a line
- name: Remove deprecated config
  lineinfile:
    path: /etc/app.conf
    regexp: '^deprecated_option='
    state: absent

# Insert after a specific line
- name: Add config after section header
  lineinfile:
    path: /etc/app.conf
    insertafter: '^\[database\]'
    line: 'pool_size=25'
```

---

## File Modules: blockinfile

```yaml
# Insert a block of text
- name: Add custom SSH config
  blockinfile:
    path: /etc/ssh/sshd_config
    block: |
      Match Group developers
          ChrootDirectory /home/%u
          ForceCommand internal-sftp
          AllowTcpForwarding no
    marker: "# {mark} ANSIBLE MANAGED - Developer SFTP"
  notify: restart sshd

# Insert with a custom marker
- name: Add iptables rules
  blockinfile:
    path: /etc/iptables/rules.v4
    insertbefore: "^-A INPUT -j DROP"
    block: |
      -A INPUT -p tcp --dport 80 -j ACCEPT
      -A INPUT -p tcp --dport 443 -j ACCEPT
    marker: "# {mark} ANSIBLE MANAGED WEB RULES"
```

---

## Package Modules: apt

```yaml
# Install a single package
- name: Install nginx
  apt:
    name: nginx
    state: present

# Install multiple packages
- name: Install web stack
  apt:
    name:
      - nginx
      - php-fpm
      - php-mysql
      - certbot
    state: present
    update_cache: yes
    cache_valid_time: 3600  # Don't update if cache < 1 hour

# Install a specific version
- name: Install specific Node.js version
  apt:
    name: nodejs=18.17.0-1nodesource1
    state: present

# Upgrade all packages
- name: Full system upgrade
  apt:
    upgrade: dist
    update_cache: yes
```

---

## Package Modules: yum / dnf

```yaml
# Install with yum
- name: Install packages (RHEL/CentOS)
  yum:
    name:
      - httpd
      - php
      - mod_ssl
    state: present

# Install with dnf (RHEL 8+)
- name: Install packages (modern RHEL)
  dnf:
    name:
      - nginx
      - python3
    state: latest

# Install from a specific repo
- name: Install from EPEL
  yum:
    name: htop
    enablerepo: epel
    state: present

# Install a local RPM
- name: Install local package
  yum:
    name: /tmp/myapp-1.0.0.rpm
    state: present
```

---

## Package Modules: pip

```yaml
# Install a Python package
- name: Install Flask
  pip:
    name: flask
    state: present

# Install from requirements.txt
- name: Install Python dependencies
  pip:
    requirements: /opt/myapp/requirements.txt
    virtualenv: /opt/myapp/venv
    virtualenv_python: python3

# Install a specific version
- name: Install specific version
  pip:
    name: django==4.2.0

# Install multiple packages
- name: Install Python packages
  pip:
    name:
      - flask==3.0.0
      - gunicorn>=21.0
      - celery[redis]
    virtualenv: /opt/myapp/venv
```

---

## Service Modules: service / systemd

```yaml
# Using service module (generic)
- name: Start and enable nginx
  service:
    name: nginx
    state: started
    enabled: yes

# Using systemd module (more control)
- name: Restart with systemd
  systemd:
    name: nginx
    state: restarted
    daemon_reload: yes

# Reload systemd after unit file change
- name: Reload systemd daemon
  systemd:
    daemon_reload: yes

# Mask a service (prevent it from starting)
- name: Mask unnecessary service
  systemd:
    name: cups
    masked: yes
```

---

## User and Group Modules

```yaml
# Create a group
- name: Create application group
  group:
    name: appgroup
    gid: 1500
    state: present

# Create a user
- name: Create application user
  user:
    name: appuser
    uid: 1500
    group: appgroup
    groups: sudo,docker
    shell: /bin/bash
    home: /home/appuser
    create_home: yes
    comment: "Application Service Account"
    state: present

# Create user with SSH key
- name: Add deploy user with SSH key
  user:
    name: deploy
    groups: sudo
    append: yes
  register: deploy_user

- name: Set authorized key
  authorized_key:
    user: deploy
    key: "{{ lookup('file', 'files/deploy_key.pub') }}"
```

---

## Cron Module

```yaml
# Create a cron job
- name: Schedule database backup
  cron:
    name: "Database backup"
    minute: "0"
    hour: "2"
    job: "/opt/scripts/backup_db.sh >> /var/log/backup.log 2>&1"
    user: postgres

# Create a cron job with special time
- name: Run cleanup on reboot
  cron:
    name: "Cleanup on reboot"
    special_time: reboot
    job: "/opt/scripts/cleanup.sh"

# Remove a cron job
- name: Remove old backup job
  cron:
    name: "Old backup"
    state: absent

# Create a cron environment variable
- name: Set cron PATH
  cron:
    name: PATH
    env: yes
    value: "/usr/local/bin:/usr/bin:/bin"
```

---

## Git Module

```yaml
# Clone a repository
- name: Clone application repository
  git:
    repo: https://github.com/myorg/myapp.git
    dest: /opt/myapp
    version: main
    force: yes

# Clone a specific branch/tag
- name: Deploy release v2.1.0
  git:
    repo: git@github.com:myorg/myapp.git
    dest: /opt/myapp
    version: v2.1.0
    accept_hostkey: yes
    key_file: /home/deploy/.ssh/deploy_key

# Update to latest
- name: Pull latest changes
  git:
    repo: https://github.com/myorg/myapp.git
    dest: /opt/myapp
    version: main
    update: yes
  register: git_result
  changed_when: git_result.after != git_result.before
```

---

## URI Module (HTTP Requests)

```yaml
# Simple GET request
- name: Check if service is up
  uri:
    url: http://localhost:8080/health
    return_content: yes
  register: health_check
  failed_when: health_check.json.status != "healthy"

# POST request with JSON body
- name: Create user via API
  uri:
    url: https://api.example.com/users
    method: POST
    body:
      username: newuser
      email: newuser@example.com
    body_format: json
    headers:
      Authorization: "Bearer {{ api_token }}"
    status_code: 201

# Download a file
- name: Download artifact
  uri:
    url: https://releases.example.com/app-v2.0.tar.gz
    dest: /tmp/app-v2.0.tar.gz
    creates: /tmp/app-v2.0.tar.gz
```

---

## Wait For Module

```yaml
# Wait for a port to become available
- name: Wait for PostgreSQL to start
  wait_for:
    port: 5432
    delay: 5
    timeout: 60

# Wait for a file to exist
- name: Wait for application to write PID file
  wait_for:
    path: /var/run/myapp.pid
    state: present
    timeout: 30

# Wait for a port to close (service stopped)
- name: Wait for old service to stop
  wait_for:
    port: 8080
    state: stopped
    timeout: 120

# Wait for a string in a log file
- name: Wait for application to be ready
  wait_for:
    path: /var/log/myapp/startup.log
    search_regex: "Application started successfully"
    timeout: 120
```

---

## Debug and Assert Modules

```yaml
# Print a variable
- name: Show hostname
  debug:
    var: ansible_hostname

# Print a message
- name: Display deployment info
  debug:
    msg: "Deploying version {{ app_version }} to {{ env }}"

# Print with verbosity control
- name: Show detailed info (only with -vv)
  debug:
    var: ansible_all_ipv4_addresses
    verbosity: 2

# Assert a condition
- name: Verify minimum memory
  assert:
    that:
      - ansible_memtotal_mb >= 2048
      - ansible_processor_vcpus >= 2
    fail_msg: "Server does not meet minimum requirements"
    success_msg: "Server meets requirements"
```

---

## Register and Return Values

```yaml
# Capture command output
- name: Get current date
  command: date +%Y%m%d
  register: date_result
  changed_when: false

- name: Show the date
  debug:
    msg: "Today is {{ date_result.stdout }}"

# Common return value attributes:
# .stdout       - standard output (string)
# .stdout_lines - stdout as a list of lines
# .stderr       - standard error
# .rc           - return code
# .changed      - whether the task changed anything
# .failed       - whether the task failed
# .results      - list of results (for loops)

- name: Check if app is running
  command: pgrep -f myapp
  register: pgrep_result
  ignore_errors: yes

- name: Start app if not running
  command: /opt/myapp/start.sh
  when: pgrep_result.rc != 0
```

---

## Module Return Values Example

```yaml
- name: Install packages and capture result
  apt:
    name: nginx
    state: present
  register: apt_result

- name: Show what happened
  debug:
    var: apt_result

# Output looks like:
# apt_result:
#   cache_update_time: 1703001234
#   cache_updated: false
#   changed: true
#   stderr: ""
#   stdout: "Reading package lists..."
#   stdout_lines: [...]
```

---

## Practical Ad-Hoc Patterns

```bash
# System Information
ansible all -m setup -a "filter=ansible_distribution*"
ansible all -m shell -a "free -m | head -3"
ansible all -m shell -a "lsblk"

# Security
ansible all -m shell -a "last -5" --become
ansible all -m shell -a "ss -tlnp" --become

# Application Management
ansible webservers -m shell -a "curl -s localhost/health"
ansible all -m shell -a "docker ps --format 'table {{.Names}}\t{{.Status}}'"

# Bulk Operations
ansible all -m shell -a "apt list --upgradable 2>/dev/null" --become
ansible all -m shell -a "journalctl -u nginx --since '1 hour ago' --no-pager"
```

---

## Ad-Hoc with Loops (One-Liners)

```bash
# Update multiple config values
ansible webservers -m lineinfile \
    -a "path=/etc/myapp.conf regexp='^max_connections' \
        line='max_connections=500'" --become

# Restart multiple services sequentially
for svc in nginx php-fpm redis; do
    ansible webservers -m service \
        -a "name=$svc state=restarted" --become
done

# Gather specific facts from all hosts
ansible all -m setup \
    -a "filter=ansible_default_ipv4" \
    --tree /tmp/facts/
```

---

## Module Best Practices

- Prefer specific modules over `command`/`shell`
- Use `command` module only when no specific module exists
- Always use fully qualified collection names (FQCN) for clarity
- Check module documentation for all available parameters
- Use `register` to capture output for later decisions
- Set `changed_when: false` for read-only commands
- Use `creates`/`removes` parameters to make commands idempotent

```yaml
# BAD: Using shell to install a package
- name: Install nginx
  shell: apt-get install -y nginx

# GOOD: Using the apt module
- name: Install nginx
  ansible.builtin.apt:
    name: nginx
    state: present
```
