import uvicorn
from fastapi.routing import APIRouter
from fastapi import FastAPI

from . import models
from .database import engine
from .api.todo_handlers import todo_router
from .api.user_handlers import user_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

main_api_router = APIRouter()

main_api_router.include_router(todo_router, prefix="/todos", tags=["todo"])
main_api_router.include_router(user_router, prefix="/users", tags=["user"])

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run("todo_app.main:app", host="0.0.0.0", port=8000, reload=True)
