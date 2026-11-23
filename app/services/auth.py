# Passwords and signed-in users.

from fastapi import Depends, HTTPException, Request
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

password_hash = PasswordHash.recommended()   # Argon2


def hash_password(password):
    return password_hash.hash(password)


def check_password(password, stored_hash):
    return password_hash.verify(password, stored_hash)


def find_user_by_email(db: Session, email):
    return db.scalars(select(User).where(User.email == email.lower())).first()


def create_user(db: Session, name, email, password):
    user = User(name=name.strip(), email=email.lower(), password_hash=hash_password(password))
    db.add(user)
    db.commit()
    return user


def current_user(request: Request, db: Session = Depends(get_db)):
    # The session cookie holds the user's ID after they sign in
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    return db.get(User, user_id)


def require_user(user: User | None = Depends(current_user)):
    # Used by every API route that needs a signed-in user
    if user is None:
        raise HTTPException(401, "Please sign in.")
    return user
