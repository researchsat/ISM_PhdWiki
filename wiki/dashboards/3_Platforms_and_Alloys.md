---
title: "Platforms and Alloys Matrix"
type: dashboard
---

# Experimental Platforms Used

A live map of which microgravity simulation platforms are tied to which papers.

```dataview
TABLE platform, facility, mission
FROM "wiki/papers"
WHERE type = "paper" AND (platform != null OR length(platform) > 0)
SORT file.name ASC
```

# Associated Alloy Systems

Map of literature by alloy composition constraints.

```dataview
TABLE alloy_family, alloy_composition, solidification_mode
FROM "wiki/papers"
WHERE type = "paper" AND (alloy_family != null OR length(alloy_family) > 0)
SORT file.name ASC
```
