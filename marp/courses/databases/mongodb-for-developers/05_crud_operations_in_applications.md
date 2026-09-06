---
tags:
  - databases:mongodb
level: intermediate
category: databases
audience:
  - audiences:developers

---

# CRUD Operations in Applications

---

## What This Chapter Covers

- Insert, find, update, delete
- Operators
- Upserts
- Bulk operations
- Returning documents
- Errors

---

## CRUD at a Glance

![crud_methods](svg/courses/databases/mongodb-for-developers/05_crud_operations_in_applications/crud_methods.svg)

---

## CRUD Choosing The Right Call

![crud_decision](svg/courses/databases/mongodb-for-developers/05_crud_operations_in_applications/crud_decision.svg)

---

## Insert

```python
db.users.insert_one({"name": "Alice", "email": "a@b.com"})
db.users.insert_many([{"name": "Bob"}, {"name": "Carol"}])
```

- Auto-generated _id if not provided
- Returns the inserted IDs

---

## Find

```python
user = db.users.find_one({"email": "a@b.com"})
all = db.users.find({"status": "active"}).limit(10)
```

- Single result: `find_one`
- Cursor: `find` (iterate)

---

## Query Operators

- `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`
- `$in`, `$nin`
- `$exists`, `$type`
- `$or`, `$and`, `$not`, `$nor`
- `$regex` for pattern match

---

## Examples

```python
db.users.find({"age": {"$gte": 18}})
db.orders.find({"status": {"$in": ["pending", "shipping"]}})
db.users.find({"email": {"$regex": "^alice"}})
```

---

## Update Operators

- `$set`: set field
- `$unset`: remove field
- `$inc`: increment
- `$push`, `$pull`: array add / remove
- `$rename`: rename field

---

## Update Examples

```python
db.users.update_one({"_id": 1}, {"$set": {"status": "active"}})
db.users.update_one({"_id": 1}, {"$inc": {"login_count": 1}})
db.users.update_one({"_id": 1}, {"$push": {"tags": "vip"}})
```

---

## Upsert

```python
db.users.update_one(
    {"email": "a@b.com"},
    {"$set": {"name": "Alice"}},
    upsert=True
)
```

- Update if exists; insert if not
- Atomic

---

## Delete

```python
db.users.delete_one({"_id": 1})
db.orders.delete_many({"status": "cancelled"})
```

- One or many
- Returns deleted count

---

## findOneAndUpdate

```python
result = db.users.find_one_and_update(
    {"_id": 1},
    {"$inc": {"counter": 1}},
    return_document=ReturnDocument.AFTER
)
```

- Atomic: update + return
- Useful for counters, locks

---

## Bulk Operations

```python
db.users.bulk_write([
    InsertOne({"name": "A"}),
    UpdateOne({"name": "B"}, {"$set": {"active": True}}),
    DeleteOne({"name": "C"}),
])
```

- One round trip
- Massive speedup
- Error handling per op

---

## Bulk Write Strategy

![bulk_write_strategy](svg/courses/databases/mongodb-for-developers/05_crud_operations_in_applications/bulk_write_strategy.svg)

---

## Cursors

- `find()` returns a cursor
- Iterate; rewinds; close
- Driver handles batching
- Watch: huge result sets in memory

---

## Projection

```python
db.users.find({}, {"name": 1, "email": 1, "_id": 0})
```

- Return only specified fields
- Saves bandwidth
- Required for big documents

---

## Errors

- Duplicate key: 11000
- Validation: 121
- Network: handled by driver retries
- Most: catch, decide, retry or fail

---

## Common CRUD Mistakes

- Update without `$set` (replaces the whole document)
- Find without limit on huge collections
- No projection; pulling all fields
- Many small ops where bulk would do
- Ignoring duplicate key errors silently
