#!/usr/bin/env python3
"""
팔로워들의 최신 트윗 수집 스크립트
"""
import json
import subprocess
import os
from datetime import datetime

# 팔로워 목록 로드
followers_file = "data/followers_list.json"
with open(followers_file, "r", encoding="utf-8") as f:
    followers_data = json.load(f)

all_tweets = []

# 인증 토큰
auth_token = "b37280fd9cca4df70b68feb788d99ea8c3d7bfa8"
ct0 = "d5b9d6cc30b6c65184c52838c23379e623d69479076333994b5988b423adb6f69483488c8e8a3d44ec92955752263dc24bfe59e68c126cf8ccfb0f814115b48fe443126a3888ace5660cebf1524615ef"

# 각 팔로워의 트윗 수집
for user in followers_data["users"]:
    username = user["username"]
    name = user["name"]
    user_id = user["id"]

    print(f"Collecting tweets from @{username} ({name})...")

    # bird 명령어 실행 (명령줄 옵션으로 인증 토큰 전달)
    result = subprocess.run(
        [
            "bird",
            "--auth-token", auth_token,
            "--ct0", ct0,
            "user-tweets", username,
            "-n", "10",
            "--json"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode == 0 and result.stdout:
        try:
            # bird CLI가 바로 배열을 반환
            tweets_list = json.loads(result.stdout)

            # tweets_list가 리스트인지 확인
            if isinstance(tweets_list, list):
                for tweet in tweets_list:
                    tweet_info = {
                        "user_username": username,
                        "user_name": name,
                        "user_id": user_id,
                        "tweet_id": tweet.get("id"),
                        "text": tweet.get("text", ""),
                        "created_at": tweet.get("createdAt"),
                        "favorite_count": tweet.get("likeCount", 0),  # likeCount
                        "retweet_count": tweet.get("retweetCount", 0),
                        "reply_count": tweet.get("replyCount", 0),
                        "quote_count": tweet.get("quoteCount", 0),
                        "view_count": tweet.get("viewCount", 0),
                        "is_retweet": tweet.get("text", "").startswith("RT @"),
                        "language": tweet.get("lang", "")
                    }
                    all_tweets.append(tweet_info)
                    print(f"  - Collected tweet ID {tweet.get('id')}")
            elif isinstance(tweets_list, dict) and "tweets" in tweets_list:
                # 대체: tweets 필드가 있는 경우
                for tweet in tweets_list["tweets"]:
                    tweet_info = {
                        "user_username": username,
                        "user_name": name,
                        "user_id": user_id,
                        "tweet_id": tweet.get("id"),
                        "text": tweet.get("text", ""),
                        "created_at": tweet.get("createdAt"),
                        "favorite_count": tweet.get("likeCount", 0),
                        "retweet_count": tweet.get("retweetCount", 0),
                        "reply_count": tweet.get("replyCount", 0),
                        "quote_count": tweet.get("quoteCount", 0),
                        "view_count": tweet.get("viewCount", 0),
                        "is_retweet": tweet.get("retweetedStatus") is not None,
                        "language": tweet.get("lang", "")
                    }
                    all_tweets.append(tweet_info)
                    print(f"  - Collected tweet ID {tweet.get('id')}")

        except json.JSONDecodeError as e:
            print(f"  Error parsing JSON for @{username}: {e}")
            print(f"  stdout: {result.stdout[:500]}")
    else:
        print(f"  Failed to fetch tweets from @{username}")
        print(f"  returncode: {result.returncode}")
        print(f"  stderr: {result.stderr[:500]}")
        print(f"  stdout: {result.stdout[:500]}")

# 결과 저장
output_file = f"data/follower_tweets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_tweets, f, ensure_ascii=False, indent=2)

print(f"\n✅ Total tweets collected: {len(all_tweets)}")
print(f"📁 Saved to: {output_file}")
