from dataclasses import dataclass

from pydantic import BaseModel, Field


class ChatModel(BaseModel):
    session_id: str = Field(..., description="Session ID of user")
    sender_id: str = Field(..., description="User ID")
    sender_name: str = Field(..., description="User name")
    sender_message: str = Field(..., description="Question of user")


@dataclass
class GenerationRequest:
    data: any
    file: any
    histories: list
    language: str
    standalone_query: str


class HumanFeedbackModel(ChatModel):
    response_message: str = Field(..., description="Bot response message")
    human_feedback: str = Field(..., description="Human feedback")
