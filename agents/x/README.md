# Stock & Mining Dashboard

## 프로젝트 개요

한국/미국 주식 + 비트코인 + 마이닝 회사 코인 보유량 추적 대시보드

## 핵심 기능

### 1. 마이닝 회사 코인 보유량 추적 🪙
- **MicroStrategy (MSTR)**
  - 비트코인 보유량 추적
  - 분기별/월별 변화
  - 매수/매도 내역

- **Bitmine** (확인 필요)
  - 비트코인/이더리움 보유량
  - 채굴량 변화

### 2. 시장 지수
- KOSPI, NASDAQ, S&P 500
- 비트코인, 이더리움 가격

### 3. 거시 경제
- 금리 동향
- 인플레이션 지표
- 뉴스 헤드라인

## 기술 스택

- **프론트엔드:** Next.js 15 + React
- **스타일:** Tailwind CSS
- **데이터 소스:**
  - Yahoo Finance API
  - CoinGecko API
  - MicroStrategy 공식 리포트
  - SEC filings (10-Q, 10-K)

## 데이터 수집 방법

### MicroStrategy 비트코인 보유량
1. **공식 리포트:** https://www.microstrategy.com/en/bitcoin
2. **SEC Filings:** 10-Q (분기), 10-K (연간)
3. **API:** 데이터 정제 후 JSON으로 저장

### Bitmine/마이닝 회사 데이터
- SEC Filings에서 추출
- CoinGecko 기업 보유량 데이터 확인

## 프로젝트 구조

```
/
├── app/                    # Next.js App Router
│   ├── page.tsx           # 메인 대시보드
│   ├── mining/            # 마이닝 회사 페이지
│   └── api/               # API 라우트
├── components/            # React 컴포넌트
├── data/                  # 데이터 파일
│   ├── microstrategy.json
│   └── mining-companies.json
└── lib/                   # 유틸리티
```

## 시작 방법

```bash
npm create next-app@latest
npm install recharts lucide-react
```

---

마이닝 회사들의 코인 보유량은 시장 센티먼트를 파악하는 중요한 지표입니다! 🐦
