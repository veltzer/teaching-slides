---
tags:
  - practices:devops
  - tools:ansible
  - infrastructure:configuration-management
  - infrastructure:cloud
  - practices:automation
level: intermediate
category: devops
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---

# Ansible Fundamentals

## Course Overview
- 3-day comprehensive `Ansible` training
- Day 1: Fundamentals, inventory, ad-hoc commands, playbook basics
- Day 2: Playbooks, roles, advanced features, secrets management
- Day 3: Advanced patterns, custom modules, Tower/AWX, CI/CD

---

## What is Ansible?

- Open-source automation platform by Red Hat
- Configuration management, application deployment, orchestration
- Written in `Python`, uses `YAML` for configuration
- Communicates over `SSH` (Linux) or `WinRM` (Windows)
- No agents required on managed nodes ("agentless")

---

## Architecture

![ansible_arch](svg/courses/devops/ansible/01_fundamentals/ansible_arch.svg)

---

## Why Ansible?

- **Simple**: `YAML`-based, human-readable playbooks
- **Agentless**: No software to install on managed nodes
- **Powerful**: Orchestrate complex multi-tier deployments
- **Flexible**: Works with cloud, on-prem, containers, network devices
- **Extensible**: Custom modules in any language
- **Idempotent**: Safe to run multiple times

---

## Ansible vs Other Tools

| Feature | `Ansible` | `Puppet` | `Chef` | `SaltStack` |
|---------|---------|--------|------|-----------|
| Language | `YAML` | Ruby DSL | Ruby DSL | `YAML` |
| Architecture | Agentless | Agent-based | Agent-based | Agent/Agentless |
| Transport | `SSH` | HTTPS | HTTPS | ZeroMQ/`SSH` |
| Learning Curve | Low | Medium | High | Medium |
| Push/Pull | Push | Pull | Pull | Both |

---

## Ansible Architecture

![ansible_architecture](svg/courses/devops/ansible/01_fundamentals/ansible_architecture.svg)

---

## How Ansible Works

1. Reads inventory to discover target hosts
1. Connects to managed nodes via `SSH`
1. Copies small programs ("modules") to managed nodes
1. Executes modules on managed nodes
1. Removes modules after execution
1. Reports results back to control node

---

## Key Concepts

- **Control Node**: Machine where `Ansible` is installed and runs from
- **Managed Node**: Target machine being configured
- **Inventory**: List of managed nodes
- **Module**: Unit of work (e.g., `copy`, `yum`, `service`)
- **Task**: A single action using a module
- **Play**: Maps hosts to tasks
- **Playbook**: A file containing one or more plays

---

## Agentless Design Deep Dive

- Only requirement on managed nodes: `Python` (2.7+ or 3.5+) and `SSH`
- Modules are transferred, executed, then removed
- No daemon running, no ports to open, no PKI to manage
- Reduces attack surface and maintenance overhead
- Uses `OpenSSH` for transport (battle-tested security)

---

## Agentless vs Agent-Based

![agentless_vs_agent_based](svg/courses/devops/ansible/01_fundamentals/agentless_vs_agent_based.svg)

---

## Ansible Use Cases

- **Configuration Management**: Ensure servers are in desired state
- **Application Deployment**: Deploy code to multiple servers
- **Orchestration**: Coordinate multi-tier application rollouts
- **Provisioning**: Create cloud infrastructure (AWS, Azure, GCP)
- **Security & Compliance**: Enforce security policies
- **Network Automation**: Configure routers, switches, firewalls

---

## Real-World Ansible Adoption

- NASA uses `Ansible` to manage satellite ground systems
- Red Hat uses `Ansible` internally for IT automation
- Major banks use `Ansible` for compliance automation
- Telecom companies use `Ansible` for network device management
- Over 20,000+ community modules available on `Ansible Galaxy`

---

## Ansible Components Overview

![ansible_components_overview](svg/courses/devops/ansible/01_fundamentals/ansible_components_overview.svg)

---

## Ansible Versions

- **Ansible (community)**: Full package with collections
- **ansible-core**: Minimal engine, fewer built-in modules
- Version scheme: `ansible-core` 2.14, 2.15, 2.16, 2.17
- `ansible` package: 7.x, 8.x, 9.x, 10.x (bundles collections)
- Always check compatibility matrix for your environment

---

## Prerequisites for This Course

- Basic Linux command-line skills
- Understanding of `SSH` key-based authentication
- Familiarity with `YAML` syntax
- Basic `Python` knowledge (helpful but not required)
- Access to lab environment with control + managed nodes

---

## YAML Crash Course

- `YAML` = "YAML Ain't Markup Language"
- Indentation-based (spaces only, no tabs!)
- Key-value pairs, lists, and dictionaries
- Used for playbooks, inventory, variable files, and configuration

```yaml
# Key-value pairs
name: webserver
port: 8080
enabled: true

# List
packages:
  - nginx
  - python3
  - git
```

---

## YAML Data Types

```yaml
# Strings
name: "hello world"
unquoted: hello world

# Numbers
port: 8080
ratio: 3.14

# Booleans
enabled: true
debug: false

# Null
value: null
also_null: ~

# Multiline strings
description: |
  This preserves
  line breaks
folded: >
  This folds into
  a single line
```

---

## YAML Lists and Dictionaries

```yaml
# List (block style)
fruits:
  - apple
  - banana
  - cherry

# List (inline style)
fruits: [apple, banana, cherry]

# Dictionary (block style)
server:
  name: web01
  ip: 192.168.1.10
  port: 80

# Dictionary (inline style)
server: {name: web01, ip: 192.168.1.10}
```

---

## YAML Gotchas in Ansible

```yaml
# GOTCHA 1: Boolean strings
# These are all interpreted as boolean true:
values:
  - yes    # true
  - Yes    # true
  - TRUE   # true
  - on     # true

# Fix: Quote them
safe_values:
  - "yes"
  - "on"

# GOTCHA 2: Colon in values
# This breaks:
# message: Error: file not found
# Fix:
message: "Error: file not found"

# GOTCHA 3: Starting with special chars
# name: {{variable}}     # BREAKS
name: "{{ variable }}"   # Works
```

---

## Lab Environment Setup

![lab_environment_setup](svg/courses/devops/ansible/01_fundamentals/lab_environment_setup.svg)

---

## Installing Ansible - Ubuntu/Debian

```bash
# Method 1: APT (system package)
sudo apt update
sudo apt install ansible

# Method 2: pip (recommended for latest version)
sudo apt install python3-pip
pip3 install ansible

# Method 3: pipx (isolated environment)
pipx install ansible

# Verify installation
ansible --version
```

---

## Installing Ansible - RHEL/CentOS

```bash
# Method 1: DNF (RHEL 8+)
sudo dnf install ansible-core

# Method 2: YUM (RHEL 7)
sudo yum install epel-release
sudo yum install ansible

# Method 3: pip
sudo dnf install python3-pip
pip3 install ansible

# Verify
ansible --version
ansible-community --version
```

---

## Installing Ansible - macOS

```bash
# Method 1: Homebrew
brew install ansible

# Method 2: pip
pip3 install ansible

# Method 3: pipx
pipx install ansible

# Verify
ansible --version
which ansible
```

---

## Verifying Your Installation

```bash
$ ansible --version
ansible [core 2.16.0]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/user/.ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  ansible collection location = /home/user/.ansible/collections
  executable location = /usr/bin/ansible
  python version = 3.10.12
  jinja version = 3.1.2
  libyaml = True
```

---

## Ansible Configuration File

- `Ansible` looks for config in this order:
    1. `ANSIBLE_CONFIG` environment variable
    1. `./ansible.cfg` (current directory)
    1. `~/.ansible.cfg` (home directory)
    1. `/etc/ansible/ansible.cfg` (global)

- First file found wins (no merging)

---

## Basic ansible.cfg

```ini
[defaults]
inventory = ./inventory
remote_user = ansible
ask_pass = false
host_key_checking = false
retry_files_enabled = false
stdout_callback = yaml

[privilege_escalation]
become = true
become_method = sudo
become_user = root
become_ask_pass = false

[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s
pipelining = true
```

---

## Important Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `inventory` | Path to inventory file | `/etc/ansible/hosts` |
| `remote_user` | SSH user for connections | Current user |
| `become` | Enable privilege escalation | `false` |
| `forks` | Parallel processes | `5` |
| `timeout` | SSH connection timeout | `10` |
| `host_key_checking` | Verify SSH host keys | `true` |
| `log_path` | Log file location | None |

---

## Setting Up SSH Keys

```bash
# Generate SSH key pair on control node
ssh-keygen -t ed25519 -C "ansible-control"

# Copy public key to managed nodes
ssh-copy-id ansible@web01
ssh-copy-id ansible@db01

# Test connectivity
ssh ansible@web01 "hostname"
ssh ansible@db01 "hostname"

# For multiple hosts at once
for host in web01 web02 db01 db02; do
    ssh-copy-id ansible@$host
done
```

---

## Creating the Ansible User

```bash
# On each managed node, create a dedicated ansible user
sudo useradd -m -s /bin/bash ansible
sudo passwd ansible

# Grant sudo access without password
echo "ansible ALL=(ALL) NOPASSWD: ALL" | \
    sudo tee /etc/sudoers.d/ansible

# Verify
sudo -l -U ansible
```

---

## Inventory Basics

- The inventory defines which hosts `Ansible` manages
- Can be a simple `INI` or `YAML` file
- Groups hosts logically
- Assigns variables to hosts and groups

```ini
# inventory (INI format)
[webservers]
web01 ansible_host=192.168.56.20
web02 ansible_host=192.168.56.21

[dbservers]
db01 ansible_host=192.168.56.30

[all:vars]
ansible_user=ansible
ansible_python_interpreter=/usr/bin/python3
```

---

## Inventory in YAML Format

```yaml
# inventory.yml
all:
  vars:
    ansible_user: ansible
    ansible_python_interpreter: /usr/bin/python3
  children:
    webservers:
      hosts:
        web01:
          ansible_host: 192.168.56.20
        web02:
          ansible_host: 192.168.56.21
    dbservers:
      hosts:
        db01:
          ansible_host: 192.168.56.30
```

---

## Inventory Groups

```ini
# Groups can be nested
[webservers]
web01
web02

[dbservers]
db01
db02

[monitoring]
nagios01

# Group of groups
[production:children]
webservers
dbservers

# All production servers inherit these vars
[production:vars]
env=production
ntp_server=ntp.prod.example.com
```

---

## Special Inventory Groups

- `all`: Every host in the inventory (implicit)
- `ungrouped`: Hosts not in any explicit group

```ini
# These hosts are in 'ungrouped'
jumpbox ansible_host=10.0.0.1
bastion ansible_host=10.0.0.2

[webservers]
web01
web02

# 'all' includes jumpbox, bastion, web01, web02
# 'ungrouped' includes only jumpbox, bastion
```

---

## Host Variables in Inventory

```ini
[webservers]
web01 ansible_host=192.168.56.20 http_port=80 max_clients=200
web02 ansible_host=192.168.56.21 http_port=8080 max_clients=100

[dbservers]
db01 ansible_host=192.168.56.30 db_port=5432 db_name=appdb
```

```yaml
# YAML equivalent
webservers:
  hosts:
    web01:
      ansible_host: 192.168.56.20
      http_port: 80
      max_clients: 200
    web02:
      ansible_host: 192.168.56.21
      http_port: 8080
      max_clients: 100
```

---

## Group Variables in Inventory

```ini
[webservers]
web01
web02

[webservers:vars]
http_port=80
document_root=/var/www/html
max_clients=256

[dbservers]
db01

[dbservers:vars]
db_port=5432
max_connections=100
```

---

## Host and Group Variable Files

```tree
project/
├── ansible.cfg
├── inventory
├── host_vars/
│   ├── web01.yml        # Variables for web01
│   └── db01.yml         # Variables for db01
├── group_vars/
│   ├── all.yml          # Variables for all hosts
│   ├── webservers.yml   # Variables for webservers group
│   └── dbservers.yml    # Variables for dbservers group
└── playbooks/
```

---

## Host Vars File Example

```yaml
# host_vars/web01.yml

---
ansible_host: 192.168.56.20
http_port: 80
ssl_enabled: true
ssl_cert_path: /etc/ssl/certs/web01.pem
vhosts:
  - name: app.example.com
    document_root: /var/www/app
    port: 443
  - name: api.example.com
    document_root: /var/www/api
    port: 8443
```

---

## Group Vars File Example

```yaml
# group_vars/webservers.yml

---
nginx_version: "1.24"
nginx_worker_processes: auto
nginx_worker_connections: 1024

firewall_allowed_ports:
  - 80
  - 443

log_rotation:
  max_size: 100M
  keep_days: 30
  compress: true

monitoring:
  enabled: true
  endpoint: http://nagios.example.com/api
```

---

## Inventory Ranges and Patterns

```ini
# Numeric ranges
[webservers]
web[01:10]          # web01 through web10

# Alphabetic ranges
[databases]
db-[a:f]            # db-a through db-f

# Using patterns in commands
ansible web* -m ping              # All hosts starting with web
ansible webservers:dbservers -m ping  # Union of two groups
ansible webservers:&production -m ping  # Intersection
ansible webservers:!web01 -m ping     # Exclude web01
```

---

## Multiple Inventory Sources

```bash
# Directory-based inventory
inventory/
├── production
├── staging
└── development

# Use a directory
ansible-playbook -i inventory/ site.yml

# Or specify multiple files
ansible-playbook -i production -i staging site.yml

# In ansible.cfg
[defaults]
inventory = inventory/production,inventory/staging
```

---

## Verifying Your Inventory

```bash
# List all hosts
ansible all --list-hosts -i inventory

# List hosts in a group
ansible webservers --list-hosts -i inventory

# Show inventory as a graph
ansible-inventory --graph -i inventory

# Show inventory as JSON
ansible-inventory --list -i inventory

# Show variables for a specific host
ansible-inventory --host web01 -i inventory
```

---

## Inventory Graph Output

```bash
$ ansible-inventory --graph
@all:
  |--@ungrouped:
  |--@production:
  |  |--@webservers:
  |  |  |--web01
  |  |  |--web02
  |  |--@dbservers:
  |  |  |--db01
  |  |  |--db02
  |--@monitoring:
  |  |--nagios01
```

---

## Ad-Hoc Commands

- Quick, one-line `Ansible` commands
- Great for one-time tasks and testing
- Not reusable like playbooks
- Syntax: `ansible <pattern> -m <module> -a "<args>"`

```bash
# Test connectivity
ansible all -m ping

# Run a shell command
ansible all -m shell -a "uptime"

# Check disk space
ansible webservers -m command -a "df -h"
```

---

## Common Ad-Hoc Examples

```bash
# Gather facts about a host
ansible web01 -m setup

# Copy a file to all webservers
ansible webservers -m copy \
    -a "src=/tmp/config.conf dest=/etc/app/config.conf"

# Install a package
ansible webservers -m apt \
    -a "name=nginx state=present" --become

# Start a service
ansible webservers -m service \
    -a "name=nginx state=started enabled=yes" --become

# Create a user
ansible all -m user \
    -a "name=deploy state=present groups=sudo" --become
```

---

## The command vs shell Module

```bash
# command module (default): Doesn't use shell
# - No pipes, redirects, or shell variables
# - Safer, more predictable
ansible all -m command -a "ls /tmp"

# shell module: Runs through /bin/sh
# - Supports pipes, redirects, variables
# - Less safe (shell injection risk)
ansible all -m shell -a "cat /etc/passwd | grep root"

# raw module: Doesn't need Python
# - Used for bootstrapping Python on nodes
ansible all -m raw -a "apt install -y python3"
```

---

## Managing Files with Ad-Hoc

```bash
# Copy a file
ansible all -m copy \
    -a "src=./motd dest=/etc/motd owner=root mode=0644" \
    --become

# Create a directory
ansible all -m file \
    -a "path=/opt/myapp state=directory mode=0755" \
    --become

# Download a file from URL
ansible all -m get_url \
    -a "url=https://example.com/file.tar.gz dest=/tmp/"

# Create a symlink
ansible all -m file \
    -a "src=/opt/myapp/current dest=/opt/myapp/latest state=link"

# Delete a file
ansible all -m file -a "path=/tmp/junk state=absent"
```

---

## Managing Packages with Ad-Hoc

```bash
# APT (Debian/Ubuntu)
ansible webservers -m apt \
    -a "name=nginx state=latest update_cache=yes" --become

# YUM/DNF (RHEL/CentOS)
ansible dbservers -m yum \
    -a "name=postgresql state=present" --become

# Install multiple packages
ansible all -m apt \
    -a "name=git,curl,wget state=present" --become

# Remove a package
ansible all -m apt \
    -a "name=apache2 state=absent" --become
```

---

## Managing Services with Ad-Hoc

```bash
# Start a service
ansible webservers -m service \
    -a "name=nginx state=started" --become

# Stop a service
ansible webservers -m service \
    -a "name=nginx state=stopped" --become

# Restart a service
ansible webservers -m service \
    -a "name=nginx state=restarted" --become

# Enable a service at boot
ansible webservers -m service \
    -a "name=nginx enabled=yes" --become

# Check service status
ansible webservers -m shell -a "systemctl status nginx"
```

---

## Gathering Facts with Ad-Hoc

```bash
# Get all facts
ansible web01 -m setup

# Filter facts
ansible web01 -m setup -a "filter=ansible_os_family"
ansible web01 -m setup -a "filter=ansible_distribution*"
ansible web01 -m setup -a "filter=ansible_memory_mb"

# Common useful facts:
# ansible_hostname          - short hostname
# ansible_fqdn              - fully qualified domain name
# ansible_default_ipv4      - primary IPv4 info
# ansible_os_family         - Debian, RedHat, etc.
# ansible_distribution      - Ubuntu, CentOS, etc.
# ansible_memtotal_mb       - total RAM in MB
# ansible_processor_vcpus   - number of vCPUs
```

---

## Ad-Hoc Command Options

| Option | Description |
|--------|-------------|
| `-i` | Inventory file |
| `-m` | Module name |
| `-a` | Module arguments |
| `-b` / `--become` | Use sudo |
| `-K` / `--ask-become-pass` | Prompt for sudo password |
| `-u` | Remote user |
| `-k` / `--ask-pass` | Prompt for SSH password |
| `-f` | Number of forks (parallelism) |
| `-v` / `-vvv` / `-vvvv` | Verbosity level |
| `--check` | Dry run mode |

---

## Introduction to Playbooks

- Playbooks are `YAML` files describing desired state
- Contain one or more "plays"
- Each play targets a set of hosts
- Each play contains ordered list of tasks
- Tasks call modules with specific arguments
- Playbooks are **idempotent**: safe to run repeatedly

---

## Your First Playbook

```yaml
# first_playbook.yml

---
- name: My first playbook
  hosts: webservers
  become: true

  tasks:
    - name: Ensure nginx is installed
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Ensure nginx is running
      service:
        name: nginx
        state: started
        enabled: yes
```

---

## Running a Playbook

```bash
# Basic execution
ansible-playbook first_playbook.yml

# Specify inventory
ansible-playbook -i inventory first_playbook.yml

# Dry run (check mode)
ansible-playbook --check first_playbook.yml

# Verbose output
ansible-playbook -v first_playbook.yml    # minimal
ansible-playbook -vv first_playbook.yml   # more detail
ansible-playbook -vvv first_playbook.yml  # connection info
ansible-playbook -vvvv first_playbook.yml # maximum debug

# Limit to specific hosts
ansible-playbook --limit web01 first_playbook.yml
```

---

## Playbook Structure

```yaml

---
# Play 1
- name: Configure webservers
  hosts: webservers
  become: true
  vars:
    http_port: 80
  tasks:
    - name: Task 1
      # ...
    - name: Task 2
      # ...
  handlers:
    - name: Handler 1
      # ...

# Play 2
- name: Configure databases
  hosts: dbservers
  become: true
  tasks:
    - name: Task A
      # ...
```

---

## Play Keywords

| Keyword | Description |
|---------|-------------|
| `name` | Description of the play |
| `hosts` | Target hosts/groups |
| `become` | Enable privilege escalation |
| `become_user` | User to become (default: root) |
| `vars` | Variables for this play |
| `vars_files` | Load variables from files |
| `tasks` | List of tasks to execute |
| `handlers` | Tasks triggered by `notify` |
| `pre_tasks` | Tasks run before roles |
| `post_tasks` | Tasks run after roles |
| `roles` | List of roles to apply |
| `gather_facts` | Gather host facts (default: true) |

---

## Task Syntax

```yaml
tasks:
  # Full syntax
  - name: Install nginx
    ansible.builtin.apt:
      name: nginx
      state: present
    become: true
    when: ansible_os_family == "Debian"
    tags:
      - packages
      - webserver

  # Short syntax (module as key)
  - name: Check uptime
    command: uptime

  # With register to capture output
  - name: Check disk space
    command: df -h
    register: disk_output
```

---

## Handlers

- Special tasks that run only when notified
- Triggered by the `notify` keyword in a task
- Run once at the end of all tasks (even if notified multiple times)
- Common use: restart services after config changes

```yaml
tasks:
  - name: Update nginx config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: restart nginx

  - name: Update SSL cert
    copy:
      src: ssl.pem
      dest: /etc/ssl/certs/app.pem
    notify: restart nginx

handlers:
  - name: restart nginx
    service:
      name: nginx
      state: restarted
```

---

## Handler Execution Order

```yaml
# Handlers run in the ORDER THEY ARE DEFINED,
# not the order they are notified

handlers:
  - name: restart nginx     # Runs first (defined first)
    service:
      name: nginx
      state: restarted

  - name: restart php-fpm   # Runs second
    service:
      name: php-fpm
      state: restarted

# To force handlers to run mid-play:
tasks:
  - name: Update config
    template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    notify: restart nginx

  - meta: flush_handlers    # Forces handlers to run NOW

  - name: Verify nginx is up
    uri:
      url: http://localhost
```

---

## Multiple Handlers

```yaml
tasks:
  - name: Update application config
    template:
      src: app.conf.j2
      dest: /etc/myapp/config.yml
    notify:
      - restart application
      - clear cache
      - send notification

handlers:
  - name: restart application
    service:
      name: myapp
      state: restarted

  - name: clear cache
    command: /opt/myapp/bin/clear-cache

  - name: send notification
    uri:
      url: https://hooks.slack.com/services/XXX
      method: POST
      body: '{"text": "App config updated"}'
      body_format: json
```

---

## Complete Playbook: Web Server Setup

```yaml

---
- name: Setup web servers
  hosts: webservers
  become: true
  vars:
    packages:
      - nginx
      - certbot
      - python3-certbot-nginx

  tasks:
    - name: Install required packages
      apt:
        name: "{{ packages }}"
        state: present
        update_cache: yes

    - name: Deploy nginx configuration
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/nginx.conf
        backup: yes
      notify: reload nginx

    - name: Create web root directory
      file:
        path: /var/www/myapp
        state: directory
        owner: www-data
        group: www-data
        mode: '0755'

    - name: Deploy index page
      copy:
        src: files/index.html
        dest: /var/www/myapp/index.html
        owner: www-data
        group: www-data
```

---

## Web Server Setup: Service and Handlers

```yaml
    - name: Ensure nginx is started
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: reload nginx
      service:
        name: nginx
        state: reloaded
```

---

## Playbook: Database Server Setup

```yaml

---
- name: Setup PostgreSQL database servers
  hosts: dbservers
  become: true

  tasks:
    - name: Install PostgreSQL
      apt:
        name:
          - postgresql
          - postgresql-contrib
          - python3-psycopg2
        state: present

    - name: Ensure PostgreSQL is running
      service:
        name: postgresql
        state: started
        enabled: yes

    - name: Create application database
      become_user: postgres
      postgresql_db:
        name: myapp_db
        state: present

    - name: Create database user
      become_user: postgres
      postgresql_user:
        db: myapp_db
        name: myapp_user
        password: "{{ db_password }}"
        priv: ALL
        state: present
```

---

## Idempotency

- Running a playbook multiple times produces the same result
- Tasks check current state before making changes
- `changed` = action was taken; `ok` = already in desired state

```bash
# First run: installs packages, creates files
$ ansible-playbook setup.yml
TASK [Install nginx] ***********************
changed: [web01]

# Second run: nothing to do
$ ansible-playbook setup.yml
TASK [Install nginx] ***********************
ok: [web01]
```

---

## Playbook Output Explained

```output
PLAY [Setup web servers] ***************

TASK [Gathering Facts] *****************
ok: [web01]
ok: [web02]

TASK [Install nginx] *******************
changed: [web01]
ok: [web02]

TASK [Deploy config] *******************
changed: [web01]
changed: [web02]

RUNNING HANDLER [reload nginx] *********
changed: [web01]
changed: [web02]

PLAY RECAP *****************************
web01    : ok=4  changed=3  unreachable=0  failed=0  skipped=0
web02    : ok=4  changed=2  unreachable=0  failed=0  skipped=0
```

---

## Check Mode and Diff Mode

```bash
# Check mode: dry run, no changes made
ansible-playbook --check site.yml

# Diff mode: show what would change
ansible-playbook --diff site.yml

# Combine both
ansible-playbook --check --diff site.yml

# In a task, force check mode behavior
- name: Always runs in check mode
  command: validate-config.sh
  check_mode: yes

# Or force a task to always execute (even in check mode)
- name: Always runs even in check mode
  command: echo "gathering data"
  check_mode: no
```

---

## Useful Ansible Commands

```bash
# List all available modules
ansible-doc -l

# Get documentation for a module
ansible-doc apt
ansible-doc copy
ansible-doc template

# List all hosts in inventory
ansible all --list-hosts

# Test connectivity
ansible all -m ping

# Syntax check a playbook
ansible-playbook --syntax-check site.yml

# List tasks in a playbook
ansible-playbook --list-tasks site.yml

# List hosts targeted by a playbook
ansible-playbook --list-hosts site.yml
```

---

## Exercise: Day 1 Lab

1. Set up `ansible.cfg` in your project directory
1. Create an inventory file with at least 2 groups
1. Set up `host_vars` and `group_vars` directories
1. Test connectivity with `ansible all -m ping`
1. Use ad-hoc commands to:
    - Check disk space on all hosts
    - Install `htop` on all hosts
    - Create a directory `/opt/myapp` on webservers
1. Write a playbook that:
    - Installs `nginx` on webservers
    - Installs `postgresql` on dbservers
    - Starts and enables both services
    - Uses handlers for service restarts

---

## Day 1 Summary

- `Ansible` is an agentless automation tool using `SSH` and `Python`
- Configuration is done in `YAML`
- Inventory defines managed hosts and their variables
- Ad-hoc commands are great for quick, one-off tasks
- Playbooks describe desired state in a repeatable way
- Handlers run only when notified (typically for service restarts)
- Idempotency ensures playbooks are safe to run multiple times
