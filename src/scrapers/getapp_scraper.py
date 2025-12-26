import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models.review_schema import build_review
from utils.date_utils import within_range
from config.constants import HEADERS, GETAPP_BASE_URL

def scrape_getapp(company, start_date, end_date):
    reviews = []
    page = 1

    while True:
        url = f"{GETAPP_BASE_URL}/{company}/reviews/?page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        blocks = soup.find_all("div", class_="review-card")

        if not blocks:
            break

        for block in blocks:
            try:
                title = block.find("h3").get_text(strip=True)
                content = block.find("p").get_text(strip=True)
                date_text = block.find("time")["datetime"][:10]
                review_date = datetime.strptime(date_text, "%Y-%m-%d")

                if not within_range(review_date, start_date, end_date):
                    continue

                reviews.append(
                    build_review(
                        title,
                        content,
                        date_text,
                        None,
                        None,
                        "getapp"
                    )
                )
            except Exception:
                continue

        page += 1

    return reviews
