from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel, Field


class DocsModel(BaseModel):
    docs_link: Optional[str]
    docs_file: Optional[UploadFile]
