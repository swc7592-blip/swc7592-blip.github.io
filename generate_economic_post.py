#!/usr/bin/env python3
"""
Economic News Post Generator
Fetches financial data using yfinance, creates summary tables, and generates a blog post.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

# Dynamic date configuration
today = datetime.now()
date_str = today.strftime('%Y-%m-%d')
year_month_str = today.strftime('%Y년 %m월')
POST_PATH = f"/Users/shin/.openclaw/workspace/swc7592-blip.github.io/_posts/{date_str}-economic-trends-analysis.md"

# Instruments to fetch
INSTRUMENTS = {
    # Stock Indices
    'sp500': {'ticker': '^GSPC', 'title': 'S&P 500', 'category': '주식지수', 'unit': '지수'},
    'nasdaq': {'ticker': '^IXIC', 'title': 'Nasdaq 100', 'category': '주식지수', 'unit': '지수'},
    'dowjones': {'ticker': '^DJI', 'title': 'Dow Jones', 'category': '주식지수', 'unit': '지수'},
    'kospi': {'ticker': '^KS11', 'title': 'KOSPI', 'category': '주식지수', 'unit': '지수'},

    # Interest Rates
    'treasury10': {'ticker': '^TNX', 'title': '2년 국채 금리', 'category': '금리', 'unit': '%'},
    'treasury30': {'ticker': '^TYX', 'title': '30년 국채 금리', 'category': '금리', 'unit': '%'},

    # Volatility
    'vix': {'ticker': '^VIX', 'title': 'VIX 지수', 'category': '변동성', 'unit': '지수'},

    # Currency / FX
    'usdkrw': {'ticker': 'USDKRW=X', 'title': 'USD/KRW', 'category': '환율', 'unit': '원'},
    'eurusd': {'ticker': 'EURUSD=X', 'title': 'EUR/USD', 'category': '환율', 'unit': 'USD'},
    'usdjpy': {'ticker': 'USDJPY=X', 'title': 'USD/JPY', 'category': '환율', 'unit': 'JPY'},

    # Cryptocurrencies
    'bitcoin': {'ticker': 'BTC-USD', 'title': '비트코인 (Bitcoin)', 'category': '크립토', 'unit': 'USD'},
    'ethereum': {'ticker': 'ETH-USD', 'title': '이더리움 (Ethereum)', 'category': '크립토', 'unit': 'USD'},
    'sol': {'ticker': 'SOL-USD', 'title': '솔라나 (SOL)', 'category': '크립토', 'unit': 'USD'},

    # Metals (금속)
    'gold': {'ticker': 'GC=F', 'title': '금 (Gold)', 'category': '금속', 'unit': 'USD/oz'},
    'silver': {'ticker': 'SI=F', 'title': '은 (Silver)', 'category': '금속', 'unit': 'USD/oz'},
    'copper': {'ticker': 'HG=F', 'title': '구리 (Copper)', 'category': '금속', 'unit': 'USD/pound'},
    'aluminum': {'ticker': 'ALI=F', 'title': '알루미늄 (Aluminum)', 'category': '금속', 'unit': 'USD/ton'},
    'platinum': {'ticker': 'PL=F', 'title': '백금 (Platinum)', 'category': '금속', 'unit': 'USD/oz'},

    # Raw Materials (원료)
    'wti': {'ticker': 'CL=F', 'title': 'WTI 원유 (WTI Crude)', 'category': '원료', 'unit': 'USD/배럴'},
    'brent': {'ticker': 'BZ=F', 'title': 'Brent 원유 (Brent Crude)', 'category': '원료', 'unit': 'USD/배럴'},
    'natural_gas': {'ticker': 'NG=F', 'title': '천연가스 (Natural Gas)', 'category': '원료', 'unit': 'USD/MMBtu'},
    'gasoline': {'ticker': 'RB=F', 'title': '휘발유 (RBOB Gasoline)', 'category': '원료', 'unit': 'USD/갤런'},
    'palladium': {'ticker': 'PA=F', 'title': '팔라듐 (Palladium)', 'category': '금속', 'unit': 'USD/oz'},

    # Agricultural Products (농산물)
    'wheat': {'ticker': 'ZW=F', 'title': '밀 (Wheat)', 'category': '농산물', 'unit': 'USD/bushel'},
    'corn': {'ticker': 'ZC=F', 'title': '옥수수 (Corn)', 'category': '농산물', 'unit': 'USD/bushel'},
    'soybeans': {'ticker': 'ZS=F', 'title': '대두 (Soybeans)', 'category': '농산물', 'unit': 'USD/bushel'},
    'coffee': {'ticker': 'KC=F', 'title': '커피 (Coffee)', 'category': '농산물', 'unit': 'USD/pound'}
}

def fetch_data():
    """Fetch data for all instruments over last 30 days."""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)  # Get more data to ensure we have 30 trading days

    print(f"Fetching data from {start_date.date()} to {end_date.date()}...")

    data = {}
    for key, info in INSTRUMENTS.items():
        print(f"  Fetching {info['title']} ({info['ticker']})...")
        try:
            df = yf.download(info['ticker'], start=start_date, end=end_date, progress=False)
            # Get the last 30 trading days (rows)
            df = df.tail(30)
            # Flatten MultiIndex columns
            df.columns = df.columns.get_level_values(0)
            data[key] = {
                'df': df,
                'info': info
            }
            print(f"    ✓ Fetched {len(df)} data points")
        except Exception as e:
            print(f"    ✗ Error fetching {info['title']}: {e}")
            data[key] = None

    return data

def analyze_data(data):
    """Analyze fetched data and generate insights."""
    analysis = {}

    for key, item in data.items():
        if item is None:
            continue

        df = item['df']
        info = item['info']

        # Get close/adj close column
        if 'Close' in df.columns:
            prices = df['Close']
        else:
            prices = df['Adj Close']

        # Calculate statistics
        start_price = prices.iloc[0]
        end_price = prices.iloc[-1]
        change = end_price - start_price
        change_pct = (change / start_price) * 100

        # Find min and max
        max_price = prices.max()
        min_price = prices.min()
        max_idx = prices.idxmax()
        min_idx = prices.idxmin()

        # Get date - it's the index itself
        max_date = pd.Timestamp(max_idx).strftime('%Y-%m-%d')
        min_date = pd.Timestamp(min_idx).strftime('%Y-%m-%d')

        analysis[key] = {
            'title': info['title'],
            'category': info['category'],
            'unit': info['unit'],
            'start_price': round(float(start_price), 2),
            'end_price': round(float(end_price), 2),
            'change': round(float(change), 2),
            'change_pct': round(float(change_pct), 2),
            'max_price': round(float(max_price), 2),
            'max_date': max_date,
            'min_price': round(float(min_price), 2),
            'min_date': min_date
        }

    return analysis

def create_summary_table(analysis):
    """Create a summary table of all instruments."""
    # Group by category
    categories = {
        '금속': [],
        '원료': [],
        '농산물': [],
        '주식지수': [],
        '크립토': [],
        '금리': [],
        '환율': [],
        '변동성': []
    }

    for key, item in analysis.items():
        category = item['category']
        if category in categories:
            categories[category].append(item)

    # Build tables for each category
    tables = {}
    for category, items in categories.items():
        if not items:
            continue

        # Sort by title
        items.sort(key=lambda x: x['title'])

        # Build markdown table
        table_lines = []
        table_lines.append(f"| 항목 | 현재 가격 | 시작 가격 | 변동 | 변동률 | 기간 중 최고 | 최고 날짜 | 기간 중 최저 | 최저 날짜 |")
        table_lines.append("|------|----------|----------|------|--------|------------|----------|------------|----------|")

        for item in items:
            trend = "📈" if item['change_pct'] > 0 else "📉"
            table_lines.append(
                f"| {item['title']} | "
                f"{item['end_price']} {item['unit']} | "
                f"{item['start_price']} {item['unit']} | "
                f"{item['change']:+.2f} {item['unit']} | "
                f"{trend} {item['change_pct']:+.2f}% | "
                f"{item['max_price']} {item['unit']} | "
                f"{item['max_date']} | "
                f"{item['min_price']} {item['unit']} | "
                f"{item['min_date']} |"
            )

        tables[category] = '\n'.join(table_lines)

    return tables

def generate_blog_post(tables, analysis):
    """Generate blog post with tables and analysis."""

    blog_post = f"""---
layout: post
title: "{year_month_str} 글로벌 경제 동향 분석: 금리 정책과 시장 트렌드"
date: {date_str} 06:00:00 +0900
categories: [economy, global-finance]
tags: [경제, 연준, 금리, 인플레이션, 주식, 금융, 금, 은, 백금, 구리, 알루미늄, WTI 원유, Brent 원유, 천연가스, 휘발유, 팔라듐, 밀, 옥수수, 대두, 커피, USD/KRW, EUR/USD, USD/JPY, Nasdaq, Dow Jones, VIX, 2년 국채, 30년 국채, 솔라나, 비트코인, 이더리움, KOSPI, S&P 500]
description: "{date_str} 글로벌 및 한국 경제 동향 분석 - 환율, 주식지수, 금리, 변동성, 금속, 원료, 농산물, 크립토 시장 트렌드"
---

## {year_month_str} 글로벌 경제 동향 분석: 금리 정책과 시장 트렌드

최근 30일간의 주요 금융 지수 데이터를 분석하여 {year_month_str} 현재 글로벌 및 한국 경제의 동향을 정리해 드립니다. 본 분석은 **yfinance** 데이터를 기반으로 하며, **금속**(금, 은, 백금, 구리, 알루미늄), **원료**(WTI 원유, Brent 원유, 천연가스, 휘발유), **농산물**(밀, 옥수수, 대두, 커피, 요소), **크립토**(비트코인, 이더리움), **주식 지수**(S&P 500, KOSPI), **금리**(10년 국채 금리) 등 주요 지표를 포괄적으로 다룹니다.

---

## 📊 주요 지수 요약표

"""

    # Add tables for each category
    for category in ['금속', '원료', '농산물', '환율', '변동성', '주식지수', '크립토', '금리']:
        if category in tables:
            blog_post += f"\n### {category}\n\n{tables[category]}\n\n"

    # Add summary and analysis
    blog_post += """---

## 🌍 경제 트렌드 요약

최근 30일간의 데이터를 바탕으로 주요 경제 동향을 요약합니다:

### 📈 상승한 항목

"""

    # List trending up items
    trending_up = [item for item in analysis.values() if item['change_pct'] > 0]
    trending_up.sort(key=lambda x: x['change_pct'], reverse=True)

    for item in trending_up[:5]:
        blog_post += f"- **{item['title']}**: +{item['change_pct']:.2f}% ({item['start_price']} → {item['end_price']} {item['unit']})\n"

    blog_post += "\n### 📉 하락한 항목\n\n"

    # List trending down items
    trending_down = [item for item in analysis.values() if item['change_pct'] < 0]
    trending_down.sort(key=lambda x: x['change_pct'])

    for item in trending_down[:5]:
        blog_post += f"- **{item['title']}**: {item['change_pct']:.2f}% ({item['start_price']} → {item['end_price']} {item['unit']})\n"

    blog_post += """
---

## 🎯 주요 시사점

### 투자자 관점

1. **자산 배분**: 전통 자산(주식, 채권, 금, 은)과 크립토 자산(비트코인, 이더리움) 간의 상관관계를 고려한 균형 잡힌 포트폴리오가 필요합니다.

2. **원자재 다각화**: 에너지(원유, 천연가스), 금속(금, 은, 구리, 알루미늄), 농산물(밀, 옥수수, 커피)에 대한 분석을 통해 인플레이션 헷지를 고려해야 합니다.

3. **리스크 관리**: 경제 불확실성이 높을 때는 안전자산(금, 은, 국채) 비중 확대를 고려해야 합니다.

4. **장기 관점**: 단기 변동성에 일희일비하지 않고 기본적인 경제 펀더멘털을 중심으로 투자 결정을 내려야 합니다.

### 정책 관점

1. **통화 정책**: 인플레이션 억제와 경제 성장 간의 균형이 중요합니다.

2. **거시 안정**: 금융 시장 안정을 위한 유연한 정책 대응이 필요합니다.

---

## 🔮 전망

향후 경제 상황은 다음 요인들의 영향을 받을 것으로 예상됩니다:

- 연준의 금리 정책 방향성
- 글로벌 인플레이션 추이
- 지정학적 리스크의 완화 여부
- 주요 경제국의 성장세

---

## 📌 결론

{year_month_str} 현재 글로벌 경제는 여전히 변동성이 높은 상황입니다. 위 표를 통해 주요 지수들의 움직임을 한눈에 파악할 수 있으며, 데이터 기반의 객관적 분석에 기초한 투자 및 경제 활동이 필요합니다.

본 포스트에서 제공하는 데이터와 표는 **yfinance**를 통해 수집된 실제 시장 데이터를 기반으로 하며, 지속적인 업데이트를 통해 최신 경제 동향을 파악하는 데 활용하실 수 있습니다.

---

*본 분석은 정보 제공 목적으로 작성되었으며, 투자 조언이 아닙니다. 투자 결정 시에는 반드시 전문가의 조언을 구하시기 바랍니다.*
"""

    # Write blog post
    with open(POST_PATH, 'w', encoding='utf-8') as f:
        f.write(blog_post)

    print(f"\n✓ Blog post saved: {POST_PATH}")

    return blog_post

def main():
    """Main execution function."""
    print("=" * 60)
    print("Economic News Post Generator")
    print("=" * 60)

    # Step 1: Fetch data
    print("\n[1/3] Fetching financial data...")
    data = fetch_data()

    # Step 2: Analyze data
    print("\n[2/3] Analyzing data...")
    analysis = analyze_data(data)

    # Step 3: Create summary tables
    print("\n[3/3] Creating summary tables...")
    tables = create_summary_table(analysis)

    # Step 4: Generate blog post
    print("\n[4/4] Generating blog post...")
    blog_post = generate_blog_post(tables, analysis)

    print("\n" + "=" * 60)
    print("✓ All tasks completed successfully!")
    print("=" * 60)

    # Print summary
    print("\n📋 Summary:")
    print(f"  - Blog post: {POST_PATH}")
    print(f"  - Data source: yfinance")
    print(f"  - Instruments analyzed: {len([d for d in data.values() if d is not None])}")
    print(f"  - Categories covered: {len(tables)}")

    return {
        'analysis': analysis,
        'tables': tables,
        'post_path': POST_PATH
    }

if __name__ == '__main__':
    result = main()
