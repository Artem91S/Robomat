from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect

from app.core.config import Config
from app.api.router import api
from app.core.db_connection import engine

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.OPTIONS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api, prefix=Config.MAIN_ROUTE)


@app.get("/")
def initial():
    return {"message": "Fast API is running!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
