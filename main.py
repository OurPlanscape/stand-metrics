from fastapi import FastAPI, Request

from calculator import calculate
from config import settings
from models import StandMetricRequest

app = FastAPI()


@app.get("/health")
async def health():
    return {"app": settings.app_name, "status": "ok"}


@app.post("/metrics")
async def get_metrics(request: StandMetricRequest):
    datalayer = request.datalayer
    stands = request.stands
    stats = calculate(datalayer=datalayer, stands=stands)
    return stats


@app.get("/exception")
async def raise_exception(request: Request):
    raise KeyError()
