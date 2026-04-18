import os
import glob
import yaml
import re

def gather_papers(wiki_dir):
    papers = []
    papers_dir = os.path.join(wiki_dir, 'papers')
    for filepath in glob.glob(os.path.join(papers_dir, '*.md')):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract YAML frontmatter
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                frontmatter = yaml.safe_load(match.group(1))
                if frontmatter and frontmatter.get('type') == 'paper':
                    frontmatter['filename'] = os.path.basename(filepath).replace('.md', '')
                    papers.append(frontmatter)
            except yaml.YAMLError:
                pass
    return papers

def compile_dashboards():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    wiki_dir = os.path.join(base_dir, 'wiki')
    dashboard_dir = os.path.join(wiki_dir, 'dashboards')
    
    papers = gather_papers(wiki_dir)
    
    # 1_All_Papers_Database.md
    db1_path = os.path.join(dashboard_dir, '1_All_Papers_Database.md')
    if os.path.exists(db1_path):
        with open(db1_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        static_start = "<!-- STATIC_TABLE_START -->\n"
        static_end = "<!-- STATIC_TABLE_END -->"
        
        # Build table
        table_md = "| Title | Year | Authors | Platform | Alloy Family |\n"
        table_md += "|-------|------|---------|----------|--------------|\n"
        papers_sorted = sorted(papers, key=lambda x: str(x.get('year', '')), reverse=True)
        for p in papers_sorted:
            title = p.get('title', '')
            year = str(p.get('year', ''))
            authors = ", ".join(p.get('authors', [])) if isinstance(p.get('authors'), list) else str(p.get('authors', ''))
            platform = ", ".join(p.get('platform', [])) if isinstance(p.get('platform'), list) else str(p.get('platform', ''))
            alloy = ", ".join(p.get('alloy_family', [])) if isinstance(p.get('alloy_family'), list) else str(p.get('alloy_family', ''))
            link = f"[[wiki/papers/{p['filename']}\\|{title}]]"
            table_md += f"| {link} | {year} | {authors} | {platform} | {alloy} |\n"
            
        replacement = static_start + "### Static Render (For Quartz)\n" + table_md + static_end
        
        if static_start in content:
            content = re.sub(r'<!-- STATIC_TABLE_START -->.*?<!-- STATIC_TABLE_END -->', replacement, content, flags=re.DOTALL)
        else:
            content += "\n" + replacement
            
        with open(db1_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    # 2_Review_Queue_and_Gaps.md
    db2_path = os.path.join(dashboard_dir, '2_Review_Queue_and_Gaps.md')
    if os.path.exists(db2_path):
        with open(db2_path, 'r', encoding='utf-8') as f:
            content2 = f.read()
            
        table_md2 = "| Title | Review Status | Last Reviewed |\n"
        table_md2 += "|-------|---------------|---------------|\n"
        papers_review = sorted(papers, key=lambda x: str(x.get('last_reviewed', '')), reverse=True)
        for p in papers_review:
            if str(p.get('review_status', '')) not in ["done", "complete"]:
                title = p.get('title', '')
                status = str(p.get('review_status', ''))
                last_reviewed = str(p.get('last_reviewed', ''))
                link = f"[[wiki/papers/{p['filename']}\\|{title}]]"
                table_md2 += f"| {link} | {status} | {last_reviewed} |\n"
                
        replacement2 = static_start + "### Static Render (For Quartz)\n" + table_md2 + static_end
        if static_start in content2:
            content2 = re.sub(r'<!-- STATIC_TABLE_START -->.*?<!-- STATIC_TABLE_END -->', replacement2, content2, flags=re.DOTALL)
        else:
            content2 += "\n" + replacement2
        with open(db2_path, 'w', encoding='utf-8') as f:
            f.write(content2)

    # 3_Platforms_and_Alloys.md
    db3_path = os.path.join(dashboard_dir, '3_Platforms_and_Alloys.md')
    if os.path.exists(db3_path):
        with open(db3_path, 'r', encoding='utf-8') as f:
            content3 = f.read()
            
        table_md3 = "| Title | Platform | Alloy Family |\n"
        table_md3 += "|-------|----------|--------------|\n"
        for p in papers:
            title = p.get('title', '')
            platform = ", ".join(p.get('platform', [])) if isinstance(p.get('platform'), list) else str(p.get('platform', ''))
            alloy = ", ".join(p.get('alloy_family', [])) if isinstance(p.get('alloy_family'), list) else str(p.get('alloy_family', ''))
            link = f"[[wiki/papers/{p['filename']}\\|{title}]]"
            table_md3 += f"| {link} | {platform} | {alloy} |\n"
                
        replacement3 = static_start + "### Static Render (For Quartz)\n" + table_md3 + static_end
        if static_start in content3:
            content3 = re.sub(r'<!-- STATIC_TABLE_START -->.*?<!-- STATIC_TABLE_END -->', replacement3, content3, flags=re.DOTALL)
        else:
            content3 += "\n" + replacement3
        with open(db3_path, 'w', encoding='utf-8') as f:
            f.write(content3)
            
    print("Compiled static dashboard tables.")

if __name__ == '__main__':
    compile_dashboards()
