import { NextResponse } from 'next/server';

export async function GET() {
  try {
    const response = await fetch(
      'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,krw&include_24hr_change=true',
      {
        next: { revalidate: 60 }, // Cache for 60 seconds
      }
    );

    if (!response.ok) {
      throw new Error(`CoinGecko API failed: ${response.status}`);
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Crypto prices API error:', error);
    // Return cached data or default values on error
    return NextResponse.json({
      bitcoin: { usd: 0, usd_24h_change: 0, krw: 0, krw_24h_change: 0 },
      ethereum: { usd: 0, usd_24h_change: 0, krw: 0, krw_24h_change: 0 },
      error: 'Failed to fetch crypto prices',
    }, { status: 200 });
  }
}
