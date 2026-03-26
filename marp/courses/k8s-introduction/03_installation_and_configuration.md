# Installation and Configuration

---

## Installation Options Overview

1. **Local Development**: Single-node clusters
1. **Managed Services**: Cloud provider solutions
1. **Production**: Self-managed clusters
1. **Learning**: Lightweight distributions
1. **Testing**: Ephemeral environments

---

## Local Development Tools

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Local Kubernetes Options</text>
  <rect x="100" y="80" width="150" height="100" fill="#4285f4" rx="5"/>
  <text x="175" y="110" text-anchor="middle" fill="white" font-weight="bold">Minikube</text>
  <text x="175" y="135" text-anchor="middle" fill="white" font-size="11">Most popular</text>
  <text x="175" y="155" text-anchor="middle" fill="white" font-size="11">Full features</text>
  <rect x="275" y="80" width="150" height="100" fill="#34a853" rx="5"/>
  <text x="350" y="110" text-anchor="middle" fill="white" font-weight="bold">Kind</text>
  <text x="350" y="135" text-anchor="middle" fill="white" font-size="11">K8s in Docker</text>
  <text x="350" y="155" text-anchor="middle" fill="white" font-size="11">CI/CD friendly</text>
  <rect x="450" y="80" width="150" height="100" fill="#fbbc04" rx="5"/>
  <text x="525" y="110" text-anchor="middle" font-weight="bold">K3s</text>
  <text x="525" y="135" text-anchor="middle" font-size="11">Lightweight</text>
  <text x="525" y="155" text-anchor="middle" font-size="11">Edge/IoT</text>
  <rect x="625" y="80" width="125" height="100" fill="#ea4335" rx="5"/>
  <text x="687" y="110" text-anchor="middle" fill="white" font-weight="bold">Docker</text>
  <text x="687" y="135" text-anchor="middle" fill="white" font-size="11">Desktop</text>
  <text x="687" y="155" text-anchor="middle" fill="white" font-size="11">Built-in</text>
  <rect x="100" y="210" width="650" height="100" fill="#e8f5e9" rx="5"/>
  <text x="425" y="240" text-anchor="middle" font-weight="bold">Your Local Machine</text>
  <text x="425" y="270" text-anchor="middle" font-size="14">Choose based on your needs:</text>
  <text x="425" y="290" text-anchor="middle" font-size="12">Learning → Minikube | Testing → Kind | Resource-constrained → K3s</text>
</svg>

---

## Minikube Overview

1. **Purpose**: Local Kubernetes development
1. **Features**: Closest to production
1. **Addons**: Built-in extensions
1. **Drivers**: Multiple virtualization options
1. **Resources**: Configurable CPU/memory

---

## System Requirements

1. **CPU**: 2 cores minimum
1. **Memory**: 2GB minimum (4GB recommended)
1. **Disk**: 20GB free space
1. **OS**: Linux, macOS, Windows
1. **Virtualization**: Enabled in BIOS

---

## Pre-Installation Checklist

```bash
# Check virtualization support (Linux)
grep -E --color 'vmx|svm' /proc/cpuinfo

# Check available memory
free -h

# Check disk space
df -h

# Check kernel version
uname -r
```

---

## Installing kubectl

```bash
# Download latest kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s \
  https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Make executable
chmod +x kubectl

# Move to PATH
sudo mv kubectl /usr/local/bin/

# Verify installation
kubectl version --client
```

---

## Installing Minikube

```bash
# Download Minikube binary
curl -LO https://storage.googleapis.com/minikube/releases/latest/\
minikube-linux-amd64

# Install Minikube
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Verify installation
minikube version

# Clean up
rm minikube-linux-amd64
```

---

## Minikube Drivers

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Minikube Driver Options</text>
  <rect x="100" y="80" width="200" height="80" fill="#4285f4" rx="5"/>
  <text x="200" y="110" text-anchor="middle" fill="white" font-weight="bold">Docker (Recommended)</text>
  <text x="200" y="135" text-anchor="middle" fill="white" font-size="12">Lightweight</text>
  <text x="200" y="150" text-anchor="middle" fill="white" font-size="12">No VM needed</text>
  <rect x="320" y="80" width="200" height="80" fill="#34a853" rx="5"/>
  <text x="420" y="110" text-anchor="middle" fill="white" font-weight="bold">VirtualBox</text>
  <text x="420" y="135" text-anchor="middle" fill="white" font-size="12">Cross-platform</text>
  <text x="420" y="150" text-anchor="middle" fill="white" font-size="12">Full isolation</text>
  <rect x="540" y="80" width="200" height="80" fill="#fbbc04" rx="5"/>
  <text x="640" y="110" text-anchor="middle" font-weight="bold">KVM2 (Linux)</text>
  <text x="640" y="135" text-anchor="middle" font-size="12">Native Linux</text>
  <text x="640" y="150" text-anchor="middle" font-size="12">Best performance</text>
  <rect x="100" y="180" width="200" height="80" fill="#ea4335" rx="5"/>
  <text x="200" y="210" text-anchor="middle" fill="white" font-weight="bold">Hyperkit (macOS)</text>
  <text x="200" y="235" text-anchor="middle" fill="white" font-size="12">Native macOS</text>
  <text x="200" y="250" text-anchor="middle" fill="white" font-size="12">Lightweight</text>
  <rect x="320" y="180" width="200" height="80" fill="#9c27b0" rx="5"/>
  <text x="420" y="210" text-anchor="middle" fill="white" font-weight="bold">Hyper-V (Windows)</text>
  <text x="420" y="235" text-anchor="middle" fill="white" font-size="12">Windows native</text>
  <text x="420" y="250" text-anchor="middle" fill="white" font-size="12">Enterprise ready</text>
  <rect x="540" y="180" width="200" height="80" fill="#607d8b" rx="5"/>
  <text x="640" y="210" text-anchor="middle" fill="white" font-weight="bold">None (Bare Metal)</text>
  <text x="640" y="235" text-anchor="middle" fill="white" font-size="12">Direct on host</text>
  <text x="640" y="250" text-anchor="middle" fill="white" font-size="12">Advanced users</text>
</svg>

---

## Starting Minikube

```bash
# Start with default settings
minikube start

# Start with specific driver
minikube start --driver=docker

# Start with custom resources
minikube start --cpus=4 --memory=8192

# Start with specific Kubernetes version
minikube start --kubernetes-version=v1.28.0
```

---

## Minikube Start Process

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <text x="400" y="30" text-anchor="middle" font-size="16" font-weight="bold">Minikube Start Sequence</text>
  <rect x="50" y="60" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="125" y="95" text-anchor="middle" fill="white">1. Check Driver</text>
  <rect x="50" y="140" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="125" y="175" text-anchor="middle" fill="white">2. Create VM/Container</text>
  <rect x="50" y="220" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="125" y="255" text-anchor="middle" fill="white">3. Configure Network</text>
  <rect x="50" y="300" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="125" y="335" text-anchor="middle" fill="white">4. Install Kubernetes</text>
  <rect x="250" y="60" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="325" y="95" text-anchor="middle" fill="white">5. Start kubelet</text>
  <rect x="250" y="140" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="325" y="175" text-anchor="middle" fill="white">6. Start API Server</text>
  <rect x="250" y="220" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="325" y="255" text-anchor="middle" fill="white">7. Start etcd</text>
  <rect x="250" y="300" width="150" height="60" fill="#34a853" rx="5"/>
  <text x="325" y="335" text-anchor="middle" fill="white">8. Start Controllers</text>
  <rect x="450" y="60" width="150" height="60" fill="#fbbc04" rx="5"/>
  <text x="525" y="95" text-anchor="middle">9. Configure kubectl</text>
  <rect x="450" y="140" width="150" height="60" fill="#fbbc04" rx="5"/>
  <text x="525" y="175" text-anchor="middle">10. Verify Cluster</text>
  <rect x="450" y="220" width="150" height="60" fill="#fbbc04" rx="5"/>
  <text x="525" y="255" text-anchor="middle">11. Enable Addons</text>
  <rect x="450" y="300" width="150" height="60" fill="#fbbc04" rx="5"/>
  <text x="525" y="335" text-anchor="middle">12. Ready!</text>
  <path d="M 200 90 L 245 90" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <path d="M 400 90 L 445 90" stroke="#666" stroke-width="2" marker-end="url(#arrow)"/>
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#666"/>
    </marker>
  </defs>
</svg>

---

## Verifying Installation

```bash
# Check cluster status
minikube status

# Get cluster info
kubectl cluster-info

# Check nodes
kubectl get nodes

# Check system pods
kubectl get pods -n kube-system
```

---

## Minikube Configuration

```bash
# View current configuration
minikube config view

# Set default driver
minikube config set driver docker

# Set default memory
minikube config set memory 4096

# Set default CPUs
minikube config set cpus 2
```

---

## Minikube Profiles

```bash
# Create new profile
minikube start -p development

# List profiles
minikube profile list

# Switch profile
minikube profile development

# Delete profile
minikube delete -p development
```

---

## Minikube Addons

```bash
# List available addons
minikube addons list

# Enable addon
minikube addons enable dashboard
minikube addons enable metrics-server
minikube addons enable ingress

# Disable addon
minikube addons disable dashboard
```

---

## Popular Minikube Addons

1. **dashboard**: Kubernetes web UI
1. **metrics-server**: Resource metrics
1. **ingress**: NGINX ingress controller
1. **storage-provisioner**: Dynamic volumes
1. **registry**: Local Docker registry

---

## Accessing Minikube VM

```bash
# SSH into Minikube
minikube ssh

# Run command in Minikube
minikube ssh -- docker ps

# Copy files to Minikube
minikube cp file.txt:/tmp/file.txt

# Mount local directory
minikube mount /local/path:/remote/path
```

---

## Minikube Dashboard

```bash
# Start dashboard
minikube dashboard

# Get dashboard URL
minikube dashboard --url

# Access in background
minikube dashboard &

# Custom port
minikube dashboard --port=8080
```

---

## kubectl Configuration

```bash
# View config
kubectl config view

# Get contexts
kubectl config get-contexts

# Use context
kubectl config use-context minikube

# Set namespace
kubectl config set-context --current --namespace=default
```

---

## kubectl Autocomplete

```bash
# Bash completion
echo 'source <(kubectl completion bash)' >> ~/.bashrc
source ~/.bashrc

# Zsh completion
echo 'source <(kubectl completion zsh)' >> ~/.zshrc
source ~/.zshrc

# Alias with completion
alias k=kubectl
complete -F __start_kubectl k
```

---

## Environment Variables

```bash
# Set KUBECONFIG
export KUBECONFIG=$HOME/.kube/config

# Multiple configs
export KUBECONFIG=$HOME/.kube/config:$HOME/.kube/config-dev

# Minikube Docker env
eval $(minikube docker-env)

# Unset Docker env
eval $(minikube docker-env -u)
```

---

## Installing Kind

```bash
# Download Kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64

# Make executable
chmod +x ./kind

# Move to PATH
sudo mv ./kind /usr/local/bin/kind

# Verify
kind version
```

---

## Kind Cluster Configuration

```yaml
# kind-config.yaml
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
networking:
  podSubnet: "10.240.0.0/16"
  serviceSubnet: "10.0.0.0/16"
```

---

## Creating Kind Cluster

```bash
# Simple cluster
kind create cluster

# Named cluster
kind create cluster --name dev

# With config file
kind create cluster --config kind-config.yaml

# Multiple nodes
kind create cluster --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
EOF
```

---

## Installing K3s

```bash
# Quick install
curl -sfL https://get.k3s.io | sh -

# Install without traefik
curl -sfL https://get.k3s.io | sh -s - --disable traefik

# Install as agent
curl -sfL https://get.k3s.io | K3S_URL=https://server:6443 \
  K3S_TOKEN=token sh -

# Check status
sudo systemctl status k3s
```

---

## K3s Configuration

```bash
# Get kubeconfig
sudo cat /etc/rancher/k3s/k3s.yaml

# Copy config for user
mkdir -p $HOME/.kube
sudo cp /etc/rancher/k3s/k3s.yaml $HOME/.kube/config
sudo chown $USER:$USER $HOME/.kube/config

# Access cluster
kubectl get nodes
```

---

## Docker Desktop Kubernetes

1. **Enable**: Settings → Kubernetes → Enable
1. **Version**: Select Kubernetes version
1. **Reset**: Reset Kubernetes cluster
1. **Resources**: Configure in Docker settings
1. **Context**: docker-desktop

---

## Cloud Managed Services

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f0f0f0" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">Managed Kubernetes Services</text>
  <rect x="100" y="100" width="200" height="80" fill="#ff9900" rx="5"/>
  <text x="200" y="130" text-anchor="middle" font-weight="bold">AWS</text>
  <text x="200" y="155" text-anchor="middle" font-size="14">EKS</text>
  <text x="200" y="170" text-anchor="middle" font-size="11">Elastic Kubernetes Service</text>
  <rect x="320" y="100" width="200" height="80" fill="#4285f4" rx="5"/>
  <text x="420" y="130" text-anchor="middle" fill="white" font-weight="bold">Google Cloud</text>
  <text x="420" y="155" text-anchor="middle" fill="white" font-size="14">GKE</text>
  <text x="420" y="170" text-anchor="middle" fill="white" font-size="11">Google Kubernetes Engine</text>
  <rect x="540" y="100" width="200" height="80" fill="#0078d4" rx="5"/>
  <text x="640" y="130" text-anchor="middle" fill="white" font-weight="bold">Azure</text>
  <text x="640" y="155" text-anchor="middle" fill="white" font-size="14">AKS</text>
  <text x="640" y="170" text-anchor="middle" fill="white" font-size="11">Azure Kubernetes Service</text>
  <rect x="200" y="220" width="200" height="80" fill="#ff5722" rx="5"/>
  <text x="300" y="250" text-anchor="middle" fill="white" font-weight="bold">DigitalOcean</text>
  <text x="300" y="275" text-anchor="middle" fill="white" font-size="14">DOKS</text>
  <rect x="420" y="220" width="200" height="80" fill="#00599c" rx="5"/>
  <text x="520" y="250" text-anchor="middle" fill="white" font-weight="bold">IBM Cloud</text>
  <text x="520" y="275" text-anchor="middle" fill="white" font-size="14">IKS</text>
</svg>

---

## Production Installation Options

1. **kubeadm**: Official Kubernetes tool
1. **kops**: Kubernetes Operations
1. **kubespray**: Ansible playbooks
1. **Rancher**: Management platform
1. **OpenShift**: Enterprise Kubernetes

---

## kubeadm Installation

```bash
# Install kubeadm, kubelet, kubectl
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl

# Add Kubernetes GPG key
sudo curl -fsSL https://packages.cloud.google.com/apt/doc/\
apt-key.gpg | sudo apt-key add -

# Add Kubernetes repository
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | \
  sudo tee /etc/apt/sources.list.d/kubernetes.list

# Install packages
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
```

---

## Initializing Master Node

```bash
# Initialize cluster
sudo kubeadm init --pod-network-cidr=10.244.0.0/16

# Configure kubectl for user
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Install network plugin (Flannel)
kubectl apply -f https://raw.githubusercontent.com/flannel-io/\
flannel/master/Documentation/kube-flannel.yml
```

---

## Joining Worker Nodes

```bash
# On master, get join command
kubeadm token create --print-join-command

# On worker, join cluster
sudo kubeadm join master-ip:6443 --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash>

# Verify nodes
kubectl get nodes
```

---

## Network Plugins (CNI)

1. **Flannel**: Simple overlay network
1. **Calico**: Network policies support
1. **Weave**: Automatic mesh network
1. **Cilium**: eBPF-based networking
1. **Canal**: Flannel + Calico

---

## Installing Network Plugin

```bash
# Flannel
kubectl apply -f https://raw.githubusercontent.com/\
flannel-io/flannel/master/Documentation/kube-flannel.yml

# Calico
kubectl apply -f https://docs.projectcalico.org/\
manifests/tigera-operator.yaml

# Weave
kubectl apply -f https://github.com/weaveworks/weave/\
releases/download/v2.8.1/weave-daemonset-k8s.yaml
```

---

## High Availability Setup

<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <rect x="50" y="50" width="700" height="300" fill="#f9f9f9" stroke="#333" stroke-width="2"/>
  <text x="400" y="30" text-anchor="middle" font-size="18" font-weight="bold">HA Kubernetes Architecture</text>
  <rect x="100" y="80" width="150" height="60" fill="#4285f4" rx="5"/>
  <text x="175" y="115" text-anchor="middle" fill="white">Load Balancer</text>
  <rect x="300" y="80" width="120" height="60" fill="#34a853" rx="5"/>
  <text x="360" y="105" text-anchor="middle" fill="white" font-size="12">Master 1</text>
  <text x="360" y="125" text-anchor="middle" fill="white" font-size="10">etcd, API</text>
  <rect x="440" y="80" width="120" height="60" fill="#34a853" rx="5"/>
  <text x="500" y="105" text-anchor="middle" fill="white" font-size="12">Master 2</text>
  <text x="500" y="125" text-anchor="middle" fill="white" font-size="10">etcd, API</text>
  <rect x="580" y="80" width="120" height="60" fill="#34a853" rx="5"/>
  <text x="640" y="105" text-anchor="middle" fill="white" font-size="12">Master 3</text>
  <text x="640" y="125" text-anchor="middle" fill="white" font-size="10">etcd, API</text>
  <rect x="150" y="200" width="100" height="60" fill="#fbbc04" rx="5"/>
  <text x="200" y="235" text-anchor="middle">Worker 1</text>
  <rect x="270" y="200" width="100" height="60" fill="#fbbc04" rx="5"/>
  <text x="320" y="235" text-anchor="middle">Worker 2</text>
  <rect x="390" y="200" width="100" height="60" fill="#fbbc04" rx="5"/>
  <text x="440" y="235" text-anchor="middle">Worker 3</text>
  <rect x="510" y="200" width="100" height="60" fill="#fbbc04" rx="5"/>
  <text x="560" y="235" text-anchor="middle">Worker 4</text>
  <line x1="175" y1="140" x2="360" y2="140" stroke="#666" stroke-width="2"/>
  <line x1="175" y1="140" x2="500" y2="140" stroke="#666" stroke-width="2"/>
  <line x1="175" y1="140" x2="640" y2="140" stroke="#666" stroke-width="2"/>
</svg>

---

## Troubleshooting Installation

```bash
# Check system logs
journalctl -xeu kubelet

# Check Docker/containerd
systemctl status docker
systemctl status containerd

# Reset kubeadm
sudo kubeadm reset

# Clean iptables
sudo iptables -F && sudo iptables -t nat -F

# Check ports
sudo netstat -tulpn | grep -E '6443|2379|10250'
```

---

## Common Installation Issues

1. **Swap enabled**: Disable with `swapoff -a`
1. **Firewall blocking**: Configure ports
1. **Container runtime**: Ensure Docker/containerd running
1. **Network plugin**: Install CNI plugin
1. **DNS issues**: Check CoreDNS pods

---

## Verification Steps

```bash
# Check all components
kubectl get all --all-namespaces

# Test deployment
kubectl create deployment test --image=nginx
kubectl expose deployment test --port=80
kubectl get svc test

# Clean up test
kubectl delete deployment test
kubectl delete svc test
```

---

## Minikube Tips

1. **Resource allocation**: Start with sufficient resources
1. **Driver selection**: Docker driver recommended
1. **Addon management**: Enable only needed addons
1. **Profile usage**: Separate environments
1. **Cleanup**: Regular `minikube delete` and restart

---

## Configuration Best Practices

1. **Backup configs**: Keep kubeconfig safe
1. **Use contexts**: Separate environments
1. **Namespace isolation**: Default namespace per project
1. **Resource limits**: Set appropriate limits
1. **Regular updates**: Keep tools updated

---

## Summary

1. Multiple installation options available
1. Minikube best for local development
1. Kind great for CI/CD testing
1. K3s for resource-constrained environments
1. Cloud services for production workloads
