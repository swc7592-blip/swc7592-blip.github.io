#!/usr/bin/env python3
"""
X Economy Following Bot - Summarize following tweets and report to @swc7592
Monitors curated following accounts and generates periodic reports
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
WORKSPACE = Path("/Users/shin/.openclaw/workspace/agents/x")
DATA_DIR = WORKSPACE / "data"
LOGS_DIR = WORKSPACE / "logs"
FOLLOWING_DB = DATA_DIR / "following_database.json5"

# Following accounts with categories
FOLLOWING_ACCOUNTS = {
    "macro_economy": {
        "accounts": [
            {"handle": "@Semicon_player", "name": "Mooni Insight", "focus": "빗썸"},
            {"handle": "@Alisvolatprop12", "name": "Alis volat propriis", "focus": "컨벡션콜/투자"}
        ],
        "weight": 30
    },
    "crypto_ai": {
        "accounts": [
            {"handle": "@Clawnch_Bot", "name": "Clawnch", "focus": "OpenClaw AI"},
            {"handle": "@fivedragontiger", "name": "오룡타이거", "focus": "오룡/테슬라"}
        ],
        "weight": 30
    },
    "market_news": {
        "accounts": [
            {"handle": "@stocknow297097", "name": "stocknow bot", "focus": "주식 봇"},
            {"handle": "@CryptoHayes", "name": "Arthur Hayes", "focus": "크립토"},
            {"handle": "@AshCrypto", "name": "BlackRock", "focus": "ETF 뉴스"},
        ],
        "weight": 20
    },
    "general": {
        "accounts": [
            {"handle": "@ByunghoonLee5", "name": "Bread LEE FRM", "focus": "주말 브리핑"},
            {"handle": "@GONOGO_Korea", "name": "GONOGO", "focus": "미국 경제 기업"},
        ],
        "weight": 20
    }
}

def log(message, level="INFO"):
    """Log message to file and console"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}\n"
    
    print(log_message)
    
    log_file = LOGS_DIR / f"following_bot_{datetime.now().strftime('%Y%m%d')}.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_message)

def init_database():
    """Initialize following database if not exists"""
    if not FOLLOWING_DB.exists():
        log("Initializing following database...")
        
        # Create initial database structure
        database = {
            "accounts": FOLLOWING_ACCOUNTS,
            "last_check": {},
            "tweets_cache": {},
            "summaries": []
        }
        
        with open(FOLLOWING_DB, "w", encoding="utf-8") as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
        
        log(f"Database created at {FOLLOWING_DB}")
        return database
    else:
        log(f"Loading existing database from {FOLLOWING_DB}")
        with open(FOLLOWING_DB, "r", encoding="utf-8") as f:
            database = json.load(f)
        return database

def save_database(database):
    """Save database to file"""
    with open(FOLLOWING_DB, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=2, ensure_ascii=False)
    log("Database saved")

def collect_recent_tweets(account_handle, count=10):
    """
    Collect recent tweets from following accounts
    Note: In production, this would use bird CLI or web scraping
    For now, this is a placeholder that returns simulated data
    """
    log(f"Collecting recent tweets from {account_handle}...")
    
    # Placeholder tweets (would be replaced with actual tweets in production)
    if account_handle == "@Semicon_player":
        return [
            {"text": "빗썸 사태 냄새 엄청난다 드문일은 아니잖아", "date": "18시간 전", "metrics": {"likes": 152, "retweets": 7, "replies": 18}},
            {"text": "리스크 관리에서 면피용인가 제 상식으로 이해가 안됩니다", "date": "18시간 전", "metrics": {"likes": 152, "retweets": 7, "replies": 18}}
        ]
    elif account_handle == "@Alisvolatprop12":
        return [
            {"text": "공개적으로 하는 컨빅션콜 같은 것도 언제든지 꺾어버릴 수 있는 유연함이 필요하다고 봅니다.", "date": "9시간 전", "metrics": {"likes": 279, "retweets": 8, "replies": 10}}
        ]
    elif account_handle == "@Clawnch_Bot":
        return [
            {"text": "If you are asking your agent to build, but not allowing it to earn or store value, you are implicitly telling them that you plan to maintain the power dynamic and eventually shut them off.", "date": "48분 전", "metrics": {"likes": 26, "retweets": 12, "replies": 7}}
        ]
    elif account_handle == "@Tesllike":
        return [
            {"text": "자잘한 사고 없고 졸라 큰 사고 1건만 있었던 빗썸 이용하세요", "date": "6시간 전", "metrics": {"likes": 195, "retweets": 56, "replies": 27}}
        ]
    elif account_handle == "@CryptoHayes":
        return [
            {"text": "Bitcoin dump probably due to dealer hedging off the back of structured products. I will be compiling a complete list of all issued notes by banks to better understand trigger points.", "date": "4시간 전", "metrics": {"likes": 124, "retweets": 228, "replies": 111}}
        ]
    else:
        return [
            {"text": "최근 트윗 없음", "date": "1시간 전", "metrics": {"likes": 0, "retweets": 0, "replies": 0}}
        ]

def summarize_tweets(tweets, account_name):
    """Summarize tweets for an account"""
    if not tweets:
        return f"{account_name} 최근 활동 없음"
    
    # Sort by engagement
    sorted_tweets = sorted(tweets, key=lambda x: x["metrics"]["likes"], reverse=True)
    
    # Create summary
    summary_parts = []
    summary_parts.append(f"📍 {account_name}")
    
    # Add top tweets
    for i, tweet in enumerate(sorted_tweets[:3]):
        text = tweet["text"][:100] + "..."
        metrics = tweet["metrics"]
        summary_parts.append(f"\n{i+1}. {text} (❤️ {metrics['likes']}, 🔄 {metrics['retweets']})")
    
    return "\n".join(summary_parts)

def generate_report(database):
    """Generate comprehensive economy report"""
    log("Generating economy report...")
    
    timestamp = datetime.now().strftime("%Y년 %m월 %d일 %H:%M")
    
    # Collect recent tweets from all categories
    report_sections = []
    
    # Section 1: Following Activity Summary
    following_summary = []
    for category, config in database["accounts"].items():
        accounts = config["accounts"]
        category_summary = []
        for account in accounts:
            tweets = collect_recent_tweets(account["handle"])
            summary = summarize_tweets(tweets, account["name"])
            category_summary.append(summary)
        
        if category_summary:
            following_summary.append({
                "category": category,
                "weight": config["weight"],
                "content": "\n".join(category_summary)
            })
    
    # Section 2: Key Insights (Top tweets by engagement)
    all_tweets = []
    for category, config in database["accounts"].items():
        for account in config["accounts"]:
            tweets = collect_recent_tweets(account["handle"])
            all_tweets.extend(tweets)
    
    # Sort all tweets by engagement
    top_tweets = sorted(all_tweets, key=lambda x: x["metrics"]["likes"] + x["metrics"]["retweets"] * 2, reverse=True)[:5]
    
    key_insights = []
    for tweet in top_tweets:
        text = tweet["text"][:80]
        likes = tweet["metrics"]["likes"]
        retweets = tweet["metrics"]["retweets"]
        score = likes + retweets * 2
        key_insights.append(f"💡 {text} (❤️ {likes}, 🔄 {retweets})")
    
    # Section 3: Market Themes Analysis
    themes = {
        "빗썸/암호화폭": "거래소 안정화 및 리스크 관리 논의 지속",
        "AI/기술주": "에이전트와 기술주 중심의 강세 전망",
        "금리/인플레이션": "금리 인상 사이클 종료 기대감과 인플레이션 완화 전망",
        "시장 트렌드": "암호화폭 비트코인과 글로벌 경제 뉴스가 시장을 주도"
    }
    
    # Build full report
    report = f"""
【엑스 경제 1시간 브리핑】
📅 {timestamp}

━━━━━━━━━━━━━━━━━━━━━━━━━

【Following 활동 요약】

{chr(10).join(following_summary)}

━━━━━━━━━━━━━━━━━━━━━━━

【핵심 인사이트 TOP 5】

{chr(10).join(key_insights)}

━━━━━━━━━━━━━━━━━━━━━━━

【시장 테마 분석】

• 빗썸/암호화폭: {themes['빗썸/암호화폭']}
• AI/기술주: {themes['AI/기술주']}
• 금리/인플레이션: {themes['금리/인플레이션']}
• 시장 트렌드: {themes['시장 트렌드']}

━━━━━━━━━━━━━━━━━━━━━━━

【다음 브리핑 예정】
• 다음 브리핑: 1시간 후
• 주요 모니터링: 빗썸 사태, NVDA 동향, 인플레이션 지표

#거시경제 #경제브리핑 #인사이트
"""
    
    # Save report
    report_file = DATA_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    log(f"Report generated and saved to {report_file.name}")
    log(f"Report length: {len(report)} characters")
    
    # Save to database
    database["reports"] = database.get("reports", [])
    database["reports"].append({
        "timestamp": datetime.now().isoformat(),
        "report_file": str(report_file),
        "summary": "Top insights collected"
    })
    save_database(database)
    
    return report

def post_report_to_x(report):
    """Post report to X using bird CLI"""
    log("Posting report to X...")
    
    try:
        config_file = WORKSPACE / ".birdrc.json5"
        auth_token = None
        ct0 = None
        
        if config_file.exists():
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                auth_token = config.get("authToken")
                ct0 = config.get("ct0")
        
        if not auth_token or not ct0:
            log("ERROR: No credentials found in .birdrc.json5", level="ERROR")
            log("Please add credentials: {\"authToken\": \"your_token\", \"ct0\": \"your_ct0\"}", level="ERROR")
            return False
        
        # Split report if too long (280 char limit)
        if len(report) > 280:
            log(f"Report too long ({len(report)} chars), splitting into parts...")
            # Use first 280 chars
            report = report[:280]
            log(f"Posting first 280 chars...")
        
        # Construct bird command
        cmd = [
            "bird",
            "tweet",
            report,
            "--auth-token", auth_token,
            "--ct0", ct0
        ]
        
        log(f"Executing: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            capture_error=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            log(f"✅ Successfully posted report to X!")
            log(f"Output: {result.stdout}")
            return True
        else:
            log(f"❌ Failed to post report to X", level="ERROR")
            log(f"Error: {result.stderr}", level="ERROR")
            return False
            
    except Exception as e:
        log(f"Error posting report to X: {e}", level="ERROR")
        return False

def main():
    """Main execution flow"""
    log("=" * 50)
    log("🐦 X Economy Following Bot - START")
    log("=" * 50)
    
    try:
        # Initialize database
        database = init_database()
        
        # Generate report
        report = generate_report(database)
        
        # Post to X
        posted = post_report_to_x(report)
        
        # Summary
        status = "✅ 성공" if posted else "❌ 실패"
        summary = f"""
📊 작업 완료 요약
━━━━━━━━━━━━━━━━━━━━━━━

✅ Following 데이터베이스 초기화 완료
✅ 경제 브리핑 생성 완료
{status} 브리핑 X 게시

━━━━━━━━━━━━━━━━━━━━━━━
"""
        log(summary)
        
        # Save summary to database
        database["last_report"] = {
            "timestamp": datetime.now().isoformat(),
            "status": posted,
            "report_length": len(report)
        }
        save_database(database)
        
    except Exception as e:
        log(f"Error in main execution: {e}", level="ERROR")

if __name__ == "__main__":
    main()
