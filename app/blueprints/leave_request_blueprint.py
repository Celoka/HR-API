from flask import request, Blueprint
from app.blueprints.base_blueprint import BaseBlueprint
from app.controllers.leave_request_controller import LeaveRequestController

url_prefix = '{}/leave_request'.format(BaseBlueprint.base_url_prefix)
leave_request_blueprint = Blueprint('leave_request', __name__, url_prefix=url_prefix)
leave_request_controller = LeaveRequestController(request)


@leave_request_blueprint.route('/', strict_slashes=False, methods=['POST'])
def create_leave_request():
    return leave_request_controller.create_leave_request()


@leave_request_blueprint.route('/<int:user_id>', strict_slashes=False, methods=['GET'])
def list_leave_requests(user_id):
    return leave_request_controller.get_leave_requests(user_id)


@leave_request_blueprint.route('/<int:leave_request_id>/', strict_slashes=False, methods=['GET'])
def get_leave_request(leave_request_id):
    return leave_request_controller.get_leave_request(leave_request_id)


@leave_request_blueprint.route('/<int:leave_request_id>/', strict_slashes=False, methods=['PUT'])
def update_leave_request(leave_request_id):
    return leave_request_controller.update_leave_request_status(leave_request_id)


@leave_request_blueprint.route('<int:leave_request_id>/', strict_slashes=False, methods=['DELETE'])
def delete_leave_request(leave_request_id):
    return leave_request_controller.delete_leave_request_status(leave_request_id)
