from typing import Dict, List

from src.config.settings import settings
from src.query_utils.common.search_relevance import get_pipeline_to_exclude_low_relevant_search_items


def get_search_product_pipeline(query: str, exclude_low_relevant_results: bool = False) -> List[Dict]:
    if not query.strip():
        return []

    search_product_pipeline = [
        {'$search': {
            'index': settings.atlas_search_product_index_name.strip(),
            'compound': {
                'must': [
                    {
                        'text': {
                            'query': query.strip(),
                            'path': "name"
                        }
                    }
                ],
                "should": [
                    {'text': {
                        'query': query.strip(),
                        'path': "search_terms",
                        "score": {"constant": {"value": 0.2}}
                    }}
                ]
            }
        }
        }
    ]

    if exclude_low_relevant_results:
        search_product_pipeline.extend(get_pipeline_to_exclude_low_relevant_search_items(settings.relevance_threshold))

    return search_product_pipeline
