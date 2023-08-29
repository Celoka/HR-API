from app.services.base_service import BaseService
from app.models.leave_requests_model import LeaveRequest


class LeaveRequestService(BaseService):

    def __init__(self):
        BaseService.__init__(self, LeaveRequest)

    def create_leave_request(self,
                      user_id, 
                      leave_start,
                      leave_end,
                      event_type,
                      status="Pending",
                      description=None):
        leave_request = LeaveRequest(
            user_id=user_id,
            leave_start=leave_start,
            leave_end=leave_end,
            event_type=event_type,
            status=status,
            description=description
        )
        leave_request.save()
        return leave_request
