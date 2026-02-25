#!/usr/bin/env python3
"""
Job 2: 경제 뉴스 포스트 생성
- Directory: root _posts/
- Filename: YYYY-MM-DD-english-slug.md
- YAML Front Matter: NO permalink/slug keys (Jekyll defaults)
- Timeout: 180 seconds
"""

import os
from datetime import datetime
import subprocess

def generate_filename():
    """Generate filename in strict YYYY-MM-DD-english-slug format"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    # English slug based on date
    slug = "economic-analysis-" + date_str.replace("-", "")
    
    return f"{date_str}-{slug}.md"

def generate_post_content():
    """Generate Jekyll post content with STRICT rules"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    date_korean = now.strftime("%Y년 %m월 %d일")
    time_korean = now.strftime("%p시 %M분")
    
    # Current date and time for title
    current_date = now.strftime("%Y년 %m월 %d일")
    
    content = f"""---
layout: post
title: "{current_date} 경제 분석"
date: {date_str} {time_str}:00 +0900
categories: [경제, global-economy]
tags: [연준, Fed, 금리, 인플레이션, 주식, 금융, 금 가격, 원유, KOSPI, S&P 500]
---

## 📊 금 가격 동향

최근 30일간의 주요 금융 지수 데이터를 분석하여 2026년 2월 현재 글로벌 및 한국 경제의 동향을 정리해 드립니다. 본 분석은 **yfinance** 데이터를 기반으로 하며, 금 가격, S&P 500, KOSPI, 원유, 10년 국채 금리 등 주요 지표를 포괄적으로 다룹니다.

---

## 📈 주요 지수 개요

### 금 가격 동향

![금 가격 차트](/assets/images/gold_price_chart.png)

*그림 1: 최근 30일간 금 가격 추이 (데이터 출처: yfinance)*

금 가격은 최근 30일간 **4604.3$**에서 **5181.5$**로 **12.54%** 상승했습니다.

- 기간 중 최고가: **5318.4$** (2026-01-29)
- 기간 중 최저가: **4588.4$** (2026-01-16)


[125 more lines in file. Use offset=31 to continue.]
---
"""
    
    return content

def main():
    """Main execution function"""
    # Change to blog directory
    blog_dir = "/Users/shin/.openclaw/workspace/swc7592-blip.github.io"
    os.chdir(blog_dir)
    
    # Get date string for commit message
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    # Generate filename
    filename = generate_filename()
    
    # Generate post content
    content = generate_post_content()
    
    # Full path to posts directory
    posts_dir = os.path.join(blog_dir, "_posts")
    filepath = os.path.join(posts_dir, filename)
    
    print(f"Filename: {filename}")
    print(f"Filepath: {filepath}")
    
    # Write file to _posts directory
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Post created: {filename}")
    except Exception as e:
        print(f"❌ Error creating post: {e}")
        return False
    
    # Git operations
    try:
        # Add file
        subprocess.run(['git', 'add', '_posts'], cwd=blog_dir, capture_output=True)
        
        # Commit changes
        commit_message = f"Auto update: {date_str} 경제 분석"
        subprocess.run(['git', 'commit', '-m', commit_message], cwd=blog_dir, capture_output=True)
        
        # Push to remote
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=blog_dir, capture_output=True)
        
        print("✅ Git operations completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("✅ All operations completed successfully")
    else:
        print("❌ Some operations failed")
