import os

posts_dir = "_posts"
print("🔍 제목 복구 작업을 시작합니다...")

for filename in os.listdir(posts_dir):
    if filename.endswith(".md"):
        filepath = os.path.join(posts_dir, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        # 이미 제목이 있는지 확인
        has_title = any(line.strip().startswith("title:") for line in lines)
        
        # 제목이 없으면 파일명을 제목으로 추가
        if not has_title and len(lines) > 0 and lines[0].strip() == "---":
            # 파일명에서 날짜와 확장자 제거
            raw_title = filename.replace(".md", "")
            # 날짜 형식(YYYY-MM-DD-) 제거 시도
            if len(raw_title) > 11 and raw_title[4] == '-' and raw_title[7] == '-':
                 raw_title = raw_title[11:]
            
            # 제목 줄 생성
            new_title_line = f'title: "{raw_title}"\n'
            lines.insert(1, new_title_line)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"✅ 복구됨: {raw_title}")

print("🎉 모든 빈 제목이 채워졌습니다!")
