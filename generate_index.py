"""
generate_index.py — PetPedia Hub
articles/ folder ke saare HTML files ko scan karta hai
aur index.html generate karta hai with proper links
"""

import os
import glob
from datetime import datetime

# Configuration
ARTICLES_DIR = "articles"
OUTPUT_FILE = "index.html"
SITE_NAME = "🐾 PetPedia Hub"
SITE_URL = "https://petpediahub.online"

def extract_meta_from_html(filepath):
    """Extract title, description, date from HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title = ""
    description = ""
    date_str = ""
    
    # Extract title
    if '<title>' in content and '</title>' in content:
        title_start = content.find('<title>') + 7
        title_end = content.find('</title>')
        title = content[title_start:title_end].strip()
        # Remove site name from title
        if '|' in title:
            title = title.split('|')[0].strip()
    
    # Extract meta description
    if 'name="description"' in content:
        desc_start = content.find('content="', content.find('name="description"')) + 9
        desc_end = content.find('"', desc_start)
        description = content[desc_start:desc_end].strip()
    
    # Extract date
    if 'datePublished' in content:
        date_start = content.find('"datePublished"') + 18
        date_str = content[date_start:date_start+10].strip('"').strip()
    elif 'article:published_time' in content:
        date_start = content.find('content="', content.find('article:published_time"')) + 9
        date_end = content.find('"', date_start)
        date_str = content[date_start:date_end].strip()[:10]
    
    # Extract featured image
    image = ""
    if 'og:image' in content:
        img_start = content.find('content="', content.find('og:image"')) + 9
        img_end = content.find('"', img_start)
        image = content[img_start:img_end].strip()
    
    # Extract category from breadcrumb
    category = ""
    if 'BreadcrumbList' in content:
        # Try to find category from breadcrumb
        cat_section = content[content.find('BreadcrumbList'):]
        if '"position": 2' in cat_section:
            name_start = cat_section.find('"name": "', cat_section.find('"position": 2')) + 9
            name_end = cat_section.find('"', name_start)
            category = cat_section[name_start:name_end].strip()
    
    return {
        'title': title,
        'description': description,
        'date': date_str,
        'image': image,
        'category': category,
        'filename': os.path.basename(filepath),
        'url': f"{SITE_URL}/{ARTICLES_DIR}/{os.path.basename(filepath)}"
    }

def generate_index():
    """Generate index.html with all articles"""
    
    # Find all HTML files in articles directory
    html_files = glob.glob(os.path.join(ARTICLES_DIR, "*.html"))
    
    if not html_files:
        print("⚠️ Koi article nahi mila articles/ folder mein!")
        return
    
    articles = []
    for filepath in html_files:
        try:
            meta = extract_meta_from_html(filepath)
            if meta['title']:
                articles.append(meta)
        except Exception as e:
            print(f"❌ Error reading {filepath}: {e}")
    
    # Sort by date (newest first)
    articles.sort(key=lambda x: x['date'], reverse=True)
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{SITE_NAME} — Latest Articles</title>
    <meta name="description" content="Latest pet care articles, vet-approved guides, and dog food recall alerts from PetPedia Hub.">
    <link rel="canonical" href="{SITE_URL}/" />
    <meta property="og:title" content="{SITE_NAME} — Latest Articles">
    <meta property="og:description" content="Latest pet care articles, vet-approved guides, and dog food recall alerts.">
    <meta property="og:url" content="{SITE_URL}/">
    <meta property="og:type" content="website">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Poppins', sans-serif; background: #fafafa; color: #333; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 20px; }}
        header {{ background: linear-gradient(135deg, #e1306c, #c0143c); color: #fff; padding: 40px 0; text-align: center; margin-bottom: 40px; }}
        header h1 {{ font-size: 2.5rem; font-weight: 700; }}
        header p {{ font-size: 1.1rem; opacity: 0.9; margin-top: 10px; }}
        .articles-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 25px; }}
        .article-card {{ background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.08); transition: transform 0.2s, box-shadow 0.2s; }}
        .article-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 25px rgba(0,0,0,0.12); }}
        .article-card img {{ width: 100%; height: 200px; object-fit: cover; }}
        .article-card-body {{ padding: 20px; }}
        .article-card .category {{ display: inline-block; background: #fff0f3; color: #e1306c; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600; margin-bottom: 10px; }}
        .article-card h2 {{ font-size: 1.15rem; line-height: 1.4; margin-bottom: 10px; }}
        .article-card h2 a {{ color: #222; text-decoration: none; }}
        .article-card h2 a:hover {{ color: #e1306c; }}
        .article-card .description {{ font-size: 0.88rem; color: #666; line-height: 1.5; margin-bottom: 12px; }}
        .article-card .date {{ font-size: 0.78rem; color: #999; }}
        .footer {{ text-align: center; padding: 40px 0; color: #888; font-size: 0.9rem; border-top: 1px solid #eee; margin-top: 40px; }}
        @media (max-width: 768px) {{ .articles-grid {{ grid-template-columns: 1fr; }} header h1 {{ font-size: 1.8rem; }} }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{SITE_NAME}</h1>
            <p>Vet-approved pet care guides, dog food recall alerts & expert advice</p>
        </div>
    </header>
    <main class="container">
        <div class="articles-grid">
"""

    for article in articles:
        date_display = article['date'] if article['date'] else "Recent"
        image_html = f'<img src="{article["image"]}" alt="{article["title"]}" loading="lazy">' if article['image'] else '<div style="height:200px;background:#f0f0f0;"></div>'
        category_html = f'<span class="category">{article["category"]}</span>' if article['category'] else ''
        
        html += f"""
            <article class="article-card">
                {image_html}
                <div class="article-card-body">
                    {category_html}
                    <h2><a href="{article['url']}">{article['title']}</a></h2>
                    <p class="description">{article['description'][:150]}...</p>
                    <span class="date">📅 {date_display}</span>
                </div>
            </article>
"""

    html += f"""
        </div>
    </main>
    <footer class="footer">
        <p>&copy; 2026 PetPedia Hub — All rights reserved</p>
    </footer>
</body>
</html>
"""

    # Write index.html
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Generated {OUTPUT_FILE} with {len(articles)} articles!")
    print(f"📁 Location: {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    generate_index()