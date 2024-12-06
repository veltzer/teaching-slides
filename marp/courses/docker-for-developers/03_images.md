# Creating Your Own Docker Images

---

## What is a Dockerfile?

![0](../../../out/mermaid/marp/courses/docker-for-developers/03_images.md/0.png)

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

![1](../../../out/mermaid/marp/courses/docker-for-developers/03_images.md/1.png)

---

## Build Context

![2](../../../out/mermaid/marp/courses/docker-for-developers/03_images.md/2.png)

---

## Building Your First Image

![3](../../../out/mermaid/marp/courses/docker-for-developers/03_images.md/3.png)

---

## Layer Caching

![4](../../../out/mermaid/marp/courses/docker-for-developers/03_images.md/4.png)

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

![5](../../../out/mermaid/marp/courses/docker-for-developers/03_images.md/5.png)

---

## Multi-stage Builds

![6](../../../out/mermaid/marp/courses/docker-for-developers/03_images.md/6.png)

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

![7](../../../out/mermaid/marp/courses/docker-for-developers/03_images.md/7.png)

---

## Troubleshooting Builds

![8](../../../out/mermaid/marp/courses/docker-for-developers/03_images.md/8.png)
