import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MAIN_ROUTE = "/api/v1"
    TZ = "Europe/Kyiv"
    DB_URL = os.environ.get("DATABASE_URL")
    OPTIONS = ["*"]
    TEST_DB_URL = os.environ.get("TEST_DB_URL")
