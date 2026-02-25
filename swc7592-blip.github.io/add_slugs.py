#!/usr/bin/env python3
"""Add slug field to all posts that don't have one"""
import os
import re
from pathlib import Path
import hashlib

def generate_slug(title):
    """Generate a slug from Korean/English title"""
    # Remove special characters and spaces
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    # Replace spaces with hyphens
    slug = re.sub(r'[-\s]+', '-', slug)
    # Limit length
    slug = slug[:100]
    return slug

def process_post(filepath):
    """Add slug to post if it doesn't have one"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if slug already exists
    if re.search(r'^slug:', content, re.MULTILINE):
        return False, "Already has slug"

    # Extract title
    title_match = re.search(r'^title:\s*"([^"]+)"', content, re.MULTILINE)
    if not title_match:
        return False, "No title found"

    title = title_match.group(1)

    # Generate slug
    slug = generate_slug(title)

    # Find the end of frontmatter (---)
    # Insert slug after the title line
    lines = content.split('\n')
    new_lines = []
    inserted = False

    for i, line in enumerate(lines):
        new_lines.append(line)
        if not inserted and line.startswith('title:'):
            # Insert slug after title
            indent = len(line) - len(line.lstrip())
            slug_line = ' ' * indent + f'slug: {slug}'
            new_lines.append(slug_line)
            inserted = True

    if not inserted:
        return False, "Could not insert slug"

    new_content = '\n'.join(new_lines)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, f"Added slug: {slug}"

def main():
    posts_dir = Path('_posts')
    if not posts_dir.exists():
        print("_posts directory not found")
        return

    count = 0
    for filepath in posts_dir.glob('*.md'):
        success, message = process_post(filepath)
        if success:
            print(f"✓ {filepath.name}: {message}")
            count += 1
        else:
            print(f"- {filepath.name}: {message}")

    print(f"\nTotal posts updated: {count}")

if __name__ == '__main__':
    main()
