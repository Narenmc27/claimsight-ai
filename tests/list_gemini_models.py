import os
import requests
from dotenv import load_dotenv

load_dotenv()

response = requests.get(
    "https://generativelanguage.googleapis.com/v1beta/models",
    params={"key": os.getenv("GOOGLE_API_KEY"), "pageSize": 100},
    timeout=30,
)
response.raise_for_status()

for m in response.json()["models"]:
    if "generateContent" in m.get("supportedGenerationMethods", []):
        print(m["name"].replace("models/", ""))