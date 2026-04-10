# Custom Modules and Plugins

## Topics Covered
- When to write custom modules
- Module development in `Python`
- Module argument specification
- Return values and documentation
- Custom filter plugins
- Custom callback plugins
- Testing custom modules

---

## Custom Module Structure

![Custom Module Structure](svg/courses/devops/ansible/12_custom_modules_plugins/custom_module_structure.svg)

---

## When to Write Custom Modules

- No existing module does what you need
- You need to interact with a proprietary API
- Existing modules don't support your specific use case
- You want to encapsulate complex logic into a reusable unit
- You need custom idempotency logic

---

## Module Search Path

```misc
Ansible looks for modules in this order:
1. ./library/                    (next to playbook)
2. Role's library/ directory
3. Collections plugins/modules/
4. ANSIBLE_LIBRARY environment variable
5. Configured module path in ansible.cfg
6. Built-in modules
```

```ini
# ansible.cfg
[defaults]
library = ./library:/usr/share/my_modules
```

---

## Basic Custom Module

```python
#!/usr/bin/env python3
# library/my_module.py
"""A simple custom Ansible module."""

from ansible.module_utils.basic import AnsibleModule

def run_module():
    # Define accepted arguments
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', default='present',
                   choices=['present', 'absent']),
        force=dict(type='bool', default=False),
    )

    # Initialize the module
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Get parameters
    name = module.params['name']
    state = module.params['state']

    result = dict(
        changed=False,
        name=name,
        state=state,
        message=''
    )

    # Check mode: report what would happen
    if module.check_mode:
        module.exit_json(**result)

    # Module logic here
    try:
        if state == 'present':
            # Create/ensure resource exists
            result['changed'] = True
            result['message'] = f'Resource {name} created'
        else:
            # Remove resource
            result['changed'] = True
            result['message'] = f'Resource {name} removed'
    except Exception as e:
        module.fail_json(msg=str(e), **result)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
```

---

## Using Your Custom Module

```yaml
# playbook.yml

---
- name: Test custom module
  hosts: localhost
  connection: local
  tasks:
    - name: Create a resource
      my_module:
        name: my_resource
        state: present
      register: result

    - name: Show result
      debug:
        var: result
```

---

## Module with File Operations

```python
#!/usr/bin/env python3
# library/config_manager.py
"""Manage application configuration files."""

import os
import json
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        path=dict(type='path', required=True),
        settings=dict(type='dict', required=True),
        backup=dict(type='bool', default=True),
        mode=dict(type='str', default='0644'),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    path = module.params['path']
    settings = module.params['settings']
    backup = module.params['backup']

    result = dict(changed=False, path=path)

    # Read existing config
    current_config = {}
    if os.path.exists(path):
        with open(path, 'r') as f:
            current_config = json.load(f)

    # Check if changes are needed
    if current_config == settings:
        module.exit_json(**result)

    result['changed'] = True
    result['diff'] = dict(
        before=json.dumps(current_config, indent=2),
        after=json.dumps(settings, indent=2),
    )

    if module.check_mode:
        module.exit_json(**result)

    # Backup if requested
    if backup and os.path.exists(path):
        module.backup_local(path)

    # Write new config
    with open(path, 'w') as f:
        json.dump(settings, f, indent=2)

    os.chmod(path, int(module.params['mode'], 8))

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
```

---

## Module Documentation (DOCUMENTATION String)

```python
#!/usr/bin/env python3

DOCUMENTATION = r'''

---
module: config_manager
short_description: Manage JSON configuration files
version_added: "1.0.0"
description:
    - Creates and updates JSON configuration files
    - Supports check mode and diff
    - Optionally creates backups

options:
    path:
        description: Path to the configuration file
        required: true
        type: path
    settings:
        description: Dictionary of settings to write
        required: true
        type: dict
    backup:
        description: Create a backup before modifying
        required: false
        default: true
        type: bool

author:
    - DevOps Team (@devops)
'''

EXAMPLES = r'''
- name: Create application config
  config_manager:
    path: /etc/myapp/config.json
    settings:
      database_host: db.example.com
      database_port: 5432
      debug: false

- name: Update config without backup
  config_manager:
    path: /etc/myapp/config.json
    settings:
      debug: true
    backup: false
'''

RETURN = r'''
path:
    description: Path to the configuration file
    type: str
    returned: always
changed:
    description: Whether the file was modified
    type: bool
    returned: always
diff:
    description: Before and after content
    type: dict
    returned: when changed
'''
```

---

## Module with API Interaction

```python
#!/usr/bin/env python3
# library/api_resource.py
"""Manage resources via REST API."""

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
import json

def run_module():
    module_args = dict(
        api_url=dict(type='str', required=True),
        api_token=dict(type='str', required=True, no_log=True),
        name=dict(type='str', required=True),
        state=dict(type='str', default='present',
                   choices=['present', 'absent']),
        properties=dict(type='dict', default={}),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    api_url = module.params['api_url']
    token = module.params['api_token']
    name = module.params['name']
    state = module.params['state']
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    # Check if resource exists
    response, info = fetch_url(
        module,
        f'{api_url}/resources/{name}',
        headers=headers,
        method='GET'
    )

    exists = info['status'] == 200
    result = dict(changed=False, name=name)

    if state == 'present' and not exists:
        result['changed'] = True
        if not module.check_mode:
            body = json.dumps({'name': name, **module.params['properties']})
            response, info = fetch_url(
                module, f'{api_url}/resources',
                headers=headers, method='POST', data=body
            )
            if info['status'] != 201:
                module.fail_json(msg=f"Failed to create: {info['status']}")

    elif state == 'absent' and exists:
        result['changed'] = True
        if not module.check_mode:
            response, info = fetch_url(
                module, f'{api_url}/resources/{name}',
                headers=headers, method='DELETE'
            )

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
```

---

## Custom Filter Plugins

```python
# filter_plugins/custom_filters.py
"""Custom Jinja2 filters for Ansible."""

class FilterModule:
    """Custom filters."""

    def filters(self):
        return {
            'to_cidr': self.to_cidr,
            'normalize_name': self.normalize_name,
            'split_host_port': self.split_host_port,
        }

    @staticmethod
    def to_cidr(ip, prefix=24):
        """Convert IP address to CIDR notation."""
        return f"{ip}/{prefix}"

    @staticmethod
    def normalize_name(name):
        """Normalize a string to be used as hostname."""
        return name.lower().replace(' ', '-').replace('_', '-')

    @staticmethod
    def split_host_port(address, default_port=80):
        """Split host:port string."""
        if ':' in address:
            host, port = address.rsplit(':', 1)
            return {'host': host, 'port': int(port)}
        return {'host': address, 'port': default_port}
```

---

## Using Custom Filters

```yaml
tasks:
  - name: Use custom CIDR filter
    debug:
      msg: "Network: {{ '192.168.1.0' | to_cidr(24) }}"
      # Output: Network: 192.168.1.0/24

  - name: Normalize hostname
    debug:
      msg: "Host: {{ 'My Web Server' | normalize_name }}"
      # Output: Host: my-web-server

  - name: Split host and port
    debug:
      msg: "{{ 'db.example.com:5432' | split_host_port }}"
      # Output: {'host': 'db.example.com', 'port': 5432}
```

---

## Custom Callback Plugins

```python
# callback_plugins/slack_notify.py
"""Send play results to Slack."""

from ansible.plugins.callback import CallbackBase
import json
import urllib.request

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'slack_notify'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super().__init__()
        self.webhook_url = None
        self.results = {}

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super().set_options(task_keys=task_keys, var_options=var_options, direct=direct)
        self.webhook_url = self.get_option('webhook_url')

    def v2_playbook_on_stats(self, stats):
        """Called at the end of a playbook run."""
        hosts = sorted(stats.processed.keys())
        summary = []
        for host in hosts:
            s = stats.summarize(host)
            summary.append(
                f"{host}: ok={s['ok']} changed={s['changed']} "
                f"failures={s['failures']} unreachable={s['unreachable']}"
            )

        message = {
            'text': f"*Ansible Run Complete*\n```\n{'\\n'.join(summary)}\n```"
        }

        if self.webhook_url:
            req = urllib.request.Request(
                self.webhook_url,
                data=json.dumps(message).encode(),
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req)
```

---

## Custom Lookup Plugins

```python
# lookup_plugins/custom_secret.py
"""Lookup plugin to fetch secrets from a custom vault."""

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleError
import requests

class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        results = []
        vault_url = kwargs.get('vault_url', 'https://vault.example.com')
        vault_token = kwargs.get('token', '')

        for term in terms:
            try:
                response = requests.get(
                    f'{vault_url}/v1/secret/data/{term}',
                    headers={'X-Vault-Token': vault_token}
                )
                response.raise_for_status()
                data = response.json()
                results.append(data['data']['data'])
            except Exception as e:
                raise AnsibleError(f"Error fetching secret '{term}': {e}")

        return results
```

```yaml
# Usage in playbook
- name: Get secret
  debug:
    msg: "{{ lookup('custom_secret', 'myapp/db_password', vault_url='https://vault.internal', token=vault_token) }}"
```

---

## Testing Custom Modules

```bash
# Test module directly with Python
python3 library/my_module.py <<EOF
{
    "ANSIBLE_MODULE_ARGS": {
        "name": "test_resource",
        "state": "present"
    }
}
EOF

# Test with ansible ad-hoc
ansible localhost -m my_module \
    -a "name=test state=present" \
    -M ./library

# Test in check mode
ansible localhost -m my_module \
    -a "name=test state=present" \
    -M ./library --check

# Run module unit tests
python3 -m pytest tests/unit/modules/test_my_module.py
```

---

## Module Unit Test Example

```python
# tests/unit/modules/test_my_module.py
import pytest
from unittest.mock import patch, MagicMock
from library.config_manager import run_module

@pytest.fixture
def module_args():
    return {
        'path': '/tmp/test_config.json',
        'settings': {'key': 'value'},
        'backup': False,
        'mode': '0644',
    }

def test_create_new_config(module_args, tmp_path):
    config_path = str(tmp_path / 'config.json')
    module_args['path'] = config_path

    with patch('library.config_manager.AnsibleModule') as mock_module:
        mock_instance = MagicMock()
        mock_instance.params = module_args
        mock_instance.check_mode = False
        mock_module.return_value = mock_instance

        run_module()

        mock_instance.exit_json.assert_called_once()
        call_args = mock_instance.exit_json.call_args
        assert call_args[1]['changed'] is True
```

---

## Plugin Types Summary

| Plugin Type | Location | Purpose |
|-------------|----------|---------|
| Modules | `library/` | Perform actions on hosts |
| Filter | `filter_plugins/` | Transform data in templates |
| Callback | `callback_plugins/` | React to events |
| Lookup | `lookup_plugins/` | Fetch external data |
| Inventory | `inventory_plugins/` | Dynamic host discovery |
| Connection | `connection_plugins/` | Custom transport |
| Vars | `vars_plugins/` | Load variables |
| Action | `action_plugins/` | Modify module behavior |

---

## Best Practices for Custom Modules

- Always support `check_mode`
- Use `no_log` for sensitive parameters
- Return meaningful diff data
- Include DOCUMENTATION, EXAMPLES, and RETURN strings
- Handle exceptions gracefully with `module.fail_json()`
- Make modules idempotent
- Use `AnsibleModule` helper methods
- Write unit tests
- Follow Ansible module development guidelines
