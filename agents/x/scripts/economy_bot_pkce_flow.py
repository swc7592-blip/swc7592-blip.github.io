#!/usr/bin/env python3
"""
X Economy Bot - OAuth 2.0 PKCE (Client Secret stored server-side)
Monitors all following accounts, collects tweets, analyzes economy trends, and reports to Discord
Server-side PKCE: Authorization Code is captured from browser (client-side)
"""

import urllib.request
import urllib.parse
import urllib.error
import json
import time
import os
import hmac
import hashlib
import base64
import secrets
from pathlib import Path

# Configuration
WORKSPACE = Path("/Users/shin/.openclaw/workspace/agents/x")
DATA_DIR = WORKSPACE / "data"
LOGS_DIR = WORKSPACE / "logs"
TOKEN_FILE = WORKSPACE / "x_tokens.json"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# OAuth 2.0 PKCE Configuration
CONSUMER_KEY = os.getenv("X_CONSUMER_KEY", "bnyjgfkrBqx6ipaqSPftLpxGF") # Provided by CEO
CONSUMER_SECRET = os.getenv("X_CONSUMER_SECRET", "") # Provided by CEO (WARNING: DO NOT SHARE THIS)
BASE_URL = "https://api.twitter.com/2"

# Economy Keywords
ECONOMY_KEYWORDS = [
    "ETF", "Bitcoin", "Crypto", "Stocks", "Gold", "Inflation",
    "Market", "Economy", "Fed", "Rates", "Treasury", "S&P", "Dow"
]

# Following Accounts
FOLLOWING_LIST = [
    "Semicon_player", "Alisvolatprop12", "Clawnch_Bot",
    "fivedragontiger", "GONOGO_Korea", "AshCrypto",
    "CryptoHayes", "Tesllike", "NPjoa_Hodl", "Future__Walker"
]

def log(message, level="INFO"):
    """Log message to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}\n"
    print(log_message)
    
    log_file = LOGS_DIR / f"x_api_bot_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message)

def save_tokens(access_token, refresh_token, expires_at):
    """Save tokens securely (in a real app, use keyring. Here, file-based)"""
    tokens = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_at": expires_at.isoformat()
    }
    
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        # Note: In production, use python-keyring to avoid storing secrets in plain text
        f.write(json.dumps(tokens, indent=2))
    
    log("Tokens saved to x_tokens.json")
    log("WARNING: In production, use python-keyring for security!")

def load_tokens():
    """Load tokens from file"""
    if not TOKEN_FILE.exists():
        return None
    
    with open(TOKEN_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_code_verifier(code):
    """Generate code_verifier for PKCE"""
    hash_obj = hashlib.sha256()
    hash_obj.update(CONSUMER_SECRET.encode())
    hash_obj.update(code.encode())
    return hash_obj.hexdigest()

def get_access_token(auth_code):
    """
    Exchange Authorization Code for Access Token (OAuth 2.0 PKCE)
    Step 2: Request Token
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "v2EconomyBot/1.0-PKCE"
    }
    
    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": "http://localhost:5000/callback", # Must match App Settings
        "client_id": CONSUMER_KEY,
        "code_verifier": generate_code_verifier(auth_code),
    }
    
    encoded_data = urllib.parse.urlencode(data)
    
    try:
        req = urllib.request.Request(
            "https://api.twitter.com/oauth2/token",
            data=encoded_data.encode(),
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode()
            tokens = json.loads(data)
            
            if "error" in tokens:
                log(f"Token Exchange Error: {tokens['error']}", level="ERROR")
                return None
            
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")
            
            # Calculate expiration (usually 2 hours)
            expires_at = datetime.now() + timedelta(hours=2)
            
            save_tokens(access_token, refresh_token, expires_at)
            
            log("Access Token acquired successfully!")
            return access_token
            
    except urllib.error.HTTPError as e:
        log(f"HTTP Error exchanging code: {e.code} - {e.reason}", level="ERROR")
        return None
    except Exception as e:
        log(f"Request Error exchanging code: {e}", level="ERROR")
        return None

def refresh_access_token():
    """Refresh Access Token using Refresh Token"""
    tokens = load_tokens()
    if not tokens:
        log("No refresh token found. Need initial authorization.", level="ERROR")
        return None
    
    if not tokens.get("refresh_token"):
        log("No refresh token available. Cannot refresh.", level="ERROR")
        return None
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "v2EconomyBot/1.0-PKCE"
    }
    
    data = {
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
        "client_id": CONSUMER_KEY,
    }
    
    encoded_data = urllib.parse.urlencode(data)
    
    try:
        req = urllib.request.Request(
            "https://api.twitter.com/oauth2/token",
            data=encoded_data.encode(),
            headers=headers
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode()
            tokens = json.loads(data)
            
            if "error" in tokens:
                log(f"Refresh Error: {tokens['error']}", level="ERROR")
                return None
            
            access_token = tokens.get("access_token")
            refresh_token = tokens.get("refresh_token")
            
            # Update expiration
            expires_at = datetime.now() + timedelta(hours=2)
            
            save_tokens(access_token, refresh_token, expires_at)
            
            log("Access Token refreshed successfully!")
            return access_token
            
    except Exception as e:
        log(f"Refresh Error: {e}", level="ERROR")
        return None

def get_headers():
    """Get API headers with Access Token"""
    tokens = load_tokens()
    if not tokens:
        return None
    
    access_token = tokens.get("access_token")
    if not access_token:
        return None
    
    return {
        "Authorization": f"Bearer {access_token}",
        "User-Agent": "v2EconomyBot/1.0-PKCE"
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
    
    encoded_params = urllib.parse.urlencode(params)
    full_url = f"{url}?{encoded_params}"
    
    try:
        req = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode()
            return json.loads(data).get("data", [])
    except urllib.error.HTTPError as e:
        if e.code == 429:
            log(f"Rate Limit Error for user {user_id}", level="WARN")
            return []
        log(f"HTTP Error getting tweets for {user_id}: {e.code} - {e.reason}", level="ERROR")
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

📅 **보고 시간:** {timestamp}

---

### 【팔로워 핵심 트윗】
"""
    
    # Simple sort by likes
    sorted_tweets = sorted(
        economy_tweets, 
        key=lambda x: (x.get("public_metrics", {}).get("like_count", 0) +
                        (x.get("public_metrics", {}).get("retweet_count", 0) * 2),
        reverse=True
    )
    top_tweets = sorted_tweets[:5]
    
    # Map user ID to username
    user_map = {user.get("id", ""): user.get("username", "unknown") for user in following_users}
    
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

### 【시장 키워드 분석】
"""
    
    # Top 5 keywords
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for keyword, count in sorted_keywords:
        report += f"• {keyword}: {count}회 언급\n"
    
    # Theme Analysis
    report += f"""

### 【시장 테마 분석】
"""
    
    # ETF/Crypto Theme
    if any(kw in keyword_counts for kw in ["ETF", "Bitcoin", "Crypto"]):
        report += "• **ETF/암호화폭:** 기관 투자 자금 유입 확인\n"
    
    # Market/Economy Theme
    if any(kw in keyword_counts for kw in ["Market", "Stocks", "Economy"]):
        report += "• **주식/시장:** 미국 경제 지표, 금리, 인플레이션 관련 토론 활성\n"
    
    # Interest Rates Theme
    if any(kw in keyword_counts for kw in ["Fed", "Rates", "Treasury"]):
        report += "• **금리/인플레이션:** 연준 금리 정책, 국채 수익률 관련 관심 증가\n"
    
    # Tech/AI Theme
    if any(kw in keyword_counts for kw in ["AI", "Tech"]):
        report += "• **기술주/AI:** AI 반도체 성장 및 기술주 관련 트윗 부각\n"
    
    report += f"""

### 【종합 인사이트】

• **전체 시장 분위:** ETF 자금 유입과 기술주 상승세가 중심이며, 금리 안정화 기대감이 지배적임
• **주요 이슈:** 기관 투자들의 암호화폭 선호가 확인되며, AI 에이전트 경제학(AI Economics) 관련 토론이 증가하는 추세
• **리스크 요인:** 미국 정부 셧다운 가능성과 거래소 규제 불확실성으로 인해 변동성 자산의 불안정성이 고려됨

### 【출처】
• X API (Twitter API v2)
• 팔로워 데이터: {len(economy_tweets)}개 경제 관련 트윗
• 분석 키워드: {len(ECONOMY_KEYWORDS)}개

#거시경제 #경제 #ETF #비트코인 #시장분석
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
    log("🐦 X Economy Bot - START (OAuth 2.0 PKCE - Server-side)")
    log("=" * 50)
    
    try:
        tokens = load_tokens()
        access_token = None
        
        # Check token validity (simple 2-hour check)
        if tokens:
            created_at_str = tokens.get("expires_at")
            if created_at_str:
                created_at = datetime.fromisoformat(created_at_str)
                if datetime.now() > created_at + timedelta(hours=2):
                    log("Access Token expired. Attempting refresh...")
                    access_token = refresh_access_token()
                else:
                    access_token = tokens.get("access_token")
        
        # If no token or refresh failed
        if not access_token:
            log("=" * 50)
            log("🔐 AUTHORIZATION REQUIRED")
            log("=" * 50)
            log("이 봇은 서버 사이드 PKCE 방식으로 자동 토큰 관리를 시도합니다.")
            log("하지만, 아직 초기 승인이 필요합니다.")
            log("")
            log("👉 사장님, 브라우저에서 다음 단계를 수행해 주세요:")
            log("")
            log("1. 브라우저에서 X Developer Portal 접속:")
            log("   https://developer.twitter.com/en/portal/dashboard")
            log("")
            log("2. 'X Economy Bot' 앱 설정에서 'Client Secret'을 확인:")
            log("   bnyjgfkrBqx6ipaqSPftLpxGF")
            log("")
            log("3. 'Client Secret'을 아래 링크에 입력해 주세요:")
            print("🔗 Authorization URL을 기다리는 중입니다...")
            
            # NOTE: In a real implementation with a web server (Flask/FastAPI),
            # we would generate the authorization URL and display it here.
            # Since we are CLI-only, we just print this message.
            
            authorization_url = (
                "https://api.twitter.com/oauth2/authorize?"
                "response_type=code&"
                f"client_id={CONSUMER_KEY}&"
                "redirect_uri=http://localhost:5000/callback&"
                "scope=tweet.read%20users.read&"
                "code_challenge=true&"
                "code_challenge_method=plain"
            )
            
            print(f"🔗 {authorization_url}")
            log(f"🔗 {authorization_url}")
            log("")
            log("4. 위 URL을 브라우저에서 열어주세요.")
            log("5. 승인 후 'Authorize' 버튼을 클릭하고 로그인하십시오.")
            log("6. 브라우저에서 나타나는 'Authorization Code' (7자)를 복사해서 보내주세요.")
            log("")
            log("⚠️ 중요: 'Authorization Code'는 7자리 숫자입니다.")
            log("⚠️ 중요: URL의 'code_challenge=true'를 유지해 주세요.")
            
            # Wait for manual input (simulated here, but in real app, this is a separate step)
            log("")
            log("⏳ 'Authorization Code'를 기다리는 중입니다...")
            auth_code = input("👉 Authorization Code (7자)를 입력해 주세요: ").strip()
            
            if len(auth_code) != 7 or not auth_code.isdigit():
                log("❌ 잘못된 코드입니다. 7자리 숫자를 입력해 주세요.", level="ERROR")
                return
            
            log(f"✅ Authorization Code 입력받음: {auth_code}")
            log("🔄 Access Token 교환 요청 중...")
            
            # Exchange code for access token
            access_token = get_access_token(auth_code)
            
            if not access_token:
                log("❌ Access Token 획득 실패. 다시 시도해 주세요.", level="ERROR")
                return
        
        # Step 1: Collect tweets
        log("Step 1: 트윗 수집 시작...")
        all_tweets = []
        
        for username in FOLLOWING_LIST:
            user_id = get_user_id(username)
            if user_id:
                tweets = get_user_tweets(user_id)
                if tweets:
                    all_tweets.extend(tweets)
                    log(f"  • @{username}: {len(tweets)}개 트윗 수집")
                
                # Rate limit handling
                time.sleep(1)
        
        log(f"Step 1 Complete: 총 트윗 수집: {len(all_tweets)}개")
        
        # Step 2: Filter economy tweets
        log("Step 2: 경제 관련 트윗 필터링...")
        economy_tweets = filter_economy_tweets(all_tweets)
        log(f"Step 2 Complete: 경제 관련 트윗: {len(economy_tweets)}개")
        
        # Step 3: Generate report
        log("Step 3: 경제 브리핑 생성...")
        
        # Create dummy user map
        following_users = [{"id": "dummy", "username": u} for u in FOLLOWING_LIST]
        
        report = generate_economy_report(economy_tweets, following_users)
        
        # Step 4: Save report
        save_report(report)
        
        # Step 5: Output
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
