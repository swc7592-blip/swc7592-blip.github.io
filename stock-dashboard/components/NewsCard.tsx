'use client';

import { ExternalLink, Clock } from 'lucide-react';

interface NewsCardProps {
  title: string;
  description: string;
  url: string;
  published_at: string;
  thumbnail?: string | null;
}

export default function NewsCard({ title, description, url, published_at, thumbnail }: NewsCardProps) {
  const timeAgo = new Date(published_at).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <a
      href={url}
      target="_blank"
      rel="noopener noreferrer"
      className="bg-gray-800 rounded-xl p-5 border border-gray-700 hover:border-gray-600 transition-all hover:bg-gray-700/50 block"
    >
      <div className="flex gap-4">
        {thumbnail && (
          <img
            src={thumbnail}
            alt="News thumbnail"
            className="w-24 h-24 object-cover rounded-lg flex-shrink-0"
          />
        )}
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold text-white mb-2 line-clamp-2">{title}</h4>
          <p className="text-sm text-gray-400 mb-3 line-clamp-2">{description}</p>
          <div className="flex items-center gap-2 text-xs text-gray-500">
            <Clock className="w-3 h-3" />
            <span>{timeAgo}</span>
            <ExternalLink className="w-3 h-3 ml-auto" />
          </div>
        </div>
      </div>
    </a>
  );
}
