#!/usr/bin/env python3
"""
팔로워 트윗 분석 스크립트
"""
import json
from collections import Counter
from datetime import datetime

# 트윗 데이터 로드
with open("data/follower_tweets_20260211_030105.json", "r", encoding="utf-8") as f:
    tweets = json.load(f)

print(f"📊 총 수집된 트윗: {len(tweets)}개")
print(f"📅 수집 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n" + "="*60 + "\n")

# 1. 전체 트윗 요약
print("📋 1. 전체 트윗 요약")
print("-" * 60)

# 사용자별 트윗 수
user_tweet_counts = Counter()
for tweet in tweets:
    user_tweet_counts[tweet['user_username']] += 1

print("사용자별 트윗 수:")
for username, count in user_tweet_counts.most_common():
    print(f"  - @{username}: {count}개")

# 리트윗 비율
retweet_count = sum(1 for t in tweets if t['is_retweet'])
original_count = len(tweets) - retweet_count
print(f"\n리트윗: {retweet_count}개 ({retweet_count/len(tweets)*100:.1f}%)")
print(f"오리지널 트윗: {original_count}개 ({original_count/len(tweets)*100:.1f}%)")

# 총 참여도 (좋아요 + 리트윗 + 댓글 + 인용)
total_engagement = sum(t['favorite_count'] + t['retweet_count'] + t['reply_count'] + t['quote_count'] for t in tweets)
print(f"총 참여도 (Likes+RTs+Replies+Quotes): {total_engagement:,}")

print("\n" + "="*60 + "\n")

# 2. TOP 5 트윗 상세 요약 (리트윗 기준)
print("🏆 2. TOP 5 트윗 (리트윗 수 기준)")
print("-" * 60)

top_tweets = sorted(tweets, key=lambda x: x['retweet_count'], reverse=True)[:5]
for i, tweet in enumerate(top_tweets, 1):
    print(f"\n[{i}위] @{tweet['user_username']} ({tweet['user_name']})")
    print(f"작성 시간: {tweet['created_at']}")
    print(f"참여도: ❤️{tweet['favorite_count']} 🔄{tweet['retweet_count']} 💬{tweet['reply_count']}")
    print(f"내용: {tweet['text'][:200]}...")

print("\n" + "="*60 + "\n")

# 3. 트렌드 키워드 분석
print("🔍 3. 트렌드 키워드 분석")
print("-" * 60)

# 모든 트윗 텍스트 추출
all_texts = [t['text'] for t in tweets]

# 티커 심볼 추출 ($XXXX 패턴)
import re
tickers = []
for text in all_texts:
    ticker_matches = re.findall(r'\$[A-Z]{2,5}', text)
    tickers.extend(ticker_matches)

ticker_counts = Counter(tickers)
print("상위 10개 주식/코인 티커:")
for ticker, count in ticker_counts.most_common(10):
    print(f"  - {ticker}: {count}회")

# 해시태그 추출
hashtags = []
for text in all_texts:
    hashtag_matches = re.findall(r'#\w+', text)
    hashtags.extend(hashtag_matches)

hashtag_counts = Counter(hashtags)
if hashtag_counts:
    print("\n상위 10개 해시태그:")
    for tag, count in hashtag_counts.most_common(10):
        print(f"  - {tag}: {count}회")

# 주요 단어 추출 (한글 + 영어 단어)
# 불용어 목록
stop_words = {'RT', 'the', 'and', 'to', 'of', 'in', 'for', 'is', 'on', 'with', 'at', 'from', 'by', 'it', 'this', 'that', 'are', 'was', 'be', 'as', 'or', 'https', 'http', 'co', 't', 'amp', 'quot', 'lt', 'gt', 'you', 'we', 'my', 'have', 'not', 'but', 'has', 'will', 'up', 'out', 'can', 'so', 'if', 'about', 'more', 'when', 'make', 'like', 'just', 'into', 'time', 'very', 'now', 'only', 'new', 'going', 'after'}

words = []
for text in all_texts:
    # RT @ 패턴 제거
    text = re.sub(r'RT @\w+:', '', text)
    # URL 제거
    text = re.sub(r'https?://t\.co/\w+', '', text)
    # 특수문자 제거
    text = re.sub(r'[^\w\s가-힣]', ' ', text)
    # 단어 추출 (3자 이상)
    word_matches = re.findall(r'\b[a-zA-Z가-힣]{3,}\b', text)
    words.extend([w.lower() for w in word_matches if w.lower() not in stop_words])

word_counts = Counter(words)
print("\n상위 20개 주요 단어:")
for word, count in word_counts.most_common(20):
    print(f"  - {word}: {count}회")

print("\n" + "="*60 + "\n")

# 4. 최근 활동 트렌드
print("📈 4. 최근 활동 트렌드")
print("-" * 60)

# 날짜별 트윗 수
date_counts = Counter()
for tweet in tweets:
    date_str = tweet['created_at'][:10]  # YYYY-MM-DD
    date_counts[date_str] += 1

print("날짜별 트윗 수 (최근 7일):")
for date, count in date_counts.most_common(7):
    print(f"  - {date}: {count}개")

print("\n" + "="*60 + "\n")
print("✅ 분석 완료!")
