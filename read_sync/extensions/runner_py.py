import requests
from typing import List, Dict

MANGADEX_API = "https://api.mangadex.org"

def search_manga(query: str) -> List[Dict]:
    """Search MangaDex for a manga by title."""
    print(f"Searching MangaDex for '{query}'...")
    response = requests.get(
        f"{MANGADEX_API}/manga",
        params={"title": query, "limit": 10, "includes[]": "cover_art"}
    )
    response.raise_for_status()
    data = response.json()["data"]
    
    results = []
    for item in data:
        title = item["attributes"]["title"].get("en", "Unknown Title")
        results.append({
            "id": item["id"],
            "title": title,
            "description": item["attributes"]["description"].get("en", "")
        })
    return results

def get_chapters(manga_id: str, lang: str = "en") -> List[Dict]:
    """Get a list of chapters for a specific manga."""
    response = requests.get(
        f"{MANGADEX_API}/manga/{manga_id}/feed",
        params={"translatedLanguage[]": lang, "order[chapter]": "desc", "limit": 100}
    )
    response.raise_for_status()
    data = response.json()["data"]
    
    chapters = []
    for item in data:
        chapters.append({
            "id": item["id"],
            "chapter": item["attributes"].get("chapter", "0"),
            "title": item["attributes"].get("title", ""),
            "pages": item["attributes"].get("pages", 0)
        })
    return chapters

def get_chapter_images(chapter_id: str) -> List[str]:
    """Fetch the actual image URLs for a chapter."""
    response = requests.get(f"{MANGADEX_API}/at-home/server/{chapter_id}")
    response.raise_for_status()
    data = response.json()
    
    base_url = data["baseUrl"]
    chapter_hash = data["chapter"]["hash"]
    filenames = data["chapter"]["data"]
    
    image_urls = []
    for filename in filenames:
        image_urls.append(f"{base_url}/data/{chapter_hash}/{filename}")
        
    return image_urls
