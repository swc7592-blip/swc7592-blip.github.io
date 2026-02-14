#!/usr/bin/env python3

import json
import re
from collections import Counter, defaultdict
from datetime import datetime

# Load tweets
with open('/Users/shin/.openclaw/workspace/agents/x/data/follower_tweets_20260211_030105.json', 'r') as f:
    tweets = json.load(f)

print(f"Total tweets: {len(tweets)}")
print()

# Calculate engagement score for each tweet
for tweet in tweets:
    tweet['engagement_score'] = tweet.get('retweet_count', 0) + tweet.get('favorite_count', 0) + tweet.get('reply_count', 0)

# Sort by engagement
top_tweets = sorted(tweets, key=lambda x: x['engagement_score'], reverse=True)[:5]

# Extract keywords (simple word extraction)
all_words = []
for tweet in tweets:
    text = tweet['text']
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Extract words (hashtags and regular words)
    words = re.findall(r'#?\w+', text.lower())
    all_words.extend(words)

keyword_counts = Counter(all_words)

# Categorize tweets by type
retweets = [t for t in tweets if t.get('is_retweet', False)]
originals = [t for t in tweets if not t.get('is_retweet', False)]

# Activity by user
user_activity = defaultdict(lambda: {'total': 0, 'retweets': 0, 'originals': 0})
for tweet in tweets:
    user = tweet['user_username']
    user_activity[user]['total'] += 1
    if tweet.get('is_retweet', False):
        user_activity[user]['retweets'] += 1
    else:
        user_activity[user]['originals'] += 1

# Time analysis
tweet_dates = []
for tweet in tweets:
    try:
        dt = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        tweet_dates.append(dt)
    except:
        pass

# Generate report
print("=" * 70)
print("엑스(X) 팔로워 트윗 분석 보고서")
print("=" * 70)
print()

print(f"수집 시각: 2026-02-11 03:01:05")
print(f"총 트윗 수: {len(tweets)} (유니크)")
print(f"리트윗: {len(retweets)} ({len(retweets)/len(tweets)*100:.1f}%)")
print(f"오리지널 트윗: {len(originals)} ({len(originals)/len(tweets)*100:.1f}%)")
print()

print("=" * 70)
print("1. 전체 트윗 요약 (경제 필터링 없음)")
print("=" * 70)
print()
print("주요 활동 패턴:")
print(f"- 75% 이상이 리트윗으로 정보 공유 중심")
print(f"- 인스타그램/YouTube 링크 공유가 주를 이룸")
print(f"- 경제, 코인, 주식 관련 트윗과 라이프스타일 트윗이 혼재")
print()

print("콘텐츠 카테고리:")
print("- 주식/트레이딩 시그널 (moonmarket 계정들 중심)")
print("- 경제 뉴스 큐레이션 (blazingbees 등)")
print("- 라이프스타일/일상 공유 (여행, 쇼핑, 음식)")
print("- 기술/혁신 관련 트윗 (Tesla, Rocket Lab 등)")
print()

print("=" * 70)
print("2. TOP 5 트윗 상세 요약 (참여도 기준)")
print("=" * 70)
print()

for i, tweet in enumerate(top_tweets, 1):
    print(f"TOP {i}: @{tweet['user_username']} ({tweet['user_name']})")
    print(f"트윗 ID: {tweet['tweet_id']}")
    print(f"작성 시간: {tweet['created_at']}")
    print(f"참여도: ❤️ {tweet.get('favorite_count', 0)} | 🔄 {tweet.get('retweet_count', 0)} | 💬 {tweet.get('reply_count', 0)}")
    print(f"리트윗 여부: {'예' if tweet.get('is_retweet', False) else '아니오'}")
    print(f"내용:")
    print(f"  {tweet['text'][:200]}...")
    print()

print("=" * 70)
print("3. 트렌드 키워드 분석")
print("=" * 70)
print()

print("상위 키워드 (빈도순):")
for word, count in keyword_counts.most_common(30):
    print(f"  {word}: {count}회")
print()

print("주요 해시태그:")
hashtags = {k: v for k, v in keyword_counts.items() if k.startswith('#')}
for tag, count in sorted(hashtags.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {tag}: {count}회")
print()

print("주요 주식 심볼:")
stock_symbols = {k: v for k, v in keyword_counts.items() if k.startswith('$') and len(k) > 1}
for symbol, count in sorted(stock_symbols.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {symbol}: {count}회")
print()

print("=" * 70)
print("4. 팔로워별 활동 분석")
print("=" * 70)
print()

for user, data in sorted(user_activity.items(), key=lambda x: x[1]['total'], reverse=True):
    rt_pct = data['retweets'] / data['total'] * 100 if data['total'] > 0 else 0
    print(f"@{user}:")
    print(f"  총 트윗: {data['total']}")
    print(f"  리트윗: {data['retweets']} ({rt_pct:.1f}%)")
    print(f"  오리지널: {data['originals']} ({100-rt_pct:.1f}%)")
    print()

print("=" * 70)
print("5. 경제/투자 관련 테마")
print("=" * 70)
print()

print("주요 테마:")
print("- 페니 스탁 트레이딩 ($CJMB, $KAVL, $FITY, $SXTP 등)")
print("- 원전/SMR (소형모듈원자로) 파트너십 및 개발")
print("- 전고체 배터리 기술 (토요타)")
print("- USDC 스테이블코인 유통 (다날)")
print("- 중국 희토류 통제와 반도체 산업")
print("- 코스피/코스닥 시장 동향")
print("- 비트코인 및 암호화폐")
print("- Tesla 주가 기술적 분석")
print()

print("=" * 70)
print("6. 활동 시간대 분석")
print("=" * 70)
print()

if tweet_dates:
    hours = [dt.hour for dt in tweet_dates]
    hour_counts = Counter(hours)
    print("시간대별 활동 분포:")
    for hour in sorted(hour_counts.keys()):
        bar = "█" * (hour_counts[hour] // 2)
        print(f"  {hour:02d}:00 - {hour_counts[hour]:2d}개 {bar}")
    print()

    # Most active periods
    peak_hours = hour_counts.most_common(3)
    print(f"가장 활발한 시간대:")
    for hour, count in peak_hours:
        print(f"  {hour:02d}:00 - {count}개")
    print()

print("=" * 70)
print("분석 완료")
print("=" * 70)
