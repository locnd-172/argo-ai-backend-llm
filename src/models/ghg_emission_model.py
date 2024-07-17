from typing import Dict, Any

from pydantic import BaseModel, Field


class GHGEmissionModel(BaseModel):
    facility: str = Field(..., description="emission facility")
    plant: str = Field(..., description="emission plant")
    period: str = Field(..., description="emission period")
    emission_data: Any = Field(..., description="emission data")
