# reddit.py

import config
import praw
import re
from datetime import datetime, timezone
from stocks_utils import load_tickers

# Regex for uppercase words 2–5 letters (stock tickers)
TICKER_REGEX = re.compile(r"\b[A-Z]{2,5}\b")

def get_reddit_client():
    return praw.Reddit(
        client_id=config.REDDIT_CLIENT_ID,
        client_secret=config.REDDIT_CLIENT_SECRET,
        user_agent=config.REDDIT_USER_AGENT,
        username=config.REDDIT_USERNAME,
        password=config.REDDIT_PASSWORD
    )

def extract_valid_tickers_from_text(text, valid_tickers):
    found = TICKER_REGEX.findall(text.upper())
    return list({t for t in found if t in valid_tickers and t != "IPO"})


def fetch_stock_mentions(limit_per_sub=25):
    reddit = get_reddit_client()
    results = []
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    for subreddit_name in config.SUBREDDITS:
        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.hot(limit=limit_per_sub)

        for post in posts:
            if post.over_18:
                continue

            post_time = datetime.utcfromtimestamp(post.created_utc)
            if post_time < today_start:
                continue

            full_text = f"{post.title}\n\n{post.selftext or ''}".strip()

            results.append({
                "title": post.title.strip(),
                "text": full_text,
                "summary": "",  # Leave blank for now — GPT can populate this
                "subreddit": subreddit_name,
                "url": f"https://www.reddit.com{post.permalink}",
                "created_utc": post_time.isoformat() + "Z"
            })

    return results

