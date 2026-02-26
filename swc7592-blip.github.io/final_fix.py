#!/usr/bin/env python3
"""
Final Fix for Cron Job - Recovery Script
"""

import os

path = "agents/x/daily_economy_report.py"

# Read file
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_content = []
for line in lines:
    # Fix 1: Path Bug (Removes nested folder issue)
    line = line.replace("swc7592-blip.github.io/_posts", "_posts")
    
    # Fix 2: Syntax Bug (Fixes problematic f-string quotes)
    if "log(f\"✅ X 게시:" in line:
        # Replace problematic f-string with fixed version
        line = line.replace("log(f\"✅ X 게시: {'성공' if posted else '❌ 실패'}\")", "post_status = '성공' if posted else '실패'\n        log(f\"✅ X 게시: {post_status}\")")
    if "log(f\"✅ Git push:" in line:
        line = line.replace("log(f\"✅ Git push: {'성공' if posted else '❌ 실패'}\")", "push_status = '성공' if pushed else '실패'\n        log(f\"✅ Git push: {push_status}\")")

# Write back to file
with open(path, "w", encoding="utf-8") as f:
    f.writelines(new_content)

print("Recovery Successful!")
