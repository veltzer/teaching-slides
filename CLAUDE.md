# Project Rules

## General
- All project rules must be stored in this file (CLAUDE.md), not only in Claude memory. Memory is not shared with collaborators and can be erased.

## Python
- Use `#!/usr/bin/env python` in shebang lines, never `#!/usr/bin/env python3`. python3 is the default on all systems now.
- All scripts must be executable (`chmod +x`). Run them directly (`./scripts/foo.py`), never via `python scripts/foo.py`.
