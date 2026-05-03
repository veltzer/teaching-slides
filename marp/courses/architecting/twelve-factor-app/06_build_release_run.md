---
tags:
  - concepts:architecture
  - practices:ci-cd
level: intermediate
category: architecture
audience:
  - audiences:developers
  - audiences:devops

---
# Factor V: Build, Release, Run

---
## Three Stages

![three_stages](svg/courses/architecting/twelve-factor-app/06_build_release_run/three_stages.svg)

---
## The Rule

- Strictly separate build, release, and run stages
- Each stage produces an artifact for the next
- A release is immutable; the run stage cannot modify it

---
## The Three Stages

- **Build**: convert source code into an executable bundle (binary, image, jar)
- **Release**: combine the build with config to produce a release
- **Run**: execute a release in the target environment

---
## Why Separate Them

- Builds happen in a controlled environment (CI), not on the production host
- Releases are immutable — you can roll back to any release
- Run is the only stage in production; bugs at run time can't bleed into the build
- Each stage has different dependencies and different security needs

---
## Stage Boundaries

- Output of build: an immutable artifact (e.g., a Docker image)
- Output of release: artifact + config snapshot + release id
- Output of run: a running process
- Each handoff is explicit; nothing skipped

---
## Immutable Releases

- A release is a versioned, auditable, frozen combination of code and config
- Once tagged, a release never changes — even if you redeploy it
- New deploys make new releases
- Easy rollback: deploy an older release tag

---
## Release Immutability Visualised

![release_immutability](svg/courses/architecting/twelve-factor-app/06_build_release_run/release_immutability.svg)

---
## Release Versioning

- Monotonically increasing release id (`v123`, `v124`)
- Or content-hash based (`abc123def456`)
- Either way, every release is distinguishable
- Audit trail: which release ran where, when

---
## CI/CD Pipeline Alignment

- CI handles the build stage: tests, compile, image build
- CD handles the release and run stages: tag, deploy, run
- Build artifacts move forward; run artifacts move forward; nothing moves back
- A failed run does not affect the release — it triggers a rollback to the previous release

---
## Anti-Patterns

- "SSH into prod and patch the code" — modifies the run, not the codebase
- "Hot reload config in production" — bypasses the release stage
- "Built on the production host" — mixes build and run
- "Same artifact, different config files baked in" — release stage is missing

---
## Rollback

- A working release plus the previous release id is enough to roll back
- Rollback is just a redeploy
- It should take seconds, not hours
- If rollback is hard, factor V is being violated somewhere

---
## Container Alignment

- A Docker image is a build artifact
- An image-tag plus its environment config is a release
- Running the image is the run stage
- The boundaries map cleanly onto containers

---
## Summary

- Three stages with strict boundaries: build, release, run
- Releases are immutable
- Easy rollback is the payoff
- Containers map naturally onto this factor
- Skipping a stage trades short-term speed for long-term debugging pain
