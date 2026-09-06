---
tags:
  - networking:rest
level: beginner
category: networking
audience:
  - audiences:developers

---

# REST Principles

---

## What This Chapter Covers

- Origin of REST
- Constraints
- Resources
- Representations
- HATEOAS
- Pragmatic REST

---

## Six Constraints

![rest_constraints](svg/courses/networking/restful-apis/03_rest_principles/rest_constraints.svg)

---

## Uniform Interface in Detail

![uniform_interface](svg/courses/networking/restful-apis/03_rest_principles/uniform_interface.svg)

---

## Origin

- Roy Fielding, 2000 dissertation
- Style, not a protocol
- Generalises web architecture

---

## Constraints

- Client-server
- Stateless
- Cacheable
- Layered system
- Uniform interface
- Code on demand (optional)

---

## Stateless

- Each request: complete information
- Server doesn't store client context between requests
- Scales horizontally
- Auth: send credentials each time

---

## Cacheable

- Responses indicate cacheability
- HTTP caching headers
- Reduces load, improves latency
- GET: cacheable; POST: usually not

---

## Uniform Interface

- Same conventions across the API
- Resources, methods, representations
- Predictable for consumers
- The hard-to-define one

---

## Resources

- Nouns: users, orders, products
- Identified by URLs
- Manipulated via HTTP methods
- The core REST abstraction

---

## Representations

- A resource has multiple representations
- JSON, XML, HTML
- Negotiated via Accept header
- Server sends the format the client wants

---

## HATEOAS

- Hypermedia as the engine of application state
- Responses include links to next actions
- Client navigates by following links
- Theoretical purity; rarely fully done

---

## Richardson Maturity Model

- Level 0: tunneling RPC over HTTP
- Level 1: resources
- Level 2: HTTP verbs and status codes
- Level 3: hypermedia controls

---

## Pragmatic REST

- Most "REST" is level 2
- That's fine
- Consistency matters more than purity
- Don't argue about HATEOAS in code review

---

## REST vs RPC

- REST: resources, manipulate state
- RPC: call remote functions
- Both work; mental model differs
- REST aligns with HTTP semantics

---

## Common REST Mistakes

- Verbs in URLs (/getUser instead of /users/123)
- Returning 200 for errors
- Stateful sessions
- Inconsistent resource naming
- Mixing REST and RPC styles within one API
