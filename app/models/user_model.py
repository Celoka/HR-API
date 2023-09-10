from .base_model import BaseModel, db
from app.utils.enums import PermissionLevels



class UserModel(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email_address = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(200),  nullable=True)
    role = db.Column(db.Enum(PermissionLevels), default="Staff", nullable=False)

    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    manager = db.relationship('UserModel', remote_side='UserModel.id', backref='subordinates')


    employee = db.relationship('Employee', backref='user', uselist=False)
    leave_requests = db.relationship("LeaveRequest", back_populates="user")
 