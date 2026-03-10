# Error Handling and Debugging

## Topics Covered
- Error handling strategies
- `ignore_errors` and `failed_when`
- Block/rescue/always patterns
- Debugging techniques
- Verbose mode and logging
- `ansible-lint` and best practices

---

## Default Error Behavior

- By default, `Ansible` stops executing on a host when a task fails
- Other hosts continue execution
- Remaining tasks on the failed host are skipped
- Play recap shows failed count

```text
PLAY RECAP *****************************
web01  : ok=3  changed=1  unreachable=0  failed=1
web02  : ok=5  changed=2  unreachable=0  failed=0
```

---

## ignore_errors

```yaml
# Continue even if a task fails
- name: Check if optional service exists
  command: systemctl status myoptional-service
  register: service_check
  ignore_errors: yes

- name: Configure service if it exists
  template:
    src: optional-service.conf.j2
    dest: /etc/optional-service/config.yml
  when: service_check.rc == 0

# ignore_unreachable: continue if host is unreachable
- name: Check if host responds
  ping:
  ignore_unreachable: yes
  register: ping_result

- name: Skip unreachable hosts
  debug:
    msg: "Host is reachable"
  when: ping_result is not unreachable
```

---

## failed_when

```yaml
# Custom failure conditions
- name: Run database migration
  command: /opt/myapp/migrate.sh
  register: migration_result
  failed_when:
    - migration_result.rc != 0
    - "'already up to date' not in migration_result.stdout"

# Fail only on specific output
- name: Check application status
  command: /opt/myapp/healthcheck.sh
  register: health
  failed_when: "'CRITICAL' in health.stdout"

# Multiple failure conditions
- name: Validate configuration
  command: /opt/myapp/validate-config.sh
  register: validation
  failed_when:
    - validation.rc != 0
    - validation.rc != 2  # rc=2 means warnings only
```

---

## any_errors_fatal

```yaml
# Stop ALL hosts if ANY host fails
- name: Database migration (must succeed everywhere)
  hosts: dbservers
  any_errors_fatal: true
  tasks:
    - name: Run schema migration
      command: /opt/db/migrate.sh
      # If this fails on ANY db server,
      # execution stops on ALL hosts

# Per-task equivalent
- name: Critical configuration step
  command: /opt/critical-setup.sh
  any_errors_fatal: true
```

---

## max_fail_percentage

```yaml
# Allow some hosts to fail before aborting
- name: Rolling update with failure threshold
  hosts: webservers
  serial: 5
  max_fail_percentage: 20  # Stop if >20% of batch fails

  tasks:
    - name: Deploy new version
      git:
        repo: https://github.com/myorg/myapp.git
        dest: /opt/myapp
        version: "{{ new_version }}"

    - name: Restart application
      service:
        name: myapp
        state: restarted

    - name: Verify health
      uri:
        url: http://localhost:8080/health
      register: health
      until: health.status == 200
      retries: 10
      delay: 5
```

---

## Block/Rescue/Always Pattern

```yaml
- name: Deployment with error recovery
  block:
    - name: Pull new code
      git:
        repo: https://github.com/myorg/myapp.git
        dest: /opt/myapp
        version: "v{{ new_version }}"

    - name: Install dependencies
      pip:
        requirements: /opt/myapp/requirements.txt
        virtualenv: /opt/myapp/venv

    - name: Run migrations
      command: /opt/myapp/venv/bin/python manage.py migrate

    - name: Restart application
      service:
        name: myapp
        state: restarted

  rescue:
    - name: Log failure
      debug:
        msg: "Deployment failed: {{ ansible_failed_task.name }}"

    - name: Rollback to previous version
      git:
        repo: https://github.com/myorg/myapp.git
        dest: /opt/myapp
        version: "v{{ current_version }}"

    - name: Restart with old version
      service:
        name: myapp
        state: restarted

  always:
    - name: Ensure app is running
      service:
        name: myapp
        state: started

    - name: Send notification
      uri:
        url: "{{ slack_webhook }}"
        method: POST
        body: |
          {"text": "Deploy {{ new_version }} on {{ inventory_hostname }}: {{ 'FAILED - rolled back' if ansible_failed_task is defined else 'SUCCESS' }}"}
        body_format: json
```

---

## Fail Module

```yaml
# Explicitly fail with a message
- name: Check disk space
  command: df -h /opt
  register: disk_check
  changed_when: false

- name: Fail if disk space is low
  fail:
    msg: "Insufficient disk space on {{ inventory_hostname }}. Need at least 5GB free."
  when: disk_check.stdout | regex_search('(\d+)%') | int > 90

# Fail with assert
- name: Validate required variables
  assert:
    that:
      - app_version is defined
      - app_version | length > 0
      - db_password is defined
      - db_password | length >= 12
    fail_msg: "Required variables are missing or invalid"
    success_msg: "All required variables are set"
```

---

## Debugging with debug Module

```yaml
# Print a variable
- name: Show variable value
  debug:
    var: my_variable

# Print a formatted message
- name: Show deployment info
  debug:
    msg: |
      Deploying to: {{ inventory_hostname }}
      Version: {{ app_version }}
      Environment: {{ env }}
      OS: {{ ansible_distribution }} {{ ansible_distribution_version }}

# Conditional debug (only show with -vv)
- name: Detailed debug info
  debug:
    msg: "Full facts: {{ ansible_facts }}"
    verbosity: 2
```

---

## Debugging with Verbose Mode

```bash
# Increasing verbosity levels
ansible-playbook site.yml -v      # Task results
ansible-playbook site.yml -vv     # Task input + results
ansible-playbook site.yml -vvv    # Connection debugging
ansible-playbook site.yml -vvvv   # Full connection + plugin debug

# Environment variable
ANSIBLE_VERBOSITY=3 ansible-playbook site.yml

# In ansible.cfg
[defaults]
verbosity = 1
```

---

## The Debugger

```yaml
# Enable the task debugger
- name: Task with debugger
  command: /opt/myapp/setup.sh
  debugger: on_failed

# Debugger options:
# always    - always enter debugger
# never     - never enter debugger
# on_failed - enter on failure
# on_unreachable - enter when host is unreachable
# on_skipped - enter when task is skipped

# In the debugger you can:
# p task        - print task info
# p task.args   - print task arguments
# p result      - print task result
# p vars        - print all variables
# redo          - re-run the task
# continue      - continue execution
# quit          - abort execution
```

---

## Debugging Strategy

```yaml
# Enable debugger for entire play
- name: Debug play
  hosts: webservers
  strategy: debug   # Enter debugger on ANY failure
  tasks:
    - name: This will pause on failure
      command: /opt/failing-script.sh

# Or set in ansible.cfg
# [defaults]
# enable_task_debugger = true
```

---

## Ansible Logging

```ini
# ansible.cfg
[defaults]
# Log all output to a file
log_path = /var/log/ansible/ansible.log

# Use callback plugin for structured logging
stdout_callback = yaml      # Human-readable YAML output
# stdout_callback = json    # Machine-readable JSON output
# stdout_callback = debug   # Show stderr and stdout separately
```

```bash
# Log to a specific file per run
ANSIBLE_LOG_PATH=/tmp/ansible-$(date +%Y%m%d).log \
    ansible-playbook site.yml

# Use no_log to hide sensitive data
- name: Set database password
  postgresql_user:
    name: appuser
    password: "{{ vault_db_password }}"
  no_log: true
```

---

## Callback Plugins for Debugging

```ini
# ansible.cfg
[defaults]
# Timer plugin - shows execution time per task
callback_whitelist = timer, profile_tasks, profile_roles

# profile_tasks: shows time taken per task
# profile_roles: shows time taken per role
# timer: shows total execution time
```

```bash
# Output with profile_tasks:
# TASK [Install nginx] ***********************
# ok: [web01]
# --- 2.45s
#
# TASK [Deploy config] ***********************
# changed: [web01]
# --- 0.82s
#
# PLAY RECAP Total: 12.34s
```

---

## ansible-lint

```bash
# Install ansible-lint
pip install ansible-lint

# Run linter on a playbook
ansible-lint site.yml

# Run on an entire directory
ansible-lint playbooks/

# Common rules it checks:
# - YAML syntax
# - Deprecated modules
# - Task naming conventions
# - Use of command/shell instead of proper modules
# - Missing become for privilege operations
# - Jinja2 spacing
```

---

## ansible-lint Configuration

```yaml
# .ansible-lint
---
exclude_paths:
  - .cache/
  - .github/
  - tests/

skip_list:
  - yaml[line-length]
  - name[casing]

warn_list:
  - experimental

enable_list:
  - no-changed-when
  - no-handler

# Enforce specific rules
use_default_rules: true
```

---

## Common ansible-lint Rules

| Rule | Description |
|------|-------------|
| `yaml[truthy]` | Use `true`/`false` not `yes`/`no` |
| `name[missing]` | All tasks should have names |
| `command-instead-of-module` | Use specific module instead of `command` |
| `no-changed-when` | Commands should have `changed_when` |
| `risky-shell-pipe` | Shell piped commands may hide errors |
| `no-jinja-when` | Don't use `{{ }}` in `when` |
| `role-name` | Role names should be lowercase |
| `fqcn[action-core]` | Use fully qualified collection names |

---

## Syntax Checking

```bash
# Check playbook syntax (no execution)
ansible-playbook --syntax-check site.yml

# Check with YAML linting
yamllint site.yml

# yamllint configuration
# .yamllint
---
extends: default
rules:
  line-length:
    max: 120
  truthy:
    allowed-values: ['true', 'false', 'yes', 'no']
  indentation:
    spaces: 2
  comments:
    min-spaces-from-content: 1
```

---

## Debugging Strategies Summary

```text
Problem                          Tool
-------                          ----
Playbook doesn't parse      -->  --syntax-check
Task produces wrong result  -->  -v / debug module
Variable has wrong value    -->  debug var= / -vv
SSH connection fails        -->  -vvvv
Module not found            -->  ansible-doc -l
Host unreachable            -->  ansible -m ping
Slow execution              -->  profile_tasks callback
Code quality issues         -->  ansible-lint
YAML syntax errors          -->  yamllint
Conditional logic wrong     -->  debug + when tracing
Template rendering wrong    -->  template to /tmp first
```

---

## Exercise: Error Handling Lab

1. Create a playbook with `block/rescue/always` that:
   - Attempts to deploy an application
   - Rolls back on failure
   - Always sends a notification

2. Add `assert` tasks to validate prerequisites
3. Use `failed_when` for custom failure conditions
4. Run `ansible-lint` on your playbooks and fix issues
5. Use `--check --diff -v` to debug
