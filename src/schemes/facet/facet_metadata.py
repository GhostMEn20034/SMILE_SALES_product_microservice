from typing import Dict, Union, Optional

from pydantic import BaseModel

class FacetMetadataItem(BaseModel):
    name: str # facet name
    range_to_display_name: Optional[Dict[Union[float, int], str]] = None # gteq from range value to display name mapping
