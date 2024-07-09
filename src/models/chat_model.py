from dataclasses import dataclass

from pydantic import BaseModel, Field


class ChatModel(BaseModel):
    session_id: str = Field(..., description="Session ID of user")
    sender_message: str = Field(..., description="Question of user")


@dataclass
class GenerationRequest:
    data: any
    file: any
    histories: list
    language: str
    standalone_query: str
