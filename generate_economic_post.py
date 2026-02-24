#!/usr/bin/env python3
"""
Economic News Post Generator
Fetches financial data using yfinance, creates charts, and generates a blog post.
"""

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime, timedelta
import os
import json

# Set up Korean font for matplotlib
plt.rcParams['font.sans-serif'] = ['AppleGothic', 'Malgun Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Configuration
OUTPUT_DIR = "/Users/shin/.openclaw/workspace/swc7592-blip.github.io/assets/images/2026-02-25"
POST_PATH = "/Users/shin/.openclaw/workspace/swc7592-blip.github.io/_posts/2026-02-25-economic-trends-analysis.md"

# Instruments to fetch
INSTRUMENTS = {
    'gold': {'ticker': 'GC=F', 'title': '금 가격', 'filename': 'gold_price_chart.png', 'ylabel': '가격 (USD/oz)'},
    'sp500': {'ticker': '^GSPC', 'title': 'S&P 500', 'filename': 'sp500_chart.png', 'ylabel': '지수'},
    'kospi': {'ticker': '^KS11', 'title': 'KOSPI', 'filename': 'kospi_chart.png', 'ylabel': '지수'},
    'oil': {'ticker': 'CL=F', 'title': '원유 가격', 'filename': 'oil_price_chart.png', 'ylabel': '가격 (USD/배럴)'},
    'treasury': {'ticker': '^TNX', 'title': '10년 국채 금리', 'filename': 'treasury_rate_chart.png', 'ylabel': '금리 (%)'}
}

def create_output_directory():
    """Create the output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")

def fetch_data():
    """Fetch data for all instruments over the last 30 days."""
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

def create_chart(data):
    """Create and save charts for each instrument."""
    chart_files = {}
    
    for key, item in data.items():
        if item is None:
            continue
        
        df = item['df']
        info = item['info']
        
        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot data
        if 'Close' in df.columns:
            ax.plot(df.index, df['Close'], linewidth=2, color='#2563eb', label='종가')
        elif 'Adj Close' in df.columns:
            ax.plot(df.index, df['Adj Close'], linewidth=2, color='#2563eb', label='수정 종가')
        
        # Format x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
        plt.xticks(rotation=45)
        
        # Labels and title
        ax.set_xlabel('날짜', fontsize=12)
        ax.set_ylabel(info['ylabel'], fontsize=12)
        ax.set_title(f'{info["title"]} - 최근 30일 추이', fontsize=14, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        # Add source annotation
        ax.annotate('데이터 출처: yfinance', xy=(0.02, 0.02), xycoords='axes fraction',
                   fontsize=8, alpha=0.7)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save chart
        chart_path = os.path.join(OUTPUT_DIR, info['filename'])
        plt.savefig(chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        
        chart_files[key] = info['filename']
        print(f"  ✓ Saved: {info['filename']}")
    
    return chart_files

def analyze_data(data):
    """Analyze the fetched data and generate insights."""
    analysis = {}
    
    for key, item in data.items():
        if item is None:
            continue
        
        df = item['df']
        info = item['info']
        
        # Get the close/adj close column
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
        
        # Get the date - it's the index itself
        max_date = pd.Timestamp(max_idx).strftime('%Y-%m-%d')
        min_date = pd.Timestamp(min_idx).strftime('%Y-%m-%d')
        
        analysis[key] = {
            'title': info['title'],
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

def generate_blog_post(chart_files, analysis):
    """Generate the blog post with charts and analysis."""
    
    # Generate analysis text
    summary_lines = []
    
    # Build individual analysis
    gold_analysis = analysis.get('gold', {})
    sp500_analysis = analysis.get('sp500', {})
    kospi_analysis = analysis.get('kospi', {})
    oil_analysis = analysis.get('oil', {})
    treasury_analysis = analysis.get('treasury', {})
    
    # Determine trends
    gold_trend = "상승" if gold_analysis.get('change_pct', 0) > 0 else "하락"
    sp500_trend = "상승" if sp500_analysis.get('change_pct', 0) > 0 else "하락"
    kospi_trend = "상승" if kospi_analysis.get('change_pct', 0) > 0 else "하락"
    oil_trend = "상승" if oil_analysis.get('change_pct', 0) > 0 else "하락"
    treasury_trend = "상승" if treasury_analysis.get('change_pct', 0) > 0 else "하락"
    
    blog_post = f"""---
layout: post
title: "2026년 2월 글로벌 경제 동향 분석: 금리 정책과 시장 트렌드"
date: 2026-02-25 06:00:00 +0900
categories: [economy, global-finance]
tags: [경제, 연준, 금리, 인플레이션, 주식, 금융, 금 가격, 원유, KOSPI, S&P 500]
description: "2026년 2월 25일 글로벌 및 한국 경제 동향 분석과 주요 지수 트렌드"
image: /assets/images/2026-02-25/gold_price_chart.png
---

## 2026년 2월 글로벌 경제 동향 분석: 금리 정책과 시장 트렌드

최근 30일간의 주요 금융 지수 데이터를 분석하여 2026년 2월 현재 글로벌 및 한국 경제의 동향을 정리해 드립니다. 본 분석은 **yfinance** 데이터를 기반으로 하며, 금 가격, S&P 500, KOSPI, 원유, 10년 국채 금리 등 주요 지표를 포괄적으로 다룹니다.

---

## 📊 주요 지수 개요

### 금 가격 동향

![금 가격 차트](/assets/images/2026-02-25/gold_price_chart.png)

*그림 1: 최근 30일간 금 가격 추이 (데이터 출처: yfinance)*

금 가격은 최근 30일간 **{gold_analysis.get('start_price', 'N/A')}$**에서 **{gold_analysis.get('end_price', 'N/A')}$**로 **{gold_analysis.get('change_pct', 0):.2f}%** {gold_trend}했습니다.

- 기간 중 최고가: **{gold_analysis.get('max_price', 'N/A')}$** ({gold_analysis.get('max_date', 'N/A')})
- 기간 중 최저가: **{gold_analysis.get('min_price', 'N/A')}$** ({gold_analysis.get('min_date', 'N/A')})

금은 전통적으로 인플레이션 헤지 수단으로 활용되며, 최근 경제 불확실성이 높아짐에 따라 안전자산으로서의 선호도가 변화하고 있습니다.

---

### S&P 500 지수

![S&P 500 차트](/assets/images/2026-02-25/sp500_chart.png)

*그림 2: 최근 30일간 S&P 500 지수 추이 (데이터 출처: yfinance)*

미국 주식시장을 대표하는 S&P 500 지수는 최근 30일간 **{sp500_analysis.get('start_price', 'N/A')}**에서 **{sp500_analysis.get('end_price', 'N/A')}**로 **{sp500_analysis.get('change_pct', 0):.2f}%** {sp500_trend}했습니다.

- 기간 중 최고치: **{sp500_analysis.get('max_price', 'N/A')}** ({sp500_analysis.get('max_date', 'N/A')})
- 기간 중 최저치: **{sp500_analysis.get('min_price', 'N/A')}** ({sp500_analysis.get('min_date', 'N/A')})

미국 경제의 성장세와 기업 실적, 그리고 연준의 금리 정책이 주가에 큰 영향을 미치고 있습니다.

---

### KOSPI 지수

![KOSPI 차트](/assets/images/2026-02-25/kospi_chart.png)

*그림 3: 최근 30일간 KOSPI 지수 추이 (데이터 출처: yfinance)*

한국 주식시장을 대표하는 KOSPI 지수는 최근 30일간 **{kospi_analysis.get('start_price', 'N/A')}**에서 **{kospi_analysis.get('end_price', 'N/A')}**로 **{kospi_analysis.get('change_pct', 0):.2f}%** {kospi_trend}했습니다.

- 기간 중 최고치: **{kospi_analysis.get('max_price', 'N/A')}** ({kospi_analysis.get('max_date', 'N/A')})
- 기간 중 최저치: **{kospi_analysis.get('min_price', 'N/A')}** ({kospi_analysis.get('min_date', 'N/A')})

KOSPI는 글로벌 시장 동향, 반도체 등 수출 주도 기업의 실적, 그리고 원/달러 환율 등 다양한 요인에 영향을 받습니다.

---

### 원유 가격

![원유 가격 차트](/assets/images/2026-02-25/oil_price_chart.png)

*그림 4: 최근 30일간 원유 가격 추이 (데이터 출처: yfinance)*

WTI 원유 가격은 최근 30일간 **{oil_analysis.get('start_price', 'N/A')}$**에서 **{oil_analysis.get('end_price', 'N/A')}$**로 **{oil_analysis.get('change_pct', 0):.2f}%** {oil_trend}했습니다.

- 기간 중 최고가: **{oil_analysis.get('max_price', 'N/A')}$** ({oil_analysis.get('max_date', 'N/A')})
- 기간 중 최저가: **{oil_analysis.get('min_price', 'N/A')}$** ({oil_analysis.get('min_date', 'N/A')})

원유 가격은 공급망 문제, OPEC+ 생산 결정, 글로벌 경제 성장 전망 등 복합적인 요인에 의해 결정됩니다.

---

### 10년 국채 금리

![10년 국채 금리 차트](/assets/images/2026-02-25/treasury_rate_chart.png)

*그림 5: 최근 30일간 미국 10년 국채 금리 추이 (데이터 출처: yfinance)*

미국 10년 국채 금리는 최근 30일간 **{treasury_analysis.get('start_price', 'N/A')}%**에서 **{treasury_analysis.get('end_price', 'N/A')}%**로 **{treasury_analysis.get('change_pct', 0):.2f}%** {treasury_trend}했습니다.

- 기간 중 최고치: **{treasury_analysis.get('max_price', 'N/A')}%** ({treasury_analysis.get('max_date', 'N/A')})
- 기간 중 최저치: **{treasury_analysis.get('min_price', 'N/A')}%** ({treasury_analysis.get('min_date', 'N/A')})

장기 국채 금리는 시장의 인플레이션 기대치와 경제 성장 전망을 반영하는 중요한 지표입니다.

---

## 🌍 글로벌 vs 지역 시장 비교

### 경제 트렌드 요약

최근 30일간의 데이터를 바탕으로 볼 때, 글로벌 경제는 다음과 같은 특징을 보이고 있습니다:

1. **주식시장**: 미국 S&P 500과 한국 KOSPI 모두 {sp500_trend if sp500_analysis.get('change_pct', 0) * kospi_analysis.get('change_pct', 0) > 0 else "서로 다른 방향성을 보이며"} 움직였습니다.

2. **원자재**: 금과 원유 가격의 변동성은 시장의 불확실성과 전망을 반영하고 있습니다.

3. **금리**: 장기 국채 금리의 움직임은 연준의 통화 정책 기대와 경제 성장 전망을 나타냅니다.

### 한국 시장 특징

KOSPI는 다음 요인들에 민감하게 반응하고 있습니다:

- 반도체 등 핵심 수출 품목의 글로벌 수요 변화
- 미-중 경제 갈등 등 지정학적 리스크
- 환율 변동에 따른 수출 기업 수익성 변화

---

## 📈 주요 시사점

### 투자자 관점

1. **자산 배분**: 금과 주식, 채권 간의 상관관계를 고려한 균형 잡힌 포트폴리오가 필요합니다.

2. **리스크 관리**: 경제 불확실성이 높을 때는 안전자산 비중 확대를 고려해야 합니다.

3. **장기 관점**: 단기 변동성에 일희일비하지 않고 기본적인 경제 펀더멘털을 중심으로 투자 결정을 내려야 합니다.

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

2026년 2월 현재 글로벌 경제는 여전히 변동성이 높은 상황입니다. 주요 지수들의 움직임을 모니터링하면서 데이터 기반의 객관적 분석에 기초한 투자 및 경제 활동이 필요합니다.

본 포스트에서 제공하는 데이터와 차트는 **yfinance**를 통해 수집된 실제 시장 데이터를 기반으로 하며, 지속적인 업데이트를 통해 최신 경제 동향을 파악하는 데 활용하실 수 있습니다.

---

*본 분석은 정보 제공 목적으로 작성되었으며, 투자 조언이 아닙니다. 투자 결정 시에는 반드시 전문가의 조언을 구하시기 바랍니다.*
"""
    
    # Write the blog post
    with open(POST_PATH, 'w', encoding='utf-8') as f:
        f.write(blog_post)
    
    print(f"\n✓ Blog post saved: {POST_PATH}")
    
    return blog_post

def main():
    """Main execution function."""
    print("="*60)
    print("Economic News Post Generator")
    print("="*60)
    
    # Step 1: Create output directory
    print("\n[1/4] Creating output directory...")
    create_output_directory()
    
    # Step 2: Fetch data
    print("\n[2/4] Fetching financial data...")
    data = fetch_data()
    
    # Step 3: Create charts
    print("\n[3/4] Creating charts...")
    chart_files = create_chart(data)
    
    # Step 4: Analyze data
    print("\n[4/4] Analyzing data...")
    analysis = analyze_data(data)
    
    # Step 5: Generate blog post
    print("\n[5/5] Generating blog post...")
    blog_post = generate_blog_post(chart_files, analysis)
    
    print("\n" + "="*60)
    print("✓ All tasks completed successfully!")
    print("="*60)
    
    # Print summary
    print("\n📋 Summary:")
    print(f"  - Charts created: {len(chart_files)}")
    print(f"  - Blog post: {POST_PATH}")
    print(f"  - Data source: yfinance")
    print(f"  - Instruments analyzed: {len([d for d in data.values() if d is not None])}")
    
    return {
        'chart_files': chart_files,
        'analysis': analysis,
        'post_path': POST_PATH
    }

if __name__ == '__main__':
    result = main()
