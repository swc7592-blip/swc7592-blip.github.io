'use client';

import { Bitcoin, TrendingUp, TrendingDown, Wallet, Activity } from 'lucide-react';

interface DailyStatusCardProps {
  name: string;
  symbol: string;
  price: number;
  change: number;
  changePercent: number;
  currency: string;
  icon?: React.ReactNode;
  lastUpdate?: Date;
}

export default function DailyStatusCard({
  name,
  symbol,
  price,
  change,
  changePercent,
  currency,
  icon,
  lastUpdate,
}: DailyStatusCardProps) {
  const isPositive = change >= 0;
  const displayChange = isPositive ? `+${change.toFixed(2)}` : change.toFixed(2);
  const displayPercent = isPositive ? `+${changePercent.toFixed(2)}` : changePercent.toFixed(2);

  return (
    <div className="bg-gray-800 rounded-xl p-5 border border-gray-700 hover:border-gray-600 transition-colors">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          {icon}
          <div>
            <h3 className="text-base font-bold">{name}</h3>
            <p className="text-xs text-gray-400">{symbol}</p>
          </div>
        </div>
        <span className="text-xs bg-gray-700 px-2 py-1 rounded">{currency}</span>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-baseline">
          <span className="text-gray-400 text-sm">Price</span>
          <span className="text-2xl font-bold">{price.toLocaleString()}</span>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-gray-400 text-sm">24h Change</span>
          <div className="flex items-center gap-2">
            {isPositive ? (
              <TrendingUp className="w-4 h-4 text-green-500" />
            ) : (
              <TrendingDown className="w-4 h-4 text-red-500" />
            )}
            <span className={`font-semibold text-sm ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
              {displayChange} ({displayPercent}%)
            </span>
          </div>
        </div>

        {lastUpdate && (
          <div className="flex justify-between items-center pt-2 border-t border-gray-700">
            <span className="text-gray-400 text-xs">Updated</span>
            <span className="text-xs text-gray-500">
              {lastUpdate.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' })}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
