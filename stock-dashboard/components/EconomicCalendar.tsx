'use client';

import { useState, useEffect } from 'react';
import { Calendar, TrendingUp, X } from 'lucide-react';
import EconomicEventCard from './EconomicEventCard';
import EconomicEventHistory from './EconomicEventHistory';

export default function EconomicCalendar() {
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
              ★★★ (3 stars only)
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
            <TrendingUp className="w-8 h-8 animate-pulse mx-auto text-blue-500" />
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
              No 3-star events scheduled for this {period}
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
