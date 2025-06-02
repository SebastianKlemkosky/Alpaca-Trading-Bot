import requests
import os
import json
from datetime import datetime

NASDAQ_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
OTHER_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"
TICKER_FILE = r"Stocks/tickers.json"

def download_and_save_tickers(filepath=TICKER_FILE):
    ticker_map = {}

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

                    if symbol.isalpha():
                        if " - " in raw_name:
                            name, share_type = raw_name.split(" - ", 1)
                        else:
                            name, share_type = raw_name, ""

                        ticker_map[symbol] = {
                            "name": name.strip(),
                            "type": share_type.strip()
                        }

        except Exception as e:
            print(f"⚠️ Failed to fetch from {url}: {e}")

    if not ticker_map:
        print("❌ No tickers downloaded.")
        return {}

    # Add timestamp metadata
    ticker_map["__meta__"] = {
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }

    try:
        with open(filepath, "w") as f:
            json.dump(ticker_map, f, indent=2)
        print(f"✅ Saved {len(ticker_map)-1} tickers to {filepath}")
    except Exception as e:
        print(f"⚠️ Failed to save tickers to file: {e}")

    return ticker_map


def load_tickers(filepath=TICKER_FILE):
    print("📥 Refreshing ticker list from NASDAQ/NYSE...")
    return download_and_save_tickers(filepath)

