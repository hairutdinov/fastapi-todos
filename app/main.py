import uvicorn
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from . import models
from .database import engine
from .routers import todo, user
from .dependencies import get_token_header

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo App")

main_api_router = APIRouter()

main_api_router.include_router(todo.router, prefix="/todos", tags=["todo"])
main_api_router.include_router(user.router, prefix="/users", tags=["user"])

app.include_router(main_api_router)

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}


class Item(BaseModel):
    id: str
    title: str
    description: str | None = None


@app.post("/items", dependencies=[Depends(get_token_header)], response_model=Item, status_code=201)
async def create_item(item: Item) -> Item:
    if item.id in fake_db:
        raise HTTPException(status_code=400, detail="Item already exists")
    fake_db[item.id] = item
    return item


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
