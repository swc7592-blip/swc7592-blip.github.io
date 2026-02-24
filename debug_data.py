#!/usr/bin/env python3
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

end_date = datetime.now()
start_date = end_date - timedelta(days=60)

ticker = 'GC=F'
df = yf.download(ticker, start=start_date, end=end_date, progress=False)
df = df.tail(30)

print("Original DataFrame structure:")
print(df.info())
print("\nColumns:", df.columns.tolist())
print("\nIndex:", df.index)
print("\nIndex type:", type(df.index))

# Try to access Close prices
if 'Close' in df.columns:
    prices = df['Close']
    print("\nPrices type:", type(prices))
    print("\nFirst few prices:")
    print(prices.head())
    
    max_price = prices.max()
    print("\nMax price:", max_price)
    
    max_idx = prices.idxmax()
    print("\nMax idx:", max_idx)
    print("Max idx type:", type(max_idx))
    
    # Try different ways to get the date
    print("\nTrying to get date...")
    print("Option 1 (direct):", df.loc[max_idx])
    print("Option 2 (reset_index):")
    df_reset = df.reset_index()
    print(df_reset.info())
