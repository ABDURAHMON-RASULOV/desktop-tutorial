import requests
import pandas as pd
import time
import json
import re
from bs4 import BeautifulSoup

BASE_URL = "https://www.imdb.com"
TOP_250_URL = f"{BASE_URL}/chart/top/"
HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0"
}

def extract_movie_urls():
    res = requests.get(TOP_250_URL, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    data = soup.find("script", type="application/ld+json")
    if not data:
        print("⚠️ Could not find JSON data.")
        return []

    parsed = json.loads(data.string)
    movies = parsed.get("itemListElement", [])

    links = [item["item"]["url"] for item in movies if "item" in item]
    return links

def scrape_movie(link):
    full_link = link if link.startswith("http") else f"https://www.imdb.com{link}"
    res = requests.get(full_link, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    time.sleep(1)

    try:
        # Title
        title_tag = soup.find("h1")
        title = title_tag.text.strip() if title_tag else "Unknown Title"

        # Rating
        rating_tag = soup.select_one('[data-testid="hero-rating-bar__aggregate-rating__score"] > span')
        rating = float(rating_tag.text) if rating_tag else None

        # Year
        release_info = soup.select_one('[data-testid="title-details-releasedate"]')
        year = None
        if release_info:
            match = re.search(r"\b(19|20)\d{2}\b", release_info.text)
            if match:
                year = int(match.group())

        # Genres (robust)
        # Genres (robust)
    

        genre_tags = soup.select('[data-testid="genres"] a')
        genres = [g.text.strip() for g in genre_tags] if genre_tags else []


        # Runtime
        runtime_tag = soup.select_one('[data-testid="title-techspec_runtime"]')
        runtime = runtime_tag.text.strip() if runtime_tag else "Unknown"

        # Director
        director_tag = soup.select_one('[data-testid="title-pc-principal-credit"] a')
        director = director_tag.text.strip() if director_tag else "Unknown"

        # Top 3 Cast
        cast_tags = soup.select('[data-testid="title-cast-item__actor"]')
        cast = [c.text.strip() for c in cast_tags[:3]] if cast_tags else []

        # Votes
        votes_tag = soup.select_one('[data-testid="hero-rating-bar__aggregate-rating__score"] + div')
        votes = None
        if votes_tag:
            votes_text = votes_tag.text.replace(",", "").strip()
            if votes_text:
                votes = int(votes_text.split()[0])

        # Box Office
        box_office = "N/A"
        bo_section = soup.find("li", {"data-testid": "title-boxoffice-cumulativeworldwidegross"})
        if bo_section:
            bo_tag = bo_section.find("span", class_="ipc-metadata-list-item__list-content-item")
            if bo_tag:
                box_office = bo_tag.text.strip()

        return {
            "Title": title,
            "Year": year,
            "Rating": rating,
            "Votes": votes,
            "Genres": genres,
            "Runtime": runtime,
            "Director": director,
            "Top 3 Cast": cast,
            "Box Office": box_office
        }

    except Exception as e:
        print(f"❌ Error parsing {link}: {e}")
        return None

def scrape_top_250():
    print("🔍 Fetching movie links...")
    links = extract_movie_urls()
    print(f"✅ Found {len(links)} movie links")

    all_data = []
    for i, link in enumerate(links):
        print(f"{i+1}. Scraping: {link}")
        movie = scrape_movie(link)
        if movie:
            all_data.append(movie)

    return pd.DataFrame(all_data)

if __name__ == "__main__":
    df = scrape_top_250()
    df.to_csv("imdb_top250_raw.csv", index=False)
    print("✅ Scraping complete! Data saved to imdb_top250_raw.csv")
