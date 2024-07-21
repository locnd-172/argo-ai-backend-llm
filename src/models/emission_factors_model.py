from typing import Any, Optional

from pydantic import BaseModel, Field


class EmissionFactorModel(BaseModel):
    name: str = Field(..., description="EF name")
    description: Optional[str] = Field(..., description="EF description")
    co2: float = Field(0, description="CO2 value")
    co2_unit: str = Field("kg/ha", description="CO2 unit")
    ch4: float = Field(0, description="CH4 value")
    ch4_unit: str = Field("kg/ha", description="CH4 unit")
    n2o: float = Field(0, description="N2O value")
    n2o_unit: str = Field("kg/ha", description="N2O unit")
    source: str = Field(..., description="EF source/library")
    link: str = Field(..., description="EF source link")
    scope: int = Field(1, description="EF scope")


class UpdateEmissionFactorModel(EmissionFactorModel):
    document_id: Optional[str] = Field(default="", description="")
