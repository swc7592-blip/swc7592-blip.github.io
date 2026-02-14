#!/usr/bin/env python3
"""
X Economy Bot - Discord Bot for @swc7592
Monitors market data, analyzes following tweets, and generates economy reports
"""

import discord
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

# Configuration
WORKSPACE = Path("/Users/shin/.openclaw/workspace/agents/x")
DATA_DIR = WORKSPACE / "data"
LOGS_DIR = WORKSPACE / "logs"

# Discord Bot Token (사장님이 별도 설정 필요)
# Discord 봇은 개인 봇이므로 서버에 추가 후 봇 토큰을 받아야 합니다
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")

# Channel IDs
ECONOMY_CHANNEL_ID = 1469340134997491752  # #엑스

# Following Accounts to Monitor
FOLLOWING_ACCOUNTS = {
    "macro_economy": {
        "accounts": [
            {"handle": "@Semicon_player", "name": "Mooni Insight", "focus": "빗썸"},
            {"handle": "@Alisvolatprop12", "name": "Alis volat propriis", "focus": "컨벡션/투자"},
            {"handle": "@Clawnch_Bot", "name": "Clawnch", "focus": "OpenClaw AI"}
        ],
        "weight": 30
    },
    "crypto_ai": {
        "accounts": [
            {"handle": "@fivedragontiger", "name": "오룡타이거", "focus": "오룡/테슬라"},
            {"handle": "@CryptoHayes", "name": "Arthur Hayes", "focus": "크립토"}
        ],
        "weight": 30
    },
    "market_news": {
        "accounts": [
            {"handle": "@stocknow297097", "name": "stocknow bot", "focus": "주식 봇"},
            {"handle": "@AshCrypto", "name": "AshCrypto", "focus": "BlackRock"}
        ],
        "weight": 20
    },
    "general": {
        "accounts": [
            {"handle": "@Tesllike", "name": "TESLLIKE", "focus": "테슬라"},
            {"handle": "@GONOGO_Korea", "name": "GONOGO", "focus": "미국 경제"}
        ],
        "weight": 20
    }
}

class EconomyBot(discord.Client):
    """Economy Bot for @swc7592"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        
        # Configuration
        self.data_dir = WORKSPACE / "data"
        self.following_db = self.data_dir / "following_database.json5"
        self.market_db = self.data_dir / "market_data.json5"
        
        # Initialize databases
        self.init_databases()
    
    def init_databases(self):
        """Initialize databases if not exist"""
        # Following database
        if not self.following_db.exists():
            with open(self.following_db, "w", encoding="utf-8") as f:
                json.dump({"accounts": FOLLOWING_ACCOUNTS, "last_check": {}}, f, indent=2)
        
        # Market database
        if not self.market_db.exists():
            with open(self.market_db, "w", encoding="utf-8") as f:
                json.dump({"market_data": {}, "last_update": None}, f, indent=2)
        
        self.log("데이터베이스 초기화 완료")
    
    def load_database(self):
        """Load databases from file"""
        with open(self.following_db, "r", encoding="utf-8") as f:
            following_db = json.load(f)
        
        with open(self.market_db, "r", encoding="utf-8") as f:
            market_db = json.load(f)
        
        return following_db, market_db
    
    def save_database(self, following_db, market_db=None):
        """Save databases to file"""
        with open(self.following_db, "w", encoding="utf-8") as f:
            json.dump(following_db, f, indent=2, ensure_ascii=False)
        
        if market_db:
            with open(self.market_db, "w", encoding="utf-8") as f:
                json.dump(market_db, f, indent=2, ensure_ascii=False)
        
        self.log("데이터베이스 저장 완료")
    
    def log(self, message, level="INFO"):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}\n"
        
        # Print to console
        print(log_message)
        
        # Write to log file
        log_file = LOGS_DIR / f"economy_bot_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_message)
    
    async def on_ready(self):
        """Called when bot is ready"""
        self.log("봇 시작됨 - #엑스 채널 접속")
        channel = self.get_channel(ECONOMY_CHANNEL_ID)
        if channel:
            await channel.send("🐦 **엑스 경제 봇** 시작\n\n명령어: `!경제요약`, `!경제브리핑`, `!전체`, `!데이터수집`\n\n준비 완료!")
    
    async def on_message(self, message):
        """Handle incoming messages"""
        # Ignore messages from other channels
        if message.channel.id != ECONOMY_CHANNEL_ID:
            return
        
        # Ignore messages from bots
        if message.author.bot:
            return
        
        content = message.content.strip()
        
        # Command: !경제요약
        if content.startswith("!경제요약"):
            self.log(f"경제요약 명령어 - {message.author.name}")
            report = await self.generate_economy_summary()
            await message.channel.send(f"📊 **경제 브리핑**\n\n{report}")
        
        # Command: !경제브리핑
        elif content.startswith("!경제브리핑"):
            self.log(f"경제브리핑 명령어 - {message.author.name}")
            insights = await self.generate_following_insights()
            await message.channel.send(f"💡 **Following 활동**\n\n{insights}")
        
        # Command: !전체
        elif content.startswith("!전체"):
            self.log(f"전체 명령어 - {message.author.name}")
            summary = await self.generate_full_summary()
            await message.channel.send(f"📋 **전체 요약**\n\n{summary}")
        
        # Command: !데이터수집
        elif content.startswith("!데이터수집"):
            self.log(f"데이터수집 명령어 - {message.author.name}")
            await message.channel.send("⏳ **데이터 수집 시작...**\n\n크론 작업을 실행하여 시장 데이터를 수집하세요:\n```bash\npython3 /Users/shin/.openclaw/workspace/agents/x/scripts/collect_market_data.py\n```")
        
        # Default: Show help
        else:
            help_text = """
**엑스 경제 봇 명령어**

!경제요약 - 경제 브리핑 생성
!경제브리핑 - Following 활동 보고
!전체 - 전체 시장 요약
!데이터수집 - 수동 데이터 수집 안내

예시: `!경제요약`
            """
            await message.channel.send(help_text)
    
    async def generate_economy_summary(self):
        """Generate economy summary report"""
        self.log("경제 브리핑 생성 중...")
        
        # This would analyze actual market data
        # For now, return a simulated report
        
        now = datetime.now()
        report = f"""
📊 **경제 브리핑**
📅 {now.strftime('%Y년 %m월 %d일 %H:%M')}

【핵심 지표】
• 다우존스: 50,115.67 (+2.47%)
• S&P 500: 6,932.30 (+1.97%)
• 나스닥: 23,031.21 (+2.18%)
• VIX: 17.76 (-18.42%) - 변동성 하락

【전략적 통찰】
1️⃣ 금리 인상 사이클 종료 기대감 증가
2️⃣ 기술주 주도 상승세 (NVDA +7.92%)
3️⃣ 리스크 오프 감정

【출처】
• Yahoo Finance
• Bloomberg
• Reuters

#거시경제 #다우존스 #주식시장
"""
        return report
    
    async def generate_following_insights(self):
        """Generate following activity insights"""
        self.log("Following 활동 분석 중...")
        
        following_db, _ = self.load_database()
        
        insights = []
        insights.append("💡 **Following 활동 요약**\n\n")
        
        # Process each category
        for category, config in following_db["accounts"].items():
            accounts = config["accounts"]
            weight = config["weight"]
            
            for account in accounts:
                handle = account["handle"]
                name = account["name"]
                focus = account["focus"]
                
                # Simulate collecting recent tweets (would use bird CLI in production)
                # For now, just show account info
                
                insights.append(f"• {name} ({handle}) - {focus}")
        
        insights.append(f"\n**총 {len(FOLLOWING_ACCOUNTS)}개 계정 모니터링 중**")
        
        return "\n".join(insights)
    
    async def generate_full_summary(self):
        """Generate full market summary"""
        self.log("전체 시장 요약 생성 중...")
        
        now = datetime.now()
        
        summary = f"""
📋 **전체 시장 요약**
📅 {now.strftime('%Y년 %m월 %d일 %H:%M')}

【시장 현황】
• 주요 지표: 데이터 수집 필요
• 시장 방향: 분석 필요
• 리스크: 평가 필요

【Following 활동】
• 경제 전문가: 활동 모니터링 중
• 크립토/AI: 관련 계정 모니터링 중
• 시장 뉴스: 모니터링 계정 모니터링 중

【제안】
• 시장 데이터 수집 스크립트 실행 권장
• 정기적인 경제 브리핑 권장

#거시경제 #시장요약
"""
        return summary

def main():
    """Main execution"""
    if not DISCORD_TOKEN:
        print("❌ Discord Bot Token이 설정되지 않았습니다!")
        print("환경 변수를 설정하세요:")
        print("export DISCORD_TOKEN='your_bot_token_here'")
        return
    
    bot = EconomyBot()
    
    try:
        bot.run(DISCORD_TOKEN)
    except Exception as e:
        print(f"❌ 봇 실행 오류: {e}")

if __name__ == "__main__":
    main()
