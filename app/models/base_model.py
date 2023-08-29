from app import db
from sqlalchemy import exc
from datetime import datetime
from app.utils import convert_to_camel_case

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer(), primary_key=True)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    created_at  = db.Column(db.DateTime(), default=datetime.now())
    updated_at  = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())


    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except(exc.IntegrityError, exc.InvalidRequestError):
            db.session().rollback()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        serialized = {
            convert_to_camel_case(column.name): getattr(self, column.name) for column in self.__table__.columns if column.name not in ['created_at', 'update_at']
        }
        return serialized
