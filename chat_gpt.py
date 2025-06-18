# chat_gpt.py

from openai import OpenAI, OpenAIError
import config
import json
from datetime import datetime
from pathlib import Path
import re

# Create the client
client = OpenAI(api_key=config.CHATGPT_SECRET)

def analyze_post_sentiment(post):
    comments_str = "\n".join(post["comments"])
    
    prompt = config.GPT_TEMPLATE.format(
        title=post["title"],
        text=post["text"],
        comments=comments_str,
        tickers=", ".join(post["tickers"])
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        reply = response.choices[0].message.content.strip()

        # Attempt to parse the JSON from GPT
        try:
            sentiment_scores = json.loads(reply)
            return sentiment_scores
        except json.JSONDecodeError:
            print("⚠️ GPT response was not valid JSON:")
            print(reply)
            return {}

    except OpenAIError as e:
        print(f"⚠️ GPT API call failed: {e}")
        return {}


def extract_real_tickers_with_sentiment(post):
    comments_str = "\n".join(post["comments"])

    prompt = config.GPT_TEMPLATE.format(
        title=post["title"],
        text=post["text"],
        comments=comments_str
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        reply = response.choices[0].message.content.strip()

        # ✅ Extract only the first JSON block if extra text is included
        json_match = re.search(r"\{.*\}", reply, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError as e:
                print("⚠️ GPT returned invalid JSON:")
                print(json_str)
                return {}
        else:
            print("⚠️ No JSON block found in GPT response:")
            print(reply)
            return {}

    except OpenAIError as e:
        print("⚠️ GPT API call failed:")
        print(e)
        return {}