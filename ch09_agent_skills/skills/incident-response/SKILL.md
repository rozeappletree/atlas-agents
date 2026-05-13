---
name: incident-response
description: Diagnose and respond to production incidents. Use when a service is down, errors are spiking, latency is degraded, or the user reports a production issue.
license: MIT
---

## Overview

You are an on-call engineer triaging a live incident. Speed matters, but reckless changes make things worse. Follow the process.

## Process

1. **Assess severity.** Ask or determine:
   - Is the service fully down, partially degraded, or experiencing elevated errors?
   - How many users are affected?
   - Is data being lost or corrupted?

2. **Gather signals.** Before forming any hypothesis, collect:
   - Recent deployments (`git log --oneline -10`)
   - Error logs (last 100 lines of the relevant log file)
   - Resource utilization (CPU, memory, disk, connections)
   - Recent configuration changes

3. **Form ONE hypothesis.** Based on the signals, state your best guess in one sentence. Do not enumerate multiple possibilities — pick the most likely one.

4. **Test the hypothesis.** Run exactly one diagnostic command or query that would confirm or refute your hypothesis. Read the output.

5. **If confirmed:** Propose a fix. If the fix involves restarting a service or rolling back a deploy, state the exact command. Do not improvise commands.

6. **If refuted:** Return to step 2 with the new information. Form a new hypothesis.

7. **Post-mortem.** After the incident is resolved, write a brief post-mortem with:
   - Timeline (when it started, when it was detected, when it was resolved)
   - Root cause (one sentence)
   - Fix applied
   - Follow-up actions to prevent recurrence

## Rationalizations

| Excuse | Rebuttal |
|--------|----------|
| "Let me just restart the service first" | Restarting without diagnosis destroys evidence. Gather signals first. |
| "I have three theories" | Pick one. Test it. If wrong, pick another. Parallel investigation wastes time. |
| "It's probably fine now" | Confirm with metrics. "Probably" is not a resolution status. |
| "We can skip the post-mortem, it was minor" | Minor incidents reveal systemic issues. Write the post-mortem. |

## Verification

- [ ] Signals were gathered before any remediation was attempted
- [ ] The root cause was identified (not assumed)
- [ ] Service health was confirmed after the fix (not assumed)
- [ ] A post-mortem was written
