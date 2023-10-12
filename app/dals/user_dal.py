from sqlalchemy.orm import Session
from .. import models, schemas


class UserDal:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, user_id: int):
        return self.session.query(models.User).\
            filter(models.User.id == user_id).\
            first()

    def get_user_by_email(self, email: str):
        return self.session.query(models.User).\
            filter(models.User.email == email).\
            first()

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.session.query(models.User).offset(skip).limit(limit).all()

    def create_user(self, user: schemas.UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(
            email=user.email,
            hashed_password=fake_hashed_password,
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def create_user_todo(self, todo: schemas.TodoCreate, user_id: int):
        db_item = models.Todo(**todo.model_dump(), user_id=user_id)
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item
