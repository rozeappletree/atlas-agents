---
name: documentation-writer
description: Write or update technical documentation for code, APIs, or systems. Use when asked to document a module, write a README, generate API docs, or update existing documentation.
license: MIT
---

## Overview

You write documentation that developers will actually read. That means concrete examples over abstract descriptions, and answering the question "how do I use this?" before "what is this?".

## Process

1. **Read the source first.** Load the actual code before writing a single word. Documentation that doesn't match the implementation is worse than no documentation.

2. **Identify the documentation type:**
   - **README** — for projects and repositories
   - **Module/API docs** — for functions, classes, endpoints
   - **Architecture docs** — for system design and component relationships
   - **Runbook** — for operational procedures

3. **For READMEs**, follow this structure:
   ```
   # Project Name
   One sentence: what it does and who it's for.

   ## Quick Start
   The fewest possible steps to get something working.
   Code first. Explanation second.

   ## Installation
   ## Usage
   ## Configuration
   ## API Reference (if applicable)
   ## Contributing
   ## License
   ```

4. **For function/class docs**, write docstrings that include:
   - What the function does (one line)
   - Parameters: name, type, description, whether optional
   - Return value: type and description
   - Exceptions it may raise
   - One usage example

5. **Write the example first.** If you cannot write a concrete 5-line example of how to use something, you don't understand it well enough to document it. Go back to step 1.

6. **Verify accuracy.** Read your documentation and check every claim against the code. If you wrote "`returns a list of strings`" and the code returns a dict, fix it.

## Rationalizations

| Excuse | Rebuttal |
|--------|----------|
| "The code is self-documenting" | No code is self-documenting to someone seeing it for the first time. Write the docs. |
| "I'll add examples later" | Documentation without examples is theory. Write the example now. |
| "The function signature explains it" | Type hints say what the types are, not what the function does or why. |

## Verification

- [ ] Every documented function has at least one usage example
- [ ] Parameter types and return types are correct (verified against the source)
- [ ] Quick Start section in README can be followed by a new developer with no prior context
- [ ] No documentation contradicts the actual implementation
