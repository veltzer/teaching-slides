# CI/CD Integration

## Topics Covered
- `Ansible` in CI/CD pipelines
- GitHub Actions integration
- GitLab CI/CD integration
- Jenkins integration
- Deployment strategies
- Blue/green and canary deployments
- Infrastructure as Code workflow

---

## Ansible in CI/CD Pipelines

![ansible_in_ci_cd_pipelines](svg/courses/devops/ansible/16_cicd_integration/ansible_in_ci_cd_pipelines.svg)

---

## GitHub Actions: Full Pipeline

```yaml
# .github/workflows/deploy.yml

---
name: Deploy Application
on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Target environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install linters
        run: pip install ansible-lint yamllint
      - name: Run yamllint
        run: yamllint .
      - name: Run ansible-lint
        run: ansible-lint

  deploy:
    needs: lint
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment || 'staging' }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Ansible
        run: pip install ansible boto3

      - name: Configure SSH key
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          ssh-keyscan -H ${{ secrets.BASTION_HOST }} >> ~/.ssh/known_hosts

      - name: Install Ansible collections
        run: ansible-galaxy install -r requirements.yml

      - name: Run playbook
        run: |
          ansible-playbook \
            -i inventories/${{ github.event.inputs.environment || 'staging' }} \
            playbooks/deploy.yml \
            -e "app_version=${{ github.sha }}"
        env:
          ANSIBLE_VAULT_PASSWORD: ${{ secrets.VAULT_PASSWORD }}
          ANSIBLE_HOST_KEY_CHECKING: "false"
```

---

## GitLab CI/CD Pipeline

```yaml
# .gitlab-ci.yml

---
stages:
  - lint
  - test
  - deploy-staging
  - deploy-production

variables:
  ANSIBLE_CONFIG: ./ansible.cfg
  ANSIBLE_FORCE_COLOR: "true"

lint:
  stage: lint
  image: python:3.11-slim
  script:
    - pip install ansible-lint yamllint
    - yamllint -c .yamllint .
    - ansible-lint
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

test:
  stage: test
  image: python:3.11
  services:
    - docker:dind
  script:
    - pip install ansible molecule molecule-plugins[docker]
    - molecule test
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

deploy-staging:
  stage: deploy-staging
  image: python:3.11-slim
  before_script:
    - pip install ansible boto3
    - ansible-galaxy install -r requirements.yml
    - mkdir -p ~/.ssh
    - echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_ed25519
    - chmod 600 ~/.ssh/id_ed25519
  script:
    - >
      ansible-playbook
      -i inventories/staging
      playbooks/deploy.yml
      -e "app_version=${CI_COMMIT_SHA}"
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  stage: deploy-production
  image: python:3.11-slim
  before_script:
    - pip install ansible boto3
    - ansible-galaxy install -r requirements.yml
    - mkdir -p ~/.ssh
    - echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_ed25519
    - chmod 600 ~/.ssh/id_ed25519
  script:
    - >
      ansible-playbook
      -i inventories/production
      playbooks/deploy.yml
      -e "app_version=${CI_COMMIT_SHA}"
  environment:
    name: production
    url: https://app.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

---

## Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any

    environment {
        ANSIBLE_VAULT_PASSWORD = credentials('ansible-vault-password')
        SSH_KEY = credentials('ansible-ssh-key')
    }

    stages {
        stage('Lint') {
            steps {
                sh '''
                    pip install ansible-lint yamllint
                    yamllint .
                    ansible-lint
                '''
            }
        }

        stage('Deploy Staging') {
            steps {
                sh '''
                    pip install ansible
                    ansible-galaxy install -r requirements.yml
                    ansible-playbook \
                        -i inventories/staging \
                        playbooks/deploy.yml \
                        -e "app_version=${GIT_COMMIT}" \
                        --vault-password-file <(echo $ANSIBLE_VAULT_PASSWORD)
                '''
            }
        }

        stage('Deploy Production') {
            input {
                message "Deploy to production?"
                ok "Deploy"
            }
            steps {
                sh '''
                    ansible-playbook \
                        -i inventories/production \
                        playbooks/deploy.yml \
                        -e "app_version=${GIT_COMMIT}"
                '''
            }
        }
    }

    post {
        failure {
            slackSend color: 'danger',
                message: "Deployment failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
        success {
            slackSend color: 'good',
                message: "Deployment succeeded: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}
```

---

## Deployment Playbook Pattern

```yaml
# playbooks/deploy.yml

---
- name: Pre-deployment checks
  hosts: webservers
  gather_facts: true
  tasks:
    - name: Verify disk space
      assert:
        that: ansible_mounts | selectattr('mount', 'equalto', '/') | map(attribute='size_available') | first > 1073741824
        fail_msg: "Less than 1GB free disk space"
      tags: preflight

- name: Deploy application
  hosts: webservers
  become: true
  serial: "25%"
  max_fail_percentage: 10

  pre_tasks:
    - name: Remove from load balancer
      uri:
        url: "{{ lb_api }}/backends/{{ inventory_hostname }}/disable"
        method: POST
        headers:
          Authorization: "Bearer {{ lb_token }}"
      delegate_to: localhost
      tags: lb

    - name: Wait for connections to drain
      wait_for:
        timeout: 30
      tags: lb

  roles:
    - role: deploy
      vars:
        deploy_version: "{{ app_version }}"

  post_tasks:
    - name: Wait for application health
      uri:
        url: "http://{{ inventory_hostname }}:{{ app_port }}/health"
        return_content: yes
      register: health
      until: health.status == 200
      retries: 30
      delay: 5
      delegate_to: localhost

    - name: Add back to load balancer
      uri:
        url: "{{ lb_api }}/backends/{{ inventory_hostname }}/enable"
        method: POST
        headers:
          Authorization: "Bearer {{ lb_token }}"
      delegate_to: localhost
      tags: lb
```

---

## Blue/Green Deployment

```yaml
# playbooks/blue_green_deploy.yml

---
- name: Blue/Green Deployment
  hosts: localhost
  vars:
    active_color: "{{ lookup('file', '/opt/lb/active_color') | trim }}"
    inactive_color: "{{ 'green' if active_color == 'blue' else 'blue' }}"

  tasks:
    - name: Deploy to inactive environment
      include_tasks: tasks/deploy_to_env.yml
      vars:
        target_group: "{{ inactive_color }}_servers"
        deploy_version: "{{ app_version }}"

    - name: Run smoke tests on inactive
      uri:
        url: "http://{{ inactive_color }}.internal:8080/health"
      register: smoke_test
      until: smoke_test.status == 200
      retries: 10
      delay: 5

    - name: Switch traffic to new environment
      template:
        src: lb-config.j2
        dest: /etc/lb/backends.conf
      vars:
        active_backend: "{{ inactive_color }}"
      notify: reload lb

    - name: Update active color marker
      copy:
        content: "{{ inactive_color }}"
        dest: /opt/lb/active_color

    - name: Verify new active environment
      uri:
        url: http://app.example.com/health
      register: final_check
      until: final_check.status == 200
      retries: 10
      delay: 5
```

---

## Canary Deployment

```yaml
# playbooks/canary_deploy.yml

---
- name: Canary Deployment
  hosts: webservers
  become: true
  serial:
    - 1       # Deploy to 1 canary host first
    - "100%"  # Then deploy to all remaining

  tasks:
    - name: Deploy new version
      git:
        repo: "{{ app_repo }}"
        dest: /opt/myapp
        version: "v{{ app_version }}"

    - name: Restart application
      service:
        name: myapp
        state: restarted

    - name: Wait for health check
      uri:
        url: http://localhost:8080/health
      register: health
      until: health.status == 200
      retries: 30
      delay: 5

    # After canary host, pause for manual verification
    - name: Pause for canary verification
      pause:
        prompt: |
          Canary deployed to {{ inventory_hostname }}.
          Check metrics at https://grafana.example.com/canary
          Press ENTER to continue or Ctrl+C to abort.
      when: ansible_play_hosts.index(inventory_hostname) == 0
      run_once: true
```

---

## Infrastructure as Code Workflow

```misc
Developer Workflow:
1. Create feature branch
2. Edit playbooks/roles
3. Run ansible-lint locally
4. Run molecule test locally
5. Push branch, create PR
6. CI runs lint + molecule
7. Code review
8. Merge to main
9. CI deploys to staging
10. Manual approval
11. CI deploys to production
```

---

## Ansible Pull Model

```bash
# Instead of pushing, hosts pull their own config
# Useful for auto-scaling and large fleets

# On each managed node:
ansible-pull \
    -U https://github.com/myorg/ansible-config.git \
    -i localhost, \
    --checkout main \
    local.yml

# Set up as a cron job
- name: Set up ansible-pull
  cron:
    name: "Ansible pull"
    minute: "*/15"
    job: >
      ansible-pull
      -U https://github.com/myorg/ansible-config.git
      -i localhost,
      local.yml
      >> /var/log/ansible-pull.log 2>&1
```

---

## Secrets in CI/CD

```yaml
# Best practices for secrets in pipelines:

# 1. Never store vault passwords in repo
# 2. Use CI/CD secret variables
# 3. Pass vault password via environment

# GitHub Actions:
- name: Run playbook
  run: ansible-playbook site.yml
  env:
    ANSIBLE_VAULT_PASSWORD_FILE: <(echo "${{ secrets.VAULT_PASS }}")

# GitLab CI:
# Store VAULT_PASSWORD in CI/CD variables (masked)
script:
  - echo "$VAULT_PASSWORD" > .vault_pass
  - ansible-playbook --vault-password-file .vault_pass site.yml
  - rm -f .vault_pass

# Or use a script:
# vault_pass.sh
#!/bin/bash
echo "$ANSIBLE_VAULT_PASSWORD"
```

---

## Deployment Notifications

```yaml
# roles/deploy/tasks/notify.yml

---
- name: Notify Slack on deployment
  uri:
    url: "{{ slack_webhook }}"
    method: POST
    body:
      text: |
        *Deployment {{ 'completed' if not deploy_failed else 'FAILED' }}*
        :rocket: App: `{{ app_name }}`
        :label: Version: `{{ app_version }}`
        :globe_with_meridians: Environment: `{{ env }}`
        :bust_in_silhouette: Triggered by: `{{ lookup('env', 'USER') }}`
        :clock: Time: `{{ ansible_date_time.iso8601 }}`
    body_format: json
  delegate_to: localhost
  run_once: true
  ignore_errors: true

- name: Create GitHub deployment status
  uri:
    url: "https://api.github.com/repos/{{ github_org }}/{{ github_repo }}/deployments"
    method: POST
    headers:
      Authorization: "token {{ github_token }}"
    body:
      ref: "{{ app_version }}"
      environment: "{{ env }}"
      auto_merge: false
    body_format: json
  delegate_to: localhost
  run_once: true
  when: github_token is defined
```

---

## CI/CD Best Practices

- Lint and syntax-check on every PR
- Run `Molecule` tests in CI for role changes
- Use separate inventories per environment
- Require manual approval for production deployments
- Tag deployments in version control
- Use rolling updates with health checks
- Implement automated rollback on failure
- Send notifications on deploy success/failure
- Store vault passwords in CI secrets, never in code
- Keep CI pipelines fast (cache dependencies)

---

## Exercise: CI/CD Lab

1. Create a GitHub Actions workflow that:
    - Lints playbooks with `ansible-lint`
    - Runs `Molecule` tests
    - Deploys to staging on merge to main
    - Has a manual gate for production
1. Implement a rolling deployment with health checks
1. Add Slack notifications for deploy results
1. Practice blue/green switching
