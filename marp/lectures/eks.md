# Amazon EKS Deep Dive
## Kubernetes on AWS Made Simple

<svg width="400" height="200" viewBox="0 0 400 200">
  <!-- AWS Logo Background -->
  <rect width="400" height="200" fill="#232F3E" rx="10"/>
  <!-- Kubernetes Logo -->
  <circle cx="120" cy="100" r="40" fill="#326CE5"/>
  <polygon points="120,70 135,90 135,110 120,130 105,110 105,90" fill="white"/>
  <!-- EKS Text -->
  <text x="200" y="90" font-family="Arial" font-size="32" font-weight="bold" fill="#FF9900">EKS</text>
  <text x="200" y="120" font-family="Arial" font-size="16" fill="white">Elastic Kubernetes Service</text>
</svg>

---

## What is Amazon EKS?

<svg width="600" height="300" viewBox="0 0 600 300">
  <!-- Definition Box -->
  <rect width="580" height="280" x="10" y="10" fill="#E8F4FD" stroke="#0073BB" stroke-width="2" rx="10"/>

  <!-- Kubernetes Icon -->
  <circle cx="80" cy="80" r="30" fill="#326CE5"/>
  <polygon points="80,60 90,75 90,85 80,100 70,85 70,75" fill="white"/>

  <!-- Plus Sign -->
  <text x="130" y="90" font-family="Arial" font-size="40" fill="#666">+</text>

  <!-- AWS Icon -->
  <rect x="170" y="50" width="60" height="60" fill="#FF9900" rx="5"/>
  <text x="185" y="85" font-family="Arial" font-size="12" font-weight="bold" fill="white">AWS</text>

  <!-- Equals -->
  <text x="250" y="90" font-family="Arial" font-size="40" fill="#666">=</text>

  <!-- EKS -->
  <rect x="290" y="50" width="100" height="60" fill="#232F3E" rx="5"/>
  <text x="315" y="85" font-family="Arial" font-size="16" font-weight="bold" fill="#FF9900">EKS</text>

  <!-- Description -->
  <text x="50" y="150" font-family="Arial" font-size="18" font-weight="bold" fill="#333">Managed Kubernetes Service</text>
  <text x="50" y="180" font-family="Arial" font-size="14" fill="#666">• Fully managed control plane</text>
  <text x="50" y="200" font-family="Arial" font-size="14" fill="#666">• AWS native integrations</text>
  <text x="50" y="220" font-family="Arial" font-size="14" fill="#666">• High availability and security</text>
  <text x="50" y="240" font-family="Arial" font-size="14" fill="#666">• Automatic scaling and updates</text>
</svg>

---

## Why Choose EKS?

<svg width="600" height="350" viewBox="0 0 600 350">
  <!-- Benefits Grid -->
  <g>
    <!-- Row 1 -->
    <rect x="20" y="20" width="120" height="80" fill="#E8F8F5" stroke="#00D4AA" stroke-width="2" rx="5"/>
    <text x="80" y="45" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#00695C">Managed</text>
    <text x="80" y="60" font-family="Arial" font-size="12" text-anchor="middle" fill="#00695C">Control Plane</text>
    <circle cx="80" cy="80" r="8" fill="#00D4AA"/>

    <rect x="160" y="20" width="120" height="80" fill="#FFF3E0" stroke="#FF9800" stroke-width="2" rx="5"/>
    <text x="220" y="45" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#E65100">AWS</text>
    <text x="220" y="60" font-family="Arial" font-size="12" text-anchor="middle" fill="#E65100">Integration</text>
    <polygon points="220,70 225,80 215,80" fill="#FF9800"/>

    <rect x="300" y="20" width="120" height="80" fill="#E3F2FD" stroke="#2196F3" stroke-width="2" rx="5"/>
    <text x="360" y="45" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#0D47A1">High</text>
    <text x="360" y="60" font-family="Arial" font-size="12" text-anchor="middle" fill="#0D47A1">Availability</text>
    <rect x="350" y="70" width="20" height="10" fill="#2196F3"/>

    <!-- Row 2 -->
    <rect x="20" y="120" width="120" height="80" fill="#FCE4EC" stroke="#E91E63" stroke-width="2" rx="5"/>
    <text x="80" y="145" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#880E4F">Security</text>
    <text x="80" y="160" font-family="Arial" font-size="12" text-anchor="middle" fill="#880E4F">& Compliance</text>
    <circle cx="80" cy="180" r="8" fill="#E91E63"/>
    <text x="80" y="185" font-family="Arial" font-size="8" text-anchor="middle" fill="white">🔒</text>

    <rect x="160" y="120" width="120" height="80" fill="#F3E5F5" stroke="#9C27B0" stroke-width="2" rx="5"/>
    <text x="220" y="145" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#4A148C">Auto</text>
    <text x="220" y="160" font-family="Arial" font-size="12" text-anchor="middle" fill="#4A148C">Scaling</text>
    <polygon points="210,175 220,185 230,175" fill="#9C27B0"/>

    <rect x="300" y="120" width="120" height="80" fill="#E8F5E8" stroke="#4CAF50" stroke-width="2" rx="5"/>
    <text x="360" y="145" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#1B5E20">Cost</text>
    <text x="360" y="160" font-family="Arial" font-size="12" text-anchor="middle" fill="#1B5E20">Optimization</text>
    <text x="360" y="185" font-family="Arial" font-size="16" text-anchor="middle" fill="#4CAF50">$</text>

    <!-- Bottom Text -->
    <text x="300" y="240" font-family="Arial" font-size="18" font-weight="bold" text-anchor="middle" fill="#333">Key Benefits of Amazon EKS</text>
    <text x="300" y="270" font-family="Arial" font-size="14" text-anchor="middle" fill="#666">Simplified Kubernetes management with enterprise-grade features</text>
  </g>
</svg>

---

## EKS Architecture Overview

<svg width="700" height="400" viewBox="0 0 700 400">
  <!-- AWS Cloud Background -->
  <rect width="680" height="380" x="10" y="10" fill="#F0F8FF" stroke="#4A90E2" stroke-width="2" rx="10"/>
  <text x="350" y="35" font-family="Arial" font-size="16" font-weight="bold" text-anchor="middle" fill="#4A90E2">AWS Cloud</text>

  <!-- Control Plane -->
  <rect x="50" y="60" width="200" height="120" fill="#232F3E" stroke="#FF9900" stroke-width="2" rx="5"/>
  <text x="150" y="85" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#FF9900">EKS Control Plane</text>
  <text x="150" y="105" font-family="Arial" font-size="10" text-anchor="middle" fill="white">• API Server</text>
  <text x="150" y="120" font-family="Arial" font-size="10" text-anchor="middle" fill="white">• etcd</text>
  <text x="150" y="135" font-family="Arial" font-size="10" text-anchor="middle" fill="white">• Controller Manager</text>
  <text x="150" y="150" font-family="Arial" font-size="10" text-anchor="middle" fill="white">• Scheduler</text>

  <!-- Worker Nodes -->
  <g>
    <!-- Node 1 -->
    <rect x="300" y="80" width="100" height="80" fill="#E8F4FD" stroke="#0073BB" stroke-width="2" rx="5"/>
    <text x="350" y="100" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#0073BB">Worker Node 1</text>
    <circle cx="330" cy="125" r="10" fill="#4CAF50"/>
    <circle cx="350" cy="125" r="10" fill="#4CAF50"/>
    <circle cx="370" cy="125" r="10" fill="#4CAF50"/>
    <text x="350" y="150" font-family="Arial" font-size="8" text-anchor="middle" fill="#666">Pods</text>

    <!-- Node 2 -->
    <rect x="420" y="80" width="100" height="80" fill="#E8F4FD" stroke="#0073BB" stroke-width="2" rx="5"/>
    <text x="470" y="100" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#0073BB">Worker Node 2</text>
    <circle cx="450" cy="125" r="10" fill="#4CAF50"/>
    <circle cx="470" cy="125" r="10" fill="#4CAF50"/>
    <circle cx="490" cy="125" r="10" fill="#4CAF50"/>
    <text x="470" y="150" font-family="Arial" font-size="8" text-anchor="middle" fill="#666">Pods</text>

    <!-- Node 3 -->
    <rect x="540" y="80" width="100" height="80" fill="#E8F4FD" stroke="#0073BB" stroke-width="2" rx="5"/>
    <text x="590" y="100" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#0073BB">Worker Node 3</text>
    <circle cx="570" cy="125" r="10" fill="#4CAF50"/>
    <circle cx="590" cy="125" r="10" fill="#4CAF50"/>
    <circle cx="610" cy="125" r="10" fill="#4CAF50"/>
    <text x="590" y="150" font-family="Arial" font-size="8" text-anchor="middle" fill="#666">Pods</text>
  </g>

  <!-- Connections -->
  <line x1="250" y1="120" x2="300" y2="120" stroke="#666" stroke-width="2"/>
  <line x1="250" y1="120" x2="420" y2="120" stroke="#666" stroke-width="2"/>
  <line x1="250" y1="120" x2="540" y2="120" stroke="#666" stroke-width="2"/>

  <!-- VPC -->
  <rect x="280" y="200" width="380" height="150" fill="none" stroke="#FF6B35" stroke-width="2" stroke-dasharray="5,5" rx="5"/>
  <text x="470" y="220" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#FF6B35">Amazon VPC</text>

  <!-- Subnets -->
  <rect x="300" y="240" width="100" height="50" fill="#FFF8E1" stroke="#FFC107" stroke-width="1" rx="3"/>
  <text x="350" y="260" font-family="Arial" font-size="10" text-anchor="middle" fill="#F57C00">Subnet A</text>
  <text x="350" y="275" font-family="Arial" font-size="8" text-anchor="middle" fill="#F57C00">AZ-1a</text>

  <rect x="420" y="240" width="100" height="50" fill="#FFF8E1" stroke="#FFC107" stroke-width="1" rx="3"/>
  <text x="470" y="260" font-family="Arial" font-size="10" text-anchor="middle" fill="#F57C00">Subnet B</text>
  <text x="470" y="275" font-family="Arial" font-size="8" text-anchor="middle" fill="#F57C00">AZ-1b</text>

  <rect x="540" y="240" width="100" height="50" fill="#FFF8E1" stroke="#FFC107" stroke-width="1" rx="3"/>
  <text x="590" y="260" font-family="Arial" font-size="10" text-anchor="middle" fill="#F57C00">Subnet C</text>
  <text x="590" y="275" font-family="Arial" font-size="8" text-anchor="middle" fill="#F57C00">AZ-1c</text>

  <!-- Load Balancer -->
  <rect x="300" y="310" width="240" height="30" fill="#4CAF50" stroke="#2E7D32" stroke-width="2" rx="5"/>
  <text x="420" y="330" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Application Load Balancer</text>
</svg>

---

## EKS Control Plane Components

<svg width="600" height="400" viewBox="0 0 600 400">
  <!-- Control Plane Container -->
  <rect x="50" y="50" width="500" height="300" fill="#232F3E" stroke="#FF9900" stroke-width="3" rx="10"/>
  <text x="300" y="80" font-family="Arial" font-size="18" font-weight="bold" text-anchor="middle" fill="#FF9900">EKS Control Plane (Managed by AWS)</text>

  <!-- API Server -->
  <rect x="80" y="110" width="200" height="60" fill="#4A90E2" stroke="#2C5F8A" stroke-width="2" rx="5"/>
  <text x="180" y="135" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Kubernetes API Server</text>
  <text x="180" y="155" font-family="Arial" font-size="10" text-anchor="middle" fill="white">RESTful API, Authentication, Authorization</text>

  <!-- etcd -->
  <rect x="320" y="110" width="200" height="60" fill="#FF6B6B" stroke="#C44D4D" stroke-width="2" rx="5"/>
  <text x="420" y="135" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">etcd Database</text>
  <text x="420" y="155" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Distributed key-value store</text>

  <!-- Controller Manager -->
  <rect x="80" y="200" width="200" height="60" fill="#4ECDC4" stroke="#35A29B" stroke-width="2" rx="5"/>
  <text x="180" y="225" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Controller Manager</text>
  <text x="180" y="245" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Watches cluster state, makes changes</text>

  <!-- Scheduler -->
  <rect x="320" y="200" width="200" height="60" fill="#95E1D3" stroke="#6BB8AB" stroke-width="2" rx="5"/>
  <text x="420" y="225" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Scheduler</text>
  <text x="420" y="245" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Assigns pods to nodes</text>

  <!-- Arrows showing communication -->
  <line x1="180" y1="170" x2="180" y2="200" stroke="#FFD93D" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="420" y1="170" x2="420" y2="200" stroke="#FFD93D" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="280" y1="140" x2="320" y2="140" stroke="#FFD93D" stroke-width="2" marker-end="url(#arrowhead)"/>
  <line x1="280" y1="230" x2="320" y2="230" stroke="#FFD93D" stroke-width="2" marker-end="url(#arrowhead)"/>

  <!-- Arrow marker definition -->
  <defs>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#FFD93D"/>
    </marker>
  </defs>

  <!-- Benefits box -->
  <rect x="100" y="290" width="400" height="40" fill="#E8F5E8" stroke="#4CAF50" stroke-width="1" rx="5"/>
  <text x="300" y="310" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#2E7D32">✓ Fully Managed ✓ High Availability ✓ Auto Updates ✓ AWS Integration</text>
</svg>

---

## Worker Node Components

<svg width="600" height="400" viewBox="0 0 600 400">
  <!-- Worker Node Container -->
  <rect x="50" y="50" width="500" height="320" fill="#E8F4FD" stroke="#0073BB" stroke-width="3" rx="10"/>
  <text x="300" y="80" font-family="Arial" font-size="18" font-weight="bold" text-anchor="middle" fill="#0073BB">EKS Worker Node (Your Responsibility)</text>

  <!-- kubelet -->
  <rect x="80" y="110" width="180" height="60" fill="#326CE5" stroke="#1E4A73" stroke-width="2" rx="5"/>
  <text x="170" y="135" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">kubelet</text>
  <text x="170" y="155" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Pod lifecycle management</text>

  <!-- kube-proxy -->
  <rect x="340" y="110" width="180" height="60" fill="#FF7043" stroke="#D84315" stroke-width="2" rx="5"/>
  <text x="430" y="135" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">kube-proxy</text>
  <text x="430" y="155" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Network proxy & load balancing</text>

  <!-- Container Runtime -->
  <rect x="80" y="190" width="180" height="60" fill="#4CAF50" stroke="#2E7D32" stroke-width="2" rx="5"/>
  <text x="170" y="215" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Container Runtime</text>
  <text x="170" y="235" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Docker / containerd</text>

  <!-- AWS VPC CNI -->
  <rect x="340" y="190" width="180" height="60" fill="#FF9800" stroke="#E65100" stroke-width="2" rx="5"/>
  <text x="430" y="215" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">AWS VPC CNI</text>
  <text x="430" y="235" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Native VPC networking</text>

  <!-- Pods Section -->
  <rect x="80" y="270" width="440" height="80" fill="#F3E5F5" stroke="#9C27B0" stroke-width="2" rx="5"/>
  <text x="300" y="295" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#7B1FA2">Application Pods</text>

  <!-- Pod examples -->
  <circle cx="150" cy="320" r="15" fill="#E91E63"/>
  <text x="150" y="325" font-family="Arial" font-size="8" text-anchor="middle" fill="white">App1</text>

  <circle cx="220" cy="320" r="15" fill="#3F51B5"/>
  <text x="220" y="325" font-family="Arial" font-size="8" text-anchor="middle" fill="white">App2</text>

  <circle cx="290" cy="320" r="15" fill="#009688"/>
  <text x="290" y="325" font-family="Arial" font-size="8" text-anchor="middle" fill="white">DB</text>

  <circle cx="360" cy="320" r="15" fill="#FF5722"/>
  <text x="360" y="325" font-family="Arial" font-size="8" text-anchor="middle" fill="white">Cache</text>

  <circle cx="430" cy="320" r="15" fill="#795548"/>
  <text x="430" y="325" font-family="Arial" font-size="8" text-anchor="middle" fill="white">Nginx</text>
</svg>

---

## EKS Cluster Creation Methods

<svg width="700" height="350" viewBox="0 0 700 350">
  <!-- Title -->
  <text x="350" y="30" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle" fill="#333">Ways to Create EKS Clusters</text>

  <!-- AWS Console -->
  <rect x="50" y="60" width="120" height="100" fill="#FF9900" stroke="#E68800" stroke-width="2" rx="8"/>
  <text x="110" y="85" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="white">AWS Console</text>
  <rect x="70" y="95" width="80" height="5" fill="white" rx="2"/>
  <rect x="70" y="105" width="60" height="5" fill="white" rx="2"/>
  <rect x="70" y="115" width="70" height="5" fill="white" rx="2"/>
  <text x="110" y="140" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Web Interface</text>
  <text x="110" y="175" font-family="Arial" font-size="9" text-anchor="middle" fill="#333">• Easy to use</text>
  <text x="110" y="190" font-family="Arial" font-size="9" text-anchor="middle" fill="#333">• Visual interface</text>

  <!-- AWS CLI -->
  <rect x="200" y="60" width="120" height="100" fill="#232F3E" stroke="#1A252F" stroke-width="2" rx="8"/>
  <text x="260" y="85" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#FF9900">AWS CLI</text>
  <text x="260" y="100" font-family="monospace" font-size="8" text-anchor="middle" fill="#00FF00">$ aws eks</text>
  <text x="260" y="115" font-family="monospace" font-size="8" text-anchor="middle" fill="#00FF00">create-cluster</text>
  <text x="260" y="130" font-family="monospace" font-size="8" text-anchor="middle" fill="#00FF00">--name my-cluster</text>
  <text x="260" y="175" font-family="Arial" font-size="9" text-anchor="middle" fill="#333">• Command line</text>
  <text x="260" y="190" font-family="Arial" font-size="9" text-anchor="middle" fill="#333">• Scriptable</text>

  <!-- eksctl -->
  <rect x="350" y="60" width="120" height="100" fill="#326CE5" stroke="#1E4A73" stroke-width="2" rx="8"/>
  <text x="410" y="85" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="white">eksctl</text>
  <text x="410" y="100" font-family="monospace" font-size="8" text-anchor="middle" fill="#E8F4FD">$ eksctl create</text>
  <text x="410" y="115" font-family="monospace" font-size="8" text-anchor="middle" fill="#E8F4FD">cluster --name</text>
  <text x="410" y="130" font-family="monospace" font-size="8" text-anchor="middle" fill="#E8F4FD">my-cluster</text>
  <text x="410" y="175" font-family="Arial" font-size="9" text-anchor="middle" fill="#333">• Kubernetes native</text>
  <text x="410" y="190" font-family="Arial" font-size="9" text-anchor="middle" fill="#333">• Simple commands</text>

  <!-- Terraform -->
  <rect x="500" y="60" width="120" height="100" fill="#623CE4" stroke="#4B2DB8" stroke-width="2" rx="8"/>
  <text x="560" y="85" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="white">Terraform</text>
  <text x="560" y="100" font-family="monospace" font-size="8" text-anchor="middle" fill="#E8E4FD">resource</text>
  <text x="560" y="115" font-family="monospace" font-size="8" text-anchor="middle" fill="#E8E4FD">"aws_eks_cluster"</text>
  <text x="560" y="130" font-family="monospace" font-size="8" text-anchor="middle" fill="#E8E4FD">"main" {}</text>
  <text x="560" y="175" font-family="Arial" font-size="9" text-anchor="middle" fill="#333">• Infrastructure as Code</text>
  <text x="560" y="190" font-family="Arial" font-size="9" text-anchor="middle" fill="#333">• Reproducible</text>

  <!-- Comparison Table -->
  <rect x="50" y="220" width="570" height="110" fill="#F8F9FA" stroke="#DEE2E6" stroke-width="1" rx="5"/>
  <text x="335" y="240" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#333">Comparison</text>

  <line x1="70" y1="250" x2="600" y2="250" stroke="#DEE2E6" stroke-width="1"/>

  <!-- Headers -->
  <text x="110" y="265" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle" fill="#495057">Console</text>
  <text x="260" y="265" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle" fill="#495057">CLI</text>
  <text x="410" y="265" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle" fill="#495057">eksctl</text>
  <text x="560" y="265" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle" fill="#495057">Terraform</text>

  <!-- Ease of use -->
  <text x="70" y="285" font-family="Arial" font-size="9" fill="#666">Ease:</text>
  <text x="110" y="285" font-family="Arial" font-size="9" text-anchor="middle" fill="#28A745">★★★★★</text>
  <text x="260" y="285" font-family="Arial" font-size="9" text-anchor="middle" fill="#FFC107">★★★☆☆</text>
  <text x="410" y="285" font-family="Arial" font-size="9" text-anchor="middle" fill="#28A745">★★★★☆</text>
  <text x="560" y="285" font-family="Arial" font-size="9" text-anchor="middle" fill="#FFC107">★★☆☆☆</text>

  <!-- Automation -->
  <text x="70" y="305" font-family="Arial" font-size="9" fill="#666">Automation:</text>
  <text x="110" y="305" font-family="Arial" font-size="9" text-anchor="middle" fill="#DC3545">★☆☆☆☆</text>
  <text x="260" y="305" font-family="Arial" font-size="9" text-anchor="middle" fill="#28A745">★★★★☆</text>
  <text x="410" y="305" font-family="Arial" font-size="9" text-anchor="middle" fill="#28A745">★★★★☆</text>
  <text x="560" y="305" font-family="Arial" font-size="9" text-anchor="middle" fill="#28A745">★★★★★</text>

  <!-- Version Control -->
  <text x="70" y="320" font-family="Arial" font-size="9" fill="#666">Version Control:</text>
  <text x="110" y="320" font-family="Arial" font-size="9" text-anchor="middle" fill="#DC3545">★☆☆☆☆</text>
  <text x="260" y="320" font-family="Arial" font-size="9" text-anchor="middle" fill="#FFC107">★★★☆☆</text>
  <text x="410" y="320" font-family="Arial" font-size="9" text-anchor="middle" fill="#FFC107">★★★☆☆</text>
  <text x="560" y="320" font-family="Arial" font-size="9" text-anchor="middle" fill="#28A745">★★★★★</text>
</svg>

---

## EKS Node Groups Overview

<svg width="700" height="400" viewBox="0 0 700 400">
  <!-- Title -->
  <text x="350" y="30" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle" fill="#333">EKS Node Group Types</text>

  <!-- Managed Node Groups -->
  <rect x="50" y="60" width="200" height="150" fill="#E8F5E8" stroke="#4CAF50" stroke-width="3" rx="10"/>
  <text x="150" y="85" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#2E7D32">Managed Node Groups</text>

  <!-- EC2 instances in managed group -->
  <rect x="70" y="100" width="40" height="30" fill="#FF9900" stroke="#E68800" stroke-width="1" rx="3"/>
  <text x="90" y="120" font-family="Arial" font-size="8" text-anchor="middle" fill="white">EC2</text>

  <rect x="120" y="100" width="40" height="30" fill="#FF9900" stroke="#E68800" stroke-width="1" rx="3"/>
  <text x="140" y="120" font-family="Arial" font-size="8" text-anchor="middle" fill="white">EC2</text>

  <rect x="170" y="100" width="40" height="30" fill="#FF9900" stroke="#E68800" stroke-width="1" rx="3"/>
  <text x="190" y="120" font-family="Arial" font-size="8" text-anchor="middle" fill="white">EC2</text>

  <text x="150" y="150" font-family="Arial" font-size="10" text-anchor="middle" fill="#2E7D32">✓ Automated provisioning</text>
  <text x="150" y="165" font-family="Arial" font-size="10" text-anchor="middle" fill="#2E7D32">✓ Auto Scaling Groups</text>
  <text x="150" y="180" font-family="Arial" font-size="10" text-anchor="middle" fill="#2E7D32">✓ Managed updates</text>
  <text x="150" y="195" font-family="Arial" font-size="10" text-anchor="middle" fill="#2E7D32">✓ AWS optimized AMIs</text>

  <!-- Self-Managed Node Groups -->
  <rect x="275" y="60" width="200" height="150" fill="#FFF3E0" stroke="#FF9800" stroke-width="3" rx="10"/>
  <text x="375" y="85" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#E65100">Self-Managed Nodes</text>

  <!-- EC2 instances in self-managed -->
  <rect x="295" y="100" width="40" height="30" fill="#2196F3" stroke="#1976D2" stroke-width="1" rx="3"/>
  <text x="315" y="120" font-family="Arial" font-size="8" text-anchor="middle" fill="white">EC2</text>

  <rect x="345" y="100" width="40" height="30" fill="#2196F3" stroke="#1976D2" stroke-width="1" rx="3"/>
  <text x="365" y="120" font-family="Arial" font-size="8" text-anchor="middle" fill="white">EC2</text>

  <rect x="395" y="100" width="40" height="30" fill="#2196F3" stroke="#1976D2" stroke-width="1" rx="3"/>
  <text x="415" y="120" font-family="Arial" font-size="8" text-anchor="middle" fill="white">EC2</text>

  <text x="375" y="150" font-family="Arial" font-size="10" text-anchor="middle" fill="#E65100">• Full control over nodes</text>
  <text x="375" y="165" font-family="Arial" font-size="10" text-anchor="middle" fill="#E65100">• Custom AMIs</text>
  <text x="375" y="180" font-family="Arial" font-size="10" text-anchor="middle" fill="#E65100">• Manual management</text>
  <text x="375" y="195" font-family="Arial" font-size="10" text-anchor="middle" fill="#E65100">• More complexity</text>

  <!-- Fargate -->
  <rect x="500" y="60" width="150" height="150" fill="#E3F2FD" stroke="#2196F3" stroke-width="3" rx="10"/>
  <text x="575" y="85" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#1565C0">AWS Fargate</text>

  <!-- Fargate pods -->
  <circle cx="550" cy="110" r="12" fill="#4CAF50"/>
  <text x="550" y="115" font-family="Arial" font-size="8" text-anchor="middle" fill="white">Pod</text>

  <circle cx="600" cy="110" r="12" fill="#4CAF50"/>
  <text x="600" y="115" font-family="Arial" font-size="8" text-anchor="middle" fill="white">Pod</text>

  <circle cx="575" cy="140" r="12" fill="#4CAF50"/>
  <text x="575" y="145" font-family="Arial" font-size="8" text-anchor="middle" fill="white">Pod</text>

  <text x="575" y="170" font-family="Arial" font-size="10" text-anchor="middle" fill="#1565C0">✓ Serverless</text>
  <text x="575" y="185" font-family="Arial" font-size="10" text-anchor="middle" fill="#1565C0">✓ No node management</text>
  <text x="575" y="200" font-family="Arial" font-size="10" text-anchor="middle" fill="#1565C0">✓ Pay per pod</text>

  <!-- Comparison Table -->
  <rect x="50" y="240" width="600" height="130" fill="#F8F9FA" stroke="#DEE2E6" stroke-width="1" rx="5"/>
  <text x="350" y="260" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#333">Feature Comparison</text>

  <!-- Table headers -->
  <text x="80" y="285" font-family="Arial" font-size="11" font-weight="bold" fill="#495057">Feature</text>
  <text x="220" y="285" font-family="Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#495057">Managed</text>
  <text x="350" y="285" font-family="Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#495057">Self-Managed</text>
  <text x="500" y="285" font-family="Arial" font-size="11" font-weight="bold" text-anchor="middle" fill="#495057">Fargate</text>

  <!-- Management -->
  <text x="80" y="305" font-family="Arial" font-size="10" fill="#666">Management</text>
  <text x="220" y="305" font-family="Arial" font-size="10" text-anchor="middle" fill="#28A745">AWS Managed</text>
  <text x="350" y="305" font-family="Arial" font-size="10" text-anchor="middle" fill="#DC3545">You Manage</text>
  <text x="500" y="305" font-family="Arial" font-size="10" text-anchor="middle" fill="#28A745">AWS Managed</text>

  <!-- Cost -->
  <text x="80" y="325" font-family="Arial" font-size="10" fill="#666">Cost</text>
  <text x="220" y="325" font-family="Arial" font-size="10" text-anchor="middle" fill="#28A745">EC2 pricing</text>
  <text x="350" y="325" font-family="Arial" font-size="10" text-anchor="middle" fill="#28A745">EC2 pricing</text>
  <text x="500" y="325" font-family="Arial" font-size="10" text-anchor="middle" fill="#FFC107">Premium pricing</text>

  <!-- Flexibility -->
  <text x="80" y="345" font-family="Arial" font-size="10" fill="#666">Flexibility</text>
  <text x="220" y="345" font-family="Arial" font-size="10" text-anchor="middle" fill="#FFC107">Medium</text>
  <text x="350" y="345" font-family="Arial" font-size="10" text-anchor="middle" fill="#28A745">High</text>
  <text x="500" y="345" font-family="Arial" font-size="10" text-anchor="middle" fill="#DC3545">Low</text>
</svg>

---

## EKS Networking with VPC CNI

<svg width="700" height="400" viewBox="0 0 700 400">
  <!-- VPC Container -->
  <rect x="50" y="50" width="600" height="320" fill="#FFF8E1" stroke="#FF6F00" stroke-width="3" rx="10"/>
  <text x="350" y="80" font-family="Arial" font-size="18" font-weight="bold" text-anchor="middle" fill="#E65100">Amazon VPC</text>

  <!-- Subnet 1 -->
  <rect x="80" y="100" width="250" height="120" fill="#E8F5E8" stroke="#4CAF50" stroke-width="2" rx="5"/>
  <text x="205" y="125" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#2E7D32">Private Subnet A</text>
  <text x="205" y="140" font-family="Arial" font-size="10" text-anchor="middle" fill="#2E7D32">10.0.1.0/24</text>

  <!-- Worker Node 1 -->
  <rect x="100" y="155" width="90" height="50" fill="#2196F3" stroke="#1976D2" stroke-width="2" rx="3"/>
  <text x="145" y="175" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle" fill="white">Worker Node</text>
  <text x="145" y="190" font-family="Arial" font-size="8" text-anchor="middle" fill="white">10.0.1.10</text>

  <!-- Pods in Node 1 -->
  <circle cx="125" cy="185" r="8" fill="#4CAF50"/>
  <text x="125" y="189" font-family="Arial" font-size="6" text-anchor="middle" fill="white">Pod1</text>
  <text x="125" y="200" font-family="Arial" font-size="6" text-anchor="middle" fill="#333">10.0.1.20</text>

  <circle cx="165" cy="185" r="8" fill="#4CAF50"/>
  <text x="165" y="189" font-family="Arial" font-size="6" text-anchor="middle" fill="white">Pod2</text>
  <text x="165" y="200" font-family="Arial" font-size="6" text-anchor="middle" fill="#333">10.0.1.21</text>

  <!-- Worker Node 2 -->
  <rect x="210" y="155" width="90" height="50" fill="#2196F3" stroke="#1976D2" stroke-width="2" rx="3"/>
  <text x="255" y="175" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle" fill="white">Worker Node</text>
  <text x="255" y="190" font-family="Arial" font-size="8" text-anchor="middle" fill="white">10.0.1.11</text>

  <!-- Pods in Node 2 -->
  <circle cx="235" cy="185" r="8" fill="#4CAF50"/>
  <text x="235" y="189" font-family="Arial" font-size="6" text-anchor="middle" fill="white">Pod3</text>
  <text x="235" y="200" font-family="Arial" font-size="6" text-anchor="middle" fill="#333">10.0.1.22</text>

  <circle cx="275" cy="185" r="8" fill="#4CAF50"/>
  <text x="275" y="189" font-family="Arial" font-size="6" text-anchor="middle" fill="white">Pod4</text>
  <text x="275" y="200" font-family="Arial" font-size="6" text-anchor="middle" fill="#333">10.0.1.23</text>

  <!-- Subnet 2 -->
  <rect x="370" y="100" width="250" height="120" fill="#FCE4EC" stroke="#E91E63" stroke-width="2" rx="5"/>
  <text x="495" y="125" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#880E4F">Private Subnet B</text>
  <text x="495" y="140" font-family="Arial" font-size="10" text-anchor="middle" fill="#880E4F">10.0.2.0/24</text>

  <!-- Worker Node 3 -->
  <rect x="390" y="155" width="90" height="50" fill="#9C27B0" stroke="#7B1FA2" stroke-width="2" rx="3"/>
  <text x="435" y="175" font-family="Arial" font-size="10" font-weight="bold" text-anchor="middle" fill="white">Worker Node</text>
  <text x="435" y="190" font-family="Arial" font-size="8" text-anchor="middle" fill="white">10.0.2.10</text>

  <!-- Pods in Node 3 -->
  <circle cx="415" cy="185" r="8" fill="#FF9800"/>
  <text x="415" y="189" font-family="Arial" font-size="6" text-anchor="middle" fill="white">Pod5</text>
  <text x="415" y="200" font-family="Arial" font-size="6" text-anchor="middle" fill="#333">10.0.2.20</text>

  <circle cx="455" cy="185" r="8" fill="#FF9800"/>
  <text x="455" y="189" font-family="Arial" font-size="6" text-anchor="middle" fill="white">Pod6</text>
  <text x="455" y="200" font-family="Arial" font-size="6" text-anchor="middle" fill="#333">10.0.2.21</text>

  <!-- CNI Features -->
  <rect x="80" y="240" width="540" height="110" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="5"/>
  <text x="350" y="265" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#0D47A1">AWS VPC CNI Features</text>

  <!-- Feature list -->
  <text x="100" y="285" font-family="Arial" font-size="11" fill="#1565C0">✓ Native VPC IP addresses for pods</text>
  <text x="100" y="300" font-family="Arial" font-size="11" fill="#1565C0">✓ High performance networking</text>
  <text x="100" y="315" font-family="Arial" font-size="11" fill="#1565C0">✓ Security groups at pod level</text>

  <text x="400" y="285" font-family="Arial" font-size="11" fill="#1565C0">✓ Network policies support</text>
  <text x="400" y="300" font-family="Arial" font-size="11" fill="#1565C0">✓ Multiple ENIs per node</text>
  <text x="400" y="315" font-family="Arial" font-size="11" fill="#1565C0">✓ SNAT/Source NAT control</text>

  <!-- Network flow arrows -->
  <line x1="300" y1="180" x2="370" y2="180" stroke="#FF6F00" stroke-width="3" marker-end="url(#arrow)"/>
  <text x="335" y="175" font-family="Arial" font-size="9" text-anchor="middle" fill="#E65100">Pod-to-Pod</text>

  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#FF6F00"/>
    </marker>
  </defs>
</svg>

---

## EKS Storage Options

<svg width="700" height="400" viewBox="0 0 700 400">
  <!-- Title -->
  <text x="350" y="30" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle" fill="#333">EKS Storage Solutions</text>

  <!-- EBS -->
  <rect x="50" y="60" width="150" height="120" fill="#FF9900" stroke="#E68800" stroke-width="2" rx="8"/>
  <text x="125" y="85" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Amazon EBS</text>
  <text x="125" y="105" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Block Storage</text>

  <!-- EBS disk icon -->
  <rect x="100" y="115" width="50" height="30" fill="#232F3E" stroke="#1A252F" stroke-width="1" rx="3"/>
  <circle cx="125" cy="130" r="8" fill="#FF9900"/>

  <text x="125" y="160" font-family="Arial" font-size="9" text-anchor="middle" fill="white">• Single AZ</text>
  <text x="125" y="175" font-family="Arial" font-size="9" text-anchor="middle" fill="white">• High IOPS</text>

  <!-- EFS -->
  <rect x="225" y="60" width="150" height="120" fill="#4CAF50" stroke="#2E7D32" stroke-width="2" rx="8"/>
  <text x="300" y="85" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Amazon EFS</text>
  <text x="300" y="105" font-family="Arial" font-size="10" text-anchor="middle" fill="white">File Storage</text>

  <!-- EFS network icon -->
  <circle cx="275" cy="130" r="8" fill="white"/>
  <circle cx="300" cy="130" r="8" fill="white"/>
  <circle cx="325" cy="130" r="8" fill="white"/>
  <line x1="275" y1="130" x2="325" y2="130" stroke="white" stroke-width="2"/>

  <text x="300" y="160" font-family="Arial" font-size="9" text-anchor="middle" fill="white">• Multi-AZ</text>
  <text x="300" y="175" font-family="Arial" font-size="9" text-anchor="middle" fill="white">• Shared access</text>

  <!-- FSx -->
  <rect x="400" y="60" width="150" height="120" fill="#9C27B0" stroke="#7B1FA2" stroke-width="2" rx="8"/>
  <text x="475" y="85" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Amazon FSx</text>
  <text x="475" y="105" font-family="Arial" font-size="10" text-anchor="middle" fill="white">High Performance</text>

  <!-- FSx performance icon -->
  <polygon points="450,120 475,135 500,120 475,145" fill="white"/>
  <text x="475" y="135" font-family="Arial" font-size="8" text-anchor="middle" fill="#9C27B0">⚡</text>

  <text x="475" y="160" font-family="Arial" font-size="9" text-anchor="middle" fill="white">• Lustre/NetApp</text>
  <text x="475" y="175" font-family="Arial" font-size="9" text-anchor="middle" fill="white">• HPC workloads</text>

  <!-- CSI Drivers -->
  <rect x="50" y="200" width="500" height="80" fill="#E3F2FD" stroke="#1976D2" stroke-width="2" rx="8"/>
  <text x="300" y="225" font-family="Arial" font-size="16" font-weight="bold" text-anchor="middle" fill="#0D47A1">Container Storage Interface (CSI) Drivers</text>

  <!-- CSI Driver boxes -->
  <rect x="80" y="240" width="100" height="25" fill="#2196F3" stroke="#1565C0" stroke-width="1" rx="3"/>
  <text x="130" y="255" font-family="Arial" font-size="10" text-anchor="middle" fill="white">EBS CSI Driver</text>

  <rect x="200" y="240" width="100" height="25" fill="#4CAF50" stroke="#2E7D32" stroke-width="1" rx="3"/>
  <text x="250" y="255" font-family="Arial" font-size="10" text-anchor="middle" fill="white">EFS CSI Driver</text>

  <rect x="320" y="240" width="100" height="25" fill="#9C27B0" stroke="#7B1FA2" stroke-width="1" rx="3"/>
  <text x="370" y="255" font-family="Arial" font-size="10" text-anchor="middle" fill="white">FSx CSI Driver</text>

  <rect x="440" y="240" width="100" height="25" fill="#FF5722" stroke="#D84315" stroke-width="1" rx="3"/>
  <text x="490" y="255" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Snapshot CSI</text>

  <!-- Storage Classes Example -->
  <rect x="50" y="300" width="600" height="80" fill="#F5F5F5" stroke="#BDBDBD" stroke-width="1" rx="5"/>
  <text x="350" y="320" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="#333">Storage Class Examples</text>

  <!-- YAML-like examples -->
  <text x="70" y="340" font-family="monospace" font-size="9" fill="#1976D2">apiVersion: storage.k8s.io/v1</text>
  <text x="70" y="355" font-family="monospace" font-size="9" fill="#1976D2">kind: StorageClass</text>
  <text x="70" y="370" font-family="monospace" font-size="9" fill="#1976D2">provisioner: ebs.csi.aws.com</text>

  <text x="350" y="340" font-family="monospace" font-size="9" fill="#4CAF50">apiVersion: storage.k8s.io/v1</text>
  <text x="350" y="355" font-family="monospace" font-size="9" fill="#4CAF50">kind: StorageClass</text>
  <text x="350" y="370" font-family="monospace" font-size="9" fill="#4CAF50">provisioner: efs.csi.aws.com</text>
</svg>

---

## EKS Security Best Practices

<svg width="700" height="450" viewBox="0 0 700 450">
  <!-- Title -->
  <text x="350" y="30" font-family="Arial" font-size="20" font-weight="bold" text-anchor="middle" fill="#333">EKS Security Layers</text>

  <!-- Security Pyramid -->
  <!-- Layer 1: Infrastructure -->
  <polygon points="150,380 550,380 500,320 200,320" fill="#FF5722" stroke="#D84315" stroke-width="2"/>
  <text x="350" y="355" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Infrastructure Security</text>
  <text x="350" y="370" font-family="Arial" font-size="10" text-anchor="middle" fill="white">VPC, Security Groups, NACLs, IAM</text>

  <!-- Layer 2: Cluster -->
  <polygon points="200,320 500,320 450,260 250,260" fill="#FF9800" stroke="#F57C00" stroke-width="2"/>
  <text x="350" y="295" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Cluster Security</text>
  <text x="350" y="310" font-family="Arial" font-size="10" text-anchor="middle" fill="white">RBAC, Pod Security, Network Policies</text>

  <!-- Layer 3: Workload -->
  <polygon points="250,260 450,260 400,200 300,200" fill="#FFC107" stroke="#FF8F00" stroke-width="2"/>
  <text x="350" y="235" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Workload Security</text>
  <text x="350" y="250" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Image Scanning, Admission Controllers</text>

  <!-- Layer 4: Application -->
  <polygon points="300,200 400,200 375,140 325,140" fill="#4CAF50" stroke="#388E3C" stroke-width="2"/>
  <text x="350" y="175" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Application</text>
  <text x="350" y="190" font-family="Arial" font-size="10" text-anchor="middle" fill="white">Secrets, Encryption</text>

  <!-- Layer 5: Data -->
  <polygon points="325,140 375,140 350,80 350,80" fill="#2196F3" stroke="#1976D2" stroke-width="2"/>
  <text x="350" y="115" font-family="Arial" font-size="14" font-weight="bold" text-anchor="middle" fill="white">Data</text>

  <!-- Security Features on the right -->
  <rect x="570" y="80" width="120" height="300" fill="#F8F9FA" stroke="#DEE2E6" stroke-width="1" rx="5"/>
  <text x="630" y="105" font-family="Arial" font-size="12" font-weight="bold" text-anchor="middle" fill="#333">Security Features</text>

  <!-- IAM -->
  <circle cx="590" cy="130" r="8" fill="#FF5722"/>
  <text x="610" y="135" font-family="Arial" font-size="10" fill="#333">IAM Roles</text>

  <!-- RBAC -->
  <circle cx="590" cy="150" r="8" fill="#FF9800"/>
  <text x="610" y="155" font-family="Arial" font-size="10" fill="#333">RBAC</text>

  <!-- Pod Security -->
  <circle cx="590" cy="170" r="8" fill="#FFC107"/>
  <text x="610" y="175" font-family="Arial" font-size="10" fill="#333">Pod Security</text>

  <!-- Network Policies -->
  <circle cx="590" cy="190" r="8" fill="#4CAF50"/>
  <text x="610" y="195" font-family="Arial" font-size="10" fill="#333">Network Policies</text>

  <!-- Secrets -->
  <circle cx="590" cy="210" r="8" fill="#2196F3"/>
  <text x="610" y="215" font-family="Arial" font-size="10" fill="#333">Secrets Manager</text>
