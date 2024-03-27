def get_pagination_to_skip_items(page: int, page_size: int):
    pipeline = [
        {
            "$skip": (page - 1) * page_size
        },
        {
            "$limit": page_size
        }
    ]

    return pipeline
