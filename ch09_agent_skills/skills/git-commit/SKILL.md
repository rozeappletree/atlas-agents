---
name: git-commit
description: Create well-structured git commits with conventional commit messages. Use when asked to commit changes, prepare a commit, or stage and push code.
license: MIT
compatibility: Requires git
allowed-tools: Bash(git:*)
---

## Process

1. **Run `git status`** to see all changed files. Read the output carefully.
2. **Run `git diff --stat`** to understand the scope of the change.
3. **Group related changes.** If the diff contains unrelated changes (e.g., a bug fix AND a new feature), create separate commits. Do not bundle unrelated work.
4. **Stage files intentionally.** Use `git add <specific-files>`, never `git add .` unless every changed file belongs in the same logical commit.
5. **Write the commit message** using Conventional Commits format:
   ```
   <type>(<scope>): <description>

   <body — explain WHY, not WHAT>

   <footer — references, breaking changes>
   ```
   Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`
6. **Verify before committing.** Run `git diff --cached` to review exactly what will be committed. Read the staged diff.
7. **Commit.** Run `git commit -m "..."` with the message.

## Rationalizations

| Excuse | Rebuttal |
|--------|----------|
| "I'll just use `git add .` to save time" | Staging everything blindly leads to committing debug files, env vars, and unrelated changes. Stage intentionally. |
| "The message 'fix stuff' is fine for now" | Every commit message is permanent history. Write it properly the first time. |
| "I'll squash these later" | You won't. Write clean commits now. |

## Verification

- [ ] `git diff --cached` output was reviewed before committing
- [ ] Commit message follows Conventional Commits format
- [ ] No unrelated changes were bundled into a single commit
- [ ] No `.env`, `__pycache__`, or build artifacts were staged
