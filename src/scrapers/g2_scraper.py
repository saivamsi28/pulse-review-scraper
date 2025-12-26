from bs4 import BeautifulSoup
from datetime import datetime
import time

from utils.driver import get_driver
from utils.date_utils import within_range
from models.review_schema import build_review


def scrape_g2(company, start_date, end_date):
    driver = get_driver()
    reviews = []
    page = 1

    while True:
        url = f"https://www.g2.com/products/{company}/reviews?page={page}"
        print("Fetching:", url)

        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        blocks = soup.find_all("div", class_="paper")

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

                rating_tag = block.find("span", class_="fw-semibold")
                rating = rating_tag.get_text(strip=True) if rating_tag else None

                reviewer_tag = block.find("span", class_="link")
                reviewer = reviewer_tag.get_text(strip=True) if reviewer_tag else None

                reviews.append(
                    build_review(
                        title=title,
                        review=content,
                        date=date_text,
                        rating=rating,
                        reviewer_name=reviewer,
                        source="g2"
                    )
                )
            except Exception:
                continue

        page += 1

    driver.quit()
    return reviews
