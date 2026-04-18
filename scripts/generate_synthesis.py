import os
import glob
import re

SYNTHESES_DIR = '/Users/rduggineni/Documents/Papers2020-26_WikiAntiGravity/phd-wiki/wiki/syntheses'
PAPERS_DIR = '/Users/rduggineni/Documents/Papers2020-26_WikiAntiGravity/phd-wiki/wiki/papers'
INDEX_FILE = '/Users/rduggineni/Documents/Papers2020-26_WikiAntiGravity/phd-wiki/wiki/_index.md'

topics = {
    "Convection_vs_microstructure_under_microgravity": {
        "title": "Convection vs Microstructure under Microgravity",
        "keywords": ["convection", "marangoni", "flow", "gjitter", "g-level", "stirring", "buoyancy", "magnetic field"],
        "papers": []
    },
    "Platforms_for_metal_alloy_microgravity_research": {
        "title": "Platforms for Metal Alloy Microgravity Research",
        "keywords": ["iss", "eml", "esl", "space station", "sounding rocket", "parabolic", "declic", "drop tower", "levitation"],
        "papers": []
    },
    "Implications_for_in-space_manufacturing": {
        "title": "Implications for In-Space Manufacturing",
        "keywords": ["ism", "isru", "manufacturing", "additive", "3d printing", "laser", "lunar", "regolith", "welding", "fabrication", "component"],
        "papers": []
    },
    "Open_questions_for_my_PhD": {
        "title": "Open Questions and Contradictions for my PhD",
        "keywords": ["contradict", "anomalous", "unresolved", "unknown", "open question", "future work", "poorly understood", "spurious"],
        "papers": []
    }
}

def extract_summary_from_md(content):
    # Try to grab the first summary lines
    match = re.search(r'# Summary\n(.*?)\n# ', content, re.DOTALL)
    if match:
        sum_text = match.group(1).strip()
        if sum_text:
            return sum_text
    return ""

def process_papers():
    md_files = glob.glob(os.path.join(PAPERS_DIR, '*.md'))
    
    for md_path in md_files:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        filename = os.path.basename(md_path).replace('.md', '')
        link = f"[[wiki/papers/{filename}]]"
        
        # Get title from frontmatter if possible
        title_match = re.search(r'title:\s*"(.*?)"', content)
        title = title_match.group(1) if title_match else filename
        
        summary = extract_summary_from_md(content)
        search_text = content.lower()
        
        for key, data in topics.items():
            for kw in data["keywords"]:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, search_text):
                    # Found a match
                    if not any(p['link'] == link for p in data["papers"]):
                        data["papers"].append({
                            "title": title,
                            "link": link,
                            "summary": summary
                        })
                    break

def generate_synthesis_pages():
    for key, data in topics.items():
        filename = f"{key}.md"
        filepath = os.path.join(SYNTHESES_DIR, filename)
        
        links_block = "\n".join([f"- {p['link']}: {p['summary']}" for p in data['papers']])
        
        yaml = f"""---
type: synthesis
title: "{data['title']}"
scope: "Generated aggregation based on keyword heuristics"
status: "draft"
tags:
  - synthesis
---

# {data['title']}

## Purpose
This page aggregates findings from all extracted literature notes that match the conceptual keywords for this topic.

## Relevant Literature Insights
{links_block}

## Open Analysis
*Pending manual synthesis by researcher.*
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(yaml)
        print(f"Generated {filename} with {len(data['papers'])} paper references.")

def update_index_links():
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for key in topics.keys():
        old_link = f"[[{key}]]"
        new_link = f"[[wiki/syntheses/{key}|{topics[key]['title']}]]"
        content = content.replace(old_link, new_link)
        
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated _index.md synthesis links.")

if __name__ == '__main__':
    process_papers()
    generate_synthesis_pages()
    update_index_links()
