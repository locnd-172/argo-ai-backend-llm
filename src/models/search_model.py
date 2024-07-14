from typing import Optional
from pydantic import BaseModel


class SearchHybridModel(BaseModel):
    search: str
    index: Optional[str]
    top: Optional[int]
