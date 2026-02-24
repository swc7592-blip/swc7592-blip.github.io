import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    try:
        async with async_playwright() as p:
            print("🔗 크롬(실제 화면 모드) 접속 중...")
            browser = await p.chromium.launch_persistent_context(
                user_data_dir="/Users/shin/Library/Application Support/Google/Chrome/Default",
                headless=False,
                args=['--no-sandbox']
            )
            page = await browser.new_page()
            
            print("📍 네이버 블로그 에디터 접속 (30초 완전 대기)...")
            await page.goto("https://blog.naver.com/hedge499/postwrite", timeout=60000)
            # 네이버 에디터는 로딩이 매우 느리므로 30초 넉넉히 대기합니다.
            await page.wait_for_timeout(30000)

            # 1. 텍스트 입력 (탭 키 방식 유지하되 더 정교하게)
            print("✍️ 본문 작성 시작 (화면 중앙 클릭 후 탭 이동)...")
            await page.mouse.click(640, 500)
            await page.wait_for_timeout(1000)
            for _ in range(8):
                await page.keyboard.press("Tab")
                await asyncio.sleep(0.3)
            
            await page.keyboard.type("2026년 장기요양보험료 전망 및 핵심 요약")
            await page.wait_for_timeout(1000)
            await page.keyboard.press("Tab")
            await page.keyboard.press("Tab")
            await page.keyboard.type("안녕하세요. hedge499입니다. 원격 자동화로 작성된 2026년 정책 안내글입니다.")
            await page.wait_for_timeout(2000)

            # 2. 발행 버튼 타격 (글자 '발행'을 직접 찾아서 클릭)
            print("🚀 '발행' 글자를 찾아 클릭 시도...")
            try:
                # 화면 전체에서 '발행'이라는 텍스트가 포함된 요소를 찾아 클릭
                await page.get_by_text("발행", exact=True).first.click(timeout=10000)
                print("✅ 1차 발행 메뉴 진입 성공")
            except:
                print("⚠️ 버튼 찾기 실패, 좌표(우측상단) 강제 클릭...")
                await page.mouse.click(1150, 60) # 1280 해상도 기준 우측 상단

            await page.wait_for_timeout(3000)

            # 3. 최종 확인 버튼 (글자 '발행하기'를 찾아 클릭)
            print("💾 '발행하기' 버튼 최종 타격...")
            try:
                await page.get_by_role("button", name="발행하기").click(timeout=10000)
                print("🎉 포스팅 발행 성공!")
            except:
                print("⚠️ 최종 버튼 찾기 실패, 엔터(Enter) 강제 주입...")
                # 버튼을 못 찾아도 팝업이 떠있을 확률이 높으므로 엔터 3번 연타
                for _ in range(3):
                    await page.keyboard.press("Enter")
                    await asyncio.sleep(1)

            print(f"🏁 최종 상태 URL: {page.url}")
            await page.screenshot(path="final_check.png")
            await browser.close()

    except Exception as e:
        print(f"❌ 전체 오류: {e}")

if __name__ == "__main__":
    asyncio.run(run_bot())
