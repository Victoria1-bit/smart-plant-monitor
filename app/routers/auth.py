from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.services import auth as auth_service

router = APIRouter(prefix="/api/auth", tags=["auth"])


class RegisterForm(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginForm(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


@router.post("/register", status_code=201)
def register(form: RegisterForm, request: Request, db: Session = Depends(get_db)):
    if auth_service.find_user_by_email(db, form.email):
        raise HTTPException(409, "An account with this email already exists.")

    user = auth_service.create_user(db, form.name, form.email, form.password)

    # Sign the new user in straight away
    request.session.clear()
    request.session["user_id"] = user.user_id
    return {"name": user.name, "email": user.email}


@router.post("/login")
def login(form: LoginForm, request: Request, db: Session = Depends(get_db)):
    user = auth_service.find_user_by_email(db, form.email)

    # The same message for a wrong email and a wrong password,
    # so nobody can find out which emails have accounts
    if user is None or not auth_service.check_password(form.password, user.password_hash):
        raise HTTPException(401, "The email or password is incorrect.")

    request.session.clear()
    request.session["user_id"] = user.user_id
    return {"name": user.name, "email": user.email}


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Signed out."}


@router.get("/me")
def me(user: User = Depends(auth_service.require_user)):
    return {"name": user.name, "email": user.email}
