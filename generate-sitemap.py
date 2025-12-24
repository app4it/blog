#!/usr/bin/env python3
"""
Sitemap Generator for App4it Blog
Automatically generates sitemap.xml based on posts in posts/posts.json
"""

import json
import os
from datetime import datetime
import re

def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)
    
    if match:
        frontmatter = {}
        for line in match.group(1).split('\n'):
            # Skip empty lines
            if not line.strip():
                continue
            # Look for key: value pattern
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                # Remove quotes (single or double) from the beginning and end
                if value and ((value.startswith('"') and value.endswith('"')) or 
                             (value.startswith("'") and value.endswith("'"))):
                    value = value[1:-1]
                frontmatter[key] = value
        return frontmatter
    return {}

def generate_sitemap():
    """Generate sitemap.xml from blog posts"""
    
    base_url = "https://blog.app4it.de"
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Read posts.json
    with open('posts/posts.json', 'r') as f:
        posts = json.load(f)
    
    # Start building sitemap XML
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        '  <!-- Homepage -->',
        '  <url>',
        f'    <loc>{base_url}/</loc>',
        f'    <lastmod>{current_date}</lastmod>',
        '    <changefreq>weekly</changefreq>',
        '    <priority>1.0</priority>',
        '  </url>',
    ]
    
    # Add each blog post
    for post_file in posts:
        slug = post_file.replace('.md', '')
        post_path = f'posts/{post_file}'
        
        # Read post to get metadata
        try:
            with open(post_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            frontmatter = parse_frontmatter(content)
            post_date = frontmatter.get('date', current_date)
            
            xml_lines.extend([
                f'  <!-- {slug} -->',
                '  <url>',
                f'    <loc>{base_url}/post?slug={slug}</loc>',
                f'    <lastmod>{post_date}</lastmod>',
                '    <changefreq>monthly</changefreq>',
                '    <priority>0.8</priority>',
                '  </url>',
            ])
        except Exception as e:
            print(f'Warning: Could not process {post_file}: {e}')
    
    xml_lines.append('</urlset>')
    
    # Write sitemap.xml
    sitemap_content = '\n'.join(xml_lines)
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    
    print(f'✓ Sitemap generated successfully with {len(posts)} blog posts')
    print(f'  Location: sitemap.xml')
    print(f'  URL: {base_url}/sitemap.xml')

if __name__ == '__main__':
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    generate_sitemap()
