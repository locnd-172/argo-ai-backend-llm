from pydantic import BaseModel, Field
from typing import Optional

from fastapi import UploadFile


class DocsModel(BaseModel):
    docs_link: Optional[str]
    docs_file: Optional[UploadFile]
