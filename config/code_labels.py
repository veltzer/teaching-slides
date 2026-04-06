"""
Valid code block language labels for this project.
Extracted from text_labels.txt — edit that file as the source of truth,
then keep this module in sync.
"""

# Standard languages (Prism-recognised syntax highlighting)
STANDARD = frozenset({
    "bash",
    "python",
    "c",
    "cpp",
    "csharp",
    "rust",
    "yaml",
    "json",
    "hcl",
    "cmake",
    "markdown",
    "scala",
    "javascript",
    "makefile",
    "java",
    "sql",
    "dockerfile",
    "ini",
    "toml",
    "html",
    "go",
    "xml",
    "ruby",
    "typescript",
    "gas",
    "dts",
    "nginx",
    "kotlin",
    "php",
    "lua",
    "groovy",
    "css",
    "jsx",
    "graphql",
    "protobuf",
    "diff",
    "http",
    "jinja",
})

# Custom semantic labels (no syntax highlighting, for categorisation)
SEMANTIC = frozenset({
    "tree",
    "diagram",
    "config",
    "output",
    "console",
    "template",
    "gitignore",
    "cron",
    "protocol",
    "misc",
})

# Rare / one-off labels
RARE = frozenset({
    "esql",
    "asm",
    "arm",
    "nasm",
    "mips",
    "riscv",
    "ld",
    "gdb",
    "promql",
    "cython",
    "cuda",
    "redis",
    "rego",
    "vim",
    "apache",
    "properties",
    "conf",
    "jsonc",
    "jsonl",
    "asl",
    "wat",
    "terraform",
    "gitattributes",
    "cfg",
})

# Full set of all valid labels
VALID: frozenset = STANDARD | SEMANTIC | RARE
