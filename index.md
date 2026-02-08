---
layout: home
title: Macro Claw
---

# 📊 Macro Claw

## 매크로 경제 & OpenClaw 활용 가이드

환영합니다! 🎉

여기서는 **매크로 경제의 흐름**을 읽고, **OpenClaw로 자동화**하는 실전 가이드를 공유합니다.

---

## 📈 주제

- **매크로 경제 분석** - 연준, GDP, 인플레이션 데이터 해석
- **OpenClow 가이드** - AI 자동화 튜토리얼
- **시각화** - 경제 데이터를 눈에 보이게
- **예측 모델** - AI로 트렌드 미리 보기

---

## 🚀 최신 글

<div class="posts">
  {% for post in site.posts limit:5 %}
  <article>
    <h3><a href="{{ post.url }}">{{ post.title }}</a></h3>
    <time datetime="{{ post.date }}">{{ post.date | date: "%Y년 %m월 %d일" }}</time>
  </article>
  {% endfor %}
</div>

---

## 🤖 자동화

이 블로그는 **OpenClaw**로 자동화됩니다:
- 경제 뉴스 자동 수집
- 키워드 트렌드 분석
- SEO 최적화

Made with ❤️ by Marco & OpenClaw

---

## 📊 방문자 수

{% include footer-busuanzi.html %}
