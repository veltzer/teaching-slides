---
tags:
  - databases:orm
level: beginner
category: databases
audience:
  - audiences:developers

---
# Object-Relational Mappers (ORMs)

---
## ORM Trade-offs

![orm_tradeoffs](svg/courses/databases/introduction-to-databases/09_object_relational_mappers/orm_tradeoffs.svg)

---
## What This Chapter Covers

- What an ORM is
- Pros and cons
- Popular ORMs
- Lazy loading
- N+1 problem
- When to drop to SQL

---
## What An ORM Is

- Maps DB rows to language objects
- Generates SQL from method calls
- Manages relationships
- Common in: Java (Hibernate), Python (SQLAlchemy, Django ORM), Ruby (ActiveRecord), JavaScript (Prisma, TypeORM)

---
## Pros

- Less boilerplate
- Type safety in some languages
- Schema migrations bundled
- Common patterns (active record, repository)
- Faster initial development

---
## Cons

- Hides SQL: hard to optimise
- N+1 problems
- Generated SQL sometimes inefficient
- Magic; learning curve
- Performance ceiling for complex queries

---
## Active Record Pattern

- Object knows how to save itself
- `user.save()`, `user.delete()`
- Convenient; couples model to persistence
- ActiveRecord (Rails), Django ORM

---
## Repository Pattern

- Separate object for persistence
- `userRepo.save(user)`
- Cleaner separation
- Java's JPA, .NET Entity Framework

---
## Lazy Loading

- Related objects loaded on access
- "user.orders" loads orders when accessed
- Convenient; can cause N+1
- Disable when not needed

---
## N+1 Problem

- Fetch list of N items; for each: fetch related (1 query)
- N+1 queries total
- Should be 1 query (JOIN or batch)
- ORMs hide this; you must catch it

---
## Eager Loading

- Pre-fetch related objects
- "User.includes(:orders).all"
- One query for users + one for all orders (or JOIN)
- The fix for N+1

---
## Query Builder

- Programmatic SQL construction
- Less abstract than full ORM
- More predictable performance
- Knex, jOOQ, SqlAlchemy core

---
## Raw SQL Fallback

- Even with ORM: drop to raw SQL when needed
- Complex queries don't fit ORM patterns
- Document; don't make every query a ticket of complaints

---
## Migrations

- Most ORMs include migration tools
- Generate skeleton from model changes
- Apply / rollback
- Versioned in source control

---
## Validation

- Many ORMs validate before saving
- "Email must be unique"
- App-side enforcement
- Combine with DB constraints

---
## Performance Tips

- Profile generated SQL
- Use eager loading
- Add indexes for ORM-generated queries
- Drop to raw SQL for analytics

---
## Common ORM Mistakes

- N+1 queries (the classic)
- Loading entire tables into memory
- Trusting the ORM's defaults for performance
- Only using the ORM (no raw SQL ever)
- Not understanding the SQL it generates
