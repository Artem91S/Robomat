from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db_connection import get_db
from app.schemas.events import EventBase, EventRead
from app.services.events import EventService
from app.core.logging import logger

event_router = APIRouter(tags=["Event"], prefix="/event")


@event_router.post("/", response_model=list[EventRead])
def create_event(
    body: list[EventBase] = Body(...),
    session: Session = Depends(get_db),
    event_service: EventService = Depends(EventService),
):

    if not body:
        logger.warning("No event data provided in request body")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No event data provided"
        )
    new_events = event_service.create_event(body, session)
    return [event.to_read_model() for event in new_events]
