from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Setting(Base):
    # One row only (settingID 1) holding the moisture levels
    __tablename__ = "setting"

    setting_id: Mapped[int] = mapped_column("settingID", Integer, primary_key=True)
    dry_threshold: Mapped[int] = mapped_column("dryThreshold", Integer, nullable=False, default=30)
    wet_threshold: Mapped[int] = mapped_column("wetThreshold", Integer, nullable=False, default=70)
