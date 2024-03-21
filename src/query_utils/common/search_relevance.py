from typing import Dict, List


def get_pipeline_to_exclude_low_relevant_search_items(relevance_threshold: float) -> List[Dict]:
    """
    Use this pipeline stage only after search stage.
    This pipeline allows you to exclude search items with low relevancy.
    :param relevance_threshold: minimum normalized score so search items not to be excluded
    """
    pipeline = [
        {"$addFields": {
            "score": {
                "$meta": "searchScore"
            }
        }},
        {"$setWindowFields": {
            "output": {
                "maxScore": {
                    "$max": "$score"
                }
            }
        }},
        {"$addFields": {
            "normalizedScore": {
                "$divide": ["$score", "$maxScore"]
            }
        }},
        {"$match": {
            "normalizedScore": {"$gte": relevance_threshold}
        }},
    ]

    return pipeline
