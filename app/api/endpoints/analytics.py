from fastapi import APIRouter, Depends, Query
from datetime import date

from sqlalchemy.orm import Session

from app.core.db_connection import get_db
from app.schemas.analytics import (
    UserCountByDateResponse,
    UserCountParams,
    UserTopParams,
    EventCountTopResponse,
)
from app.schemas.events import EventReadWithCursor
from app.services.analytics import AnalyticsService

router = APIRouter(prefix="/stats", tags=["Analytics"])


@router.get("/dau", response_model=UserCountByDateResponse)
def get_user_ids_by_day(
    from_: date = Query(alias="from"),
    to: date = Query(...),
    session: Session = Depends(get_db),
    analytics_service: AnalyticsService = Depends(AnalyticsService),
):
    params = UserCountParams(from_=from_, to=to)
    return analytics_service.users_by_day(params, session)


@router.get("/top-events", response_model=EventCountTopResponse)
def get_top_events(
    from_: date = Query(alias="from"),
    to: date = Query(...),
    limit: int = Query(10, gt=0),
    session: Session = Depends(get_db),
    analytics_service: AnalyticsService = Depends(AnalyticsService),
):
    params = UserTopParams(from_=from_, to=to, limit=limit)
    return analytics_service.top_events(params, session)


@router.get("/retention", response_model=EventReadWithCursor)
def get_retention_analysis(
    start_date: date,
    window: int,
    page_size: int = Query(20, gt=0),
    last_id: int | None = None,
    session: Session = Depends(get_db),
    analytics_service: AnalyticsService = Depends(AnalyticsService),
):
    return analytics_service.retention_analysis(
        start_date, window, page_size, last_id, session
    )
