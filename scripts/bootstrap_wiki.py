import os
import re
import urllib.parse

def generate_slug(text):
    text = text.replace('—', '-').replace('_', '-').replace(' ', '_')
    text = re.sub(r'[^A-Za-z0-9_\-]', '', text)
    return text.strip('_')

def get_author_year_title(alias, filename):
    # alias like: "Zhang 2024 — ESL control on CSS"
    parts = alias.split('—')
    left = parts[0].strip().split(' ')
    author = left[0] if len(left) > 0 else "Unknown"
    year = left[-1] if len(left) > 1 and left[-1].isdigit() else ""
    title = parts[1].strip() if len(parts) > 1 else filename.replace('.pdf', '')
    slug = f"{generate_slug(author)}_{year}_{generate_slug(title)}"
    return author, year, title, slug

def extract_tags(text):
    text = text.lower()
    related = []
    if 'al-cu' in text or 'al - cu' in text or 'al--cu' in text: related.append('[[wiki/alloys/Al-Cu]]')
    if 'al-si' in text or 'al - si' in text: related.append('[[wiki/alloys/Al-Si]]')
    if 'al-ni' in text or 'al - ni' in text or 'alni' in text: related.append('[[wiki/alloys/Al-Ni]]')
    if 'ti-6al-4v' in text or 'ti-46al' in text or 'ti-alloys' in text or 'ti64' in text: related.append('[[wiki/alloys/Ti-alloys]]')
    if 'ni-based' in text or 'superalloy' in text: related.append('[[wiki/alloys/Ni-superalloys]]')
    if 'transparent' in text or 'scn' in text: related.append('[[wiki/alloys/SCN-transparent-analog]]')
    
    if 'iss' in text or 'space station' in text: related.append('[[wiki/platforms/ISS-experiments]]')
    if 'eml' in text or 'levitation' in text or 'esl' in text: related.append('[[wiki/platforms/containerless-EML]]')
    if 'sounding rocket' in text or 'maser' in text: related.append('[[wiki/platforms/sounding-rockets]]')
    if 'declic' in text or 'dsi' in text: related.append('[[wiki/platforms/DECLIC-DSI]]')
    
    if 'phase-field' in text or 'phase field' in text: related.append('[[wiki/modelling/phase-field]]')
    if 'cellular automaton' in text or 'ca-fvm' in text or 'ca fe' in text: related.append('[[wiki/modelling/CA-FE-models]]')
    
    if 'dendritic' in text or 'dendrite' in text: related.append('[[wiki/physics/dendritic-growth]]')
    if 'columnar-to-equiaxed' in text or 'cet' in text: related.append('[[wiki/physics/nucleation-CET]]')
    if 'eutectic' in text: related.append('[[wiki/physics/eutectic-solidification]]')
    if 'directional solidification' in text or 'ds' in text: related.append('[[wiki/methods/directional-solidification]]')
    if 'marangoni' in text: related.append('[[wiki/flow/marangoni-flow]]')
    if 'thermophysical' in text: related.append('[[wiki/methods/thermophysical-property]]')

    # Remove duplicates
    return list(dict.fromkeys(related))

def bootstrap_wiki():
    base_dir = '/Users/rduggineni/Documents/Papers2020-26_WikiAntiGravity'
    index_path = os.path.join(base_dir, 'phd-wiki', 'wiki', '_index.md')
    papers_dir = os.path.join(base_dir, 'phd-wiki', 'wiki', 'papers')
    
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()

    # Regex to find table rows with PDF links
    # | [[../FileName.pdf|Alias]] | Finding |
    pattern = re.compile(r'\|\s*\[\[\.\.\/([^\|]+)\|([^\]]+)\]\]\s*\|\s*(.*?)\s*\|')
    
    new_index_content = index_content
    matches = pattern.findall(index_content)
    
    for filename, alias, finding in matches:
        author, year, title, slug = get_author_year_title(alias, filename)
        md_filename = f"{slug}.md"
        md_filepath = os.path.join(papers_dir, md_filename)
        
        pdf_path = f"[[../../{filename}]]"
        
        combined_text = f"{title} {finding} {filename}"
        auto_links = extract_tags(combined_text)
        related_pages = "\n".join([f"- \"{lnk}\"" for lnk in auto_links])
        if not related_pages:
            related_pages = "[]"
            
        yaml_frontmatter = f"""---
type: paper
title: "{title.replace('"', '')}"
citekey: "{slug}"
year: {year if year else 'null'}
authors: ["{author}"]
journal: ""
doi: ""
zotero_key: ""
pdf: "{pdf_path}"
source_status: "raw"
tags:
  - paper

gravity_regime: ""
platform: []
facility: []
mission: []

alloy_family: []
alloy_composition: []

process: []
solidification_mode: []
flow_regime: []
convection_control: []

diagnostics: []
thermophysical_properties: []
microstructure: []
phase_selection: []
nucleation_behaviour: []
model_used: []

sample_geometry: ""
heating_method: []
cooling_rate: ""
undercooling: ""
containerless: false

relevance_to_in_space_manufacturing: ""
relevance_to_my_phd: ""
confidence: ""
contradictions: []

related_pages: {related_pages if related_pages != "[]" else "[]"}
review_status: "draft"
last_reviewed: ""
---
"""
        
        related_links_str = "\n".join([f"- {lnk}" for lnk in auto_links]) if auto_links else ""
        
        body = f"""
# Summary
{finding}

# Research question

# Experimental or modelling setup

# Materials and alloy system

# Platform and gravity context

# Flow behaviour

# Solidification behaviour

# Key findings
{finding}

# Relevance to in-space manufacturing

# Relevance to my PhD

# Methods and diagnostics

# Models and interpretation

# Contradictions or uncertainties

# Quotable lines

# Related pages
{related_links_str}
"""
        with open(md_filepath, 'w', encoding='utf-8') as f:
            f.write(yaml_frontmatter + body)
            
        # Update index.md replacing the row
        old_link = f"[[../{filename}|{alias}]]"
        # We need to escape spaces correctly for a markdown link inside wiki link? 
        # Obsidian wikilink handles spaces.
        new_link = f"[[wiki/papers/{md_filename.replace('.md', '')}|{alias}]]"
        
        new_index_content = new_index_content.replace(old_link, new_link)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_index_content)
        
    print(f"Successfully processed {len(matches)} papers.")

if __name__ == '__main__':
    bootstrap_wiki()
