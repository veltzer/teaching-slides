---
tags:
  - infrastructure:linux
  - practices:command-line
level: intermediate
category: operating-systems
audience:
  - audiences:developers
  - audiences:sysadmins
  - audiences:devops

---
# Introduction to Linux Package Management

---
## Package Manager Layers

![package_layers](svg/courses/operating_systems/linux-package-managers/01_introduction/package_layers.svg)

---
## Version Pinning

![version_pinning](svg/courses/operating_systems/linux-package-managers/01_introduction/version_pinning.svg)

---
## Where Does Software Come From?

A modern Linux machine pulls software from many places:

- The distribution's repositories (`apt`, `dnf`, `pacman`, ...)
- Cross-distribution sandboxed formats (`flatpak`, `snap`, `appimage`)
- Declarative systems (`nix`, `guix`)
- Language ecosystems (`pip`, `cargo`, `npm`, `gem`, `go`, ...)
- `GitHub` releases
- Container images
- Source tarballs and `git` clones

Each of these has its own command, its own concept of "version", its own update story, and its own security model.

---
## What a Package Manager Does

A package manager is a system that installs, upgrades, removes and tracks software in a controlled way.

- Knows what is installed and what files belong to which package
- Resolves dependencies automatically
- Verifies signatures and checksums
- Provides clean upgrade and rollback
- Provides clean removal
- Gives you an audit trail

Without a package manager you are doing all of this by hand.

---
## What Life Looks Like Without a Package Manager

- "I have no idea what is installed on this machine."
- "Which version of `openssl` is running?"
- "I upgraded one library and three programs broke."
- "How do I uninstall this thing I built last year?"
- "Is this binary in `/usr/local/bin` even from a trusted source?"
- "Why do I have eleven copies of `python` on this server?"

This is exactly the world that package managers were built to fix.

---
## The Five Hard Problems

Every package manager has to solve, or at least make tradeoffs about, the same five problems:

1. 1. 1. **Dependency resolution** — package A needs library B at version >= 2.0
1. 1. 1. **Versioning** — multiple versions of the same thing may need to coexist
1. 1. 1. **Reproducibility** — can I rebuild the same system tomorrow?
1. 1. 1. **Security** — is this package authentic and unmodified?
1. 1. 1. **Lifecycle** — install, upgrade, downgrade, remove, audit

How a tool answers these is what makes it different from the others.

---
## High-Level vs Low-Level Tools

Most package managers come in pairs.

- **Low-level** tools work on a single package file
    - `dpkg` for `.deb` files
    - `rpm` for `.rpm` files
    - They install, query, remove. They do *not* fetch, do *not* resolve dependencies.
- **High-level** tools work with repositories
    - `apt` on top of `dpkg`
    - `dnf` on top of `rpm`
    - They fetch, resolve, and orchestrate the low-level tool

You almost always want the high-level tool. The low-level tool is for surgery.

---
## The Linux Package Management Landscape

| Family | Low-level | High-level | Format |
|---|---|---|---|
| `Debian`/`Ubuntu` | `dpkg` | `apt` | `.deb` |
| `RHEL`/`Fedora` | `rpm` | `dnf` (was `yum`) | `.rpm` |
| `Arch` | — | `pacman` | `.pkg.tar.zst` |
| `openSUSE` | `rpm` | `zypper` | `.rpm` |
| `Alpine` | — | `apk` | `.apk` |
| `Gentoo` | — | `portage`/`emerge` | source |
| Cross-distro | — | `flatpak`, `snap`, `appimage` | various |
| Declarative | — | `nix`, `guix` | various |

---
## Distribution Repos vs Third-Party vs Upstream

A piece of software can reach you via several paths:

- **Distribution repository** — packaged by the distro maintainers, well integrated, often a bit older
- **Third-party repository** — `PPA`, `Copr`, vendor-hosted (`Docker`, `Google`, ...). Faster updates, more risk
- **Upstream binary** — `GitHub` release, `.tar.gz` from a website. Latest, but you own the lifecycle
- **Language registry** — `pip`, `cargo`, `npm`. Right version for your project, isolated from system
- **Sandboxed store** — `flatpak`, `snap`. Newest GUI apps, sandboxed from the rest of the system
- **Source build** — last resort

The further from the distro, the fresher the software and the more responsibility on you.

---
## What "Installed" Even Means

The same program can be installed in very different ways:

```bash
# As a system package
apt install ripgrep         # /usr/bin/rg, owned by dpkg

# Via a language manager
cargo install ripgrep       # ~/.cargo/bin/rg, owned by cargo

# As a sandboxed app
snap install ripgrep        # /snap/bin/rg, owned by snap

# From an upstream binary
curl -L .../rg.tar.gz | tar xz   # ~/bin/rg, owned by you
```

Four different `rg` binaries. Four different update stories. Four different things in your `$PATH`.

---
## A First Rule of Hygiene

Pick the *most distribution-native* option that works.

- If the distro packages it at a version that works for you, use that.
- If you need a newer version, prefer a *signed* third-party repo.
- For developer tooling tied to a specific project, use the language's package manager inside a project-local directory (`venv`, `cargo`, `node_modules`).
- For GUI apps that the distro doesn't have, `flatpak` or `snap`.
- Only fall back to "download from `GitHub`" or "build from source" when the above don't fit.

This is the order most experienced sysadmins reach for, and the rest of this course will explain why.

---
## What This Course Covers

1. 1. 1. The `Debian` family: `dpkg` and `apt`
1. 1. 1. The `Red Hat` family: `rpm` and `dnf`
1. 1. 1. Universal/sandboxed formats: `flatpak`, `snap`, `appimage`, `nix`
1. 1. 1. Language package managers: `pip`, `cargo`, `npm`, `gem`, `go`, ...
1. 1. 1. `GitHub` releases and source builds
1. 1. 1. How to choose between them, and how to mix them safely

By the end you should be able to install almost anything on almost any Linux box, and pick the right tool the first time.
