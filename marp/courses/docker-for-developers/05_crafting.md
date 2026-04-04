# Crafting Your Image

---

## Dockerfile Language Overview

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="70" ry="35" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="98" text-anchor="middle" font-size="12" fill="white" font-weight="bold">Dockerfile</text>
  <text x="300" y="113" text-anchor="middle" font-size="10" fill="white">Language</text>
  <ellipse cx="100" cy="45" rx="70" ry="28" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="100" y="42" text-anchor="middle" font-size="11">Build</text>
  <text x="100" y="57" text-anchor="middle" font-size="10">FROM, RUN, COPY</text>
  <ellipse cx="500" cy="45" rx="70" ry="28" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="500" y="42" text-anchor="middle" font-size="11">Configure</text>
  <text x="500" y="57" text-anchor="middle" font-size="10">ENV, ARG, EXPOSE</text>
  <ellipse cx="100" cy="165" rx="70" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="162" text-anchor="middle" font-size="11">Execute</text>
  <text x="100" y="177" text-anchor="middle" font-size="10">CMD, ENTRYPOINT</text>
  <ellipse cx="500" cy="165" rx="70" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="162" text-anchor="middle" font-size="11">Metadata</text>
  <text x="500" y="177" text-anchor="middle" font-size="10">LABEL, USER</text>
  <line x1="240" y1="78" x2="160" y2="62" stroke="#333" stroke-width="1.5"/>
  <line x1="360" y1="78" x2="440" y2="62" stroke="#333" stroke-width="1.5"/>
  <line x1="240" y1="122" x2="160" y2="148" stroke="#333" stroke-width="1.5"/>
  <line x1="360" y1="122" x2="440" y2="148" stroke="#333" stroke-width="1.5"/>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd1_04_crafting" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="30" width="140" height="60" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="90" y="55" text-anchor="middle" font-size="11" font-weight="bold">ENV</text>
  <text x="90" y="73" text-anchor="middle" font-size="10">Runtime variable</text>
  <line x1="160" y1="60" x2="218" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_04_crafting)"/>
  <rect x="220" y="30" width="160" height="60" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="55" text-anchor="middle" font-size="11" font-weight="bold">ARG</text>
  <text x="300" y="73" text-anchor="middle" font-size="10">Build-time only variable</text>
  <line x1="380" y1="60" x2="428" y2="60" stroke="#333" stroke-width="2" marker-end="url(#arrowd1_04_crafting)"/>
  <rect x="430" y="30" width="150" height="60" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="505" y="55" text-anchor="middle" font-size="11" font-weight="bold">Image</text>
  <text x="505" y="73" text-anchor="middle" font-size="10">ENV persists, ARG gone</text>
  <rect x="20" y="120" width="560" height="55" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="140" text-anchor="middle" font-size="10" fill="#555">ENV: baked into image, available at runtime (ENV APP_PORT=8080)</text>
  <text x="300" y="158" text-anchor="middle" font-size="10" fill="#555">ARG: only during build, set via --build-arg (ARG VERSION=1.0)</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd2_04_crafting" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="170" height="70" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="45" text-anchor="middle" font-size="11" font-weight="bold">ENTRYPOINT</text>
  <text x="105" y="62" text-anchor="middle" font-size="10">Fixed executable</text>
  <text x="105" y="77" text-anchor="middle" font-size="10" fill="#555">["nginx", "-g"]</text>
  <rect x="215" y="20" width="170" height="70" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="45" text-anchor="middle" font-size="11" font-weight="bold">CMD</text>
  <text x="300" y="62" text-anchor="middle" font-size="10">Default arguments</text>
  <text x="300" y="77" text-anchor="middle" font-size="10" fill="#555">["daemon off;"]</text>
  <line x1="190" y1="55" x2="213" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd2_04_crafting)"/>
  <text x="300" y="112" text-anchor="middle" font-size="10" fill="#666">Combined at runtime:</text>
  <rect x="215" y="120" width="170" height="30" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="140" text-anchor="middle" font-size="10">nginx -g "daemon off;"</text>
  <rect x="420" y="20" width="160" height="70" fill="#fff3e0" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="45" text-anchor="middle" font-size="11" font-weight="bold">RUN</text>
  <text x="500" y="62" text-anchor="middle" font-size="10">Build-time only</text>
  <text x="500" y="77" text-anchor="middle" font-size="10" fill="#555">Creates layers</text>
  <rect x="20" y="120" width="170" height="65" fill="#ffebee" stroke="#333" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="105" y="142" text-anchor="middle" font-size="10" fill="#555">CMD is overridden by</text>
  <text x="105" y="157" text-anchor="middle" font-size="10" fill="#555">docker run args;</text>
  <text x="105" y="172" text-anchor="middle" font-size="10" fill="#555">ENTRYPOINT is not</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="18" text-anchor="middle" font-size="11" fill="#555">Layer caching: change invalidates all subsequent layers</text>
  <rect x="30" y="30" width="540" height="30" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="50" text-anchor="middle" font-size="11">1. FROM (base image) - rarely changes</text>
  <text x="550" y="50" font-size="10" fill="#4caf50">cached</text>
  <rect x="30" y="65" width="540" height="30" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="85" text-anchor="middle" font-size="11">2. RUN apt-get install (system deps) - infrequent</text>
  <text x="550" y="85" font-size="10" fill="#4caf50">cached</text>
  <rect x="30" y="100" width="540" height="30" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="120" text-anchor="middle" font-size="11">3. COPY package.json (app deps) - sometimes</text>
  <text x="550" y="120" font-size="10" fill="#2196f3">maybe</text>
  <rect x="30" y="135" width="540" height="30" fill="#fff3e0" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="155" text-anchor="middle" font-size="11">4. RUN npm install (install deps) - if #3 changed</text>
  <rect x="30" y="170" width="540" height="30" fill="#ffebee" stroke="#333" stroke-width="2" rx="3"/>
  <text x="300" y="190" text-anchor="middle" font-size="11">5. COPY . . (source code) - changes often</text>
  <text x="550" y="190" font-size="10" fill="#f44336">rebuild</text>
</svg>

---

## Build Arguments and Variables

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd4_04_crafting" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="15" width="170" height="80" fill="#e3f2fd" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="38" text-anchor="middle" font-size="11" font-weight="bold">ARG (Build-time)</text>
  <text x="105" y="55" text-anchor="middle" font-size="10">--build-arg VER=1.0</text>
  <text x="105" y="72" text-anchor="middle" font-size="10" fill="#555">Available in Dockerfile</text>
  <text x="105" y="87" text-anchor="middle" font-size="10" fill="#555">Not in final image</text>
  <rect x="215" y="15" width="170" height="80" fill="#f3e5f5" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="38" text-anchor="middle" font-size="11" font-weight="bold">ENV (Runtime)</text>
  <text x="300" y="55" text-anchor="middle" font-size="10">ENV APP_ENV=prod</text>
  <text x="300" y="72" text-anchor="middle" font-size="10" fill="#555">Persists in image</text>
  <text x="300" y="87" text-anchor="middle" font-size="10" fill="#555">Overridable: -e flag</text>
  <line x1="190" y1="55" x2="213" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd4_04_crafting)"/>
  <text x="202" y="48" text-anchor="middle" font-size="9" fill="#666">set</text>
  <rect x="410" y="15" width="170" height="80" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="495" y="38" text-anchor="middle" font-size="11" font-weight="bold">ARG + ENV</text>
  <text x="495" y="55" text-anchor="middle" font-size="10">ARG VERSION</text>
  <text x="495" y="72" text-anchor="middle" font-size="10">ENV VER=$VERSION</text>
  <text x="495" y="87" text-anchor="middle" font-size="10" fill="#555">Promotes to runtime</text>
  <rect x="20" y="115" width="560" height="65" fill="#f9f9f9" stroke="#999" stroke-width="1" rx="5" stroke-dasharray="4,3"/>
  <text x="300" y="138" text-anchor="middle" font-size="10" fill="#555">Build: docker build --build-arg VERSION=2.0 .</text>
  <text x="300" y="155" text-anchor="middle" font-size="10" fill="#555">Run:   docker run -e APP_ENV=staging myapp</text>
  <text x="300" y="172" text-anchor="middle" font-size="10" fill="#c62828">Warning: ARG values visible in image history - never use for secrets</text>
</svg>

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

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowd5_04_crafting" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L0,6 L9,3 z" fill="#333"/>
    </marker>
  </defs>
  <rect x="20" y="20" width="170" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="105" y="42" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Do</text>
  <text x="105" y="58" text-anchor="middle" font-size="10">Use specific base tags</text>
  <text x="105" y="73" text-anchor="middle" font-size="10">Combine RUN commands</text>
  <line x1="190" y1="55" x2="218" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_04_crafting)"/>
  <rect x="220" y="20" width="160" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="300" y="42" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Do</text>
  <text x="300" y="58" text-anchor="middle" font-size="10">Clean cache in same RUN</text>
  <text x="300" y="73" text-anchor="middle" font-size="10">Use .dockerignore</text>
  <line x1="380" y1="55" x2="418" y2="55" stroke="#333" stroke-width="2" marker-end="url(#arrowd5_04_crafting)"/>
  <rect x="420" y="20" width="160" height="70" fill="#e8f5e9" stroke="#333" stroke-width="2" rx="5"/>
  <text x="500" y="42" text-anchor="middle" font-size="11" font-weight="bold" fill="#2e7d32">Do</text>
  <text x="500" y="58" text-anchor="middle" font-size="10">Non-root USER</text>
  <text x="500" y="73" text-anchor="middle" font-size="10">Multi-stage builds</text>
  <rect x="20" y="110" width="270" height="70" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="155" y="132" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">Avoid</text>
  <text x="155" y="148" text-anchor="middle" font-size="10">Secrets in ENV/ARG</text>
  <text x="155" y="163" text-anchor="middle" font-size="10">Running as root in production</text>
  <rect x="310" y="110" width="270" height="70" fill="#ffebee" stroke="#333" stroke-width="2" rx="5"/>
  <text x="445" y="132" text-anchor="middle" font-size="11" font-weight="bold" fill="#c62828">Avoid</text>
  <text x="445" y="148" text-anchor="middle" font-size="10">Using :latest tag in production</text>
  <text x="445" y="163" text-anchor="middle" font-size="10">Unnecessary packages in image</text>
</svg>

---

## Shell vs Exec Form

| Form | Example | Use Case |
|------|---------|----------|
| Shell | `RUN apt-get update` | Shell processing needed |
| Exec | `CMD ["python", "app.py"]` | Direct execution |
| Mixed | `ENTRYPOINT ["npm", "start"]` | Standardized execution |

---

## Labels and Metadata

<svg width="600" height="200" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="300" cy="100" rx="65" ry="30" fill="#673ab7" stroke="#333" stroke-width="2"/>
  <text x="300" y="98" text-anchor="middle" font-size="12" fill="white" font-weight="bold">LABEL</text>
  <text x="300" y="113" text-anchor="middle" font-size="10" fill="white">Metadata</text>
  <ellipse cx="100" cy="45" rx="75" ry="28" fill="#e3f2fd" stroke="#333" stroke-width="2"/>
  <text x="100" y="42" text-anchor="middle" font-size="10">maintainer</text>
  <text x="100" y="57" text-anchor="middle" font-size="10" fill="#555">"team@co.com"</text>
  <ellipse cx="500" cy="45" rx="75" ry="28" fill="#f3e5f5" stroke="#333" stroke-width="2"/>
  <text x="500" y="42" text-anchor="middle" font-size="10">version</text>
  <text x="500" y="57" text-anchor="middle" font-size="10" fill="#555">"1.0.0"</text>
  <ellipse cx="100" cy="165" rx="75" ry="28" fill="#e8f5e9" stroke="#333" stroke-width="2"/>
  <text x="100" y="162" text-anchor="middle" font-size="10">description</text>
  <text x="100" y="177" text-anchor="middle" font-size="10" fill="#555">"My web app"</text>
  <ellipse cx="500" cy="165" rx="75" ry="28" fill="#fff3e0" stroke="#333" stroke-width="2"/>
  <text x="500" y="162" text-anchor="middle" font-size="10">org.opencontainers</text>
  <text x="500" y="177" text-anchor="middle" font-size="10" fill="#555">OCI standard labels</text>
  <line x1="245" y1="78" x2="165" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="78" x2="435" y2="60" stroke="#333" stroke-width="1.5"/>
  <line x1="245" y1="122" x2="165" y2="148" stroke="#333" stroke-width="1.5"/>
  <line x1="355" y1="122" x2="435" y2="148" stroke="#333" stroke-width="1.5"/>
</svg>

---

## Instruction Formatting

| Style | Example | Use Case |
|-------|---------|----------|
| Single line | `RUN command` | Simple operations |
| Multi-line | `RUN command1 && \` | Complex operations |
| Array | `CMD ["executable"]` | Precise execution |
| Heredoc | `RUN <<EOF` | Complex scripts |
