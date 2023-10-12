from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..dals.user_dal import UserDal
from ..database import get_db


class EmailAlreadyRegistered(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Email already registered")


router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, db: Session = Depends(get_db)
) -> schemas.User:
    user_dal = UserDal(db)
    db_user = user_dal.get_user_by_email(email=user.email)
    if db_user:
        raise EmailAlreadyRegistered()
    return user_dal.create_user(user)


@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    user_dal = UserDal(db)
    return user_dal.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user_dal = UserDal(db)
    return user_dal.get_user(user_id)


@router.post("/{user_id}/todos", response_model=schemas.Todo)
def create_todo_for_user(
    user_id: int, todo: schemas.TodoCreate, db: Session = Depends(get_db)
):
    user_dal = UserDal(db)
    return user_dal.create_user_todo(user_id=user_id, todo=todo)
