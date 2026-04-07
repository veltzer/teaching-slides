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

![local_development_tools](svg/courses/devops/k8s-introduction/03_installation_and_configuration/local_development_tools.svg)

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

![minikube_drivers](svg/courses/devops/k8s-introduction/03_installation_and_configuration/minikube_drivers.svg)

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

![minikube_start_process](svg/courses/devops/k8s-introduction/03_installation_and_configuration/minikube_start_process.svg)

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

![cloud_managed_services](svg/courses/devops/k8s-introduction/03_installation_and_configuration/cloud_managed_services.svg)

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

![high_availability_setup](svg/courses/devops/k8s-introduction/03_installation_and_configuration/high_availability_setup.svg)

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
