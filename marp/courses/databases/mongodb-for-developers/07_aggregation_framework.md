---
tags:
  - databases:mongodb
  - databases:aggregation
level: intermediate
category: databases
audience:
  - audiences:developers

---

# Aggregation Framework

---

## What This Chapter Covers

- The pipeline model
- Common stages: $match, $group, $project
- Lookups (joins)
- Window-like functions
- Optimisation

---

## The Pipeline

```javascript
db.orders.aggregate([
    { $match: { status: "complete" } },
    { $group: { _id: "$customer_id", total: { $sum: "$amount" } } },
    { $sort: { total: -1 } },
    { $limit: 10 }
])
```

- Stages, processed in order
- Each stage's output is next stage's input

---

## Pipeline Visualized

![pipeline_stages](svg/courses/databases/mongodb-for-developers/07_aggregation_framework/pipeline_stages.svg)

---

## Pipeline Thinking

![pipeline_thinking](svg/courses/databases/mongodb-for-developers/07_aggregation_framework/pipeline_thinking.svg)

---

## $match

- Like find()
- Place early to reduce data
- Uses indexes (when first stage)

---

## $project

- Reshape documents
- Add / remove / compute fields
- `{ $project: { name: 1, year: { $year: "$created_at" } } }`

---

## $group

```javascript
{ $group: {
    _id: "$category",
    count: { $sum: 1 },
    avg_price: { $avg: "$price" },
    max: { $max: "$price" }
}}
```

- Like SQL GROUP BY
- _id is the group key
- Many accumulators

---

## $lookup (Join)

```javascript
{ $lookup: {
    from: "users",
    localField: "user_id",
    foreignField: "_id",
    as: "user"
}}
```

- Join with another collection
- Result: array under `as`
- Use sparingly (more expensive than embedding)

---

## $unwind

- Flatten an array
- One document per array element
- Common after $lookup
- Or for "explode tags" workflows

---

## $sort, $limit, $skip

- Like find cursor methods but in pipeline
- Order matters; sort before limit
- Limit early to reduce work

---

## $facet

```javascript
{ $facet: {
    counts: [ { $count: "total" } ],
    by_status: [ { $group: { _id: "$status", n: { $sum: 1 } } } ]
}}
```

- Multiple pipelines on the same input
- One pass through data
- Useful for: dashboards

---

## $setWindowFields

- Window-function-like
- Running totals, rankings
- MongoDB 5+
- Postgres-style power

---

## Aggregation Operators

- Math: $add, $subtract, $multiply
- String: $concat, $toUpper, $substr
- Date: $year, $month, $dayOfWeek
- Array: $arrayElemAt, $size
- Many; check docs

---

## Pipeline Optimisation

- $match before $group (filter first)
- $project to drop unnecessary fields
- Indexes on $match fields
- $limit early
- The planner reorders some; you should still write efficiently

---

## Aggregation vs Application Code

- Heavy aggregations: faster in DB
- Light: app-side simpler
- Trade-off: DB load vs network bandwidth
- For dashboards: usually DB

---

## Performance

- `explain()` works on pipelines
- Watch: stages without index support
- Memory limit: 100MB per stage (configurable)
- $allowDiskUse for big aggregations

---

## Common Aggregation Mistakes

- $match late in pipeline (no index use)
- $project with no benefit
- $lookup on huge unrelated collections
- Memory limit hit; no allowDiskUse
- Aggregations done in app when DB would be faster
