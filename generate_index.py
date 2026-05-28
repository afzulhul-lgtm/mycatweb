"""
generate_index.py  v1.0 — PetPedia Hub
========================================
Run this script every time you add new articles.
Reads articles/ folder and injects static HTML article links
into index.html so that Google can index all your articles.

TECHVIBE-STYLE: Dual layout
  - Static SEO list (Google sees this)
  - JS card layout (users see this)

HOW TO RUN:
    python generate_index.py
"""

import os
import glob
import re

# ---- CHANGE THIS PATH TO MATCH YOUR COMPUTER ----
WEBSITE_ROOT = r"C:\Users\abdul\OneDrive\Desktop\mycatweb"
# --------------------------------------------------

SITE_URL   = "https://petpediahub.online"
ARTICLES_DIR = os.path.join(WEBSITE_ROOT, "articles")
INDEX_HTML   = os.path.join(WEBSITE_ROOT, "index.html")

# ================================================================
print("=" * 55)
print("  PetPedia Hub generate_index.py  v1.0")
print("=" * 55)
print()

# Validate paths
if not os.path.exists(ARTICLES_DIR):
    print(f"ERROR: articles/ folder nahi mila:\n  {ARTICLES_DIR}")
    exit(1)

if not os.path.exists(INDEX_HTML):
    print(f"ERROR: index.html nahi mila:\n  {INDEX_HTML}")
    exit(1)

# Scan articles folder
print("Scanning articles/ folder...")
html_files = glob.glob(os.path.join(ARTICLES_DIR, "*.html"))

if not html_files:
    print("ERROR: articles/ folder mein koi HTML files nahi mili!")
    exit(1)

print(f"OK: {len(html_files)} HTML files mile\n")

# Extract metadata
def extract_meta(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title = ""
    description = ""
    date_str = ""
    image = ""
    
    # Title
    title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
    if title_match:
        title = title_match.group(1).strip()
        if '|' in title:
            title = title.split('|')[0].strip()
    
    # Description
    desc_match = re.search(r'<meta\s+name="description"\s+content="(.*?)"', content)
    if desc_match:
        description = desc_match.group(1).strip()
    
    # Date
    date_match = re.search(r'"datePublished":\s*"(.*?)"', content)
    if not date_match:
        date_match = re.search(r'content="(\d{4}-\d{2}-\d{2})"', content)
    if date_match:
        date_str = date_match.group(1).strip()
    
    # Image
    img_match = re.search(r'<meta\s+property="og:image"\s+content="(.*?)"', content)
    if img_match:
        image = img_match.group(1).strip()
    
    filename = os.path.basename(filepath)
    
    return {
        'title': title,
        'description': description[:120] + '...' if len(description) > 120 else description,
        'date': date_str,
        'image': image,
        'filename': filename,
        'url': f"{SITE_URL}/articles/{filename}"
    }

articles = []
for filepath in html_files:
    try:
        meta = extract_meta(filepath)
        if meta['title']:
            articles.append(meta)
    except Exception as e:
        print(f"WARNING: {os.path.basename(filepath)} read error: {e}")

# Sort by date (newest first)
articles.sort(key=lambda x: x['date'], reverse=True)

print(f"OK: {len(articles)} articles ka metadata ready\n")

# Build static HTML list items (TechVibe style)
print("Building static HTML...")

items_html = ""
for art in articles:
    img_src = art['image'] if art['image'] else f"articles/default.webp"
    date_display = art['date'] if art['date'] else "Recent"
    
    # Format date nicely
    try:
        from datetime import datetime
        dt = datetime.strptime(art['date'], '%Y-%m-%d')
        date_display = dt.strftime('%B %d, %Y')
    except:
        pass
    
    items_html += f"""                <li>
                    <a href="{art['url']}">
                        <img src="{img_src}" alt="{art['title']}" loading="lazy" width="400" height="225">
                        <div>
                            <h3>{art['title']}</h3>
                            <p>{art['description']} &mdash; <small>{date_display}</small></p>
                        </div>
                    </a>
                </li>
"""

print(f"OK: {len(articles)} articles ka HTML ready\n")

# Inject into index.html
print("index.html update ho raha hai...")

with open(INDEX_HTML, 'r', encoding='utf-8') as f:
    html = f.read()

# Find the placeholder comment
start_marker = "<!-- generate_index.py fills this automatically -->"
end_marker = "<!-- If you have not run generate_index.py yet, your articles -->"

if start_marker not in html:
    print("ERROR: index.html mein placeholder marker nahi mila!")
    print("Make sure index.html mein yeh line hai:")
    print("  <!-- generate_index.py fills this automatically -->")
    exit(1)

# Find positions
start_pos = html.index(start_marker)
end_pos = html.index(end_marker, start_pos) if end_marker in html[start_pos:] else len(html)

# Build new content
before = html[:start_pos]
after = html[end_pos:]

new_html = before + start_marker + "\n" + items_html + "                " + html[start_pos + len(start_marker):end_pos] + after

# Actually we need a cleaner approach — just replace between markers
parts = html.split(start_marker, 1)
if len(parts) == 2:
    after_marker = parts[1]
    if end_marker in after_marker:
        _, after_end = after_marker.split(end_marker, 1)
        new_html = parts[0] + start_marker + "\n" + items_html + "                " + end_marker + after_end
    else:
        new_html = parts[0] + start_marker + "\n" + items_html + "\n            " + parts[1]
else:
    new_html = html

with open(INDEX_HTML, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"OK: index.html updated — {len(articles)} articles injected\n")

print("=" * 55)
print(f"DONE! {len(articles)} articles Google ke liye inject ho gaye.")
print("=" * 55)
print("""
Next steps:
  1. index.html check karo — articles list dikhni chahiye
  2. Hostinger se deploy karo
  3. Google Search Console:
     URL Inspection -> https://petpediahub.online/
     -> "Request Indexing"

Har baar naye articles add karne ke baad yeh script chalayein!
""")