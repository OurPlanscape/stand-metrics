from fastapi import FastAPI

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
    env = request.env
    stats = calculate(datalayer=datalayer, stands=stands, env=env)
    return stats
