from pydantic import BaseModel, EmailStr, ConfigDict


class TunedModel(BaseModel):
    model_config: ConfigDict = ConfigDict(
        # tells pydantic to convert even non dict obj to json
        from_attributes=True
    )


class TodoBase(BaseModel):
    title: str
    description: str | None = None
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


class UserRead(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class BearerToken(Token):
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None
