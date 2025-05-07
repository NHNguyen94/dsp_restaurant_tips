from fastapi import APIRouter

from src.api.v1.prediction_router import router as prediction_router

router = APIRouter(prefix="/v1")

router.include_router(prediction_router, prefix="/prediction")
