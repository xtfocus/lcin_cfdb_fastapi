from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class UnchartedStatus(BaseModel):
    """
    The Response model for status/uncharted_en_main route
    """

    uncharted_en_mains: List[str] = []


class ValidationStatus(BaseModel):
    """
    The Response model for status/validate route
    """

    dictionary_size: int
    count_uncharted_en_mains: int
    count_charted: Dict[str, int]
    count_charted_to_all_vsources: int
