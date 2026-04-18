# PhD Knowledge Vault: User Guide & Walkthrough

Welcome to your Agentic Obsidian Wiki! This guide explains how to properly utilize the architecture we've built. Your literature is no longer a static folder of PDFs; it is an interconnected database tracking authors, alloys, flow phenomena, and in-space manufacturing platforms.

---

## 1. Opening the Environment

1. Download and install **Obsidian**.
2. Select **Open folder as vault**.
3. Point Obsidian to the `/phd-wiki/` folder located inside your `Papers2020-26_WikiAntiGravity` directory.
4. **Crucial Step**: In Obsidian settings (the gear icon), navigate to Community Plugins, turn off Safe Mode, search for **Dataview**, and install/enable it. Dataview is the live-updating SQL dashboard engine that powers your QA and review tables.

---

## 2. Navigating the Vault

Your central homepage is `wiki/_index.md`. Start here every session.

### The 4 Core Hubs
- **Papers (`wiki/papers/`)**: This holds the 54 extracted nodes. Every paper has YAML metadata (author, platform, confidence), the scraped PDF abstract, and dedicated space for your notes.
- **Dashboards (`wiki/dashboards/`)**: Built leveraging the Dataview plugin. Click these nodes in your index to see live matrices showing which papers lack reviews, which alloys map to which platforms, and your overall database sorted by year.
- **Entities (`wiki/authors/`, `wiki/alloys/`, etc.)**: If you click `[Al-Cu]` inside a paper note, you will jump to the overarching Al-Cu alloy hub, where you can trace every other paper that touches that system!
- **Syntheses (`wiki/syntheses/`)**: The capstone nodes aggregating large-scale concepts (e.g. *Convection vs Microstructure*). 

> [!TIP]
> Use Obsidian's **Graph View** (Ctrl/Cmd-G). You will immediately see clusters of papers orbiting around key platforms (like `ISS-EML`) and Authors. This visual web is entirely powered by the tags we ingested.

---

## 3. Workflow: Processing an Existing Paper

Instead of reading PDFs raw, operate primarily inside your Markdown files:

1. Open `_index.md`, scroll to the bottom table, and click on a paper you want to read (e.g., `Zimmermann__grain-refined_Al-Cu_ISS`).
2. Inside that `.md` file, you will find the `pdf: [[...]]` link perfectly pointing to the original document. Click it if you need to reference the original figures.
3. Review the `# Abstract (Raw Extraction)` block that was automatically scraped.
4. **Your Job**: Read the paper, and then write your own analysis natively underneath `# Research question` and `# Key findings`.
5. When finished, change the YAML frontmatter at the top from `review_status: "draft"` to `review_status: "checked"`. It will automatically disappear from your Dataview Review Queue Dashboard!

---

## 4. Workflow: Ingesting a BRAND NEW Paper

When you discover your 55th paper, do not just toss the PDF into a folder!

1. Download the `New_Paper.pdf` and place it in the root folder.
2. Inside Obsidian, duplicate the **Paper note template** (found safely in the layout blueprint) and create a new file in `wiki/papers/`.
3. Fill out the YAML: add `authors: ["Smith"]`, `related_pages: - [[wiki/alloys/Nb-Si]]`, etc.
4. Add the `# Summary`.
5. Link it! Open `wiki/_index.md` and add a new bullet linking to your newly created markdown file. 
6. Because of the bidirectional nature of the vault, your new paper will immediately appear in your Dataview tables and Graph View.

> [!NOTE]  
> If you tag an author or alloy that doesn't exist yet, simply create that file inside `/authors/` or `/alloys/` utilizing the standard templates. 

---

## 5. Routine Maintenance and Governance

A healthy database requires linting. Your AI generated a python script (`phd-wiki/scripts/lint_wiki.py`) that acts as an automated safety check.

**How to run it:**
Open a terminal located in your root `Papers` directory and execute:
```bash
python3 phd-wiki/scripts/lint_wiki.py
```

**What it does:**
- It scans the YAML and text of every single note in your repository.
- If it catches a paper with no conceptual links (an "orphan"), it flags it.
- If it catches a paper with `review_status: "draft"` missing critical reviews, it flags it.
- It outputs exactly what broke directly to `phd-wiki/wiki/log.md`. Always aim for the script to report: *"All checks passed. Graph is healthy."*
