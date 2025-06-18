# main.py
from reddit import fetch_stock_mentions
from stocks_utils import download_and_save_tickers, update_ticker_score
from dotenv import load_dotenv
import os
from chat_gpt import extract_real_tickers_with_sentiment

load_dotenv()

def main():
    download_and_save_tickers()
    posts = fetch_stock_mentions(limit_per_sub=5)
    print(f"📥 Collected {len(posts)} posts.\n")

    for post in posts:
        print(f"🔎 Analyzing post from r/{post['subreddit']}: {post['title'][:60]}...")
        print(f"🔗 {post['url']}")
        
        tickers_with_data = extract_real_tickers_with_sentiment(post)

        if not tickers_with_data:
            print("⚠️ No clear stock tickers found.\n")
            continue

        for ticker, info in tickers_with_data.items():
            company = info.get("company", "Unknown Company")
            sentiment = info.get("sentiment", "unknown")
            print(f"✅ {ticker} — {company} ({sentiment})")

        print("—" * 60)


if __name__ == "__main__":
    main()

