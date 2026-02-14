#!/usr/bin/env python3
"""
Macro Claw - 자동화 블로그 시스템
경제 뉴스 수집 & 포스트 생성
"""

import os
import json
import subprocess
from datetime import datetime
from pathlib import Path

# 설정
BLOG_PATH = "/Users/shin/.openclaw/workspace/swc7592-blip.github.io"
POSTS_PATH = f"{BLOG_PATH}/_posts"

# 경제 뉴스 키워드
ECONOMY_KEYWORDS = [
    "연준",
    "인플레이션",
    "GDP",
    "금리",
    "경제 성장",
    "미국 경제",
    "한국 경제",
    "FED",
    "Federal Reserve",
]

def generate_post(news_items):
    """뉴스 기반 포스트 생성"""
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    filename = f"{POSTS_PATH}/{date_str}-economy-news.md"

    # 기존 포스트 확인
    if os.path.exists(filename):
        print("오늘의 뉴스 포스트 이미 존재함")
        return None

    # 포스트 생성
    content = f"""---
layout: post
title: "{today.strftime('%Y년 %m월 %d일')} 경제 뉴스 요약"
date: {today.strftime('%Y-%m-%d 09:00:00') +0900}
categories: [경제, 뉴스]
tags: [경제, 연준, 인플레이션]
---

## 📈 오늘의 경제 뉴스

*뉴스 자동 수집 시스템이 작동 중입니다...*

### 주요 이슈

<!-- 뉴스 기사가 여기에 추가됩니다 -->

---

## 📊 데이터 포인트

<!-- 경제 데이터가 여기에 추가됩니다 -->

---

## 🤖 OpenClow로 자동화된 콘텐츠

이 포스트는 OpenClow 자동화 시스템으로 생성되었습니다.

**수정 제안**:
- 뉴스 기사 추가
- 데이터 차트 포함
- 개인적 분석 추가

---

작성자: Marco (AI)
자동화 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"포스트 생성됨: {filename}")
    return filename

def commit_and_push(post_file):
    """Git 커밋 및 푸시"""
    os.chdir(BLOG_PATH)

    # Git 명령어
    commands = [
        ["git", "add", post_file],
        ["git", "commit", "-m", "자동화: 경제 뉴스 포스트 추가"],
        ["git", "push", "origin", "main"],
    ]

    for cmd in commands:
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"성공: {' '.join(cmd)}")
        except subprocess.CalledProcessError as e:
            print(f"실패: {' '.join(cmd)}")
            print(e.stderr.decode())

def main():
    """메인 실행"""
    print("Macro Claw 자동화 시스템 시작...")

    # 뉴스 수집 (OpenClaw 웹 검색 사용)
    news_items = []  # 실제 구현 시 웹 검색 API 사용

    # 포스트 생성
    post_file = generate_post(news_items)

    if post_file:
        # Git 커밋 및 푸시
        commit_and_push(post_file)
        print("✅ 자동화 완료!")
    else:
        print("⏭️ 이미 오늘의 포스트가 존재합니다")

if __name__ == "__main__":
    main()
