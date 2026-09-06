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

# Inventory Deep Dive

## Topics Covered
- Static inventory patterns and best practices
- Inventory plugins
- Dynamic inventory concepts
- Connection variables
- Inventory testing and validation

---

## Ansible Inventory Architecture

![Ansible Inventory Architecture](svg/courses/devops/ansible/02_inventory_deep_dive/inventory_architecture.svg)

---

## Inventory Sources

![inventory_kinds](svg/courses/devops/ansible/02_inventory_deep_dive/inventory_kinds.svg)

---

## Static Inventory Patterns

```ini
# Production-like inventory structure
[webservers]
web-prod-[01:05]

[webservers:vars]
ansible_port=22
app_env=production

[dbservers]
db-prod-[01:03]

[cache]
redis-[01:02]

[loadbalancers]
lb-[01:02]

[production:children]
webservers
dbservers
cache
loadbalancers
```

---

## Inventory with Connection Parameters

```yaml
# inventory.yml
all:
  hosts:
    jump_host:
      ansible_host: 10.0.0.1
      ansible_user: admin
      ansible_port: 2222
      ansible_ssh_private_key_file: ~/.ssh/jump_key
  children:
    internal:
      vars:
        ansible_ssh_common_args: >-
          -o ProxyJump=admin@10.0.0.1:2222
      hosts:
        app01:
          ansible_host: 172.16.0.10
        app02:
          ansible_host: 172.16.0.11
```

---

## Inventory for Mixed Environments

```yaml
all:
  children:
    linux:
      children:
        ubuntu:
          hosts:
            web01:
              ansible_host: 192.168.1.10
        rhel:
          hosts:
            app01:
              ansible_host: 192.168.1.20
      vars:
        ansible_connection: ssh

    windows:
      hosts:
        win01:
          ansible_host: 192.168.1.30
      vars:
        ansible_connection: winrm
        ansible_winrm_transport: ntlm
        ansible_winrm_server_cert_validation: ignore
```

---

## Inventory Variable Precedence

```misc
(lowest priority)
1. all group vars  (group_vars/all)
2. parent group vars
3. child group vars
4. host vars (host_vars/<host>)
5. play vars
6. play vars_files
7. play vars_prompt
8. task vars
9. role vars
10. block vars
11. extra vars (-e)  <-- highest priority
(highest priority)
```

---

## Organizing Large Inventories

```tree
inventories/
├── production/
│   ├── hosts.yml
│   ├── group_vars/
│   │   ├── all.yml
│   │   ├── webservers.yml
│   │   └── dbservers.yml
│   └── host_vars/
│       ├── web01.yml
│       └── db01.yml
├── staging/
│   ├── hosts.yml
│   ├── group_vars/
│   │   └── all.yml
│   └── host_vars/
└── development/
    ├── hosts.yml
    └── group_vars/
        └── all.yml
```

---

## Environment-Specific Variables

```yaml
# inventories/production/group_vars/all.yml

---
env: production
dns_servers:
  - 10.0.1.53
  - 10.0.2.53
ntp_server: ntp.prod.example.com
log_level: warn
backup_enabled: true
monitoring_endpoint: https://monitor.prod.example.com

# inventories/staging/group_vars/all.yml

---
env: staging
dns_servers:
  - 10.1.1.53
ntp_server: ntp.staging.example.com
log_level: info
backup_enabled: false
monitoring_endpoint: https://monitor.staging.example.com
```

---

## Inventory Patterns in Commands

```bash
# All hosts
ansible all -m ping

# Specific group
ansible webservers -m ping

# Multiple groups (union)
ansible 'webservers:dbservers' -m ping

# Intersection (hosts in BOTH groups)
ansible 'webservers:&production' -m ping

# Exclusion (webservers but NOT web01)
ansible 'webservers:!web01' -m ping

# Regex pattern
ansible '~web\d+' -m ping

# Combine patterns
ansible 'webservers:&production:!web01' -m ping

# First host in group
ansible 'webservers[0]' -m ping
```

---

## Inventory Aliases and Special Variables

```ini
# Aliases
jumper ansible_host=192.168.1.50 ansible_port=5555

# Special connection variables
[all:vars]
ansible_connection=ssh          # or local, docker, winrm
ansible_ssh_private_key_file=~/.ssh/mykey
ansible_become=true
ansible_become_method=sudo      # or su, pbrun, pfexec
ansible_python_interpreter=/usr/bin/python3
ansible_shell_type=bash
```

---

## Validating Inventory

```bash
# List all hosts in JSON format
ansible-inventory -i inventory --list

# Display a graph of the inventory
ansible-inventory -i inventory --graph

# Show vars for a specific host
ansible-inventory -i inventory --host web01

# Export inventory
ansible-inventory -i inventory --list --export

# Check a YAML inventory for syntax errors
ansible-inventory -i inventory.yml --list > /dev/null

# Count hosts per group
ansible-inventory -i inventory --graph | grep -c '|--'
```

---

## Inventory Best Practices

- Use `YAML` format for complex inventories
- Separate inventories per environment (prod, staging, dev)
- Use `group_vars/` and `host_vars/` directories
- Keep secrets in `Ansible Vault` encrypted files
- Use meaningful group names that reflect function
- Document your inventory structure
- Version control your inventory files
- Use dynamic inventory for cloud environments
- Validate inventory before running playbooks

---

## Inventory Groups and Hosts

![inventory_groups_and_hosts](svg/courses/devops/ansible/02_inventory_deep_dive/inventory_groups_and_hosts.svg)

---

## Inventory Variable Files

![inventory_variable_files](svg/courses/devops/ansible/02_inventory_deep_dive/inventory_variable_files.svg)
