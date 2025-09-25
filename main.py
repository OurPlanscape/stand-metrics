from fastapi import FastAPI

from calculator import calculate
from config import settings
from models import StandMetricRequest

app = FastAPI()


@app.get("/health")
def health():
    return {"app": settings.app_name, "status": "ok"}


@app.post("/metrics")
def get_metrics(request: StandMetricRequest):
    datalayer = request.datalayer
    stands = request.stands
    stats = calculate(datalayer=datalayer, stands=stands)
    return stats
