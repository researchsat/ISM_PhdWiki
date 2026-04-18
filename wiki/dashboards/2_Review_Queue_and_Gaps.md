---
title: "Review Queue and Gaps"
type: dashboard
---

# Action Required: Review Queue

The following papers have been ingested as a foundational draft but remain marked as `review_status: "draft"`.

```dataview
TABLE year, source_status, confidence
FROM "wiki/papers"
WHERE type = "paper" AND review_status = "draft"
SORT file.name ASC
```

# Missing Datapoints (Governance)

The following papers are missing crucial relevance scoring or confidence metrics.

```dataview
TABLE review_status, confidence, relevance_to_in_space_manufacturing AS "ISM Relevance"
FROM "wiki/papers"
WHERE type = "paper" AND (!confidence OR !relevance_to_in_space_manufacturing)
SORT file.name ASC
```
