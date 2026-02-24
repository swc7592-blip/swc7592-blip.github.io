'use client';

import { TrendingUp, TrendingDown, AlertTriangle, Clock, BarChart3 } from 'lucide-react';

interface EconomicEventCardProps {
  name: string;
  date: string;
  time: string;
  timeKST: string; // 한국 시간
  importance: 'high' | 'medium' | 'low';
  currency: string;
  previous: string;
  forecast: string;
  actual: string | null;
  onClick?: () => void;
}

export default function EconomicEventCard({
  name,
  date,
  time,
  timeKST,
  importance,
  currency,
  previous,
  forecast,
  actual,
  onClick,
}: EconomicEventCardProps) {
  const importanceColor = {
    high: 'text-yellow-400',
    medium: 'text-orange-400',
    low: 'text-gray-400',
  };

  const importanceStars = {
    high: '★★★',
    medium: '★★',
    low: '★',
  };

  const formatDisplayDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  return (
    <div
      onClick={onClick}
      className="bg-gray-800 rounded-xl p-5 border border-gray-700 hover:border-blue-500 transition-all cursor-pointer"
    >
      <div className="flex items-start justify-between mb-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs bg-gray-700 px-2 py-1 rounded">{currency}</span>
            <span className={`text-xs font-semibold ${importanceColor[importance]}`}>
              {importanceStars[importance]}
            </span>
          </div>
          <h3 className="text-lg font-bold text-white">{name}</h3>
        </div>
        <div className="text-right ml-4">
          <p className="text-xs text-gray-400 flex items-center gap-1 justify-end">
            <Clock className="w-3 h-3" />
            KST
          </p>
          <p className="text-2xl font-bold text-blue-400">{timeKST}</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-3 text-sm">
        <div>
          <p className="text-gray-400 text-xs mb-1">Previous</p>
          <p className="font-semibold text-gray-200">{previous}</p>
        </div>
        <div>
          <p className="text-gray-400 text-xs mb-1">Forecast</p>
          <p className="font-semibold text-blue-400">{forecast}</p>
        </div>
        <div>
          <p className="text-gray-400 text-xs mb-1">Actual</p>
          <p className={`font-semibold ${actual ? (actual.startsWith('+') ? 'text-green-400' : 'text-red-400') : 'text-gray-500'}`}>
            {actual || '--'}
          </p>
        </div>
      </div>

      {onClick && (
        <div className="mt-4 pt-3 border-t border-gray-700">
          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold py-2 px-4 rounded-lg transition-colors flex items-center justify-center gap-2">
            <BarChart3 className="w-4 h-4" />
            View {name} History
          </button>
        </div>
      )}
    </div>
  );
}
