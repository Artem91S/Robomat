from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from app.core.logging import logger
from app.models import EventDB
from app.schemas.events import EventBase


class EventService:
    def create_event(
        self, events_data: list[EventBase], session: Session
    ) -> list[EventDB]:
        response_events = []
        logger.debug(f"Creating {len(events_data)} events")
        for data in events_data:
            try:
                new_event = EventDB(**data.to_dict())
                session.add(new_event)
                session.commit()
                response_events.append(new_event)
                break
                logger.success(f"Event created with ID: {new_event.id}")
            except IntegrityError as e:
                session.rollback()
                logger.warning(f"Integrity Exception occurred. {e}")
                continue
            except SQLAlchemyError as e:
                session.rollback()
                logger.warning(f"ORM Exception occurred. {e}")
                continue

        logger.success(f"Successfully added {len(response_events)} events")
        return response_events
