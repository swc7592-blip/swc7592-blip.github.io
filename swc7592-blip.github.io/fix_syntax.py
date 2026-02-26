import os

file_path = "agents/x/daily_economy_report.py"

# Read file
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Fix datetime import and usage
lines[0] = "from datetime import datetime, timedelta, timezone\n"
lines[3] = "kst = timezone(timedelta(hours=9))\n"
lines[5] = "safe_time = datetime.datetime.now(kst) - datetime.timedelta(minutes=5)\n"

# Fix line 507: Use simple string status
lines[507] = '        post_status = "성공" if posted else "실패"\n'
lines[508] = '        log(f"✅ X 게시: {post_status}")\n'

# Write file
with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("문법 오류 수정 완료!")
