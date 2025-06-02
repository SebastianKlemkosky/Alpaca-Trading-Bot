# main.py

import config
from reddit import fetch_stock_mentions
from dotenv import load_dotenv
import os
from stocks_utils import load_tickers

load_dotenv()

def main():
    posts = fetch_stock_mentions(limit_per_sub=5)
    print(f"📥 Collected {len(posts)} posts from Reddit today.\n")

    for post in posts:
        print(f"r/{post['subreddit']} | {post['created_utc']}")
        print(f"Title: {post['title']}")
        print(f"URL: {post['url']}")
        print(f"Text: {post['text'][:150]}...")  # Truncate long text
        print("—" * 60)


if __name__ == "__main__":
    main()


# TODO: Enhance tickers.json entries to include:
#       - points: running sentiment score
#       - high: all-time high score
#       - low: all-time low score
#       - last_updated: ISO timestamp of last change
#       - occurrences: count of mentions across Reddit posts

# TODO: Parse multiple subreddits daily from config.SUBREDDITS

# TODO: Extract Reddit post title, selftext, and top 10 comments

# TODO: Use ChatGPT to classify sentiment for each post (or for each mentioned stock)

# TODO: Assign point values per stock:
#       e.g., +2 = strong positive, +1 = neutral, -1 = negative

# TODO: Upsert point values to persistent stock_scores.json or DB
#       Structure:
#       {
#           "TSLA": {
#               "score": 17,
#               "last_updated": "2025-06-02",
#               "history": [{"date": "2025-06-01", "delta": +3}, ...]
#           },
#           ...
#       }

# TODO: Decide on score retention policy:
#       Option A: Keep score forever (accumulate)
#       Option B: Apply weekly decay
#       Option C: Reset scores every 2 weeks
#       → (Current plan: always keep score, no reset)

# TODO: Every 2 weeks (payday trigger):
#       - Filter stocks with score ≥ threshold (e.g., 5)
#       - Rank top 10 by score
#       - Allocate $100 across stocks proportionally
#       - Execute trades via Alpaca API

# TODO: Log trades with ticker, score, amount invested, share price, date

# TODO: Optional: Store raw Reddit data and sentiment outputs in JSON file daily (e.g., reddit_dump_YYYY-MM-DD.json)

# TODO: Optional: Add CLI flags or config switches (dry-run, simulate, threshold override)


# TODO (NICE TO HAVE): Manual signal adjustment framework
#       - Allow manual entry of events, signals, or influencer trades
#       - Attach + or - point weights to specific tickers (e.g., "Elon tweets TSLA" → +3)

# TODO (NICE TO HAVE): Track multi-subreddit impact
#       - If a stock appears in multiple subreddits on the same day, apply bonus weight
#       - Example: "TSLA mentioned in r/stocks and r/wallstreetbets" → +2 extra points

# TODO (NICE TO HAVE): Create an interface (CLI or simple JSON input) to inject manual news/events
#       Structure:
#       {
#           "ticker": "NVDA",
#           "reason": "NVIDIA keynote hype",
#           "points": +3,
#           "source": "manual",
#           "date": "2025-06-02"
#       }

# TODO (NICE TO HAVE): Allow overrides or boosts to scores in stock_scores.json
#       → Manual scores should still be tracked in history for transparency
