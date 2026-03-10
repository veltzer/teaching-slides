# Ansible Vault for Secrets Management

## Topics Covered
- Why encrypt secrets
- Creating and editing encrypted files
- Encrypting individual variables
- Using vault in playbooks
- Multi-vault IDs and password files
- Vault best practices

---

## Why Ansible Vault?

- Playbooks and inventory are stored in version control
- Secrets (passwords, API keys, certificates) must not be in plaintext
- `Ansible Vault` encrypts data at rest using `AES-256`
- Encrypted files can be safely committed to `Git`
- Decryption happens transparently at runtime

---

## What to Encrypt

- Database passwords and connection strings
- API keys and tokens
- `SSL`/`TLS` certificates and private keys
- Cloud provider credentials
- Application secrets
- User passwords
- Any sensitive configuration values

---

## Creating an Encrypted File

```bash
# Create a new encrypted file
ansible-vault create secrets.yml
# Opens your $EDITOR, prompts for vault password

# The file is encrypted with AES-256
$ cat secrets.yml
$ANSIBLE_VAULT;1.1;AES256
61626364656667686970716...
31323334353637383930...

# View encrypted file contents
ansible-vault view secrets.yml

# Edit an encrypted file
ansible-vault edit secrets.yml
```

---

## Encrypting Existing Files

```bash
# Encrypt an existing file
ansible-vault encrypt group_vars/production/secrets.yml

# Decrypt a file (returns to plaintext)
ansible-vault decrypt group_vars/production/secrets.yml

# Re-key (change the password)
ansible-vault rekey secrets.yml

# Encrypt a string (inline)
ansible-vault encrypt_string 'SuperSecretPassword123' \
    --name 'db_password'

# Output:
# db_password: !vault |
#   $ANSIBLE_VAULT;1.1;AES256
#   61626364656667686970716...
```

---

## Encrypted Variables in Files

```yaml
# group_vars/production/vault.yml (encrypted file)
---
vault_db_password: SuperSecretPassword123
vault_api_key: sk-abc123def456
vault_ssl_private_key: |
  -----BEGIN PRIVATE KEY-----
  MIIEvgIBADANBgkqhkiG9w...
  -----END PRIVATE KEY-----

# group_vars/production/vars.yml (plain text)
---
db_password: "{{ vault_db_password }}"
api_key: "{{ vault_api_key }}"
ssl_key: "{{ vault_ssl_private_key }}"
```

---

## Inline Encrypted Variables

```yaml
# Mix encrypted and plain variables in the same file
# group_vars/all.yml
---
app_name: mywebapp
app_port: 8080
debug_mode: false

# Encrypted inline using ansible-vault encrypt_string
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  6162636465666768697071...

api_token: !vault |
  $ANSIBLE_VAULT;1.1;AES256
  3132333435363738393031...

# Plain variables continue normally
log_level: info
```

---

## Using Vault in Playbooks

```bash
# Prompt for vault password
ansible-playbook site.yml --ask-vault-pass

# Use a password file
ansible-playbook site.yml --vault-password-file ~/.vault_pass

# Use environment variable
export ANSIBLE_VAULT_PASSWORD_FILE=~/.vault_pass
ansible-playbook site.yml

# In ansible.cfg
# [defaults]
# vault_password_file = ~/.vault_pass
```

---

## Vault Password File

```bash
# Create a password file
echo 'MyVaultPassword123' > ~/.vault_pass
chmod 600 ~/.vault_pass

# Or use a script that outputs the password
cat > ~/.vault_pass.sh << 'EOF'
#!/bin/bash
# Could fetch from a secrets manager
cat ~/.vault_pass
EOF
chmod 700 ~/.vault_pass.sh

# Use the script
ansible-playbook site.yml \
    --vault-password-file ~/.vault_pass.sh

# Or fetch from environment
cat > ~/.vault_env.sh << 'EOF'
#!/bin/bash
echo "$ANSIBLE_VAULT_SECRET"
EOF
```

---

## Multiple Vault IDs

```bash
# Create files with different vault IDs
ansible-vault create --vault-id prod@prompt secrets_prod.yml
ansible-vault create --vault-id dev@prompt secrets_dev.yml

# Use a password file per vault ID
ansible-vault create \
    --vault-id prod@~/.vault_pass_prod \
    secrets_prod.yml

# Run playbook with multiple vault IDs
ansible-playbook site.yml \
    --vault-id prod@~/.vault_pass_prod \
    --vault-id dev@~/.vault_pass_dev

# Encrypt string with vault ID
ansible-vault encrypt_string \
    --vault-id prod@~/.vault_pass_prod \
    'SuperSecret' --name 'prod_db_password'
```

---

## Vault with Variable Files Pattern

```text
group_vars/
├── all/
│   ├── vars.yml          # Plain text variables
│   └── vault.yml         # Encrypted variables
├── production/
│   ├── vars.yml          # Plain text
│   └── vault.yml         # Encrypted (production secrets)
└── staging/
    ├── vars.yml          # Plain text
    └── vault.yml         # Encrypted (staging secrets)
```

```yaml
# group_vars/production/vault.yml (encrypted)
vault_db_password: "prod-super-secret-password"
vault_api_key: "prod-api-key-12345"

# group_vars/production/vars.yml (plain)
db_password: "{{ vault_db_password }}"
api_key: "{{ vault_api_key }}"
db_host: db.prod.internal
```

---

## no_log for Runtime Security

```yaml
# Prevent sensitive data from appearing in logs
- name: Create database user
  postgresql_user:
    name: appuser
    password: "{{ vault_db_password }}"
  no_log: true

# Without no_log, the password would appear in:
# - Verbose output (-v)
# - Log files
# - Callback plugin output
# - Error messages

# Set no_log globally for sensitive roles
- name: Apply secrets
  include_role:
    name: configure_secrets
  no_log: true
```

---

## Vault Best Practices

- Prefix vault variables with `vault_` for clarity
- Keep encrypted and plain variables in separate files
- Use `no_log: true` on tasks that handle secrets
- Never commit vault passwords to version control
- Use different vault passwords per environment
- Rotate vault passwords regularly
- Use a vault password script that fetches from a secrets manager
- Add `.vault_pass` to `.gitignore`
- Document which files are encrypted

---

## Integrating with External Secrets Managers

```yaml
# Using HashiCorp Vault via lookup
- name: Get secret from HashiCorp Vault
  set_fact:
    db_password: "{{ lookup('hashi_vault', 'secret/data/myapp:db_password') }}"

# Using AWS Secrets Manager
- name: Get secret from AWS
  set_fact:
    api_key: "{{ lookup('amazon.aws.aws_secret', 'myapp/api_key') }}"

# Using Azure Key Vault
- name: Get secret from Azure
  set_fact:
    cert: "{{ lookup('azure.azcollection.azure_keyvault_secret', 'myCert', vault_url='https://myvault.vault.azure.net') }}"

# Using environment variables (simple approach)
- name: Use env var
  set_fact:
    token: "{{ lookup('env', 'API_TOKEN') }}"
```

---

## Exercise: Vault Lab

1. Create an encrypted vault file with database credentials
2. Reference vault variables from plain variable files
3. Use `ansible-vault encrypt_string` for inline encryption
4. Run a playbook using `--vault-password-file`
5. Practice `ansible-vault edit`, `view`, `rekey`
6. Implement the `vault_` prefix naming convention
