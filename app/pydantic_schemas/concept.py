from typing import List, Optional

from pydantic import BaseModel


class ViConceptModel(BaseModel):
    """
    The Response model for Vietnamese concept
    """

    vn_main: Optional[str] = None
    en_main: Optional[str] = None
    vn_synonyms: Optional[List[str]] = [None]
