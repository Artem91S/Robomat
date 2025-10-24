from datetime import date, timedelta

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import EventDB
from app.schemas.analytics import (
    UserCountByDateResponse,
    UserCountParams,
    UserTopParams,
    EventTopResponse,
    EventCountTopResponse,
)
from app.schemas.events import EventRead, EventReadWithCursor


class AnalyticsService:
    def users_by_day(
        self, params: UserCountParams, session: Session
    ) -> UserCountByDateResponse:
        count_unique_ids = (
            session.query(EventDB.user_id)
            .distinct()
            .filter(EventDB.occurred_at.between(params.from_, params.to))
            .count()
        )
        return UserCountByDateResponse(
            user_count=count_unique_ids,
            params=params,
        )

    def top_events(
        self, params: UserTopParams, session: Session
    ) -> EventCountTopResponse:
        top_events_query = (
            select(
                EventDB.event_type, func.count(EventDB.event_id).label("event_count")
            )
            .select_from(EventDB)
            .filter(EventDB.occurred_at.between(params.from_, params.to))
            .group_by(EventDB.event_type)
            .order_by(func.count(EventDB.event_id).desc())
            .limit(params.limit)
        )
        top_events = session.execute(top_events_query).all()
        return EventCountTopResponse(
            count=len(top_events),
            response=[EventTopResponse.model_validate(event) for event in top_events],
        )

    def retention_analysis(
        self,
        start_date: date,
        window: int,
        page_size: int,
        last_id: int | None,
        session: Session,
    ) -> EventReadWithCursor:
        # window will be month
        end_date = start_date + timedelta(days=window * 30)
        query_data = (
            select(EventDB)
            .filter(EventDB.occurred_at.between(start_date, end_date))
            .order_by(EventDB.occurred_at.desc())
            .limit(page_size)
        )
        if last_id is not None:
            query_data = query_data.filter(EventDB.id > last_id)

        all_data = session.execute(query_data).scalars().all()

        return EventReadWithCursor(
            response=[EventRead.model_validate(event) for event in all_data],
            cursor=all_data[-1].id if all_data else None,
        )
