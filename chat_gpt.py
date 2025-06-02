# chat_gpt.py

from openai import OpenAI, OpenAIError
import config
import json
from datetime import datetime
from pathlib import Path
from stocks_utils import log_rewritten_post

# Create the client
client = OpenAI(api_key=config.CHATGPT_SECRET)

# Log file for rewritten outputs
LOG_FILE = "rewritten_log.json"

def rewrite_post_for_linkedin(post):
    post_json = json.dumps(post, indent=2)
    prompt = config.GPT_TEMPLATE.format(post_json=post_json)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        rewritten = response.choices[0].message.content.strip()

        log_rewritten_post(
            post,
            rewritten,
            input_tokens=response.usage.prompt_tokens,
            output_tokens=response.usage.completion_tokens,
            model="gpt-4o"
        )

        return rewritten

    except OpenAIError as e:
        print(f"⚠️ GPT API call failed: {e}")
        return "[GPT call failed]"

