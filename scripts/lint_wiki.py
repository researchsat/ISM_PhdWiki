import os
import glob
import re

PAPERS_DIR = '/Users/rduggineni/Documents/Papers2020-26_WikiAntiGravity/phd-wiki/wiki/papers'
LOG_FILE = '/Users/rduggineni/Documents/Papers2020-26_WikiAntiGravity/phd-wiki/wiki/log.md'

def append_to_log(message):
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(message + "\n")
    except FileNotFoundError:
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write("# Maintenance Log\n\n" + message + "\n")

def lint_papers():
    md_files = glob.glob(os.path.join(PAPERS_DIR, '*.md'))
    issues = []
    
    for md_path in md_files:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        filename = os.path.basename(md_path)
        
        # Check 1: Empty Related Links
        if 'related_pages: []' in content or 'related_pages:\n[]' in content:
            issues.append(f"- **WARNING (Orphan):** `{filename}` has 0 extracted related topics.")
            
        # Check 2: Abstract Failure
        if 'Could not automatically extract abstract.' in content:
            issues.append(f"- **INFO (Missing Text):** `{filename}` failed programmatic abstract extraction.")
            
        # Check 3: Missing confidence / contradictions (QA queue)
        if 'confidence: ""' in content:
            issues.append(f"- **TODO (Governance):** `{filename}` is missing QA metrics like confidence/contradictions.")
            
    # Output to log
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    log_entry = f"## Lint Run: {timestamp}\nScanned {len(md_files)} component files.\n\n"
    if issues:
        log_entry += "\n".join(issues)
    else:
        log_entry += "- All checks passed. Graph is healthy."
        
    log_entry += "\n\n---\n"
    append_to_log(log_entry)
    print(f"Lint complete. Found {len(issues)} governance items. Check wiki/log.md.")

if __name__ == '__main__':
    lint_papers()
