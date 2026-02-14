#!/usr/bin/env python3
"""
YouTube Shorts Analyzer - Google Data API v3
Fetches latest shorts from a specific channel and analyzes trends
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import time
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
WORKSPACE = Path("/Users/shin/.openclaw/workspace/agents/x")
DATA_DIR = WORKSPACE / "data"
LOGS_DIR = WORKSPACE / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Google Docs Source (CEO provided)
GOOGLE_DOCS_EXPORT_URL = "https://docs.google.com/document/d/1WoIDNTJDgC1FD_G922U3M09XMlGDN-63XnI7t_XbeYM/export?format=txt"

# YouTube Data API Configuration
# NOTE: The API key is expected to be found in the Google Doc text
YOUTUBE_API_KEY = "" # Will be extracted from doc
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"

# Target Channel
CHANNEL_HANDLE = "곰돌이식사장" # @곰돌이식사장
CHANNEL_ID = "UCKw0O4z8t8t8w8t8w8t8w8t8t8w8t8w8t8w8t8w8t8w8t8w8t8w8t8" # Need to resolve this

# Economy Keywords (Korean and English)
ECONOMY_KEYWORDS = [
    "ETF", "Bitcoin", "Crypto", "Stocks", "Gold", "Inflation",
    "Market", "Economy", "Fed", "Rates", "Treasury", "S&P", "Dow"
]

def log(message, level="INFO"):
    """Log message to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}\n"
    
    print(log_message)
    
    log_file = LOGS_DIR / f"youtube_shorts_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message)

def fetch_google_docs_text():
    """Fetch Google Docs text content"""
    try:
        req = urllib.request.Request(GOOGLE_DOCS_EXPORT_URL)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode()
            log("Google Docs text fetched successfully!")
            return data
    except urllib.error.HTTPError as e:
        log(f"HTTP Error fetching Google Docs: {e.code} - {e.reason}", level="ERROR")
        return None
    except Exception as e:
        log(f"Request Error fetching Google Docs: {e}", level="ERROR")
        return None

def extract_youtube_api_key(text):
    """Extract YouTube Data API Key from text"""
    # Look for d1... pattern (d1WoIDNT...)
    match = re.search(r"d1[A-Za-z0-9_-]{35}", text)
    
    if match:
        api_key = match.group()
        log(f"YouTube API Key extracted: {api_key[:10]}...{api_key[-10]}")
        return api_key
    else:
        log("YouTube API Key not found in text!", level="ERROR")
        return None

def search_youtube_shorts(api_key):
    """Search for latest shorts from channel"""
    if not api_key:
        return []
    
    headers = {
        "Accept": "application/json",
        "X-Goog-Api-Client-Version": "3",
        "X-Goog-Api-Key": api_key
    }
    
    # Search query: "곰돌이식사장 short"
    # Note: Using 'shorts' filter might be complex, 
    # using general search query for now
    params = {
        "part": "snippet",
        "maxResults": 10,
        "q": "곰돌이식사장 short",
        "order": "date", # Get latest
        "type": "video"
        "videoDuration": "short" # Try to get shorts
    }
    
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{YOUTUBE_API_URL}?{encoded_params}"
    
    try:
        req = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode()
            return json.loads(data).get("items", [])
    except urllib.error.HTTPError as e:
        log(f"HTTP Error searching YouTube: {e.code} - {e.reason}", level="ERROR")
        return []
    except Exception as e:
        log(f"Request Error searching YouTube: {e}", level="ERROR")
        return []

def filter_economy_shorts(shorts):
    """Filter shorts for economy related content"""
    economy_shorts = []
    
    if not shorts:
        return economy_shorts
    
    for item in shorts:
        snippet = item.get("snippet", {})
        title = snippet.get("title", "").lower()
        
        # Check for economy keywords
        if any(keyword in title for keyword in ECONOMY_KEYWORDS):
            economy_shorts.append(item)
    
    return economy_shorts

def generate_youtube_report(economy_shorts):
    """Generate economy report"""
    if not economy_shorts:
        return "경제 관련 유튜브 숏츠가 없습니다."
    
    timestamp = datetime.now().strftime("%Y년 %m월 %d일 %H:%M (KST)")
    
    report = f"""
【유튜브 숏츠 경제 브리핑】

📅 **보고 시간:** {timestamp}

---

### 【채널 핵심 숏츠 TOP 5】

"""
    
    # Sort by views or date
    sorted_shorts = sorted(
        economy_shorts, 
        key=lambda x: int(x.get("snippet", {}).get("publishedAt", "0")[:10].replace("-", "").replace("T", "").replace("Z", "").replace(":", "").replace("+", "")),
        reverse=True
    )
    top_shorts = sorted_shorts[:5]
    
    for i, item in enumerate(top_shorts, 1):
        snippet = item.get("snippet", {})
        title = snippet.get("title", "Unknown Title")
        video_id = item.get("id", {}).get("videoId", "")
        publish_time = snippet.get("publishedAt", "Unknown")
        
        report += f"""
{i}. 제목: {title}
• 영상 ID: {video_id}
• 게시일: {publish_time}
"""
    
    # Keyword Analysis
    keyword_counts = {}
    for item in economy_shorts:
        title = item.get("snippet", {}).get("title", "").lower()
        for keyword in ECONOMY_KEYWORDS:
            if keyword in title:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
    
    report += f"""

### 【채널 키워드 분석】

"""
    
    # Top 5 keywords
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for keyword, count in sorted_keywords:
        report += f"• {keyword}: {count}회 언급\n"
    
    report += f"""

### 【시장 테마 분석】

"""
    
    # ETF/Crypto Theme
    if any(kw in keyword_counts for kw in ["ETF", "Bitcoin", "Crypto"]):
        report += "• **ETF/암호화폭:** 유튜버 쇼츠(Shorts)에서도 ETF/암호화폭 관련 키워드 빈도 확인\n"
    
    # Market/Economy Theme
    if any(kw in keyword_counts for kw in ["Market", "Stocks", "Economy"]):
        report += "• **주식/시장:** 경제 지표 및 시장 동향 관련 쇼츠 발견\n"
    
    # Interest Rates Theme
    if any(kw in keyword_counts for kw in ["Fed", "Rates", "Treasury"]):
        report += "• **금리/인플레이션:** 연준 금리 정책 및 국채 관련 관심 증가\n"
    
    # Tech/AI Theme
    if any(kw in keyword_counts for kw in ["AI", "Tech"]):
        report += "• **기술주/AI:** 기술주 및 AI 관련 쇼츠 부각\n"
    
    report += f"""

### 【종합 인사이트】

• **전체 채널 분위:** 유튜브 숏츠(Shorts) 형식의 경제 관련 콘텐츠 증가 경향
• **주요 이슈:** 경제 키워드를 활용한 쇼츠 발견
• **시나리오:** 쇼츠(Shorts)의 빠른 확산성은 경제 정보의 습득 속도를 가속시킬 가능성 있음

### 【출처】

• Google Data API v3
• 채널: @{CHANNEL_HANDLE}
• 데이터 기준: 최신 숏츠(Shorts) 10개

#유튜브 #쇼츠 #경제 #숏츠 #데이터분석
"""
    
    return report

def save_report(report):
    """Save report to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = DATA_DIR / f"youtube_shorts_report_{timestamp}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    log(f"Report saved to {filename.name}")

def main():
    """Main execution flow"""
    log("=" * 50)
    log("📺 YouTube Shorts Analyzer - START")
    log("=" * 50)
    
    try:
        # Step 1: Fetch Google Docs Text
        log("Step 1: Google Docs 텍스트 추출 중...")
        docs_text = fetch_google_docs_text()
        
        if not docs_text:
            log("ERROR: Google Docs 텍스트를 가져올 수 없습니다.", level="ERROR")
            return
        
        # Step 2: Extract YouTube API Key
        log("Step 2: YouTube API Key 추출 중...")
        YOUTUBE_API_KEY = extract_youtube_api_key(docs_text)
        
        if not YOUTUBE_API_KEY:
            log("ERROR: YouTube API Key를 찾을 수 없습니다.", level="ERROR")
            return
        
        # Step 3: Search YouTube Shorts
        log("Step 3: 유튜브 숏츠 검색 중...")
        shorts = search_youtube_shorts(YOUTUBE_API_KEY)
        log(f"Step 3 Complete: 총 숏츠 수집: {len(shorts)}개")
        
        # Step 4: Filter Economy Related Shorts
        log("Step 4: 경제 관련 숏츠 필터링 중...")
        economy_shorts = filter_economy_shorts(shorts)
        log(f"Step 4 Complete: 경제 관련 숏츠: {len(economy_shorts)}개")
        
        # Step 5: Generate Report
        log("Step 5: 유튜브 경제 브리핑 생성...")
        report = generate_youtube_report(economy_shorts)
        
        # Step 6: Save Report
        save_report(report)
        
        # Step 7: Output to Console
        print("\n" + "=" * 50)
        print("📺 [YOUTUBE SHORTS ANALYSIS]")
        print("=" * 50)
        print(report)
        print("=" * 50)
        
        log("✅ 실행 완료!")
        
    except Exception as e:
        log(f"CRITICAL ERROR: {e}", level="ERROR")
    
    log("=" * 50)
    log("📺 YouTube Shorts Analyzer - END")
    log("=" * 50)

if __name__ == "__main__":
    main()
