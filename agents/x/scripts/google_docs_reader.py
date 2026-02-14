#!/usr/bin/env python3
"""
Google Docs Reader
Reads the content of a Google Docs link and extracts text
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import re
from pathlib import Path

# Configuration
WORKSPACE = Path("/Users/shin/.openclaw/workspace/agents/x")
DATA_DIR = WORKSPACE / "data"
LOGS_DIR = WORKSPACE / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Target URL
TARGET_URL = "https://docs.google.com/document/d/1WoIDNTJDgC1FD_G922U3M09XlGDN-63XnI7t_XbeYM/view?tab=t.0#heading=h.52eca8v8718"

def log(message, level="INFO"):
    """Log message to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}\n"
    
    print(log_message)
    
    log_file = LOGS_DIR / f"google_docs_reader_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message)

def fetch_google_docs(url):
    """Fetch Google Docs content"""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode()
            log(f"Google Docs content fetched successfully! Length: {len(data)}")
            return data
    except urllib.error.HTTPError as e:
        log(f"HTTP Error fetching Google Docs: {e.code} - {e.reason}", level="ERROR")
        return None
    except Exception as e:
        log(f"Request Error fetching Google Docs: {e}", level="ERROR")
        return None

def extract_text_from_html(html_content):
    """Extract text from Google Docs HTML"""
    # Google Docs exports simple HTML with content in <body>
    # Simple tag removal (not perfect, but sufficient for reading)
    
    # Remove style and script tags
    html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL)
    
    # Remove other tags
    text_content = re.sub(r'<[^>]+>', '', html_content)
    
    # Clean up whitespace
    text_content = re.sub(r'\s+', ' ', text_content)
    text_content = text_content.strip()
    
    return text_content

def main():
    """Main execution flow"""
    log("=" * 50)
    log("📺 Google Docs Reader - START")
    log("=" * 50)
    
    try:
        # Step 1: Fetch Google Docs content
        log("Step 1: Google Docs 링크에서 문서 가져오는 중...")
        html_content = fetch_google_docs(TARGET_URL)
        
        if not html_content:
            log("ERROR: 문서를 가져올 수 없습니다.", level="ERROR")
            return
        
        # Step 2: Extract text
        log("Step 2: HTML 파싱 및 텍스트 변환 중...")
        text_content = extract_text_from_html(html_content)
        
        # Step 3: Output text
        print("\n" + "=" * 50)
        print("📄 [문서 내용]")
        print("=" * 50)
        print(text_content)
        print("=" * 50)
        
        # Step 4: Save to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = DATA_DIR / f"google_docs_article_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(text_content)
        
        log(f"문서 저장됨: {filename.name}")
        log("✅ 작업 완료!")
        
    except Exception as e:
        log(f"CRITICAL ERROR: {e}", level="ERROR")
    
    log("=" * 50)
    log("📺 Google Docs Reader - END")
    log("=" * 50)

if __name__ == "__main__":
    main()
