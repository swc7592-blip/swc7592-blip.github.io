# 🚀 사장님 블로그 세팅 가이드

## 상황
GitHub 인증으로 자동화가 어려워서, 쉬운 방법으로 진행합니다!

---

## 📋 사장님이 하실 일 (3단계, 10분 완성)

### 1단계: Jekyll 테마 설치 (GitHub 웹에서)

1. 사장님이 만든 `macro-claw.github.io` 리포지토리로 이동
2. `Create new file` 클릭
3. 파일명: `_config.yml`
4. 내용 복사해서 붙여넣기 (아래 코드):

```yaml
title: Macro Claw
description: 매크로 경제 & OpenClaw 활용 가이드
author: thanksdany
lang: ko
theme: minima
google_analytics: G-XXXXXXXXXX  # 나중에 추가

plugins:
  - jekyll-seo-tag
  - jekyll-sitemap
```

5. `Commit changes` → `Commit directly to the main branch` 클릭

---

### 2단계: 메인 페이지 만들기

1. 리포지토리에서 `Create new file` 클릭
2. 파일명: `index.md`
3. 내용 복사해서 붙여넣기:

```markdown
---
layout: home
title: Macro Claw
---

# 📊 Macro Claw

## 매크로 경제 & OpenClaw 활용 가이드

환영합니다! 여기서는:

- 📈 매크로 경제 분석
- 🤖 OpenClaw 자동화 가이드
- 💡 경제 데이터 시각화
- 🔧 실전 튜토리얼

다룹니다.

## 최신 글

[추가됨...]
```

4. `Commit changes`

---

### 3단계: 첫 번째 포스트 추가

1. `Create new file` 클릭
2. 폴더명: `_posts` (앞에 언더바 필수)
3. 파일명: `_posts/2026-02-07-welcome.md` (날짜-제목.md 형식)
4. 내용:

```markdown
---
layout: post
title: "Macro Claw 블로그 오픈!"
date: 2026-02-07 18:00:00 +0900
categories: openclaw
---

## 🎉 블로그가 열렸습니다!

안녕하세요! 매크로 경제와 OpenClow 활용에 관한 여정을 시작합니다.

## 앞으로 다룰 주제

- 연준 정책 분석
- GDP/인플레이션 데이터 해석
- OpenClow로 경제 뉴스 자동화
- 경제 예측 모델 만들기

계속 지켜봐 주세요! 📊
```

5. `Commit changes`

---

## ✅ 완료 확인

1. `https://macro-claw.github.io` 접속
2. 사이트가 보이면 성공! (1-2분 소요)

---

## 📌 다음 단계

이 기본 세팅이 완료되면:

- SEO 최적화 (구글 서치 콘솔 등록)
- 구글 애널리틱스 연동
- 멋진 테마로 변경
- 자동화 시스템 구축

을 진행하겠습니다!

---

혹시 막히는 곳 있으면 말씀하세요. 🚀
