from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app import models  # noqa: F401  (loads the tables before create_all)
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.routers import auth, pages, readings
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

# The session cookie is signed with SECRET_KEY, so it can not be changed
# by the browser. It lasts eight hours.
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key.get_secret_value(),
    max_age=8 * 60 * 60,
    same_site="lax",
    https_only=settings.session_https_only,
)

app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(readings.router)
app.include_router(settings_router.router)
