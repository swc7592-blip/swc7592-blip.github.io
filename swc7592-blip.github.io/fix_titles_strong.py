import os
import re

posts_dir = "_posts"
print("🔍 강력한 제목 복구 작업을 시작합니다...")

for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        # 파일명에서 날짜(YYYY-MM-DD) 떼고 제목만 추출
        raw_title = filename.replace(".md", "")
        if len(raw_title) > 11 and raw_title[4] == '-' and raw_title[7] == '-':
             raw_title = raw_title[11:]
        
        changed = False
        title_exists = False
        
        # 한 줄씩 검사
        for i, line in enumerate(lines):
            # 'title:' 로 시작하는 줄을 찾음
            if line.strip().startswith("title:"):
                title_exists = True
                # 내용이 비어있거나 따옴표만 있는 경우 ("" or '')
                value = line.split(":", 1)[1].strip().replace('"', '').replace("'", "")
                if not value: 
                    lines[i] = f'title: "{raw_title}"\n' # 제목 강제 주입
                    changed = True
                    print(f"🔧 수정됨 (빈 제목 채움): {filename}")
                break
        
        # 아예 title 항목이 없으면 두 번째 줄에 추가
        if not title_exists and len(lines) > 0 and lines[0].strip() == "---":
            lines.insert(1, f'title: "{raw_title}"\n')
            changed = True
            print(f"➕ 추가됨 (제목 항목 신설): {filename}")

        # 변경사항이 있으면 파일 저장
        if changed:
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(lines)

print("🎉 작업 끝! 이제 git push를 해주세요.")
