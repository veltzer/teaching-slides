---
tags:
  - infrastructure:linux
  - audiences:sysadmin
level: intermediate
category: operating-systems
audience:
  - audiences:sysadmins
  - audiences:developers

---
# Universal and Sandboxed Package Formats

---
## Why Universal Formats Exist

Distribution packages have real limitations:

- A version is fixed by the distro release. You get `Firefox 115` until you upgrade `Ubuntu`.
- Each distro has its own format. App authors have to package for `apt`, `dnf`, `pacman`, `apk`, ...
- System libraries shift over time. A `.deb` from 2020 may not install today.
- A native `.deb`/`.rpm` runs with the user's full privileges.

Universal formats answer:

- Ship one bundle that works on any distro.
- Bundle the dependencies. Don't depend on what the host happens to have.
- Run the app in a sandbox so it can't read your whole `$HOME`.

---
## The Three Big Universal Formats

| | `flatpak` | `snap` | `appimage` |
|---|---|---|---|
| Origin | community / `Red Hat` ties | `Canonical` | community |
| Server | `flathub` (and others) | `Snap Store` (single) | none — direct download |
| Sandboxed | yes (`bubblewrap`) | yes (`apparmor`) | no |
| Install required | yes | yes | no — just run the file |
| Auto-update | optional | yes, mandatory by default | manual |
| Cross-distro | yes | yes | yes |
| Server can be self-hosted | yes | no (single store) | n/a |

Not competing on quite the same axes — pick by your priorities.

---
## `flatpak`

```bash
# Install (most distros)
sudo apt install flatpak       # or dnf, etc.

# Add the main remote
flatpak remote-add --if-not-exists flathub \
  https://flathub.org/repo/flathub.flatpakrepo

# Search and install (system-wide)
flatpak search gimp
flatpak install flathub org.gimp.GIMP

# Or install for just the current user
flatpak install --user flathub org.gimp.GIMP

# Run
flatpak run org.gimp.GIMP

# Update / remove
flatpak update
flatpak uninstall org.gimp.GIMP
flatpak uninstall --unused
```

---
## `flatpak` Concepts: Runtimes and Sandboxing

A `flatpak` app does *not* depend on your distro's libraries. It depends on a **runtime**.

```bash
# What runtimes are installed?
flatpak list --runtime

# A runtime is itself a flatpak — for example:
# org.freedesktop.Platform/x86_64/23.08
# org.gnome.Platform/x86_64/45
```

When you install GIMP, `flatpak` will pull in the runtime it was built against. Many apps share one runtime, so disk usage is amortized.

The sandbox uses `bubblewrap`. By default the app cannot:

- read your home directory (only `~/.var/app/<id>/`)
- access random files
- talk to other apps' D-Bus services

You grant access explicitly with portals or with `flatpak override`.

---
## `flatpak` Permissions

```bash
# Show what an app is allowed to do
flatpak info --show-permissions org.gimp.GIMP

# Grant or deny access
flatpak override --user --filesystem=home org.gimp.GIMP
flatpak override --user --nofilesystem=home org.gimp.GIMP

# Reset
flatpak override --reset org.gimp.GIMP
```

```bash
# Inspect the sandbox interactively
flatpak run --command=sh org.gimp.GIMP
$ ls /home          # likely empty or restricted
$ ls /app           # the app's bundled tree
```

This is the security advantage: a malicious or compromised flatpak app sees a small, well-defined slice of your machine.

---
## `snap`

`snap` is `Canonical`'s answer. Default on `Ubuntu`, available on most distros.

```bash
# Search
snap find firefox

# Install
sudo snap install firefox

# A specific channel
sudo snap install --channel=latest/edge firefox

# List installed snaps
snap list

# Show info / current channel
snap info firefox

# Update one snap or all
sudo snap refresh firefox
sudo snap refresh

# Remove
sudo snap remove firefox
```

---
## `snap` Channels

A snap publisher offers up to four parallel streams of the same app.

| Channel | Meaning |
|---|---|
| `stable` | Production. The default. |
| `candidate` | About to become `stable`. |
| `beta` | Pre-release. |
| `edge` | Latest commit, may be broken. |

```bash
# Install a specific channel
sudo snap install code --classic --channel=latest/edge

# Switch channels for an installed snap
sudo snap refresh code --channel=stable

# Hold updates (one snap or all)
sudo snap refresh --hold=24h firefox
sudo snap refresh --hold
```

By default snaps update automatically in the background. This is convenient and infuriating.

---
## `snap` Confinement

```bash
# Three confinement modes:
# - strict     — full sandbox (the default)
# - classic    — full system access (used by IDEs, docker)
# - devmode    — sandbox warnings only, no enforcement (dev only)

# What confinement does this snap use?
snap info code | grep confinement

# What interfaces does it have plugged?
snap connections firefox
```

```bash
# Connect / disconnect an interface (give/revoke a permission)
sudo snap connect firefox:home
sudo snap disconnect firefox:home
```

A "classic" snap is essentially a tarball with auto-update. Don't be misled by the word *snap*: classic snaps have no sandbox.

---
## `appimage`

The simplest of the three: one file, no install, no daemon, no store.

```bash
# Download an .AppImage
wget https://example.com/krita-5.2.0.AppImage

# Make it executable and run
chmod +x krita-5.2.0.AppImage
./krita-5.2.0.AppImage
```

That's it. The file contains the app and its dependencies in a self-mounting `squashfs`.

```bash
# Inspect contents without running
./krita-5.2.0.AppImage --appimage-extract
ls squashfs-root/

# Mount only (read-only)
./krita-5.2.0.AppImage --appimage-mount
```

There is no auto-update, no central registry, no sandbox. You are the package manager.

---
## `appimagelauncher`: Optional Polish

Most distros don't integrate `AppImages` with the desktop by default. `appimagelauncher` does.

```bash
# After installing appimagelauncher, double-clicking an AppImage offers:
# - Run once
# - Integrate (move to ~/Applications, add menu entry, register types)
# - Remove
```

Without it: you end up with `~/Downloads/foo.AppImage` and a desktop entry you wrote by hand. With it: it feels more like a real application.

---
## `nix`: A Different Philosophy

`nix` is not just a package manager — it's a *functional* package manager.

- Every package is built reproducibly from a description (`Nix expression`)
- Packages live under `/nix/store/<hash>-name-version/`, never overwritten
- Multiple versions coexist trivially
- Per-user "profiles" pick which packages are visible
- A configuration file can describe an entire system

```bash
# Install nix on any Linux (multi-user mode)
sh <(curl -L https://nixos.org/nix/install) --daemon

# Find and install a package
nix-env -qaP firefox
nix-env -iA nixpkgs.firefox

# Or with the modern flakes CLI
nix profile install nixpkgs#firefox

# Run without installing
nix run nixpkgs#hello

# Drop into a shell with packages, no install
nix shell nixpkgs#cowsay nixpkgs#fortune
```

---
## `nix` Strengths and Costs

Strengths:

- Reproducible. Same input → same output. Forever.
- Multi-version coexistence is trivial.
- Rollback is one command (`nix-env --rollback`).
- Works alongside *any* host distro without conflict.

Costs:

- The learning curve is real. The Nix language is its own thing.
- `/nix/store/` can grow quickly and confuses backup tools.
- Disk usage is higher than native packages.
- Documentation has historically been rough.

`nix` is loved by reproducibility-obsessed teams (and CI/CD pipelines) and ignored by everyone else. Worth knowing about.

---
## `guix`: The GNU Cousin

`guix` is `GNU`'s functional package manager, similar in design to `nix` but configured in `Guile Scheme` instead of the Nix language.

```bash
guix install firefox
guix package -i firefox
guix package -r firefox     # remove
guix pull                   # update guix itself
guix system reconfigure /etc/config.scm   # on Guix System
```

You won't run into `guix` in the wild as often as `nix`, but it's the same idea: declarative, reproducible, hash-keyed package store.

---
## When to Use Which

Rough guide:

- **Distribution package** — first choice. Tightest integration, smallest footprint, fastest startup, best security updates.
- **`flatpak`** — desktop GUI apps you want sandboxed and current. Most "I want the latest Firefox/GIMP/VS Code" use cases.
- **`snap`** — same niche as `flatpak`; specifically attractive on `Ubuntu` and for server-side apps `Canonical` ships (`lxd`, `microk8s`).
- **`appimage`** — one-shot tools, portable runs from a USB stick, demos.
- **`nix`/`guix`** — reproducibility-critical environments, multi-version dev setups, `NixOS` systems.

In practice: distro packages for the system, one universal format for the desktop apps, language tools for development.

---
## Mixing Universal Formats with Distro Packages

You can absolutely have all of these on one machine — and you usually do.

- A `flatpak` GIMP next to a `snap` VS Code next to an `apt`-installed `nginx` is fine. They don't share libraries.
- The downside is duplication: each universal app brings its own copy of `glib`, `gtk`, `Qt`, etc. Disk and RAM cost is real.
- Be careful with two installs of the *same* app — `firefox` from `apt`, `flatpak`, and `snap` simultaneously will leave you wondering why your bookmarks are in three places.

A simple rule: pick *one* installer per app. Pick the package manager that lifecycles it best.
