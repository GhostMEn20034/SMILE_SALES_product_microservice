from typing import List, Dict

from bson import ObjectId


def get_facet_category_priority(category_ids: List[ObjectId]) -> List[Dict]:
    """
    Returns list of switch-case branches to define priority of category
    where the first category has priority 1 and the last one has priority: category_ids length - 1
    """
    branches = []
    for index, category_id in enumerate(category_ids):
        if category_id == "*":
            branches.append(
                {"case": {"$eq": [category_id, "$categories"]}, "then": index + 1}
            )
        else:
            branches.append(
                {"case": {"$in": [category_id, "$categories"]}, "then": index + 1}
            )

    return branches
