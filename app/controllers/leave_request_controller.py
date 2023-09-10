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
        current_user = self.request.user_obj
        user_id = current_user.get('user_id')

        user = self.user_service.get(user_id)

        if not user:
            return self.handle_response("This user does not exist", status_code=404)

        leave_start, leave_end, event_type, description = self.request_params(
            'leaveStart',
            'leaveEnd',
            'eventType',
            'description')

        if event_type not in leave_types:
            return self.handle_response(f"Invalid request type '{event_type}'", status_code=404)

        if not user.manager:
            return self.handle_response("Action cannot be performed. User has not been assigned a manager", status_code=403)

        leave_requests = self.leave_request_service.filter_by(user_id=user_id, status='Pending')
        # if leave_requests.count() > 0:
        #     return self.handle_response("Cannot process request because user has pending leave request.", status_code=409)

        new_leave_request = self.leave_request_service.create_leave_request(
            user_id, leave_start, leave_end, event_type, description)

        user_name = f'{current_user.get("first_name", "").capitalize()} {current_user.get("last_name", "").capitalize()}'
        manager_name = f'{user.manager.first_name.capitalize()} {user.manager.last_name.capitalize()}'
        email_subject = 'User Leave Request'

        send_email(
            to=user.manager.email_address,
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
        manager = self.request.user_obj
        data = self.request.get_json()

        subordinate_id, leave_request_id, status, reason = (
            data.get('subordinateId'),
            data.get('leaveRequestId'),
            data.get('status'),
            data.get('reason')
        )

        if status not in status_types:
            return self.handle_response(f"Invalid request type '{status}' ", status_code=404)

        user = self.user_service.get(subordinate_id)
        leave_request = self.leave_request_service.get(leave_request_id)

        if not user:
            return self.handle_response('User not found', status_code=404)

        if (user.manager_id == manager['user_id'] or manager['role'] == "Super admin"):
            return self.handle_response('This user is not the subordinate of this manager, therefore this action cannot be processed', status_code=400)

        if leave_request:
            updated_leave_request = self.leave_request_service.update(
                leave_request,
                status=status,
                reason=reason,
                actioned_by=manager['user_id']
            )
            manager_first_name = manager['first_name']
            manager_last_name = manager['last_name']

            user_name = f'{user.first_name.capitalize()} {user.last_name.capitalize()}'
            manager_name = f'{manager_first_name.capitalize()} {manager_last_name.capitalize()}'

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
