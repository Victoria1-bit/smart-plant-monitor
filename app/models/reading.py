from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Reading(Base):
    __tablename__ = "reading"

    reading_id: Mapped[int] = mapped_column("readingID", Integer, primary_key=True)
    # Soil moisture as a percentage, 0 to 100
    moisture: Mapped[int] = mapped_column(Integer, nullable=False)
    # True until real readings arrive from the sensor
    simulated: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    recorded_at: Mapped[datetime] = mapped_column("recordedAt", DateTime, nullable=False, index=True)
