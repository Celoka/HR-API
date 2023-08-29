from .base_model import BaseModel, db



class Employee(BaseModel):
    __tablename__ = "employees"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=True)
