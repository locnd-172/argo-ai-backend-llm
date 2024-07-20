from pydantic import BaseModel, Field


class UploadLinkModel(BaseModel):
    document_link: str = ""


class UploadTextModel(BaseModel):
    document_title: str = Field("")
    document_text: str = Field("")


class DeleteDocumentModel(BaseModel):
    document_titles: list = Field([], description="List of document titles to delete")
