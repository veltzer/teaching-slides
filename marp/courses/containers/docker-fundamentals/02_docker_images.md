---
tags:
  - infrastructure:docker
  - infrastructure:images
level: beginner
category: containers
audience:
  - audiences:developers
  - audiences:devops

---
# Docker Images

---
## What This Chapter Covers

- What an image is, mechanically
- Image layers and the union filesystem
- Pulling, listing, inspecting, removing
- Tags and versioning
- Public and private registries

---
## What an Image Is

- A read-only snapshot of a filesystem plus metadata
- Includes everything needed to start a container: code, runtime, libs, config
- Identified by a *digest* (a SHA256 hash) and addressable by *tags*
- Stored locally after `docker pull`
- Multiple containers can run from the same image

---
## Image Layers

- An image is *not* one big blob
- Each instruction in a Dockerfile creates a new layer
- Layers are stacked; the final filesystem is the union
- Layers are *content-addressable*: the same layer is shared across images
- Pulling a new image often only downloads the layers you don't have

---
## Layers Visualised

![image_layers](svg/courses/containers/docker-fundamentals/02_docker_images/image_layers.svg)

---
## The Union Filesystem

- Multiple layers presented as one merged filesystem
- A file in an upper layer hides the same path in a lower layer
- Common drivers: overlay2 (Linux), btrfs, zfs
- Container writes go to a *thin writable layer* on top
- That writable layer disappears when the container is removed

---
## Pulling an Image

```bash
docker pull nginx
docker pull nginx:1.27-alpine
docker pull ubuntu@sha256:abcdef...
```

- By tag (mutable) or by digest (immutable)
- Default registry: Docker Hub
- Other registries: prefix the image name (`gcr.io/google-containers/...`)

---
## Listing Local Images

```bash
docker images
docker image ls
docker images --format '{{.Repository}}:{{.Tag}}\t{{.Size}}'
```

- Shows repository, tag, image ID, size
- `--no-trunc` for full image IDs
- `--filter` to narrow down (`-f reference=nginx*`)

---
## Inspecting an Image

```bash
docker image inspect nginx:latest
docker history nginx:latest
```

- `inspect`: full JSON of metadata, environment, exposed ports, entrypoint
- `history`: shows the layer-by-layer build steps and their sizes
- Useful for debugging "why is this image 3 GB?"

---
## Removing Images

```bash
docker rmi nginx:1.27-alpine
docker image prune          # remove dangling images
docker image prune -a       # remove ALL unused images (careful)
docker system prune -a      # remove unused images, containers, networks
```

- `dangling`: layers that aren't referenced by a tagged image
- Disk usage adds up fast — periodic pruning is normal
- A locked image (used by a container) won't be removed

---
## Image Tags

- A tag is a *human-readable label* for a digest
- `nginx:1.27-alpine`, `python:3.12-slim`, `myapp:v1.2.3`
- Tags are *mutable*: today's `:latest` is not tomorrow's `:latest`
- For reproducibility: pin to specific versions, or use digests
- Convention: `image:major.minor[-variant]`

---
## Tagging Strategies

- **Latest moving tag**: `:latest`, `:stable` — convenient but unreliable
- **Specific version**: `:1.2.3` — preferred in production
- **Major.minor**: `:1.27` — auto-updates patch level
- **Digest pinning**: `nginx@sha256:abc...` — fully immutable
- Most teams use specific versions for prod, `:latest` for local dev

---
## Tagging Your Own Images

```bash
docker tag myapp:latest myapp:v1.2.3
docker tag myapp:latest registry.example.com/myapp:v1.2.3
docker push registry.example.com/myapp:v1.2.3
```

- Multiple tags can point to the same image
- Tag for a registry by prefixing the URL
- `push` requires authentication for private registries

---
## Docker Hub

- The default public registry: hub.docker.com
- Free for public images; paid tiers for private
- Official images: maintained by the project (nginx, postgres, redis)
- Verified Publisher: maintained by recognised vendors
- Anyone else: community images — vet before using

---
## Other Registries

- **AWS ECR**: tied to AWS accounts and IAM
- **Google Artifact Registry / GCR**: integrated with GCP
- **Azure Container Registry (ACR)**: integrated with Azure
- **GitHub Container Registry (GHCR)**: free for public repos
- **Self-hosted**: Harbor, Nexus, JFrog Artifactory, plain `registry`

---
## Working With Private Registries

```bash
docker login registry.example.com
docker pull registry.example.com/team/myapp:v1.0
docker push registry.example.com/team/myapp:v1.1
```

- `docker login` stores credentials in `~/.docker/config.json`
- For CI: use a service account / token, not a personal password
- Most registries support OAuth/OIDC tokens

---
## Image Size

- Smaller images = faster pulls, smaller attack surface
- Choose minimal base images: `alpine`, `distroless`, `scratch`
- Use multi-stage builds (covered later) to drop build-time tools
- Audit with `docker history` and `dive`
- A 1.5 GB image is rarely necessary; aim for under 200 MB

---
## Common Mistakes

- Trusting `:latest` in production
- Building on top of huge `ubuntu` base when `alpine` would do
- Building one image per environment (dev/staging/prod) instead of one image + config
- Pulling without authentication, then puzzled by rate limits
- Pushing secrets baked into image layers (they stay forever, even if "deleted")
