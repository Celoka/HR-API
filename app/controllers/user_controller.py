from app import bcrypt, db
from app.controllers.base_controller import BaseController
from app.services.user_service import User
from app.services.employee_service import EmployeeService
from app.services.leave_request_service import LeaveRequestService
from app.utils.auth import Auth
from app.utils.helper import parse_leave_request_object


role_type = ["Super admin", "Admin", "Staff"]


class UserController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.user_service = User()
        self.employee_service = EmployeeService()
        self.user_leave_request_service = LeaveRequestService()

    def create_user(self, role="Staff"):
        first_name, last_name, email_address, password = self.request_params(
            'firstName', 'lastName', 'emailAddress', 'password')
        user = self.user_service.filter_first(
            **{'email_address': email_address})
        if user:
            return self.handle_response('User with this email already exists', status_code=409)
        password = bcrypt.generate_password_hash(password, 10).decode()
        user = self.user_service.create_user(
            first_name,
            last_name,
            email_address,
            password,
            role=role)
        self.employee_service.create_employee(user.id)
        return self.handle_response('OK', payload={'user': user.serialize()}, status_code=201)

    def create_staff_user(self):
        return self.create_user(role="Staff")

    def create_super_admin_user(self):
        return self.create_user(role="Super admin")

    def login(self):
        email_address, password = self.request_params(
            'emailAddress', 'password')
        user = self.user_service.filter_first(
            **{'email_address': email_address})
        if user:
            if bcrypt.check_password_hash(user.password, password):
                token = Auth.create_token(user.id)
                del user.password
                return self.handle_response('Ok', payload={'user': user.serialize(), 'token': token})
            else:
                return self.handle_response('Wrong password', status_code=400)
        else:
            return self.handle_response('User does not exist', status_code=404)

    def list_users_and_status(self):
        user_leave_statuses = self.user_leave_request_service.fetch_all()
        leave_status_list = [parse_leave_request_object(
            user_leave_status) for user_leave_status in user_leave_statuses.items]
        return self.handle_response('OK', payload={'users_status': leave_status_list, 'meta': self.pagination_meta(user_leave_statuses)})

    def get_manager(self, user_id):
        user = self.user_service.get(user_id)
        if not user:
            return self.handle_response('User not found', status_code=404)
        if user.manager:
            return self.handle_response('OK', payload={
                'managerId': user.manager.id,
                'managerName': user.manager.first_name})
        return self.handle_response('User does not have a manager')

    def get_subordinates(self, user_id):
        user = self.user_service.get(user_id)
        if not user:
            return self.handle_response('User not found', status_code=404)
        subordinates = user.subordinates
        subordinate_data = [{'id': s.id, 'firstName': s.first_name,
                            'lastName': s.last_name} for s in subordinates]
        return self.handle_response('OK', payload={'subordinateData': subordinate_data})

    def assign_manager(self):
        subordinate_id, manager_id, admin_id = self.request_params('subordinateId', 'managerId', 'adminId')

        admin_user = self.user_service.get(admin_id)
        subordinate_user = self.user_service.get(subordinate_id)
        manager = self.user_service.get(manager_id)

        if not subordinate_user or not manager or not admin_user:
            return self.handle_response('Cannot perform this action. User or Manager or Admin User not found', status_code=403)

        if admin_user.role != "Super admin":
            return self.handle_response('Cannot perform this action. Current user is not a super admin', status_code=403)
        
        if subordinate_user.manager_id == manager_id:
            return self.handle_response('A manager has been assigned to this user.', status_code=409)
        
        if manager.role not in ["Super admin"  "Admin"]:
            self.user_service.update(manager, role='Admin')

        subordinate_user.manager = manager
        db.session.commit()

        return self.handle_response('Manager assigned successfully')
