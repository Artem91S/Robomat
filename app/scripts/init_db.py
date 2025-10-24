import sys

from app.core.db_connection import Base, engine, SessionLocal
from app.core.logging import logger
from app.models import EventDB
import app.models


def init_db():
    logger.debug("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.debug("Database tables created.")

    with SessionLocal() as session:
        logger.debug("Checking initial data ...")
        exist_data = session.query(EventDB).count()
        if exist_data == 0:
            logger.debug("No data in DB")
            sys.exit(1)
        else:
            logger.debug("Data is already in DB")
            sys.exit(0)


if __name__ == "__main__":
    init_db()
