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
# Conditionals and Loops

## Topics Covered
- Advanced conditional patterns
- Complex loop constructs
- Combining conditions and loops
- Loop filtering and transformations
- Performance considerations

---

## Loops and Conditionals in Ansible

![Loops and Conditionals in Ansible](svg/courses/devops/ansible/06_conditionals_and_loops/loops_and_conditionals.svg)

---

## Conditional Operators

```yaml
# Comparison operators
when: ansible_memtotal_mb >= 4096
when: app_version != "1.0.0"
when: users | length > 0

# String tests
when: ansible_distribution == "Ubuntu"
when: "'webservers' in group_names"
when: server_role is match("web.*")
when: hostname is search("prod")

# Variable tests
when: custom_config is defined
when: optional_feature is undefined
when: backup_enabled is truthy
when: debug_mode is falsy

# Type tests
when: my_var is string
when: my_var is number
when: my_var is mapping   # dict
when: my_var is iterable
```

---

## Complex Conditionals

```yaml
tasks:
  # AND (all conditions must be true)
  - name: Production webserver only
    template:
      src: prod-nginx.conf.j2
      dest: /etc/nginx/nginx.conf
    when:
      - env == "production"
      - "'webservers' in group_names"
      - ansible_memtotal_mb >= 4096

  # OR
  - name: Install on Debian-based systems
    apt:
      name: nginx
    when: ansible_distribution == "Ubuntu" or
          ansible_distribution == "Debian"

  # NOT
  - name: Skip on test environments
    service:
      name: monitoring-agent
      state: started
    when: env != "test" and env != "development"

  # Combined
  - name: Complex condition
    debug:
      msg: "Running special config"
    when: >
      (env == "production" and region == "us-east") or
      (env == "staging" and force_update | default(false))
```

---

## Conditional with Registered Variables

```yaml
tasks:
  - name: Check if application is installed
    stat:
      path: /opt/myapp/bin/myapp
    register: app_binary

  - name: Install application
    command: /opt/installer/install.sh
    when: not app_binary.stat.exists

  - name: Check application version
    command: /opt/myapp/bin/myapp --version
    register: version_check
    changed_when: false
    when: app_binary.stat.exists

  - name: Upgrade if version is old
    command: /opt/installer/upgrade.sh
    when:
      - version_check is defined
      - version_check.rc == 0
      - version_check.stdout is version(target_version, '<')
```

---

## Conditional with Failed/Changed/Skipped

```yaml
tasks:
  - name: Try to start the application
    command: /opt/myapp/start.sh
    register: start_result
    ignore_errors: yes

  - name: Install dependencies if start failed
    apt:
      name: "{{ required_packages }}"
      state: present
    when: start_result is failed

  - name: Send notification if config changed
    uri:
      url: https://hooks.slack.com/services/XXX
      method: POST
      body: '{"text": "Config updated on {{ inventory_hostname }}"}'
      body_format: json
    when: config_task is changed

  - name: Log skipped hosts
    debug:
      msg: "{{ inventory_hostname }} was skipped"
    when: previous_task is skipped
```

---

## Ternary Operator (Inline If)

```yaml
tasks:
  # Ternary filter
  - name: Set config based on environment
    template:
      src: "{{ (env == 'production') | ternary('prod.conf.j2', 'dev.conf.j2') }}"
      dest: /etc/myapp/config.conf

  # Inline if expression
  - name: Set worker count
    set_fact:
      workers: "{{ ansible_processor_vcpus * 2 if env == 'production' else 2 }}"

  # In templates
  # log_level: {{ 'warn' if env == 'production' else 'debug' }}
  # replicas: {{ 3 if env == 'production' else 1 }}
```

---

## Advanced Loop: until (Retry)

```yaml
# Retry until a condition is met
- name: Wait for application to become healthy
  uri:
    url: http://localhost:8080/health
    return_content: yes
  register: health_result
  until: health_result.status == 200
  retries: 30
  delay: 10

# Retry with custom condition
- name: Wait for database to accept connections
  command: pg_isready -h localhost -p 5432
  register: pg_result
  until: pg_result.rc == 0
  retries: 10
  delay: 5
  changed_when: false

# Retry with complex condition
- name: Wait for cluster to be fully ready
  uri:
    url: http://localhost:9200/_cluster/health
    return_content: yes
  register: cluster_health
  until:
    - cluster_health.status == 200
    - cluster_health.json.status == "green"
  retries: 60
  delay: 10
```

---

## Loop with Conditionals

```yaml
# Filter items in a loop
- name: Install only required packages
  apt:
    name: "{{ item.name }}"
    state: present
  loop:
    - name: nginx
      required: true
    - name: php-fpm
      required: true
    - name: memcached
      required: false
    - name: varnish
      required: false
  when: item.required

# Conditional per item
- name: Manage services based on role
  service:
    name: "{{ item.name }}"
    state: "{{ item.state }}"
    enabled: "{{ item.enabled }}"
  loop:
    - name: nginx
      state: started
      enabled: true
    - name: php-fpm
      state: started
      enabled: true
    - name: memcached
      state: "{{ 'started' if cache_enabled else 'stopped' }}"
      enabled: "{{ cache_enabled }}"
```

---

## Loop with Filters

```yaml
vars:
  all_users:
    - name: alice
      role: developer
      active: true
    - name: bob
      role: admin
      active: true
    - name: charlie
      role: developer
      active: false
    - name: diana
      role: admin
      active: true

tasks:
  # Select items using selectattr
  - name: Create only active users
    user:
      name: "{{ item.name }}"
      state: present
    loop: "{{ all_users | selectattr('active', 'equalto', true) | list }}"

  # Select admins only
  - name: Add admin users to sudo group
    user:
      name: "{{ item.name }}"
      groups: sudo
      append: yes
    loop: "{{ all_users | selectattr('role', 'equalto', 'admin') | selectattr('active') | list }}"
```

---

## Loop with Product (Cross-Join)

```yaml
vars:
  environments:
    - staging
    - production
  services:
    - web
    - api
    - worker

tasks:
  # Create directories for each env/service combination
  - name: Create service directories
    file:
      path: "/opt/{{ item.0 }}/{{ item.1 }}"
      state: directory
    loop: "{{ environments | product(services) | list }}"
    # Creates: /opt/staging/web, /opt/staging/api, ...
    #          /opt/production/web, /opt/production/api, ...
```

---

## Loop with Sequence

```yaml
# Generate a sequence of numbers
- name: Create numbered config files
  template:
    src: worker.conf.j2
    dest: "/etc/myapp/worker-{{ item }}.conf"
  loop: "{{ range(1, worker_count + 1) | list }}"

# With specific format
- name: Create backup directories for each day
  file:
    path: "/backup/day-{{ '%02d' | format(item) }}"
    state: directory
  loop: "{{ range(1, 8) | list }}"
  # Creates: /backup/day-01 through /backup/day-07
```

---

## Loop with Inventory

```yaml
# Loop over hosts in a group
- name: Add all webservers to load balancer
  command: >
    /opt/lb/add-backend.sh
    --name {{ item }}
    --ip {{ hostvars[item]['ansible_host'] }}
    --port 8080
  loop: "{{ groups['webservers'] }}"
  delegate_to: loadbalancer

# Loop over groups
- name: Show all groups
  debug:
    msg: "Group {{ item }} has {{ groups[item] | length }} hosts"
  loop: "{{ groups.keys() | list }}"
  when: item not in ['all', 'ungrouped']
```

---

## Parallel Loops with zip

```yaml
vars:
  server_names:
    - web01
    - web02
    - web03
  server_ips:
    - 192.168.1.10
    - 192.168.1.11
    - 192.168.1.12

tasks:
  # Iterate two lists together
  - name: Add hosts entries
    lineinfile:
      path: /etc/hosts
      line: "{{ item.1 }}  {{ item.0 }}"
    loop: "{{ server_names | zip(server_ips) | list }}"

  # Result:
  # 192.168.1.10  web01
  # 192.168.1.11  web02
  # 192.168.1.12  web03
```

---

## Flattening and Unique

```yaml
vars:
  team_packages:
    developers:
      - git
      - vim
      - python3
    ops:
      - git
      - docker
      - terraform
    security:
      - git
      - nmap
      - wireshark

tasks:
  # Flatten all packages and deduplicate
  - name: Install all team packages
    apt:
      name: "{{ team_packages.values() | list | flatten | unique }}"
      state: present
    # Installs: git, vim, python3, docker, terraform, nmap, wireshark
    # (git appears only once)
```

---

## changed_when and failed_when

```yaml
tasks:
  # Custom changed condition
  - name: Run database migration
    command: /opt/myapp/migrate.sh
    register: migration
    changed_when: "'Migrated' in migration.stdout"

  # Never mark as changed (read-only command)
  - name: Check current version
    command: cat /opt/myapp/VERSION
    register: current_version
    changed_when: false

  # Custom failure condition
  - name: Check application health
    uri:
      url: http://localhost:8080/health
      return_content: yes
    register: health
    failed_when:
      - health.status != 200 or
        health.json.status != 'healthy'

  # Ignore specific return codes
  - name: Check if process exists
    command: pgrep -f myapp
    register: pgrep_result
    failed_when: pgrep_result.rc > 1  # rc=1 means not found (ok)
    changed_when: false
```

---

## Conditional Import and Include

```yaml
# Include tasks based on OS
- name: Include OS-specific tasks
  include_tasks: "{{ ansible_os_family | lower }}.yml"

# Include with fallback
- name: Include environment config
  include_tasks: "{{ item }}"
  with_first_found:
    - "tasks/{{ env }}.yml"
    - "tasks/default.yml"

# Conditional role inclusion
- name: Apply security role only in production
  include_role:
    name: security_hardening
  when: env == "production"

# Import vars conditionally
- name: Load environment variables
  include_vars: "vars/{{ env }}.yml"
```

---

## Exercise: Conditionals and Loops Lab

1. Create a playbook that:
    1. Detects the OS and installs appropriate packages
    1. Creates users from a list with conditional group membership
    1. Sets up firewall rules using a loop with dict2items
    1. Retries a health check until the service is ready
    1. Uses `block/rescue` for error handling
1. Test with `--check --diff` first
1. Verify idempotency by running twice

---

## Loop Constructs

![loop_constructs](svg/courses/devops/ansible/06_conditionals_and_loops/loop_constructs.svg)

---

## Conditional Expressions

![conditional_expressions](svg/courses/devops/ansible/06_conditionals_and_loops/conditional_expressions.svg)
