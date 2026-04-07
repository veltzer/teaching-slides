# Creating Your Own Docker Images

---

## What is a Dockerfile

![what_is_a_dockerfile](svg/courses/devops/docker-for-developers/04_images/what_is_a_dockerfile.svg)

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

![image_building_process](svg/courses/devops/docker-for-developers/04_images/image_building_process.svg)

---

## Build Context

![build_context](svg/courses/devops/docker-for-developers/04_images/build_context.svg)

---

## Building Your First Image

![building_your_first_image](svg/courses/devops/docker-for-developers/04_images/building_your_first_image.svg)

---

## Layer Caching

![layer_caching](svg/courses/devops/docker-for-developers/04_images/layer_caching.svg)

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

![common_dockerfile_instructions](svg/courses/devops/docker-for-developers/04_images/common_dockerfile_instructions.svg)

---

## Multi-stage Builds

![multi_stage_builds](svg/courses/devops/docker-for-developers/04_images/multi_stage_builds.svg)

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

![running_your_image](svg/courses/devops/docker-for-developers/04_images/running_your_image.svg)

---

## Troubleshooting Builds

![troubleshooting_builds](svg/courses/devops/docker-for-developers/04_images/troubleshooting_builds.svg)
