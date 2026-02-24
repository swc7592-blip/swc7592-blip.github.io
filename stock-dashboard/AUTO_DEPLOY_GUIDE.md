# 🚀 Vercel 자동 배포 설정 가이드

사장님, GitHub에 푸시할 때마다 자동으로 Vercel에 배포되도록 설정하겠습니다!

## 📋 설정 단계 (1분 소요)

### 1단계: Vercel 대시보드 접속

1. https://vercel.com/dashboard 접속
2. `stock-dashboard` 프로젝트 클릭

### 2단계: Git Integration 설정

1. 상단 탭에서 **"Settings"** 클릭
2. **"Git"** 탭 클릭
3. **"Link Repository"** 버튼 클릭

### 3단계: GitHub 리포지토리 연결

1. **GitHub** 선택
2. `swc7592-blip/stock-dashboard` 리포지토리 선택
3. **"Connect"** 버튼 클릭

### 4단계: 배포 룰 설정

1. **Branch:** `main`
2. **Root Directory:** `/` (그대로)
3. **"Save"** 버튼 클릭

---

## ✅ 완료!

이제 이후부터는 다음을 할 때마다 **자동으로 배포**됩니다:

- 코드를 GitHub에 푸시 (`git push origin main`)
- 새로운 기능 추가
- 버그 수정

---

## 🔄 테스트

설정 완료 후, 테스트를 위해:

```bash
git add -A
git commit -m "Test auto-deploy"
git push origin main
```

→ Vercel에서 자동으로 배포 시작!

---

## 📱 알림 설정

배포 완료 알림을 받고 싶으면:

1. Vercel 대시보드 → Settings → Notifications
2. Email/Slack/Discord 연결
3. 배포 성공/실패 알림 켜기

---

## 🎯 추가 기능

자동 배포가 설정되면:
- ⚡ 푸시 후 1-2분 내 배포 완료
- 🔄 이전 버전으로 롤백 가능
- 📊 배포 히스토리 확인
- 🔍 배포 로그 확인

---

설정 완료 후 알려주세요! 바로 테스트 배포를 시작하겠습니다! 🚀
