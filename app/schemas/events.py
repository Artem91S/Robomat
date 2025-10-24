import uuid
from typing import Dict, Any
from uuid import UUID

from pydantic import Field, BaseModel, ConfigDict

from datetime import datetime

from app.schemas.base import BaseSchema


class EventBase(BaseModel):
    event_id: UUID
    occurred_at: datetime
    user_id: int
    event_type: str
    properties: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "event_id": str(uuid.uuid4()),
                    "occurred_at": datetime.now().isoformat(),
                    "user_id": 9999,
                    "event_type": "test",
                    "properties": {"item_id": "SKU2710", "length": 123},
                }
            ]
        },
    )

    def to_dict(self):
        return {
            "event_id": str(self.event_id),
            "occurred_at": self.occurred_at,
            "user_id": self.user_id,
            "event_type": self.event_type,
            "properties": self.properties,
        }


class EventRead(EventBase):
    id: int


class EventReadWithCursor(BaseSchema):
    cursor: int | None = None
    response: list[EventRead]
