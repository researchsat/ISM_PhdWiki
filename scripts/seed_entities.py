import os
import glob
import re

WIKI_ROOT = '/Users/rduggineni/Documents/Papers2020-26_WikiAntiGravity/phd-wiki/wiki'
PAPERS_DIR = os.path.join(WIKI_ROOT, 'papers')
AUTHORS_DIR = os.path.join(WIKI_ROOT, 'authors')
ALLOYS_DIR = os.path.join(WIKI_ROOT, 'alloys')

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Blueprint templates
AUTHOR_TEMPLATE = """---
type: author
name: "{name}"
aliases: []
affiliations: []
themes: []
recurring_platforms: []
recurring_alloys: []
papers: []
tags:
  - author
---

# Summary

# Contributions to the field

# Recurring topics

# Related papers

# Notes
"""

ALLOY_TEMPLATE = """---
type: alloy
name: "{name}"
family: ""
aliases: []
representative_compositions: []
key_processes: []
key_phenomena: []
platforms: []
papers: []
tags:
  - alloy
---

# Summary

# Why this alloy system matters

# Thermophysical and solidification relevance

# Known microgravity studies

# Flow and solidification behaviour

# Related methods

# Related papers

# Open questions
"""

def seed():
    ensure_dir(AUTHORS_DIR)
    ensure_dir(ALLOYS_DIR)
    
    md_files = glob.glob(os.path.join(PAPERS_DIR, '*.md'))
    authors_found = set()
    alloys_found = set()
    
    # Extract from papers
    for md_path in md_files:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract authors
        author_match = re.search(r'authors:\s*\["(.*?)"\]', content)
        if author_match:
            author_names = author_match.group(1).split('", "') # Handles potential multiple authors or just single
            for aname in author_names:
                if aname and aname.strip() != "Unknown":
                    authors_found.add(aname.strip())

        # Extract alloys
        alloy_matches = re.findall(r'\[\[wiki/alloys/(.*?)\]\]', content)
        for amatch in alloy_matches:
            # Drop the split anchor if it exists `[[wiki/alloys/AlCu|AlCu]]`
            alloys_found.add(amatch.split('|')[0].strip())

    authors_created = 0
    alloys_created = 0

    # Seed Authors
    for author in authors_found:
        # Sanitize filename
        safe_name = author.replace(' ', '_').replace('/', '_')
        path = os.path.join(AUTHORS_DIR, f"{safe_name}.md")
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(AUTHOR_TEMPLATE.format(name=author))
            authors_created += 1

    # Seed Alloys
    for alloy in alloys_found:
        safe_name = alloy.replace(' ', '_').replace('/', '_')
        path = os.path.join(ALLOYS_DIR, f"{safe_name}.md")
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                f.write(ALLOY_TEMPLATE.format(name=alloy))
            alloys_created += 1

    print(f"Entities Seeded! Generated {authors_created} missing Author records and {alloys_created} missing Alloy records.")

if __name__ == '__main__':
    seed()
