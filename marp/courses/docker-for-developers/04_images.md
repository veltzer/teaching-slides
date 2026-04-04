# Creating Your Own Docker Images

---

## What is a Dockerfile

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="200" y="10" width="200" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="35" text-anchor="middle" font-size="12" font-weight="bold">Dockerfile</text>
  <rect x="30" y="70" width="120" height="35" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="92" text-anchor="middle" font-size="11">FROM</text>
  <rect x="170" y="70" width="120" height="35" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="230" y="92" text-anchor="middle" font-size="11">COPY / ADD</text>
  <rect x="310" y="70" width="120" height="35" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="370" y="92" text-anchor="middle" font-size="11">RUN</text>
  <rect x="450" y="70" width="120" height="35" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="92" text-anchor="middle" font-size="11">CMD</text>
  <line x1="300" y1="50" x2="90" y2="70" stroke="#333" stroke-width="1.5"/>
  <line x1="300" y1="50" x2="230" y2="70" stroke="#333" stroke-width="1.5"/>
  <line x1="300" y1="50" x2="370" y2="70" stroke="#333" stroke-width="1.5"/>
  <line x1="300" y1="50" x2="510" y2="70" stroke="#333" stroke-width="1.5"/>
  <rect x="30" y="130" width="540" height="50" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="150" text-anchor="middle" font-size="11" fill="#555">Text instructions that define how to build</text>
  <text x="300" y="168" text-anchor="middle" font-size="11" fill="#555">a Docker image step by step</text>
</svg>

---

## Basic Dockerfile Structure

| Instruction | Purpose | Example |
|-------------|---------|---------|
| FROM | Base image | `FROM ubuntu:22.04` |
| WORKDIR | Set working directory | `WORKDIR /app` |
| COPY | Copy files | `COPY . /app` |
| RUN | Execute commands | `RUN apt-get update` |
| CMD | Default command | `CMD ["python", "app.py"]` |
| EXPOSE | Port information | `EXPOSE 8080` |

---

## Dockerfile Example

```dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
```

---

## Image Building Process

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_03_images" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="60" width="120" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="95" text-anchor="middle" font-size="11" font-weight="bold">Dockerfile</text>
  <text x="90" y="115" text-anchor="middle" font-size="10" fill="#555">Instructions</text>
  <rect x="240" y="60" width="120" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="90" text-anchor="middle" font-size="11" font-weight="bold">docker build</text>
  <text x="300" y="110" text-anchor="middle" font-size="10" fill="#555">Layer by layer</text>
  <text x="300" y="125" text-anchor="middle" font-size="10" fill="#555">execution</text>
  <rect x="450" y="60" width="120" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="95" text-anchor="middle" font-size="11" font-weight="bold">Image</text>
  <text x="510" y="115" text-anchor="middle" font-size="10" fill="#555">Ready to run</text>
  <line x1="150" y1="100" x2="238" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_images)"/>
  <line x1="360" y1="100" x2="448" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_03_images)"/>
  <text x="195" y="90" text-anchor="middle" font-size="10" fill="#666">parse</text>
  <text x="405" y="90" text-anchor="middle" font-size="10" fill="#666">create</text>
</svg>

---

## Build Context

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_03_images" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="20" width="160" height="160" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="110" y="45" text-anchor="middle" font-size="12" font-weight="bold">Build Context (.)</text>
  <rect x="50" y="60" width="120" height="25" fill="#e3f2fd" stroke="#333" stroke-width="1" rx="3"/>
  <text x="110" y="77" text-anchor="middle" font-size="10">Dockerfile</text>
  <rect x="50" y="95" width="120" height="25" fill="#e8f5e9" stroke="#333" stroke-width="1" rx="3"/>
  <text x="110" y="112" text-anchor="middle" font-size="10">app source code</text>
  <rect x="50" y="130" width="120" height="25" fill="#f3e5f5" stroke="#333" stroke-width="1" rx="3"/>
  <text x="110" y="147" text-anchor="middle" font-size="10">config files</text>
  <line x1="190" y1="100" x2="280" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_03_images)"/>
  <text x="235" y="90" text-anchor="middle" font-size="10" fill="#666">sent to</text>
  <rect x="282" y="55" width="130" height="90" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="347" y="85" text-anchor="middle" font-size="11" font-weight="bold">Docker</text>
  <text x="347" y="105" text-anchor="middle" font-size="11" font-weight="bold">Daemon</text>
  <text x="347" y="125" text-anchor="middle" font-size="10" fill="#555">builds image</text>
  <line x1="412" y1="100" x2="455" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_03_images)"/>
  <rect x="457" y="70" width="120" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="517" y="95" text-anchor="middle" font-size="11" font-weight="bold">Image</text>
  <text x="517" y="115" text-anchor="middle" font-size="10" fill="#555">layers</text>
</svg>

---

## Building Your First Image

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd3_03_images" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="130" height="40" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="85" y="55" text-anchor="middle" font-size="12" font-weight="bold">Developer</text>
  <line x1="85" y1="70" x2="85" y2="190" stroke="#333" stroke-width="2"/>
  <rect x="235" y="30" width="130" height="40" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="55" text-anchor="middle" font-size="12" font-weight="bold">Docker CLI</text>
  <line x1="300" y1="70" x2="300" y2="190" stroke="#333" stroke-width="2"/>
  <rect x="450" y="30" width="130" height="40" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="515" y="55" text-anchor="middle" font-size="12" font-weight="bold">Daemon</text>
  <line x1="515" y1="70" x2="515" y2="190" stroke="#333" stroke-width="2"/>
  <line x1="85" y1="100" x2="298" y2="100" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_03_images)"/>
  <text x="190" y="93" text-anchor="middle" font-size="10">docker build .</text>
  <line x1="300" y1="120" x2="513" y2="120" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd3_03_images)"/>
  <text x="406" y="113" text-anchor="middle" font-size="10">send context + Dockerfile</text>
  <line x1="515" y1="150" x2="302" y2="150" stroke="#333" stroke-width="1.5" stroke-dasharray="5,5" marker-end="url(#arrowd3_03_images)"/>
  <text x="406" y="143" text-anchor="middle" font-size="10">image ID + build output</text>
</svg>

---

## Layer Caching

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="11" fill="#555">Each instruction creates a cached layer</text>
  <rect x="150" y="30" width="300" height="30" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="50" text-anchor="middle" font-size="11">FROM ubuntu:22.04</text>
  <text x="520" y="50" font-size="10" fill="#4caf50">cached</text>
  <rect x="150" y="65" width="300" height="30" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="85" text-anchor="middle" font-size="11">RUN apt-get update</text>
  <text x="520" y="85" font-size="10" fill="#4caf50">cached</text>
  <rect x="150" y="100" width="300" height="30" fill="#fff3e0" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="120" text-anchor="middle" font-size="11">COPY requirements.txt .</text>
  <text x="520" y="120" font-size="10" fill="#ff9800">changed</text>
  <rect x="150" y="135" width="300" height="30" fill="#ffebee" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="155" text-anchor="middle" font-size="11">RUN pip install -r requirements.txt</text>
  <text x="520" y="155" font-size="10" fill="#f44336">rebuild</text>
  <rect x="150" y="170" width="300" height="30" fill="#ffebee" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="190" text-anchor="middle" font-size="11">COPY . .</text>
  <text x="520" y="190" font-size="10" fill="#f44336">rebuild</text>
</svg>

---

## Best Practices for Dockerfile

| Category | Practice | Reason |
|----------|----------|---------|
| Base Image | Use official, specific version | Security, stability |
| Layer Order | Most stable first | Better caching |
| Commands | Combine RUN commands | Reduce layers |
| Dependencies | Clear cache after install | Reduce image size |
| Security | Don't store secrets | Security best practice |

---

## Common Dockerfile Instructions

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="15" width="130" height="75" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="75" y="38" text-anchor="middle" font-size="11" font-weight="bold">Build Stage</text>
  <text x="75" y="55" text-anchor="middle" font-size="10">FROM, RUN</text>
  <text x="75" y="70" text-anchor="middle" font-size="10">COPY, WORKDIR</text>
  <rect x="155" y="15" width="130" height="75" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="220" y="38" text-anchor="middle" font-size="11" font-weight="bold">Config Stage</text>
  <text x="220" y="55" text-anchor="middle" font-size="10">ENV, ARG</text>
  <text x="220" y="70" text-anchor="middle" font-size="10">LABEL, EXPOSE</text>
  <rect x="310" y="15" width="130" height="75" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="375" y="38" text-anchor="middle" font-size="11" font-weight="bold">Runtime</text>
  <text x="375" y="55" text-anchor="middle" font-size="10">CMD, ENTRYPOINT</text>
  <text x="375" y="70" text-anchor="middle" font-size="10">USER, HEALTHCHECK</text>
  <rect x="460" y="15" width="130" height="75" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="525" y="38" text-anchor="middle" font-size="11" font-weight="bold">Metadata</text>
  <text x="525" y="55" text-anchor="middle" font-size="10">LABEL, STOPSIGNAL</text>
  <text x="525" y="70" text-anchor="middle" font-size="10">VOLUME, SHELL</text>
  <rect x="10" y="110" width="580" height="40" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="128" text-anchor="middle" font-size="10" fill="#555">Instructions execute top-to-bottom; each RUN/COPY/ADD creates a new image layer</text>
  <text x="300" y="143" text-anchor="middle" font-size="10" fill="#555">Order matters for caching efficiency</text>
</svg>

---

## Multi-stage Builds

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd6_03_images" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="160" height="160" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="100" y="45" text-anchor="middle" font-size="11" font-weight="bold">Stage 1: Build</text>
  <rect x="35" y="55" width="130" height="20" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="100" y="69" text-anchor="middle" font-size="10">FROM golang AS build</text>
  <rect x="35" y="80" width="130" height="20" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="100" y="94" text-anchor="middle" font-size="10">COPY source code</text>
  <rect x="35" y="105" width="130" height="20" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="100" y="119" text-anchor="middle" font-size="10">RUN go build</text>
  <rect x="35" y="135" width="130" height="30" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="100" y="154" text-anchor="middle" font-size="10">binary artifact</text>
  <line x1="180" y1="100" x2="218" y2="100" stroke="#333" stroke-width="2" marker-end="url(#arrowd6_03_images)"/>
  <text x="200" y="90" text-anchor="middle" font-size="10" fill="#666">COPY</text>
  <text x="200" y="115" text-anchor="middle" font-size="10" fill="#666">--from</text>
  <rect x="220" y="50" width="160" height="100" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="75" text-anchor="middle" font-size="11" font-weight="bold">Stage 2: Runtime</text>
  <rect x="235" y="85" width="130" height="20" fill="#fff" stroke="#999" stroke-width="1" rx="3"/>
  <text x="300" y="99" text-anchor="middle" font-size="10">FROM alpine</text>
  <rect x="235" y="110" width="130" height="25" fill="#fff3e0" stroke="#333" stroke-width="1" rx="3"/>
  <text x="300" y="127" text-anchor="middle" font-size="10">binary only</text>
  <rect x="430" y="50" width="150" height="100" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="505" y="80" text-anchor="middle" font-size="11" fill="#333" font-weight="bold">Result</text>
  <text x="505" y="100" text-anchor="middle" font-size="10" fill="#4caf50">Small final image</text>
  <text x="505" y="115" text-anchor="middle" font-size="10" fill="#4caf50">No build tools</text>
  <text x="505" y="130" text-anchor="middle" font-size="10" fill="#4caf50">No source code</text>
</svg>

---

## Image Tagging Strategy

| Tag Type | Purpose | Example |
|----------|---------|---------|
| Latest | Most recent version | `myapp:latest` |
| Version | Specific release | `myapp:1.0.0` |
| Stage | Development phase | `myapp:staging` |
| Hash | Git commit | `myapp:git-abc123` |

---

## Running Your Image

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd7_03_images" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="30" y="30" width="120" height="50" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="50" text-anchor="middle" font-size="11" font-weight="bold">Image</text>
  <text x="90" y="68" text-anchor="middle" font-size="10">myapp:1.0</text>
  <line x1="150" y1="55" x2="218" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd7_03_images)"/>
  <text x="184" y="48" text-anchor="middle" font-size="10" fill="#666">docker run</text>
  <rect x="220" y="20" width="160" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="45" text-anchor="middle" font-size="11" font-weight="bold">Container</text>
  <text x="300" y="62" text-anchor="middle" font-size="10">Running instance</text>
  <text x="300" y="78" text-anchor="middle" font-size="10" fill="#555">-p 5000:5000 -d</text>
  <rect x="220" y="120" width="160" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="142" text-anchor="middle" font-size="11" font-weight="bold">Host: localhost</text>
  <text x="300" y="162" text-anchor="middle" font-size="10">port 5000 mapped</text>
  <line x1="300" y1="90" x2="300" y2="118" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd7_03_images)"/>
  <text x="340" y="108" font-size="10" fill="#666">port map</text>
  <rect x="440" y="120" width="140" height="60" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="510" y="142" text-anchor="middle" font-size="11" font-weight="bold">External</text>
  <text x="510" y="162" text-anchor="middle" font-size="10">curl localhost:5000</text>
  <line x1="380" y1="150" x2="438" y2="150" stroke="#333" stroke-width="1.5" marker-end="url(#arrowd7_03_images)"/>
</svg>

---

## Troubleshooting Builds

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd8_03_images" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="25" width="140" height="65" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="50" text-anchor="middle" font-size="11" font-weight="bold">Build Error</text>
  <text x="90" y="70" text-anchor="middle" font-size="10">Step 4/7 fails</text>
  <line x1="160" y1="57" x2="218" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_03_images)"/>
  <rect x="220" y="20" width="160" height="75" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="11" font-weight="bold">Debug Strategy</text>
  <text x="300" y="60" text-anchor="middle" font-size="10">docker build --no-cache</text>
  <text x="300" y="75" text-anchor="middle" font-size="10">docker run -it image sh</text>
  <text x="300" y="90" text-anchor="middle" font-size="10" fill="#555">inspect failed layer</text>
  <line x1="380" y1="57" x2="428" y2="57" stroke="#333" stroke-width="2" marker-end="url(#arrowd8_03_images)"/>
  <rect x="430" y="25" width="150" height="65" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="50" text-anchor="middle" font-size="11" font-weight="bold">Fix and Rebuild</text>
  <text x="505" y="70" text-anchor="middle" font-size="10">Correct Dockerfile</text>
  <rect x="20" y="120" width="560" height="60" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="142" text-anchor="middle" font-size="10" fill="#555">Common issues: missing files, wrong base image, permission errors,</text>
  <text x="300" y="158" text-anchor="middle" font-size="10" fill="#555">network timeouts during package install, syntax errors in RUN commands</text>
</svg>
