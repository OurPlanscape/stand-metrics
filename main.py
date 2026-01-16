import logging

from fastapi import FastAPI
from google.cloud import logging as cloud_logging

from calculator import calculate
from config import settings
from models import StandMetricRequest

app = FastAPI()

client = cloud_logging.Client()

client.setup_logging(log_level=logging.INFO)


@app.get("/health")
async def health():
    return {"app": settings.app_name, "status": "ok"}


@app.post("/metrics")
async def get_metrics(request: StandMetricRequest):
    datalayer = request.datalayer
    stands = request.stands
    stats = calculate(datalayer=datalayer, stands=stands)
    return stats
