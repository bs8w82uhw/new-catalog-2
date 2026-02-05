---
title: Documentation Governance
---

## Rules

1. All documentation changes go through Pull Requests.
2. At least one approval is required before merge.
3. CODEOWNERS review is required for documentation files.
4. `knowledge-registry.json` must be updated with every docs change.
5. High-risk automation docs must include policy and escalation sections.

## Document Status

-  `draft`: not approved for agents.
-  `active`: reviewed and approved.
-  `deprecated`: kept for migration/history only.

## Mandatory Metadata

-  `owner`
-  `status`
-  `agent_ready`
-  `risk_level`
-  `last_reviewed_at`
-  `next_review_at`