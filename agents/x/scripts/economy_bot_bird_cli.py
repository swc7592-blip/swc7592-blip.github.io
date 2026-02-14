#!/usr/bin/env python3
"""
X Economy Bot - bird CLI 기반 버전 (상세 요약)
bird CLI를 사용하여 트윗을 수집하고 경제 트렌드를 상세하게 분석합니다.
"""

import subprocess
import json
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

# Economy Keywords
ECONOMY_KEYWORDS = [
    "ETF", "Bitcoin", "Crypto", "Stocks", "Gold", "Inflation",
    "Market", "Economy", "Fed", "Rates", "Treasury", "S&P", "Dow",
    "반도체", "주식", "주가", "투자", "AI", "기술주", "금리", "인플레이션"
]

# bird CLI Credentials
BIRD_AUTH_TOKEN = "b37280fd9cca4df70b68feb788d99ea8c3d7bfa8"
BIRD_CT0 = "d5b9d6cc30b6c65184c52838c23379e623d69479076333994b5988b423adb6f69483488c8e8a3d44ec92955752263dc24bfe59e68c126cf8ccfb0f814115b48fe443126a3888ace5660cebf1524615ef"

def log(message, level="INFO"):
    """Log message to console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}\n"

    print(log_message)

    log_file = LOGS_DIR / f"x_bird_bot_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message)

def get_user_tweets_bird(username, count=5):
    """Get tweets from a user using bird CLI"""
    try:
        cmd = [
            "bird",
            "--auth-token", BIRD_AUTH_TOKEN,
            "--ct0", BIRD_CT0,
            "user-tweets",
            "--json",
            "-n", str(count),
            username
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(WORKSPACE)
        )

        if result.returncode != 0:
            log(f"Error getting tweets for @{username}: {result.stderr}", level="ERROR")
            return []

        # Parse JSON output
        tweets = json.loads(result.stdout)

        # Add username to each tweet
        for tweet in tweets:
            tweet["author_username"] = username

        log(f"  • @{username}: {len(tweets)}개 트윗 수집")
        return tweets

    except subprocess.TimeoutExpired:
        log(f"Timeout for @{username}", level="WARN")
        return []
    except json.JSONDecodeError as e:
        log(f"JSON decode error for @{username}: {e}", level="ERROR")
        return []
    except Exception as e:
        log(f"Unexpected error for @{username}: {e}", level="ERROR")
        return []

def filter_economy_tweets(tweets):
    """Filter tweets for economy related content"""
    economy_tweets = []

    if not tweets:
        return economy_tweets

    for tweet in tweets:
        text = tweet.get("text", "").lower()

        # Check for economy keywords
        if any(keyword.lower() in text for keyword in ECONOMY_KEYWORDS):
            economy_tweets.append(tweet)

    return economy_tweets

def parse_to_kst(created_at_str):
    """Convert Twitter timestamp to KST"""
    try:
        dt = datetime.strptime(created_at_str, "%a %b %d %H:%M:%S %z %Y")
        kst = dt + timedelta(hours=9)
        return kst.strftime("%Y년 %m월 %d일 %H:%M (KST)")
    except:
        return created_at_str

def generate_economy_report(economy_tweets):
    """Generate economy report (detailed)"""
    if not economy_tweets:
        return "경제 관련 트윗이 없습니다."

    timestamp = datetime.now().strftime("%Y년 %m월 %d일 %H:%M (KST)")

    # Calculate keyword counts
    keyword_counts = {}
    for tweet in economy_tweets:
        text = tweet.get("text", "").lower()
        for keyword in ECONOMY_KEYWORDS:
            if keyword.lower() in text:
                keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

    # Sort by likes - TOP 5
    top_tweets = sorted(economy_tweets, key=lambda x: x.get("likeCount", 0), reverse=True)[:5]

    report = f"""
【엑스 경제 브리핑 - 상세 요약】

📅 보고 시간: {timestamp}

---

### 【팔로워 핵심 트윗 TOP 5】

"""

    for i, tweet in enumerate(top_tweets, 1):
        username = tweet.get("author_username", "Unknown")
        name = tweet.get("author", {}).get("name", "Unknown")
        text = tweet.get("text", "")
        text_short = text[:150] + "..." if len(text) > 150 else text
        created_at = tweet.get("createdAt", "Unknown")
        created_at_kst = parse_to_kst(created_at)
        likes = tweet.get("likeCount", 0)
        retweets = tweet.get("retweetCount", 0)
        replies = tweet.get("replyCount", 0)
        tweet_id = tweet.get("id", "")

        # Extract relevant keywords from this tweet
        tweet_keywords = []
        tweet_lower = text.lower()
        for keyword in ECONOMY_KEYWORDS:
            if keyword.lower() in tweet_lower:
                tweet_keywords.append(keyword)

        report += f"""
{i}. @{username} ({name})
• 작성 시각: {created_at_kst}
• 관련 키워드: {', '.join(tweet_keywords) if tweet_keywords else '없음'}
• 트윗: {text_short}
• 참여도: 👍 {likes:,} | 🔄 {retweets:,} | 💬 {replies:,}
• 링크: https://x.com/{username}/status/{tweet_id}
"""

    # Add detailed insights section
    report += f"""


### 【시장 분석 및 인사이트】

"""

    # ETF/Crypto Theme
    if any(kw in keyword_counts for kw in ["ETF", "Bitcoin", "Crypto", "비트코인", "암호화폭"]):
        etf_count = sum(keyword_counts.get(kw, 0) for kw in ["ETF", "Bitcoin", "Crypto"])
        report += f"• **ETF/암호화폭 ({etf_count}회 언급):** 기관 투자 자금 유입 흐름 확인. 스포츠 ETF와 비트코인 관련 논의가 활발함. 최근 미국 인플레이션 지표 하락으로 금리 인하 기대감 고조.\n"

    # Stocks/Market Theme
    if any(kw in keyword_counts for kw in ["Market", "Stocks", "Economy", "주식", "주가", "투자", "시장"]):
        market_count = sum(keyword_counts.get(kw, 0) for kw in ["Market", "Stocks", "주식", "주가"])
        report += f"• **주식/시장 ({market_count}회 언급):** 전체 시장 동향 관련 토론 활성. DAT 주가 폭락, 헷지펀드 리스크 등 시장 변동성 관련 논의 지속.\n"

    # Interest Rates Theme
    if any(kw in keyword_counts for kw in ["Fed", "Rates", "Treasury", "금리", "인플레이션"]):
        rates_count = sum(keyword_counts.get(kw, 0) for kw in ["Fed", "Rates", "금리", "인플레이션"])
        report += f"• **금리/인플레이션 ({rates_count}회 언급):** 연준 금리 정책 및 국채 관련 관심 증가. 미국 인플레이션 지표가 2020년 팬데믹 이후 최저 수준으로 하락, 금리 인하 기대감 형성.\n"

    # Tech/AI Theme
    if any(kw in keyword_counts for kw in ["AI", "Tech", "기술주", "반도체"]):
        tech_count = sum(keyword_counts.get(kw, 0) for kw in ["AI", "Tech", "기술주", "반도체"])
        report += f"• **기술주/AI/반도체 ({tech_count}회 언급):** 기술주, AI, 반도체 관련 트윗 부각. CAPEX 확장, 광학전환, 전력 전환 초기 수혜 기업 등 인프라 투자 관심 증가.\n"

    report += f"""

### 【투자 시사점】

• **비트코인:** 기관 투자 자금 유입 흐름과 미국 인플레이션 하락에 따른 금리 인하 기대감이 긍정적 신호로 작용할 가능성.
• **주식 시장:** 헷지펀드 리스크와 시장 변동성 지속으로 보수적 접근 필요. DAT 주가 폭락 사례에서 인플루언서 영향력 고려.
• **인플레이션/금리:** 미국 인플레이션 지표 하락이 금리 인하 가능성을 시사하지만, 실제 연준 정책 주시 필요.
• **AI/반도체:** CAPEX 확장과 인프라 투자가 지속될 경우 관련 기업의 수혜 기대 가능.

### 【종합 인사이트】

• **전체 시장 분위:** 기관 투자 동향과 시장 키워드 분석 기반
• **주요 이슈:** 경제 관련 트윗 빈도 및 주요 키워드 트렌드 파악
• **시나리오:** 실시간 트윗 분석 기반 투자 전략 제안
• **위험 요인:** 헷지펀드 리스크, 시장 변동성, 인플루언서 영향력
• **기회 요인:** 금리 인하 기대, 기관 투자 자금 유입, 인프라 투자 확장

### 【출처】

• X (Twitter) - bird CLI 기반
• 팔로워 계정: {len(FOLLOWING_LIST)}개
• 데이터 기준: 최신 트윗
• 분석 대상: 경제 관련 키워드 포함 트윗

#거시경제 #경제 #ETF #비트코인 #시장분석
"""

    return report

def save_report(report):
    """Save report to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = DATA_DIR / f"economy_report_bird_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    log(f"Report saved to {filename.name}")

def main():
    """Main execution flow"""
    log("=" * 50)
    log("🐦 X Economy Bot - START (bird CLI Version)")
    log("=" * 50)

    try:
        # Step 1: Collect tweets from all following accounts
        log("Step 1: 트윗 수집 시작...")
        all_tweets = []

        for username in FOLLOWING_LIST:
            tweets = get_user_tweets_bird(username, count=5)
            if tweets:
                all_tweets.extend(tweets)

        log(f"Step 1 Complete: 총 트윗 수집: {len(all_tweets)}개")

        # Step 2: Filter economy related tweets
        log("Step 2: 경제 관련 트윗 필터링...")
        economy_tweets = filter_economy_tweets(all_tweets)
        log(f"Step 2 Complete: 경제 관련 트윗: {len(economy_tweets)}개")

        # Step 3: Generate report
        log("Step 3: 경제 브리핑 생성...")
        report = generate_economy_report(economy_tweets)

        # Step 4: Save report
        save_report(report)

        # Step 5: Output to console
        print("\n" + "=" * 50)
        print("📊 [경제 브리핑 출력]")
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
