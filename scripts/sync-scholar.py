import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")
USER_ID = os.getenv("SCHOLAR_USER_ID")

if not API_KEY or not USER_ID:
    raise ValueError("Missing SERPAPI_KEY or SCHOLAR_USER_ID in .env")

url = "https://serpapi.com/search.json"
params = {
    "engine": "google_scholar_author",
    "author_id": USER_ID,
    "api_key": API_KEY,
    "hl": "en"
}

all_articles = []
start = 0

while True:
    params["start"] = start
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    articles = data.get("articles", [])
    if not articles:
        break

    for article in articles:
        all_articles.append({
            "title": article.get("title"),
            "authors": article.get("authors"),
            "year": article.get("year"),
            "publication": article.get("publication"),
            "link": article.get("link"),
            "citation_id": article.get("citation_id")
        })

    if data.get("serpapi_pagination", {}).get("next"):
        start += len(articles)
    else:
        break

Path("data").mkdir(exist_ok=True)

with open("data/publications.json", "w", encoding="utf-8") as f:
    json.dump(all_articles, f, indent=2, ensure_ascii=False)

print(f"Saved {len(all_articles)} publications to data/publications.json")