from geojson_pydantic import FeatureCollection

from calculator import calculate
from models import DataLayer


class TestCalculatorFunction:
    def test_calculate_calls_zonal_stats(self, mocker):
        result = [
            {
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": []},
                "properties": {
                    "id": 1,
                    "min": 1,
                    "mean": 1,
                    "median": 1,
                    "max": 1,
                    "sum": 1,
                    "count": 1,
                    "majority": 1,
                    "minority": 1,
                },
            }
        ]
        datalayer = DataLayer(
            **{
                "id": 10,
                "nodata": 0,
                "url": "gs://planscape-datastore-dev/datalayers/1/a27c1c61-c99d-464e-91f7-0abc94bfe36c.tif",
            }
        )
        stands = FeatureCollection(
            **{
                "type": "FeatureCollection",
                "features": [result[0]],
            }
        )
        zonal_stats = mocker.patch("calculator.zonal_stats", return_value=result)
        result = calculate(datalayer=datalayer, stands=stands)
        zonal_stats.assert_called()
