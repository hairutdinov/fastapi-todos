from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import Depends, BackgroundTasks, Path
from sqlalchemy.orm import Session
from typing import Annotated

from .. import schemas
from ..dals.user_dal import UserDal
from ..database import db_dependency
from ..auth import oauth2_scheme
from ..auth import get_current_active_user
from .. import models


class EmailAlreadyRegistered(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Email already registered")


def send_email_notification(email: str, message: str):
    with open("log.txt", "w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: db_dependency) -> schemas.User:
    user_dal = UserDal(db)
    db_user = user_dal.get_user_by_email(email=user.email)
    if db_user:
        raise EmailAlreadyRegistered()
    return user_dal.create_user(user)


@router.get("/", response_model=list[schemas.User])
def read_users(db: db_dependency, skip: int = 0, limit: int = 100):
    user_dal = UserDal(db)
    return user_dal.get_users(skip=skip, limit=limit)


@router.get("/me", response_model=schemas.UserRead)
async def read_users_me(
    current_user: Annotated[models.User, Depends(get_current_active_user)]
):
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: Annotated[int, Path(gt=0)], db: db_dependency):
    user_dal = UserDal(db)
    return user_dal.get_user(user_id)


@router.post("/{user_id}/todos", response_model=schemas.Todo)
def create_todo_for_user(user_id: int, todo: schemas.TodoCreate, db: db_dependency):
    user_dal = UserDal(db)
    return user_dal.create_user_todo(user_id=user_id, todo=todo)


@router.post("/send-notification/{email}")
async def create_user(
    email: str, bgc_task: BackgroundTasks, token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    bgc_task.add_task(send_email_notification, email=email, message="Some notification")
    return {"message": "Notification sent in the background"}
