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

# Dynamic Inventory

## Topics Covered
- Why dynamic inventory
- Inventory plugins vs scripts
- AWS EC2 dynamic inventory
- Azure dynamic inventory
- GCP dynamic inventory
- Custom inventory scripts
- Caching and performance

---

## Why Dynamic Inventory?

- Cloud environments have hosts that come and go
- Manually maintaining static inventory is error-prone
- Auto-scaling groups change instance counts
- Container orchestration creates/destroys instances
- Dynamic inventory queries cloud APIs at runtime
- Always reflects the current state of infrastructure

---

## Static vs Dynamic Inventory

![static_vs_dynamic_inventory](svg/courses/devops/ansible/11_dynamic_inventory/static_vs_dynamic_inventory.svg)

---

## Inventory Plugins vs Scripts

```misc
Inventory Plugins (recommended):
  - Written in Python
  - Configured via YAML
  - Support caching natively
  - Part of Ansible collections
  - Enabled via ansible.cfg

Inventory Scripts (legacy):
  - Executable scripts in any language
  - Must output JSON on stdout
  - --list returns all hosts
  - --host <hostname> returns host vars
  - Still supported but deprecated
```

---

## Enabling Inventory Plugins

```ini
# ansible.cfg
[inventory]
enable_plugins = amazon.aws.aws_ec2, azure.azcollection.azure_rm, google.cloud.gcp_compute, auto, host_list, yaml, ini

# Plugin config files must end with specific suffixes:
# AWS:   .aws_ec2.yml or .aws_ec2.yaml
# Azure: .azure_rm.yml or .azure_rm.yaml
# GCP:   .gcp.yml or .gcp.yaml
```

---

## AWS EC2 Dynamic Inventory

```yaml
# inventory/aws_ec2.yml

---
plugin: amazon.aws.aws_ec2

# AWS credentials (or use env vars / IAM role)
aws_access_key_id: "{{ lookup('env', 'AWS_ACCESS_KEY_ID') }}"
aws_secret_access_key: "{{ lookup('env', 'AWS_SECRET_ACCESS_KEY') }}"

regions:
  - us-east-1
  - eu-west-1

# Filter instances
filters:
  instance-state-name: running
  "tag:Environment": production

# Group instances by tags
keyed_groups:
  - key: tags.Environment
    prefix: env
    separator: "_"
  - key: tags.Role
    prefix: role
    separator: "_"
  - key: placement.region
    prefix: region
    separator: "_"
  - key: instance_type
    prefix: type
    separator: "_"

# Set host variables
compose:
  ansible_host: public_ip_address
  ansible_user: "'ec2-user'"
```

---

## AWS EC2 Inventory: Advanced Filters

```yaml
# inventory/aws_ec2.yml

---
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1

filters:
  instance-state-name: running
  "tag:ManagedBy": ansible
  "tag:Environment":
    - production
    - staging

# Complex grouping
keyed_groups:
  - key: tags.Role | default('untagged')
    prefix: role
  - key: tags.Environment | default('unknown')
    prefix: env
  - key: platform_details | regex_search('Linux')
    prefix: os
    value: linux

# Conditional host variables
compose:
  ansible_host: public_ip_address | default(private_ip_address)
  ansible_user: "'ubuntu' if image_id.startswith('ami-ubuntu') else 'ec2-user'"
  environment: tags.Environment | default('unknown')

# Hostnames
hostnames:
  - tag:Name
  - dns-name
  - private-ip-address
```

---

## Testing AWS Dynamic Inventory

```bash
# Install the AWS collection
ansible-galaxy collection install amazon.aws

# Install boto3
pip install boto3 botocore

# Test the inventory plugin
ansible-inventory -i inventory/aws_ec2.yml --graph

# Example output:
# @all:
#   |--@env_production:
#   |  |--web-prod-01
#   |  |--web-prod-02
#   |  |--db-prod-01
#   |--@env_staging:
#   |  |--web-staging-01
#   |--@role_webserver:
#   |  |--web-prod-01
#   |  |--web-prod-02
#   |  |--web-staging-01
#   |--@role_database:
#   |  |--db-prod-01

# List host variables
ansible-inventory -i inventory/aws_ec2.yml --host web-prod-01

# Ping discovered hosts
ansible -i inventory/aws_ec2.yml all -m ping
```

---

## Azure Dynamic Inventory

```yaml
# inventory/azure_rm.yml

---
plugin: azure.azcollection.azure_rm

# Authentication (or use env vars)
auth_source: auto  # Uses env vars or managed identity

# Include specific resource groups
include_vm_resource_groups:
  - production-rg
  - staging-rg

# Grouping
keyed_groups:
  - prefix: tag
    key: tags
  - prefix: location
    key: location
  - prefix: os
    key: os_profile.system
    separator: "_"

# Conditional groups
conditional_groups:
  linux: os_profile.system == 'linux'
  windows: os_profile.system == 'windows'

# Host variables
compose:
  ansible_host: public_ip_address | default(private_ip_address)
  ansible_user: os_profile.admin_username
```

---

## GCP Dynamic Inventory

```yaml
# inventory/gcp_compute.yml

---
plugin: google.cloud.gcp_compute

# Authentication
auth_kind: serviceaccount
service_account_file: /path/to/service-account.json

# Projects and zones
projects:
  - my-gcp-project

zones:
  - us-central1-a
  - us-east1-b

# Filters
filters:
  - status = RUNNING
  - labels.managed-by = ansible

# Grouping
keyed_groups:
  - key: labels.environment
    prefix: env
  - key: labels.role
    prefix: role
  - key: zone
    prefix: zone

compose:
  ansible_host: networkInterfaces[0].accessConfigs[0].natIP | default(networkInterfaces[0].networkIP)
```

---

## Custom Inventory Script

```python
#!/usr/bin/env python3
"""Custom dynamic inventory script."""
import json
import argparse
import requests

def get_inventory():
    """Query CMDB or API for host information."""
    # Example: query an internal API
    response = requests.get("https://cmdb.example.com/api/hosts")
    hosts = response.json()

    inventory = {
        "_meta": {"hostvars": {}},
        "all": {"children": ["webservers", "dbservers"]},
        "webservers": {"hosts": []},
        "dbservers": {"hosts": []},
    }

    for host in hosts:
        group = host["role"] + "s"
        if group in inventory:
            inventory[group]["hosts"].append(host["name"])
        inventory["_meta"]["hostvars"][host["name"]] = {
            "ansible_host": host["ip"],
            "ansible_user": host.get("ssh_user", "ansible"),
            "env": host.get("environment", "unknown"),
        }

    return inventory
```

---

## Custom Inventory Script: CLI Entry Point

```python
def get_host(hostname):
    """Get variables for a specific host."""
    inventory = get_inventory()
    return inventory["_meta"]["hostvars"].get(hostname, {})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--host")
    args = parser.parse_args()

    if args.list:
        print(json.dumps(get_inventory(), indent=2))
    elif args.host:
        print(json.dumps(get_host(args.host), indent=2))
```

---

## Using Custom Inventory Scripts

```bash
# Make the script executable
chmod +x inventory/custom_inventory.py

# Test the script
./inventory/custom_inventory.py --list
./inventory/custom_inventory.py --host web01

# Use with ansible
ansible -i inventory/custom_inventory.py all -m ping

# Use in playbook
ansible-playbook -i inventory/custom_inventory.py site.yml
```

---

## Inventory Caching

```yaml
# In inventory plugin config
# inventory/aws_ec2.yml

---
plugin: amazon.aws.aws_ec2
cache: true
cache_plugin: jsonfile
cache_timeout: 3600        # Cache for 1 hour
cache_connection: /tmp/ansible_inventory_cache
cache_prefix: aws_ec2

# Or in ansible.cfg
# [inventory]
# cache = true
# cache_plugin = jsonfile
# cache_timeout = 3600
# cache_connection = /tmp/ansible_inventory
```

```bash
# Clear the cache
ansible-inventory -i inventory/aws_ec2.yml --flush-cache

# Refresh inventory
ansible-inventory -i inventory/aws_ec2.yml --list --refresh-cache
```

---

## Combining Static and Dynamic Inventory

```tree
inventory/
├── static_hosts.yml       # Static hosts (on-prem)
├── aws_ec2.yml           # AWS dynamic inventory
├── azure_rm.yml          # Azure dynamic inventory
├── group_vars/
│   ├── all.yml
│   ├── webservers.yml
│   └── dbservers.yml
└── host_vars/
    └── bastion.yml
```

```bash
# Point to the directory; Ansible merges all sources
ansible-playbook -i inventory/ site.yml
```

---

## Constructed Inventory Plugin

```yaml
# inventory/constructed.yml

---
plugin: constructed
strict: false

# Create groups from existing variables
groups:
  # Group by environment
  production: env == 'production'
  staging: env == 'staging'

  # Group by memory size
  large_memory: ansible_memtotal_mb >= 8192
  small_memory: ansible_memtotal_mb < 8192

  # Complex grouping
  prod_webservers: env == 'production' and 'webservers' in group_names

# Add computed variables
compose:
  display_name: inventory_hostname ~ ' (' ~ ansible_host ~ ')'
  is_large: ansible_memtotal_mb >= 8192

keyed_groups:
  - key: ansible_os_family
    prefix: os
```

---

## Dynamic Inventory Best Practices

- Use inventory plugins over legacy scripts
- Enable caching for cloud inventory (reduce API calls)
- Use filters to limit scope (don't discover everything)
- Tag cloud resources consistently for clean grouping
- Combine static and dynamic inventory when needed
- Test inventory discovery with `ansible-inventory --graph`
- Use `compose` to set `ansible_host` and `ansible_user`
- Handle hosts without public IPs (use bastion/jump host)
- Document required credentials and permissions

---

## Exercise: Dynamic Inventory Lab

1. Set up AWS/Azure/GCP dynamic inventory (or mock with script)
1. Configure keyed groups based on tags
1. Set `ansible_host` using `compose`
1. Enable caching and test cache behavior
1. Combine with a static inventory file
1. Run a playbook against dynamically discovered hosts

---

## Cloud Provider Plugins

![cloud_provider_plugins](svg/courses/devops/ansible/11_dynamic_inventory/cloud_provider_plugins.svg)
