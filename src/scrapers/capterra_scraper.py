from bs4 import BeautifulSoup
from datetime import datetime
import time

from utils.driver import get_driver
from utils.date_utils import within_range
from models.review_schema import build_review


def scrape_capterra(company, start_date, end_date):
    driver = get_driver()
    reviews = []
    page = 1

    while True:
        url = f"https://www.capterra.com/p/{company}/reviews?page={page}"
        print("Fetching:", url)

        driver.get(url)
        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
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

                rating_tag = block.find("span", class_="rating")
                rating = rating_tag.get_text(strip=True) if rating_tag else None

                reviews.append(
                    build_review(
                        title=title,
                        review=content,
                        date=review_date.strftime("%Y-%m-%d"),
                        rating=rating,
                        reviewer_name=None,
                        source="capterra"
                    )
                )
            except Exception:
                continue

        page += 1

    driver.quit()
    return reviews
