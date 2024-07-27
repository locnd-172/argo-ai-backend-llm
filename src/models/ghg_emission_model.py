from typing import Any

from pydantic import BaseModel, Field


class GHGEmissionModel(BaseModel):
    facility_name: str = Field(..., description="emission facility")
    plant: str = Field(..., description="emission plant")
    period_start: str = Field(..., description="emission period start")
    period_end: str = Field(..., description="emission period end")
    emission_data: Any = Field(..., description="emission data")


class EmissionFacility(BaseModel):
    facility_name: str = Field(..., description="emission facility name")
    plant: str = Field(..., description="emission plant")
    period_start: str = Field(..., description="emission period start")
    period_end: str = Field(..., description="emission period end")


class OrganicAmendment(BaseModel):
    straw_incorporated_short_value: float = Field(..., description="straw incorporated short value")
    straw_incorporated_long_value: float = Field(..., description="straw incorporated long value")
    compost_value: float = Field(..., description="compost value")
    farm_yard_manure_value: float = Field(..., description="farm yard manure value")
    green_manure_value: float = Field(..., description="green manure value")


class Irrigation(BaseModel):
    days_flooded: int = Field(..., description="days flooded")
    is_continuous_flooding: bool = Field(False, description="is continuous flooding")
    is_single_aeration: bool = Field(False, description="is single aeration")
    is_multiple_aeration: bool = Field(False, description="is multiple aeration")
    is_rainfed: bool = Field(False, description="is rainfed")
    is_upland: bool = Field(False, description="is upland")
    area: float = Field(..., description="area")


class CropProtection(BaseModel):
    pesticide_value: float = Field(..., description="pesticide value")
    herbicide_value: float = Field(..., description="herbicide value")
    fungicide_value: float = Field(..., description="fungicide value")
    insecticide_value: float = Field(..., description="insecticide value")


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
