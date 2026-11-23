from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from app import models  # noqa: F401  (loads the tables before create_all)
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.routers import pages, readings
from app.routers import settings as settings_router
from app.services.readings import add_simulated_history, get_levels


@asynccontextmanager
async def lifespan(app: FastAPI):
    # When the app starts: make any missing tables, the settings row
    # and, on an empty database, a week of simulated readings
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        get_levels(db)
        add_simulated_history(db)
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

app.include_router(pages.router)
app.include_router(readings.router)
app.include_router(settings_router.router)


@app.post("/api/login")
def login():
    # The login form is ready but real accounts are not built yet
    raise HTTPException(501, "Sign in is not connected yet. Accounts will be added next.")
