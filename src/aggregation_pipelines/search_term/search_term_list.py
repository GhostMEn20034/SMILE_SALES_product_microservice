from src.config.settings import settings


def get_pipeline_to_find_search_terms(query: str, limit: int = 10) -> list:
    index_name = settings.atlas_search_search_terms_index_name.strip()
    pipeline = [
        {
            "$search": {
                "index": index_name,
                "autocomplete": {
                    "query": query,
                    "path": "name",
                },
            }
        },
        {
            "$limit": limit,
        },
        {
            "$project": {
                "_id": 0,
                "name": 1,
                "trend_search_term": {"$toBool": False}
            }
        },
    ]

    return pipeline


def get_pipeline_to_find_top_n_search_terms(limit: int = 10) -> list:
    pipeline = [
        {
            "$sort": {"search_count": -1, "last_searched": -1}
        },
        {
            "$limit": limit
        },
        {
            "$project": {
                "_id": 0,
                "name": 1,
                "trend_search_term": {"$toBool": True}
            }
        },
    ]

    return pipeline
