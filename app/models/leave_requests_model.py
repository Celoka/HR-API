from .base_model import BaseModel, db
from app.utils.enums import LeaveRequestType



class LeaveRequest(BaseModel):
    __tablename__="leave_requets"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    leave_start = db.Column(db.DateTime, nullable=False)
    leave_end = db.Column(db.DateTime, nullable=False)
    description =  db.Column(db.String(100), nullable=True)
    event_type = db.Column(db.Enum(LeaveRequestType), default="Holiday", nullable=False)
    status = db.Column(db.String(20), default='Pending')
