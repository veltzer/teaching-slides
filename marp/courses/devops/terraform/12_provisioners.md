---
tags:
  - practices:devops
  - tools:terraform
  - infrastructure:infrastructure-as-code
  - infrastructure:cloud
  - tools:terragrunt
level: intermediate
category: devops
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---

# Provisioners

## Provisioner Types Overview

| Provisioner | Description | Runs On |
|-------------|-------------|---------|
| `local-exec` | Execute command locally | Your machine |
| `remote-exec` | Execute command remotely | Target resource |
| `file` | Upload files/directories | Target resource |

---

## Provisioner Execution Flow

![provisioner_execution_flow](svg/courses/devops/terraform/12_provisioners/provisioner_execution_flow.svg)

---

## local-exec Provisioner

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  provisioner "local-exec" {
    command = "echo ${self.public_ip} >> hosts.txt"
  }
}
```

- Runs on the machine where Terraform is executed
- Useful for triggering external tools
- No connection block needed

---

## local-exec with Working Directory

```hcl
provisioner "local-exec" {
  command     = "./deploy.sh"
  working_dir = "${path.module}/scripts"
}
```

---

## local-exec with Environment Variables

```hcl
provisioner "local-exec" {
  command = "ansible-playbook -i '${self.public_ip},' playbook.yml"

  environment = {
    ANSIBLE_HOST_KEY_CHECKING = "false"
    APP_VERSION               = var.app_version
    ENVIRONMENT               = var.environment
  }
}
```

---

## local-exec with Different Interpreters

```hcl
# Use Python
provisioner "local-exec" {
  command     = "process.py ${self.id}"
  interpreter = ["python3", "-c"]
}

# Use PowerShell on Windows
provisioner "local-exec" {
  command     = "Write-Host 'Instance: ${self.id}'"
  interpreter = ["PowerShell", "-Command"]
}

# Use bash explicitly
provisioner "local-exec" {
  command     = "echo 'Done' && date"
  interpreter = ["/bin/bash", "-c"]
}
```

---

## local-exec Use Cases

```hcl
# Update Ansible inventory
provisioner "local-exec" {
  command = <<-EOT
    cat >> inventory.ini <<EOF
    [web]
    ${self.public_ip} ansible_user=ubuntu
    EOF
  EOT
}

# Trigger webhook
provisioner "local-exec" {
  command = <<-EOT
    curl -X POST https://hooks.slack.com/services/xxx \
      -H 'Content-type: application/json' \
      -d '{"text":"Instance ${self.id} created"}'
  EOT
}
```

---

## local-exec with null_resource

```hcl
resource "null_resource" "ansible" {
  triggers = {
    instance_ids = join(",", aws_instance.web[*].id)
  }

  provisioner "local-exec" {
    command = "ansible-playbook -i inventory.ini site.yml"

    environment = {
      ANSIBLE_HOST_KEY_CHECKING = "false"
    }
  }

  depends_on = [aws_instance.web]
}
```

---

## remote-exec Provisioner

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  key_name      = aws_key_pair.deployer.key_name

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa")
    host        = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
      "sudo systemctl start nginx",
    ]
  }
}
```

---

## remote-exec: inline vs script vs scripts

```hcl
# Option 1: Inline commands
provisioner "remote-exec" {
  inline = [
    "echo 'Hello'",
    "sudo apt-get update",
  ]
}

# Option 2: Single script file
provisioner "remote-exec" {
  script = "${path.module}/scripts/setup.sh"
}

# Option 3: Multiple script files
provisioner "remote-exec" {
  scripts = [
    "${path.module}/scripts/install.sh",
    "${path.module}/scripts/configure.sh",
  ]
}
```

---

## remote-exec Script Upload

```misc
When using script or scripts:

1. Terraform uploads script to /tmp on remote host
2. Sets execute permission (chmod +x)
3. Executes the script
4. Captures stdout/stderr
5. Removes script after execution

Important:
  - Script must have proper shebang (#!/bin/bash)
  - Exit code determines success/failure
  - Cannot use Terraform variables directly in script files
  - Use file provisioner + remote-exec for templated scripts
```

---

## Templated Remote Scripts

```hcl
# Step 1: Upload templated script
provisioner "file" {
  content = templatefile("${path.module}/setup.sh.tpl", {
    db_host     = aws_db_instance.main.endpoint
    environment = var.environment
  })
  destination = "/tmp/setup.sh"
}

# Step 2: Execute uploaded script
provisioner "remote-exec" {
  inline = [
    "chmod +x /tmp/setup.sh",
    "/tmp/setup.sh",
  ]
}
```

---

## File Provisioner: Uploading Files

```hcl
# Upload a single file
provisioner "file" {
  source      = "configs/nginx.conf"
  destination = "/tmp/nginx.conf"
}

# Upload with inline content
provisioner "file" {
  content     = "DATABASE_URL=${aws_db_instance.main.endpoint}"
  destination = "/tmp/env"
}
```

---

## File Provisioner: Uploading Directories

```hcl
# Upload entire directory
provisioner "file" {
  source      = "configs/"     # Trailing slash: upload contents
  destination = "/opt/configs"
}

# Without trailing slash: upload directory itself
provisioner "file" {
  source      = "configs"     # No trailing slash
  destination = "/opt"
  # Creates /opt/configs/
}
```

---

## File Provisioner Behavior

```tree
source = "configs/"   (trailing slash)
  Local: configs/
    ├── app.conf
    └── db.conf
  Remote: /opt/configs/
    ├── app.conf
    └── db.conf

source = "configs"    (no trailing slash)
  Local: configs/
    ├── app.conf
    └── db.conf
  Remote: /opt/configs/
    ├── app.conf
    └── db.conf
```

---

## Complete Provisioner Example

```hcl
resource "aws_instance" "app" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.small"
  key_name      = aws_key_pair.deployer.key_name
  subnet_id     = aws_subnet.public.id

  vpc_security_group_ids = [aws_security_group.app.id]

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/deployer")
    host        = self.public_ip
  }

  # Continues on next slide...
}
```

---

## Complete Provisioner Example (continued)

```hcl
  # Step 1: Upload configuration
  provisioner "file" {
    content = templatefile("${path.module}/app.conf.tpl", {
      db_host = aws_db_instance.main.endpoint
      port    = 8080
    })
    destination = "/tmp/app.conf"
  }

  # Step 2: Upload setup script
  provisioner "file" {
    source      = "${path.module}/scripts/setup.sh"
    destination = "/tmp/setup.sh"
  }

  # Step 3: Run setup
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/setup.sh",
      "sudo /tmp/setup.sh",
    ]
  }
```

---

## Provisioner Error Handling

```hcl
# Fail on error (default) - resource is tainted
provisioner "remote-exec" {
  on_failure = fail
  inline     = ["exit 1"]
}

# Continue on error - resource is not tainted
provisioner "remote-exec" {
  on_failure = continue
  inline     = ["optional-command || true"]
}
```

```misc
on_failure = fail:
  Resource marked as tainted
  Next apply will recreate it

on_failure = continue:
  Error is logged but ignored
  Resource remains healthy
```

---

## Creation vs Destroy Provisioners

```hcl
resource "aws_instance" "web" {
  # ...

  # Runs after creation (default)
  provisioner "remote-exec" {
    when   = create  # default, can be omitted
    inline = ["sudo /opt/scripts/register.sh"]
  }

  # Runs before destruction
  provisioner "remote-exec" {
    when   = destroy
    inline = ["sudo /opt/scripts/deregister.sh"]

    connection {
      type = "ssh"
      user = "ubuntu"
      host = self.public_ip
    }
  }
}
```

---

## Destroy Provisioner Limitations

- Cannot reference other resources (they may already be destroyed)
- Can only use `self` references
- Connection info must be self-contained
- If destroy provisioner fails, resource is still destroyed

```hcl
# This WILL NOT work in destroy provisioner:
provisioner "remote-exec" {
  when = destroy
  inline = [
    # Cannot reference aws_db_instance here!
    "echo ${aws_db_instance.main.endpoint}",  # ERROR
  ]
}
```

---

## Provisioner Ordering

```hcl
resource "aws_instance" "web" {
  # ...

  # Runs first
  provisioner "file" {
    source      = "app.tar.gz"
    destination = "/tmp/app.tar.gz"
  }

  # Runs second
  provisioner "remote-exec" {
    inline = ["tar xzf /tmp/app.tar.gz -C /opt/app"]
  }

  # Runs third
  provisioner "local-exec" {
    command = "echo 'Deployment complete' >> deploy.log"
  }
}
```

---

## null_resource for Provisioner Workflows

```hcl
resource "null_resource" "deploy_app" {
  # Recreate when these change
  triggers = {
    app_version = var.app_version
    config_hash = md5(file("app.conf"))
  }

  provisioner "local-exec" {
    command = <<-EOT
      ansible-playbook deploy.yml \
        -e "version=${var.app_version}" \
        -e "hosts=${join(",", aws_instance.web[*].public_ip)}"
    EOT
  }

  depends_on = [aws_instance.web]
}
```

---

## terraform_data Resource (Replaces null_resource)

```hcl
# Terraform 1.4+ replacement for null_resource
resource "terraform_data" "deploy" {
  input = var.app_version

  provisioner "local-exec" {
    command = "deploy.sh ${self.output}"
  }
}
```

- Built-in, no provider needed
- `input` triggers replacement (like `triggers`)
- `output` stores the input value in state

---

## Provisioners with for_each

```hcl
resource "aws_instance" "web" {
  for_each      = toset(["web1", "web2", "web3"])
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  key_name      = aws_key_pair.deployer.key_name

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa")
    host        = self.public_ip
  }

  provisioner "remote-exec" {
    inline = [
      "sudo hostnamectl set-hostname ${each.key}",
    ]
  }
}
```

---

## Alternatives to Provisioners

| Need | Instead of Provisioner | Use |
|------|----------------------|-----|
| Install packages | `remote-exec` | User data / cloud-init |
| Configure server | `remote-exec` | Packer pre-baked image |
| Deploy app | `remote-exec` | CI/CD pipeline |
| Run Ansible | `local-exec` | Ansible directly |
| Register DNS | `local-exec` | `aws_route53_record` |
| Send notification | `local-exec` | CI/CD pipeline |

---

## When Provisioners ARE Appropriate

- Bootstrapping a resource that cannot use user data
- Integrating with legacy tools during migration
- One-time setup tasks not covered by any provider
- Running external tools that have no Terraform provider
- Cleanup tasks on resource destruction

---

## Chapter Summary

- `local-exec` runs commands on the Terraform host
- `remote-exec` runs commands on the created resource via SSH/WinRM
- `file` uploads files and directories to remote resources
- Provisioners require a `connection` block for remote access
- Provisioners run in declaration order
- `on_failure` controls whether errors taint the resource
- `when = destroy` runs before resource deletion
- `terraform_data` replaces `null_resource` in Terraform 1.4+
- Prefer user data, Packer images, or Ansible over provisioners
