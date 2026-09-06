---
tags:
  - infrastructure:linux
  - audiences:sysadmin
level: intermediate
category: operating-systems
audience:
  - audiences:sysadmins
  - audiences:devops

---

# Choosing the Right Tool and Best Practices

---

## The Big Picture

We've now seen six worlds:

1. 1. 1. Distribution: `dpkg`/`apt`, `rpm`/`dnf`, `pacman`, `apk`
1. 1. 1. Sandboxed/universal: `flatpak`, `snap`, `appimage`
1. 1. 1. Declarative: `nix`, `guix`
1. 1. 1. Language: `pip`, `cargo`, `npm`, `gem`, `go`, ...
1. 1. 1. `GitHub` releases / pre-built binaries
1. 1. 1. Source builds

A real Linux machine usually mixes several. The question is not "which one is best?" — it's "which one for this need?"

---

## A Decision Flow

For a given thing you want to install:

- Is it part of the distribution and recent enough? → **distro package**
- Is there an official third-party repo from the vendor? → **distro package via that repo**
- Is it a sandboxed desktop GUI app? → **`flatpak` (or `snap`)**
- Is it a project-scoped library or developer tool? → **language package manager** in a project-local environment
- Is it a `Python` CLI tool you want available globally? → **`pipx`**
- Is it a `Rust` / `Go` CLI tool? → **`cargo install`** / **`go install`**
- Is it a static binary published as a `GitHub` release? → **download + verify + `/usr/local/bin/`**
- None of the above? → **build from source**, with `stow` or `checkinstall`

Walk the list top-to-bottom. Stop at the first match.

---

## Distro Package Manager Matrix

![distro_matrix](svg/courses/operating_systems/linux-package-managers/07_comparison_and_best_practices/distro_matrix.svg)

---

## Comparison: Trust Surface

How much do you have to trust to install this?

| Source | What you trust |
|---|---|
| Distro package | Distro maintainers + signed repo |
| Third-party repo with `signed-by` | Vendor + their key |
| `flatpak` from `flathub` | `Flathub` reviewers + app maintainer |
| `snap` from store | Canonical + publisher |
| `pip`/`cargo`/`npm` | Registry + every transitive author |
| `GitHub` release with signature | Project owners + their CI |
| `GitHub` release, no signature | The project + the network path |
| `curl ... \| sudo bash` | Everything, every time, no record |

Each row down trusts more parties. Pick accordingly.

---

## Comparison: Update Story

| Source | Updates |
|---|---|
| Distro package | `apt upgrade` / `dnf upgrade` |
| Third-party repo | Same as distro |
| `flatpak` | `flatpak update` (or auto) |
| `snap` | Automatic by default, mandatory eventually |
| Language package | Per-project, `pip install -U`, `cargo update` |
| `GitHub` release | Manual; you must notice |
| Source build | Manual; you must rebuild |

The further you get from system tools, the more security updates become *your* job.

---

## Comparison: Reproducibility

| Source | Same input → same output? |
|---|---|
| Distro package | Yes (with pinned version + repo snapshot) |
| Third-party repo | Yes |
| `flatpak`/`snap` | Yes (channels + revisions) |
| `appimage` | Yes (it's one file) |
| `nix`/`guix` | Yes — by design, from the ground up |
| Language package + lock file | Yes (lock file pins everything transitively) |
| Language package without lock file | No |
| `GitHub` release | Yes (tag is immutable) |
| Source build | Only if you pin source + toolchain + flags |

If you care about reproducibility, the answer rotates around lock files and pins.

---

## Mixing Package Managers Safely

You will mix them. Some rules of thumb that prevent most pain:

- **One owner per file.** Don't let `apt` and `pip` both write to `/usr/lib/python*/site-packages/`. Pick one.
- **One installer per app.** Don't have `firefox` from `apt`, `flatpak`, *and* `snap`.
- **Project tools live in projects.** `Node.js` deps in `node_modules/`. `Python` deps in `.venv/`. Don't put them in `/usr/`.
- **System tools live in system paths.** `nginx` belongs to `apt`. Don't `pip install` something that conflicts.
- **Per-user is your friend.** `~/.local/`, `~/.cargo/`, `~/.npm-global/`, `pipx`. No `sudo` needed, no system corruption possible.

If your `$PATH` has more than two `bin` directories, you're fine. If you're not sure which one wins, run `which`.

---

## Common Pitfalls

```bash
# 1. pip install as root, on the system Python
sudo pip install requests
# Conflicts with the distro's python3-requests. Tools start failing weirdly.

# 2. curl | sudo bash
curl -fsSL https://example.com/install.sh | sudo bash
# No verification, no audit, no uninstall, no version pin.

# 3. Forgetting to lock language deps
npm install express        # works today
npm install express        # different transitive tree tomorrow

# 4. Trusting an abandoned PPA
sudo add-apt-repository ppa:joe/ancient-stuff
# Last updated 2018. Probably has unpatched CVEs.

# 5. Disabling gpgcheck
gpgcheck=0   # in /etc/yum.repos.d/foo.repo
# You've turned off the chain of trust to silence one error.
```

Each of these is a real story you'll hear from real sysadmins.

---

## Auditing What's Installed

Periodically take stock. The whole point of a package manager is that it can answer this.

```bash
# Debian/Ubuntu — manually-installed packages
apt-mark showmanual

# What did I add via dpkg outside apt?
dpkg-query -W -f='${Package} ${Version}\n' > installed-packages.txt

# RHEL/Fedora — full transaction history
dnf history list
dnf history info LAST

# What's in /usr/local/bin not owned by any package?
find /usr/local/bin -type f -exec dpkg -S {} \; 2>&1 | \
  grep "no path found" | awk -F: '{print $2}'

# Snaps installed
snap list

# Flatpaks installed
flatpak list

# Per-user tools you may have forgotten about
ls ~/.cargo/bin/ ~/.local/bin/ ~/go/bin/ ~/.npm-global/bin/ 2>/dev/null
```

If you can't reproduce the list of installed software, you can't reproduce the machine.

---

## Reproducing a Machine

For a server you actually care about, "reinstall by hand" is not a recovery plan. A few approaches:

```bash
# Cheap and simple: export the manual-install set
sudo apt-mark showmanual > packages.txt
# On the new machine
xargs sudo apt install -y < packages.txt
```

```bash
# Better: a config-management tool that tracks intent
# - Ansible playbook with a list of packages
# - Puppet manifest
# - Chef recipe
# - NixOS configuration.nix
# - Dockerfile
```

```bash
# Best for cattle: don't reproduce the box, rebuild it
# - VM image baked with packer + ansible
# - Container image with a Dockerfile
# - NixOS rebuilt from a flake
```

The point: at *some* level you should have a written description of what's on the machine.

---

## Security: A Short List

The most-recommended-and-most-ignored list in this whole course.

1. 1. 1. **Use signed repositories.** `gpgcheck=1`. `signed-by=`. Always.
1. 1. 1. **Verify GitHub releases** with checksums and, if available, signatures (`gh attestation`, `cosign`).
1. 1. 1. **Pin language deps** with lock files in `git`.
1. 1. 1. **Run security updates promptly.** Configure `unattended-upgrades` (Debian/Ubuntu) or `dnf-automatic` (RHEL/Fedora).
1. 1. 1. **Don't `pip install` / `npm install -g` as `root`.** Use `pipx`, `venv`, per-user prefixes.
1. 1. 1. **Don't `curl | sudo bash`.** If you do, save the script first and read it.
1. 1. 1. **Keep an inventory.** Manual installs need a written record.
1. 1. 1. **Remove what you don't use.** `apt autoremove`, `flatpak uninstall --unused`, `pipx uninstall`.

---

## A Production Server Profile

For a typical Linux server, a sensible posture:

- Distro packages for everything the distro ships well: `nginx`, `postgresql`, `openssh`, `systemd` ecosystem.
- A handful of *signed* third-party repos for vendor software: `Docker`, `PostgreSQL` upstream, `kubernetes`.
- `unattended-upgrades` configured to apply security patches automatically.
- *No* desktop universal formats — no `flatpak`/`snap` GUI apps on a headless server.
- `Go`/`Rust`/`Python` tools pinned to versions, ideally inside containers.
- Manual `/usr/local/` installs documented in a runbook or `Ansible` playbook.

Boring is the goal. The exciting servers are the ones that page you at 3am.

---

## A Developer Workstation Profile

Different priorities — you're optimizing for fast iteration on many tools.

- Distro packages for the *base* (compilers, build tools, system libraries).
- `flatpak` from `flathub` for current GUI apps.
- `pipx` for `Python` CLIs (`black`, `httpie`, `poetry`).
- `cargo install` / `go install` for `Rust`/`Go` CLIs (`ripgrep`, `bat`, `fzf`).
- Per-project: `venv`, `Cargo.toml`, `package.json`, `go.mod`. Lockfiles always.
- Optionally `nix-shell` or `devbox` for ad-hoc reproducible environments.
- Some `~/bin/` for personal scripts.

Mix freely. Just keep one installer per app.

---

## Closing Exercise

Take any small open-source CLI tool of your choice. Install it five different ways and compare:

1. 1. 1. From the distro repository (if available)
1. 1. 1. From the project's `GitHub` release (verified)
1. 1. 1. As a `flatpak` or `snap` (if available)
1. 1. 1. With its language's package manager (`cargo install`, `pipx`, `npm install -g`, `go install`)
1. 1. 1. Built from source

For each:

- How long did the install take?
- How big is the install footprint?
- How do you upgrade it?
- How do you uninstall it cleanly?
- What runs as `root` during install?

You will end the exercise with strong opinions about which to reach for first.

---

## What to Take Away

- **Package managers are tools for managing risk and lifecycle**, not just for getting binaries onto disk.
- **The right tool depends on the question**: system service vs project library vs sandboxed app vs one-off CLI.
- **Mixing is fine, mixing carelessly is not.** One owner per file, one installer per app.
- **Security and reproducibility live in the package manager.** When you step outside, you take them with you.
- **Manual installs are a legitimate last resort** — but write down what you did, because in six months you won't remember.

The goal isn't to memorize every command. It's to know which world a problem belongs to and reach for the right tool the first time.
