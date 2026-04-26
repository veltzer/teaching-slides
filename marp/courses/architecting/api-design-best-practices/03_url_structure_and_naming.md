---
tags:
  - concepts:api
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# URL Structure and Naming

---
## URL as User Interface

- URLs are read by developers, not just machines
- A clear URL is documentation
- A confusing URL is a permanent burden — changing it breaks consumers
- Spend effort getting URLs right; they outlast almost everything else

---
## Resource Naming

- Use nouns, not verbs: `/orders`, not `/getOrders`
- Use plurals for collections: `/users`, not `/user`
- Use lowercase: `/customer-orders`, not `/customerOrders`
- Use hyphens, not underscores: `/customer-orders`, not `/customer_orders`
- Be consistent across the whole API

---
## Hierarchical Resources

- Express ownership and containment with nesting
- `/orders/42/items` = items of order 42
- `/customers/c1/orders` = orders of customer c1
- Deep nesting (>2 levels) gets unreadable; flatten when it does

---
## When to Nest

- Nest when the child resource only makes sense in the parent's context
- An order line item only exists within an order — nest
- A user's address might also stand alone — keep it as `/addresses/N` and reference

---
## When Not to Nest

- "User has many orders, order has many items" → don't write `/users/42/orders/123/items/9`
- After 2 levels, switch to flat with cross-references
- `/items/9` with `order_id` field beats deep nesting

---
## Collection vs Singleton Resources

- `/orders` is a collection — multiple orders
- `/orders/42` is a singleton — one order
- `/users/me` is a special singleton — the current user
- Use `/me` or `/current` for "the actor making the request"

---
## Path vs Query Parameters

- **Path**: identifies a resource — `/users/42`
- **Query**: filters, sorts, paginates — `/users?role=admin&limit=20`
- Path = which resource; query = how to view it

---
## Path Parameter Examples

- `/users/{user_id}` — specific user
- `/orders/{order_id}/items/{item_id}` — specific line item
- The path identifies; nothing more

---
## Query Parameter Examples

- `?status=pending` — filter
- `?sort=created_at&order=desc` — sort
- `?limit=20&cursor=abc` — paginate
- `?fields=id,total` — sparse fieldsets

---
## Action Endpoints

- Sometimes the operation isn't a CRUD verb
- "Cancel this order", "send a verification email"
- Two patterns:
    - Sub-resource: `POST /orders/42/cancel`
    - Action endpoint: `POST /orders/42/actions/cancel`
- Either is fine; pick one and apply consistently

---
## Naming Patterns to Avoid

- `/api/v1/getUserOrdersByCustomerId` — verb soup
- `/data/orders` — what's "data"?
- `/orders.json` — file extensions in URLs (use Accept header)
- Inconsistent plurals: `/orders` and `/customer`

---
## Pluralization

- Almost everything should be plural: `/orders`, `/users`, `/products`
- Even singletons: `/users/me` not `/user/me`
- Exception: when the resource is genuinely singular: `/account/settings`
- Pick a rule, document it, follow it

---
## Trailing Slashes

- Pick a rule: with or without trailing slash
- Redirect the other to your canonical form
- Consistency reduces 404s from copy-pasted URLs

---
## Casing Recap

- URLs: lowercase, hyphen-separated
- Query parameter names: lowercase, snake_case or hyphen-case
- JSON field names: snake_case OR camelCase (just be consistent)
- Header names: case-insensitive, but conventionally `Pascal-Kebab-Case`

---
## A Concrete Style Guide Excerpt

- Plural nouns for collections
- Lowercase, hyphen-separated paths
- snake_case JSON field names
- ISO 8601 dates with timezone (`2026-01-15T14:23:00Z`)
- UUIDs for new resource IDs
- Cursor-based pagination

---
## Summary

- URLs are part of the user interface
- Plural nouns, lowercase, hyphen-separated
- Path = identity; query = view
- Stop nesting at 2 levels
- Pick conventions and apply them everywhere
