# 🔧 Google 설정 가이드

## ✅ 완료된 작업
- [x] 블로그 구축 완료
- [x] sitemap.xml 생성
- [x] robots.txt 생성
- [x] 자동화 cron job 설정 (경제 뉴스, 키워드 트렌드, 포스트 생성)

---

## 📋 사장님이 해야 할 작업

### 1. Google Search Console (10분)

1. [Google Search Console](https://search.google.com/search-console/welcome) 접속
2. **URL 접두사** 선택
3. URL 입력: `https://swc7592-blip.github.io/`
4. **계속** 클릭
5. **HTML 태그** 선택
6. 이 태그 복사:
   ```html
   <meta name="google-site-verification" content="XXXXXXXXXXXXXXXX" />
   ```

7. 사장님께서 알려주시면, 제가 `_config.yml` 또는 `_includes/head.html`에 추가하겠습니다.

8. **확인** 클릭 → 인증 완료

9. 인증 후:
   - 왼쪽 메뉴 → **색인 생성** → **사이트맵** 클릭
   - 새 사이트맿 추가: `https://swc7592-blip.github.io/sitemap.xml`
   - **제출** 클릭

---

### 2. Google Analytics (15분)

1. [Google Analytics](https://analytics.google.com/) 접속
2. **측정 시작** 클릭
3. 계정 설정:
   - 계정 이름: `Macro Claw`
   - **다음** 클릭

4. 속성 설정:
   - 속성 이름: `Macro Claw Blog`
   - 리포트 시간대: `대한민국`
   - **다음** 클릭

5. 비즈니스 정보:
   - 산업 카테고리: `기술` 또는 `교육`
   - **만들기** 클릭

6. 데이터 스트림 설정:
   - 웹사이트 URL: `https://swc7592-blip.github.io`
   - 스트림 이름: `Macro Claw`
   - **스트림 만들기** 클릭

7. **측정 ID** 복사 (예: `G-XXXXXXXXXX`)
8. 사장님께서 측정 ID를 알려주시면 제가 블로그에 추가하겠습니다

---

### 3. Google AdSense (준비 필요)

**현재 상태:**
- 포스트 1개 (최소 10개 필요)
- 방문자 수 아직 없음

**AdSense 승인 조건:**
- ✅ 고유한 콘텐츠
- ✅ 정책 준수
- ✅ 활성화된 사이트
- ⏳ 방문자 수 (일주일에 100명 이상 권장)
- ⏳ 충분한 콘텐츠 (최소 10-15개 포스트)

**자동화가 도와드릴 부분:**
- 매일 자동으로 뉴스 포스트 생성
- SEO 최적화로 방문자 유치
- 2-3주 후 AdSense 승인 가능

---

## 🎯 다음 단계

사장님께서:
1. **Search Console**에 사이트맿 등록 완료 → "완료"라고 말씀해주세요
2. **Analytics** 측정 ID 알려주시면 → 제가 바로 블로그에 추가하겠습니다
3. 그러면 자동화가 계속 작동하면서 콘텐츠가 쌓입니다!

---

## 🤖 현재 자동화 중인 작업

| 작업 | 빈도 | 다음 실행 |
|------|------|-----------|
| 경제 뉴스 수집 | 매일 | 내일 오전 9시 |
| 키워드 트렌드 분석 | 매주 월요일 | 오전 9시 |
| 자동 포스트 생성 | 매주 수요일 | 오전 10시 |

---

**아무것도 안 하셔도 됩니다! 자동화가 작동합니다!** 🚀
