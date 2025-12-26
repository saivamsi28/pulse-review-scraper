import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models.review_schema import build_review
from utils.date_utils import within_range
from config.constants import HEADERS, CAPTERRA_BASE_URL

def scrape_capterra(company, start_date, end_date):
    reviews = []
    page = 1

    while True:
        url = f"{CAPTERRA_BASE_URL}/{company}/reviews?page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        blocks = soup.find_all("div", class_="review")

        if not blocks:
            break

        for block in blocks:
            try:
                title = block.find("h3").get_text(strip=True)
                content = block.find("p").get_text(strip=True)
                date_text = block.find("time").get_text(strip=True)
                review_date = datetime.strptime(date_text, "%b %d, %Y")

                if not within_range(review_date, start_date, end_date):
                    continue

                rating = block.find("span", class_="rating")
                rating_value = rating.get_text(strip=True) if rating else None

                reviews.append(
                    build_review(
                        title,
                        content,
                        review_date.strftime("%Y-%m-%d"),
                        rating_value,
                        None,
                        "capterra"
                    )
                )
            except Exception:
                continue

        page += 1

    return reviews
