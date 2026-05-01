---
tags:
  - databases:design
  - databases:er
level: intermediate
category: databases
audience:
  - audiences:developers

---
# Entity-Relationship Modeling

---
## What This Chapter Covers

- Entities, attributes, relationships
- Cardinality
- ER diagrams
- Mapping to tables
- Examples

---
## Entities

- Real-world things you track
- "Customer", "Order", "Product"
- Become tables (usually)

---
## Attributes

- Properties of entities
- "Customer has name, email"
- Become columns

---
## Relationships

- Connections between entities
- "Customer places Orders"
- Captured by foreign keys

---
## Cardinality

- 1:1: each row in A relates to at most one in B
- 1:N: A has many B; B has one A
- M:N: each A relates to many B; each B to many A
- Drives the schema

---
## Mapping 1:N

- The "many" side has a foreign key
- Order.customer_id references Customer.id
- One column on Order

---
## Mapping M:N

- Add a junction table
- StudentCourse(student_id, course_id)
- Composite primary key

---
## Mapping 1:1

- Foreign key on either side, marked unique
- Or: same primary key as the related entity
- Less common; sometimes inheritance

---
## Identifying vs Non-Identifying

- Identifying: child can't exist without parent (composite key)
- Non-identifying: child exists independently
- Most are non-identifying

---
## ER Diagrams

- Boxes: entities
- Lines: relationships
- Crow's foot or UML
- Tools: dbdiagram.io, draw.io

---
## A Worked Example

- Order, Customer, Product, OrderLine
- Customer 1:N Order
- Order 1:N OrderLine
- OrderLine M:1 Product

---
## Common Mistakes

- Confusing 1:N with M:N
- Not identifying optionality (nullable FK)
- Missing the junction table for M:N
- Over-normalising at the ER level
