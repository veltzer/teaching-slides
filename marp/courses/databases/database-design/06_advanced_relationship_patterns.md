---
tags:
  - databases:design
  - databases:relationships
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Advanced Relationship Patterns

---
## What This Chapter Covers

- Self-referencing relationships
- Polymorphic associations
- Hierarchies
- Many-to-many with metadata
- Soft deletes
- Audit trails

---
## Self-Referencing

- Table references itself
- Employee.manager_id &#8594; Employee.id
- Org charts, comment threads, parent-child

---
## Tree Structures

- Parent ID per row
- Recursive CTEs to query
- Materialised paths: store full path
- Nested sets: numeric encoding
- Pick by query needs

---
## Polymorphic Associations

- "Comment can be on Post OR Photo OR Video"
- Two columns: commentable_type, commentable_id
- Trade-off: no real foreign keys
- Often a smell; consider per-target tables

---
## Better Polymorphism

- Separate join tables: comment_post, comment_photo
- Real foreign keys
- More tables; more joins
- Better integrity

---
## Inheritance Mapping Patterns

![inheritance_patterns](svg/courses/databases/database-design/06_advanced_relationship_patterns/inheritance_patterns.svg)

---
## M:N With Metadata

- Junction table has its own columns
- enrollment(student_id, course_id, grade, enrolled_at)
- Now it's a first-class entity, not just a join

---
## Beyond Plain Junctions

![junction_extras](svg/courses/databases/database-design/06_advanced_relationship_patterns/junction_extras.svg)

---
## Soft Deletes

- deleted_at column instead of DELETE
- WHERE deleted_at IS NULL on every query
- Recoverable
- Adds complexity; not always worth it

---
## Audit Trails

- Track who changed what, when
- Audit table: row_id, table, action, who, when, before, after
- Or: temporal tables (Postgres, SQL Server)

---
## Versioning

- Multiple versions of a row
- version_id, valid_from, valid_to
- Bitemporal: as-of time + valid time
- Complex; use only when required

---
## Hierarchies (Adjacency List)

- parent_id per row
- Simple, recursive queries
- Slow for deep trees

---
## Hierarchies (Closure Table)

- Separate table: ancestor_id, descendant_id, depth
- All ancestor relationships explicit
- Fast queries; expensive updates
- Useful for read-heavy hierarchies

---
## Common Pattern Mistakes

- Polymorphic associations without need
- Soft deletes "just in case"
- Self-referencing tables without recursive query support
- M:N as a junction table when it's actually a domain entity
- Over-engineering audit when simple version columns would do
