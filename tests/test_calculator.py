import pytest
from geojson_pydantic import FeatureCollection

from calculator import calculate, url_to_local
from models import DataLayer


class TestURLToLocal:
    def test_returns_correctly(self):
        url = "gs://planscape-datastore-dev/datalayers/1/a27c1c61-c99d-464e-91f7-0abc94bfe36c.tif"
        local = url_to_local(url, env="dev")
        assert (
            local == "/datastore/datalayers/1/a27c1c61-c99d-464e-91f7-0abc94bfe36c.tif"
        )

    def test_raise_key_error(self):
        url = "gs://planscape-datastore-dev/datalayers/1/a27c1c61-c99d-464e-91f7-0abc94bfe36c.tif"
        with pytest.raises(KeyError):
            url_to_local(url, env="foo")


class TestCalculatorFunction:
    def test_foo(self):
        assert 1 == 1

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
        result = calculate(datalayer=datalayer, stands=stands, env="dev")
        zonal_stats.assert_called()
