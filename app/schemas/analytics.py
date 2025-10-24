from app.schemas.base import BaseSchema
from datetime import date


class UserCountParams(BaseSchema):
    from_: date
    to: date


class UserTopParams(UserCountParams):
    limit: int


class UserCountByDateResponse(BaseSchema):
    user_count: int
    params: UserCountParams


class EventTopResponse(BaseSchema):
    event_type: str
    event_count: int


class EventCountTopResponse(BaseSchema):
    response: list[EventTopResponse]
    count: int
