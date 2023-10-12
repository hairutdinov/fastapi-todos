from pydantic import BaseModel, EmailStr


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class TodoBase(BaseModel):
    title: str
    description: str
    priority: int


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase, TunedModel):
    id: int
    user_id: int


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase, TunedModel):
    id: int
    is_active: bool
    todos: list[Todo] = []
