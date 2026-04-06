# Testing with Molecule

## Topics Covered
- Why test `Ansible` code
- Testing pyramid for infrastructure
- `Molecule` framework overview
- Writing and running tests
- Testing with Docker containers
- Verifiers: `Ansible`, `testinfra`
- CI integration for role testing

---

## Why Test Ansible Code?

- Playbooks are code and should be tested like code
- Catch errors before they reach production
- Validate idempotency (running twice produces same result)
- Ensure roles work across different OS versions
- Enable confident refactoring
- Required for shared roles on `Ansible Galaxy`

---

## Testing Pyramid for Infrastructure

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="350" font-family="sans-serif">
<polygon points="30,220 590,220 634,340 -14,340" fill="#e3f2fd" stroke="#999" stroke-width="1"/>
<text x="310" y="285" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">Unit Tests (module tests, filter tests)</text>
<polygon points="80,130 539,130 575,220 44,220" fill="#e8f5e9" stroke="#999" stroke-width="1"/>
<text x="310" y="180" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">Linting & Syntax (ansible-lint, yamllint)</text>
<polygon points="131,60 489,60 517,130 103,130" fill="#fff3e0" stroke="#999" stroke-width="1"/>
<text x="310" y="100" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">Functional Tests (Molecule + verifier)</text>
<polygon points="181,10 438,10 458,60 161,60" fill="#fce4ec" stroke="#999" stroke-width="1"/>
<text x="310" y="40" font-size="12" font-weight="bold" fill="#333" text-anchor="middle">Integration Tests (full stack, multi-host)</text>
</svg>

---

## Testing Tools Overview

| Tool | Purpose |
|------|---------|
| `yamllint` | `YAML` syntax validation |
| `ansible-lint` | `Ansible` best practices |
| `ansible-playbook --syntax-check` | Playbook syntax |
| `ansible-playbook --check` | Dry run |
| `Molecule` | Full role testing framework |
| `testinfra` | Python-based infrastructure tests |
| `Vagrant` | VM-based testing |
| `Docker` | Container-based testing |

---

## Installing Molecule

```bash
# Install Molecule with Docker driver
pip install molecule molecule-plugins[docker]

# Or with Vagrant driver
pip install molecule molecule-vagrant

# Or with Podman
pip install molecule molecule-plugins[podman]

# Verify installation
molecule --version
```

---

## Initializing Molecule for a Role

```bash
# Create a new role with Molecule
molecule init role my_role --driver-name docker

# Add Molecule to an existing role
cd roles/nginx
molecule init scenario --driver-name docker

# Result:
roles/nginx/
├── defaults/
├── handlers/
├── meta/
├── molecule/
│   └── default/
│       ├── converge.yml
│       ├── molecule.yml
│       └── verify.yml
├── tasks/
├── templates/
└── vars/
```

---

## Molecule Configuration

```yaml
# molecule/default/molecule.yml
---
dependency:
  name: galaxy
  options:
    requirements-file: requirements.yml

driver:
  name: docker

platforms:
  - name: ubuntu-22
    image: ubuntu:22.04
    pre_build_image: true
    command: /sbin/init
    tmpfs:
      - /run
      - /tmp
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:rw
    privileged: true

  - name: debian-12
    image: debian:12
    pre_build_image: true
    command: /sbin/init
    privileged: true

provisioner:
  name: ansible
  config_options:
    defaults:
      callbacks_enabled: profile_tasks

verifier:
  name: ansible
```

---

## Converge Playbook

```yaml
# molecule/default/converge.yml
---
- name: Converge
  hosts: all
  become: true

  vars:
    nginx_vhosts:
      - server_name: test.example.com
        document_root: /var/www/test
        port: 80

  pre_tasks:
    - name: Update apt cache (Debian)
      apt:
        update_cache: yes
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"

  roles:
    - role: nginx
```

---

## Verify Playbook (Ansible Verifier)

```yaml
# molecule/default/verify.yml
---
- name: Verify
  hosts: all
  become: true

  tasks:
    - name: Verify nginx is installed
      command: nginx -v
      register: nginx_version
      changed_when: false

    - name: Assert nginx is installed
      assert:
        that:
          - nginx_version.rc == 0

    - name: Verify nginx is running
      service_facts:

    - name: Assert nginx service is running
      assert:
        that:
          - "'nginx' in ansible_facts.services"
          - "ansible_facts.services['nginx'].state == 'running'"

    - name: Verify nginx responds on port 80
      uri:
        url: http://localhost:80
        return_content: yes
      register: http_response

    - name: Assert HTTP response
      assert:
        that:
          - http_response.status == 200

    - name: Verify config file exists
      stat:
        path: /etc/nginx/nginx.conf
      register: config_file

    - name: Assert config file
      assert:
        that:
          - config_file.stat.exists
          - config_file.stat.mode == '0644'
```

---

## Molecule Commands

```bash
# Full test lifecycle
molecule test

# Individual steps:
molecule create      # Create test instances
molecule converge    # Run the role
molecule idempotence # Run again, check for changes
molecule verify      # Run verification tests
molecule destroy     # Tear down instances

# Interactive development:
molecule converge    # Apply role
molecule login       # SSH into test instance
molecule verify      # Check results
molecule converge    # Apply changes
molecule destroy     # Clean up

# List instances
molecule list
```

---

## Molecule Test Sequence

```misc
molecule test runs these steps in order:

1. dependency     - Install role dependencies
2. lint          - Run linters (yamllint, ansible-lint)
3. cleanup       - Clean up from previous runs
4. destroy       - Remove existing instances
5. syntax        - Syntax check
6. create        - Create test instances
7. prepare       - Prepare instances (pre-requisites)
8. converge      - Run the role
9. idempotence   - Run again (verify no changes)
10. side_effect  - Run side effect playbook
11. verify       - Run verification tests
12. cleanup      - Clean up
13. destroy      - Remove instances
```

---

## Testing with testinfra

```python
# molecule/default/tests/test_nginx.py
"""Tests for nginx role."""
import testinfra

def test_nginx_is_installed(host):
    """Verify nginx package is installed."""
    nginx = host.package("nginx")
    assert nginx.is_installed

def test_nginx_is_running(host):
    """Verify nginx service is running and enabled."""
    nginx = host.service("nginx")
    assert nginx.is_running
    assert nginx.is_enabled

def test_nginx_config(host):
    """Verify nginx configuration file."""
    config = host.file("/etc/nginx/nginx.conf")
    assert config.exists
    assert config.user == "root"
    assert config.mode == 0o644
    assert config.contains("worker_processes")

def test_nginx_port(host):
    """Verify nginx is listening on port 80."""
    socket = host.socket("tcp://0.0.0.0:80")
    assert socket.is_listening

def test_vhost_config(host):
    """Verify virtual host is configured."""
    vhost = host.file("/etc/nginx/sites-enabled/test.example.com.conf")
    assert vhost.exists
    assert vhost.contains("server_name test.example.com")
```

---

## testinfra Configuration

```yaml
# molecule/default/molecule.yml
---
verifier:
  name: testinfra
  options:
    v: true
    sudo: true
  additional_files_or_dirs:
    - ../shared/tests/
  env:
    PYTHONDONTWRITEBYTECODE: "1"
```

```bash
# Run testinfra manually
molecule verify

# Or directly
py.test --connection=ansible \
    --ansible-inventory=molecule/default/inventory \
    molecule/default/tests/
```

---

## Multiple Test Scenarios

```tree
roles/nginx/
└── molecule/
    ├── default/               # Default scenario
    │   ├── molecule.yml
    │   ├── converge.yml
    │   └── verify.yml
    ├── ssl/                   # SSL-specific tests
    │   ├── molecule.yml
    │   ├── converge.yml       # Tests with SSL vars
    │   └── verify.yml
    └── multi-platform/        # Cross-platform tests
        ├── molecule.yml       # Ubuntu + RHEL + Debian
        ├── converge.yml
        └── verify.yml
```

```bash
# Run specific scenario
molecule test -s ssl
molecule test -s multi-platform

# Run default scenario
molecule test
```

---

## Prepare Playbook

```yaml
# molecule/default/prepare.yml
# Run BEFORE the role to set up prerequisites
---
- name: Prepare
  hosts: all
  become: true

  tasks:
    - name: Install Python (for raw bootstrapping)
      raw: apt-get update && apt-get install -y python3
      changed_when: false
      when: ansible_os_family == "Debian"

    - name: Create required directories
      file:
        path: "{{ item }}"
        state: directory
      loop:
        - /etc/ssl/certs
        - /var/www

    - name: Install test SSL certificate
      copy:
        content: |
          -----BEGIN CERTIFICATE-----
          MIITest...
          -----END CERTIFICATE-----
        dest: /etc/ssl/certs/test.pem
```

---

## Side Effect Playbook

```yaml
# molecule/default/side_effect.yml
# Run AFTER converge to test additional scenarios
---
- name: Side Effect - Simulate failure recovery
  hosts: all
  become: true

  tasks:
    - name: Stop nginx to simulate failure
      service:
        name: nginx
        state: stopped

    - name: Corrupt config to test recovery
      copy:
        content: "invalid config"
        dest: /etc/nginx/nginx.conf
```

---

## CI Integration: GitHub Actions

```yaml
# .github/workflows/molecule.yml
---
name: Molecule Test
on:
  push:
    branches: [main]
  pull_request:

jobs:
  molecule:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        distro:
          - ubuntu2204
          - debian12
          - rockylinux9

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install ansible molecule molecule-plugins[docker]

      - name: Run Molecule tests
        run: molecule test
        env:
          MOLECULE_DISTRO: ${{ matrix.distro }}
```

---

## CI Integration: GitLab CI

```yaml
# .gitlab-ci.yml
---
stages:
  - lint
  - test

lint:
  stage: lint
  image: python:3.11
  script:
    - pip install yamllint ansible-lint
    - yamllint .
    - ansible-lint

molecule:
  stage: test
  image: docker:latest
  services:
    - docker:dind
  variables:
    DOCKER_HOST: tcp://docker:2375
  before_script:
    - apk add python3 py3-pip gcc musl-dev python3-dev libffi-dev
    - pip install ansible molecule molecule-plugins[docker]
  script:
    - molecule test
```

---

## Testing Best Practices

- Test every role with `Molecule`
- Test on multiple OS platforms
- Verify idempotency (run converge twice)
- Use `testinfra` for thorough verification
- Test with different variable combinations
- Include `Molecule` tests in CI/CD pipeline
- Keep tests fast (use containers over VMs)
- Test error scenarios with side_effect playbooks
- Use `prepare` for prerequisites, not in the role itself
- Pin dependency versions for reproducibility

---

## Exercise: Molecule Lab

1. Create a new role with `molecule init`
1. Write the role tasks (install nginx, deploy config)
1. Write verify tests (package installed, service running)
1. Run the full `molecule test` cycle
1. Add a second platform (Debian + Ubuntu)
1. Add `testinfra` tests for port and config validation
1. Fix any idempotency issues
