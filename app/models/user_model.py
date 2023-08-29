from .base_model import BaseModel, db
from app.utils.enums import PermissionLevels



class UserModel(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email_address = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(750), nullable=False)
    role = db.Column(db.Enum(PermissionLevels), default="Staff", nullable=False)

    employee = db.relationship('Employee', backref='user', uselist=False)
