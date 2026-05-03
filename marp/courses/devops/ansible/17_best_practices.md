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
# Best Practices and Real-World Patterns

## Topics Covered
- Project structure and organization
- Naming conventions
- Security best practices
- Common design patterns
- Multi-environment management
- Real-world deployment patterns
- Troubleshooting guide
- Course summary

---

## Ansible Best Practices

![Ansible Best Practices](svg/courses/devops/ansible/17_best_practices/ansible_best_practices.svg)

---

## Recommended Project Structure

```tree
ansible-project/
├── ansible.cfg
├── requirements.yml           # Galaxy requirements
├── .ansible-lint             # Linter config
├── .yamllint                 # YAML linter config
├── inventories/
│   ├── production/
│   │   ├── hosts.yml
│   │   ├── group_vars/
│   │   │   ├── all/
│   │   │   │   ├── vars.yml
│   │   │   │   └── vault.yml  # Encrypted
│   │   │   ├── webservers.yml
│   │   │   └── dbservers.yml
│   │   └── host_vars/
│   └── staging/
│       ├── hosts.yml
│       └── group_vars/
├── roles/
│   ├── common/
│   ├── nginx/
│   ├── app/
│   └── postgresql/
├── playbooks/
│   ├── site.yml              # Master playbook
│   ├── deploy.yml
│   ├── rollback.yml
│   └── maintenance.yml
├── plugins/
│   ├── filter/
│   └── callback/
├── library/                   # Custom modules
├── templates/
├── files/
└── scripts/                   # Helper scripts
```

---

## Naming Conventions

```yaml
# Roles: lowercase with underscores
roles/
  nginx_proxy/
  postgresql_primary/
  app_deploy/

# Variables: prefix with role name
# In roles/nginx/defaults/main.yml:
nginx_worker_processes: auto
nginx_listen_port: 80
nginx_ssl_enabled: false

# Vault variables: prefix with vault_
vault_db_password: "encrypted..."
vault_api_key: "encrypted..."

# Tasks: descriptive, start with verb
- name: Install required packages
- name: Deploy nginx configuration
- name: Ensure service is running
- name: Create application user

# Handlers: start with action verb
handlers:
  - name: restart nginx
  - name: reload postgresql
  - name: restart application
```

---

## Playbook Style Guide

```yaml
# DO: Use fully qualified collection names
- name: Install packages
  ansible.builtin.apt:
    name: nginx
    state: present

# DON'T: Use short module names
- name: Install packages
  apt:
    name: nginx

# DO: Always name your tasks
- name: Create application directory
  file:
    path: /opt/myapp
    state: directory

# DON'T: Skip task names
- file:
    path: /opt/myapp
    state: directory

# DO: Use YAML syntax for module args
- name: Install nginx
  apt:
    name: nginx
    state: present

# DON'T: Use key=value syntax
- name: Install nginx
  apt: name=nginx state=present
```

---

## Security Best Practices

```yaml
# 1. Never store secrets in plaintext
# Use Ansible Vault for all secrets
db_password: "{{ vault_db_password }}"

# 2. Use no_log for sensitive tasks
- name: Set database password
  postgresql_user:
    name: appuser
    password: "{{ vault_db_password }}"
  no_log: true

# 3. Limit sudo access
become: true
become_user: appuser  # Not root when possible

# 4. Use SSH keys, never passwords
ansible_ssh_private_key_file: ~/.ssh/ansible_key

# 5. Validate SSL certificates
- uri:
    url: https://api.example.com
    validate_certs: yes  # Don't disable this in production

# 6. Minimize privileged operations
# Only become root when necessary
- name: Read application log (no sudo needed)
  command: cat /var/log/myapp/app.log
  become: false
```

---

## Idempotency Patterns

```yaml
# PATTERN: Use creates/removes for command idempotency
- name: Initialize database (only if not already done)
  command: /opt/myapp/init-db.sh
  args:
    creates: /opt/myapp/.db_initialized

# PATTERN: Use stat to check before acting
- name: Check if app is deployed
  stat:
    path: /opt/myapp/current
  register: app_deployed

- name: Deploy application
  git:
    repo: "{{ app_repo }}"
    dest: /opt/myapp/current
  when: not app_deployed.stat.exists

# PATTERN: changed_when for shell commands
- name: Run migration
  command: python manage.py migrate --check
  register: migration_check
  changed_when: "'No migrations' not in migration_check.stdout"
  failed_when: migration_check.rc > 1
```

---

## Multi-Environment Pattern

```yaml
# Use the same playbooks, different inventories
# inventories/production/group_vars/all/vars.yml
env: production
app_replicas: 3
db_replicas: 2
log_level: warn
debug_mode: false
monitoring_enabled: true
backup_retention_days: 30

# inventories/staging/group_vars/all/vars.yml
env: staging
app_replicas: 1
db_replicas: 1
log_level: info
debug_mode: true
monitoring_enabled: true
backup_retention_days: 7

# inventories/development/group_vars/all/vars.yml
env: development
app_replicas: 1
db_replicas: 0
log_level: debug
debug_mode: true
monitoring_enabled: false
backup_retention_days: 1
```

```bash
# Deploy to specific environment
ansible-playbook -i inventories/staging playbooks/deploy.yml
ansible-playbook -i inventories/production playbooks/deploy.yml
```

---

## Rolling Deployment Pattern

```yaml
# playbooks/rolling_deploy.yml

---
- name: Rolling deployment
  hosts: webservers
  become: true
  serial: "25%"
  max_fail_percentage: 10
  any_errors_fatal: false

  pre_tasks:
    - name: Disable in load balancer
      command: /opt/lb/disable {{ inventory_hostname }}
      delegate_to: "{{ groups['loadbalancers'][0] }}"

    - name: Wait for connections to drain
      wait_for:
        timeout: 15

  tasks:
    - name: Stop application
      service:
        name: myapp
        state: stopped

    - name: Deploy new version
      unarchive:
        src: "https://releases.example.com/myapp-{{ app_version }}.tar.gz"
        dest: /opt/myapp/
        remote_src: yes

    - name: Run post-deploy scripts
      command: /opt/myapp/post-deploy.sh

    - name: Start application
      service:
        name: myapp
        state: started
```

---

## Rolling Deployment: Post Tasks

```yaml
  post_tasks:
    - name: Health check
      uri:
        url: "http://localhost:{{ app_port }}/health"
      register: health
      until: health.status == 200
      retries: 30
      delay: 5

    - name: Enable in load balancer
      command: /opt/lb/enable {{ inventory_hostname }}
      delegate_to: "{{ groups['loadbalancers'][0] }}"
```

---

## Rollback Pattern

```yaml
# playbooks/rollback.yml

---
- name: Rollback deployment
  hosts: webservers
  become: true
  serial: "50%"
  vars:
    releases_dir: /opt/myapp/releases
    current_link: /opt/myapp/current

  tasks:
    - name: Get list of releases
      find:
        paths: "{{ releases_dir }}"
        file_type: directory
      register: releases

    - name: Sort releases by date
      set_fact:
        sorted_releases: "{{ releases.files | sort(attribute='mtime', reverse=true) }}"

    - name: Identify previous release
      set_fact:
        previous_release: "{{ sorted_releases[1].path }}"
      when: sorted_releases | length > 1

    - name: Switch symlink to previous release
      file:
        src: "{{ previous_release }}"
        dest: "{{ current_link }}"
        state: link
      when: previous_release is defined

    - name: Restart application
      service:
        name: myapp
        state: restarted

    - name: Verify health
      uri:
        url: http://localhost:8080/health
      register: health
      until: health.status == 200
      retries: 30
      delay: 5
```

---

## Zero-Downtime Deployment

```yaml
# Symlink-based deployment with releases directory
vars:
  app_root: /opt/myapp
  releases_dir: "{{ app_root }}/releases"
  shared_dir: "{{ app_root }}/shared"
  current_release: "{{ releases_dir }}/{{ app_version }}"

tasks:
  - name: Create release directory
    file:
      path: "{{ current_release }}"
      state: directory

  - name: Deploy application code
    unarchive:
      src: "https://artifacts.example.com/myapp-{{ app_version }}.tar.gz"
      dest: "{{ current_release }}"
      remote_src: yes

  - name: Link shared files
    file:
      src: "{{ shared_dir }}/{{ item }}"
      dest: "{{ current_release }}/{{ item }}"
      state: link
    loop:
      - config/database.yml
      - config/secrets.yml
      - log
      - tmp
```

---

## Zero-Downtime: Switch and Cleanup

```yaml
  - name: Switch current symlink
    file:
      src: "{{ current_release }}"
      dest: "{{ app_root }}/current"
      state: link
    notify: restart app

  - name: Clean old releases (keep last 5)
    shell: |
      ls -dt {{ releases_dir }}/*/ | tail -n +6 | xargs rm -rf
    changed_when: false
```

---

## Database Migration Pattern

```yaml
# playbooks/db_migrate.yml

---
- name: Database migration
  hosts: dbservers[0]    # Only run on primary DB
  become: true
  become_user: postgres

  tasks:
    - name: Backup database before migration
      postgresql_db:
        name: "{{ db_name }}"
        state: dump
        target: "/backups/pre-migration-{{ ansible_date_time.epoch }}.sql"

    - name: Run migrations
      command: >
        {{ app_root }}/venv/bin/python
        {{ app_root }}/manage.py migrate
        --no-input
      register: migration_result
      changed_when: "'Applying' in migration_result.stdout"

    - name: Display migration results
      debug:
        msg: "{{ migration_result.stdout_lines }}"

    - name: Verify database connectivity
      postgresql_query:
        db: "{{ db_name }}"
        query: "SELECT 1"
      register: db_check

    - name: Assert database is healthy
      assert:
        that: db_check.rowcount == 1
        fail_msg: "Database health check failed after migration"
```

---

## Configuration Drift Detection

```yaml
# playbooks/drift_check.yml

---
- name: Detect configuration drift
  hosts: all
  become: true
  gather_facts: true

  tasks:
    - name: Run configuration in check mode
      include_role:
        name: "{{ item }}"
      loop: "{{ group_names | map('regex_replace', '^', '') | list }}"
      check_mode: true
      register: drift_results

    - name: Report drift
      debug:
        msg: "DRIFT DETECTED on {{ inventory_hostname }}"
      when: drift_results is changed

    - name: Send drift report
      uri:
        url: "{{ monitoring_webhook }}"
        method: POST
        body:
          host: "{{ inventory_hostname }}"
          drift_detected: "{{ drift_results is changed }}"
          timestamp: "{{ ansible_date_time.iso8601 }}"
        body_format: json
      delegate_to: localhost
      when: drift_results is changed
```

---

## Compliance Checking Pattern

```yaml
# playbooks/compliance.yml

---
- name: Security compliance checks
  hosts: all
  become: true

  tasks:
    - name: Check SSH configuration
      block:
        - name: Verify PasswordAuthentication is disabled
          command: grep "^PasswordAuthentication no" /etc/ssh/sshd_config
          changed_when: false

        - name: Verify root login is disabled
          command: grep "^PermitRootLogin no" /etc/ssh/sshd_config
          changed_when: false

        - name: Verify SSH protocol 2
          command: grep "^Protocol 2" /etc/ssh/sshd_config
          changed_when: false
      rescue:
        - name: Report SSH non-compliance
          set_fact:
            compliance_failures: "{{ compliance_failures | default([]) + ['SSH configuration'] }}"

    - name: Check firewall is active
      command: ufw status
      register: fw_status
      changed_when: false
      failed_when: "'inactive' in fw_status.stdout"

    - name: Check unattended upgrades
      stat:
        path: /etc/apt/apt.conf.d/20auto-upgrades
      register: auto_upgrades

    - name: Report compliance status
      debug:
        msg: |
          Compliance Report for {{ inventory_hostname }}:
          - SSH hardened: {{ 'PASS' if compliance_failures is not defined else 'FAIL' }}
          - Firewall active: {{ 'PASS' if fw_status.rc == 0 else 'FAIL' }}
          - Auto-updates: {{ 'PASS' if auto_upgrades.stat.exists else 'FAIL' }}
```

---

## Patching Pattern

```yaml
# playbooks/patch.yml

---
- name: System patching
  hosts: all
  become: true
  serial: "20%"
  max_fail_percentage: 5

  pre_tasks:
    - name: Create pre-patch snapshot
      command: /opt/scripts/create-snapshot.sh
      delegate_to: localhost

  tasks:
    - name: Update all packages
      apt:
        upgrade: safe
        update_cache: yes
        cache_valid_time: 3600
      register: update_result

    - name: Check if reboot is required
      stat:
        path: /var/run/reboot-required
      register: reboot_required

    - name: Reboot if required
      reboot:
        reboot_timeout: 300
        msg: "Reboot initiated by Ansible patching"
      when: reboot_required.stat.exists
```

---

## Patching Pattern: Verification

```yaml
  tasks:
    - name: Verify services after reboot
      service_facts:

    - name: Assert critical services are running
      assert:
        that:
          - "'nginx.service' in ansible_facts.services"
          - "ansible_facts.services['nginx.service'].state == 'running'"
        fail_msg: "Critical service not running after patch"

  post_tasks:
    - name: Send patch report
      debug:
        msg: |
          Patching complete on {{ inventory_hostname }}
          Packages updated: {{ update_result.stdout_lines | default([]) | length }}
          Reboot required: {{ reboot_required.stat.exists }}
```

---

## Troubleshooting Guide

```misc
Problem: "Permission denied"
  - Check become: true
  - Check ansible_user has sudo access
  - Check SSH key permissions (600)

Problem: "Host unreachable"
  - ansible -m ping hostname
  - Check SSH connectivity manually
  - Check firewall rules
  - Verify ansible_host in inventory

Problem: "Module not found"
  - ansible-doc -l | grep module_name
  - Install required collection
  - Check ANSIBLE_LIBRARY path

Problem: "Variable undefined"
  - Use debug module to inspect vars
  - Check variable precedence
  - Verify file is being loaded
  - Use default() filter

Problem: "Task always shows changed"
  - Add changed_when: false
  - Use specific modules instead of command/shell
  - Check module documentation for idempotency

Problem: "Slow execution"
  - Enable pipelining
  - Increase forks
  - Enable fact caching
  - Use profile_tasks callback
```

---

## Common Mistakes to Avoid

```yaml
# MISTAKE 1: Using shell when a module exists
# Bad:
- shell: apt-get install -y nginx
# Good:
- apt:
    name: nginx
    state: present

# MISTAKE 2: Not quoting Jinja2 expressions at start of value
# Bad:
- debug:
    msg: {{ my_var }}
# Good:
- debug:
    msg: "{{ my_var }}"

# MISTAKE 3: Using {{ }} in when clauses
# Bad:
  when: "{{ my_var }} == true"
# Good:
  when: my_var == true

# MISTAKE 4: Hardcoding values
# Bad:
- apt:
    name: nginx=1.18.0
# Good:
- apt:
    name: "nginx={{ nginx_version }}"
```

---

## Additional Common Mistakes

```yaml
# MISTAKE 5: Not using handlers for service restarts
# Bad:
- template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
- service:
    name: nginx
    state: restarted  # Restarts EVERY run

# Good:
- template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx

# MISTAKE 6: Ignoring return codes
# Bad:
- command: /opt/app/check.sh
  ignore_errors: yes
# Good:
- command: /opt/app/check.sh
  register: check_result
  failed_when: check_result.rc > 1

# MISTAKE 7: Not using block for error handling
# Bad: Multiple ignore_errors tasks
# Good: block/rescue/always pattern
```

---

## Ansible Ecosystem Tools

| Tool | Purpose |
|------|---------|
| `ansible-playbook` | Execute playbooks |
| `ansible-galaxy` | Install roles and collections |
| `ansible-vault` | Encrypt/decrypt secrets |
| `ansible-doc` | Module documentation |
| `ansible-lint` | Playbook linting |
| `ansible-navigator` | TUI for `Ansible` content |
| `ansible-builder` | Build execution environments |
| `molecule` | Role testing framework |
| `ansible-pull` | Pull-mode execution |
| `ansible-inventory` | Inventory inspection |
| `ansible-console` | Interactive REPL |
| `ansible-config` | Configuration inspection |

---

## Further Learning Resources

- **Documentation**: docs.ansible.com
- **Galaxy**: galaxy.ansible.com
- **GitHub**: github.com/ansible/ansible
- **Community**: forum.ansible.com
- **Certifications**: Red Hat Certified Specialist in Ansible
- **Books**: "Ansible for DevOps" by Jeff Geerling
- **YouTube**: Jeff Geerling's Ansible 101 series
- **Practice**: Set up a home lab with VMs or containers

---

## Day 3 Summary

- Dynamic inventory discovers hosts from cloud APIs
- Custom modules extend `Ansible` for proprietary systems
- Tower/AWX adds enterprise features: RBAC, workflows, API
- Performance tuning: forks, pipelining, caching, async
- `Molecule` provides a full testing framework for roles
- CI/CD integration enables automated testing and deployment
- Follow best practices for maintainable, secure automation

---

## Course Summary

**Day 1**: Fundamentals
- `Ansible` architecture and agentless design
- Installation, configuration, `SSH` setup
- Inventory management (static, groups, variables)
- Ad-hoc commands and common modules
- Playbook basics: plays, tasks, handlers

**Day 2**: Playbooks, Roles, and Advanced Features
- Variables, facts, and `Jinja2` templating
- Conditionals, loops, and filters
- Roles: structure, creation, `Galaxy`
- Error handling and debugging
- `Ansible Vault` for secrets management
- Tags, includes, and imports

**Day 3**: Advanced Ansible and Real-World Patterns
- Dynamic inventory (AWS, Azure, GCP)
- Custom modules and plugins
- Tower/AWX overview
- Performance tuning
- Testing with `Molecule`
- CI/CD integration
- Best practices and deployment patterns

---

## Final Exercise: Capstone Project

Build a complete `Ansible` project that:

1. **Structure**: Proper directory layout with roles
1. **Inventory**: Multi-environment (staging + production)
1. **Roles**: Create 3+ roles (common, web, database)
1. **Vault**: Encrypt all secrets
1. **Templates**: Use `Jinja2` for dynamic configuration
1. **Testing**: `Molecule` tests for at least one role
1. **CI/CD**: GitHub Actions workflow for linting + testing
1. **Deployment**: Rolling update with health checks
1. **Rollback**: Automated rollback on failure
1. **Documentation**: Variables and usage documented

---

## Thank You

- Questions and discussion
- Feedback welcome
- Continue practicing with your lab environment
- Join the `Ansible` community forums
- Consider Red Hat Ansible certification

---

## Code Organization

![code_organization](svg/courses/devops/ansible/17_best_practices/code_organization.svg)

---

## Idempotence Principles

![idempotence_principles](svg/courses/devops/ansible/17_best_practices/idempotence_principles.svg)
