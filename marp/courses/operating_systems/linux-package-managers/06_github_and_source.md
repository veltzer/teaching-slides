---
tags:
  - infrastructure:linux
  - audiences:sysadmin
  - audiences:developers
level: intermediate
category: operating-systems
audience:
  - audiences:sysadmins
  - audiences:developers

---

# GitHub Releases and Source Builds

---

## When the Distro Doesn't Have It

The package manager covers most cases. The remaining ones:

- The distro version is too old, and there is no official `PPA` or `Copr`.
- The project doesn't ship distro packages at all.
- You need a *specific* release for compatibility.
- It's an internal binary your company built.

For these you have two paths:

- Download a pre-built binary, often from a `GitHub` release.
- Build from source.

Both work, both are common, both come with the same caveat: you, not the package manager, now own the lifecycle.

---

## `GitHub` Releases as a Distribution Channel

`GitHub` lets each project attach binaries to a tagged release.

- Predictable URL: `github.com/owner/repo/releases`
- Often pre-built per OS and architecture (`...-linux-amd64.tar.gz`, `...-linux-arm64.tar.gz`)
- Usually accompanied by a `SHA256SUMS` file
- Increasingly accompanied by signatures (`cosign`, `gh attestation`)
- Versioned via `git` tags

This is how a huge fraction of modern infrastructure tooling ships: `kubectl`, `helm`, `terraform`, `gh`, `k9s`, `lazygit`, ...

---

## Downloading a `GitHub` Release By Hand

```bash
# 1. Find the release page
# https://github.com/cli/cli/releases

# 2. Pick the right asset for your platform
curl -L -o gh.tar.gz \
  https://github.com/cli/cli/releases/download/v2.50.0/gh_2.50.0_linux_amd64.tar.gz

# 3. Verify the checksum (the project will publish one)
curl -L -o checksums.txt \
  https://github.com/cli/cli/releases/download/v2.50.0/gh_2.50.0_checksums.txt
sha256sum -c --ignore-missing checksums.txt

# 4. Extract and place the binary
tar xzf gh.tar.gz
sudo install -m 0755 gh_2.50.0_linux_amd64/bin/gh /usr/local/bin/gh

# 5. Verify
gh --version
```

`/usr/local/bin/` is the conventional place for locally-installed binaries. Distros leave it alone.

---

## Using the `gh` CLI to Fetch Releases

If you have `gh` installed, fetching is much nicer.

```bash
# List recent releases of a repo
gh release list --repo cli/cli

# Show details
gh release view v2.50.0 --repo cli/cli

# Download all assets of a release into the current dir
gh release download v2.50.0 --repo cli/cli

# Download a specific asset by glob
gh release download --repo cli/cli --pattern '*linux_amd64.tar.gz'

# Latest release
gh release download --repo cli/cli --pattern '*linux_amd64.tar.gz'
```

Convenient in scripts because you don't have to URL-build by hand.

---

## Verifying What You Downloaded

The download is only as trustworthy as the verification step. The minimum is a checksum, ideally a signature.

```bash
# Step 1: SHA256 against a published checksums file
sha256sum -c --ignore-missing checksums.txt

# Step 2: GPG signature, classic style
curl -L -o release.tar.gz.asc https://example.com/release.tar.gz.asc
gpg --verify release.tar.gz.asc release.tar.gz

# Step 3: Modern artifact attestations on GitHub (sigstore-backed)
gh attestation verify release.tar.gz --owner cli

# Step 4: cosign signatures (popular for container/OCI artifacts)
cosign verify-blob \
  --certificate release.tar.gz.crt \
  --signature release.tar.gz.sig \
  release.tar.gz
```

If a project offers signatures and you skip them, you've made the download untrusted on purpose.

---

## Where to Put the Binary

`Linux` has informal conventions. Pick one and be consistent.

| Path | When to use |
|---|---|
| `/usr/local/bin/` | Available to all users, you're root |
| `/opt/<app>/` | Self-contained app with many files |
| `~/.local/bin/` | Per-user, no `sudo` needed |
| `~/bin/` | Per-user, classic UNIX style |

```bash
# Make sure ~/.local/bin is in PATH (it is by default on most distros)
echo $PATH | tr ':' '\n' | grep local

# Drop a single binary in
install -m 0755 ./gh ~/.local/bin/

# Drop a self-contained app in /opt
sudo mkdir -p /opt/myapp
sudo tar xzf myapp-1.0.tar.gz -C /opt/myapp --strip-components=1
sudo ln -s /opt/myapp/bin/myapp /usr/local/bin/myapp
```

Avoid `/usr/bin/` and `/bin/`. Those belong to the distro's package manager.

---

## The Real Problem: There Is No Lifecycle

Once you `cp` a binary into `/usr/local/bin`, the system has no idea:

- where it came from
- what version it is
- whether it has known CVEs
- how to upgrade it
- how to remove it cleanly

`apt list --installed` won't show it. `dnf history` won't show it. `rpm -qf /usr/local/bin/foo` returns "not owned by any package". Three months from now, *you* are the package manager.

---

## Mitigating the Lifecycle Gap

A few practical patterns to make this less painful.

```bash
# 1. Keep a manifest of what you installed manually
cat >> ~/.local/manual-install.log <<EOF
$(date -I) gh 2.50.0 sha256:abc... /usr/local/bin/gh
EOF
```

```bash
# 2. Wrap in a script with version embedded
sudo tee /usr/local/bin/install-gh > /dev/null <<'EOF'
#!/bin/bash
VERSION="2.50.0"
SHA="..."
curl -L -o /tmp/gh.tar.gz \
  https://github.com/cli/cli/releases/download/v${VERSION}/gh_${VERSION}_linux_amd64.tar.gz
echo "$SHA  /tmp/gh.tar.gz" | sha256sum -c
tar -C /tmp -xzf /tmp/gh.tar.gz
install -m 0755 /tmp/gh_${VERSION}_linux_amd64/bin/gh /usr/local/bin/gh
EOF
sudo chmod +x /usr/local/bin/install-gh
```

This isn't beautiful. It is, however, the difference between "I can recreate this server" and "I cannot."

---

## Source Install Flow

![source_install_flow](svg/courses/operating_systems/linux-package-managers/06_github_and_source/source_install_flow.svg)

---

## Building From Source: The Classic `autotools` Recipe

```bash
# 1. Download the source tarball and verify the signature
wget https://example.com/myapp-1.0.tar.gz
wget https://example.com/myapp-1.0.tar.gz.sig
gpg --verify myapp-1.0.tar.gz.sig

# 2. Extract
tar xzf myapp-1.0.tar.gz
cd myapp-1.0

# 3. Configure, build, install
./configure --prefix=/usr/local
make -j$(nproc)
sudo make install

# 4. Some projects support uninstall, many don't
sudo make uninstall
```

`./configure` checks for build dependencies and adapts to your system. If it fails, the message usually tells you which `-dev` package to install.

---

## Build Dependencies on Debian/Ubuntu

```bash
# The "everything you usually need to build C/C++ code"
sudo apt install build-essential

# Per-package: ask apt for the build deps of an existing package
sudo apt build-dep nginx

# Common -dev libraries
sudo apt install libssl-dev libxml2-dev zlib1g-dev pkg-config
```

If a project's `./configure` says `error: cannot find libfoo`, the answer is almost always `apt install libfoo-dev`.

---

## Build Dependencies on RHEL/Fedora

```bash
# The equivalent meta-package
sudo dnf groupinstall "Development Tools"
# or
sudo dnf install gcc gcc-c++ make autoconf automake

# Per-package build deps
sudo dnf builddep nginx

# -dev libraries are -devel here
sudo dnf install openssl-devel libxml2-devel zlib-devel
```

Naming convention reminder: `Debian` uses `-dev`, `Red Hat` uses `-devel`. Otherwise it's the same idea.

---

## `cmake`, `meson`, `ninja`: The Modern Builds

Many newer projects don't use `autotools`. The most common alternatives:

```bash
# cmake: out-of-tree build is the convention
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
cmake --build . -j$(nproc)
sudo cmake --install .

# meson + ninja: faster, simpler config language
meson setup build --prefix=/usr/local
meson compile -C build
sudo meson install -C build

# bare make: ./configure replaced by editing a Makefile
make -j$(nproc)
sudo make install PREFIX=/usr/local
```

The shape is always the same: configure → build → install. The vocabulary changes per build system.

---

## `checkinstall`: Wrap a `make install` in a `.deb`

`checkinstall` runs `make install`, watches what files appear, and packages them into a `.deb` (or `.rpm`).

```bash
sudo apt install checkinstall

cd myapp-1.0
./configure --prefix=/usr/local
make -j$(nproc)

# Instead of "sudo make install":
sudo checkinstall \
  --pkgname=myapp \
  --pkgversion=1.0 \
  --pkgrelease=1 \
  --maintainer="me@example.com" \
  --requires="libc6,libssl3"

# Now you have a real .deb
ls myapp_1.0-1_amd64.deb

# Remove cleanly via dpkg
sudo dpkg -r myapp
```

Crude but effective. The `.deb` it produces is not great for redistribution, but it gives you a clean uninstall.

---

## `GNU stow`: A Directory Per Manual Install

`stow` lets you install several manual builds without them stepping on each other.

```bash
sudo apt install stow

# Build to a per-app prefix
./configure --prefix=/usr/local/stow/myapp-1.0
make -j$(nproc)
sudo make install

# Activate: stow creates symlinks from /usr/local/{bin,lib,...} into the prefix
cd /usr/local/stow
sudo stow myapp-1.0

# Deactivate: removes the symlinks, files stay
sudo stow -D myapp-1.0
```

`/usr/local/stow/myapp-1.0/` and `/usr/local/stow/myapp-1.1/` can coexist. Switch by `unstow` + `stow`.

---

## `apt source` and `dpkg-buildpackage`

If a Debian package exists but you want a tweaked version, build it from the distro's source package.

```bash
# Make sure deb-src lines are enabled in /etc/apt/sources.list

# Download the source
apt source nginx

# Install the build deps
sudo apt build-dep nginx

# Patch / modify
cd nginx-*/
# ...edit code, debian/changelog, debian/control...

# Build
dpkg-buildpackage -us -uc -b

# Install the resulting .deb
cd ..
sudo dpkg -i nginx_*.deb
```

This is the *right* way to make a custom build of a distro package. You stay inside the package manager's ecosystem.

---

## The Hidden Cost: Security Updates

This is the killer argument for using package managers.

When a CVE drops in `openssl`:

- `apt` users run `apt upgrade` and they're done.
- `dnf` users run `dnf upgrade` and they're done.
- `flatpak`/`snap` users get an automatic background update.

But:

- Manually-installed `/usr/local/bin/foo` linked against a vendored `openssl`? You have to know about the CVE, find the project's release page, download a new binary, verify it, install it.
- A program built from source against a vendored library? You rebuild it.

Multiplied across dozens of manual installs on a server, this becomes the difference between "patched" and "vulnerable for six months because no one remembered."

---

## Source Build Checklist

If you're going to build from source, make it survivable.

1. 1. 1. Document *what* and *why* in `/usr/local/src/<app>/README.md` or similar.
1. 1. 1. Verify signature/checksum before building.
1. 1. 1. Build into `/usr/local/stow/<app>-<version>/` or `/opt/<app>/`. Never `/usr/bin/`.
1. 1. 1. Wrap with `checkinstall` if it's a one-off binary.
1. 1. 1. Record the build dependencies (`apt build-dep` output).
1. 1. 1. Subscribe to the project's security mailing list or `Atom` feed.
1. 1. 1. Plan the *uninstall* before you do the install. If you can't, don't.

If any of these feels like too much effort: that's a sign you should be looking for a `flatpak`, a `snap`, a third-party repo, or a language-package version instead.
