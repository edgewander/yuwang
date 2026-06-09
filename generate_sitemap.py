#!/usr/bin/env python3
"""
Generate sitemap.xml, robots.txt, and article-index.js for prison-art.cn
Scans all .md files in docs/ and category mappings from cat-*.md
"""
import os
import re
import json
from datetime import datetime, timezone

DOCS_DIR = os.path.join(os.path.dirname(__file__), 'docs')
SITE_URL = 'https://prison-art.cn'

# Category mapping from cat-*.md filenames
CATEGORY_MAP = {
    'cat-art.md': '艺术介入监狱',
    'cat-history.md': '监狱历史',
    'cat-misc.md': '杂谈',
    'cat-music.md': '监狱音乐',
    'cat-painting.md': '监狱绘画',
    'cat-photo.md': '监狱摄影',
    'cat-poetry.md': '监狱诗歌',
    'cat-travel.md': '监狱旅游',
}

def parse_categories():
    """Parse cat-*.md files to get article->category mapping"""
    articles = {}  # slug -> {title, categories, path}
    for cat_file, cat_name in CATEGORY_MAP.items():
        cat_path = os.path.join(DOCS_DIR, cat_file)
        if not os.path.exists(cat_path):
            continue
        with open(cat_path, 'r', encoding='utf-8') as f:
            for line in f:
                m = re.search(r'\[([^\]]+)\]\((\d+\.\d+(?:\.\d+)?)\.md\)', line)
                if m:
                    title = m.group(1).strip()
                    slug = m.group(2)
                    if slug not in articles:
                        articles[slug] = {'title': title, 'categories': [], 'path': slug}
                    if cat_name not in articles[slug]['categories']:
                        articles[slug]['categories'].append(cat_name)
    return articles

def parse_all_md():
    """Get all .md files and extract first heading as title"""
    all_md = {}
    for fname in os.listdir(DOCS_DIR):
        if not fname.endswith('.md'):
            continue
        slug = fname.replace('.md', '')
        if slug.startswith('_'):
            continue
        fpath = os.path.join(DOCS_DIR, fname)
        mtime = os.path.getmtime(fpath)
        mod_date = datetime.fromtimestamp(mtime, tz=timezone.utc).strftime('%Y-%m-%d')
        title = None
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('# ') and not line.startswith('## '):
                        title = line[2:].strip()
                        break
        except:
            pass
        all_md[slug] = {
            'path': slug,
            'title': title or slug,
            'lastmod': mod_date,
        }
    return all_md

def generate_sitemap(all_md):
    """Generate sitemap.xml"""
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    urls = [f'  <url>\n    <loc>{SITE_URL}/</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>1.0</priority>\n  </url>']
    # Add category pages
    for cat_file, cat_name in CATEGORY_MAP.items():
        slug = cat_file.replace('.md', '')
        urls.append(f'  <url>\n    <loc>{SITE_URL}/#/{slug}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>')
    # Add all articles
    for slug, info in sorted(all_md.items()):
        if slug in ('00', 'contribute', '_sidebar'):
            continue
        urls.append(f'  <url>\n    <loc>{SITE_URL}/#/{slug}</loc>\n    <lastmod>{info["lastmod"]}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>')

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(urls)}
</urlset>'''
    sitemap_path = os.path.join(os.path.dirname(__file__), 'sitemap.xml')
    with open(sitemap_path, 'w', encoding='utf-8') as f:
        f.write(xml)
    print(f'sitemap.xml generated: {len(urls)} URLs')

def generate_robots():
    """Generate robots.txt"""
    txt = f'''# prison-art.cn
User-agent: *
Allow: /
Sitemap: {SITE_URL}/sitemap.xml

# Block common bot paths
User-agent: AhrefsBot
Disallow: /

User-agent: SemrushBot
Disallow: /
'''
    robots_path = os.path.join(os.path.dirname(__file__), 'robots.txt')
    with open(robots_path, 'w', encoding='utf-8') as f:
        f.write(txt)
    print('robots.txt generated')

def generate_article_index(all_md, cat_articles):
    """Generate article-index.js for related reading and search"""
    # Merge category info into all_md
    index = []
    for slug, info in sorted(all_md.items()):
        if slug in ('00', 'contribute', '_sidebar'):
            continue
        entry = {
            'slug': slug,
            'title': info['title'],
            'path': f'#{slug}',
            'categories': cat_articles.get(slug, {}).get('categories', []),
        }
        index.append(entry)

    js = f'''// Auto-generated article index for related reading module
// Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}
var ARTICLE_INDEX = {json.dumps(index, ensure_ascii=False, indent=2)};
'''
    idx_path = os.path.join(DOCS_DIR, 'article-index.js')
    with open(idx_path, 'w', encoding='utf-8') as f:
        f.write(js)
    print(f'article-index.js generated: {len(index)} articles')

if __name__ == '__main__':
    print('Parsing categories...')
    cat_articles = parse_categories()
    print(f'  Found {len(cat_articles)} categorized articles')

    print('Scanning all markdown files...')
    all_md = parse_all_md()
    print(f'  Found {len(all_md)} markdown files')

    generate_sitemap(all_md)
    generate_robots()
    generate_article_index(all_md, cat_articles)
    print('Done!')
