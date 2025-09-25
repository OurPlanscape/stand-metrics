from typing import Any, List

from geojson_pydantic import Feature, FeatureCollection
from pydantic import BaseModel


class DataLayer(BaseModel):
    id: int
    url: str
    nodata: Any


class StandMetricRequest(BaseModel):
    datalayer: DataLayer
    stands: FeatureCollection


class StandMetricResponse(BaseModel):
    features: List[Feature]
