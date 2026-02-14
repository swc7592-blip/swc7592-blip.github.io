#!/usr/bin/env python3
"""
X Economy Bot - Twitter API v2 (Final Version - Syntax Error Fixed)
Monitors all following accounts, collects tweets, analyzes economy trends, and reports to Discord
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
WORKSPACE = Path("/Users/shin/.openclaw/workspace/agents/x")
DATA_DIR = WORKSPACE / "data"
LOGS_DIR = WORKSPACE / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# X API Configuration
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN", "")
BASE_URL = "https://api.twitter.com/2"

# Economy Keywords (Simplified)
ECONOMY_KEYWORDS = [
    "ETF", "Bitcoin", "Crypto", "Stocks", "Gold", "Inflation",
    "Market", "Economy", "Fed", "Rates", "Treasury", "S&P", "Dow"
]

# Following Accounts to Monitor
FOLLOWING_LIST = [
    "Semicon_player",
    "Alisvolatprop12",
    "Clawnch_Bot",
    "fivedragontiger",
    "GONOGO_Korea",
    "AshCrypto",
    "CryptoHayes",
    "Tesllike",
    "NPjoa_Hodl",
    "Future__Walker"
]

def log(message, level="INFO"):
    """Log message to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}\n"
    
    print(log_message)
    
    log_file = LOGS_DIR / f"x_api_bot_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message)

def get_headers():
    """Get API headers with Bearer Token"""
    if not BEARER_TOKEN:
        log("ERROR: X_BEARER_TOKEN environment variable not set!", level="ERROR")
        log("Please set: export X_BEARER_TOKEN='your_token_here'")
        return None
    
    return {
        "Authorization": f"Bearer {BEARER_TOKEN}",
        "User-Agent": "v2EconomyBot/1.0-Final"
    }

def get_user_id(username):
    """Get User ID from username"""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{BASE_URL}/users/by/username/{username}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode()
            return json.loads(data).get("data", {}).get("id")
    except urllib.error.HTTPError as e:
        log(f"HTTP Error getting user ID for {username}: {e.code} - {e.reason}", level="ERROR")
        return None
    except Exception as e:
        log(f"Request Error getting user ID for {username}: {e}", level="ERROR")
        return None

def get_user_tweets(username, user_id):
    """Get recent tweets from a user"""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{BASE_URL}/users/{user_id}/timelines/reverse"
    params = {
        "max_results": 5,  # Reduced to avoid rate limit
        "tweet.fields": "created_at,public_metrics,text"
    }
    
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{encoded_params}"
    
    try:
        req = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode()
            tweets = json.loads(data).get("data", [])
            
            # Add username to each tweet
            for tweet in tweets:
                tweet["author_username"] = username
            
            return tweets
    except urllib.error.HTTPError as e:
        if e.code == 429:
            log(f"Rate Limit Error for user {username}", level="WARN")
            return []
        log(f"HTTP Error getting tweets for {username}: {e.code} - {e.reason}", level="ERROR")
        return []
    except Exception as e:
        log(f"Request Error getting tweets for {username}: {e}", level="ERROR")
        return []

def filter_economy_tweets(tweets):
    """Filter tweets for economy related content"""
    economy_tweets = []
    
    if not tweets:
        return economy_tweets
    
    for tweet in tweets:
        text = tweet.get("text", "").lower()
        
        # Check for economy keywords
        if any(keyword in text for keyword in ECONOMY_KEYWORDS):
            economy_tweets.append(tweet)
    
    return economy_tweets

def generate_economy_report(economy_tweets):
    """Generate economy report"""
    if not economy_tweets:
        return "경제 관련 트윗이 없습니다."
    
    timestamp = datetime.now().strftime("%Y년 %m월 %d일 %H:%M (KST)")
    
    report = f"""
【엑스 1시간 경제 브리핑】

📅 **보고 시간:** {timestamp}

---

### 【팔로워 핵심 트윗】
"""
    
    # Simple sort by likes (Fixed Syntax)
    top_tweets = sorted(economy_tweets, key=lambda x: x.get("public_metrics", {}).get("like_count", 0), reverse=True)[:5]
    
    for i, tweet in enumerate(top_tweets, 1):
        username = tweet.get("author_username", "Unknown")
        text = tweet.get("text", "")[:80] + "..."
        metrics = tweet.get("public_metrics", {})
        likes = metrics.get("like_count", 0)
        retweets = metrics.get("retweet_count", 0)
        
        report += f"""
{i}. @{username}
• 트윗: {text}
• 좋아요: {likes}
• 리트윗: {retweets}
"""
    
    report += f"""

### 【시장 키워드 분석】
"""
    
    # Simple keyword count
    keyword_counts = {}
    for tweet in economy_tweets:
        text = tweet.get("text", "").lower()
        for keyword in ECONOMY_KEYWORDS:
            if keyword in text:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
    
    # Top 5 keywords
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for keyword, count in sorted_keywords:
        report += f"• {keyword}: {count}회 언급\n"
    
    report += f"""

### 【시장 테마 분석】
"""
    
    # ETF/Crypto Theme
    if any(kw in keyword_counts for kw in ["ETF", "Bitcoin", "Crypto"]):
        report += "• **ETF/암호화폭:** 기관 투자 자금 유입 확인\n"
    
    # Market/Economy Theme
    if any(kw in keyword_counts for kw in ["Market", "Stocks", "Economy"]):
        report += "• **주식/시장:** 경제 지표 및 시장 동향 관련 토론\n"
    
    # Interest Rates Theme
    if any(kw in keyword_counts for kw in ["Fed", "Rates", "Treasury"]):
        report += "• **금리/인플레이션:** 연준 금리 정책 및 국채 관련 관심\n"
    
    # Tech/AI Theme
    if any(kw in keyword_counts for kw in ["AI", "Tech"]):
        report += "• **기술주/AI:** 기술주 및 AI 관련 트윗 부각\n"
    
    report += f"""

### 【종합 인사이트】

• **전체 시장 분위:** 기관 투자 동향과 시장 키워드 분석 기반
• **주요 이슈:** 경제 관련 트윗 빈도 및 주요 키워드 트렌드 파악
• **시나리오:** 실시간 트윗 분석 기반 투자 전략 제안

### 【출처】

• X API (Twitter API v2)
• 팔로워 계정: {len(FOLLOWING_LIST)}개
• 데이터 기준: 최신 트윗

#거시경제 #경제 #ETF #주식시장
"""
    
    return report

def save_report(report):
    """Save report to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = DATA_DIR / f"economy_report_final_{timestamp}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)
    
    log(f"Report saved to {filename.name}")

def main():
    """Main execution flow"""
    log("=" * 50)
    log("🐦 X Economy Bot - START (Final Fixed Version)")
    log("=" * 50)
    
    try:
        # Step 1: Collect tweets from all following accounts
        log("Step 1: Following 트윗 수집 시작...")
        all_tweets = []
        
        for username in FOLLOWING_LIST:
            user_id = get_user_id(username)
            if user_id:
                tweets = get_user_tweets(username, user_id)
                if tweets:
                    all_tweets.extend(tweets)
                    log(f"  ✓ @{username}: {len(tweets)}개 트윗 수집")
                
                # Rate limit handling (Essential!)
                time.sleep(2)  # Delay to avoid rate limit
        
        log(f"Step 1 Complete: 총 트윗 수집: {len(all_tweets)}개")
        
        # Step 2: Filter economy related tweets
        log("Step 2: 경제 관련 트윗 필터링 중...")
        economy_tweets = filter_economy_tweets(all_tweets)
        log(f"Step 2 Complete: 경제 관련 트윗: {len(economy_tweets)}개")
        
        # Step 3: Generate report
        log("Step 3: 경제 브리핑 생성 중...")
        report = generate_economy_report(economy_tweets)
        
        # Step 4: Save report
        save_report(report)
        
        # Step 5: Output to console
        print("\n" + "=" * 50)
        print("📊 [ECONOMY REPORT OUTPUT]")
        print("=" * 50)
        print(report)
        print("=" * 50)
        
        log("✅ 실행 완료!")
        
    except Exception as e:
        log(f"CRITICAL ERROR: {e}", level="ERROR")
    
    log("=" * 50)
    log("🐦 X Economy Bot - END")
    log("=" * 50)

if __name__ == "__main__":
    main()
