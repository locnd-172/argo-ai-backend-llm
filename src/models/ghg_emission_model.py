from typing import Dict, Any, List, Optional

from pydantic import BaseModel, Field


class GHGEmissionModel(BaseModel):
    facility: str = Field(..., description="emission facility")
    plant: str = Field(..., description="emission plant")
    period: str = Field(..., description="emission period")
    emission_data: Any = Field(..., description="emission data")

class OrganicAmendment(BaseModel):
    # type: str = Field(..., description="organic amendment")
    # value: int = Field(..., description="organic amendment value")
    straw_incorporated_short_value: float = Field(..., description="straw incorporated short value")
    straw_incorporated_long_value: float = Field(..., description="straw incorporated long value")
    compost_value: float = Field(..., description="compost value")
    farm_yard_manure_value: float = Field(..., description="farm yard manure value")
    green_manure_value: float = Field(..., description="green manure value")
class Irrigation(BaseModel):
    days_flooded: int = Field(..., description="days flooded")
    # irrigation_type: str = Field(..., description="irrigation type")
    is_continuous_flooding: bool = Field(False, description="is continuous flooding")
    is_single_aeration: bool = Field(False, description="is single aeration")
    is_multiple_aeration: bool  = Field(False, description="is multiple aeration")
    is_rainfed: bool = Field(False, description="is rainfed")
    is_upland: bool = Field(False, description="is upland")
    area: float = Field(..., description="area")
class CropProtection(BaseModel):
    # type: str = Field(..., description="crop protection type")
    # value: int = Field(..., description="crop protection value")
    pesticide_value: float = Field(..., description="pesticide value")
    herbicide_value: float = Field(..., description="herbicide value")
    fungicide_value: float = Field(..., description="fungicide value")
    insecticide_value: float = Field(..., description="insecticide value")
# class CropResidue(BaseModel):
#     # type: str = Field(..., description="crop residue type")
#     # value: int = Field(..., description="crop residue value")
class LandManagement(BaseModel):
    fertilizer_value: int = Field(..., description="fertilizer value")
    animal_manure_value: int = Field(..., description="animal manure value")
    landfill_value: float = Field(..., description="landfill value")
    incineration_value: float = Field(..., description="incineration value")
    crop_burning_value: float = Field(..., description="crop_burning value")
    composting_value: float = Field(..., description="composting value")
class Energy(BaseModel):
    diesel_value: float = Field(..., description="diesel value")
    gasoline_value: float = Field(..., description="gasoline value")
    electricity_value: float = Field(..., description="electricity value")

