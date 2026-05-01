---
tags:
  - databases:neo4j
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Introduction to Neo4j

---
## What This Chapter Covers

- What a graph database is
- When graph wins
- Neo4j basics
- Core concepts
- Course outline

---
## What A Graph Database Is

- Nodes for entities
- Relationships between them
- Both have properties
- Queries traverse edges

---
## Why Graph

- Relationships are first-class
- Traversal is cheap
- Schema is flexible
- Patterns easier to express

---
## When Graph Wins

- Social networks
- Recommendations
- Fraud detection
- Knowledge graphs
- Hierarchies and dependencies

---
## When Graph Loses

- Aggregations over rows
- Wide analytical scans
- Strongly tabular data
- Pure key-value lookup

---
## Property Graph Model

- Nodes have labels
- Relationships have types
- Both have key-value properties
- No fixed schema

---
## Property Graph Visualized

![property_graph](svg/courses/databases/neo4j/01_introduction/property_graph.svg)

---
## Cypher

- Declarative query language
- Pattern matching syntax
- Reads like ASCII art
- Standard across multiple graph DBs

---
## Sample Pattern

- (a:Person)-[:FRIEND]->(b:Person)
- Match nodes and relationships
- Filter by labels and properties
- Return what you want

---
## Storage

- Native graph storage
- Index-free adjacency
- Pointers between nodes
- Constant time traversal

---
## ACID

- Real transactions
- Consistent across nodes and edges
- Important for financial graphs
- Differentiator from many graph stores

---
## Versions

- Community: free
- Enterprise: clustering, security, audit
- Aura: hosted
- Pick by needs

---
## Hardware Profile

- RAM matters most
- SSD for cold paths
- Cores help concurrent queries
- Heap and page cache tuned together

---
## Course Outline

- Cypher basics
- Modeling
- Performance
- Operations
- Graph algorithms

---
## Common Beginner Mistakes

- Modeling like SQL
- Property explosion
- No indexes on lookup keys
- Long Cypher in app code
- Ignoring transaction size
