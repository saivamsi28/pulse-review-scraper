from datetime import datetime

def validate_dates(start_date, end_date):
    if start_date > end_date:
        raise ValueError("Start date cannot be after end date")

def validate_source(source):
    allowed = ["g2", "capterra", "getapp"]
    if source not in allowed:
        raise ValueError(f"Source must be one of {allowed}")
