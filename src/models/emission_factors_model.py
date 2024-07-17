from typing import Any, Optional

from pydantic import BaseModel, Field


class EmissionFactorModel(BaseModel):
    name: str = Field(..., description="EF name")
    co2: float = Field(..., description="CO2 value")
    co2_unit: str = Field(..., description="CO2 unit")
    ch4: float = Field(..., description="CH4 value")
    ch4_unit: str = Field(..., description="CH4 unit")
    n2o: float = Field(..., description="N2O value")
    n2o_unit: str = Field(..., description="N2O unit")
    source: str = Field(..., description="EF source/library")
    link: str = Field(..., description="EF source link")
    scope: int = Field(..., description="EF scope")
    document_id: Optional[str] = Field(default="", description="")
