from typing import Any

from pydantic import BaseModel, Field


class ChatModel(BaseModel):
    session_id: str = Field(..., description="Session ID of user")
    sender_message: str = Field(..., description="Question of user")

    # sender_language: Optional[Literal["en", "vi"]] = Field(None, description="Language of user message")

    # def __init__(self, session_id: str, sender_message: str, /, **data: Any):
    #     super().__init__(**data)
    #     self.session_id = session_id
    #     self.sender_message = sender_message
