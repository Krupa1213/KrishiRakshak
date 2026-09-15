from pydantic import BaseModel
from typing import List, Optional


class Farmer(BaseModel):
    name: str
    state: str
    district: str
    land_size: float
    crops: List[str]


class Farm(BaseModel):
    farm_id: str
    farmer_name: str
    latitude: float
    longitude: float
    area_acres: float
    crop: str
    crop_variety: Optional[str] = None
    sowing_date: Optional[str] = None
    soil_type: Optional[str] = None
    irrigation_type: Optional[str] = None
    growth_stage: Optional[str] = None


class CropData(BaseModel):
    farm_id: str
    crop_name: str
    crop_variety: Optional[str] = None
    sowing_date: Optional[str] = None
    growth_stage: Optional[str] = None
    expected_harvest_date: Optional[str] = None


class SoilData(BaseModel):
    farm_id: str
    soil_type: Optional[str] = None
    ph: Optional[float] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    moisture: Optional[float] = None


class MarketData(BaseModel):
    crop_name: str
    market_name: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    price_per_quintal: Optional[float] = None
    market_date: Optional[str] = None


class GovernmentScheme(BaseModel):
    scheme_name: str
    description: Optional[str] = None
    state: Optional[str] = None
    eligibility: Optional[str] = None
    benefits: Optional[str] = None
    application_link: Optional[str] = None