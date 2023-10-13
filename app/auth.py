from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Annotated, Any
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .settings import SECRET_KEY, ALGORITHM
from .schemas import TokenData
from .dals.user_dal import UserDal
from .crypt import oauth2_scheme, verify_password
from .models import User
from .database import db_dependency


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user_dal = UserDal(db)
    user = user_dal.get_user_by_email(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def authenticate_user(db: Session, email: str, password: str) -> User | bool:
    user_dal = UserDal(db)
    user = user_dal.get_user_by_email(email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
