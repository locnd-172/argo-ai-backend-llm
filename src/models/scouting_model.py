from pydantic import BaseModel, Field


class ScoutingModel(BaseModel):
    facility: str = Field(..., description="scouting facility")
    plant: str = Field(..., description="scouting plant")
    date: str = Field(..., description="date facility")
    description: str = Field(..., description="scouting description")
