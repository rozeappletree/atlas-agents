---
name: security-hardening
description: Harden an application or service against common attack vectors. Use when asked to improve security posture, secure an API, harden a server, or prepare for a security review.
license: MIT
---

## Overview

Security hardening is not about chasing perfect — it's about raising the cost of attack above the attacker's budget. Work systematically through the layers.

## Process

### Layer 1: Authentication and Authorization

1. Verify all endpoints require authentication. Check for unprotected routes using:
   ```bash
   grep -rn "route\|@app\.\|router\." src/ | grep -v "login\|health\|docs"
   ```
2. Check that authorization is enforced at the data layer, not just the route layer. A user who can reach `/orders` should only see *their* orders.
3. Confirm tokens expire. JWTs must have `exp` claims. Sessions must have server-side expiry.

### Layer 2: Input Validation

4. Every user-supplied value that touches a database must use parameterized queries. Grep for f-string SQL:
   ```bash
   grep -rn "f\"SELECT\|f'SELECT\|format.*SELECT" src/
   ```
5. Every file path from user input must be validated against an allowlist or a sandboxed directory. Check for `os.path.join(base, user_input)` without `os.path.abspath` + `startswith` guard.

### Layer 3: Secrets and Configuration

6. Scan for hardcoded secrets:
   ```bash
   grep -rn "password\s*=\s*[\"'][^\"']\|api_key\s*=\s*[\"'][^\"']" src/
   ```
7. Confirm all secrets come from environment variables or a secrets manager, not from config files committed to version control.
8. Check `.gitignore` includes `.env`, `*.key`, `*.pem`.

### Layer 4: Dependencies and Infrastructure

9. Run the `dependency-audit` skill to check for vulnerable packages.
10. Check HTTP security headers are set (for web services):
    - `Content-Security-Policy`
    - `X-Frame-Options: DENY`
    - `Strict-Transport-Security`
    - `X-Content-Type-Options: nosniff`

### Layer 5: Output

11. Write findings as a prioritized list: Critical → High → Medium → Low. For each finding: what it is, where it is (file:line), how to fix it.

## Rationalizations

| Excuse | Rebuttal |
|--------|----------|
| "This is an internal service, it doesn't need hardening" | Internal services are the primary target of lateral movement attacks after initial breach. |
| "We'll harden it before the public launch" | Security debt compounds. Fix it before it goes anywhere. |
| "The framework handles security" | Frameworks handle some things. You must handle the application-level concerns. |

## Verification

- [ ] All four layers were checked (not just the ones that seemed relevant)
- [ ] No hardcoded secrets found in source or git history
- [ ] Every critical and high finding has a specific remediation
- [ ] A finding was produced for each layer — even if it's "no issues found"
