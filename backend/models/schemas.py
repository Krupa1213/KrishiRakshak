from pydantic import BaseModel
from typing import List


class Farmer(BaseModel):
    name: str
    state: str
    district: str
    land_size: float
    crops: List[str]