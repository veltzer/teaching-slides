---
tags:
  - networking:rest
  - networking:http
level: beginner
category: networking
audience:
  - audiences:developers

---

# HTTP Fundamentals

---

## Request &amp; Response

![http_request](svg/courses/networking/restful-apis/02_http_fundamentals/http_request.svg)

---

## What This Chapter Covers

- HTTP request and response
- Methods
- Status codes
- Headers
- Bodies and content types
- HTTP versions

---

## HTTP Request Anatomy

- Method (GET, POST, ...)
- URL / path
- Headers (key-value)
- Optional body

---

## HTTP Response Anatomy

- Status code (200, 404, ...)
- Headers
- Optional body
- Same model as request

---

## Methods

- GET: read
- POST: create / generic action
- PUT: replace
- PATCH: partial update
- DELETE: remove
- HEAD, OPTIONS: meta

---

## Method Properties

- Safe: no side effects (GET, HEAD)
- Idempotent: same result on retry (GET, PUT, DELETE)
- POST: typically neither

---

## Status Code Classes

- 1xx: informational
- 2xx: success
- 3xx: redirection
- 4xx: client error
- 5xx: server error

---

## Common 2xx

- 200 OK
- 201 Created
- 202 Accepted
- 204 No Content

---

## Common 4xx

- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 409 Conflict
- 422 Unprocessable

---

## Common 5xx

- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable
- 504 Gateway Timeout

---

## Headers

- Metadata for request and response
- Auth: Authorization, Cookie
- Content: Content-Type, Content-Length
- Caching: Cache-Control, ETag
- CORS: Access-Control-*

---

## Content Types

- application/json: most common
- application/xml: legacy
- multipart/form-data: file uploads
- text/html: web pages

---

## HTTP / 1.1 vs 2 vs 3

- 1.1: text protocol, head-of-line blocking
- 2: binary, multiplexing
- 3: over QUIC / UDP, faster on lossy links
- API consumers usually unaware

---

## TLS

- HTTPS: HTTP over TLS
- Encryption + authentication of server
- Required for production
- Free certs via Let's Encrypt

---

## Common HTTP Mistakes

- Returning 200 with error in body
- Confusing 401 (auth) with 403 (perms)
- Caching POST responses
- Missing Content-Type header
- Logging sensitive headers (Authorization)

---

## HTTP Method Semantics

![http_methods](svg/courses/networking/restful-apis/02_http_fundamentals/http_methods.svg)
