'use client';

import { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, AlertTriangle, Clock, Flame, Target } from 'lucide-react';
import DailyStatusCard from '@/components/DailyStatusCard';
import EconomicEventCard from './EconomicEventCard';
import EconomicEventHistory from './EconomicEventHistory';
import EconomicCalendar from './EconomicCalendar';
import BitcoinHoldingsChart from '@/components/BitcoinHoldingsChart';
import StockIndexCard from '@/components/StockIndexCard';
import NewsCard from '@/components/NewsCard';
import miningHoldings from '../data/mining-holdings.json';

// Mock Polymarket data
const MOCK_POLYMARKET_BETS = [
  {
    id: '1',
    title: 'Bitcoin > $100,000 by end of 2026',
    description: 'Market sentiment remains bullish as institutional adoption accelerates',
    volume: '$125M',
    yes: '65%',
    end: '2026-12-31',
    category: 'Crypto',
    hot: true,
  },
  {
    id: '2',
    title: 'Fed Rate Cut to 3.75% in Q3 2026',
    description: 'Cooling inflation data supports additional monetary easing',
    volume: '$45M',
    yes: '58%',
    end: '2026-09-30',
    category: 'Macro',
    hot: true,
  },
  {
    id: '3',
    title: 'US GDP Growth > 3% in 2026',
    description: 'Strong consumer spending and business investment',
    volume: '$32M',
    yes: '52%',
    end: '2026-12-31',
    category: 'Macro',
    hot: true,
  },
  {
    id: '4',
    title: 'Ethereum ETF Approval by SEC',
    description: 'Institutional demand expected to drive price higher',
    volume: '$28M',
    yes: '71%',
    end: '2026-06-30',
    category: 'Crypto',
    hot: true,
  },
  {
    id: '5',
    title: 'S&P 500 Hits 5,500',
    description: 'Tech sector leads gains amid AI boom',
    volume: '$89M',
    yes: '48%',
    end: '2026-11-30',
    category: 'Stock Market',
    hot: true,
  },
  {
    id: '6',
    title: 'China Reopens Economy by Q3 2026',
    description: 'Stimulus measures expected to boost global growth',
    volume: '$18M',
    yes: '55%',
    end: '2026-09-30',
    category: 'Macro',
    hot: true,
  },
];

export default function PolymarketBets() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading
    setTimeout(() => setLoading(false), 500);
  }, []);

  return (
    <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Flame className="w-6 h-6 text-orange-500" />
          <h2 className="text-2xl font-bold">
            Top Hottest Economy-Related Bets
          </h2>
        </div>
        <span className="text-sm bg-orange-500/20 text-orange-400 px-2 py-1 rounded">
          From Polymarket
        </span>
      </div>

      {loading ? (
        <div className="text-center py-12">
          <TrendingUp className="w-8 h-8 animate-pulse mx-auto text-orange-500" />
          <p className="text-gray-400 mt-4">Loading hottest bets...</p>
        </div>
      ) : (
        <div className="space-y-4">
          {MOCK_POLYMARKET_BETS.slice(0, 3).map((bet) => (
            <div key={bet.id} className="bg-gray-700/50 rounded-lg p-5 border border-gray-600 hover:border-orange-500/30 transition-colors">
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-xs bg-red-500/20 text-red-400 px-2 py-1 rounded flex items-center gap-1">
                      <Flame className="w-3 h-3" />
                      {bet.category}
                    </span>
                    {bet.hot && (
                      <span className="text-xs bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded">
                        🔥 Hot
                      </span>
                    )}
                  </div>
                  <h3 className="text-lg font-bold text-white">{bet.title}</h3>
                  <p className="text-gray-400 text-sm mt-2">{bet.description}</p>
                </div>
                <div className="text-right ml-4">
                  <Target className="w-5 h-5 text-blue-400 opacity-50" />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-3 text-sm mt-4">
                <div>
                  <p className="text-gray-400 text-xs mb-1">Volume</p>
                  <p className="font-semibold text-purple-400">{bet.volume}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-xs mb-1">Yes Vote</p>
                  <p className={`font-semibold ${Number(bet.yes) > 60 ? 'text-green-400' : 'text-yellow-400'}`}>
                    {bet.yes}%
                  </p>
                </div>
                <div>
                  <p className="text-gray-400 text-xs mb-1">Target Date</p>
                  <p className="font-semibold text-blue-400">{bet.end}</p>
                </div>
              </div>

              <div className="mt-4 flex items-center gap-2">
                <div className="flex-1 bg-gray-900 rounded-lg h-2 overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-green-500 to-green-400 rounded-full transition-all"
                    style={{ width: `${bet.yes}%` }}
                  />
                </div>
                <span className="text-xs text-gray-400">Yes</span>
                <div className="flex-1 bg-gray-900 rounded-lg h-2 overflow-hidden">
                  <div 
                    className="h-full bg-gradient-to-r from-red-500 to-red-400 rounded-full transition-all"
                    style={{ width: `${100 - Number(bet.yes)}%` }}
                  />
                </div>
                <span className="text-xs text-gray-400">No</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
