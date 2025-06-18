# reddit.py

import config
import praw
import re
from datetime import datetime, timedelta
from stocks_utils import load_tickers

TICKER_REGEX = re.compile(r"\b[A-Z]{2,5}\b")
BLOCKED_TICKERS = {
    "CEO", "CFO", "IPO", "USA", "ETF", "FBI", "SEC", "IRS", "YOLO",
    "AI", "ML", "GDP", "USD", "BUY", "SELL", "CALL", "PUT", "MOON"
}

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

    # 📅 Rolling 24-hour window
    time_threshold = datetime.utcnow() - timedelta(hours=24)

    for subreddit_name in config.SUBREDDITS:
        subreddit = reddit.subreddit(subreddit_name)
        posts = subreddit.hot(limit=limit_per_sub)
        sub_results = []

        for post in posts:
            if post.over_18:
                continue

            post_time = datetime.utcfromtimestamp(post.created_utc)
            if post_time < time_threshold:
                continue

            full_text = f"{post.title}\n\n{post.selftext or ''}".strip()

            # 📥 Extract top 10 comments
            post.comments.replace_more(limit=0)
            comments = [c.body.strip() for c in post.comments[:10] if hasattr(c, "body")]
            combined_text = f"{post.title} {post.selftext or ''} {' '.join(comments)}"
            valid_ticker_list = extract_valid_tickers_from_text(combined_text, load_tickers().keys())

            if valid_ticker_list:
                sub_results.append({
                    "title": post.title.strip(),
                    "text": full_text,
                    "summary": "",  # GPT-generated summary can go here
                    "subreddit": subreddit_name,
                    "url": f"https://www.reddit.com{post.permalink}",
                    "created_utc": post_time.isoformat() + "Z",
                    "comments": comments,
                    "tickers": valid_ticker_list
                })

        print(f"✅ r/{subreddit_name}: {len(sub_results)} posts in past 24h")
        results.extend(sub_results)

    return results

def extract_valid_tickers_from_text(text, valid_tickers):
    found = TICKER_REGEX.findall(text)  # Don't .upper() the whole thing
    return list({
        t for t in found
        if t == t.upper() and t in valid_tickers and t not in BLOCKED_TICKERS
    })








