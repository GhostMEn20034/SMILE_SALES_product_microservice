from fastapi.exceptions import HTTPException
from pydantic import ValidationError
from json import loads
from typing import Dict

from src.schemes.product.facet_values.facet_value_filters import FacetFilterObject

def get_facet_filters(stringified_facet_filters: str) -> Dict[str, FacetFilterObject]:
    facet_filters: Dict = loads(stringified_facet_filters)
    if not isinstance(facet_filters, Dict):
        raise HTTPException(status_code=400, detail={"chosen_facets": "Facet filters are not valid"})

    validated_facet_filters: Dict[str, FacetFilterObject] = {}
    for key, value in facet_filters.items():
        try:
            # Attempt to create a FacetFilterObject from the value.
            validated_facet_filters[key] = FacetFilterObject(**value)
        except ValidationError as e:
            # If validation fails, raise an HTTPException with the error details.
            raise HTTPException(status_code=400, detail={"chosen_facets": f"Facet filter for '{key}' is not valid: {str(e)}"})

    return validated_facet_filters