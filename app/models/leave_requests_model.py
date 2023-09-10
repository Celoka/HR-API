from .base_model import BaseModel, db
from sqlalchemy import Enum
from app.utils.enums import LeaveRequestType



class LeaveRequest(BaseModel):
    __tablename__="leave_requets"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    leave_start = db.Column(db.DateTime, nullable=False)
    leave_end = db.Column(db.DateTime, nullable=False)
    description =  db.Column(db.String(100), nullable=True)
    is_paid_leave = db.Column(db.String(120), default='Yes')
    event_type = db.Column(db.Enum(LeaveRequestType), default="Holiday", nullable=False)
    status = db.Column(db.String(120), default='Pending')
    reason = db.Column(db.String(250), nullable=True)
    actioned_by = db.Column(db.Integer, nullable=True)

    user = db.relationship("UserModel", back_populates="leave_requests")
