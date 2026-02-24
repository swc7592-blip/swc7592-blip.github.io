'use client';

import { TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react';

interface StockIndexCardProps {
  name: string;
  symbol: string;
  country: string;
  price: number;
  change: number;
  changePercent: number;
  fallback?: boolean;
  lastUpdate?: Date;
}

export default function StockIndexCard({
  name,
  symbol,
  country,
  price,
  change,
  changePercent,
  fallback,
  lastUpdate,
}: StockIndexCardProps) {
  if (fallback) {
    return (
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 opacity-60">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-lg font-bold">{name}</h3>
            <p className="text-sm text-gray-400">{country}</p>
          </div>
          <AlertTriangle className="w-5 h-5 text-yellow-500" />
        </div>

        <div className="space-y-2">
          <div className="flex justify-between items-baseline">
            <span className="text-gray-400 text-sm">Status</span>
            <span className="text-yellow-500 text-sm font-semibold">
              Data unavailable
            </span>
          </div>
        </div>
      </div>
    );
  }

  const isPositive = change >= 0;
  const displayChange = isPositive ? `+${change.toFixed(2)}` : change.toFixed(2);
  const displayPercent = isPositive ? `+${changePercent.toFixed(2)}` : changePercent.toFixed(2);

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 hover:border-gray-600 transition-colors">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-bold">{name}</h3>
          <p className="text-sm text-gray-400">{country}</p>
        </div>
        <span className="text-xs bg-gray-700 px-2 py-1 rounded">{symbol}</span>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-baseline">
          <span className="text-gray-400 text-sm">Price</span>
          <span className="text-2xl font-bold">{price.toLocaleString()}</span>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-gray-400 text-sm">Change</span>
          <div className="flex items-center gap-2">
            {isPositive ? (
              <TrendingUp className="w-4 h-4 text-green-500" />
            ) : (
              <TrendingDown className="w-4 h-4 text-red-500" />
            )}
            <span className={`font-semibold ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
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
