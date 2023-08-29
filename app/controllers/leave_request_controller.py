from app.controllers.base_controller import BaseController
from app.services.leave_request_service import LeaveRequestService
from app.services.user_service import User
from app.utils.helper import conflict_handler

class LeaveRequestController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.leave_request_service = LeaveRequestService()
        self.user_service = User()

    def create_leave_request(self):
        leave_start, leave_end, event_type, description, email_address = self.request_params(
            'leaveStart', 
            'leaveEnd',
            'description',
            'eventType',
            'emailAddress')
        
        user = self.user_service.filter_first(**{'email_address': email_address})
        leave_requests = self.leave_request_service.filter_by(**{
            'user_id': user.id, 
            'status': 'Pending'})
        pending_requests = [leave_request for leave_request in leave_requests.items]

        if len(pending_requests) > 0:
            msg = "Cannot process request because user has pending leave request."
            return self.handle_response("Incomplete Request", conflict_handler(msg,'UserName: '+user.email_address), status_code=409)
        new_leave_request = self.leave_request_service.create_leave_request(
            user.id, leave_start, leave_end, event_type, description
        )
        return self.handle_response('Ok', payload={'request': new_leave_request.serialize()}, status_code=201)

    def get_leave_requests(self, user_id):
        leave_requests = self.leave_request_service.filter_by(**{'user_id': user_id})
        leave_request_list = [leave_request.serialize() for leave_request in leave_requests.items]
        return self.handle_response('Ok', payload={'leave_requests': leave_request_list})
    
    def get_leave_request(self, leave_request_id):
        leave_request = self.leave_request_service.get(leave_request_id)
        return self.handle_response('Ok', payload={'leave_request': leave_request.serialize()})


    def update_leave_request_status(self, leave_request_id):
        status = self.request_params('status')
        leave_request = self.leave_request_service.get(leave_request_id)
        if leave_request:
            data = {}
            if status:
                data['status'] = status
            self.leave_request_service.update(leave_request, **data)
            return self.handle_response('Ok', payload={'status': 'Updated!', 'leave_request': leave_request.serialize()})
        return self.handle_response('Invalid or Incorrect leave_request_id given', status_code=400)
    
    def delete_leave_request_status(self, leave_request_id):
        leave_request = self.leave_request_service.get(leave_request_id)
        data = {}
        if leave_request:
            data['is_deleted'] = True
            self.leave_request_service.update(leave_request, **data)
            return self.handle_response('Ok', payload={'status': 'Deleted!'})
        return self.handle_response('Invalid or incorrect leave_request_id', status_code=400)
