from sqlalchemy import Column, Integer, String, DateTime, JSON

from app.core.db_connection import Base
from app.schemas.events import EventRead


class EventDB(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(String, unique=True, index=True)
    occurred_at = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    event_type = Column(String, nullable=False)
    properties = Column(JSON, nullable=False)

    def to_read_model(self) -> EventRead:
        return EventRead.model_validate(self)
