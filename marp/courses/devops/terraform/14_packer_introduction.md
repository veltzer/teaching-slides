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

<svg xmlns="http://www.w3.org/2000/svg" width="650" height="390" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="10" y="10" width="290" height="365" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="155" y="32" text-anchor="middle" font-size="13" fill="#bf360c" font-weight="bold">Without Packer (runtime)</text>
  <rect x="30" y="55" width="230" height="48" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="145" y="83" text-anchor="middle" font-size="12" fill="#222">Launch Instance</text>
  <line x1="145" y1="103" x2="145" y2="121" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="30" y="121" width="230" height="48" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="145" y="149" text-anchor="middle" font-size="12" fill="#222">Install Software</text>
  <text x="145" y="164" text-anchor="middle" font-size="10" fill="#bf360c">10–20 min</text>
  <line x1="145" y1="169" x2="145" y2="187" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="30" y="187" width="230" height="48" rx="4" fill="#fff3e0" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="145" y="215" text-anchor="middle" font-size="12" fill="#222">Configure App</text>
  <line x1="145" y1="235" x2="145" y2="253" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="30" y="253" width="230" height="48" rx="4" fill="#ffccbc" stroke="#ef6c00" stroke-width="1.5"/>
  <text x="145" y="281" text-anchor="middle" font-size="12" fill="#222">Ready (slow start)</text>
  <rect x="345" y="10" width="295" height="365" rx="4" fill="#e8f5e9" stroke="#388e3c" stroke-width="1.5"/>
  <text x="492" y="32" text-anchor="middle" font-size="13" fill="#1b5e20" font-weight="bold">With Packer (pre-baked)</text>
  <rect x="368" y="55" width="248" height="48" rx="4" fill="#e8f5e9" stroke="#388e3c" stroke-width="1.5"/>
  <text x="492" y="81" text-anchor="middle" font-size="12" fill="#222">Build Image</text>
  <text x="492" y="97" text-anchor="middle" font-size="10" fill="#1b5e20">(once)</text>
  <line x1="492" y1="103" x2="492" y2="121" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="368" y="121" width="248" height="48" rx="4" fill="#e8f5e9" stroke="#388e3c" stroke-width="1.5"/>
  <text x="492" y="147" text-anchor="middle" font-size="12" fill="#222">Store Image</text>
  <line x1="492" y1="169" x2="492" y2="187" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="368" y="187" width="248" height="48" rx="4" fill="#c8e6c9" stroke="#388e3c" stroke-width="1.5"/>
  <text x="492" y="213" text-anchor="middle" font-size="12" fill="#222">Launch Instance</text>
  <text x="492" y="229" text-anchor="middle" font-size="10" fill="#1b5e20">(fast, < 1 min)</text>
</svg>

---

## Packer Architecture

<svg xmlns="http://www.w3.org/2000/svg" width="620" height="320" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="200" y="10" width="215" height="65" rx="4" fill="#e3f2fd" stroke="#1976d2" stroke-width="1.5"/>
  <text x="307" y="37" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">Packer Config</text>
  <text x="307" y="56" text-anchor="middle" font-size="12" fill="#555">(.pkr.hcl)</text>
  <line x1="307" y1="75" x2="307" y2="100" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="210" y="100" width="195" height="60" rx="4" fill="#bbdefb" stroke="#1565c0" stroke-width="1.5"/>
  <text x="307" y="128" text-anchor="middle" font-size="14" fill="#222" font-weight="bold">Packer Core</text>
  <line x1="307" y1="160" x2="307" y2="185" stroke="#555" stroke-width="1.5"/>
  <line x1="110" y1="185" x2="505" y2="185" stroke="#555" stroke-width="1.5"/>
  <line x1="110" y1="185" x2="110" y2="210" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="307" y1="185" x2="307" y2="210" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="505" y1="185" x2="505" y2="210" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="40" y="210" width="140" height="60" rx="4" fill="#e8f5e9" stroke="#388e3c" stroke-width="1.5"/>
  <text x="110" y="235" text-anchor="middle" font-size="13" fill="#222">Builder</text>
  <text x="110" y="253" text-anchor="middle" font-size="13" fill="#222">AWS</text>
  <line x1="110" y1="270" x2="110" y2="290" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="40" y="290" width="140" height="30" rx="4" fill="#e8f5e9" stroke="#388e3c" stroke-width="1.5"/>
  <text x="110" y="310" text-anchor="middle" font-size="12" fill="#222">AMI</text>
  <rect x="235" y="210" width="140" height="60" rx="4" fill="#fff3e0" stroke="#f57c00" stroke-width="1.5"/>
  <text x="305" y="235" text-anchor="middle" font-size="13" fill="#222">Builder</text>
  <text x="305" y="253" text-anchor="middle" font-size="13" fill="#222">Azure</text>
  <line x1="305" y1="270" x2="305" y2="290" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="235" y="290" width="140" height="30" rx="4" fill="#fff3e0" stroke="#f57c00" stroke-width="1.5"/>
  <text x="305" y="310" text-anchor="middle" font-size="12" fill="#222">VHD</text>
  <rect x="430" y="210" width="140" height="60" rx="4" fill="#fce4ec" stroke="#c2185b" stroke-width="1.5"/>
  <text x="500" y="235" text-anchor="middle" font-size="13" fill="#222">Builder</text>
  <text x="500" y="253" text-anchor="middle" font-size="13" fill="#222">Docker</text>
  <line x1="500" y1="270" x2="500" y2="290" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="430" y="290" width="140" height="30" rx="4" fill="#fce4ec" stroke="#c2185b" stroke-width="1.5"/>
  <text x="500" y="310" text-anchor="middle" font-size="12" fill="#222">Image</text>
</svg>

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

```misc
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

<svg xmlns="http://www.w3.org/2000/svg" width="540" height="440" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="70" y="15" width="400" height="46" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="270" y="41" text-anchor="middle" font-size="13" fill="#222" font-weight="bold">packer build</text>
  <line x1="270" y1="61" x2="270" y2="73" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="70" y="73" width="400" height="56" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="270" y="95" text-anchor="middle" font-size="13" fill="#222">1. Launch temporary instance</text>
  <text x="270" y="113" text-anchor="middle" font-size="11" fill="#555">   (from source AMI)</text>
  <line x1="270" y1="129" x2="270" y2="141" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="70" y="141" width="400" height="46" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="270" y="167" text-anchor="middle" font-size="13" fill="#222">2. Connect via SSH/WinRM</text>
  <line x1="270" y1="187" x2="270" y2="199" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="70" y="199" width="400" height="56" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="270" y="221" text-anchor="middle" font-size="13" fill="#222">3. Run provisioners</text>
  <text x="270" y="239" text-anchor="middle" font-size="11" fill="#555">   (install software)</text>
  <line x1="270" y1="255" x2="270" y2="267" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="70" y="267" width="400" height="46" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="270" y="293" text-anchor="middle" font-size="13" fill="#222">4. Stop instance</text>
  <line x1="270" y1="313" x2="270" y2="325" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="70" y="325" width="400" height="56" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="270" y="347" text-anchor="middle" font-size="13" fill="#222">5. Create image</text>
  <text x="270" y="365" text-anchor="middle" font-size="11" fill="#555">   (AMI snapshot)</text>
  <line x1="270" y1="381" x2="270" y2="393" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="70" y="393" width="400" height="56" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="270" y="415" text-anchor="middle" font-size="13" fill="#222">6. Terminate temporary</text>
  <text x="270" y="433" text-anchor="middle" font-size="11" fill="#555">   instance</text>
  <line x1="270" y1="449" x2="270" y2="461" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="70" y="461" width="400" height="56" rx="4" fill="#c8e6c9" stroke="#333" stroke-width="1.5"/>
  <text x="270" y="483" text-anchor="middle" font-size="13" fill="#222">7. Output artifact</text>
  <text x="270" y="501" text-anchor="middle" font-size="11" fill="#555">   (AMI ID)</text>
</svg>

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

<svg xmlns="http://www.w3.org/2000/svg" width="520" height="430" font-family="sans-serif">
  <defs>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
    <marker id="arr2" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#555"/>
    </marker>
  </defs>  <rect x="60" y="15" width="400" height="46" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="41" text-anchor="middle" font-size="13" fill="#222">1. Code Change</text>
  <line x1="260" y1="61" x2="260" y2="73" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="73" width="400" height="46" rx="4" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="99" text-anchor="middle" font-size="13" fill="#222">2. Build Application</text>
  <line x1="260" y1="119" x2="260" y2="131" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="131" width="400" height="56" rx="4" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="153" text-anchor="middle" font-size="13" fill="#222">3. Packer Build</text>
  <text x="260" y="171" text-anchor="middle" font-size="11" fill="#555">   (create AMI with app)</text>
  <line x1="260" y1="187" x2="260" y2="199" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="199" width="400" height="56" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="221" text-anchor="middle" font-size="13" fill="#222">4. Terraform Plan</text>
  <text x="260" y="239" text-anchor="middle" font-size="11" fill="#555">   (reference new AMI)</text>
  <line x1="260" y1="255" x2="260" y2="267" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="267" width="400" height="56" rx="4" fill="#fff3e0" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="289" text-anchor="middle" font-size="13" fill="#222">5. Terraform Apply</text>
  <text x="260" y="307" text-anchor="middle" font-size="11" fill="#555">   (deploy new instances)</text>
  <line x1="260" y1="323" x2="260" y2="335" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="335" width="400" height="46" rx="4" fill="#ede7f6" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="361" text-anchor="middle" font-size="13" fill="#222">6. Health Check / Smoke Test</text>
  <line x1="260" y1="381" x2="260" y2="393" stroke="#555" stroke-width="1.5" marker-end="url(#arr)"/>
  <rect x="60" y="393" width="400" height="56" rx="4" fill="#c8e6c9" stroke="#333" stroke-width="1.5"/>
  <text x="260" y="415" text-anchor="middle" font-size="13" fill="#222">7. DNS/LB Switch to</text>
  <text x="260" y="433" text-anchor="middle" font-size="11" fill="#555">   New Instances</text>
</svg>

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
