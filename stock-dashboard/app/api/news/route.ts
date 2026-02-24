import { NextResponse } from 'next/server';

// Sample news data as fallback
const SAMPLE_NEWS = [
  {
    title: 'Bitcoin Holds Strong Above $67,000 as Institutional Adoption Continues',
    description: 'Major financial institutions continue to increase their Bitcoin holdings amid growing market confidence.',
    url: 'https://coingecko.com/news/bitcoin-holds-strong-above-67000',
    published_at: new Date().toISOString(),
    thumbnail: null,
  },
  {
    title: 'MicroStrategy Increases Bitcoin Treasury Holdings',
    description: 'The software company adds more Bitcoin to its balance sheet, cementing its position as the largest corporate holder.',
    url: 'https://coingecko.com/news/microstrategy-increases-bitcoin-holdings',
    published_at: new Date(Date.now() - 3600000).toISOString(),
    thumbnail: null,
  },
  {
    title: 'Ethereum Layer 2 Solutions See Record Transaction Volumes',
    description: 'Scalability solutions on the Ethereum network continue to gain traction among users and developers.',
    url: 'https://coingecko.com/news/ethereum-layer2-solutions-gain-traction',
    published_at: new Date(Date.now() - 7200000).toISOString(),
    thumbnail: null,
  },
];

export async function GET() {
  try {
    // Fetch crypto news from CoinGecko
    const response = await fetch('https://api.coingecko.com/api/v3/news', {
      next: { revalidate: 300 }, // Cache for 5 minutes
    });

    if (!response.ok) {
      throw new Error(`CoinGecko News API failed: ${response.status}`);
    }

    const data = await response.json();

    // Check if we have data
    if (!data || !data.data || !Array.isArray(data.data)) {
      console.log('No news data from CoinGecko, using samples');
      return NextResponse.json(SAMPLE_NEWS);
    }

    // Filter for relevant news (MicroStrategy, Bitcoin, Ethereum, Mining)
    const filteredNews = data.data
      .filter((item: any) => {
        const title = item.title?.toLowerCase() || '';
        const description = item.description?.toLowerCase() || '';
        const keywords = [
          'microstrategy',
          'bitmine',
          'bitcoin',
          'ethereum',
          'mining',
          'crypto',
          'mstr',
          'btc',
          'eth',
        ];
        return keywords.some((keyword) =>
          title.includes(keyword) || description.includes(keyword)
        );
      })
      .slice(0, 10)
      .map((item: any) => ({
        title: item.title || 'No title',
        description: (item.description?.slice(0, 200) || 'No description available') + '...',
        url: item.url || '#',
        published_at: item.published_at || new Date().toISOString(),
        thumbnail: item.thumb || null,
      }));

    // If no relevant news found, return samples
    if (filteredNews.length === 0) {
      console.log('No relevant news found, using samples');
      return NextResponse.json(SAMPLE_NEWS);
    }

    return NextResponse.json(filteredNews);
  } catch (error) {
    console.error('News API error:', error);
    // Return sample news on any error
    return NextResponse.json(SAMPLE_NEWS);
  }
}
