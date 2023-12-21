from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class ViConceptModel(BaseModel):
    """
    The Response model for Vietnamese concept
    """

    vn_main: Optional[str]
    en_main: Optional[str]
    vn_synonyms: Optional[List[str]]
    en_synonyms: Optional[List[str]]
    en_main_vsrc: Optional[Dict[str, Union[str, None]]]
