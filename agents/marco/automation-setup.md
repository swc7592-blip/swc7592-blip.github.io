# 🤖 자동화 시스템 구축

## 1. Google 서치 콘솔 등록

### 사장님이 해야 할 일 (5분)

1. [Google Search Console](https://search.google.com/search-console/welcome) 접속
2. **URL 접두사** 선택
3. 블로그 URL 입력: `https://swc7592-blip.github.io/`
4. **계속** 클릭
5. **HTML 태그** 인증 방법 선택
6. 복사한 메타 태그를 `_config.yml`에 추가하거나 `_includes/head.html`에 추가
7. **확인** 클릭

### 인증 후
- **색인 생성** → **sitemap.xml** 추가: `https://swc7592-blip.github.io/sitemap.xml`

---

## 2. Google Analytics 연동

### 사장님이 해야 할 일 (10분)

1. [Google Analytics](https://analytics.google.com/) 접속
2. **측정 시작** 클릭
3. 계정 이름: `Macro Claw`
4. 데이터 스트림 설정:
   - 웹사이트 URL: `https://swc7592-blip.github.io`
   - 스트림 이름: `Macro Claw Blog`
5. **측정 ID** 복사 (예: `G-XXXXXXXXXX`)

### 마콜이 처리할 작업
측정 ID를 `_config.yml`에 추가:
```yaml
google_analytics: G-XXXXXXXXXX
```

---

## 3. Google AdSense 승인 준비

### 필요한 것
- 최소 10개의 고유 포스트
- 방문자 수 (일주일에 100명 이상 권장)
- 명확한 카테고리와 태그

### 마콜이 처리할 작업
- 자동으로 포스트 생성
- SEO 최적화
- 구조화된 데이터 추가

---

## 4. OpenClaw 자동화 시스템

### 자동화 작업
1. **매일 오전 9시**: 경제 뉴스 수집
2. **매주 월요일**: 키워드 트렌드 분석
3. **매주 수요일**: 새 포스트 초안 생성
4. **매일 오후 6시**: SEO 점수 체크

### 구현 방법
- OpenClaw cron job으로 자동 실행
- 블로그 리포지토리에 자동 커밋
- GitHub Actions로 자동 배포
