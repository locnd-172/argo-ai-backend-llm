from typing import Dict, Any, List, Optional

from pydantic import BaseModel, Field


class GHGEmissionModel(BaseModel):
    facility: str = Field(..., description="emission facility")
    plant: str = Field(..., description="emission plant")
    period: str = Field(..., description="emission period")
    emission_data: Any = Field(..., description="emission data")

class OrganicAmendment(BaseModel):
    type: str = Field(..., description="organic amendment")
    value: int = Field(..., description="organic amendment value")
class Irrigation(BaseModel):
    days_flooded: int = Field(..., description="days flooded")
    irrigation_type: str = Field(..., description="irrigation type")
    area: float = Field(..., description="area")
    organic_amendment_list: List[OrganicAmendment] = Field(..., description="organic amendment list")

class CropProtection(BaseModel):
    type: str = Field(..., description="crop protection type")
    value: int = Field(..., description="crop protection value")

class CropResidue(BaseModel):
    type: str = Field(..., description="crop residue type")
    value: int = Field(..., description="crop residue value")
class LandManagament(BaseModel):
    fertilizer_value: int = Field(..., description="fertilizer value")
    animal_manure_value: int = Field(..., description="animal manure value")
class Energy(BaseModel):
    diesel_value: float = Field(..., description="diesel value")
    gasoline_value: float = Field(..., description="gasoline value")
    electricity_value: float = Field(..., description="electricity value")

