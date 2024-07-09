from pydantic import BaseModel
from typing import Optional, List


class SearchHybridModel(BaseModel):
    search: str
    index: Optional[str]
    top: Optional[int]
