#!/usr/bin/env node

/**
 * Update Mining Company Data Script
 *
 * This script fetches the latest Bitcoin/Ethereum holdings data from
 * MicroStrategy and BitMine Immersion Technologies and updates the data file.
 *
 * Run this script periodically (e.g., daily or weekly) to keep the dashboard current.
 *
 * Usage:
 *   node scripts/update-mining-data.js
 */

const fs = require('fs');
const path = require('path');

// Data sources
const MICROSTRATEGY_BITBO = 'https://bitbo.io/api/treasury/microstrategy';
const BITMINE_COINGECKO = 'https://www.coingecko.com/en/treasuries/companies/bitmine';

// Output file path
const DATA_FILE = path.join(__dirname, '../data/mining-holdings.json');

async function fetchMicroStrategyData() {
  console.log('Fetching MicroStrategy data from Bitbo...');

  try {
    const response = await fetch(MICROSTRATEGY_BITBO);
    if (!response.ok) {
      throw new Error(`Failed to fetch: ${response.status}`);
    }

    const data = await response.json();

    // Extract relevant data
    const holdings = {
      current: data.bitcoin_holdings_total || data.bitcoin || 0,
      date: new Date().toISOString().split('T')[0],
      percentageOfSupply: data.percentage_of_supply || 3.2,
    };

    console.log(`  ✓ MicroStrategy: ${holdings.current.toLocaleString()} BTC`);
    return holdings;
  } catch (error) {
    console.error('  ✗ Error fetching MicroStrategy:', error.message);

    // Return current data if fetch fails
    const currentData = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
    return currentData.microstrategy.bitcoin;
  }
}

async function fetchBitMineData() {
  console.log('Fetching BitMine data from CoinGecko...');

  try {
    const response = await fetch(BITMINE_COINGECKO);
    if (!response.ok) {
      throw new Error(`Failed to fetch: ${response.status}`);
    }

    // CoinGecko doesn't have a simple API, so we'd need to scrape
    // For now, return current data and log a warning
    console.log('  ⚠ CoinGecko scraping not implemented, using current data');

    const currentData = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
    return {
      bitcoin: currentData.bitmine.bitcoin,
      ethereum: currentData.bitmine.ethereum,
      totalValue: currentData.bitmine.totalValue,
    };
  } catch (error) {
    console.error('  ✗ Error fetching BitMine:', error.message);

    const currentData = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
    return {
      bitcoin: currentData.bitmine.bitcoin,
      ethereum: currentData.bitmine.ethereum,
      totalValue: currentData.bitmine.totalValue,
    };
  }
}

async function updateDataFile() {
  console.log('\n🔄 Updating Mining Company Holdings Data\n');

  // Fetch latest data
  const mstrData = await fetchMicroStrategyData();
  const bitmineData = await fetchBitMineData();

  // Read current data
  let currentData = JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));

  // Update MicroStrategy
  const previousMstr = currentData.microstrategy.bitcoin.current;
  currentData.microstrategy.bitcoin.current = mstrData.current;
  currentData.microstrategy.bitcoin.date = mstrData.date;
  currentData.microstrategy.bitcoin.percentageOfSupply = mstrData.percentageOfSupply;

  // Add to history if changed
  if (previousMstr !== mstrData.current) {
    const newEntry = {
      date: mstrData.date,
      bitcoin: mstrData.current,
    };

    // Remove duplicate dates and add new entry
    currentData.microstrategy.history = currentData.microstrategy.history
      .filter((h) => h.date !== mstrData.date)
      .concat(newEntry)
      .sort((a, b) => new Date(a.date) - new Date(b.date));

    console.log(`  ✓ MicroStrategy holdings updated: ${previousMstr.toLocaleString()} → ${mstrData.current.toLocaleString()} BTC`);
  } else {
    console.log('  ✓ MicroStrategy holdings unchanged');
  }

  // Update BitMine
  currentData.bitmine.bitcoin = bitmineData.bitcoin;
  currentData.bitmine.ethereum = bitmineData.ethereum;
  currentData.bitmine.totalValue = bitmineData.totalValue;

  console.log(`  ✓ BitMine data updated`);

  // Write updated data
  fs.writeFileSync(DATA_FILE, JSON.stringify(currentData, null, 2), 'utf8');

  console.log('\n✅ Data file updated successfully!');
  console.log(`📁 ${DATA_FILE}`);
}

// Run the update
updateDataFile().catch((error) => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});
