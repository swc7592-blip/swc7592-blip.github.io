'use client';

import { useState, useEffect } from 'react';
import { Calendar, RefreshCw, Loader2, Bitcoin, Wallet, TrendingUp, Newspaper } from 'lucide-react';
import DailyStatusCard from '@/components/DailyStatusCard';
import EconomicEventCard from '@/components/EconomicEventCard';
import EconomicEventHistory from '@/components/EconomicEventHistory';
import BitcoinHoldingsChart from '@/components/BitcoinHoldingsChart';
import StockIndexCard from '@/components/StockIndexCard';
import NewsCard from '@/components/NewsCard';
import miningHoldings from '../data/mining-holdings.json';
import { Clock } from 'lucide-react';

export default function Home() {
  const [cryptoPrices, setCryptoPrices] = useState<any>(null);
  const [stockIndexes, setStockIndexes] = useState<any[]>([]);
  const [news, setNews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [cryptoRes, stockRes, newsRes] = await Promise.allSettled([
        fetch('/api/crypto-prices'),
        fetch('/api/stock-indexes'),
        fetch('/api/news'),
      ]);

      // Process crypto prices
      if (cryptoRes.status === 'fulfilled') {
        const cryptoData = await cryptoRes.value.json();
        setCryptoPrices(cryptoData);
      } else {
        console.error('Crypto API failed:', cryptoRes.reason);
      }

      // Process stock indexes
      if (stockRes.status === 'fulfilled') {
        const stockData = await stockRes.value.json();
        setStockIndexes(stockData);
      } else {
        console.error('Stock API failed:', stockRes.reason);
      }

      // Process news
      if (newsRes.status === 'fulfilled') {
        const newsData = await newsRes.value.json();
        setNews(newsData);
      } else {
        console.error('News API failed:', newsRes.reason);
      }

      setLastUpdate(new Date());
    } catch (error) {
      console.error('Error fetching data:', error);
      setError('Some data failed to load. Please try refreshing.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();

    // Auto-refresh every 5 minutes
    const interval = setInterval(fetchData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const btcPrice = cryptoPrices?.bitcoin?.usd || 0;
  const btcChange = cryptoPrices?.bitcoin?.usd_24h_change || 0;
  const ethPrice = cryptoPrices?.ethereum?.usd || 0;
  const ethChange = cryptoPrices?.ethereum?.usd_24h_change || 0;

  const mstrTotalValue = miningHoldings.microstrategy.bitcoin.current * btcPrice;
  const bitmineTotalValue =
    miningHoldings.bitmine.bitcoin * btcPrice +
    miningHoldings.bitmine.ethereum.current * ethPrice +
    miningHoldings.bitmine.totalValue;

  return (
    <main className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="border-b border-gray-800 p-6 sticky top-0 bg-gray-900/95 backdrop-blur-sm z-10">
        <div className="container mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3">
              <Bitcoin className="w-8 h-8 text-orange-500" />
              Woo Chang - Crypto & Stock Dashboard
            </h1>
            <p className="text-gray-400 mt-1">
              Real-time tracking of economic indicators, crypto prices, and stock indexes
            </p>
            <div className="flex items-center gap-4 mt-2 text-sm">
              <p className="text-blue-400">
                📅 Current Date: {new Date().toLocaleDateString('ko-KR', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })}
              </p>
              {lastUpdate && (
                <p className="text-gray-400 flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  Last Update: {lastUpdate.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                </p>
              )}
            </div>
          </div>
          <button
            onClick={fetchData}
            disabled={loading}
            className="flex items-center gap-2 bg-gray-800 hover:bg-gray-700 px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
            Refresh
          </button>
        </div>
      </header>

      {/* Error Message */}
      {error && (
        <div className="container mx-auto mt-6">
          <div className="bg-red-900/20 border border-red-700 text-red-400 px-4 py-3 rounded-lg">
            {error}
          </div>
        </div>
      )}

      {/* Content */}
      <div className="container mx-auto p-6 space-y-8">
        {/* Economic Calendar - TOP SECTION */}
        <EconomicCalendar />

        {/* Daily Status Cards - SECOND SECTION */}
        <div>
          <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
            <TrendingUp className="w-6 h-6" />
            Daily Market Status
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <DailyStatusCard
              name="Bitcoin"
              symbol="BTC"
              price={btcPrice}
              change={btcPrice * (btcChange / 100)}
              changePercent={btcChange}
              currency="USD"
              icon={<Bitcoin className="w-6 h-6 text-orange-500" />}
              lastUpdate={lastUpdate || undefined}
            />
            <DailyStatusCard
              name="Ethereum"
              symbol="ETH"
              price={ethPrice}
              change={ethPrice * (ethChange / 100)}
              changePercent={ethChange}
              currency="USD"
              icon={<Wallet className="w-6 h-6 text-purple-500" />}
              lastUpdate={lastUpdate || undefined}
            />
          </div>
        </div>

        {/* Live Prices & Stats - THIRD SECTION */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">MSTR Total Value</p>
                <p className="text-2xl font-bold text-blue-400 mt-1">
                  ${(mstrTotalValue / 1000000000).toFixed(2)}B
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  714,644 BTC
                </p>
              </div>
              <Bitcoin className="w-10 h-10 text-blue-500 opacity-20" />
            </div>
          </div>

          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">BitMine Total Value</p>
                <p className="text-2xl font-bold text-green-400 mt-1">
                  ${(bitmineTotalValue / 1000000000).toFixed(2)}B
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  4,325,739 ETH + 193 BTC
                </p>
              </div>
              <TrendingUp className="w-10 h-10 text-green-500 opacity-20" />
            </div>
          </div>
        </div>

        {/* Stock Indexes - FOURTH SECTION */}
        {stockIndexes.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <TrendingUp className="w-6 h-6" />
              Stock Market Indexes
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {stockIndexes.map((index) => (
                <StockIndexCard key={index.symbol} {...index} lastUpdate={lastUpdate} />
              ))}
            </div>
          </div>
        )}

        {/* MicroStrategy Section with Chart - FIFTH SECTION */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
            <h2 className="text-2xl font-bold mb-4">
              {miningHoldings.microstrategy.name}
            </h2>
            <div className="space-y-4">
              <div className="bg-gray-700/50 rounded-lg p-4">
                <p className="text-gray-400 text-sm">Bitcoin Holdings</p>
                <p className="text-4xl font-bold text-orange-400 mt-1">
                  {miningHoldings.microstrategy.bitcoin.current.toLocaleString()} BTC
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  {miningHoldings.microstrategy.bitcoin.percentageOfSupply}% of total supply
                </p>
              </div>

              <div className="bg-gray-700/50 rounded-lg p-4">
                <p className="text-gray-400 text-sm">Current Value</p>
                <p className="text-3xl font-bold text-green-400 mt-1">
                  ${(mstrTotalValue / 1000000000).toFixed(2)}B
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  @ ${btcPrice.toLocaleString()} per BTC
                </p>
              </div>

              <div className="bg-gray-700/50 rounded-lg p-4">
                <p className="text-gray-400 text-sm">Data Sources</p>
                <a
                  href={miningHoldings.microstrategy.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:underline text-sm mt-1 block"
                >
                  Official Website →
                </a>
                <a
                  href={miningHoldings.microstrategy.dataSource}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:underline text-sm"
                >
                  Bitbo Treasury →
                </a>
              </div>
            </div>
          </div>

          <BitcoinHoldingsChart history={miningHoldings.microstrategy.history} />
        </div>

        {/* BitMine Section - SIXTH SECTION */}
        <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
          <h2 className="text-2xl font-bold mb-6">
            {miningHoldings.bitmine.name}
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-gray-700/50 rounded-lg p-4">
              <p className="text-gray-400 text-sm">Bitcoin</p>
              <p className="text-3xl font-bold text-orange-400 mt-1">
                {miningHoldings.bitmine.bitcoin} BTC
              </p>
              <p className="text-sm text-gray-500 mt-1">
                ${(miningHoldings.bitmine.bitcoin * btcPrice).toLocaleString()}
              </p>
            </div>

            <div className="bg-gray-700/50 rounded-lg p-4">
              <p className="text-gray-400 text-sm">Ethereum</p>
              <p className="text-3xl font-bold text-purple-400 mt-1">
                {miningHoldings.bitmine.ethereum.current.toLocaleString()} ETH
              </p>
              <p className="text-sm text-gray-500 mt-1">
                ${(miningHoldings.bitmine.ethereum.current * ethPrice).toLocaleString()}
              </p>
            </div>

            <div className="bg-gray-700/50 rounded-lg p-4">
              <p className="text-gray-400 text-sm">Total Crypto Value</p>
              <p className="text-3xl font-bold text-green-400 mt-1">
                ${((miningHoldings.bitmine.bitcoin * btcPrice +
                  miningHoldings.bitmine.ethereum.current * ethPrice) / 1000000000).toFixed(2)}B
              </p>
            </div>

            <div className="bg-gray-700/50 rounded-lg p-4">
              <p className="text-gray-400 text-sm">Total Treasury</p>
              <p className="text-3xl font-bold text-blue-400 mt-1">
                ${(bitmineTotalValue / 1000000000).toFixed(2)}B
              </p>
              <p className="text-sm text-gray-500 mt-1">
                Incl. cash & investments
              </p>
            </div>
          </div>

          <div className="mt-6 flex gap-4">
            <a
              href={miningHoldings.bitmine.website}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:underline text-sm"
            >
              Official Website →
            </a>
            <a
              href={miningHoldings.bitmine.dataSource}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:underline text-sm"
            >
              CoinGecko Treasury →
            </a>
          </div>
        </div>

        {/* News Section - SEVENTH SECTION */}
        {news.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <Newspaper className="w-6 h-6" />
              Latest News
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {news.map((item, index) => (
                <NewsCard key={index} {...item} />
              ))}
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center text-gray-500 text-sm py-8 border-t border-gray-800">
          <p>
            Last updated: {lastUpdate ? lastUpdate.toLocaleString() : 'Loading...'}
          </p>
          <p className="mt-2">
            Data from CoinGecko, Yahoo Finance, Bitbo, and official company sources
          </p>
        </div>
      </div>
    </main>
  );
}

// Separate component for Economic Calendar
function EconomicCalendar() {
  const [period, setPeriod] = useState<'daily' | 'weekly' | 'monthly'>('daily');
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedEvent, setSelectedEvent] = useState<any>(null);
  const [eventHistory, setEventHistory] = useState<any>(null);

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/economic-calendar?period=${period}`);
      const data = await response.json();
      setEvents(data.events || []);
    } catch (error) {
      console.error('Error fetching economic calendar:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
  }, [period]);

  const handleEventClick = async (eventName: string) => {
    try {
      const response = await fetch(`/api/economic-calendar?indicator=${encodeURIComponent(eventName)}`);
      const data = await response.json();
      setSelectedEvent(eventName);
      setEventHistory(data);
    } catch (error) {
      console.error('Error fetching event history:', error);
    }
  };

  const tabs = [
    { id: 'daily' as const, label: 'Daily' },
    { id: 'weekly' as const, label: 'Weekly' },
    { id: 'monthly' as const, label: 'Monthly' },
  ];

  return (
    <>
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <Calendar className="w-6 h-6 text-blue-500" />
            <h2 className="text-2xl font-bold">
              {period.charAt(0).toUpperCase() + period.slice(1)} Economic Calendar
            </h2>
            <span className="text-sm bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded">
              High Importance Only (★★★)
            </span>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setPeriod(tab.id)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                period === tab.id
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Content */}
        {loading ? (
          <div className="text-center py-12">
            <Calendar className="w-8 h-8 animate-pulse mx-auto text-blue-500" />
            <p className="text-gray-400 mt-4">Loading economic calendar...</p>
          </div>
        ) : events.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {events.map((event) => (
              <EconomicEventCard
                key={event.id}
                {...event}
                onClick={() => handleEventClick(event.name)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <Calendar className="w-16 h-16 mx-auto text-gray-600 mb-4" />
            <p className="text-gray-400 text-lg">
              No high importance events scheduled for this {period}
            </p>
            <p className="text-gray-500 text-sm mt-2">
              Check back later for upcoming events
            </p>
          </div>
        )}
      </div>

      {/* History Modal */}
      {selectedEvent && eventHistory && (
        <EconomicEventHistory
          indicator={selectedEvent}
          history={eventHistory.history || []}
          onClose={() => {
            setSelectedEvent(null);
            setEventHistory(null);
          }}
        />
      )}
    </>
  );
}
