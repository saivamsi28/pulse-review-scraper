def build_review(
    title,
    review,
    date,
    rating=None,
    reviewer_name=None,
    source=None
):
    return {
        "title": title,
        "review": review,
        "date": date,
        "rating": rating,
        "reviewer_name": reviewer_name,
        "source": source
    }
