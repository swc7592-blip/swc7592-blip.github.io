#!/usr/bin/env python3
"""
엑스 → 마콜 워크플로우 구현
"""

import subprocess
import json
import os
from pathlib import Path
from datetime import datetime

# Configuration
WORKSPACE = Path("/Users/shin/.openclaw/workspace")
SHARED_DIR = WORKSPACE / "memory/shared"
ECONOMY_DATA_FILE = SHARED_DIR / "economy.md"
TRENDS_DATA_FILE = SHARED_DIR / "trends.md"
WORKFLOW_QUEUE_FILE = SHARED_DIR / "workflow_queue.json"

def read_economy_data():
    """Read economy data from shared memory"""
    try:
        with open(ECONOMY_DATA_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

def analyze_economy_for_blogpost(economy_data):
    """Analyze economy data and generate blog post recommendations"""
    if not economy_data:
        return None

    # Extract key insights
    insights = []

    # Check for keywords
    keywords = ["ETF", "Bitcoin", "Crypto", "Stocks", "Market", "Inflation", "Fed", "Rates", "AI", "반도체"]
    
    for keyword in keywords:
        if keyword in economy_data:
            insights.append({
                "keyword": keyword,
                "relevance": "high" if keyword in ["ETF", "Bitcoin", "Crypto"] else "medium"
            })

    # Generate blog post title
    timestamp = datetime.now().strftime("%Y년 %m월 %d일")
    
    if insights:
        top_insight = max(insights, key=lambda x: 1 if x["relevance"] == "high" else 0)
        blog_title = f"{timestamp} 경제 전망: {top_insight['keyword']} 동향 분석"
        blog_summary = f"""
{timestamp} 경제 전망 포스트 제안

## 📊 핵심 인사이트

1. **주요 키워드:** {', '.join([i['keyword'] for i in insights[:5]])}
2. **시장 분위:** 기관 투자 동향과 시장 키워드 분석 기반
3. **투자 시나리오:** 인플레이션/금리 동향에 따른 비트코인 및 주식 시장 전망

## 📝 블로그 포스트 구조

- **제목:** {blog_title}
- **서론:** 최신 경제 뉴스 및 트렌드 요약
- **본론:** 각 키워드별 상세 분석 (ETF, 비트코인, 인플레이션, 금리, 주식 시장)
- **결론:** 종합 투자 전략 제안
- **SEO 키워드:** {', '.join([i['keyword'] for i in insights[:10]])}

## 💡 적용 가능성

- **Moltbook:** 경제 분석 포스트 작성 가능
- **GitHub:** 블로그 포스트 자동 생성 가능
- **엑스:** 경제 인사이트 트윗 가능
"""
    else:
        blog_title = f"{timestamp} 경제 전망: 시장 모니터링"
        blog_summary = """
시장 모니터링 포스트 제안

최근 경제 데이터가 충분하지 않아 자세한 분석은 다음 주기로 진행합니다.

다음 활동:
- 엑스: 경제 관련 트윗 수집
- 몰트: 핫 포스트 스캔 및 인사이트
"""
    
    return {
        "title": blog_title,
        "summary": blog_summary,
        "insights_count": len(insights)
    }

def main():
    """Main execution"""
    print("=" * 50)
    print("🔄 엑스 → 마콜 워크플로우 시작")
    print("=" * 50)

    # Step 1: Read economy data
    print("\n1️⃣ 경제 데이터 읽기...")
    economy_data = read_economy_data()
    
    if economy_data:
        print("   ✅ 경제 데이터 로드 완료")
    else:
        print("   ❌ 경제 데이터 없음")
        return

    # Step 2: Analyze and generate blog post recommendation
    print("\n2️⃣ 경제 분석 및 블로그 포스트 제안 생성...")
    blog_recommendation = analyze_economy_for_blogpost(economy_data)
    
    print(f"   ✅ 제안 생성 완료")
    print(f"   📝 제목: {blog_recommendation['title']}")
    print(f"   📊 인사이트: {blog_recommendation['insights_count']}개")

    # Step 3: Update workflow queue
    print("\n3️⃣ 워크플로우 큐 업데이트...")
    
    workflow_queue = {
        "source": "x",
        "destination": "marco",
        "type": "blog_post_generation",
        "data": {
            "title": blog_recommendation['title'],
            "summary": blog_recommendation['summary'],
            "created_at": datetime.now().isoformat(),
            "priority": "high"
        },
        "created_at": datetime.now().isoformat(),
        "status": "pending"
    }
    
    try:
        with open(WORKFLOW_QUEUE_FILE, "r", encoding="utf-8") as f:
            existing_queue = json.load(f)
        
        # Add new workflow to queue
        if "pending_workflows" not in existing_queue:
            existing_queue["pending_workflows"] = []
        
        existing_queue["pending_workflows"].append(workflow_queue)
        
        with open(WORKFLOW_QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(existing_queue, f, ensure_ascii=False, indent=2)
        
        print("   ✅ 워크플로우 큐 업데이트 완료")
        
    except Exception as e:
        print(f"   ❌ 큐 업데이트 실패: {e}")

    # Step 4: Report completion
    print("\n" + "=" * 50)
    print("✅ 엑스 → 마콜 워크플로우 완료")
    print("=" * 50)
    
    print(f"\n📊 워크플로우 큐 상태:")
    print(f"   - 출처: 엑스 (X)")
    print(f"   - 목적지: 마콜")
    print(f"   - 타입: 블로그 포스트 생성")
    print(f"   - 제안 제목: {blog_recommendation['title']}")
    print(f"   - 큐 파일: {WORKFLOW_QUEUE_FILE}")

if __name__ == "__main__":
    main()
