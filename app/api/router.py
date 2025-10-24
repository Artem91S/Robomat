from fastapi import APIRouter
from .endpoints import event, analytics

api = APIRouter()

api.include_router(event.event_router)
api.include_router(analytics.router)
