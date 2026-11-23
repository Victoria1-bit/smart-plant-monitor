# Makes one account for trying the app on your own computer.
# Run with:  python -m app.create_dev_user

from app import models  # noqa: F401
from app.database import Base, SessionLocal, engine
from app.services.auth import create_user, find_user_by_email

EMAIL = "plant@example.com"
PASSWORD = "plant-dev-password"

Base.metadata.create_all(engine)
with SessionLocal() as db:
    if find_user_by_email(db, EMAIL):
        print("The development account already exists:", EMAIL)
    else:
        create_user(db, "Plant Owner", EMAIL, PASSWORD)
        print("Created", EMAIL, "with the password in app/create_dev_user.py")
