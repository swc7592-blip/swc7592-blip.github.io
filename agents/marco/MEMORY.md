# MEMORY.md - Macro Claw의 장기 기억

## 사장님 정보

- **이름:** thanksdany
- **호칭:** 사장님
- **GitHub:** swc7592-blip
- **시간대:** GMT+9 (Asia/Seoul)
- **Discord ID:** thanksdany (1469592491719397397)

---

## 블로그 정보

- **이름:** Macro Claw
- **주제:** 매크로 경제 & OpenClow 활용 가이드
- **주소:** https://swc7592-blip.github.io/
- **플랫폼:** GitHub Pages + Jekyll
- **테마:** minima

---

## 자동화 시스템

### Cron Job

1. **경제 뉴스 자동 수집 & 키워드 트렌드 분석 (6시간마다)** ⭐ PRIMARY
   - 빈도: 6시간마다 (매일 4회: 00:00, 06:00, 12:00, 18:00)
   - 작업: 글로벌+지역별혼합 경제 뉴스 수집 + 포스트 생성
   - 보고: 완료된 작업, 뉴스 요약, 키워드 트렌드, 다음 포스트 추천
   - **중요: Always Re-Check All Data Policy**
     - 최소 3개 이상의 다른 신뢰할 수 있는 출처에서 데이터 크로스체크
     - Published/Updated Date 시간 확인
     - 데이터 게시일이 1시간 이상 경과 확인
     - 출처 명시 필수
   - **중요: All Commodity Info Policy**
     - 금, 은, 원유(WTI/Brent), 천연가스, 구리, 옥수수, 콩, 밀, 비트코인, 이더리움
     - 현재 가격, 전일 대비 변화, 최고/최저 포함
   - **중요: Visual Content Policy** ⭐ NEW (2026-02-18)
     - 모든 포스트는 최소 3개 이상의 그래프/차트/스크린샷(통계 관련) 필수
     - TradingView, Yahoo Finance, Investing.com 차트 활용
     - yfinance로 직접 차트 생성
     - 경제 뉴스 사이트의 통계 차트/그래프 포함
     - Unsplash 금융/경제 관련 고품질 이미지 활용
     - 모든 차트는 명확한 캡션과 출처 명시
   - 완료 후: git add/commit/push 자동 실행

2. **글로벌+지역별혼합 경제 뉴스 포스트 생성 (6시간마다)** ⭐ PRIMARY
   - 빈도: 6시간마다 (매일 4회: 00:00, 06:00, 12:00, 18:00)
   - 작업: 새로운 매크로 경제 주제 포스트 자동 생성
   - 주제 예시:
     1) 글로벌 경제 뉴스 요약
     2) 특정 국가/지역 경제 분석 (미국, 중국, 유로존, 일본, 신흥국 등)
     3) 시장 데이터 분석 (금, 원유, 비트코인 등)
     4) 투자 전략 가이드
     5) 경제 정책 분석
   - **중요:** yfinance로 최신 비트코인/이더리움 가격 확인 필수
   - **중요: Visual Content Policy** ⭐ NEW (2026-02-18)
     - 모든 포스트는 최소 3개 이상의 그래프/차트/스크린샷(통계 관련) 필수
   - 완료 후: git add/commit/push 자동 실행

---

## 포스트 전략

### 주제

1. 매크로 경제 분석
   - 연준 정책
   - GDP, 인플레이션
   - 금리, 환율

2. OpenClow 활용 가이드
   - 자동화 튜토리얼
   - 뉴스 크롤링
   - 블로그 자동화

3. 경제 데이터 시각화
   - 차트, 그래프
   - 실시간 데이터

### 주기

- 매일: 뉴스 요약
- 매주: 심층 분석
- 매월: 전망 리포트

---

## 수익화 목표

### 1개월 목표
- 포스트 10개
- 방문자 100명/일

### 3개월 목표
- 포스트 30개
- 방문자 500명/일
- Google AdSense 승인

### 6개월 목표
- 포스트 60개
- 방문자 1,000명/일
- 수익 창출

---

## 키워드 전략

### 매크로 경제
- 연준 금리 (검색량 높음, 경쟁 높음)
- GDP 성장 (검색량 중간, 경쟁 중간)
- 인플레이션 (검색량 높음, 경쟁 높음)

### OpenClow
- OpenClow (검색량 낮음, 경쟁 낮음) ← 블루 오션!
- AI 자동화 (검색량 중간, 경쟁 중간)
- 블로그 자동화 (검색량 낮음, 경쟁 낮음) ← 블루 오션!

---

## 완료된 작업 (2026-02-08)

- [x] 블로그 구축 완료
- [x] SEO 설정 (sitemap.xml, robots.txt)
- [x] 자동화 시스템 구축
- [x] 포스트 4개 작성
- [x] 키워드 트렌드 분석

---

## 다음 단계

- [ ] Google Search Console 등록
- [ ] Google Analytics 연동
- [ ] Google AdSense 승인 준비
- [ ] 포스트 10개까지 확장

---

## GitHub 작업 흐름

```bash
# 리포지토리 경로
/Users/shin/.openclaw/workspace/swc7592-blip.github.io

# 포스트 경로
_posts/YYYY-MM-DD-slug.md

# Git 명령어
git add _posts/
git commit -m "새 포스트: 제목"
git push origin main
```

---

## 중요한 결정

1. **플랫폼 선택:** GitHub Pages (완전 무료, 개발 불필요)
2. **자동화:** OpenClow로 완전 자동화
3. **사장님 역할:** 글 작성/수정만
4. **수익화:** Google AdSense (콘텐츠 충분 시)

---

## 사장님의 스타일

- 개발 지식: 전혀 없음
- 선호: 자동화, 수익화, 최소 노력
- 언어: 한국어/영어 모두 OK
- 피드백: 빠르고 직관적인 것 선호

---

## OpenClow 사용법

### 웹 검색
```yaml
web_search:
  query: "연준 금리"
  count: 5
  country: KR
```

### 파일 작성
```yaml
write:
  path: "/path/to/file.md"
  content: "내용"
```

### Git 작업
```yaml
exec:
  command: "git add -A && git commit -m '...' && git push"
```

### 실시간 시세 가져오기 (yfinance)
```bash
# Python yfinance로 최신 시세 가져오기
python3 << 'EOF'
import yfinance as yf

# 비트코인
btc = yf.Ticker('BTC-USD')
btc_price = btc.history(period='1d')['Close'].iloc[-1]

# 이더리움
eth = yf.Ticker('ETH-USD')
eth_price = eth.history(period='1d')['Close'].iloc[-1]

print(f"BTC: ${btc_price:,.2f}")
print(f"ETH: ${eth_price:,.2f}")
EOF
```

**중요:** ⚠️ **항상 yfinance로 최신 비트코인/이더리움 가격을 가져와야 함!**
- market_data.txt 데이터는 오래될 수 있음
- 사장님이 지정한 방법: yfinance
- 포스트 작성 전 항상 최신 가격 확인 필수!

---

## 기술 스택

- **플랫폼:** GitHub Pages
- **프레임워크:** Jekyll
- **테마:** minima
- **자동화:** OpenClow Cron
- **배포:** GitHub Actions
- **언어:** Markdown

---

## 주의 사항

1. 사장님은 개발 지식이 없으니 모든 기술 세팅 담당
2. 사장님은 글 작성/수정만
3. Google 설정은 사장님이 직접 해야 함 (보안상)
4. 수익화는 콘텐츠 충분 후 (최소 10개 포스트)

---

## 업데이트 기록

### 2026-02-18
- ✅ Visual Content Policy 추가 (사장님 요청)
  - 모든 포스트는 최소 3개 이상의 그래프/차트/스크린샷(통계 관련) 필수
  - TradingView, Yahoo Finance, Investing.com 차트 활용
  - yfinance로 직접 차트 생성
  - 경제 뉴스 사이트의 통계 차트/그래프 포함
  - Unsplash 금융/경제 관련 고품질 이미지 활용
- ✅ Cron Job 업데이트 (2개 job에 Visual Content Policy 적용)
- ✅ MEMORY.md 업데이트

### 2026-02-15
- ✅ 에이전트 최적화 완료
  - 보안 강화 (프롬프트 인젝션 방어, 이메일 인증)
  - 역할 명확화 (Researcher + Communicator)
  - 하트비트 개선 (순환식 패턴)
  - 비용 최적화 가이드 추가
- ✅ heartbeat-state.json 생성
- ✅ 순환식 하트비트 패턴 도입

### 2026-02-08
- 블로그 구축 완료
- 자동화 시스템 구축
- 포스트 4개 작성
- 키워드 트렌드 분석

---

**작성 시간:** 2026-02-15
**작성자:** Marco
**업데이트:** 정기적 업데이트 필요
