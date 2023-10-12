from sqlalchemy.orm import Session
from .. import models, schemas


class TodoDal:
    def __init__(self, session: Session):
        self.session = session

    def get_todos(self, skip: int = 0, limit: int = 100):
        return self.session.query(models.Todo).offset(skip).limit(limit).all()
