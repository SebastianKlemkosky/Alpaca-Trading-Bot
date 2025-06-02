# main.py

import config
from reddit import fetch_stock_mentions
from dotenv import load_dotenv
import os
from stocks_utils import load_tickers

load_dotenv()

def main():
    posts = fetch_stock_mentions(limit_per_sub=25)
    print(f"📥 Collected {len(posts)} posts from Reddit today.\n")

    for post in posts[:5]:
        print(f"r/{post['subreddit']} | {post['created_utc']}")
        print(f"Title: {post['title']}")
        print(f"URL: {post['url']}")
        print(f"Text: {post['text'][:150]}...")  # Truncate long text
        print("—" * 60)


if __name__ == "__main__":
    main()
