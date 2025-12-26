import argparse
import json
import os

from utils.date_utils import parse_date
from utils.validators import validate_dates, validate_source
from utils.error_handler import handle_error

from scrapers.g2_scraper import scrape_g2
from scrapers.capterra_scraper import scrape_capterra
from scrapers.getapp_scraper import scrape_getapp


def main():
    parser = argparse.ArgumentParser(description="Scrape SaaS product reviews")
    parser.add_argument("--company", required=True, help="Company slug/name")
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date YYYY-MM-DD")
    parser.add_argument(
        "--source",
        required=True,
        choices=["g2", "capterra", "getapp"],
        help="Review source"
    )

    args = parser.parse_args()

    try:
        start_date = parse_date(args.start)
        end_date = parse_date(args.end)

        validate_dates(start_date, end_date)
        validate_source(args.source)

        if args.source == "g2":
            reviews = scrape_g2(args.company, start_date, end_date)
        elif args.source == "capterra":
            reviews = scrape_capterra(args.company, start_date, end_date)
        else:
            reviews = scrape_getapp(args.company, start_date, end_date)

        os.makedirs("output", exist_ok=True)

        with open("output/reviews.json", "w", encoding="utf-8") as f:
            json.dump(reviews, f, indent=2, ensure_ascii=False)

        if not reviews:
            print("Completed successfully, but no reviews matched the criteria.")
        else:
            print(f"Scraped {len(reviews)} reviews")

    except Exception as e:
        handle_error(str(e))


if __name__ == "__main__":
    main()
