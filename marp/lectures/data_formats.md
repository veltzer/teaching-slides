# Data Formats

---

## Why Data Formats Matter

- Every application reads and writes data
- Choosing the right format affects performance, readability, and interoperability
- No single format fits all use cases
- Understanding trade-offs is key to making good decisions

---

## The Formats We Will Cover

1. CSV
1. INI
1. JSON
1. YAML
1. TOML
1. JSON Lines (JSONL)
1. Parquet
1. SQLite
1. XML
1. MessagePack / Protocol Buffers (binary formats)

---

## Format Categories

<svg viewBox="0 0 700 300" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="20" width="200" height="260" rx="10" fill="#e3f2fd" stroke="#1565c0" stroke-width="2"/>
  <text x="110" y="50" text-anchor="middle" font-weight="bold" font-size="14">Text-Based</text>
  <text x="110" y="80" text-anchor="middle" font-size="12">CSV, INI, JSON</text>
  <text x="110" y="100" text-anchor="middle" font-size="12">YAML, TOML, XML</text>
  <text x="110" y="120" text-anchor="middle" font-size="12">JSON Lines</text>
  <text x="110" y="160" text-anchor="middle" font-size="11" fill="#555">Human-readable</text>
  <text x="110" y="180" text-anchor="middle" font-size="11" fill="#555">Easy to edit</text>
  <text x="110" y="200" text-anchor="middle" font-size="11" fill="#555">Larger file size</text>
  <text x="110" y="220" text-anchor="middle" font-size="11" fill="#555">Slower to parse</text>

  <rect x="250" y="20" width="200" height="260" rx="10" fill="#fce4ec" stroke="#c62828" stroke-width="2"/>
  <text x="350" y="50" text-anchor="middle" font-weight="bold" font-size="14">Binary</text>
  <text x="350" y="80" text-anchor="middle" font-size="12">Parquet, SQLite</text>
  <text x="350" y="100" text-anchor="middle" font-size="12">MessagePack, Protobuf</text>
  <text x="350" y="160" text-anchor="middle" font-size="11" fill="#555">Not human-readable</text>
  <text x="350" y="180" text-anchor="middle" font-size="11" fill="#555">Compact storage</text>
  <text x="350" y="200" text-anchor="middle" font-size="11" fill="#555">Fast to parse</text>
  <text x="350" y="220" text-anchor="middle" font-size="11" fill="#555">Needs special tools</text>

  <rect x="490" y="20" width="200" height="260" rx="10" fill="#e8f5e9" stroke="#2e7d32" stroke-width="2"/>
  <text x="590" y="50" text-anchor="middle" font-weight="bold" font-size="14">Database-Like</text>
  <text x="590" y="80" text-anchor="middle" font-size="12">SQLite, Parquet</text>
  <text x="590" y="160" text-anchor="middle" font-size="11" fill="#555">Queryable</text>
  <text x="590" y="180" text-anchor="middle" font-size="11" fill="#555">Indexed access</text>
  <text x="590" y="200" text-anchor="middle" font-size="11" fill="#555">Schema enforcement</text>
  <text x="590" y="220" text-anchor="middle" font-size="11" fill="#555">Partial reads</text>
</svg>

---

## CSV - Comma-Separated Values

- One of the oldest and simplest data formats
- Each line is a record, fields separated by commas
- Optional header row for column names
- Widely supported by spreadsheets, databases, and programming languages

---

## CSV Example

```csv
name,age,city,salary
Alice,30,New York,85000
Bob,25,San Francisco,92000
"O'Brien, Carol",35,Chicago,78000
```

Note: fields containing commas or quotes must be quoted.

---

## CSV Advantages

- Universally supported (Excel, databases, every language)
- Human-readable and editable with any text editor
- Very compact for tabular data
- Easy to generate and parse
- Streamable — process line by line without loading entire file

---

## CSV Disadvantages

- No standard specification (RFC 4180 exists but is not universally followed)
- No data types — everything is a string
- No nested or hierarchical data
- Encoding ambiguity (quoting, escaping, delimiters vary)
- No metadata or schema
- Delimiter conflicts (`TSV` uses tabs as alternative)

---

## CSV Best Practices

- Always include a header row
- Use RFC 4180 quoting rules
- Use UTF-8 encoding
- Consider `TSV` (tab-separated) when data contains many commas
- For large datasets, consider switching to Parquet

---

## INI Files

- Simple configuration file format
- Originated in early Windows systems
- Organized into sections with key-value pairs
- Still widely used: `git config`, `pip.conf`, `php.ini`, `systemd`

---

## INI Example

```ini
[database]
host = localhost
port = 5432
name = myapp

[logging]
level = INFO
file = /var/log/app.log

[feature_flags]
new_ui = true
dark_mode = false
```

---

## INI Advantages

- Extremely simple and human-readable
- Easy to edit by hand
- Sections provide natural grouping
- Low cognitive overhead for configuration

---

## INI Disadvantages

- No formal standard — implementations vary
- No nested structures (only one level of sections)
- No data types — values are strings
- No arrays or lists (some implementations add them non-standardly)
- No comments standard (`;` vs `#` varies)
- Being replaced by TOML in modern projects

---

## JSON - JavaScript Object Notation

- Lightweight data interchange format
- Derived from JavaScript but language-independent
- The de facto standard for web APIs
- Defined by RFC 8259

---

## JSON Example

```json
{
    "name": "Alice",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York"
    },
    "hobbies": ["reading", "cycling"],
    "active": true,
    "score": null
}
```

---

## JSON Data Types

| Type | Example |
|------|---------|
| String | `"hello"` |
| Number | `42`, `3.14`, `-1` |
| Boolean | `true`, `false` |
| Null | `null` |
| Array | `[1, 2, 3]` |
| Object | `{"key": "value"}` |

---

## JSON Advantages

- Universal support across all programming languages
- Self-describing with nested structures
- Native to web browsers and JavaScript
- Human-readable (when formatted)
- Well-defined specification
- Excellent tooling (`jq`, linters, validators)

---

## JSON Disadvantages

- No comments allowed in standard JSON
- Verbose — lots of quotes and braces
- No date/time type (use ISO 8601 strings by convention)
- No binary data (must Base64-encode)
- Trailing commas not allowed
- Entire file must be loaded to parse (no streaming by default)
- No schema enforcement built in (JSON Schema is separate)

---

## YAML - YAML Ain't Markup Language

- Human-friendly data serialization format
- Superset of JSON (valid JSON is valid YAML)
- Popular for configuration: Kubernetes, Docker Compose, Ansible, GitHub Actions

---

## YAML Example

```yaml
name: Alice
age: 30
address:
    street: 123 Main St
    city: New York
hobbies:
    - reading
    - cycling
active: true
score: null
```

---

## YAML Advantages

- Very human-readable — minimal syntax noise
- Supports comments with `#`
- Multi-line strings with `|` and `>`
- Anchors and aliases for reuse (`&` and `*`)
- Multiple documents in one file (`---` separator)
- Rich type system including dates

---

## YAML Disadvantages

- Indentation-sensitive — easy to make subtle errors
- Complex specification (the YAML spec is very large)
- Security risk: some parsers execute arbitrary code via tags
- The "Norway problem": `NO` is parsed as `false`
- Implicit type coercion surprises: `3.10` becomes `3.1`
- Slower to parse than JSON
- Multiple ways to express the same thing

---

## YAML Gotchas

```yaml
# These are all boolean false!
norway: NO
answer: no
flag: off

# This is a float, not a version string
python_version: 3.10  # becomes 3.1

# Fix with quotes:
norway: "NO"
python_version: "3.10"
```

Always quote strings that could be misinterpreted.

---

## TOML - Tom's Obvious Minimal Language

- Designed to be a minimal configuration file format
- Easy to read due to obvious semantics
- Used by Rust (`Cargo.toml`), Python (`pyproject.toml`), Hugo
- Specification: https://toml.io

---

## TOML Example

```toml
title = "My Application"

[database]
host = "localhost"
port = 5432
enabled = true

[servers.alpha]
ip = "10.0.0.1"
role = "frontend"

[servers.beta]
ip = "10.0.0.2"
role = "backend"
```

---

## TOML Advantages

- Unambiguous — each value has a clear type
- Native date/time support
- Comments with `#`
- No indentation sensitivity
- Maps clearly to a hash table
- Simpler specification than YAML

---

## TOML Disadvantages

- Deeply nested structures become verbose
- Less suitable for data interchange (designed for config)
- Smaller ecosystem than JSON or YAML
- Arrays of tables syntax can be confusing
- Not ideal for large or complex data structures

---

## TOML vs YAML vs JSON for Config

| Feature | JSON | YAML | TOML |
|---------|------|------|------|
| Comments | No | Yes | Yes |
| Date type | No | Yes | Yes |
| Human editing | OK | Good | Good |
| Nesting | Good | Good | Verbose |
| Ambiguity | Low | High | Low |
| Spec complexity | Low | High | Medium |

---

## JSON Lines (JSONL)

- One JSON object per line
- No enclosing array or commas between records
- File extension: `.jsonl` or `.ndjson`
- Ideal for log files, streaming, and large datasets

---

## JSON Lines Example

```json
{"name": "Alice", "age": 30, "city": "New York"}
{"name": "Bob", "age": 25, "city": "San Francisco"}
{"name": "Carol", "age": 35, "city": "Chicago"}
```

Each line is a complete, valid JSON object.

---

## JSON Lines Advantages

- Streamable — process one record at a time
- Appendable — just add a new line
- Trivial to split and merge files
- Parallelizable — each line is independent
- Works with `grep`, `wc`, `head`, `tail`
- Constant memory usage regardless of file size

---

## JSON Lines Disadvantages

- No schema or header (each line must be self-contained)
- Slightly larger than CSV for flat tabular data
- No standard way to represent relationships between records
- Less human-friendly than formatted JSON for complex objects

---

## JSON Lines Use Cases

- Application log files
- Data pipeline intermediate format
- Streaming APIs and webhooks
- Machine learning training data
- Large dataset exports from databases

---

## Parquet

- Columnar storage format from the Apache ecosystem
- Designed for efficient analytics on large datasets
- Used heavily in Spark, Hadoop, Pandas, and data lakes

---

## Parquet Architecture

<svg viewBox="0 0 600 280" xmlns="http://www.w3.org/2000/svg">
  <text x="300" y="20" text-anchor="middle" font-weight="bold" font-size="14">Row-Oriented vs Column-Oriented</text>

  <rect x="20" y="40" width="250" height="30" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="145" y="60" text-anchor="middle" font-size="11" font-weight="bold">Row Storage (CSV, JSON)</text>
  <rect x="20" y="70" width="250" height="20" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <text x="145" y="84" text-anchor="middle" font-size="10">Alice | 30 | New York</text>
  <rect x="20" y="90" width="250" height="20" fill="#e3f2fd" stroke="#333" stroke-width="1"/>
  <text x="145" y="104" text-anchor="middle" font-size="10">Bob | 25 | San Francisco</text>
  <rect x="20" y="110" width="250" height="20" fill="#bbdefb" stroke="#333" stroke-width="1"/>
  <text x="145" y="124" text-anchor="middle" font-size="10">Carol | 35 | Chicago</text>

  <rect x="330" y="40" width="250" height="30" fill="#fce4ec" stroke="#333" stroke-width="1"/>
  <text x="455" y="60" text-anchor="middle" font-size="11" font-weight="bold">Column Storage (Parquet)</text>
  <rect x="330" y="70" width="250" height="20" fill="#f8bbd0" stroke="#333" stroke-width="1"/>
  <text x="455" y="84" text-anchor="middle" font-size="10">name: Alice | Bob | Carol</text>
  <rect x="330" y="90" width="250" height="20" fill="#fce4ec" stroke="#333" stroke-width="1"/>
  <text x="455" y="104" text-anchor="middle" font-size="10">age: 30 | 25 | 35</text>
  <rect x="330" y="110" width="250" height="20" fill="#f8bbd0" stroke="#333" stroke-width="1"/>
  <text x="455" y="124" text-anchor="middle" font-size="10">city: NY | SF | Chicago</text>

  <text x="145" y="160" text-anchor="middle" font-size="11" fill="#555">Read all fields per record</text>
  <text x="455" y="160" text-anchor="middle" font-size="11" fill="#555">Read only needed columns</text>
</svg>

---

## Parquet Advantages

- Excellent compression (similar values in same column)
- Column pruning — read only the columns you need
- Predicate pushdown — skip irrelevant row groups
- Schema embedded in the file
- Supports complex nested types
- Extremely fast for analytical queries

---

## Parquet Disadvantages

- Not human-readable (binary format)
- Not suitable for record-by-record appends
- Overhead for small files
- Requires specialized libraries to read/write
- Not suitable for configuration or small datasets
- Write-once pattern — cannot update individual rows

---

## Parquet with Python

```python
import pandas as pd

# Write Parquet
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol"],
    "age": [30, 25, 35],
    "city": ["New York", "SF", "Chicago"]
})
df.to_parquet("people.parquet")

# Read Parquet (only specific columns)
df = pd.read_parquet("people.parquet", columns=["name", "age"])
```

---

## SQLite

- Serverless, self-contained relational database
- Stored as a single file
- The most widely deployed database engine in the world
- Built into Python, Android, iOS, browsers, and more

---

## SQLite as a Data Format

- A `.sqlite` or `.db` file is a complete database
- Supports SQL queries, indexes, views, triggers
- ACID-compliant transactions
- Handles concurrent readers (single writer)
- Maximum database size: 281 TB

---

## SQLite Advantages

- Full SQL query support
- Indexes for fast lookups
- ACID transactions
- Schema enforcement with types and constraints
- Zero configuration — no server needed
- Excellent for local/embedded data storage

---

## SQLite Disadvantages

- Binary format — not human-readable
- Single-writer limitation (concurrent reads are fine)
- Not ideal for high-write-throughput scenarios
- Overkill for simple key-value or flat data
- Not designed for network access (use PostgreSQL instead)
- Schema changes can be awkward

---

## SQLite with Python

```python
import sqlite3

conn = sqlite3.connect("people.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS people (
        name TEXT, age INTEGER, city TEXT
    )
""")

cursor.execute(
    "INSERT INTO people VALUES (?, ?, ?)",
    ("Alice", 30, "New York")
)
conn.commit()

for row in cursor.execute("SELECT * FROM people WHERE age > 25"):
    print(row)

conn.close()
```

---

## XML - eXtensible Markup Language

- Tag-based hierarchical format
- Was the dominant data interchange format before JSON
- Still used in SOAP, RSS, SVG, XHTML, Maven, `.csproj`

---

## XML Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<people>
    <person active="true">
        <name>Alice</name>
        <age>30</age>
        <address>
            <city>New York</city>
        </address>
    </person>
</people>
```

---

## XML Advantages

- Rich ecosystem: XPath, XSLT, XSD schemas
- Attributes and elements provide flexible modeling
- Namespaces for combining vocabularies
- Mature validation with DTD and XML Schema
- Well-suited for document-oriented data

---

## XML Disadvantages

- Very verbose — tags repeated for open and close
- Complex to parse compared to JSON
- Namespaces add complexity
- No native array type
- Largely replaced by JSON for web APIs
- Heavier tooling requirements

---

## Binary Formats: MessagePack and Protocol Buffers

**MessagePack:**
- Binary JSON — same data model, smaller and faster
- Drop-in replacement where JSON is used
- No schema required

**Protocol Buffers (Protobuf):**
- Google's schema-driven binary format
- Requires `.proto` schema definition
- Extremely compact and fast
- Used in gRPC

---

## Binary Formats Comparison

| Feature | JSON | MessagePack | Protobuf |
|---------|------|-------------|----------|
| Human-readable | Yes | No | No |
| Schema required | No | No | Yes |
| Size | Large | Small | Smallest |
| Parse speed | Slow | Fast | Fastest |
| Language support | All | Many | Many |
| Self-describing | Yes | Yes | No |

---

## Format Comparison: Size and Speed

For 1 million records with 5 fields:

| Format | Approx Size | Write Speed | Read Speed |
|--------|-------------|-------------|------------|
| CSV | 50 MB | Fast | Fast |
| JSON | 80 MB | Medium | Medium |
| JSONL | 75 MB | Fast | Fast |
| Parquet | 10 MB | Slow | Very Fast |
| SQLite | 40 MB | Medium | Very Fast |
| Protobuf | 20 MB | Fast | Very Fast |

Sizes and speeds are approximate and depend on the data.

---

## When to Use Each Format

| Use Case | Best Format |
|----------|-------------|
| Web API responses | JSON |
| Application config | TOML or YAML |
| Simple config | INI |
| Spreadsheet export | CSV |
| Log files | JSON Lines |
| Big data analytics | Parquet |
| Local app storage | SQLite |
| Document markup | XML |
| High-perf RPC | Protobuf |
| Data pipelines | JSONL or Parquet |

---

## Converting Between Formats

Python is the Swiss Army knife for format conversion:

```python
import pandas as pd

# CSV -> Parquet
df = pd.read_csv("data.csv")
df.to_parquet("data.parquet")

# JSON -> CSV
df = pd.read_json("data.json")
df.to_csv("data.csv", index=False)

# CSV -> SQLite
import sqlite3
conn = sqlite3.connect("data.db")
df = pd.read_csv("data.csv")
df.to_sql("mytable", conn, index=False)
```

---

## Converting with Command-Line Tools

```bash
# JSON -> CSV using jq
jq -r '[.name, .age, .city] | @csv' data.json

# CSV -> JSON using miller
mlr --icsv --ojson cat data.csv

# YAML -> JSON using yq
yq -o=json data.yaml

# TOML -> JSON using tomlq (part of yq)
tomlq . config.toml

# JSONL -> CSV using jq
jq -r '[.name, .age] | @csv' data.jsonl > data.csv
```

---

## Converting: INI to Other Formats

```python
import configparser
import json

config = configparser.ConfigParser()
config.read("config.ini")

# INI -> dict -> JSON
data = {s: dict(config[s]) for s in config.sections()}
print(json.dumps(data, indent=4))
```

```json
{
    "database": {
        "host": "localhost",
        "port": "5432"
    }
}
```

---

## Format Selection Decision Tree

<svg viewBox="0 0 700 420" xmlns="http://www.w3.org/2000/svg">
  <rect x="250" y="10" width="200" height="35" rx="5" fill="#e3f2fd" stroke="#333" stroke-width="1.5"/>
  <text x="350" y="33" text-anchor="middle" font-size="12" font-weight="bold">Is it configuration?</text>

  <line x1="250" y1="27" x2="150" y2="70" stroke="#333" stroke-width="1.5"/>
  <text x="185" y="47" font-size="10" fill="#2e7d32">Yes</text>
  <line x1="450" y1="27" x2="550" y2="70" stroke="#333" stroke-width="1.5"/>
  <text x="510" y="47" font-size="10" fill="#c62828">No</text>

  <rect x="50" y="70" width="200" height="35" rx="5" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="150" y="93" text-anchor="middle" font-size="12" font-weight="bold">Nested structure?</text>

  <line x1="50" y1="87" x2="20" y2="130" stroke="#333" stroke-width="1.5"/>
  <text x="20" y="110" font-size="10" fill="#c62828">No</text>
  <line x1="250" y1="87" x2="260" y2="130" stroke="#333" stroke-width="1.5"/>
  <text x="268" y="110" font-size="10" fill="#2e7d32">Yes</text>

  <rect x="-10" y="130" width="70" height="30" rx="5" fill="#fff9c4" stroke="#333" stroke-width="1"/>
  <text x="25" y="150" text-anchor="middle" font-size="11" font-weight="bold">INI</text>

  <rect x="220" y="130" width="90" height="30" rx="5" fill="#fff9c4" stroke="#333" stroke-width="1"/>
  <text x="265" y="150" text-anchor="middle" font-size="11" font-weight="bold">TOML/YAML</text>

  <rect x="450" y="70" width="200" height="35" rx="5" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="550" y="93" text-anchor="middle" font-size="12" font-weight="bold">Is it tabular data?</text>

  <line x1="450" y1="87" x2="380" y2="140" stroke="#333" stroke-width="1.5"/>
  <text x="400" y="113" font-size="10" fill="#c62828">No</text>
  <line x1="650" y1="87" x2="660" y2="140" stroke="#333" stroke-width="1.5"/>
  <text x="668" y="113" font-size="10" fill="#2e7d32">Yes</text>

  <rect x="330" y="140" width="120" height="35" rx="5" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="390" y="163" text-anchor="middle" font-size="12" font-weight="bold">Web API?</text>

  <line x1="330" y1="157" x2="310" y2="200" stroke="#333" stroke-width="1.5"/>
  <text x="305" y="180" font-size="10" fill="#2e7d32">Yes</text>
  <line x1="450" y1="157" x2="460" y2="200" stroke="#333" stroke-width="1.5"/>
  <text x="468" y="180" font-size="10" fill="#c62828">No</text>

  <rect x="270" y="200" width="70" height="30" rx="5" fill="#fff9c4" stroke="#333" stroke-width="1"/>
  <text x="305" y="220" text-anchor="middle" font-size="11" font-weight="bold">JSON</text>

  <rect x="430" y="200" width="70" height="30" rx="5" fill="#fff9c4" stroke="#333" stroke-width="1"/>
  <text x="465" y="220" text-anchor="middle" font-size="11" font-weight="bold">XML</text>

  <rect x="600" y="140" width="130" height="35" rx="5" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="665" y="163" text-anchor="middle" font-size="12" font-weight="bold">Large dataset?</text>

  <line x1="600" y1="157" x2="560" y2="210" stroke="#333" stroke-width="1.5"/>
  <text x="565" y="185" font-size="10" fill="#c62828">No</text>
  <line x1="665" y1="175" x2="665" y2="210" stroke="#333" stroke-width="1.5"/>
  <text x="680" y="195" font-size="10" fill="#2e7d32">Yes</text>

  <rect x="520" y="210" width="70" height="30" rx="5" fill="#fff9c4" stroke="#333" stroke-width="1"/>
  <text x="555" y="230" text-anchor="middle" font-size="11" font-weight="bold">CSV</text>

  <rect x="610" y="210" width="120" height="35" rx="5" fill="#e8f5e9" stroke="#333" stroke-width="1.5"/>
  <text x="670" y="233" text-anchor="middle" font-size="12" font-weight="bold">Need queries?</text>

  <line x1="610" y1="227" x2="570" y2="270" stroke="#333" stroke-width="1.5"/>
  <text x="575" y="250" font-size="10" fill="#c62828">No</text>
  <line x1="730" y1="227" x2="730" y2="270" stroke="#333" stroke-width="1.5"/>
  <text x="745" y="250" font-size="10" fill="#2e7d32">Yes</text>

  <rect x="525" y="270" width="90" height="30" rx="5" fill="#fff9c4" stroke="#333" stroke-width="1"/>
  <text x="570" y="290" text-anchor="middle" font-size="11" font-weight="bold">Parquet</text>

  <rect x="690" y="270" width="80" height="30" rx="5" fill="#fff9c4" stroke="#333" stroke-width="1"/>
  <text x="730" y="290" text-anchor="middle" font-size="11" font-weight="bold">SQLite</text>
</svg>

---

## Streaming vs Batch Processing

| Format | Streaming | Batch |
|--------|-----------|-------|
| CSV | Line by line | Full file |
| JSON | Requires SAX-style parser | Full file |
| JSONL | Line by line | Full file |
| Parquet | Row group at a time | Full file |
| SQLite | Cursor-based queries | Full table |

JSON Lines and CSV are the best choices for streaming workloads.

---

## Schema Enforcement

| Format | Built-in Schema | External Schema |
|--------|----------------|-----------------|
| CSV | None | None |
| INI | None | None |
| JSON | None | JSON Schema |
| YAML | None | JSON Schema |
| TOML | None | None |
| XML | DTD/XSD | Schematron |
| Parquet | Embedded | None needed |
| SQLite | SQL DDL | None needed |
| Protobuf | `.proto` files | None needed |

---

## Compression and Data Formats

Text formats benefit greatly from compression:

```bash
# Compress CSV with gzip
gzip data.csv          # -> data.csv.gz

# Compress JSONL with zstd (modern, fast)
zstd data.jsonl        # -> data.jsonl.zst

# Parquet has built-in compression
# Snappy (default), Gzip, Zstd, LZ4
```

Parquet with Snappy compression is often smaller than gzipped CSV.

---

## Common Pitfalls

1. Using JSON for config files (no comments!)
1. Using CSV for hierarchical data (it cannot nest)
1. Using XML for new APIs (JSON is simpler)
1. Using YAML without quoting strings carefully
1. Loading huge CSV files entirely into memory
1. Using SQLite across a network share
1. Ignoring encoding — always use UTF-8

---

## Ecosystem and Tooling

| Format | CLI Tools | Python Library |
|--------|-----------|---------------|
| CSV | `csvtool`, `miller` | `csv`, `pandas` |
| INI | — | `configparser` |
| JSON | `jq` | `json`, `orjson` |
| YAML | `yq` | `pyyaml`, `ruamel.yaml` |
| TOML | `tomlq` | `tomllib` (3.11+) |
| JSONL | `jq` | `json` (line by line) |
| Parquet | `parquet-tools` | `pyarrow`, `pandas` |
| SQLite | `sqlite3` | `sqlite3` |
| XML | `xmlstarlet` | `lxml`, `xml.etree` |

---

## Real-World Format Combinations

In practice, formats are used together:

1. **Web app**: JSON (API) + TOML (config) + SQLite (local storage)
1. **Data pipeline**: CSV (ingest) -> JSONL (processing) -> Parquet (storage)
1. **DevOps**: YAML (config) + JSON (API) + INI (legacy config)
1. **Analytics**: Parquet (data lake) + SQLite (local analysis) + CSV (reports)

---

## Summary

- **CSV**: Simple tabular data, universal compatibility
- **INI**: Simple flat configuration
- **JSON**: Structured data interchange, web APIs
- **YAML**: Human-friendly configuration
- **TOML**: Unambiguous configuration
- **JSONL**: Streaming, logs, large datasets
- **Parquet**: Analytical workloads, data lakes
- **SQLite**: Local queryable storage
- **XML**: Legacy systems, document-oriented data
- Choose based on: audience, data shape, scale, and tooling needs
