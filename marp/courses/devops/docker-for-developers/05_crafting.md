---
tags:
  - tools:docker
  - infrastructure:containers
  - practices:devops
  - networking:networking
level: intermediate
category: devops
audience:
  - audiences:developers

---

# Crafting Your Image

---

## Dockerfile Language Overview

![dockerfile_language_overview](svg/courses/devops/docker-for-developers/05_crafting/dockerfile_language_overview.svg)

---

## Core Dockerfile Keywords

| Keyword | Purpose | Example | Layer Created |
|---------|---------|---------|---------------|
| FROM | Set base image | `FROM ubuntu:22.04` | Yes |
| RUN | Execute commands | `RUN apt-get update` | Yes |
| COPY | Copy files | `COPY . /app` | Yes |
| ADD | Copy with extraction | `ADD archive.tar /` | Yes |
| CMD | Default command | `CMD ["node", "app.js"]` | No |
| ENTRYPOINT | Container executable | `ENTRYPOINT ["nginx"]` | No |

---

## Environment and Build Configuration

![environment_and_build_configuration](svg/courses/devops/docker-for-developers/05_crafting/environment_and_build_configuration.svg)

---

## File Operation Instructions

| Instruction | Usage | Example | Notes |
|-------------|-------|---------|--------|
| COPY | Basic file copy | `COPY src dest` | Preferred method |
| ADD | Advanced copy | `ADD src dest` | Tar auto-extraction |
| WORKDIR | Set working directory | `WORKDIR /app` | Affects subsequent commands |
| VOLUME | Create mount point | `VOLUME /data` | Persistent storage |

---

## Execution Control

![execution_control](svg/courses/devops/docker-for-developers/05_crafting/execution_control.svg)

---

## Network and Runtime Instructions

| Instruction | Purpose | Example |
|-------------|---------|---------|
| EXPOSE | Document ports | `EXPOSE 80` |
| HEALTHCHECK | Health monitoring | `HEALTHCHECK CMD curl -f http://localhost/` |
| STOPSIGNAL | Custom stop signal | `STOPSIGNAL SIGTERM` |
| USER | Set user context | `USER nginx` |

---

## Instruction Order and Caching

![instruction_order_and_caching](svg/courses/devops/docker-for-developers/05_crafting/instruction_order_and_caching.svg)

---

## Build Arguments and Variables

![build_arguments_and_variables](svg/courses/devops/docker-for-developers/05_crafting/build_arguments_and_variables.svg)

---

## Advanced COPY and ADD

| Feature | COPY | ADD |
|---------|------|-----|
| Local files | Yes | Yes |
| Remote URLs | No | Yes |
| Auto-extract | No | Yes |
| Recommended | Yes | Special cases |
| Cache busting | Better | Worse |

---

## Multi-line Commands

```dockerfile
# Bad Practice
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get clean

# Good Practice
RUN apt-get update && \
    apt-get install -y python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

---

## Environment Best Practices

![environment_best_practices](svg/courses/devops/docker-for-developers/05_crafting/environment_best_practices.svg)

---

## Shell vs Exec Form

| Form | Example | Use Case |
|------|---------|----------|
| Shell | `RUN apt-get update` | Shell processing needed |
| Exec | `CMD ["python", "app.py"]` | Direct execution |
| Mixed | `ENTRYPOINT ["npm", "start"]` | Standardized execution |

---

## Labels and Metadata

![labels_and_metadata](svg/courses/devops/docker-for-developers/05_crafting/labels_and_metadata.svg)

---

## Instruction Formatting

| Style | Example | Use Case |
|-------|---------|----------|
| Single line | `RUN command` | Simple operations |
| Multi-line | `RUN command1 && \` | Complex operations |
| Array | `CMD ["executable"]` | Precise execution |
| Heredoc | `RUN <<EOF` | Complex scripts |
