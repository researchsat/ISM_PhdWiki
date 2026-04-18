import os
import re
import glob
from pypdf import PdfReader

def clean_text(text):
    # Remove weird newlines and extra spaces
    text = re.sub(r'([a-z])-\n([a-z])', r'\1\2', text) # fix hyphenated word break
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_abstract_from_pdf(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = ""
        # read first 2 pages
        for i in range(min(2, len(reader.pages))):
            extracted = reader.pages[i].extract_text()
            if extracted:
                text += extracted + "\n"
        
        # Heuristic search for abstract boundaries
        match = re.search(r'(?i)abstract(.*?)(?:(?i)1\.\s*introduction|(?i)\bintroduction\b|(?i)a r t i c l e i n f o|(?i)keywords|©)', text, re.DOTALL)
        
        if match:
            abstract_raw = match.group(1).strip()
            # If it's too suspiciously short or long, maybe just fallback
            if 50 < len(abstract_raw) < 4000:
                return clean_text(abstract_raw)
        
        # Fallback 1: Just find 'abstract' and take next 1000 chars
        idx = text.lower().find('abstract')
        if idx != -1:
            raw = text[idx+8:idx+1500]
            # split by introduction if possible
            intro_idx = raw.lower().find('introduction')
            if intro_idx != -1:
                raw = raw[:intro_idx]
            return clean_text(raw)
            
        return "Could not automatically extract abstract."
    
    except Exception as e:
        return f"Error extracting from PDF: {str(e)}"

def process_all_files():
    base_dir = '/Users/rduggineni/Documents/Papers2020-26_WikiAntiGravity'
    papers_dir = os.path.join(base_dir, 'phd-wiki', 'wiki', 'papers')
    
    md_files = glob.glob(os.path.join(papers_dir, '*.md'))
    processed = 0
    
    for md_path in md_files:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract PDF filename from frontmatter
        pdf_match = re.search(r'pdf:\s*"\[\[\.\.\/\.\.\/(.+?)\]\]"', content)
        if not pdf_match:
            continue
            
        pdf_filename = pdf_match.group(1)
        pdf_filepath = os.path.join(base_dir, pdf_filename)
        
        if not os.path.exists(pdf_filepath):
            print(f"Skipping {md_path}, could not find PDF: {pdf_filename}")
            continue
            
        abstract_text = extract_abstract_from_pdf(pdf_filepath)
        
        # Avoid duplicating the abstract
        if "# Abstract (Raw Extraction)" in content:
            continue
            
        replacement_text = f"# Abstract (Raw Extraction)\n{abstract_text}\n\n# Research question"
        new_content = content.replace("# Research question", replacement_text)
        
        if new_content != content:
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            processed += 1
            
    print(f"Extraction complete. Successfully injected abstracts into {processed} markdown files.")

if __name__ == '__main__':
    process_all_files()
