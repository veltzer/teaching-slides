# Introduction to Packer

## What is Packer?

- Open-source tool by HashiCorp for building machine images
- Creates identical images for multiple platforms from a single config
- Automates image creation process
- Integrates with configuration management tools
- Produces immutable infrastructure artifacts

---

## Why Use Packer?

- **Consistency**: Same image for dev, staging, production
- **Speed**: Pre-baked images boot faster than provisioning at launch
- **Immutability**: Replace servers instead of modifying them
- **Testability**: Test images before deployment
- **Multi-Platform**: One config produces images for AWS, Azure, GCP, Docker

---

## Packer vs Runtime Provisioning

```txt
Without Packer (runtime):           With Packer (pre-baked):
+----------+                        +----------+
| Launch   |                        | Build    |
| Instance |                        | Image    |  (once)
+----+-----+                        +----+-----+
     |                                   |
+----v-----+                        +----v-----+
| Install  |  10-20 min            | Store    |
| Software |                        | Image    |
+----+-----+                        +----+-----+
     |                                   |
+----v-----+                        +----v-----+
| Configure|                        | Launch   |  (fast)
| App      |                        | Instance |  <1 min
+----+-----+                        +----------+
     |
+----v-----+
| Ready    |  (slow start)
+----------+
```

---

## Packer Architecture

```txt
+-----------------+
|  Packer Config  |
|  (.pkr.hcl)     |
+--------+--------+
         |
    +----v----+
    | Packer  |
    | Core    |
    +----+----+
         |
    +----+----+----+----+
    |         |         |
+---v---+ +--v---+ +---v---+
|Builder| |Build | |Build  |
| AWS   | |Azure | |Docker |
+---+---+ +--+---+ +---+---+
    |         |         |
+---v---+ +--v---+ +---v---+
|  AMI  | | VHD  | |Image  |
+-------+ +------+ +-------+
```

---

## Packer Terminology

| Term | Description |
|------|-------------|
| Template | Configuration file defining the image |
| Builder | Plugin that creates the image for a platform |
| Provisioner | Script/tool that installs software |
| Post-Processor | Processes the image after creation |
| Artifact | Output of a build (e.g., AMI ID) |
| Source | Base image definition |
| Build | The process of creating an image |

---

## Installing Packer

```bash
# Linux (Ubuntu/Debian)
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install packer

# macOS
brew install packer

# Verify
packer version
```

---

## Packer Template Formats

```txt
Legacy JSON format (deprecated):
  template.json

Modern HCL format (recommended):
  template.pkr.hcl
  variables.pkr.hcl

Packer HCL uses same syntax as Terraform HCL.
```

---

## Basic Packer Template (HCL)

```hcl
packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = "~> 1.2"
    }
  }
}

source "amazon-ebs" "ubuntu" {
  ami_name      = "my-app-{{timestamp}}"
  instance_type = "t3.micro"
  region        = "us-east-1"
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
}
```

---

## Build Block

```hcl
build {
  name    = "my-app"
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx",
      "sudo systemctl enable nginx",
    ]
  }

  post-processor "manifest" {
    output = "manifest.json"
  }
}
```

---

## Packer Commands

```bash
# Initialize (download plugins)
packer init template.pkr.hcl

# Validate template
packer validate template.pkr.hcl

# Format template
packer fmt template.pkr.hcl

# Build image
packer build template.pkr.hcl

# Build with variables
packer build -var "region=us-west-2" template.pkr.hcl
```

---

## Packer Build Process

```txt
packer build
    |
    v
1. Launch temporary instance (from source AMI)
    |
    v
2. Connect via SSH/WinRM
    |
    v
3. Run provisioners (install software)
    |
    v
4. Stop instance
    |
    v
5. Create image (AMI snapshot)
    |
    v
6. Terminate temporary instance
    |
    v
7. Output artifact (AMI ID)
```

---

## Packer Variables

```hcl
# variables.pkr.hcl
variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "app_version" {
  type        = string
  description = "Application version to install"
}
```

---

## Using Variables in Templates

```hcl
source "amazon-ebs" "app" {
  region        = var.aws_region
  instance_type = var.instance_type
  ami_name      = "app-${var.app_version}-{{timestamp}}"
  # ...
}
```

```bash
# Pass variables via CLI
packer build -var "app_version=1.2.3" .

# Pass variables via file
packer build -var-file="prod.pkrvars.hcl" .

# Environment variables
export PKR_VAR_app_version="1.2.3"
packer build .
```

---

## AWS Builder (amazon-ebs)

```hcl
source "amazon-ebs" "web" {
  ami_name      = "web-server-{{timestamp}}"
  instance_type = "t3.micro"
  region        = "us-east-1"

  # Source AMI
  source_ami = "ami-0c55b159cbfafe1f0"

  # Or use filter
  source_ami_filter {
    filters = {
      name = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-*"
    }
    owners      = ["099720109477"]
    most_recent = true
  }

  ssh_username = "ubuntu"

  tags = {
    Name    = "Web Server"
    Version = var.app_version
  }
}
```

---

## AWS Builder Options

| Option | Description |
|--------|-------------|
| `ami_name` | Name for the output AMI |
| `instance_type` | EC2 instance type for build |
| `region` | AWS region |
| `source_ami` | Base AMI ID |
| `source_ami_filter` | Dynamic AMI selection |
| `ssh_username` | SSH user for provisioning |
| `vpc_id` | VPC for build instance |
| `subnet_id` | Subnet for build instance |
| `security_group_id` | SG for build instance |
| `ami_regions` | Copy AMI to other regions |

---

## Multi-Region AMI

```hcl
source "amazon-ebs" "web" {
  ami_name      = "web-server-{{timestamp}}"
  instance_type = "t3.micro"
  region        = "us-east-1"

  # Copy to additional regions
  ami_regions = [
    "us-west-2",
    "eu-west-1",
    "ap-southeast-1",
  ]

  source_ami_filter {
    # ...
  }
  ssh_username = "ubuntu"
}
```

---

## Azure Builder

```hcl
source "azure-arm" "ubuntu" {
  client_id       = var.client_id
  client_secret   = var.client_secret
  subscription_id = var.subscription_id
  tenant_id       = var.tenant_id

  managed_image_resource_group_name = "packer-images-rg"
  managed_image_name                = "web-server-{{timestamp}}"

  os_type         = "Linux"
  image_publisher = "Canonical"
  image_offer     = "0001-com-ubuntu-server-jammy"
  image_sku       = "22_04-lts"

  location = "East US"
  vm_size  = "Standard_B1s"
}
```

---

## Packer Provisioners

| Provisioner | Description |
|-------------|-------------|
| `shell` | Run shell commands |
| `shell-local` | Run local commands |
| `file` | Upload files |
| `ansible` | Run Ansible playbooks |
| `chef-solo` | Run Chef recipes |
| `puppet-masterless` | Run Puppet manifests |
| `powershell` | Run PowerShell scripts |

---

## Shell Provisioner

```hcl
build {
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y nginx curl jq",
      "sudo systemctl enable nginx",
    ]
  }

  provisioner "shell" {
    script = "scripts/setup.sh"
    environment_vars = [
      "APP_VERSION=${var.app_version}",
      "ENVIRONMENT=production",
    ]
  }
}
```

---

## File Provisioner (Packer)

```hcl
build {
  sources = ["source.amazon-ebs.ubuntu"]

  # Upload configuration file
  provisioner "file" {
    source      = "configs/nginx.conf"
    destination = "/tmp/nginx.conf"
  }

  # Upload directory
  provisioner "file" {
    source      = "scripts/"
    destination = "/opt/scripts"
  }

  # Move files to final location (needs sudo)
  provisioner "shell" {
    inline = [
      "sudo mv /tmp/nginx.conf /etc/nginx/nginx.conf",
    ]
  }
}
```

---

## Ansible Provisioner

```hcl
build {
  sources = ["source.amazon-ebs.ubuntu"]

  provisioner "ansible" {
    playbook_file = "ansible/site.yml"
    user          = "ubuntu"

    extra_arguments = [
      "--extra-vars",
      "app_version=${var.app_version}",
    ]

    ansible_env_vars = [
      "ANSIBLE_HOST_KEY_CHECKING=False",
    ]
  }
}
```

---

## Post-Processors

```hcl
build {
  sources = ["source.amazon-ebs.ubuntu"]

  # ... provisioners ...

  # Output manifest with artifact IDs
  post-processor "manifest" {
    output     = "packer-manifest.json"
    strip_path = true
  }

  # Tag the AMI
  post-processor "amazon-ami-management" {
    regions    = ["us-east-1"]
    identifier = "my-app"
    keep_releases = 3
  }
}
```

---

## Post-Processor Types

| Post-Processor | Description |
|----------------|-------------|
| `manifest` | Write build info to JSON file |
| `shell-local` | Run local script after build |
| `compress` | Compress artifact |
| `docker-push` | Push Docker image to registry |
| `vagrant` | Create Vagrant box |
| `checksum` | Generate checksums |

---

## Manifest Post-Processor Output

```json
{
  "builds": [
    {
      "name": "ubuntu",
      "builder_type": "amazon-ebs",
      "build_time": 1705312200,
      "artifact_id": "us-east-1:ami-0abc123def456",
      "packer_run_uuid": "a1b2c3d4-e5f6-7890",
      "custom_data": {
        "app_version": "1.2.3"
      }
    }
  ]
}
```

---

## Multiple Builders

```hcl
source "amazon-ebs" "web" {
  ami_name      = "web-{{timestamp}}"
  instance_type = "t3.micro"
  region        = "us-east-1"
  # ...
}

source "azure-arm" "web" {
  managed_image_name = "web-{{timestamp}}"
  # ...
}

build {
  sources = [
    "source.amazon-ebs.web",
    "source.azure-arm.web",
  ]

  provisioner "shell" {
    inline = ["sudo apt-get update && sudo apt-get install -y nginx"]
  }
}
```

---

## Build-Specific Overrides

```hcl
build {
  sources = [
    "source.amazon-ebs.web",
    "source.azure-arm.web",
  ]

  # Runs for all sources
  provisioner "shell" {
    inline = ["sudo apt-get update"]
  }

  # Runs only for AWS
  provisioner "shell" {
    only   = ["amazon-ebs.web"]
    inline = ["sudo apt-get install -y awscli"]
  }

  # Runs only for Azure
  provisioner "shell" {
    only   = ["azure-arm.web"]
    inline = ["sudo apt-get install -y azure-cli"]
  }
}
```

---

## Packer with Terraform

```hcl
# Step 1: Build AMI with Packer
# packer build web-server.pkr.hcl

# Step 2: Use AMI in Terraform
data "aws_ami" "web" {
  most_recent = true
  owners      = ["self"]

  filter {
    name   = "name"
    values = ["web-server-*"]
  }

  filter {
    name   = "tag:Version"
    values = [var.app_version]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.web.id
  instance_type = "t3.micro"
}
```

---

## CI/CD Pipeline with Packer and Terraform

```txt
1. Code Change
     |
     v
2. Build Application
     |
     v
3. Packer Build (create AMI with app)
     |
     v
4. Terraform Plan (reference new AMI)
     |
     v
5. Terraform Apply (deploy new instances)
     |
     v
6. Health Check / Smoke Test
     |
     v
7. DNS/LB Switch to New Instances
```

---

## Chapter Summary

- Packer creates machine images for multiple platforms
- Templates define sources (builders), provisioners, and post-processors
- Use HCL format (`.pkr.hcl`) for modern templates
- Builders create images for AWS, Azure, GCP, Docker, etc.
- Provisioners install software during image creation
- Post-processors process the output artifact
- Combine Packer with Terraform for immutable infrastructure
- Pre-baked images boot faster than runtime provisioning
