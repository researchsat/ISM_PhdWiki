---
title: "All Papers Database"
type: dashboard
---

# All Papers Database

This dashboard acts as a live index of every paper ingested into the Vault.

```dataview
TABLE year, authors, platform, alloy_family
FROM "wiki/papers"
WHERE type = "paper"
SORT year DESC
```
