from pathlib import Path
from typing import Any, Dict, Optional

import rasterio
from boto3.session import Session
from geojson_pydantic import FeatureCollection
from rasterstats import zonal_stats

from config import settings
from models import DataLayer

STATISTICS = "min mean max median sum count majority minority"


def get_aws_session() -> Session:
    return Session(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_default_region,
    )


def get_gdal_env(
    allowed_extensions: Optional[str] = ".tif",
) -> Dict[str, Any]:
    gdal_env = {
        "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
        "CPL_VSIL_USE_TEMP_FILE_FOR_RANDOM_WRITE": "YES",
        "GDAL_CACHE_MAX": settings.gdal_cache_max,
        "VSI_CACHE": False,
        "GDAL_NUM_THREADS": settings.gdal_num_threads,
        "GDAL_TIFF_INTERNAL_MASK": True,
        "GDAL_TIFF_OVR_BLOCK_SIZE": 128,
        "CPL_DEBUG": settings.cpl_debug,
    }
    # match settings.raster_provider:
    #     case "aws":
    #         gdal_env["session"] = get_aws_session()
    #     case "gcp":
    #         gdal_env["GOOGLE_APPLICATION_CREDENTIALS"] = (
    #             settings.google_application_credentials
    #         )
    #     case _:
    #         pass
    return gdal_env


def url_to_local(url: str) -> str:
    path = Path(url)
    parts = "/".join(path.parts[2:])
    return f"/datastore/{parts}"


def calculate(
    datalayer: DataLayer,
    stands: FeatureCollection,
) -> FeatureCollection:
    local_path = url_to_local(datalayer.url)
    with rasterio.Env(**get_gdal_env()):
        stats = zonal_stats(
            vectors=stands,
            raster=local_path,
            geojson_out=True,
            stats=STATISTICS,
            nodata=datalayer.nodata,
            band=1,
        )
        return FeatureCollection(
            type="FeatureCollection",
            features=stats,
        )
