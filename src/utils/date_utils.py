from datetime import datetime

def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

def within_range(review_date, start_date, end_date):
    return start_date <= review_date <= end_date
