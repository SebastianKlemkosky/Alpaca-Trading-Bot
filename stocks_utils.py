import requests
import os
import json
from datetime import datetime

NASDAQ_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
OTHER_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"
TICKER_FILE = r"Stocks/tickers.json"

def download_and_save_tickers(filepath=TICKER_FILE):
    # Load existing tickers (if any)
    existing_data = {}
    if os.path.exists(filepath):
        try:
            with open(filepath, "r") as f:
                existing_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load existing tickers for merge: {e}")

    ticker_map = {k: v for k, v in existing_data.items() if k != "__meta__"}

    # Fetch from NASDAQ & OTHER
    for url in [NASDAQ_URL, OTHER_URL]:
        try:
            response = requests.get(url)
            response.raise_for_status()
            lines = response.text.strip().split("\n")

            for line in lines[1:-1]:
                parts = line.split("|")
                if len(parts) >= 2:
                    symbol = parts[0].strip().upper()
                    raw_name = parts[1].strip()

                    if symbol.isalpha() and symbol not in ticker_map:
                        if " - " in raw_name:
                            name, share_type = raw_name.split(" - ", 1)
                        else:
                            name, share_type = raw_name, ""

                        ticker_map[symbol] = {
                            "name": name.strip(),
                            "type": share_type.strip(),
                            "score": 0,
                            "high": 0,
                            "low": 0,
                            "occurrences": 0,
                            "last_updated": None
                        }

        except Exception as e:
            print(f"⚠️ Failed to fetch from {url}: {e}")

    if not ticker_map:
        print("❌ No tickers loaded.")
        return {}

    # Add/replace metadata timestamp
    ticker_map["__meta__"] = {
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }

    try:
        with open(filepath, "w") as f:
            json.dump(ticker_map, f, indent=2)
        print(f"✅ Merged and saved {len(ticker_map) - 1} tickers to {filepath}")
    except Exception as e:
        print(f"⚠️ Failed to save tickers to file: {e}")

    return ticker_map

def load_tickers(filepath=TICKER_FILE):
    if not os.path.exists(filepath):
        print("📥 Ticker file not found. Downloading fresh list...")
        return download_and_save_tickers(filepath)

    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Failed to load tickers: {e}")
        return {}

def update_ticker_score(ticker, delta, filepath=TICKER_FILE):
    data = load_tickers(filepath)

    if ticker not in data:
        print(f"⚠️ Ticker {ticker} not found in data.")
        return

    entry = data[ticker]
    entry["score"] += delta
    entry["occurrences"] += 1
    entry["last_updated"] = datetime.utcnow().isoformat() + "Z"

    if entry["score"] > entry.get("high", entry["score"]):
        entry["high"] = entry["score"]

    if entry["score"] < entry.get("low", entry["score"]):
        entry["low"] = entry["score"]

    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Updated score for {ticker}: {entry['score']}")
    except Exception as e:
        print(f"❌ Failed to update ticker score: {e}")
