# Playbook Basics

## Topics Covered
- Playbook structure and execution
- Variables and variable precedence
- Gathering and using facts
- Basic conditionals with `when`
- Iterating with loops
- Tags for selective execution

---

## Playbook Execution Flow

```
ansible-playbook site.yml
         |
         v
  Parse YAML file
         |
         v
  For each play:
    1. Select hosts from inventory
    2. Gather facts (if enabled)
    3. Execute pre_tasks
    4. Execute roles
    5. Execute tasks (in order)
    6. Execute post_tasks
    7. Run notified handlers
         |
         v
  Display play recap
```

---

## Defining Variables in Playbooks

```yaml
---
- name: Deploy application
  hosts: webservers
  become: true

  vars:
    app_name: mywebapp
    app_version: "2.1.0"
    app_port: 8080
    app_user: appuser
    app_home: "/opt/{{ app_name }}"
    packages:
      - nginx
      - python3
      - python3-venv

  tasks:
    - name: Create app directory
      file:
        path: "{{ app_home }}"
        state: directory
        owner: "{{ app_user }}"

    - name: Install required packages
      apt:
        name: "{{ packages }}"
        state: present
```

---

## Variable Sources

```yaml
# 1. In playbook (vars section)
vars:
  http_port: 80

# 2. In external files (vars_files)
vars_files:
  - vars/common.yml
  - "vars/{{ env }}.yml"

# 3. Prompted from user (vars_prompt)
vars_prompt:
  - name: admin_password
    prompt: "Enter admin password"
    private: yes

# 4. Command line (highest priority)
# ansible-playbook site.yml -e "http_port=8080"
# ansible-playbook site.yml -e "@vars/override.yml"

# 5. Registered variables
- command: hostname -f
  register: fqdn_result
```

---

## Variable Files

```yaml
# vars/common.yml
---
ntp_servers:
  - 0.pool.ntp.org
  - 1.pool.ntp.org
dns_servers:
  - 8.8.8.8
  - 8.8.4.4
timezone: UTC
log_retention_days: 30

# vars/production.yml
---
env: production
debug_mode: false
replicas: 3
db_host: db.prod.internal

# vars/staging.yml
---
env: staging
debug_mode: true
replicas: 1
db_host: db.staging.internal
```

---

## Using Variables

```yaml
tasks:
  # Simple variable substitution
  - name: Set hostname
    hostname:
      name: "{{ inventory_hostname }}"

  # Variable in a string
  - name: Create config from template
    template:
      src: "{{ app_name }}.conf.j2"
      dest: "/etc/{{ app_name }}/config.conf"

  # Dictionary access
  - name: Show IP address
    debug:
      msg: "IP is {{ ansible_default_ipv4.address }}"

  # List access
  - name: Show first DNS server
    debug:
      msg: "Primary DNS: {{ dns_servers[0] }}"

  # Default values
  - name: Use default if undefined
    debug:
      msg: "Port: {{ http_port | default(80) }}"
```

---

## Variable Precedence (Simplified)

```
Most Important (wins):
  1. Extra vars (-e)
  2. Task vars
  3. Block vars
  4. Role and include vars
  5. Play vars_files
  6. Play vars
  7. Host facts
  8. Registered vars
  9. Set facts
  10. host_vars/
  11. group_vars/ (child groups)
  12. group_vars/ (parent groups)
  13. group_vars/all
  14. Inventory host_vars
  15. Inventory group_vars
  16. Role defaults
Least Important:
```

---

## Ansible Facts

- Facts are system information gathered automatically
- Collected at the start of each play by the `setup` module
- Available as `ansible_*` variables
- Can be disabled with `gather_facts: false`

```yaml
- name: Show system facts
  hosts: all
  tasks:
    - name: Print OS info
      debug:
        msg: >
          {{ ansible_hostname }} runs
          {{ ansible_distribution }} {{ ansible_distribution_version }}
          with {{ ansible_memtotal_mb }}MB RAM
          and {{ ansible_processor_vcpus }} CPUs
```

---

## Commonly Used Facts

```yaml
# Operating System
ansible_os_family          # "Debian", "RedHat", "Windows"
ansible_distribution       # "Ubuntu", "CentOS", "Fedora"
ansible_distribution_version  # "22.04", "8.5"
ansible_distribution_release  # "jammy", "focal"

# Network
ansible_hostname           # "web01"
ansible_fqdn               # "web01.example.com"
ansible_default_ipv4.address  # "192.168.1.10"
ansible_all_ipv4_addresses    # ["192.168.1.10", "10.0.0.5"]

# Hardware
ansible_memtotal_mb        # 4096
ansible_processor_vcpus    # 4
ansible_devices             # disk info

# Date/Time
ansible_date_time.iso8601  # "2024-01-15T10:30:00Z"
ansible_date_time.date     # "2024-01-15"
```

---

## Custom Facts (Local Facts)

```bash
# Place custom facts on managed nodes at:
# /etc/ansible/facts.d/*.fact (INI or JSON format)
```

```ini
# /etc/ansible/facts.d/app.fact
[general]
app_name=mywebapp
app_version=2.1.0
deploy_date=2024-01-15
```

```yaml
# Access in playbooks as ansible_local
- name: Show custom facts
  debug:
    msg: >
      App: {{ ansible_local.app.general.app_name }}
      Version: {{ ansible_local.app.general.app_version }}
```

---

## Set Fact Module

```yaml
# Create new facts during play execution
- name: Set computed variables
  set_fact:
    full_app_path: "/opt/{{ app_name }}/releases/{{ app_version }}"
    deploy_timestamp: "{{ ansible_date_time.iso8601 }}"
    is_production: "{{ env == 'production' }}"

# Set fact based on conditions
- name: Determine package manager
  set_fact:
    pkg_mgr: "{{ 'apt' if ansible_os_family == 'Debian' else 'yum' }}"

# Set cacheable fact (persists between plays)
- name: Set persistent fact
  set_fact:
    deployment_id: "deploy-{{ ansible_date_time.epoch }}"
    cacheable: yes
```

---

## Conditionals with when

```yaml
tasks:
  # Simple condition
  - name: Install on Debian systems
    apt:
      name: nginx
      state: present
    when: ansible_os_family == "Debian"

  # Multiple conditions (AND)
  - name: Configure production webservers
    template:
      src: nginx-prod.conf.j2
      dest: /etc/nginx/nginx.conf
    when:
      - env == "production"
      - "'webservers' in group_names"

  # OR condition
  - name: Install on Debian or Ubuntu
    apt:
      name: nginx
    when: ansible_distribution == "Debian" or
          ansible_distribution == "Ubuntu"
```

---

## Conditional Examples

```yaml
# Check if variable is defined
- name: Use custom port if defined
  debug:
    msg: "Using port {{ custom_port }}"
  when: custom_port is defined

# Check boolean
- name: Enable debug logging
  template:
    src: debug-config.j2
    dest: /etc/app/debug.conf
  when: debug_mode | bool

# Check string content
- name: Only run on master database
  command: /opt/db/promote.sh
  when: "'master' in db_role"

# Check registered variable
- name: Check if config exists
  stat:
    path: /etc/myapp/config.yml
  register: config_file

- name: Create default config
  template:
    src: default-config.j2
    dest: /etc/myapp/config.yml
  when: not config_file.stat.exists
```

---

## Conditionals with Facts

```yaml
tasks:
  # OS-specific package installation
  - name: Install Apache (Debian)
    apt:
      name: apache2
      state: present
    when: ansible_os_family == "Debian"

  - name: Install Apache (RedHat)
    yum:
      name: httpd
      state: present
    when: ansible_os_family == "RedHat"

  # Memory-based decisions
  - name: Configure large JVM heap
    lineinfile:
      path: /etc/myapp/jvm.conf
      regexp: '^-Xmx'
      line: '-Xmx4g'
    when: ansible_memtotal_mb >= 8192

  - name: Configure small JVM heap
    lineinfile:
      path: /etc/myapp/jvm.conf
      regexp: '^-Xmx'
      line: '-Xmx512m'
    when: ansible_memtotal_mb < 8192
```

---

## Loops with loop

```yaml
# Simple list loop
- name: Install packages
  apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - php-fpm
    - php-mysql

# Better: pass the whole list (more efficient)
- name: Install packages (efficient)
  apt:
    name:
      - nginx
      - php-fpm
      - php-mysql
    state: present

# Loop over a variable
- name: Create users
  user:
    name: "{{ item }}"
    state: present
  loop: "{{ users_list }}"
```

---

## Loops with Dictionaries

```yaml
# Loop over list of dictionaries
- name: Create users with details
  user:
    name: "{{ item.name }}"
    uid: "{{ item.uid }}"
    groups: "{{ item.groups }}"
    shell: "{{ item.shell | default('/bin/bash') }}"
  loop:
    - name: alice
      uid: 1001
      groups: developers
    - name: bob
      uid: 1002
      groups: "developers,sudo"
    - name: charlie
      uid: 1003
      groups: ops
      shell: /bin/zsh
```

---

## Loop with dict2items

```yaml
vars:
  firewall_rules:
    ssh: 22
    http: 80
    https: 443
    app: 8080

tasks:
  - name: Open firewall ports
    ufw:
      rule: allow
      port: "{{ item.value }}"
      proto: tcp
      comment: "{{ item.key }}"
    loop: "{{ firewall_rules | dict2items }}"

  # item.key = 'ssh', 'http', etc.
  # item.value = 22, 80, etc.
```

---

## Loop with Index

```yaml
# Using loop with index_var
- name: Create numbered config files
  copy:
    content: "server_id={{ idx }}"
    dest: "/etc/myapp/node{{ idx }}.conf"
  loop:
    - node-a
    - node-b
    - node-c
  loop_control:
    index_var: idx

# Control loop label in output
- name: Create users (clean output)
  user:
    name: "{{ item.name }}"
    uid: "{{ item.uid }}"
  loop: "{{ users }}"
  loop_control:
    label: "{{ item.name }}"
    # Output shows: "item=alice" instead of full dict
```

---

## Nested Loops

```yaml
# Using subelements
vars:
  users:
    - name: alice
      ssh_keys:
        - "ssh-ed25519 AAAA... alice@laptop"
        - "ssh-ed25519 BBBB... alice@desktop"
    - name: bob
      ssh_keys:
        - "ssh-ed25519 CCCC... bob@laptop"

tasks:
  - name: Add SSH keys for each user
    authorized_key:
      user: "{{ item.0.name }}"
      key: "{{ item.1 }}"
    loop: "{{ users | subelements('ssh_keys') }}"
```

---

## Tags

```yaml
# Assign tags to tasks
- name: Install packages
  apt:
    name: nginx
    state: present
  tags:
    - packages
    - setup

- name: Deploy configuration
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  tags:
    - config

- name: Start service
  service:
    name: nginx
    state: started
  tags:
    - service
    - always  # 'always' tag runs unless explicitly skipped
```

---

## Using Tags

```bash
# Run only tasks with specific tag
ansible-playbook site.yml --tags "config"

# Run tasks with multiple tags
ansible-playbook site.yml --tags "packages,config"

# Skip tasks with specific tag
ansible-playbook site.yml --skip-tags "setup"

# List all tags in a playbook
ansible-playbook site.yml --list-tags

# Special tags:
# 'always' - always runs (unless --skip-tags always)
# 'never'  - never runs (unless --tags never)
```

---

## Tags on Plays and Roles

```yaml
# Tag an entire play
- name: Configure webservers
  hosts: webservers
  tags: webserver
  tasks:
    - name: Install nginx
      apt:
        name: nginx
        state: present
    # All tasks in this play get 'webserver' tag

# Tag a role
- name: Full stack setup
  hosts: all
  roles:
    - role: common
      tags: common
    - role: nginx
      tags: webserver
    - role: postgresql
      tags: database
```

---

## Blocks

```yaml
# Group tasks and apply common attributes
- name: Web server setup
  block:
    - name: Install nginx
      apt:
        name: nginx
        state: present

    - name: Deploy config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf

    - name: Start nginx
      service:
        name: nginx
        state: started
  when: "'webservers' in group_names"
  become: true
  tags: webserver
```

---

## Block Error Handling

```yaml
- name: Deploy with rollback
  block:
    - name: Deploy new version
      git:
        repo: https://github.com/myorg/myapp.git
        dest: /opt/myapp
        version: "{{ new_version }}"

    - name: Run database migrations
      command: /opt/myapp/migrate.sh

    - name: Restart application
      service:
        name: myapp
        state: restarted

  rescue:
    - name: Rollback to previous version
      git:
        repo: https://github.com/myorg/myapp.git
        dest: /opt/myapp
        version: "{{ old_version }}"

    - name: Restart with old version
      service:
        name: myapp
        state: restarted

  always:
    - name: Send deployment notification
      uri:
        url: https://hooks.slack.com/services/XXX
        method: POST
        body: '{"text": "Deployment {{ "succeeded" if not ansible_failed_task is defined else "failed and rolled back" }}"}'
        body_format: json
```

---

## Playbook: Complete Web Application

```yaml
---
- name: Deploy web application
  hosts: webservers
  become: true
  vars:
    app_name: mywebapp
    app_version: "2.1.0"
    app_user: www-data
    app_root: /var/www/mywebapp
    venv_path: "{{ app_root }}/venv"
    repo_url: https://github.com/myorg/mywebapp.git

  tasks:
    - name: Install system dependencies
      apt:
        name:
          - python3
          - python3-venv
          - python3-pip
          - nginx
          - supervisor
        state: present
        update_cache: yes
      tags: packages

    - name: Create application directory
      file:
        path: "{{ app_root }}"
        state: directory
        owner: "{{ app_user }}"
        mode: '0755'
      tags: setup

    - name: Clone application code
      git:
        repo: "{{ repo_url }}"
        dest: "{{ app_root }}/src"
        version: "v{{ app_version }}"
      notify: restart app
      tags: deploy

    - name: Create virtual environment
      pip:
        requirements: "{{ app_root }}/src/requirements.txt"
        virtualenv: "{{ venv_path }}"
        virtualenv_python: python3
      tags: deploy

    - name: Deploy nginx config
      template:
        src: templates/nginx-app.conf.j2
        dest: /etc/nginx/sites-available/{{ app_name }}
      notify: reload nginx
      tags: config

    - name: Enable nginx site
      file:
        src: /etc/nginx/sites-available/{{ app_name }}
        dest: /etc/nginx/sites-enabled/{{ app_name }}
        state: link
      notify: reload nginx
      tags: config

    - name: Deploy supervisor config
      template:
        src: templates/supervisor-app.conf.j2
        dest: /etc/supervisor/conf.d/{{ app_name }}.conf
      notify: restart app
      tags: config

  handlers:
    - name: reload nginx
      service:
        name: nginx
        state: reloaded

    - name: restart app
      supervisorctl:
        name: "{{ app_name }}"
        state: restarted
```

---

## Exercise: Playbook Basics Lab

1. Create a playbook that:
   - Uses variables for package names and paths
   - Installs different packages based on OS family
   - Creates users with a loop
   - Uses handlers for service restarts
   - Has tags for selective execution

2. Use `--check --diff` to preview changes
3. Use `--tags` to run specific parts
4. Use `--limit` to target specific hosts

---

## Playbook Basics Summary

- Variables can come from many sources with clear precedence
- Facts provide rich system information automatically
- `when` conditionals control task execution
- Loops iterate over lists and dictionaries
- Tags allow selective execution of tasks
- Blocks group tasks and enable error handling
- Handlers run only when notified and deduplicate
