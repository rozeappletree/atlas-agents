---
name: deploy-checklist
description: Execute a structured deployment to staging or production. Use when asked to deploy, ship, release, push to production, or promote to staging.
license: MIT
compatibility: Requires git and access to the deployment target
allowed-tools: Bash(git:*) Bash(docker:*) Bash(kubectl:*)
---

## Clarification Gates

You must have unambiguous answers to these before touching anything:

- **Target:** staging or production? (Never assume. Never infer from branch name.)
- **Deploying what:** which service, which version/tag/commit SHA?
- **Rollback plan:** does one exist, and do you have access to execute it?

If the user says "deploy the thing" without specifying the environment, that is not sufficient information. Ask.

> **Model Proposes, Code Disposes:** You propose the deploy sequence. The CI/CD system or platform CLI executes it. You do not write deployment commands from memory — you use exactly the command documented in the project's deploy runbook or Makefile.

### Pre-deployment

1. **Confirm the target environment.** Ask if not specified: staging or production? Never assume production.
2. **Check the branch.** Verify you are on the correct branch:
   ```bash
   git branch --show-current
   ```
3. **Check for uncommitted changes:**
   ```bash
   git status --porcelain
   ```
   If there are uncommitted changes, STOP. Commit or stash them first.
4. **Run the test suite.** Execute the project's full test command. If any test fails, STOP. Do not deploy with failing tests.
5. **Check the changelog/diff.** Run `git log --oneline main..HEAD` to see what will be deployed. Present this to the user.

### Deployment

6. **Execute the deploy command.** Use the project's existing deployment mechanism:
   - Docker: `docker build && docker push`
   - Kubernetes: `kubectl apply -f`
   - Platform-specific: `fly deploy`, `vercel --prod`, `gcloud run deploy`
   Use exactly the command documented in the project. Do not invent deployment commands.

7. **Wait for deployment to complete.** Do not proceed until the deployment tool confirms success.

### Post-deployment

8. **Smoke test.** Hit the health endpoint or run a basic functional test:
   ```bash
   curl -s https://<deployed-url>/health | jq .
   ```
9. **Monitor for 2 minutes.** Check error rates and latency. If either spikes, recommend an immediate rollback.

## Rationalizations

| Excuse | Rebuttal |
|--------|----------|
| "Tests are slow, I'll skip them" | Deploying untested code is how you get paged at 3 AM. Run the tests. |
| "It works on my machine" | That is not evidence. The test suite is evidence. |
| "I'll just deploy and fix issues as they come" | You have no rollback plan if you don't know what changed. Check the diff first. |

## Verification

- [ ] Target environment was explicitly confirmed (not assumed)
- [ ] All tests passed before deployment
- [ ] Deployment tool reported success
- [ ] Health check returned 200 after deployment
- [ ] No error spike observed in the first 2 minutes
