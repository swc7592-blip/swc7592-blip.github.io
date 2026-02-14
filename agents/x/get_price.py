import yfinance as yf
from datetime import datetime

# 1. 가져올 모든 원자재 리스트 (티커 정리)
tickers = {
    # 귀금속
    'Gold': 'GC=F',
    'Silver': 'SI=F',
    'Platinum': 'PL=F',
    
    # 에너지
    'WTI Crude Oil': 'CL=F',
    'Brent Crude': 'BZ=F',
    'Natural Gas': 'NG=F',
    
    # 금속 (산업용)
    'Copper': 'HG=F',
    'Aluminum': 'ALI=F',
    
    # 농산물
    'Corn': 'ZC=F',
    'Soybean': 'ZS=F',
    'Wheat': 'ZW=F',
    
    # 암호화폐
    'Bitcoin': 'BTC-USD',
    'Ethereum': 'ETH-USD'
}

print("=== Fetching Market Data... ===")
lines = []
lines.append(f"Update Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
lines.append("-" * 30)

for name, symbol in tickers.items():
    try:
        data = yf.Ticker(symbol)
        # 가장 최신 종가 가져오기
        price = data.history(period="1d")['Close'].iloc[-1]
        
        # 보기 좋게 포맷팅 (달러 표시, 소수점 2자리)
        formatted_line = f"{name}: ${price:,.2f}"
        lines.append(formatted_line)
        print(formatted_line) # 화면에도 출력
    except Exception as e:
        error_msg = f"{name}: Error ({symbol})"
        lines.append(error_msg)
        print(error_msg)

# 2. 우충봇이 읽을 파일로 저장 (market_data.txt)
with open("market_data.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("\nSuccess! Data saved to 'market_data.txt'")
