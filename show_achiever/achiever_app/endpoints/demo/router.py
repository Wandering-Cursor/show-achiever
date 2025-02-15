from fastapi import APIRouter

demo_router = APIRouter(
    prefix="/demo",
    tags=["demo"],
)
