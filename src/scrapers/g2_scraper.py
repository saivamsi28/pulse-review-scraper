import requests
from bs4 import BeautifulSoup
from datetime import datetime
from models.review_schema import build_review
from utils.date_utils import within_range
from config.constants import HEADERS, G2_BASE_URL

def scrape_g2(company, start_date, end_date):
    reviews = []
    page = 1

    while True:
        url = f"{G2_BASE_URL}/{company}/reviews?page={page}"
        print("Fetching:", url)

        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Stopped: received status code {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        review_blocks = soup.find_all("div", class_="paper")

        if not review_blocks:
            if page == 1:
                print(
                    "Warning: No reviews found in static HTML. "
                    "G2 reviews are loaded dynamically via JavaScript."
                )
            break

        for block in review_blocks:
            try:
                title_tag = block.find("h3")
                body_tag = block.find("p")
                time_tag = block.find("time")

                if not (title_tag and body_tag and time_tag):
                    continue

                title = title_tag.get_text(strip=True)
                content = body_tag.get_text(strip=True)

                date_text = time_tag.get("datetime", "")[:10]
                review_date = datetime.strptime(date_text, "%Y-%m-%d")

                if not within_range(review_date, start_date, end_date):
                    continue

                rating_tag = block.find("span", class_="fw-semibold")
                rating = rating_tag.get_text(strip=True) if rating_tag else None

                reviewer_tag = block.find("span", class_="link")
                reviewer_name = reviewer_tag.get_text(strip=True) if reviewer_tag else None

                reviews.append(
                    build_review(
                        title=title,
                        review=content,
                        date=date_text,
                        rating=rating,
                        reviewer_name=reviewer_name,
                        source="g2"
                    )
                )
            except Exception:
                continue

        page += 1

    return reviews
