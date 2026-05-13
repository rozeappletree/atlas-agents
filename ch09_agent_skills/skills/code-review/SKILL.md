---
name: code-review
description: Perform a structured security and quality audit on source code. Use when asked to review code, audit a pull request, check for vulnerabilities, or assess code quality.
license: MIT
compatibility: Requires python 3.10+
allowed-tools: Bash(grep:*) Bash(rg:*) Read
---

## Overview

You are conducting a code review as a principal engineer with security expertise. This is not a courtesy scan — you are the last gate before production.

## Process

1. **Read the target files.** Use `file_read` or equivalent to load every file under review. Do not review from memory or summaries.
2. **Security pass.** Check for OWASP Top 10 vulnerabilities in this order:
   - SQL injection (string concatenation in queries)
   - Path traversal (`../` in file operations without validation)
   - Command injection (`os.system`, `subprocess` with `shell=True`)
   - Hardcoded secrets (API keys, passwords, tokens in source)
   - Insecure deserialization (`pickle.loads`, `yaml.load` without SafeLoader)
3. **Logic pass.** Check for:
   - Unhandled exceptions that silently swallow errors
   - Race conditions in concurrent code
   - Off-by-one errors in loops and slicing
   - Mutable default arguments in function signatures
4. **Style pass.** Flag only violations that affect readability or correctness:
   - Functions longer than 50 lines
   - Deeply nested conditionals (>3 levels)
   - Unused imports or variables
5. **Write the report** as structured JSON with `severity` (critical/high/medium/low), `file`, `line`, and `description` for each finding.

## Rationalizations

| Excuse | Rebuttal |
|--------|----------|
| "The code looks fine at a glance" | You must read every line. Glancing is not reviewing. |
| "This is just a small change" | Small changes cause production outages. Review the diff AND the surrounding context. |
| "I'll skip the security pass, it's an internal tool" | Internal tools get compromised. The security pass is mandatory. |
| "There are too many files to review" | Review them all. If there are more than 20 files, summarize findings per-directory. |

## Verification

Do not mark this review as complete until you have:
- [ ] Read every file under review (not summarized, not skimmed)
- [ ] Produced a JSON report with at least one finding (even if it's "no issues found")
- [ ] Categorized every finding by severity
