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



"""