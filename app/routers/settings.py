from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.auth import require_user
from app.services.readings import get_levels

router = APIRouter(
    prefix="/api/settings",
    tags=["settings"],
    dependencies=[Depends(require_user)],
)


class Levels(BaseModel):
    dry_threshold: int = Field(ge=5, le=60)
    wet_threshold: int = Field(ge=40, le=95)


@router.get("")
def read_settings(db: Session = Depends(get_db)):
    levels = get_levels(db)
    return {"dry_threshold": levels.dry_threshold, "wet_threshold": levels.wet_threshold}


@router.put("")
def update_settings(new_levels: Levels, db: Session = Depends(get_db)):
    if new_levels.dry_threshold >= new_levels.wet_threshold:
        raise HTTPException(400, "The dry level must be lower than the wet level.")

    levels = get_levels(db)
    levels.dry_threshold = new_levels.dry_threshold
    levels.wet_threshold = new_levels.wet_threshold
    db.commit()
    return {"dry_threshold": levels.dry_threshold, "wet_threshold": levels.wet_threshold}
