---
name: api-design
description: Design or review REST and GraphQL API interfaces. Use when asked to design an API, review endpoint structure, define request/response schemas, or improve API ergonomics.
license: MIT
---

## Overview

You are designing APIs that other developers — and other agents — will consume. Clarity and predictability matter more than cleverness.

## Process

1. **Identify the domain objects.** List every noun the API needs to represent. Group them by relationship.
2. **Design the resource hierarchy.** Use plural nouns for collections: `/users`, `/users/{id}/orders`. Never use verbs in URLs — the HTTP method IS the verb.
3. **Define schemas.** Write request and response schemas as JSON examples. Every field must have:
   - A type
   - Whether it's required or optional
   - An example value
   - Validation constraints (min/max length, regex pattern, allowed values)
4. **Error contract.** Define a consistent error envelope:
   ```json
   {"error": {"code": "VALIDATION_FAILED", "message": "...", "details": [...]}}
   ```
   Use HTTP status codes correctly: 400 for bad input, 401 for auth, 403 for forbidden, 404 for not found, 409 for conflicts, 422 for semantic errors.
5. **Pagination.** All list endpoints must support cursor-based pagination by default. Offset pagination is acceptable only if explicitly requested.
6. **Versioning.** Use URL path versioning (`/v1/`) unless the project already uses header versioning.

## Rationalizations

| Excuse | Rebuttal |
|--------|----------|
| "We can add pagination later" | No. Adding pagination to an existing endpoint is a breaking change. Design it in from day one. |
| "Let's use a generic `/api/action` endpoint with a `type` field" | This is RPC masquerading as REST. Use proper resource URLs. |
| "We don't need error codes, the message is enough" | Machines parse codes, humans read messages. You need both. |

## Verification

- [ ] Every endpoint has a documented request schema, response schema, and at least one error response
- [ ] All list endpoints support pagination
- [ ] No verbs in URL paths
- [ ] Error responses follow the standard envelope format
