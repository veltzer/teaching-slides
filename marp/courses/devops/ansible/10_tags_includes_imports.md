# Tags, Includes, and Imports

## Topics Covered
- Tag strategies for large projects
- Static imports vs dynamic includes
- Task file organization
- Reusable task patterns
- Import/include for roles and variables

---

## Tags Strategy

```yaml
# Tagging convention for large projects
- name: Install packages
  apt:
    name: nginx
  tags:
    - install       # Action type
    - nginx         # Component
    - webserver     # Layer

# Standard tag categories:
# Action:    install, configure, deploy, verify
# Component: nginx, postgresql, app
# Layer:     webserver, database, monitoring
# Phase:     setup, config, service
# Special:   always, never
```

---

## Tag Inheritance

```yaml
# Tags on plays apply to ALL tasks in the play
- name: Configure webservers
  hosts: webservers
  tags: webserver        # ALL tasks get this tag
  tasks:
    - name: Install nginx    # Has: webserver
      apt:
        name: nginx

    - name: Deploy config    # Has: webserver, config
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/nginx.conf
      tags: config

# Tags on blocks apply to all tasks in the block
- name: Setup tasks
  block:
    - name: Task A           # Has: setup
      debug: msg="A"
    - name: Task B           # Has: setup
      debug: msg="B"
  tags: setup
```

---

## Special Tags

```yaml
# 'always' - runs unless explicitly skipped
- name: Gather deployment info
  debug:
    msg: "Starting deployment at {{ ansible_date_time.iso8601 }}"
  tags: always

# 'never' - only runs when explicitly requested
- name: Factory reset (DANGEROUS)
  command: /opt/factory-reset.sh
  tags: never

# Running with special tags
# ansible-playbook site.yml --tags "config"
# ^^^ 'always' tasks also run
#
# ansible-playbook site.yml --skip-tags "always"
# ^^^ 'always' tasks are skipped
#
# ansible-playbook site.yml --tags "never"
# ^^^ Only 'never' tasks run (plus 'always')
```

---

## import_tasks vs include_tasks

```yaml
# import_tasks: STATIC - processed at parse time
- name: Setup webserver
  import_tasks: tasks/webserver.yml
  # Tags are inherited by imported tasks
  # Cannot use loops
  # Cannot use when with loop vars
  # Variables are resolved at parse time
  tags: webserver

# include_tasks: DYNAMIC - processed at runtime
- name: Setup webserver
  include_tasks: tasks/webserver.yml
  # Tags are NOT inherited
  # CAN use loops and conditionals
  # Variables are resolved at runtime
  when: setup_webserver | bool
  tags: webserver
```

---

## When to Use Import vs Include

```misc
Use import_tasks when:
  - You want tag inheritance
  - Tasks are always needed
  - You need --list-tasks to show them
  - File is known at parse time

Use include_tasks when:
  - Filename depends on a variable
  - Used inside a loop
  - Conditional inclusion based on facts
  - Loading OS-specific task files
```

---

## Dynamic Include Pattern

```yaml
# Include based on operating system
- name: Include OS-specific tasks
  include_tasks: "{{ ansible_os_family | lower }}.yml"
  # Loads debian.yml or redhat.yml

# Include with first_found
- name: Include environment tasks
  include_tasks: "{{ lookup('first_found', params) }}"
  vars:
    params:
      files:
        - "{{ env }}.yml"
        - "{{ ansible_os_family | lower }}.yml"
        - default.yml
      paths:
        - tasks

# Include in a loop
- name: Setup each application
  include_tasks: setup_app.yml
  loop: "{{ applications }}"
  loop_control:
    loop_var: app
  vars:
    app_name: "{{ app.name }}"
    app_version: "{{ app.version }}"
```

---

## Task File Organization

```yaml
# roles/myapp/tasks/main.yml

---
- name: Include prerequisite tasks
  import_tasks: prerequisites.yml
  tags: prerequisites

- name: Include installation tasks
  import_tasks: install.yml
  tags: install

- name: Include configuration tasks
  import_tasks: configure.yml
  tags: configure

- name: Include service tasks
  import_tasks: service.yml
  tags: service

- name: Include verification tasks
  import_tasks: verify.yml
  tags: verify
```

---

## Reusable Task File Example

```yaml
# tasks/deploy_app.yml
# Reusable deployment task file
# Required variables: app_name, app_version, app_port

---
- name: "Deploy {{ app_name }} v{{ app_version }}"
  git:
    repo: "https://github.com/myorg/{{ app_name }}.git"
    dest: "/opt/{{ app_name }}"
    version: "v{{ app_version }}"

- name: "Install {{ app_name }} dependencies"
  pip:
    requirements: "/opt/{{ app_name }}/requirements.txt"
    virtualenv: "/opt/{{ app_name }}/venv"

- name: "Deploy {{ app_name }} systemd unit"
  template:
    src: app.service.j2
    dest: "/etc/systemd/system/{{ app_name }}.service"
  notify: "restart {{ app_name }}"

- name: "Ensure {{ app_name }} is running"
  systemd:
    name: "{{ app_name }}"
    state: started
    enabled: yes
    daemon_reload: yes
```

---

## import_role vs include_role

```yaml
# import_role: Static
- name: Apply nginx role
  import_role:
    name: nginx
  vars:
    nginx_port: 8080
  tags: nginx

# include_role: Dynamic
- name: Apply role based on variable
  include_role:
    name: "{{ item }}"
  loop:
    - common
    - "{{ web_role }}"
    - monitoring

# include_role with tasks_from
- name: Run only specific tasks from role
  include_role:
    name: nginx
    tasks_from: vhosts   # Only runs tasks/vhosts.yml
```

---

## Include Variables

```yaml
# Load variables from a file
- name: Load common variables
  include_vars: vars/common.yml

# Load based on OS
- name: Load OS-specific variables
  include_vars: "vars/{{ ansible_os_family | lower }}.yml"

# Load all files from a directory
- name: Load all variable files
  include_vars:
    dir: vars/
    extensions:
      - yml
      - yaml

# Load with name prefix
- name: Load app config
  include_vars:
    file: vars/app_config.yml
    name: app_config
  # Access as: {{ app_config.key }}
```

---

## Complete Pattern: Multi-Tier Deployment

```yaml
# site.yml

---
- name: Apply base configuration
  hosts: all
  tags: base
  tasks:
    - import_tasks: tasks/base/packages.yml
    - import_tasks: tasks/base/users.yml
    - import_tasks: tasks/base/security.yml

- name: Deploy web tier
  hosts: webservers
  tags: web
  tasks:
    - include_tasks: tasks/deploy_app.yml
      vars:
        app_name: frontend
        app_version: "{{ frontend_version }}"
        app_port: 3000

- name: Deploy API tier
  hosts: apiservers
  tags: api
  tasks:
    - include_tasks: tasks/deploy_app.yml
      vars:
        app_name: backend
        app_version: "{{ backend_version }}"
        app_port: 8080

- name: Deploy database tier
  hosts: dbservers
  tags: database
  tasks:
    - import_tasks: tasks/database/setup.yml
    - import_tasks: tasks/database/migrate.yml
      tags: migrate
```

---

## Listing Tasks and Tags

```bash
# List all tasks in a playbook
ansible-playbook site.yml --list-tasks

# List all tags
ansible-playbook site.yml --list-tags

# Note: import_tasks tasks appear in --list-tasks
# but include_tasks tasks do NOT (they're dynamic)

# Run specific tags
ansible-playbook site.yml --tags "install,config"

# Skip specific tags
ansible-playbook site.yml --skip-tags "verify"

# Combine with limit
ansible-playbook site.yml --tags "deploy" --limit "web01"
```

---

## Best Practices

- Use `import_tasks` for static, always-needed includes
- Use `include_tasks` for conditional/dynamic includes
- Keep task files focused and small (< 50 lines)
- Use consistent tag naming across the project
- Document required variables at the top of task files
- Use `loop_control.loop_var` to avoid variable conflicts
- Prefer `import_role` in the `roles:` section of a play
- Use `include_role` with `tasks_from` for partial role execution
