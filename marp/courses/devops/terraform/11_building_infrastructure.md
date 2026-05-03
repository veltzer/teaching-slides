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
# Building Infrastructure

---

## Infrastructure Build Workflow

![infrastructure_workflow](svg/courses/devops/terraform/11_building_infrastructure/infrastructure_workflow.svg)

---

## Configuration Management vs Provisioning

```misc
Configuration Management:        Provisioning:
  - Install software               - Create infrastructure
  - Configure services              - Set up networks, VMs, storage
  - Manage files                    - Allocate cloud resources
  - Enforce desired state           - Define topology

  Tools: Ansible, Chef, Puppet     Tools: Terraform, CloudFormation
```

---

## Where Each Tool Fits

![where_each_tool_fits](svg/courses/devops/terraform/11_building_infrastructure/where_each_tool_fits.svg)

---

## Terraform's Role in the Stack

![terraform_s_role_in_the_stack](svg/courses/devops/terraform/11_building_infrastructure/terraform_s_role_in_the_stack.svg)

---

## Providers vs Provisioners

| Concept | Provider | Provisioner |
|---------|----------|-------------|
| Purpose | Manage resources via API | Run scripts on resources |
| When | Create/update/delete | After resource creation |
| Scope | Full CRUD lifecycle | One-time or on-destroy |
| Example | `aws_instance` | `remote-exec`, `local-exec` |
| Idempotent | Yes | Not guaranteed |
| Recommended | Yes | Last resort |

---

## Why Provisioners are a Last Resort

- Not part of the declarative model
- Not stored in state
- Not idempotent by default
- Hard to debug and test
- Break the plan/apply workflow
- Better alternatives exist

```misc
Better alternatives:
  - User data scripts (cloud-init)
  - Pre-built images (Packer)
  - Configuration management (Ansible)
  - Container images (Docker)
```

---

## User Data (cloud-init)

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  user_data = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y nginx
    systemctl start nginx
    echo "<h1>Hello from Terraform</h1>" > /var/www/html/index.html
  EOF

  user_data_replace_on_change = true

  tags = {
    Name = "web-server"
  }
}
```

---

## User Data with templatefile

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  user_data = templatefile("${path.module}/scripts/setup.sh", {
    server_name = "web-${count.index}"
    db_host     = aws_db_instance.main.endpoint
    environment = var.environment
  })
}
```

---

## User Data Template Example

```bash
#!/bin/bash
# setup.sh (template)
set -euo pipefail

hostnamectl set-hostname ${server_name}

cat > /etc/app/config.json <<'CONFIG'
{
  "database_host": "${db_host}",
  "environment": "${environment}",
  "log_level": "info"
}
CONFIG

apt-get update
apt-get install -y docker.io
systemctl enable docker
systemctl start docker
```

---

## Cloud-Init Advanced

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  user_data = <<-EOF
    #cloud-config
    package_update: true
    packages:
      - nginx
      - curl
      - jq
    write_files:
      - path: /etc/app/config.yaml
        content: |
          environment: ${var.environment}
          port: 8080
    runcmd:
      - systemctl start nginx
  EOF
}
```

---

## Tainting Resources (Legacy)

```bash
# Mark resource for recreation (deprecated command)
terraform taint aws_instance.web

# Remove taint
terraform untaint aws_instance.web
```

```bash
# Modern approach: use -replace flag
terraform apply -replace="aws_instance.web"

# Preview replacement
terraform plan -replace="aws_instance.web"
```

---

## When to Use -replace

- Instance is in a bad state (crashed, corrupted)
- Need to apply new user data
- SSL certificate needs regeneration
- Need to force a new AMI
- Debugging provisioner issues

```bash
# Replace specific indexed resource
terraform apply -replace="aws_instance.web[0]"

# Replace module resource
terraform apply -replace="module.compute.aws_instance.web"
```

---

## The file Provisioner

```hcl
resource "aws_instance" "web" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"
  key_name      = aws_key_pair.deployer.key_name

  provisioner "file" {
    source      = "conf/app.conf"
    destination = "/tmp/app.conf"

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }
}
```

---

## File Provisioner: Directory Upload

```hcl
provisioner "file" {
  # Upload entire directory
  source      = "scripts/"
  destination = "/opt/scripts"

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa")
    host        = self.public_ip
  }
}
```

- Uploads files or directories to the remote machine
- Requires SSH or WinRM connection
- Runs after resource creation

---

## File Provisioner: Inline Content

```hcl
provisioner "file" {
  content = jsonencode({
    database_host = aws_db_instance.main.endpoint
    environment   = var.environment
    api_key       = var.api_key
  })
  destination = "/opt/app/config.json"

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa")
    host        = self.public_ip
  }
}
```

---

## Connection Blocks

```hcl
resource "aws_instance" "web" {
  # ...

  connection {
    type        = "ssh"
    user        = "ubuntu"
    private_key = file("~/.ssh/id_rsa")
    host        = self.public_ip
    port        = 22
    timeout     = "5m"
  }

  provisioner "remote-exec" {
    inline = ["echo Connected!"]
  }
}
```

---
## Connection via Bastion Host: Example

```hcl
connection {
  type        = "ssh"
  user        = "ubuntu"
  private_key = file("~/.ssh/id_rsa")
  host        = self.private_ip
  bastion_host        = aws_instance.bastion.public_ip
  bastion_user        = "ubuntu"
  bastion_private_key = file("~/.ssh/bastion_key")
}
```

---
## Connection via Bastion Host

![connection_via_bastion_host](svg/courses/devops/terraform/11_building_infrastructure/connection_via_bastion_host.svg)

---

## WinRM Connection

```hcl
resource "aws_instance" "windows" {
  ami           = data.aws_ami.windows.id
  instance_type = "t3.medium"

  connection {
    type     = "winrm"
    user     = "Administrator"
    password = var.admin_password
    host     = self.public_ip
    https    = true
    insecure = true
    timeout  = "10m"
  }

  provisioner "remote-exec" {
    inline = ["powershell Write-Host 'Connected!'"]
  }
}
```

---

## Provisioner Failure Behavior

```hcl
resource "aws_instance" "web" {
  # ...

  # Default: fail and taint resource
  provisioner "remote-exec" {
    on_failure = fail    # default
    inline     = ["exit 1"]
  }

  # Continue on failure
  provisioner "remote-exec" {
    on_failure = continue
    inline     = ["some-optional-command"]
  }
}
```

---

## Destroy-Time Provisioners

```hcl
resource "aws_instance" "web" {
  # ...

  # Run before resource is destroyed
  provisioner "remote-exec" {
    when = destroy
    inline = [
      "echo 'Deregistering from load balancer...'",
      "/opt/scripts/deregister.sh",
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      private_key = file("~/.ssh/id_rsa")
      host        = self.public_ip
    }
  }
}
```

---

## Multiple Provisioners

```hcl
resource "aws_instance" "web" {
  # ...

  # Provisioners run in order
  provisioner "file" {
    source      = "scripts/setup.sh"
    destination = "/tmp/setup.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/setup.sh",
      "/tmp/setup.sh",
    ]
  }

  provisioner "local-exec" {
    command = "echo ${self.public_ip} >> inventory.txt"
  }
}
```

---

## Building Complete Infrastructure

```hcl
# Network layer
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}
```

---

## Building Complete Infrastructure (continued)

```hcl
# Security layer
resource "aws_security_group" "web" {
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

---

## Building Complete Infrastructure (compute)

```hcl
# Compute layer
resource "aws_instance" "web" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = var.instance_type
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]
  key_name               = aws_key_pair.deployer.key_name

  user_data = templatefile("${path.module}/setup.sh", {
    environment = var.environment
  })

  tags = {
    Name = "web-server"
  }
}
```

---

## Chapter Summary

- Configuration management (Ansible) configures; provisioning (Terraform) creates
- Providers manage resources via cloud APIs (recommended)
- Provisioners run scripts on resources (last resort)
- Prefer user data / cloud-init over provisioners
- Use `-replace` to force resource recreation (replaces deprecated `taint`)
- Connection blocks define SSH/WinRM access for provisioners
- Provisioners run in declaration order
- Destroy-time provisioners run with `when = destroy`
