from app.controllers.base_controller import BaseController
from app.services.leave_request_service import LeaveRequestService
from app.services.user_service import User
from app.utils.helper import conflict_handler, parse_calendar_events
from app.utils.send_mail import send_email


leave_types = ["Holiday",
               "Time off",
               "Sick leave", "Maternity leave",
               "Paternity leave", "Training day"]
status_types = ["Approved", "Rejected", "Pending"]


class LeaveRequestController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.leave_request_service = LeaveRequestService()
        self.user_service = User()

    def create_leave_request(self):
        user_id, leave_start, leave_end, event_type, description = self.request_params(
            'userId',
            'leaveStart',
            'leaveEnd',
            'eventType',
            'description')

        if event_type not in leave_types:
            return self.handle_response(f"Invalid request type '{event_type}' ", status_code=404)

        user = self.user_service.get(user_id)
        manager = self.user_service.get(user.manager_id)

        if not manager:
            return self.handle_response(f"Action cannot be performed. User has not been assigned a manager", status_code=403)

        if not user:
            return self.handle_response(f"This user does not exist", status_code=404)
        
        leave_requests = self.leave_request_service.filter_by(**{
            'user_id': user.id,
            'status': 'Pending'})

        pending_requests = [leave_request for leave_request in leave_requests.items]

        # if len(pending_requests) > 0:
        #     msg = "Cannot process request because user has pending leave request."
        #     return self.handle_response("Incomplete Request", conflict_handler(msg, 'UserName: '+user.email_address), status_code=409)
        
        new_leave_request = self.leave_request_service.create_leave_request(user_id, leave_start, leave_end, event_type, description
        )

        user_name = f'{user.first_name.capitalize()} {user.last_name.capitalize()}'
        manager_name = f'{manager.first_name.capitalize()} {manager.last_name.capitalize()}'
        email_subject = 'User Leave Request'
        send_email(
            to=manager.email_address,
            subject=email_subject,
            template='request_notification_template',
            user=user_name,
            manager=manager_name,
        )
        print('Email Sent Successfully!')

        return self.handle_response('Ok', payload={'request': new_leave_request.serialize()}, status_code=201)

    def get_calendar_events(self, user_id):
        event_list = []
        events = leave_requests = self.leave_request_service.filter_by(
            **{'user_id': user_id})
        if leave_requests:
            event_list = [parse_calendar_events(event)
                                  for event in events.items]
        return self.handle_response('Ok', payload={'calendar_events': event_list})

    def get_leave_requests(self, user_id):
        leave_request_list = []
        leave_requests = self.leave_request_service.filter_by(
            **{'user_id': user_id})
        if leave_requests:
            leave_request_list = [leave_request.serialize()
                                  for leave_request in leave_requests.items]
        return self.handle_response('Ok', payload={'leave_requests': leave_request_list})

    def get_leave_request(self, leave_request_id):
        leave_request = self.leave_request_service.get(leave_request_id)
        result = leave_request.serialize() if leave_request else {}
        return self.handle_response('Ok', payload={'leave_request': result})

    def update_leave_request_status(self):
        data = self.request.get_json()
        user_id, manager_id, leave_request_id, status, reason = (
            data.get('userId'),
            data.get('managerId'),
            data.get('leaveRequestId'),
            data.get('status'),
            data.get('reason')
        )

        if status not in status_types:
            return self.handle_response(f"Invalid request type '{status}' ", status_code=404)

        user = self.user_service.get(user_id)
        manager = self.user_service.get(manager_id)
        leave_request = self.leave_request_service.get(leave_request_id)

        if not user:
            return self.handle_response('User not found', status_code=404)

        if not (user.manager_id == manager_id or manager.role == "Super admin"):
            return self.handle_response('This user is not the subordinate of this manager, therefore this action cannot be processed', status_code=400)

        if leave_request:
            updated_leave_request = self.leave_request_service.update(
                leave_request,
                status=status,
                reason=reason,
                actioned_by=manager_id
            )
            user_name = f'{user.first_name.capitalize()} {user.last_name.capitalize()}'
            manager_name = f'{manager.first_name.capitalize()} {manager.last_name.capitalize()}'
            email_subject = f'Leave Request - {status.capitalize()}'
            send_email(
                to=user.email_address,
                subject=email_subject,
                template='request_response_template',
                user=user_name,
                manager=manager_name
            )
            return self.handle_response('Ok', payload={'status': 'Updated!', 'leave_request': updated_leave_request.serialize()})

        return self.handle_response('Invalid or Incorrect leave_request_id given', status_code=400)


    def delete_leave_request_status(self, leave_request_id):
        leave_request = self.leave_request_service.get(leave_request_id)
        data = {}
        if leave_request:
            data['is_deleted'] = True
            self.leave_request_service.update(leave_request, **data)
            return self.handle_response('Ok', payload={'status': 'Deleted!'})
        return self.handle_response('Invalid or incorrect leave_request_id', status_code=400)
