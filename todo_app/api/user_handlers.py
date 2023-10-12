from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db


class EmailAlreadyRegistered(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Email already registered")


user_router = APIRouter()


@user_router.post("/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise EmailAlreadyRegistered()
    return crud.create_user(db, user)


@user_router.get("/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)


@user_router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)


@user_router.post("/{user_id}/todos", response_model=schemas.Todo)
async def create_todo_for_user(user_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_user_todo(db, user_id=user_id, todo=todo)