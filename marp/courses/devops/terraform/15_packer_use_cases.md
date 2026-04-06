# Packer Use Cases

## Packer Use Case Overview

<svg xmlns="http://www.w3.org/2000/svg" width="530" height="226" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<rect x="10" y="10" width="240" height="88" fill="#e3f2fd" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="130.0" y="45.0" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">AWS AMIs</text>
<text x="130.0" y="63.0" text-anchor="middle" font-size="13" fill="#222222">Production server images</text>
<rect x="280" y="10" width="240" height="88" fill="#e3f2fd" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="400.0" y="45.0" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Container Images</text>
<text x="400.0" y="63.0" text-anchor="middle" font-size="13" fill="#222222">Docker, ECR, ACR</text>
<rect x="10" y="128" width="240" height="88" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="130.0" y="163.0" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">VirtualBox/VMware</text>
<text x="130.0" y="181.0" text-anchor="middle" font-size="13" fill="#222222">Development VMs, Vagrant</text>
<rect x="280" y="128" width="240" height="88" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="400.0" y="163.0" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Multi-Cloud</text>
<text x="400.0" y="181.0" text-anchor="middle" font-size="13" fill="#222222">AWS + Azure + GCP images</text>
</svg>

---

## Use Case 1: AWS Web Server AMI

```hcl
packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = "~> 1.2"
    }
  }
}

variable "app_version" {
  type = string
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}
```

---

## AWS Web Server: Source

```hcl
source "amazon-ebs" "web" {
  ami_name      = "web-server-${var.app_version}-{{timestamp}}"
  instance_type = "t3.small"
  region        = var.aws_region

  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    owners      = ["099720109477"]
    most_recent = true
  }

  ssh_username = "ubuntu"

  tags = {
    Name        = "Web Server"
    Version     = var.app_version
    BuildTime   = "{{timestamp}}"
    Base_AMI    = "{{ .SourceAMI }}"
  }
}
```

---

## AWS Web Server: Build

```hcl
build {
  sources = ["source.amazon-ebs.web"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx certbot python3-certbot-nginx",
      "sudo systemctl enable nginx",
    ]
  }

  provisioner "file" {
    source      = "configs/nginx.conf"
    destination = "/tmp/nginx.conf"
  }

  provisioner "shell" {
    inline = [
      "sudo mv /tmp/nginx.conf /etc/nginx/sites-available/default",
      "sudo nginx -t",
    ]
  }
}
```

---

## AWS Hardened Server AMI

```hcl
source "amazon-ebs" "hardened" {
  ami_name      = "hardened-ubuntu-{{timestamp}}"
  instance_type = "t3.micro"
  region        = "us-east-1"

  source_ami_filter {
    filters = {
      name = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-*"
    }
    owners      = ["099720109477"]
    most_recent = true
  }

  ssh_username = "ubuntu"

  ami_regions = ["us-east-1", "us-west-2", "eu-west-1"]
}
```

---

## Hardened Server: Provisioning

```hcl
build {
  sources = ["source.amazon-ebs.hardened"]

  provisioner "shell" {
    scripts = [
      "scripts/update-system.sh",
      "scripts/configure-ssh.sh",
      "scripts/configure-firewall.sh",
      "scripts/install-monitoring.sh",
      "scripts/cleanup.sh",
    ]
  }

  provisioner "shell" {
    inline = [
      "sudo apt-get autoremove -y",
      "sudo apt-get clean",
      "sudo rm -rf /var/lib/apt/lists/*",
      "sudo rm -rf /tmp/*",
    ]
  }
}
```

---

## Hardening Script Example

```bash
#!/bin/bash
# scripts/configure-ssh.sh
set -euo pipefail

# Disable root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Disable password authentication
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Set SSH timeout
echo "ClientAliveInterval 300" | sudo tee -a /etc/ssh/sshd_config
echo "ClientAliveCountMax 2" | sudo tee -a /etc/ssh/sshd_config

# Install fail2ban
sudo apt-get install -y fail2ban
sudo systemctl enable fail2ban
```

---

## AWS AMI with Application

```hcl
build {
  sources = ["source.amazon-ebs.app"]

  # Install runtime
  provisioner "shell" {
    inline = [
      "curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -",
      "sudo apt-get install -y nodejs",
    ]
  }

  # Upload application
  provisioner "file" {
    source      = "dist/app.tar.gz"
    destination = "/tmp/app.tar.gz"
  }

  # Install application
  provisioner "shell" {
    inline = [
      "sudo mkdir -p /opt/app",
      "sudo tar xzf /tmp/app.tar.gz -C /opt/app",
      "cd /opt/app && sudo npm install --production",
    ]
  }
}
```

---

## AWS AMI with Ansible

```hcl
build {
  sources = ["source.amazon-ebs.app"]

  provisioner "ansible" {
    playbook_file = "ansible/site.yml"
    user          = "ubuntu"

    extra_arguments = [
      "--extra-vars", "app_version=${var.app_version}",
      "--extra-vars", "environment=production",
      "-vv",
    ]

    groups = ["webservers"]
  }
}
```

---

## Ansible Playbook for Packer

```yaml
# ansible/site.yml
---
- hosts: all
  become: true
  tasks:
    - name: Install packages
      apt:
        name:
          - nginx
          - python3-pip
          - supervisor
        state: present
        update_cache: true

    - name: Deploy application config
      template:
        src: templates/app.conf.j2
        dest: /etc/app/config.conf

    - name: Enable services
      systemd:
        name: "{{ item }}"
        enabled: true
      loop:
        - nginx
        - supervisor
```

---

## Using Built AMI with Terraform

```hcl
# After Packer builds the AMI, use it in Terraform

variable "app_version" {
  type = string
}

data "aws_ami" "app" {
  most_recent = true
  owners      = ["self"]

  filter {
    name   = "name"
    values = ["web-server-${var.app_version}-*"]
  }
}

resource "aws_launch_template" "web" {
  image_id      = data.aws_ami.app.id
  instance_type = "t3.micro"
}
```

---

## Blue-Green Deployment with Packer

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="400" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="350" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">Blue-Green Deployment with Packer</text>
<text x="20" y="45" text-anchor="start" font-size="13" fill="#222222" font-weight="bold">Phase 1: Build new AMI</text>
<text x="30" y="61" text-anchor="start" font-size="12" fill="#444">Packer build → AMI v2</text>
<text x="20" y="81" text-anchor="start" font-size="13" fill="#222222" font-weight="bold">Phase 2: Deploy alongside old</text>
<text x="30" y="97" text-anchor="start" font-size="12" fill="#444">Terraform creates new ASG with AMI v2; old ASG (AMI v1) still running</text>
<text x="20" y="117" text-anchor="start" font-size="13" fill="#222222" font-weight="bold">Phase 3: Switch traffic</text>
<text x="30" y="133" text-anchor="start" font-size="12" fill="#444">Update ALB target group to new ASG</text>
<text x="20" y="153" text-anchor="start" font-size="13" fill="#222222" font-weight="bold">Phase 4: Cleanup</text>
<text x="30" y="169" text-anchor="start" font-size="12" fill="#444">Terminate old ASG</text>
<text x="160" y="232" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Before</text>
<rect x="80" y="250" width="160" height="45" fill="#e3f2fd" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="160" y="276" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">ALB</text>
<line x1="160" y1="295" x2="160" y2="345" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<rect x="80" y="345" width="160" height="45" fill="#fff3e0" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="160" y="371" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">ASG v1</text>
<text x="460" y="232" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">After</text>
<rect x="380" y="250" width="160" height="45" fill="#e3f2fd" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="460" y="276" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">ALB</text>
<line x1="460" y1="295" x2="460" y2="345" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<rect x="380" y="345" width="160" height="45" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="460" y="371" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">ASG v2</text>
</svg>

---

## Use Case 2: Docker Container Images

```hcl
packer {
  required_plugins {
    docker = {
      source  = "github.com/hashicorp/docker"
      version = "~> 1.0"
    }
  }
}

source "docker" "app" {
  image  = "ubuntu:22.04"
  commit = true
  changes = [
    "EXPOSE 8080",
    "CMD [\"/opt/app/start.sh\"]",
    "ENTRYPOINT [\"/bin/bash\"]",
  ]
}
```

---

## Docker Build

```hcl
build {
  sources = ["source.docker.app"]

  provisioner "shell" {
    inline = [
      "apt-get update",
      "apt-get install -y curl nodejs npm",
    ]
  }

  provisioner "file" {
    source      = "app/"
    destination = "/opt/app"
  }

  provisioner "shell" {
    inline = [
      "cd /opt/app && npm install --production",
    ]
  }

  post-processor "docker-tag" {
    repository = "myregistry.com/myapp"
    tags       = [var.app_version, "latest"]
  }

  post-processor "docker-push" {
    login          = true
    login_server   = "myregistry.com"
    login_username = var.registry_username
    login_password = var.registry_password
  }
}
```

---

## Packer vs Dockerfile

| Feature | Packer | Dockerfile |
|---------|--------|------------|
| Multi-platform | Yes (AMI + Docker) | Docker only |
| Language | HCL | Dockerfile syntax |
| Caching | Limited | Layer caching |
| Provisioners | Multiple tools | RUN commands |
| Post-processing | Built-in | External tools |
| Best for | Multi-platform images | Container-only |

---

## When to Use Packer for Containers

- Need the same image for VMs AND containers
- Complex provisioning requiring multiple tools
- Want Ansible/Chef provisioning in Docker builds
- Building base images with extensive setup
- CI/CD pipeline already uses Packer for AMIs

---

## ECR Push with Packer

```hcl
variable "ecr_repo" {
  type    = string
  default = "123456789.dkr.ecr.us-east-1.amazonaws.com/myapp"
}

build {
  sources = ["source.docker.app"]

  # ... provisioners ...

  post-processor "docker-tag" {
    repository = var.ecr_repo
    tags       = [var.app_version]
  }

  post-processor "docker-push" {
    ecr_login    = true
    login_server = "https://${var.ecr_repo}"
  }
}
```

---

## Use Case 3: VirtualBox Development VM

```hcl
packer {
  required_plugins {
    virtualbox = {
      source  = "github.com/hashicorp/virtualbox"
      version = "~> 1.0"
    }
  }
}

source "virtualbox-iso" "dev" {
  guest_os_type    = "Ubuntu_64"
  iso_url          = "https://releases.ubuntu.com/22.04/ubuntu-22.04-live-server-amd64.iso"
  iso_checksum     = "sha256:abcdef123456..."
  disk_size        = 40000
  memory           = 4096
  cpus             = 2
  ssh_username     = "vagrant"
  ssh_password     = "vagrant"
  shutdown_command = "echo 'vagrant' | sudo -S shutdown -P now"
}
```

---

## VirtualBox Dev VM: Build

```hcl
build {
  sources = ["source.virtualbox-iso.dev"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y git docker.io nodejs python3-pip",
      "sudo usermod -aG docker vagrant",
    ]
  }

  provisioner "file" {
    source      = "dotfiles/"
    destination = "/home/vagrant/"
  }

  post-processor "vagrant" {
    output = "builds/dev-vm-{{.Provider}}.box"
  }
}
```

---

## Vagrant Box from Packer

```bash
# Build the Vagrant box with Packer
packer build dev-vm.pkr.hcl

# Add to Vagrant
vagrant box add --name dev-vm builds/dev-vm-virtualbox.box

# Use in Vagrantfile
# Vagrant.configure("2") do |config|
#   config.vm.box = "dev-vm"
# end

vagrant up
```

---

## Use Case 4: Multi-Cloud Image

```hcl
source "amazon-ebs" "web" {
  ami_name      = "web-${var.version}-{{timestamp}}"
  instance_type = "t3.micro"
  region        = "us-east-1"
  source_ami_filter {
    filters = { name = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-*" }
    owners      = ["099720109477"]
    most_recent = true
  }
  ssh_username = "ubuntu"
}

source "azure-arm" "web" {
  managed_image_name                = "web-${var.version}"
  managed_image_resource_group_name = "packer-images"
  os_type                           = "Linux"
  image_publisher                   = "Canonical"
  image_offer                       = "0001-com-ubuntu-server-jammy"
  image_sku                         = "22_04-lts"
  location                          = "East US"
  vm_size                           = "Standard_B1s"
}
```

---

## Multi-Cloud: Shared Provisioners

```hcl
build {
  sources = [
    "source.amazon-ebs.web",
    "source.azure-arm.web",
  ]

  # Same provisioning for both clouds
  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
      "sudo systemctl enable nginx",
    ]
  }

  provisioner "ansible" {
    playbook_file = "ansible/webserver.yml"
    user          = "ubuntu"
  }
}
```

---

## Packer Build with Terraform Outputs

```bash
#!/bin/bash
# build-and-deploy.sh

# Step 1: Build AMI
AMI_ID=$(packer build -machine-readable . | \
  grep 'artifact,0,id' | \
  cut -d, -f6 | \
  cut -d: -f2)

echo "Built AMI: $AMI_ID"

# Step 2: Deploy with Terraform
cd terraform/
terraform apply \
  -var "ami_id=$AMI_ID" \
  -auto-approve
```

---

## Packer Manifest for Terraform

```hcl
# Packer post-processor
post-processor "manifest" {
  output     = "packer-manifest.json"
  strip_path = true
}
```

```hcl
# Terraform reads manifest
locals {
  manifest = jsondecode(file("${path.module}/packer-manifest.json"))
  ami_id   = local.manifest.builds[0].artifact_id
}

resource "aws_instance" "web" {
  ami           = split(":", local.ami_id)[1]
  instance_type = "t3.micro"
}
```

---

## Image Pipeline Best Practices

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="240" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="310" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">Image Pipeline</text>
<rect x="180" y="35" width="260" height="38" fill="#fff3e0" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="310" y="58" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Source Image  (Ubuntu base)</text>
<line x1="310" y1="73" x2="310" y2="103" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<rect x="130" y="103" width="360" height="38" fill="#e3f2fd" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="310" y="126" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">Base Image  (security hardening, monitoring agents)</text>
<line x1="310" y1="141" x2="310" y2="155" stroke="#555" stroke-width="1.5"/>
<line x1="80" y1="155" x2="540" y2="155" stroke="#555" stroke-width="1.5"/>
<line x1="80" y1="155" x2="80" y2="175" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<rect x="10" y="175" width="140" height="50" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="80" y="197" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">Web Server</text>
<text x="80" y="214" text-anchor="middle" font-size="12" fill="#222222">Image</text>
<line x1="310" y1="155" x2="310" y2="175" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<rect x="240" y="175" width="140" height="50" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="310" y="197" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">API Server</text>
<text x="310" y="214" text-anchor="middle" font-size="12" fill="#222222">Image</text>
<line x1="540" y1="155" x2="540" y2="175" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
<rect x="470" y="175" width="140" height="50" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="540" y="197" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">Worker</text>
<text x="540" y="214" text-anchor="middle" font-size="12" fill="#222222">Image</text>
</svg>

- Build images in layers
- Base image updated monthly for security patches
- Application images built per release

---

## Packer in CI/CD

```yaml
# .github/workflows/packer.yml
name: Build AMI
on:
  push:
    tags: ['v*']
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-packer@v3
      - name: Init
        run: packer init .
      - name: Validate
        run: packer validate .
      - name: Build
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: packer build -var "app_version=${{ github.ref_name }}" .
```

---

## AMI Lifecycle Management

```hcl
# Deregister old AMIs automatically
build {
  sources = ["source.amazon-ebs.app"]

  # ... provisioners ...

  # Keep only last 5 AMIs
  post-processor "amazon-ami-management" {
    regions       = ["us-east-1"]
    identifier    = "my-app"
    keep_releases = 5
  }
}
```

---

## Testing Packer Images

```bash
# Option 1: Launch and test manually
aws ec2 run-instances --image-id ami-abc123 --instance-type t3.micro

# Option 2: Use Terratest (Go)
# Automated testing framework for infrastructure code

# Option 3: InSpec/ServerSpec
# Compliance testing for images

# Option 4: Goss
# Quick YAML-based server validation
goss validate
```

---

## Goss Validation with Packer

```hcl
provisioner "shell" {
  inline = [
    "curl -fsSL https://goss.rocks/install | sudo sh",
  ]
}

provisioner "file" {
  source      = "tests/goss.yaml"
  destination = "/tmp/goss.yaml"
}

provisioner "shell" {
  inline = [
    "goss -g /tmp/goss.yaml validate --format documentation",
  ]
}
```

---

## Goss Test File

```yaml
# tests/goss.yaml
package:
  nginx:
    installed: true
  curl:
    installed: true

service:
  nginx:
    enabled: true
    running: true

port:
  tcp:80:
    listening: true

file:
  /etc/nginx/nginx.conf:
    exists: true
    mode: "0644"
```

---

## Immutable Infrastructure Pattern

<svg xmlns="http://www.w3.org/2000/svg" width="700" height="320" font-family="sans-serif">
<defs>
  <marker id="arr"  markerWidth="10" markerHeight="7" refX="9"   refY="3.5" orient="auto">
    <polygon points="0 0,10 3.5,0 7" fill="#555"/>
  </marker>
  <marker id="arrl" markerWidth="10" markerHeight="7" refX="1"   refY="3.5" orient="auto">
    <polygon points="10 0,0 3.5,10 7" fill="#555"/>
  </marker>
</defs>
<text x="350" y="22" text-anchor="middle" font-size="14" fill="#222222" font-weight="bold">Mutable vs Immutable Infrastructure</text>
<text x="145" y="48" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Mutable</text>
<rect x="30" y="58" width="230" height="130" fill="#fff3e0" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="145" y="83" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">Server</text>
<text x="145" y="105" text-anchor="middle" font-size="12" fill="#222222">v1 → v1.1 → v1.2</text>
<text x="145" y="127" text-anchor="middle" font-size="12" fill="#222222">← SSH in, modify</text>
<text x="145" y="149" text-anchor="middle" font-size="12" fill="#222222">   in place</text>
<text x="520" y="48" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Immutable</text>
<rect x="390" y="58" width="230" height="55" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="505" y="84" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">Server v1</text>
<text x="505" y="100" text-anchor="middle" font-size="12" fill="#222222">← Replace entirely</text>
<rect x="390" y="133" width="230" height="55" fill="#e8f5e9" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="505" y="158" text-anchor="middle" font-size="12" fill="#222222" font-weight="bold">Server v2</text>
<text x="505" y="174" text-anchor="middle" font-size="12" fill="#222222">← New image</text>
<rect x="20" y="215" width="660" height="80" fill="#f5f5f5" stroke="#333333" stroke-width="1.5" rx="4"/>
<text x="350" y="237" text-anchor="middle" font-size="13" fill="#222222" font-weight="bold">Packer enables immutable infrastructure:</text>
<text x="350" y="257" text-anchor="middle" font-size="12" fill="#222222">New code  →  New image  →  New servers  →  Old servers removed</text>
</svg>

---

## Chapter Summary

- Packer builds AMIs for production web servers and applications
- Ansible provisioner enables complex configuration in Packer builds
- Docker source creates container images alongside VM images
- VirtualBox source creates development VM images and Vagrant boxes
- Multi-cloud builds share provisioning across AWS and Azure
- Use manifest post-processor to pass AMI IDs to Terraform
- Build images in layers: base -> application-specific
- Test images with Goss, InSpec, or Terratest
- Immutable infrastructure replaces servers instead of modifying them
