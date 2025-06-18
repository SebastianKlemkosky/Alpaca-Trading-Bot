# config.py
from dotenv import load_dotenv
import os

load_dotenv()

# Reddit
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")

# OpenAI
CHATGPT_SECRET = os.getenv("CHATGPT_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Subreddits and template remain as is
SUBREDDITS = [
    "stocks",
    "investing",
    "wallstreetbets"
]

GPT_TEMPLATE = """
You are an investment analyst reviewing Reddit posts about stocks.

Given the post content (title, body, and comments), identify:
1. Which tickers clearly refer to real companies (not slang or acronyms).
2. For each real stock, provide your opinion of the sentiment based on the content.

Respond in JSON format like this:
{{
  "TICKER": {{
    "company": "Company Name",
    "sentiment": "strongly positive"  // or strongly negative, somewhat positive, neutral, etc.
  }},
  ...
}}

Only include tickers clearly used in a stock-related context.

Reddit Post:
---
Title: {title}

Body:
{text}

Top Comments:
{comments}
---
"""

