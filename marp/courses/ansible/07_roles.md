# Roles: Structure, Creation, and Galaxy

## Topics Covered
- What are roles and why use them
- Role directory structure
- Creating roles from scratch
- Role dependencies
- `Ansible Galaxy` and collections
- Role best practices

---

## What Are Roles?

- Roles are reusable, self-contained automation units
- Package tasks, handlers, variables, templates, and files together
- Enable code reuse across projects and teams
- Follow a standard directory structure
- Can be shared via `Ansible Galaxy`

---

## Why Use Roles?

```text
Without Roles:                    With Roles:
site.yml (500 lines)              site.yml (20 lines)
  - install packages              roles/
  - configure nginx                 nginx/
  - deploy templates                postgresql/
  - set up database                 app/
  - configure app                   monitoring/
  - set up monitoring
  - ... everything in one file    Each role: focused, testable,
                                  reusable, shareable
```

---

## Role Directory Structure

```text
roles/
└── nginx/
    ├── defaults/
    │   └── main.yml        # Default variables (lowest priority)
    ├── vars/
    │   └── main.yml        # Role variables (high priority)
    ├── tasks/
    │   └── main.yml        # Main task list
    ├── handlers/
    │   └── main.yml        # Handler definitions
    ├── templates/
    │   └── nginx.conf.j2   # Jinja2 templates
    ├── files/
    │   └── index.html      # Static files
    ├── meta/
    │   └── main.yml        # Role metadata and dependencies
    ├── tests/
    │   ├── inventory
    │   └── test.yml        # Test playbook
    └── README.md           # Documentation
```

---

## Creating a Role with ansible-galaxy

```bash
# Create a role skeleton
ansible-galaxy init roles/nginx

# Output:
# - roles/nginx was created successfully

# The structure is created automatically:
$ tree roles/nginx/
roles/nginx/
├── defaults/
│   └── main.yml
├── files/
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── README.md
├── tasks/
│   └── main.yml
├── templates/
├── tests/
│   ├── inventory
│   └── test.yml
└── vars/
    └── main.yml
```

---

## Role: defaults/main.yml

```yaml
# roles/nginx/defaults/main.yml
# These are the LOWEST priority variables
# Users can easily override them
---
nginx_worker_processes: auto
nginx_worker_connections: 1024
nginx_keepalive_timeout: 65
nginx_server_tokens: "off"

nginx_log_dir: /var/log/nginx
nginx_access_log: "{{ nginx_log_dir }}/access.log"
nginx_error_log: "{{ nginx_log_dir }}/error.log"

nginx_vhosts: []

nginx_ssl_protocols: "TLSv1.2 TLSv1.3"
nginx_ssl_ciphers: "ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256"

nginx_remove_default_site: true
```

---

## Role: tasks/main.yml

```yaml
# roles/nginx/tasks/main.yml
---
- name: Include OS-specific variables
  include_vars: "{{ ansible_os_family | lower }}.yml"

- name: Install nginx
  package:
    name: "{{ nginx_package_name }}"
    state: present
  tags: nginx_install

- name: Deploy nginx.conf
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
    validate: "nginx -t -c %s"
  notify: restart nginx
  tags: nginx_config

- name: Remove default site
  file:
    path: /etc/nginx/sites-enabled/default
    state: absent
  when: nginx_remove_default_site
  notify: reload nginx

- name: Deploy virtual hosts
  include_tasks: vhosts.yml
  when: nginx_vhosts | length > 0
  tags: nginx_vhosts

- name: Ensure nginx is started and enabled
  service:
    name: nginx
    state: started
    enabled: yes
  tags: nginx_service
```

---

## Role: Splitting Tasks into Files

```yaml
# roles/nginx/tasks/vhosts.yml
---
- name: Create sites-available directory
  file:
    path: /etc/nginx/sites-available
    state: directory
    mode: '0755'

- name: Deploy virtual host configs
  template:
    src: vhost.conf.j2
    dest: "/etc/nginx/sites-available/{{ item.server_name }}.conf"
  loop: "{{ nginx_vhosts }}"
  notify: reload nginx

- name: Enable virtual hosts
  file:
    src: "/etc/nginx/sites-available/{{ item.server_name }}.conf"
    dest: "/etc/nginx/sites-enabled/{{ item.server_name }}.conf"
    state: link
  loop: "{{ nginx_vhosts }}"
  notify: reload nginx

- name: Create document roots
  file:
    path: "{{ item.document_root }}"
    state: directory
    owner: "{{ item.owner | default('www-data') }}"
    mode: '0755'
  loop: "{{ nginx_vhosts }}"
  when: item.document_root is defined
```

---

## Role: handlers/main.yml

```yaml
# roles/nginx/handlers/main.yml
---
- name: restart nginx
  service:
    name: nginx
    state: restarted
  listen: restart nginx

- name: reload nginx
  service:
    name: nginx
    state: reloaded
  listen: reload nginx

- name: validate nginx config
  command: nginx -t
  listen: validate nginx
```

---

## Role: templates

```jinja2
{# roles/nginx/templates/nginx.conf.j2 #}
# Managed by Ansible - DO NOT EDIT

user www-data;
worker_processes {{ nginx_worker_processes }};
pid /run/nginx.pid;

events {
    worker_connections {{ nginx_worker_connections }};
    multi_accept on;
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout {{ nginx_keepalive_timeout }};
    types_hash_max_size 2048;
    server_tokens {{ nginx_server_tokens }};

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log {{ nginx_access_log }};
    error_log {{ nginx_error_log }};

    gzip on;
    gzip_vary on;
    gzip_min_length 256;
    gzip_types text/plain text/css application/json application/javascript;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

---

## Role: meta/main.yml

```yaml
# roles/nginx/meta/main.yml
---
galaxy_info:
  author: DevOps Team
  description: Install and configure Nginx
  company: My Company
  license: MIT
  min_ansible_version: "2.14"
  platforms:
    - name: Ubuntu
      versions:
        - jammy
        - focal
    - name: Debian
      versions:
        - bullseye
        - bookworm
  galaxy_tags:
    - nginx
    - web
    - proxy

dependencies:
  - role: common
  - role: firewall
    vars:
      firewall_allowed_ports:
        - 80
        - 443
```

---

## Role: OS-Specific Variables

```yaml
# roles/nginx/vars/debian.yml
---
nginx_package_name: nginx
nginx_service_name: nginx
nginx_conf_dir: /etc/nginx

# roles/nginx/vars/redhat.yml
---
nginx_package_name: nginx
nginx_service_name: nginx
nginx_conf_dir: /etc/nginx

# In tasks/main.yml, load the right file:
- name: Include OS-specific variables
  include_vars: "{{ ansible_os_family | lower }}.yml"
```

---

## Using Roles in Playbooks

```yaml
# Method 1: Classic roles section
---
- name: Configure webservers
  hosts: webservers
  become: true
  roles:
    - common
    - nginx
    - role: postgresql
      when: "'dbservers' in group_names"

# Method 2: With variables
- name: Configure webservers
  hosts: webservers
  become: true
  roles:
    - role: nginx
      vars:
        nginx_worker_connections: 2048
        nginx_vhosts:
          - server_name: app.example.com
            document_root: /var/www/app
```

---

## Include Role vs Import Role

```yaml
tasks:
  # import_role: Static, processed at playbook parse time
  # - Tags are inherited
  # - Cannot be used with loops
  # - Cannot be conditional per loop iteration
  - import_role:
      name: nginx
    tags: webserver

  # include_role: Dynamic, processed at runtime
  # - Can be used with loops and conditionals
  # - Tags are NOT inherited
  # - More flexible but slightly slower
  - include_role:
      name: app_deploy
    vars:
      app_version: "{{ item }}"
    loop:
      - frontend
      - backend
    when: deploy_enabled
```

---

## Role Dependencies

```yaml
# roles/app/meta/main.yml
dependencies:
  # Simple dependency
  - role: common

  # Dependency with variables
  - role: nginx
    vars:
      nginx_vhosts:
        - server_name: "{{ app_domain }}"
          proxy_pass: "http://127.0.0.1:{{ app_port }}"

  # Conditional dependency
  - role: ssl_certificates
    when: ssl_enabled | default(false)

# Note: By default, dependencies run only once
# even if listed by multiple roles.
# To run a role multiple times, set:
#   allow_duplicates: true
# in the role's meta/main.yml
```

---

## Complete Role Example: PostgreSQL

```yaml
# roles/postgresql/defaults/main.yml
---
postgresql_version: "15"
postgresql_port: 5432
postgresql_max_connections: 100
postgresql_shared_buffers: "256MB"
postgresql_work_mem: "4MB"
postgresql_data_dir: "/var/lib/postgresql/{{ postgresql_version }}/main"

postgresql_databases: []
postgresql_users: []

postgresql_hba_entries:
  - type: local
    database: all
    user: postgres
    method: peer
  - type: host
    database: all
    user: all
    address: "127.0.0.1/32"
    method: md5
```

---

## PostgreSQL Role: Tasks

```yaml
# roles/postgresql/tasks/main.yml
---
- name: Install PostgreSQL
  apt:
    name:
      - "postgresql-{{ postgresql_version }}"
      - postgresql-contrib
      - python3-psycopg2
    state: present

- name: Deploy PostgreSQL configuration
  template:
    src: postgresql.conf.j2
    dest: "{{ postgresql_data_dir }}/postgresql.conf"
  notify: restart postgresql

- name: Deploy pg_hba.conf
  template:
    src: pg_hba.conf.j2
    dest: "{{ postgresql_data_dir }}/pg_hba.conf"
  notify: reload postgresql

- name: Ensure PostgreSQL is running
  service:
    name: postgresql
    state: started
    enabled: yes

- name: Create databases
  become_user: postgres
  postgresql_db:
    name: "{{ item.name }}"
    encoding: "{{ item.encoding | default('UTF-8') }}"
    state: present
  loop: "{{ postgresql_databases }}"

- name: Create users
  become_user: postgres
  postgresql_user:
    name: "{{ item.name }}"
    password: "{{ item.password }}"
    db: "{{ item.db | default(omit) }}"
    priv: "{{ item.priv | default(omit) }}"
    state: present
  loop: "{{ postgresql_users }}"
  no_log: true
```

---

## Ansible Galaxy

- Community hub for sharing `Ansible` content
- Roles and collections from thousands of contributors
- Command-line tool: `ansible-galaxy`

```bash
# Search for roles
ansible-galaxy search nginx
ansible-galaxy search postgresql --author geerlingguy

# Install a role
ansible-galaxy install geerlingguy.nginx
ansible-galaxy install geerlingguy.postgresql

# Install to a specific path
ansible-galaxy install geerlingguy.nginx -p roles/

# Install with a specific version
ansible-galaxy install geerlingguy.nginx,4.2.0

# List installed roles
ansible-galaxy list

# Remove a role
ansible-galaxy remove geerlingguy.nginx
```

---

## Requirements File

```yaml
# requirements.yml
---
roles:
  - name: geerlingguy.nginx
    version: "4.2.0"
  - name: geerlingguy.postgresql
    version: "6.1.0"
  - name: geerlingguy.docker
  - name: custom_role
    src: git+https://github.com/myorg/custom-role.git
    version: v1.5.0

collections:
  - name: community.general
    version: ">=7.0.0"
  - name: amazon.aws
    version: "6.5.0"
  - name: community.docker
```

```bash
# Install all requirements
ansible-galaxy install -r requirements.yml

# Install collections
ansible-galaxy collection install -r requirements.yml

# Force reinstall
ansible-galaxy install -r requirements.yml --force
```

---

## Ansible Collections

- Collections bundle roles, modules, plugins, and documentation
- Namespace format: `namespace.collection`
- Replace standalone role distribution model

```bash
# Install a collection
ansible-galaxy collection install community.general
ansible-galaxy collection install amazon.aws

# Use collection modules with FQCN
- name: Create EC2 instance
  amazon.aws.ec2_instance:
    name: web01
    instance_type: t3.micro
    image_id: ami-12345678

# List installed collections
ansible-galaxy collection list

# Build your own collection
ansible-galaxy collection init myorg.mytools
```

---

## Collection Structure

```text
myorg/
└── mytools/
    ├── galaxy.yml         # Collection metadata
    ├── plugins/
    │   ├── modules/       # Custom modules
    │   ├── inventory/     # Inventory plugins
    │   ├── callback/      # Callback plugins
    │   ├── filter/        # Custom Jinja2 filters
    │   └── lookup/        # Lookup plugins
    ├── roles/
    │   ├── webserver/     # Bundled roles
    │   └── database/
    ├── playbooks/         # Example playbooks
    ├── docs/
    └── tests/
```

---

## Project Layout with Roles

```text
ansible-project/
├── ansible.cfg
├── requirements.yml
├── inventories/
│   ├── production/
│   │   ├── hosts.yml
│   │   ├── group_vars/
│   │   └── host_vars/
│   └── staging/
├── roles/
│   ├── common/           # Custom roles
│   ├── nginx/
│   ├── app/
│   └── monitoring/
├── playbooks/
│   ├── site.yml          # Main playbook
│   ├── webservers.yml
│   ├── dbservers.yml
│   └── deploy.yml
├── templates/
├── files/
└── group_vars/
    └── all/
        ├── vars.yml
        └── vault.yml
```

---

## The Site Playbook Pattern

```yaml
# playbooks/site.yml - master playbook
---
- name: Apply common configuration
  hosts: all
  become: true
  roles:
    - common

- name: Configure webservers
  hosts: webservers
  become: true
  roles:
    - nginx
    - app

- name: Configure database servers
  hosts: dbservers
  become: true
  roles:
    - postgresql

- name: Configure monitoring
  hosts: monitoring
  become: true
  roles:
    - prometheus
    - grafana
```

---

## Role Best Practices

- Keep roles focused on a single responsibility
- Use `defaults/main.yml` for all configurable values
- Document all variables in a README
- Use `meta/main.yml` for dependencies
- Include tests in `tests/` directory
- Use tags for all tasks
- Follow naming conventions: `rolename_variable_name`
- Never hardcode values; always use variables
- Use FQCN for modules: `ansible.builtin.apt`
- Test roles with `Molecule` (covered in Day 3)

---

## Exercise: Roles Lab

1. Create a `common` role that:
    - Sets timezone and hostname
    - Installs essential packages
    - Configures `NTP` and `SSH`
    - Creates admin users
1. Create an `nginx` role with:
    - Configurable virtual hosts
    - `SSL` support
    - Custom error pages
1. Use both roles in a `site.yml` playbook
1. Test with different variable values per environment
