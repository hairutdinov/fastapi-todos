from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta


from ..database import get_db
from ..auth import authenticate_user, create_access_token
from ..schemas import BearerToken
from ..settings import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter()


@router.post("/", response_model=BearerToken)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}
