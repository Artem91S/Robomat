import argparse
import json
import sys
from pathlib import Path
import csv
from dateutil import parser as date_parser
from app.core.db_connection import get_db
from app.models.events import EventDB
from app.core.logging import logger


def import_event(csv_path: Path) -> None:
    session = next(get_db())
    all_events = []
    with csv_path.open() as file:
        contents = csv.DictReader(file)
        expected_headers = {
            "event_id",
            "occurred_at",
            "user_id",
            "event_type",
            "properties_json",
        }
        if set(contents.fieldnames) != expected_headers:
            logger.warning(
                f"CSV headers do not match expected headers: {expected_headers}"
            )
            sys.exit(1)
        for row in contents:
            try:
                properties = row.get("properties_json")
                if properties:
                    properties = json.loads(properties)
            except json.JSONDecodeError:
                logger.warning(
                    f"Invalid JSON in properties_json for event_id {row['event_id']}"
                )
                properties = {}

            event = EventDB(
                event_id=row.get("event_id"),
                occurred_at=date_parser.isoparse(row.get("occurred_at")),
                user_id=row.get("user_id"),
                event_type=row.get("event_type"),
                properties=properties,
            )
            all_events.append(event)
        session.add_all(all_events)
        session.commit()
        logger.success(f"Imported {len(all_events)} events from {csv_path}")


def main():
    event_action = argparse.ArgumentParser(
        description="Event on start script save data from csv file to db"
    )
    event_action.add_argument(
        "csv_path",
        type=Path,
        help="Path to CSV file containing event data to import",
    )
    args = event_action.parse_args()
    import_event(args.csv_path)


if __name__ == "__main__":
    main()
