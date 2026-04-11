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
# Performance Tuning

## Topics Covered
- Measuring playbook performance
- Parallelism with `forks`
- `SSH` pipelining
- Async tasks
- Fact caching
- Strategy plugins
- Mitogen and other accelerators

---

## Why Performance Matters

- Large inventories: 100s or 1000s of hosts
- Complex playbooks: many tasks per host
- Time-sensitive operations: deployments, patching
- Default settings are conservative (5 forks)
- Significant speed improvements are possible with tuning

---

## Measuring Performance

```ini
# ansible.cfg - Enable profiling
[defaults]
callback_whitelist = timer, profile_tasks, profile_roles
```

```bash
# Output with profile_tasks:
# Wednesday 15 January 2024  10:30:00 +0000
#
# TASK [Install packages] ****************************
# ok: [web01] --- 4.52s
# ok: [web02] --- 4.31s
#
# TASK [Deploy config] *******************************
# changed: [web01] --- 0.82s
# changed: [web02] --- 0.79s
#
# PLAY RECAP *****************************************
# Playbook run took 0 days, 0 hours, 2 minutes, 15 seconds
```

---
## Forks: Parallelism Control

```ini
# ansible.cfg
[defaults]
forks = 20   # Default is 5
```
```bash
# Override per run
ansible-playbook site.yml -f 50
# Rule of thumb:
# forks = number of target hosts (up to ~50)
# More forks = more RAM on control node
# Each fork is a separate Python process
# ~100MB per fork (varies with modules)
```

---
## Forks: Parallelism Control

![100mb_per_fork_varies_with_modules](svg/courses/devops/ansible/14_performance_tuning/100mb_per_fork_varies_with_modules.svg)

---

## SSH Pipelining

```ini
# ansible.cfg
[ssh_connection]
pipelining = true
```

- Default: `Ansible` copies module to temp dir, then executes
- With pipelining: Module is piped over `SSH` directly
- Eliminates one `SSH` round-trip per task
- **Requirement**: `requiretty` must be disabled in `sudoers`

```bash
# On managed nodes, ensure this is NOT in /etc/sudoers:
# Defaults requiretty

# Add this instead:
# Defaults !requiretty
```

---

## SSH Connection Multiplexing

```ini
# ansible.cfg
[ssh_connection]
ssh_args = -o ControlMaster=auto -o ControlPersist=60s -o PreferAuths=publickey
control_path_dir = ~/.ansible/cp
control_path = %(directory)s/%%h-%%r
```

- `ControlMaster`: Reuse `SSH` connections
- `ControlPersist`: Keep connection alive for 60 seconds
- Avoids `SSH` handshake for each task
- Significant improvement for many tasks per host

---

## SSH Connection Tuning Summary

```ini
# ansible.cfg - Optimized SSH settings
[ssh_connection]
# Enable pipelining (reduces SSH round trips)
pipelining = true

# Connection multiplexing
ssh_args = -o ControlMaster=auto -o ControlPersist=120s -o PreferAuths=publickey

# Control path
control_path_dir = ~/.ansible/cp
control_path = %(directory)s/%%h-%%r

# Transfer method
transfer_method = piped    # Faster than sftp for small files

# Retries
retries = 3
```

---

## Async Tasks

```yaml
# Run tasks asynchronously (don't wait for completion)
- name: Long-running update
  apt:
    upgrade: dist
  async: 3600     # Maximum runtime in seconds
  poll: 0         # Don't wait (fire and forget)
  register: update_task

# Do other work while waiting...
- name: Do something else
  debug:
    msg: "This runs immediately"

# Then check on the async task
- name: Wait for update to complete
  async_status:
    jid: "{{ update_task.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 60
  delay: 30
```

---

## Async: Parallel Operations

```yaml
# Start multiple async tasks in parallel
- name: Run health checks on all services
  uri:
    url: "http://localhost:{{ item.port }}/health"
  async: 60
  poll: 0
  register: health_checks
  loop:
    - { name: web, port: 80 }
    - { name: api, port: 8080 }
    - { name: admin, port: 8443 }

# Wait for all to complete
- name: Wait for health checks
  async_status:
    jid: "{{ item.ansible_job_id }}"
  register: job_results
  until: job_results.finished
  retries: 30
  delay: 2
  loop: "{{ health_checks.results }}"
```

---

## Fact Caching

```ini
# ansible.cfg
[defaults]
gathering = smart           # Only gather if not cached
fact_caching = jsonfile      # Or redis, memcached
fact_caching_connection = /tmp/ansible_facts_cache
fact_caching_timeout = 86400  # 24 hours in seconds
```

```ini
# Using Redis for fact caching
[defaults]
gathering = smart
fact_caching = redis
fact_caching_connection = localhost:6379:0
fact_caching_timeout = 86400
fact_caching_prefix = ansible_facts_
```

- `smart`: Gather facts only if not in cache
- `implicit`: Always gather (default)
- `explicit`: Never gather unless `gather_facts: true`

---

## Disable Fact Gathering

```yaml
# Disable per play when facts aren't needed
- name: Quick task that doesn't need facts
  hosts: webservers
  gather_facts: false

  tasks:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted

# This saves 2-5 seconds per host
```

---

## Strategy Plugins

```yaml
# Default: linear (all hosts run task 1, then task 2, etc.)
- name: Standard execution
  hosts: webservers
  strategy: linear    # Default
  tasks:
    - name: Task 1    # All hosts run this
    - name: Task 2    # Then all hosts run this

# Free strategy: each host runs as fast as it can
- name: Independent execution
  hosts: webservers
  strategy: free       # Each host runs independently
  tasks:
    - name: Task 1    # Each host moves to task 2 immediately
    - name: Task 2    # without waiting for others
```

---

## Serial: Rolling Updates

```yaml
# Update hosts in batches
- name: Rolling update
  hosts: webservers
  serial: 3           # Process 3 hosts at a time
  tasks:
    - name: Deploy new version
      git:
        repo: https://github.com/myorg/myapp.git
        dest: /opt/myapp
        version: "{{ new_version }}"

    - name: Restart app
      service:
        name: myapp
        state: restarted

# Progressive serial
- name: Canary deployment
  hosts: webservers
  serial:
    - 1     # First, deploy to 1 host
    - 5     # Then 5 hosts
    - "25%" # Then 25% of remaining
  tasks:
    - name: Deploy and verify
      # ...
```

---

## Batch Processing with serial

```yaml
# Percentage-based batching
- name: Gradual rollout
  hosts: webservers
  serial: "20%"        # 20% at a time
  max_fail_percentage: 10

  pre_tasks:
    - name: Remove from load balancer
      command: /opt/lb/remove.sh {{ inventory_hostname }}
      delegate_to: loadbalancer

  tasks:
    - name: Deploy new version
      # ...

  post_tasks:
    - name: Add back to load balancer
      command: /opt/lb/add.sh {{ inventory_hostname }}
      delegate_to: loadbalancer

    - name: Wait for health check
      uri:
        url: "http://{{ inventory_hostname }}:8080/health"
      delegate_to: localhost
      register: health
      until: health.status == 200
      retries: 30
      delay: 5
```

---

## Delegation

```yaml
# Run a task on a different host
- name: Remove from load balancer before updating
  command: /opt/lb/remove-backend.sh {{ inventory_hostname }}
  delegate_to: loadbalancer

# Run locally on control node
- name: Update DNS record
  route53:
    zone: example.com
    record: "{{ inventory_hostname }}.example.com"
    type: A
    value: "{{ ansible_host }}"
  delegate_to: localhost

# Delegate facts
- name: Get load balancer info
  setup:
  delegate_to: loadbalancer
  delegate_facts: true
  # Facts are stored on loadbalancer, not current host
```

---

## run_once

```yaml
# Run a task only once, regardless of number of hosts
- name: Run database migration (only once)
  command: /opt/myapp/migrate.sh
  run_once: true
  delegate_to: "{{ groups['dbservers'][0] }}"

# Run once is useful for:
# - Database migrations
# - Sending notifications
# - Creating shared resources
# - Registering DNS records

- name: Send deployment notification
  uri:
    url: "{{ slack_webhook }}"
    method: POST
    body: '{"text": "Deployment starting for {{ ansible_play_hosts | length }} hosts"}'
    body_format: json
  run_once: true
  delegate_to: localhost
```

---

## Mitogen for Ansible

```ini
# Install mitogen
pip install mitogen

# ansible.cfg
[defaults]
strategy_plugins = /path/to/mitogen/ansible_mitogen/plugins/strategy
strategy = mitogen_linear
```

- Replaces `SSH` + temporary files with persistent `Python` interpreter
- 1.25x to 7x faster than vanilla `Ansible`
- No changes to playbooks needed
- Reduces network overhead dramatically
- May not support all modules/features

---

## Performance Tuning Checklist

```misc
1. [ ] Increase forks (20-50)
2. [ ] Enable SSH pipelining
3. [ ] Enable SSH multiplexing (ControlMaster)
4. [ ] Use fact caching (smart gathering)
5. [ ] Disable fact gathering when not needed
6. [ ] Use 'free' strategy for independent tasks
7. [ ] Use async for long-running tasks
8. [ ] Use serial for rolling updates
9. [ ] Profile with profile_tasks callback
10.[ ] Consider Mitogen for large fleets
11.[ ] Use package lists instead of loops
12.[ ] Minimize use of command/shell modules
```

---

## Performance Comparison

```output
Configuration                     Time for 100 hosts
---------------------------------------------------
Default (5 forks, no pipelining)  ~30 minutes
20 forks                          ~8 minutes
20 forks + pipelining             ~5 minutes
20 forks + pipelining + caching   ~3 minutes
Mitogen + 20 forks                ~2 minutes
50 forks + Mitogen + caching      ~1 minute
```

(Results vary based on task complexity, network latency, etc.)

---

## Exercise: Performance Lab

1. Enable `profile_tasks` and baseline a playbook
1. Increase forks and measure improvement
1. Enable `SSH` pipelining and compare
1. Set up fact caching with `jsonfile`
1. Use `async` for a long-running task
1. Implement a rolling update with `serial`
1. Compare `linear` vs `free` strategy
