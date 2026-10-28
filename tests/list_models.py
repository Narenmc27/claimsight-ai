import os
import requests
from dotenv import load_dotenv

load_dotenv()

response = requests.get(
    "https://api.groq.com/openai/v1/models",
    headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
    timeout=30,
)
response.raise_for_status()

for model in response.json()["data"]:
    print(model["id"])