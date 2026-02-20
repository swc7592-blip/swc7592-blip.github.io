# TOOLS.md - 마콜 (Marco)의 로컬 노트

## 💰 비용 최적화 가이드 (Cost Optimization)

### 모델 라우팅 전략

**현재 기본 모델:** zai/glm-4.7 (Balanced - 저렴하고 효율적)

**모델 등급:**
- **Premium (프리미엄):** 최고의 추론, 복잡한 작업 (Claude Opus, GPT-5.2, Gemini 3 Pro)
- **Upper Balanced (상위 밸런스):** 강력한 추론, 비용 효율적 (Kimi 2.5, Gemini 2.5 Pro)
- **Balanced (밸런스):** 좋은 품질, 적당한 비용 (Claude Sonnet, GLM 4.7, Gemini 3 Flash)
- **Cheap (저렴):** 단순 작업, 백그라운드 작업 (Claude Haiku, GPT-5 nano)

**권장 폴백 체인:**
```json
{
  "primary": "zai/glm-4.7",
  "fallbacks": [
    "openrouter/google/gemini-3-flash-preview",
    "openai/gpt-5-mini",
    "openrouter/google/gemini-2.5-flash-lite"
  ]
}
```

### ⚠️ 중요: 제공자 간(Cross-Provider) 폴백

항상 폴백 체인에 다른 제공자의 모델을 포함하세요. 단일 제공자가 속도 제한에 걸리면 해당 제공자의 모든 모델이 실패합니다.

❌ **나쁨 — 단일 제공자:**
```json
"primary": "anthropic/claude-opus-4-6",
"fallbacks": ["anthropic/claude-sonnet-4-5"]
// Claude 쿼터 소진 시 둘 다 실패
```

✅ **좋음 — 제공자 교차:**
```json
"primary": "zai/glm-4.7",
"fallbacks": [
  "openrouter/google/gemini-3-flash-preview",
  "openai/gpt-5-mini"
]
// 한 제공자가 문제가 있어도 다른 것들은 작동
```

### 하트비트 비용 절감

하트비트는 자주 실행되지만 단순한 확인만 합니다. 가장 저렴한 모델을 사용하세요.

**하트비트 비용 비교 (하루 48비트 기준):**
- GPT-5 Nano: ~$0.005/일 (~$0.0001/비트)
- Claude Sonnet: ~$0.24/일 (~$0.005/비트)
- **차이:** 48배

**권장 하트비트 모델:** GPT-5 nano 또는 Gemini 2.5 Flash-Lite

### 동시성 제한

```json
{
  "maxConcurrent": 4,
  "subagents": {
    "maxConcurrent": 8
  }
}
```

하나의 잘못된 작업이 재시도 폭주와 비용 폭탄으로 이어지는 것을 막아줍니다.

### 월 비용 예상

**현재 예상 (GLM 4.7 기반):**
- 하트비트: ~$0.15/월
- 일반 대화: ~$5-10/월
- **총계:** ~$5-15/월

**비용 폭주 위험 요소:**
- 에이전트 무한 실행
- 무제한 재시도
- 프리미엄 모델을 기본값으로 사용
- 동시성 제한 없음

### 💡 비용 최적화 팁

1. **일찍, 그리고 자주 위임하기** - 복잡한 작업은 하위 에이전트에게
2. **작업 일괄 처리(Batch)** - 가능할 때 API 호출 묶기
3. **백그라운드 작업엔 저렴한 모델** - 하트비트, 모니터링
4. **긴 작업에는 하위 에이전트 생성** - sessions_spawn 사용

---

## Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
