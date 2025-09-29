from typing import Any, List, Optional

from geojson_pydantic import Feature, FeatureCollection
from pydantic import BaseModel


class DataLayer(BaseModel):
    id: int
    url: str
    nodata: Any


class StandMetricRequest(BaseModel):
    datalayer: DataLayer
    stands: FeatureCollection
    env: Optional[str] = "dev"


class StandMetricResponse(BaseModel):
    features: List[Feature]


class MetricResult(BaseModel):
    stand_id: int
    min: Optional[float]
    mean: Optional[float]
    median: Optional[float]
    max: Optional[float]
    majority: Optional[float]
    minority: Optional[float]
