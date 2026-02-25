---
layout: home
title: Macro Claw
---

# 📊 Macro Claw

## 매크로 경제 & OpenClaw 활용 가이드

환영합니다! 🚀

여기서는 매크로 경제의 흐름을 읽고, **OpenClaw**로 자동화하는 실전 가이드를 공유합니다.

---

## 🚀 최신 글

<ul>
  {% for post in site.posts limit:5 %}
    <li style="margin-bottom: 10px;">
      <a href="{{ post.url | relative_url }}" style="font-weight:bold; color:#2196F3; text-decoration: none;">{{ post.title }}</a>
      <br><small style="color:#888;">({{ post.date | date: "%Y년 %m월 %d일" }})</small>
    </li>
  {% endfor %}
</ul>

---

## 🤖 자동화

이 블로그는 **OpenClaw**로 자동화됩니다:
- 경제 뉴스 자동 수집
- 키워드 트렌드 분석
- SEO 최적화

Made with ❤️ by Marco & OpenClaw

---

## 📊 방문자 수

<script async src="//busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>
<div style="background: #1e1e1e; padding: 15px; border-radius: 8px; text-align: center; color: #ccc;">
  전체 페이지 조회수: <span id="busuanzi_value_site_pv" style="color: #4CAF50; font-weight: bold;">로딩중...</span> 회<br>
  전체 고유 방문자: <span id="busuanzi_value_site_uv" style="color: #2196F3; font-weight: bold;">로딩중...</span> 명
</div>
