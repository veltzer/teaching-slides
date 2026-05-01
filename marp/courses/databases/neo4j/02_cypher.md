---
tags:
  - databases:neo4j
level: intermediate
category: databases
audience:
  - audiences:developers
  - audiences:dba

---
# Cypher

---
## What This Chapter Covers

- Match patterns
- Create and merge
- Where filtering
- Aggregations
- Procedures

---
## MATCH

- Find nodes and relationships
- Patterns match real graph
- No match means empty result
- Returns rows

---
## Patterns

- (a:Label) for node
- -[:TYPE]-> for relationship
- (a)-[:T]->(b) full pattern
- Variable length with *

---
## CREATE

- Create nodes and relationships
- Always succeeds
- May create duplicates
- Pair with MERGE for uniqueness

---
## MERGE

- Match or create
- Atomic per pattern
- Needs unique constraints to be safe
- Common for upserts

---
## SET

- Assign or update properties
- On match or always
- Map updates with += or =
- Use carefully on hot nodes

---
## DELETE And DETACH DELETE

- DELETE removes nodes only if no relationships
- DETACH DELETE removes node and edges
- Be explicit
- Easy to over-delete

---
## WHERE

- Filter rows
- Boolean expressions
- IN, =, <, >
- Pattern predicates supported

---
## RETURN

- Choose what to emit
- Aliases supported
- Aggregations like SQL
- ORDER BY and LIMIT

---
## Aggregations

- count, sum, avg, min, max
- Implicit grouping by non-aggregated columns
- collect for arrays
- Same gotchas as SQL

---
## WITH

- Pipe between query parts
- Like a subquery boundary
- Filter or aggregate then continue
- Required for multi-stage logic

---
## Variable Length Paths

- (a)-[*1..3]->(b)
- Bounded depth saves cost
- Unbounded is dangerous
- Use the shortest-path function where applicable

---
## Procedures

- CALL keyword
- Built-in for admin and analytics
- Custom in Java if needed
- Read-only vs write declared

---
## Common Cypher Mistakes

- MERGE without unique constraint
- Unbounded variable-length paths
- DETACH DELETE in scripts unintentionally
- WITH pipelines forgotten
- Cartesian patterns by accident
