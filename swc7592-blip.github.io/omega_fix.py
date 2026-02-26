path = "agents/x/daily_economy_report.py"

# Read file
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Fix 1: Line 226 (RISK_OFF emoji dict)
bad1 = '    "RISK_OFF": "리스크 오프"'
good1 = '    "RISK_OFF": "리스크 오프"'

# Fix 2: Remove trailing quote from f-string
bad2 = 'log(f"✅ X 게시: {"성공\' if posted else \'❌ 실패\'} ")'
good2 = 'log(f"✅ X 게시: {status}")'

text = text.replace(bad1, good1)
text = text.replace(bad2, good2)

# Fix 3: Ensure relative paths (no hardcoded repository folders)
text = text.replace("swc7592-blip.github.io/", "")

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("Omega Fix Applied Successfully!")
