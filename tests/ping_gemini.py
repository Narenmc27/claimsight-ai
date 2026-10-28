import os
import sys
import time
import requests
from dotenv import load_dotenv

load_dotenv()

MODELS = ["gemini-3.6-flash", "gemini-3.7-flash", "gemini-3.8-flash"]

for model in MODELS:
    start = time.time()
    try:
        r = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            params={"key": os.getenv("GOOGLE_API_KEY")},
            json={"contents": [{"parts": [{"text": "Say hello in 3 words"}]}]},
            timeout=40,
        )
        print(f"{model}: status {r.status_code} in {time.time() - start:.1f}s")
        if r.status_code != 200:
            print("   ", r.text[:200])
    except requests.exceptions.RequestException as e:
        print(f"{model}: FAILED after {time.time() - start:.1f}s ({type(e).__name__})")