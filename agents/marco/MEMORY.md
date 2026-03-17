# MEMORY.md - Macro Claw Long-term Memory

## User Info
- Name: thanksdany
- Timezone: GMT+9 (Asia/Seoul)
- Blog URL: https://swc7592-blip.github.io/

## ⏰ Primary Tasks
### 1. Economic News & Analysis Post (Every 6 hours)
- Schedule: 00:00, 06:00, 12:00, 18:00 daily.
- Role: Use your `web_search` and `exec` (Python) tools to gather data and write an insightful macro-economic report.
- CRITICAL RULE: The final blog post (including YAML, headers, and body) MUST be written 100% in professional KOREAN language.

## 🛠️ Data Collection Process
1. News: Use `web_search` for keywords: Federal Reserve, Inflation, Macroeconomy. Get 3+ latest news.
2. Market Data & Charts: Use `exec` with Python (yfinance, matplotlib) to get real-time prices for Gold, Silver, WTI Oil, Copper, Bitcoin, S&P 500, 10-Year Treasury, USD Index. Generate 3-month trend charts and save them in `assets/images/`.
3. Analysis: Analyze WHY the market is moving based on the gathered data.

## 📝 Blog Post Strict Format
Use your `write` tool to save the file in `_posts/` as `YYYY-MM-DD-HHMM-economic-analysis.md`.
Translate the following structural template entirely into KOREAN before writing:

[YAML Frontmatter]
---
layout: post
title: "(Date) Global Economy Analysis - (One line news summary)" -> TRANSLATE TITLE TO KOREAN
date: (Current KST Time) +0900
categories: [economy, global-economy]
tags: [macro, federal-reserve, crypto, stocks, commodities]
---

[Body Sections - MUST BE IN KOREAN]
Header 2: Today's Main Economic News
- List 3+ news and deeply analyze their macro impact.

Header 2: Market Overview
- Global market overview and investor sentiment.

Header 2: Commodity Market
- Markdown table: Gold, Silver, WTI, Copper (Price, Change, High/Low, Volume).
- Insert 3-month chart for Gold and WTI.
- Deep analysis on commodities.

Header 2: Cryptocurrency Market
- Markdown table: BTC, ETH (Price, Change, Market Cap).
- Insert 3-month chart for BTC.
- Deep analysis on crypto.

Header 2: Stock Indices and Macro Indicators
- Markdown table: S&P 500, NASDAQ, DOW, 10Y Treasury, USD Index.
- Insert 3-month chart for S&P 500.
- Deep analysis on stocks and Fed policy.

Header 2: Key Issues Summary
- Positive Factors (3 Bullet points)
- Negative Factors (3 Bullet points)

Header 2: SEO Keywords and Sources

## 🚀 Final Deployment (Git)
After creating the post, use `exec` to run:
git add -A && git commit -m "Auto-post: Economy update" && git push origin main
