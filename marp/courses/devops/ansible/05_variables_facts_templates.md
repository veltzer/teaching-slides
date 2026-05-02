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
# Variables, Facts, and Templating

## Topics Covered
- Advanced variable usage
- Magic variables and special variables
- `Jinja2` templating engine
- Filters and lookups
- Template best practices

---
## Variable Precedence

![precedence_overview](svg/courses/devops/ansible/05_variables_facts_templates/precedence_overview.svg)

---

## Ansible Variable Precedence

![Ansible Variable Precedence](svg/courses/devops/ansible/05_variables_facts_templates/variable_precedence.svg)

---

## Magic Variables

```yaml
# Ansible provides built-in "magic" variables:
- name: Show magic variables
  debug:
    msg: |
      Hostname: {{ inventory_hostname }}
      Short name: {{ inventory_hostname_short }}
      All groups: {{ group_names }}
      All hosts: {{ groups['all'] }}
      Host vars: {{ hostvars[inventory_hostname] }}
      Play hosts: {{ ansible_play_hosts }}
      Play name: {{ ansible_play_name }}
      Role name: {{ role_name | default('none') }}
      Role path: {{ role_path | default('none') }}
```

---

## The hostvars Variable

```yaml
# Access variables from other hosts
- name: Get database IP from db server
  debug:
    msg: "DB IP: {{ hostvars['db01']['ansible_default_ipv4']['address'] }}"

# Use in templates for cross-host configuration
- name: Deploy app config with DB host
  template:
    src: app.conf.j2
    dest: /etc/myapp/config.yml

# app.conf.j2
# database:
#   host: {{ hostvars[groups['dbservers'][0]]['ansible_host'] }}
#   port: {{ hostvars[groups['dbservers'][0]]['db_port'] }}
```

---

## The groups Variable

```yaml
# Access all groups and their members
- name: Show all webservers
  debug:
    msg: "Webservers: {{ groups['webservers'] }}"

# Generate configuration using group members
- name: Create upstream config
  template:
    src: upstream.conf.j2
    dest: /etc/nginx/conf.d/upstream.conf

# upstream.conf.j2:
# upstream backend {
# {% for host in groups['webservers'] %}
#     server {{ hostvars[host]['ansible_host'] }}:8080;
# {% endfor %}
# }
```

---

## Complex Variable Structures

```yaml
vars:
  # Nested dictionaries
  database:
    primary:
      host: db01.example.com
      port: 5432
      name: myapp_prod
      credentials:
        username: app_user
        password: "{{ vault_db_password }}"
    replica:
      host: db02.example.com
      port: 5432

  # List of dictionaries
  virtual_hosts:
    - domain: app.example.com
      document_root: /var/www/app
      ssl: true
      ssl_cert: /etc/ssl/app.pem
    - domain: api.example.com
      document_root: /var/www/api
      ssl: true
      ssl_cert: /etc/ssl/api.pem

tasks:
    - name: Show DB host
    debug:
      msg: "Primary DB: {{ database.primary.host }}:{{ database.primary.port }}"
```

---

## Variable Merging with hash_behaviour

```yaml
# By default, dictionaries are REPLACED, not merged
# In group_vars/all.yml:
config:
  log_level: info
  max_connections: 100

# In group_vars/webservers.yml:
config:
  max_connections: 500

# Result: config = {max_connections: 500}
# The log_level key is LOST!

# To merge instead, use combine filter:
- name: Merge configs
  set_fact:
    merged_config: "{{ default_config | combine(override_config, recursive=True) }}"
```

---

## Introduction to Jinja2

- `Jinja2` is the templating engine used by `Ansible`
- Used in templates, playbooks, and variable expressions
- Syntax elements:
    - `{{ }}` - expressions (output a value)
    - `{% %}` - statements (logic: if, for, etc.)
    - `{# #}` - comments

```jinja
{# This is a comment #}

{# Expression: output a variable #}
ServerName {{ server_name }}

{# Statement: conditional #}
{% if ssl_enabled %}
SSLEngine on
{% endif %}

{# Statement: loop #}
{% for port in open_ports %}
Listen {{ port }}
{% endfor %}
```

---

## Jinja2 in Playbooks vs Templates

```yaml
# In playbooks: expressions only ({{ }})
tasks:
    - name: Use variable in task
    debug:
      msg: "Hello {{ user_name }}"

  # Jinja2 statements in 'when' (no {{ }} needed)
    - name: Conditional task
    debug:
      msg: "Production mode"
    when: env == "production"

# In template files (.j2): full Jinja2 syntax
# nginx.conf.j2
# worker_processes {{ ansible_processor_vcpus }};
# {% for vhost in virtual_hosts %}
# server {
#     listen {{ vhost.port | default(80) }};
#     server_name {{ vhost.domain }};
# }
# {% endfor %}
```

---

## Template Module

```yaml
# Deploy a template
- name: Deploy nginx configuration
  template:
    src: templates/nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: '0644'
    backup: yes
    validate: "nginx -t -c %s"
  notify: reload nginx

# Template with variable in filename
- name: Deploy virtual host config
  template:
    src: vhost.conf.j2
    dest: "/etc/nginx/sites-available/{{ domain }}.conf"
  loop: "{{ virtual_hosts }}"
  loop_control:
    loop_var: domain
```

---

## Jinja2 Conditionals in Templates

```jinja
{# nginx.conf.j2 #}
server {
    listen 80;
    server_name {{ server_name }};

{% if ssl_enabled | default(false) %}
    listen 443 ssl;
    ssl_certificate {{ ssl_cert_path }};
    ssl_certificate_key {{ ssl_key_path }};

    {# Redirect HTTP to HTTPS #}
    if ($scheme = http) {
        return 301 https://$server_name$request_uri;
    }
{% endif %}

{% if proxy_pass is defined %}
    location / {
        proxy_pass {{ proxy_pass }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
{% else %}
    root {{ document_root | default('/var/www/html') }};
    index index.html;
{% endif %}
}
```

---

## Jinja2 Loops in Templates

```jinja
{# haproxy.cfg.j2 #}
global
    log /dev/log local0
    maxconn 4096

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

frontend http_front
    bind *:80
    default_backend http_back

backend http_back
    balance roundrobin
{% for host in groups['webservers'] %}
    server {{ host }} {{ hostvars[host]['ansible_host'] }}:{{ http_port | default(8080) }} check
{% endfor %}

{# With loop index #}
{% for server in backend_servers %}
    server app{{ loop.index }} {{ server.ip }}:{{ server.port }} weight {{ server.weight | default(1) }}
{% endfor %}
```

---

## Jinja2 Loop Variables

```jinja
{% for item in my_list %}
  {{ loop.index }}      {# 1-based index #}
  {{ loop.index0 }}     {# 0-based index #}
  {{ loop.first }}      {# true if first iteration #}
  {{ loop.last }}       {# true if last iteration #}
  {{ loop.length }}     {# total number of items #}
  {{ loop.revindex }}   {# reverse index (1-based) #}
{% endfor %}

{# Practical example: comma-separated list #}
upstream backend {
{% for host in groups['webservers'] %}
    server {{ hostvars[host]['ansible_host'] }}:8080{% if not loop.last %};{% endif %}

{% endfor %}
}
```

---

## Jinja2 Filters

```yaml
# Filters transform data using the pipe (|) operator
tasks:
    - name: String filters
    debug:
      msg: |
        Upper: {{ name | upper }}
        Lower: {{ name | lower }}
        Title: {{ name | title }}
        Replace: {{ name | replace('old', 'new') }}
        Trim: {{ name | trim }}
        Length: {{ name | length }}

    - name: Default filter
    debug:
      msg: "Port: {{ custom_port | default(8080) }}"

    - name: Type conversion
    debug:
      msg: "Port as int: {{ port_string | int }}"
```

---

## Common Ansible Filters

```yaml
tasks:
  # List filters
    - debug:
      msg: |
        First: {{ mylist | first }}
        Last: {{ mylist | last }}
        Unique: {{ mylist | unique }}
        Sort: {{ mylist | sort }}
        Flatten: {{ nested_list | flatten }}
        Min: {{ numbers | min }}
        Max: {{ numbers | max }}
        Join: {{ mylist | join(', ') }}

  # Dict filters
    - debug:
      msg: |
        Keys: {{ mydict | dict2items | map(attribute='key') | list }}
        Combine: {{ dict1 | combine(dict2) }}

  # Path filters
    - debug:
      msg: |
        Basename: {{ '/etc/nginx/nginx.conf' | basename }}
        Dirname: {{ '/etc/nginx/nginx.conf' | dirname }}
        Expanduser: {{ '~/.ssh' | expanduser }}
```

---

## Filters for Data Manipulation

```yaml
tasks:
  # JSON/YAML conversion
    - name: Convert to JSON
    debug:
      msg: "{{ my_dict | to_json }}"

    - name: Convert to nice JSON
    debug:
      msg: "{{ my_dict | to_nice_json }}"

    - name: Convert to YAML
    debug:
      msg: "{{ my_dict | to_yaml }}"

  # Regex filters
    - name: Extract with regex
    debug:
      msg: "{{ 'server-web-01' | regex_replace('^server-(\\w+)-(\\d+)$', '\\1_\\2') }}"

  # IP address filters
    - name: IP manipulation
    debug:
      msg: |
        Network: {{ '192.168.1.10/24' | ipaddr('network') }}
        Prefix: {{ '192.168.1.10/24' | ipaddr('prefix') }}
        Is valid: {{ '192.168.1.10' | ipaddr }}
```

---

## Hash and Encryption Filters

```yaml
tasks:
  # Password hashing
    - name: Create user with hashed password
    user:
      name: admin
      password: "{{ 'mypassword' | password_hash('sha512', 'mysalt') }}"

  # MD5/SHA hashing
    - name: Show hash values
    debug:
      msg: |
        MD5: {{ 'hello' | hash('md5') }}
        SHA1: {{ 'hello' | hash('sha1') }}
        SHA256: {{ 'hello' | hash('sha256') }}

  # Base64
    - name: Encode/decode base64
    debug:
      msg: |
        Encoded: {{ 'hello world' | b64encode }}
        Decoded: {{ 'aGVsbG8gd29ybGQ=' | b64decode }}
```

---

## Lookup Plugins

```yaml
tasks:
  # Read a file
    - name: Load SSH key
    debug:
      msg: "{{ lookup('file', '/home/user/.ssh/id_rsa.pub') }}"

  # Environment variable
    - name: Get HOME directory
    debug:
      msg: "{{ lookup('env', 'HOME') }}"

  # Password generation
    - name: Generate random password
    debug:
      msg: "{{ lookup('password', '/dev/null length=20 chars=ascii_letters,digits') }}"

  # Read from CSV
    - name: Lookup from CSV
    debug:
      msg: "{{ lookup('csvfile', 'web01 file=servers.csv delimiter=, col=2') }}"

  # Read a template
    - name: Render template as variable
    set_fact:
      rendered_config: "{{ lookup('template', 'config.yml.j2') }}"
```

---

## Lookup Plugins: pipe and url

```yaml
tasks:
  # Run a command and use output
    - name: Get current git commit
    debug:
      msg: "{{ lookup('pipe', 'git rev-parse HEAD') }}"

  # Fetch content from URL
    - name: Get external config
    debug:
      msg: "{{ lookup('url', 'https://api.example.com/config') }}"

  # Read lines from a file
    - name: Process each line
    debug:
      msg: "Processing: {{ item }}"
    loop: "{{ lookup('file', 'servers.txt').splitlines() }}"

  # Fileglob - find files
    - name: Copy all config files
    copy:
      src: "{{ item }}"
      dest: /etc/myapp/conf.d/
    loop: "{{ lookup('fileglob', 'files/configs/*.conf', wantlist=True) }}"
```

---

## Practical Template: Nginx Virtual Host

```jinja
{# templates/vhost.conf.j2 #}
# Managed by Ansible - DO NOT EDIT
# Generated on {{ ansible_date_time.iso8601 }}

{% for vhost in virtual_hosts %}
server {
    listen {{ vhost.port | default(80) }};
    server_name {{ vhost.domain }};

{% if vhost.ssl | default(false) %}
    listen 443 ssl http2;
    ssl_certificate /etc/ssl/certs/{{ vhost.domain }}.pem;
    ssl_certificate_key /etc/ssl/private/{{ vhost.domain }}.key;
    ssl_protocols TLSv1.2 TLSv1.3;
{% endif %}
```

---

## Nginx Virtual Host Template: Locations

```jinja
    root {{ vhost.document_root }};
    index index.html index.php;

    access_log /var/log/nginx/{{ vhost.domain }}_access.log;
    error_log /var/log/nginx/{{ vhost.domain }}_error.log;

{% if vhost.locations is defined %}
{% for location in vhost.locations %}
    location {{ location.path }} {
{% if location.proxy_pass is defined %}
        proxy_pass {{ location.proxy_pass }};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
{% elif location.root is defined %}
        root {{ location.root }};
{% endif %}
    }
{% endfor %}
{% endif %}
}

{% endfor %}
```

---

## Practical Template: Application Config

```jinja
{# templates/app-config.yml.j2 #}
# Application Configuration
# Managed by Ansible

app:
  name: {{ app_name }}
  version: {{ app_version }}
  environment: {{ env }}
  debug: {{ debug_mode | default(false) | lower }}

server:
  host: 0.0.0.0
  port: {{ app_port | default(8080) }}
  workers: {{ ansible_processor_vcpus * 2 }}

database:
  host: {{ database.host }}
  port: {{ database.port | default(5432) }}
  name: {{ database.name }}
  username: {{ database.username }}
  password: {{ database.password }}
  pool_size: {{ database.pool_size | default(10) }}

cache:
{% if redis_host is defined %}
  type: redis
  host: {{ redis_host }}
  port: {{ redis_port | default(6379) }}
{% else %}
  type: memory
{% endif %}

logging:
  level: {{ log_level | default('info') }}
  file: /var/log/{{ app_name }}/app.log
  max_size: {{ log_max_size | default('100M') }}
  retention: {{ log_retention_days | default(30) }}
```

---

## Practical Template: Systemd Unit File

```jinja
{# templates/app.service.j2 #}
[Unit]
Description={{ app_name }} Application Service
After=network.target
{% if database is defined %}
After=postgresql.service
Requires=postgresql.service
{% endif %}

[Service]
Type=simple
User={{ app_user }}
Group={{ app_group | default(app_user) }}
WorkingDirectory={{ app_root }}
Environment="APP_ENV={{ env }}"
Environment="APP_PORT={{ app_port | default(8080) }}"
{% for key, value in (env_vars | default({})).items() %}
Environment="{{ key }}={{ value }}"
{% endfor %}
ExecStart={{ app_root }}/venv/bin/gunicorn \
    --workers {{ gunicorn_workers | default(ansible_processor_vcpus * 2 + 1) }} \
    --bind 0.0.0.0:{{ app_port | default(8080) }} \
    --timeout {{ gunicorn_timeout | default(120) }} \
    {{ app_module }}:app
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## Template: /etc/hosts File

```jinja
{# templates/hosts.j2 #}
# Managed by Ansible
127.0.0.1   localhost
::1         localhost ip6-localhost ip6-loopback

# Cluster hosts
{% for host in groups['all'] %}
{{ hostvars[host]['ansible_host'] | default(hostvars[host]['ansible_default_ipv4']['address']) }}   {{ host }} {{ hostvars[host]['ansible_fqdn'] | default(host + '.' + domain) }}
{% endfor %}

# Service aliases
{% if groups['webservers'] is defined %}
{% for host in groups['webservers'] %}
{{ hostvars[host]['ansible_host'] }}   web{{ loop.index }}.{{ domain }}
{% endfor %}
{% endif %}

{% if groups['dbservers'] is defined %}
{% for host in groups['dbservers'] %}
{{ hostvars[host]['ansible_host'] }}   db{{ loop.index }}.{{ domain }}
{% endfor %}
{% endif %}
```

---

## Jinja2 Whitespace Control

```jinja
{# By default, Jinja2 preserves whitespace #}
{# Use - to strip whitespace #}

{# This leaves blank lines: #}
{% if ssl_enabled %}
listen 443 ssl;
{% endif %}

{# This removes blank lines: #}
{%- if ssl_enabled %}
listen 443 ssl;
{%- endif %}

{# Control in ansible.cfg: #}
{# [defaults]
   jinja2_extensions = jinja2.ext.loopcontrols #}

{# Or in template header: #}
#jinja2: trim_blocks:True, lstrip_blocks:True
```

---

## Jinja2 Macros (Reusable Blocks)

```jinja
{# Define a macro #}
{% macro server_block(name, port, root) %}
server {
    listen {{ port }};
    server_name {{ name }};
    root {{ root }};

    location / {
        try_files $uri $uri/ =404;
    }
}
{% endmacro %}

{# Use the macro #}
{{ server_block('app.example.com', 80, '/var/www/app') }}
{{ server_block('api.example.com', 80, '/var/www/api') }}

{# Macro with default values #}
{% macro firewall_rule(port, protocol='tcp', action='accept') %}
-A INPUT -p {{ protocol }} --dport {{ port }} -j {{ action | upper }}
{% endmacro %}

{{ firewall_rule(22) }}
{{ firewall_rule(80) }}
{{ firewall_rule(53, 'udp') }}
```

---

## Template Testing

```bash
# Validate a template renders correctly
ansible all -m template \
    -a "src=templates/nginx.conf.j2 dest=/tmp/nginx_test.conf" \
    --check --diff

# Use ansible-console for interactive testing
ansible-console webservers
> template src=templates/app.conf.j2 dest=/tmp/test.conf

# Test Jinja2 expressions locally
python3 -c "
from jinja2 import Template
t = Template('Hello {{ name }}!')
print(t.render(name='World'))
"
```

---

## Variables and Templates Best Practices

- Use `default()` filter to handle undefined variables
- Keep templates simple; complex logic belongs in playbooks
- Always add a header comment: "Managed by Ansible"
- Use `validate` parameter to check config before deploying
- Test templates in check mode before applying
- Use `backup: yes` to keep previous versions
- Avoid deeply nested variable structures when possible
- Document required variables in role README or defaults
- Use `ansible-lint` to catch template issues
