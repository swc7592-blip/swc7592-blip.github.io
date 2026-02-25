#!/usr/bin/env python3
"""Replace Korean slugs with English slugs based on filename"""
import os
import re
from pathlib import Path

def extract_slug_from_filename(filename):
    """Extract slug from filename (remove date prefix)"""
    # Remove date prefix (YYYY-MM-DD- or YYYY-MM-DD-HH-MM-)
    slug = re.sub(r'^\d{4}-\d{2}-\d{2}(?:-\d{2}-\d{2})?', '', filename)
    # Remove .md extension
    slug = slug.replace('.md', '')
    # Remove leading hyphen if present
    slug = slug.lstrip('-')
    return slug

def fix_post_slug(filepath):
    """Replace slug field with English slug from filename"""
    filename = filepath.name
    english_slug = extract_slug_from_filename(filename)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace slug field
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('slug:'):
            indent = len(line) - len(line.lstrip())
            new_line = ' ' * indent + f'slug: {english_slug}'
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    new_content = '\n'.join(new_lines)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, english_slug

def main():
    posts_dir = Path('_posts')
    if not posts_dir.exists():
        print("_posts directory not found")
        return

    count = 0
    for filepath in sorted(posts_dir.glob('*.md')):
        success, slug = fix_post_slug(filepath)
        if success:
            print(f"✓ {filepath.name}: {slug}")
            count += 1

    print(f"\nTotal posts updated: {count}")

if __name__ == '__main__':
    main()
