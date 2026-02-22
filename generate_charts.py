import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from datetime import datetime, timedelta
import pandas as pd

# Set Korean font for matplotlib
plt.rcParams['font.sans-serif'] = ['AppleGothic', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# Get historical data for commodities (last 30 days)
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# Create chart 1: Commodity prices over time
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
fig.suptitle('Commodity & Cryptocurrency Price Trends (Last 30 Days)', fontsize=16, fontweight='bold')

# Plot metals
for name, ticker in [('Gold', 'GC=F'), ('Silver', 'SI=F')]:
    data = yf.Ticker(ticker).history(start=start_date, end=end_date)['Close']
    ax1.plot(data.index, data.values, label=name, linewidth=2)
ax1.set_ylabel('Price (USD)', fontsize=12)
ax1.legend(loc='upper left', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_title('Precious Metals', fontsize=14, fontweight='bold')

# Plot energy and crypto
for name, ticker in [('WTI Crude', 'CL=F'), ('Natural Gas', 'NG=F'), ('Bitcoin', 'BTC-USD')]:
    data = yf.Ticker(ticker).history(start=start_date, end=end_date)['Close']
    ax2.plot(data.index, data.values, label=name, linewidth=2)
ax2.set_ylabel('Price (USD)', fontsize=12)
ax2.legend(loc='upper left', fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_title('Energy & Cryptocurrency', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('assets/macro-commodity-trends.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 1 created: macro-commodity-trends.png')

# Create chart 2: Current prices comparison
fig, ax = plt.subplots(figsize=(12, 8))
current_prices = {
    'Gold': 5059.30,
    'Silver': 82.28,
    'WTI Crude': 66.39,
    'Natural Gas': 3.05,
    'Copper': 5.83,
    'Bitcoin': 67939.80
}

colors = ['#FFD700', '#C0C0C0', '#32CD32', '#4169E1', '#B87333', '#F7931A']
bars = ax.bar(range(len(current_prices)), list(current_prices.values()), color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(current_prices)))
ax.set_xticklabels(list(current_prices.keys()), rotation=45, ha='right', fontsize=11)
ax.set_ylabel('Current Price (USD)', fontsize=12, fontweight='bold')
ax.set_title('Current Market Prices - February 22, 2026', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, current_prices.values())):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'${value:,.2f}',
            ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('assets/macro-current-prices.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 2 created: macro-current-prices.png')

# Create chart 3: Agriculture commodities
fig, ax = plt.subplots(figsize=(12, 8))
agriculture = {
    'Corn': 427.50,
    'Soybeans': 1137.50,
    'Wheat': 573.50
}

colors = ['#90EE90', '#228B22', '#F4A460']
bars = ax.bar(range(len(agriculture)), list(agriculture.values()), color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(agriculture)))
ax.set_xticklabels(list(agriculture.keys()), rotation=45, ha='right', fontsize=11)
ax.set_ylabel('Current Price (USD per bushel)', fontsize=12, fontweight='bold')
ax.set_title('Agriculture Commodity Prices - February 22, 2026', fontsize=14, fontweight='bold')
ax.grid(axis='y', alpha=0.3)

for i, (bar, value) in enumerate(zip(bars, agriculture.values())):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'${value:.2f}',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('assets/macro-agriculture.png', dpi=150, bbox_inches='tight')
plt.close()
print('Chart 3 created: macro-agriculture.png')

print('All charts generated successfully!')
