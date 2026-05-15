import time
from fastapi import FastAPI
from fastapi import HTTPException
from prometheus_client import Counter
from prometheus_client import Histogram
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from starlette.responses import Response

from app.recommender import (
    recommend_charger,
    predict_congestion,
    get_available_chargers
)

app = FastAPI(
    title="EVAT SmartCharge AI Backend API",
    description="Backend API for EV charging recommendation and monitoring.",
    version="1.0.0"
)

REQUEST_COUNT = Counter(
    "evat_request_total",
    "Total number of API requests",
    ["endpoint"]
)

REQUEST_LATENCY = Histogram(
    "evat_request_latency_seconds",
    "API request latency in seconds",
    ["endpoint"]
)


@app.get("/")
def root():
    REQUEST_COUNT.labels(endpoint="/").inc()

    return {
        "message": "Welcome to EVAT SmartCharge AI Backend API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    REQUEST_COUNT.labels(endpoint="/health").inc()

    return {
        "status": "healthy",
        "service": "EVAT SmartCharge AI Backend API"
    }


@app.get("/chargers")
def chargers():
    REQUEST_COUNT.labels(endpoint="/chargers").inc()

    return {
        "chargers": get_available_chargers()
    }


@app.get("/recommend")
def recommend(distance_km: float, availability: int, congestion: float):
    start = time.time()

    try:
        result = recommend_charger(
            distance_km=distance_km,
            availability=availability,
            congestion=congestion
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    REQUEST_COUNT.labels(endpoint="/recommend").inc()
    REQUEST_LATENCY.labels(endpoint="/recommend").observe(time.time() - start)

    return result


@app.get("/predict-congestion")
def congestion_prediction(current_usage: int, charger_capacity: int):
    start = time.time()

    try:
        result = predict_congestion(
            current_usage=current_usage,
            charger_capacity=charger_capacity
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    REQUEST_COUNT.labels(endpoint="/predict-congestion").inc()
    REQUEST_LATENCY.labels(
        endpoint="/predict-congestion"
    ).observe(time.time() - start)

    return result


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
