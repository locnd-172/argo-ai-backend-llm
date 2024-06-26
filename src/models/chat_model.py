from pydantic import BaseModel, Field


class ChatModel(BaseModel):
    session_id: str = Field(..., description="Session ID of user")
    sender_message: str = Field(..., description="Question of user")
    # sender_language: Optional[Literal["en", "vi"]] = Field(None, description="Language of user message")
