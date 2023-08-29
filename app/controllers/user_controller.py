from app import bcrypt
from app.controllers.base_controller import BaseController
from app.services.user_service import User
from app.services.employee_service import EmployeeService
from app.utils.auth import Auth

class UserController(BaseController):
    def __init__(self, request):
        BaseController.__init__(self, request)
        self.user_service = User()
        self.employee_service = EmployeeService()
        
    def create_user(self):
        first_name, last_name, email_address, password = self.request_params(
            'firstName', 'lastName', 'emailAddress', 'password')
        user = self.user_service.filter_first(**{'email_address': email_address})
        if user:
            return self.handle_response('User with this email already exists', status_code=409)
        password = bcrypt.generate_password_hash(password, 10).decode()
        user = self.user_service.create_user(first_name, last_name, email_address, password)
        employee = self.employee_service.create_employee(user.id)
        return self.handle_response('OK', payload={'user': user.serialize()}, status_code=201)
    
    def login(self):
        email_address, password = self.request_params('emailAddress', 'password')
        user = self.user_service.filter_first(**{'email_address': email_address})
        if user:
            if bcrypt.check_password_hash(user.password, password):
                token = Auth.create_token(user.id)
                del user.password
                return self.handle_response('Ok', payload={'user': user.serialize(), 'token': token})
            else:
                return self.handle_response('Wrong password', status_code=400)
        else:
            return self.handle_response('User does not exist', status_code=404)
