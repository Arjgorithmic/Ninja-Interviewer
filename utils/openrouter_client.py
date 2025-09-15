import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise EnvironmentError("OPENROUTER_API_KEY not found in .env file")

# You can change model to any available on OpenRouter (e.g., "anthropic/claude-3-haiku")
MODEL = "deepseek/deepseek-r1:free"  # Lightweight, fast, good for reasoning

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

def call_openrouter(prompt, temperature=0.3, max_tokens=500, model=MODEL):
    """
    Direct HTTP request to OpenRouter API.
    Returns the assistant's response as a string.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:8501", 
        "X-Title": "ExcelInterviewer AI",
    }

    data = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a precise assistant. Respond only with requested output."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }

    try:
        response = httpx.post(BASE_URL, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[ERROR] OpenRouter API call failed: {e}")
        return "I'm having trouble processing your answer right now. Please try again later."