---
name: dependency-audit
description: Audit project dependencies for vulnerabilities, license issues, and bloat. Use when asked to check dependencies, audit packages, find vulnerable libraries, or reduce bundle size.
license: MIT
compatibility: Requires pip or npm/yarn/pnpm
---

## Process

1. **Identify the package manager.** Look for:
   - `requirements.txt` / `pyproject.toml` / `Pipfile` → Python (pip/uv)
   - `package.json` → Node.js (npm/yarn/pnpm)
   - `go.mod` → Go
   - `Cargo.toml` → Rust

2. **Run vulnerability scan.**
   - Python: `pip audit` or `uvx pip-audit`
   - Node.js: `npm audit` or `npx better-npm-audit audit`
   - Go: `govulncheck ./...`

3. **Check for outdated packages.**
   - Python: `pip list --outdated`
   - Node.js: `npm outdated`

4. **License audit.** Check that no dependency uses a copyleft license (GPL, AGPL) in a proprietary project:
   - Python: `uvx pip-licenses --order=license`
   - Node.js: `npx license-checker --summary`

5. **Identify unused dependencies.**
   - Python: Check each import with `grep -r "import <package>" src/`
   - Node.js: `npx depcheck`

6. **Write the report** as a markdown table with columns: Package, Current Version, Latest Version, Vulnerabilities, License, Status (keep/update/remove).

## Rationalizations

| Excuse | Rebuttal |
|--------|----------|
| "We'll update dependencies later" | Known vulnerabilities are actively exploited. Flag them now. |
| "It's a dev dependency, it doesn't matter" | Dev dependencies run in CI and on developer machines — they are attack surface. |
| "Removing unused deps might break something" | If nothing imports it, nothing uses it. Remove it. |

## Verification

- [ ] Vulnerability scan was executed (not estimated)
- [ ] Every critical/high vulnerability has a recommended action (update version or replace package)
- [ ] License compatibility was checked against the project's license
