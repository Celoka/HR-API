from app.services.base_service import BaseService
from app.models.employee_model import Employee


class EmployeeService(BaseService):

    def __init__(self):
        BaseService.__init__(self, Employee)

    def create_employee(self,
                    user_id,
                    location=None):
        employee = Employee(
                    user_id=user_id,
                    location=location)
        employee.save()
        return employee
