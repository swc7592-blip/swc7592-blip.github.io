'use client';

import { Line, LineChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend, CartesianGrid } from 'recharts';
import { X, TrendingUp, TrendingDown } from 'lucide-react';

interface EconomicEventHistoryProps {
  indicator: string;
  history: Array<{ date: string; actual: string; forecast: string }>;
  onClose: () => void;
}

export default function EconomicEventHistory({ indicator, history, onClose }: EconomicEventHistoryProps) {
  // Convert string values to numbers for chart
  const chartData = history.map((item) => ({
    date: item.date,
    actual: parseFloat(item.actual.replace('%', '').replace('K', '')) || 0,
    forecast: parseFloat(item.forecast.replace('%', '').replace('K', '')) || 0,
  }));

  return (
    <div className="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4">
      <div className="bg-gray-800 rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-gray-800 border-b border-gray-700 p-6 rounded-t-2xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <X className="w-8 h-8 text-blue-500" />
              <div>
                <h2 className="text-2xl font-bold">{indicator}</h2>
                <p className="text-gray-400 text-sm">Historical Actual vs Forecast</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          {/* Chart */}
          <div className="bg-gray-900 rounded-xl p-6 mb-6">
            <h3 className="text-lg font-semibold mb-4">Historical Comparison</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis
                  dataKey="date"
                  stroke="#9ca3af"
                  fontSize={12}
                  tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                />
                <YAxis
                  stroke="#9ca3af"
                  fontSize={12}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: '1px solid #374151',
                    borderRadius: '0.5rem',
                  }}
                  labelFormatter={(value) => new Date(value).toLocaleDateString()}
                  formatter={(value?: number, name?: string) => {
                    return value !== undefined ? [value, name === 'actual' ? 'Actual' : 'Forecast'] : ['--', name === 'actual' ? 'Actual' : 'Forecast'];
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="actual"
                  stroke="#22c55e"
                  strokeWidth={2}
                  dot={{ fill: '#22c55e', strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6 }}
                  name="Actual"
                />
                <Line
                  type="monotone"
                  dataKey="forecast"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6 }}
                  name="Forecast"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* History Table */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Historical Data</h3>
            <div className="bg-gray-900 rounded-xl overflow-hidden">
              <table className="w-full text-sm">
                <thead>
                  <tr className="bg-gray-800">
                    <th className="px-4 py-3 text-left text-gray-400">Date</th>
                    <th className="px-4 py-3 text-right text-gray-400">Forecast</th>
                    <th className="px-4 py-3 text-right text-gray-400">Actual</th>
                    <th className="px-4 py-3 text-center text-gray-400">Difference</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((item, index) => {
                    const actual = parseFloat(item.actual.replace('%', '').replace('K', '')) || 0;
                    const forecast = parseFloat(item.forecast.replace('%', '').replace('K', '')) || 0;
                    const diff = actual - forecast;
                    const isPositive = diff >= 0;

                    return (
                      <tr key={index} className="border-t border-gray-800 hover:bg-gray-800/50">
                        <td className="px-4 py-3 text-gray-300">
                          {new Date(item.date).toLocaleDateString('en-US', {
                            month: 'short',
                            day: 'numeric',
                            year: 'numeric',
                          })}
                        </td>
                        <td className="px-4 py-3 text-right text-blue-400">{item.forecast}</td>
                        <td className="px-4 py-3 text-right text-green-400 font-semibold">
                          {item.actual}
                        </td>
                        <td className="px-4 py-3 text-center">
                          {diff === 0 ? (
                            <span className="text-gray-500">-</span>
                          ) : isPositive ? (
                            <span className="flex items-center justify-center gap-1 text-green-400">
                              <TrendingUp className="w-4 h-4" />
                              {diff.toFixed(1)}
                            </span>
                          ) : (
                            <span className="flex items-center justify-center gap-1 text-red-400">
                              <TrendingDown className="w-4 h-4" />
                              {diff.toFixed(1)}
                            </span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
