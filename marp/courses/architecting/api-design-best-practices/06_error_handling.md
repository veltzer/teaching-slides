---
tags:
  - concepts:api
  - concepts:best-practices
level: intermediate
category: architecture
audience:
  - audiences:developers

---
# Error Handling

---
## Structured Errors

![error_response](svg/courses/architecting/api-design-best-practices/06_error_handling/error_response.svg)

---
## Why Error Design Matters

- Errors are part of the API contract
- A consumer's error-handling code is as much code as their happy path
- Bad error responses make integrations fragile
- Good error responses make integrations debuggable

---
## What an Error Response Should Have

- An HTTP status code that matches the failure category
- A machine-readable error code
- A human-readable message
- Context: what was wrong with the request
- Optional: a link to documentation, a request id for support

---
## Error Response Anatomy

![error_envelope](svg/courses/architecting/api-design-best-practices/06_error_handling/error_envelope.svg)

---
## RFC 7807: Problem Details

- Standard format for error responses
- Content-Type: `application/problem+json`
- Standard fields: type, title, status, detail, instance
- Extensible with custom fields

---
## RFC 7807 Example

```json
{
  "type": "https://example.com/errors/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 422,
  "detail": "Your account has $50, but the order requires $95.",
  "instance": "/transactions/t-789",
  "balance": 50,
  "required": 95
}
```

---
## Use Status Codes Correctly

- 400 Bad Request: malformed request
- 401 Unauthorized: not authenticated
- 403 Forbidden: authenticated but not allowed
- 404 Not Found: resource doesn't exist (or shouldn't be visible)
- 409 Conflict: state conflict (concurrent edit, duplicate)
- 422 Unprocessable: well-formed but semantically wrong
- 429 Too Many Requests: rate limited

---
## Error Codes vs Messages

- HTTP status: broad category
- Application error code: specific machine-readable identifier
- Message: human-readable explanation

```json
{
  "code": "ORDER_ALREADY_PLACED",
  "message": "This order has already been placed and cannot be modified.",
  "status": 409
}
```

- Status for category, code for specifics, message for humans

---
## Validation Errors

- One field has multiple problems → return all at once, not one at a time
- Each entry: which field, what the problem is

```json
{
  "code": "VALIDATION_FAILED",
  "errors": [
    {"field": "email", "code": "INVALID_FORMAT", "message": "..."},
    {"field": "age", "code": "OUT_OF_RANGE", "message": "must be 18+"}
  ]
}
```

---
## Error Catalogs

- Maintain a list of all error codes the API can produce
- Each entry: code, when it's used, suggested action
- Documentation alongside the API spec
- Helps consumers handle errors systematically

---
## Consistent Error Format

- Every error response has the same shape
- Don't return `{"error": "..."}` from one endpoint and `{"message": "..."}` from another
- A single error type (or a small set) across the whole API
- Consumers can write a single error handler

---
## Don't Leak Internals

- Stack traces in production responses → security risk
- "Database connection failed: postgres://user:password@host" → very bad
- Sanitize before responding
- Log details server-side; return a generic-but-helpful message

---
## Generic Server Errors

- 500 Internal Server Error: something we didn't expect
- The response should be useful to the caller without exposing internals
- Include a request id so support can find logs

```json
{
  "code": "INTERNAL_ERROR",
  "message": "Something went wrong. Please try again or contact support.",
  "request_id": "req_abc123"
}
```

---
## Localization

- Error messages may need to be localized
- Two strategies:
    - Client-side: use the error code to pick a localized message
    - Server-side: use Accept-Language header
- Client-side gives the consumer control; server-side is simpler

---
## Anti-Patterns

- 200 OK with `{"success": false}` — defeats HTTP semantics
- Generic messages: "An error occurred"
- Returning HTML in JSON APIs (the 500 page from the framework)
- Inconsistent shapes per endpoint
- Codes that are just human strings: `"User Not Found"` vs `"USER_NOT_FOUND"`

---
## Idempotency and Errors

- A retried operation should produce the same result on success
- For errors, the retry might succeed (transient) or fail again (permanent)
- The error response should indicate which: status 5xx (retry) vs 4xx (don't)
- We cover idempotency in chapter 7

---
## Summary

- Errors are part of the API contract — design them
- Use the right HTTP status code
- Add a machine-readable error code and a human message
- Consistent shape across the whole API
- RFC 7807 is a good starting point
