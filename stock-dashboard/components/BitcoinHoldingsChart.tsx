'use client';

import { Line, LineChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import { Card } from '@/app/ui/card';

interface BitcoinHoldingsChartProps {
  history: { date: string; bitcoin: number }[];
}

export default function BitcoinHoldingsChart({ history }: BitcoinHoldingsChartProps) {
  const chartData = history.map((entry) => ({
    date: entry.date,
    bitcoin: entry.bitcoin,
  }));

  return (
    <Card className="bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h3 className="text-xl font-bold mb-4">MicroStrategy Bitcoin Holdings History</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <XAxis
            dataKey="date"
            stroke="#9ca3af"
            fontSize={12}
            tickFormatter={(value) => new Date(value).toLocaleDateString('en-US', { month: 'short', year: '2-digit' })}
          />
          <YAxis
            stroke="#9ca3af"
            fontSize={12}
            tickFormatter={(value) => `${(value / 1000).toFixed(0)}K`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1f2937',
              border: '1px solid #374151',
              borderRadius: '0.5rem',
            }}
            labelFormatter={(value) => new Date(value).toLocaleDateString()}
            formatter={(value) => [value ? value.toLocaleString() + ' BTC' : '0 BTC', 'Holdings']}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="bitcoin"
            stroke="#f97316"
            strokeWidth={2}
            dot={{ fill: '#f97316', strokeWidth: 2, r: 4 }}
            activeDot={{ r: 6 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </Card>
  );
}
