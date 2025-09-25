from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "stand-metric-calculator"
    gdal_cache_max: str = "15%"
    gdal_num_threads: str = "8"
    cpl_debug: bool = False
    raster_provider: str = "GCP"
    google_application_credentials: str = ""
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_default_region: str = "us-west1"


settings = Settings()
