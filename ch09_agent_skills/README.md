# Chapter 9: Declarative Agent Skills

Code examples for Chapter 9 of *Hands-On AI Agents*.

## Skill Library

12 production-grade skills covering the full engineering lifecycle:

| # | Skill | Trigger keywords |
|---|-------|-----------------|
| 1 | `code-review` | review code, audit PR, check for vulnerabilities, assess quality |
| 2 | `api-design` | design API, review endpoints, define schema, REST structure |
| 3 | `git-commit` | commit changes, prepare commit, stage files, push code |
| 4 | `database-migration` | update schema, run alembic, apply migrations, add column |
| 5 | `dependency-audit` | check dependencies, audit packages, find vulnerable libraries |
| 6 | `incident-response` | service is down, errors spiking, latency degraded, production issue |
| 7 | `test-generation` | write tests, add coverage, create unit tests, integration tests |
| 8 | `deploy-checklist` | deploy, ship, release, push to production, promote to staging |
| 9 | `documentation-writer` | document module, write README, generate API docs |
| 10 | `data-pipeline` | process dataset, build ETL, transform data, batch job |
| 11 | `security-hardening` | improve security, harden API, prepare for security review |
| 12 | `performance-profiling` | improve speed, reduce latency, find bottleneck, memory leak |

## Usage with the Skill Loader

```python
from skill_loader import discover_skills, build_catalog_prompt, activate_skill

catalog = discover_skills(["atlas-agents/ch09_agent_skills/skills"])
print(build_catalog_prompt(catalog))
```

## Skill Structure

Each skill follows the Agent Skills specification:
- `SKILL.md` — YAML frontmatter + process steps + rationalizations + verification checklist
- `scripts/` — (optional) bundled executable scripts
- `references/` — (optional) supplementary documentation

See `online/skill_loader.py` for the discovery and activation engine.
