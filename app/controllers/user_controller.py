from app import bcrypt, db
from app.controllers.base_controller import BaseController
from app.services.user_service import User
from app.services.employee_service import EmployeeService
from app.services.leave_request_service import LeaveRequestService
from app.utils.auth import Auth
from app.utils.helper import parse_leave_request_object, remove_password


STAFF = 'Staff'
ADMIN = 'Admin'
SUPER_ADMIN = 'Super admin'
ROLE_TYPE = [SUPER_ADMIN, ADMIN]



class UserController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.user_service = User()
        self.employee_service = EmployeeService()
        self.leave_request_service = LeaveRequestService()

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
        return self.create_user(role=STAFF)

    def create_super_admin_user(self):
        return self.create_user(role=SUPER_ADMIN)

    def login(self):
        email_address, password = self.request_params('emailAddress', 'password')
        user = self.user_service.filter_first(email_address=email_address)
        if user:
            if bcrypt.check_password_hash(user.password, password):
                user_obj = {
                    'user_id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email_address': user.email_address,
                    'role': user.role
                }
                token = Auth.create_token(user_obj)
                del user.password
                return self.handle_response('Ok', payload={'user': user.serialize(), 'token': token})
            else:
                return self.handle_response('Wrong password', status_code=400)
        else:
            return self.handle_response('User does not exist', status_code=404)

    def list_users_and_status(self):
        users_with_leave_requests = []
        all_users = self.user_service.fetch_all()

        for user in all_users:
            user_data = user.serialize()

            if user.manager:
                manager_name = f'{user.manager.first_name} {user.manager.last_name}'
                user_data['manager'] = {
                    'managerName': manager_name,
                    'managerid': user.manager.id
                }
            else:
                user_data['managerName'] = None

            leave_requests = self.leave_request_service.filter_by(user_id=user.id)
            user_data['leave_requests'] = [leave_request.serialize()
                                        for leave_request in leave_requests]

            del user_data['managerId']
            del user_data['password']

            users_with_leave_requests.append(user_data)

        return self.handle_response('OK', payload={'users': users_with_leave_requests})


    # def get_manager(self, user_id):
    #     user = self.user_service.get(user_id)
    #     if not user:
    #         return self.handle_response('User not found', status_code=404)
    #     if user.manager:
    #         return self.handle_response('OK', payload={
    #             'managerId': user.manager.id,
    #             'managerName': user.manager.first_name})
    #     return self.handle_response('User does not have a manager')

    # def get_subordinates(self, user_id):
    #     user = self.user_service.get(user_id)
    #     if not user:
    #         return self.handle_response('User not found', status_code=404)
    #     subordinates = user.subordinates
    #     subordinate_data = [{'id': s.id, 'firstName': s.first_name,
    #                         'lastName': s.last_name} for s in subordinates]
    #     return self.handle_response('OK', payload={'subordinateData': subordinate_data})

    def assign_manager(self):
        subordinate_id, manager_id, super_admin_id = self.request_params('subordinateId', 'managerId', 'superAdminId')

        manager = self.user_service.get(manager_id)
        subordinate_user = self.user_service.get(subordinate_id)
        super_admin = self.user_service.get(super_admin_id)

        if not subordinate_user or not manager:
            return self.handle_response('Cannot perform this action. User or Manager or Admin User not found', status_code=403)

        if super_admin.role != SUPER_ADMIN:
            return self.handle_response('Cannot perform this action. Current user is not a super admin', status_code=403)
        
        if subordinate_user.manager_id == manager_id:
            return self.handle_response('A manager has been assigned to this user.', status_code=409)
        
        if manager.role not in ROLE_TYPE:
            self.user_service.update(manager, role='Admin')

        subordinate_user.manager = manager
        db.session.commit()

        return self.handle_response('Manager assigned successfully')
 

    def uplift_staff_to_manager(self):
        user_id, super_admin_id = self.request_params('userId', 'superAdminId')

        user = self.user_service.get(user_id)
        super_admin = self.user_service.get(super_admin_id)

        if not user or not super_admin:
            return self.handle_response('Cannot perform this action. User or Admin User not found', status_code=403)
        
        if super_admin.role != SUPER_ADMIN:
            return self.handle_response('Cannot perform this action. Current user is not a super admin', status_code=403)            
        
        if user.role not in ROLE_TYPE:
            self.user_service.update(user, role=ADMIN)
            return self.handle_response('Admin role assigned successfully')
        return self.handle_response('This user is already an admin', status_code=200)
