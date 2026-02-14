#!/usr/bin/env python3
"""
X Economy Bot - Twitter API v2
Monitors all following accounts, collects tweets, analyzes economy trends, and reports to Discord
"""

import requests
import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
WORKSPACE = Path("/Users/shin/.openclaw/workspace/agents/x")
DATA_DIR = WORKSPACE / "data"
LOGS_DIR = WORKSPACE / "logs"
CONFIG_FILE = WORKSPACE / "config.json"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# X API Configuration
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN", "")
BASE_URL = "https://api.twitter.com/2"

# Following Accounts to Monitor
FOLLOWING_ACCOUNTS = [
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

# Economy Keywords (Korean and English)
ECONOMY_KEYWORDS = [
    "ETF", "Bitcoin", "Crypto", "Stocks", "Gold", "Inflation",
    "Market", "Economy", "Fed", "Rates", "Treasury", "S&P", "Dow",
    "금리", "인플레이션", "연준", "주식", "비트코인", "이더리움", "암호화폭",
    "거시경제", "투자", "마이크로", "시장", "경제", "밸류에이션", "디플레이션"
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
        "User-Agent": "v2EconomyBot/1.0"
    }

def get_user_id(username):
    """Get User ID from username"""
    headers = get_headers()
    if not headers:
        return None
    
    url = f"{BASE_URL}/users/by/username/{username}"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("data", {}).get("id")
        else:
            log(f"API Error getting user ID for {username}: {response.status_code}", level="ERROR")
            return None
    except Exception as e:
        log(f"Request Error getting user ID for {username}: {e}", level="ERROR")
        return None

def get_following_list(user_id, max_results=100):
    """Get list of following users (IDs)"""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{BASE_URL}/users/{user_id}/following"
    params = {
        "max_results": max_results,
        "user.fields": "id,username,name,public_metrics,description"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            return response.json().get("data", [])
        elif response.status_code == 429:
            log(f"Rate Limit Error getting following list: {response.status_code}", level="WARN")
            return []
        else:
            log(f"API Error getting following list: {response.status_code}", level="ERROR")
            return []
    except Exception as e:
        log(f"Request Error getting following list: {e}", level="ERROR")
        return []

def get_user_tweets(user_id, max_results=10):
    """Get recent tweets from a user"""
    headers = get_headers()
    if not headers:
        return []
    
    url = f"{BASE_URL}/users/{user_id}/timelines/reverse"
    params = {
        "max_results": max_results,
        "tweet.fields": "created_at,public_metrics,text,author_id",
        "expansions": "referenced_tweets.id,referenced_tweets.id.author_id"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        if response.status_code == 200:
            return response.json().get("data", [])
        elif response.status_code == 429:
            log(f"Rate Limit Error for user {user_id}", level="WARN")
            return []
        else:
            log(f"API Error getting tweets for {user_id}: {response.status_code}", level="ERROR")
            return []
    except Exception as e:
        log(f"Request Error getting tweets for {user_id}: {e}", level="ERROR")
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

def generate_economy_report(economy_tweets, following_users):
    """Generate economy report"""
    if not economy_tweets:
        return "경제 관련 트윗이 없습니다."
    
    timestamp = datetime.now().strftime("%Y년 %m월 %d일 %H:%M (KST)")
    
    report = f"""
【엑스 1시간 경제 브리핑】
📅 보고 시간: {timestamp}

【팔로워 핵심 트윗】
"""
    
    # Top 5 most engaging tweets (Simple Sort)
    sorted_tweets = sorted(economy_tweets, key=lambda x: x.get("public_metrics", {}).get("like_count", 0), reverse=True)
    top_tweets = sorted_tweets[:5]
    
    # Map user ID to username
    user_map = {u.get("id", ""): u.get("username", "unknown") for u in following_users}
    
    for i, tweet in enumerate(top_tweets, 1):
        user_id = tweet.get("author_id")
        username = user_map.get(user_id, "UnknownUser")
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
    
    # Keyword Analysis
    keyword_counts = {}
    for tweet in economy_tweets:
        text = tweet.get("text", "").lower()
        for keyword in ECONOMY_KEYWORDS:
            if keyword in text:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
    
    report += f"""

【시장 키워드 분석】
"""
    
    # Top 5 keywords
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for keyword, count in sorted_keywords:
        report += f"• {keyword}: {count}회 언급\n"
    
    report += f"""

【경제 인사이트】
• 기관 투자 동향: ETF 및 암호화폭 관련 트윗 분석
• 시장 방향성: 주요 경제 키워드 빈도 분석
• 리스크 관리: 변동성 및 정부 셧다운 등 리스크 요인 고려

【출처】
• X API (Twitter API v2)
• 팔로워 계정: {len(FOLLOWING_ACCOUNTS)}개

#거시경제 #경제 #ETF #비트코인 #시장분석
"""
    
    return report

def main():
    """Main execution flow"""
    log("=" * 50)
    log("🐦 X Economy Bot - START (API Mode)")
    log("=" * 50)
    
    try:
        # Step 1: Collect tweets from all following accounts
        log("Step 1: Collecting tweets from following accounts...")
        all_tweets = []
        
        for i, username in enumerate(FOLLOWING_ACCOUNTS, 1):
            user_id = get_user_id(username)
            if user_id:
                tweets = get_user_tweets(user_id)
                if tweets and "data" in tweets:
                    all_tweets.extend(tweets["data"])
                    log(f"  • Collected {len(tweets['data'])} tweets from @{username}")
                    
                    # Rate Limit handling
                    time.sleep(1)  # Delay to avoid rate limit
        
        log(f"Step 1 Complete: Total tweets collected: {len(all_tweets)}")
        
        # Step 2: Filter economy related tweets
        log("Step 2: Filtering for economy related tweets...")
        economy_tweets = filter_economy_tweets(all_tweets)
        log(f"Step 2 Complete: Economy related tweets: {len(economy_tweets)}")
        
        # Step 3: Generate report
        log("Step 3: Generating economy report...")
        
        # Create a dummy following_users map for this demo (normally fetched from API)
        following_users = [{"id": "dummy", "username": u} for u in FOLLOWING_ACCOUNTS]
        
        report = generate_economy_report(economy_tweets, following_users)
        
        # Step 4: Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = DATA_DIR / f"economy_report_api_{timestamp}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        
        log(f"Step 4 Complete: Report saved to {filename.name}")
        log(f"Content Preview:\n{report[:500]}...")
        
    except Exception as e:
        log(f"CRITICAL ERROR: {e}", level="ERROR")
    
    log("=" * 50)
    log("🐦 X Economy Bot - END")
    log("=" * 50)

if __name__ == "__main__":
    main()
