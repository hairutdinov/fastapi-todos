from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..dals.todo_dal import TodoDal
from ..database import db_dependency


router = APIRouter()


@router.get("/", response_model=list[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db=db_dependency):
    todo_dal = TodoDal(db)
    return todo_dal.get_todos(skip=skip, limit=limit)
