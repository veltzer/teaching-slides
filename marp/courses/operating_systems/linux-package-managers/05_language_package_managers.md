---
tags:
  - infrastructure:linux
  - audiences:developers
level: intermediate
category: operating-systems
audience:
  - audiences:developers
  - audiences:devops

---
# Language-Specific Package Managers

---
## Why Every Language Has Its Own

Distribution packages can't be the answer for everything:

- A `Python` web app needs `flask 3.0` even if your distro ships `flask 2.2`.
- A `Rust` project pins `serde 1.0.193` exactly.
- Two services on one host need different `Node.js` versions.
- Developers on `Mac`, `Windows`, and `Linux` need to share dependencies.

System package managers solve "what is on this machine?". Language package managers solve "what does this *project* need?".

The two answer different questions and can both be right at the same time.

---
## Common Themes Across Languages

Every modern language package manager has roughly the same parts:

- A **registry** — `PyPI`, `crates.io`, `npm`, `RubyGems`, `Maven Central`, ...
- A **manifest** — `pyproject.toml`, `Cargo.toml`, `package.json`, `Gemfile`, `go.mod`
- A **lock file** — pin exact versions of every transitive dependency
- An **install command** — fetch, build, place
- A way to scope installs to a project, not the whole system
- Some notion of publishing your own package

Once you know one, the rest are vocabulary changes.

---
## Three Common Themes

![lang_pkg_themes](svg/courses/operating_systems/linux-package-managers/05_language_package_managers/lang_pkg_themes.svg)

---
## Lockfiles and Resolution

![lock_file_resolution](svg/courses/operating_systems/linux-package-managers/05_language_package_managers/lockfile_resolution.svg)

---
## `Python`: `pip`, `venv`, `pipx`, `poetry`, `uv`

`Python` packaging is famously fragmented. The pieces:

- `pip` — install packages from `PyPI` into the active interpreter
- `venv` — create an isolated `Python` environment (`python -m venv .venv`)
- `pipx` — install command-line `Python` apps in their own venv
- `poetry`, `pdm`, `hatch` — full project managers with `pyproject.toml`
- `uv` — a fast modern installer/resolver written in `Rust`, drop-in for `pip` + `venv`

The right answer depends on whether you're consuming, developing, or distributing.

---
## `pip` and `venv`: The Foundation

```bash
# Create a project-local environment
python -m venv .venv
source .venv/bin/activate

# Install packages into the venv
pip install requests flask

# Pin what you have
pip freeze > requirements.txt

# Reproduce on another machine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Leave the venv
deactivate
```

The `venv` is a directory of binaries and a `lib/python*/site-packages/` tree. Activating it just adjusts `$PATH`.

---
## `PEP 668`: "externally-managed-environment"

On modern `Debian`/`Ubuntu`/`Fedora`, this fails:

```bash
$ pip install requests
error: externally-managed-environment
× This environment is externally managed
╰─> To install Python packages system-wide, try apt install ...
```

This is intentional. Mixing `pip install` and the system's package manager corrupts the system `Python`. Three correct fixes:

```bash
# 1. Use a venv (best for projects)
python -m venv .venv && source .venv/bin/activate
pip install requests

# 2. Use pipx (best for CLI apps)
pipx install black
pipx install ruff

# 3. Use the distro package
sudo apt install python3-requests
```

The override `--break-system-packages` exists. Don't.

---
## `pipx`: `Python` CLI Apps Done Right

`pipx` installs each `Python` command-line tool in its own venv and exposes only the executables.

```bash
# Install pipx itself
sudo apt install pipx
pipx ensurepath          # add ~/.local/bin to PATH

# Install tools
pipx install black
pipx install ruff
pipx install httpie
pipx install poetry

# Run a one-off without installing
pipx run cookiecutter gh:audreyfeldroy/cookiecutter-pypackage

# Manage
pipx list
pipx upgrade black
pipx upgrade-all
pipx uninstall black
```

`pipx` is the right tool for `Python`-based command-line utilities you want available globally.

---
## `poetry` and Friends

`poetry` (and `pdm`, `hatch`) handle the full project lifecycle: `pyproject.toml`, lock file, virtual env, build, publish.

```bash
poetry new mypackage
cd mypackage
poetry add requests              # adds to pyproject.toml + locks
poetry add --group dev pytest
poetry install                   # creates venv, installs everything
poetry run pytest
poetry shell                     # interactive shell in the venv
poetry build                     # creates wheel + sdist
poetry publish                   # upload to PyPI
```

`pyproject.toml` is the manifest. `poetry.lock` is the lock file. Both go into git.

---
## `uv`: The New Fast Path

`uv` is a single tool that replaces `pip`, `pip-tools`, `virtualenv`, and a lot of `poetry`. Written in `Rust`, very fast.

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Drop-in pip + venv
uv venv
uv pip install requests

# Project workflow
uv init myproject && cd myproject
uv add requests
uv add --dev pytest
uv run pytest
uv lock
uv sync

# Tool management like pipx
uv tool install ruff
uv tool run black .
```

If you start a `Python` project today, `uv` is a strong default.

---
## `Rust`: `cargo` and `crates.io`

`cargo` is the package manager and build system that ships with `Rust`. There is one way to do things, and it works.

```bash
# Create a project
cargo new myapp
cd myapp

# Cargo.toml
[dependencies]
serde = "1.0"
tokio = { version = "1", features = ["full"] }

# Build, run, test
cargo build
cargo run
cargo test
cargo build --release      # optimized

# Update / pin
cargo update
cat Cargo.lock             # exact versions, commit this
```

```bash
# Install a binary crate as a CLI tool (~/.cargo/bin/)
cargo install ripgrep
cargo install --locked just

# Update / list
cargo install --list
cargo install -f ripgrep   # force reinstall / upgrade
```

`cargo install` is the easy way to get fast modern command-line tools (`ripgrep`, `bat`, `fd`, `eza`, `tokei`, ...).

---
## `JavaScript`/`Node.js`: `npm`, `yarn`, `pnpm`

Three competing package managers, one registry (`npm`).

```bash
# npm (ships with Node)
npm init -y
npm install express
npm install --save-dev jest
npm run test
npm ci                # clean install from package-lock.json

# yarn (Facebook, more deterministic, faster than old npm)
yarn add express
yarn add --dev jest
yarn install --frozen-lockfile

# pnpm (uses a content-addressable store, much less disk)
pnpm add express
pnpm install
```

All three read `package.json`. Each has its own lock file (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`).

`pnpm`'s killer feature: every version of every package exists once on disk, hard-linked into each project.

---
## `npm`: Local vs Global

```bash
# Local (default): installs into ./node_modules/
npm install express

# Global: installs into /usr/lib/node_modules or ~/.npm-global
sudo npm install -g typescript
```

Global `npm` installs as `root` are a frequent foot-gun. Two safer alternatives:

```bash
# 1. Tell npm to install globals into your home dir
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
export PATH="$HOME/.npm-global/bin:$PATH"
npm install -g typescript

# 2. Use npx for one-off runs (no install)
npx create-react-app my-app
npx prettier --write .
```

`npx` runs a package without installing it permanently. Great for project bootstrap tools.

---
## `Ruby`: `gem` and `bundler`

```bash
# Install a gem system-wide (or per-user)
gem install rails
gem install --user-install rails

# List, update, uninstall
gem list
gem update rails
gem uninstall rails

# Inside a project: Bundler is the project-scoped manager
cat > Gemfile <<'EOF'
source "https://rubygems.org"
gem "rails", "~> 7.1"
gem "puma"
EOF

bundle install
bundle exec rails server
bundle update rails
```

`Gemfile` + `Gemfile.lock` is the project pin. Run gems via `bundle exec` to get the project's pinned version, not whatever is on `$PATH`.

---
## `Go`: `go modules`

`Go` modules are baked into the toolchain. There is no separate package manager.

```bash
# Start a module
mkdir myapp && cd myapp
go mod init github.com/me/myapp

# Add a dependency by importing it and building
go get github.com/gin-gonic/gin
go build

# Tidy: drop unused, add missing
go mod tidy

# Lock file is go.sum (checksums)
cat go.mod
cat go.sum
```

```bash
# Install a Go-based CLI tool from a module path
go install github.com/junegunn/fzf@latest
# -> ~/go/bin/fzf, you put ~/go/bin in PATH
```

The model is simple: import a module by URL, the tool fetches it, the version goes in `go.mod`. No central registry — `Go` modules come from `git` repos directly (with a public proxy in front).

---
## `Java`: `maven`, `gradle`

The JVM world has two heavyweights and several niche tools.

```bash
# maven: pom.xml, very verbose XML, very predictable
mvn clean package
mvn install
mvn dependency:tree

# gradle: build.gradle / build.gradle.kts, faster, scriptable
gradle build
gradle test
gradle dependencies
```

The shared registry is `Maven Central`. Both tools talk to it. Both use a local cache (`~/.m2/repository/`, `~/.gradle/caches/`).

Lock files exist (Gradle's `gradle.lockfile`, Maven's `enforcer-plugin`-driven approach) but are less consistently used than in newer ecosystems.

---
## `Haskell`: `cabal` and `stack`

```bash
# cabal: the original
cabal init
cabal build
cabal run
cabal install pandoc       # installs the binary to ~/.cabal/bin/

# stack: layered on top, pins a "resolver" (Stackage snapshot) for reproducibility
stack new myproject
stack build
stack exec myproject
stack install pandoc       # ~/.local/bin/pandoc
```

`stack` was created specifically to fix `cabal`'s historical reproducibility pain via curated snapshots. Modern `cabal` has caught up with `cabal.project.freeze`.

---
## Common Cross-Language Pitfalls

- **Lockfiles in git.** `package-lock.json`, `Cargo.lock`, `poetry.lock`, `Gemfile.lock`, `go.sum` all belong in `git`. Without them, "works on my machine" is the rule.
- **Mixing system and language packages.** `pip install` as `root` is the canonical way to break a `Linux` desktop. Use `venv`/`pipx`. Same for `npm install -g` as `root`.
- **Stale registries.** Always run the equivalent of `*-update` before installing on a fresh machine.
- **Trusting transitive dependencies.** A small `npm` app can pull 800 packages from 300 maintainers. Audit it.
- **Typosquatting.** `pip install requets` (note typo) is a known attack vector. Copy-paste from the official docs.
- **Dependency confusion.** A private package name accidentally also exists on the public registry, and the public one wins.

---
## A Note on Versioning Schemes

Different ecosystems mean different things by `>=1.2.0` and `^1.2.0`.

| | `npm`/`Cargo` | `pip` | `gem` |
|---|---|---|---|
| `1.2.3` | exact | exact | exact |
| `^1.2.3` | `>=1.2.3 <2.0.0` | n/a | n/a |
| `~1.2.3` | `>=1.2.3 <1.3.0` | n/a (different meaning in `cabal`) | `>=1.2.3 <1.3.0` |
| `1.2.*` | n/a | `>=1.2,<1.3` | n/a |
| `>=1.2,<2` | yes | yes | `>=1.2,<2` |

When you read someone else's manifest, check what the symbols mean in *that* ecosystem. The same character can mean different things.

---
## Private Registries and Mirrors

Most of these tools support both:

```bash
# pip: --index-url
pip install --index-url https://nexus.example.com/repository/pypi/simple/ requests

# npm: registry config
npm config set registry https://nexus.example.com/repository/npm/
npm install express

# cargo: ~/.cargo/config.toml
[source.crates-io]
replace-with = "internal"
[source.internal]
registry = "https://internal.example.com/git/index"

# gem
gem sources --add https://nexus.example.com/repository/gems/
```

In an enterprise setting you'll often install through a proxy like `Nexus`, `Artifactory`, or `JFrog`. That gives you caching, vendored packages, and a single audit point.
