from fastapi.routing import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from .. import schemas, crud
from ..database import get_db


todo_router = APIRouter()


@todo_router.get("/", response_model=list[schemas.Todo])
async def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_todos(db, skip=skip, limit=limit)
