from flask import request, Blueprint
from app.blueprints.base_blueprint import BaseBlueprint
from app.controllers.user_controller import UserController


url_prefix = '{}/user'.format(BaseBlueprint.base_url_prefix)
user_blueprint = Blueprint('user', __name__, url_prefix=url_prefix)
user_controller = UserController(request)


@user_blueprint.route('/create', strict_slashes=False, methods=['POST'])
def create_staff_user():
    return user_controller.create_staff_user()


@user_blueprint.route('/super-admin/create', strict_slashes=False, methods=['POST'])
def create_super_admin_user():
    return user_controller.create_super_admin_user()


@user_blueprint.route('/login', strict_slashes=False, methods=['POST'])
def login():
    return user_controller.login()


@user_blueprint.route('/admin/all-users', strict_slashes=False, methods=['GET'])
def get_users_and_status():
    return user_controller.list_users_and_status()


@user_blueprint.route('/manager/<int:user_id>', methods=['GET'])
def get_manager(user_id):
    return user_controller.get_manager(user_id)


@user_blueprint.route('/manager/subordinates/<int:user_id>', methods=['GET'])
def get_subordinate(user_id):
    return user_controller.get_subordinates(user_id)


@user_blueprint.route('/assign-manager', methods=['POST'])
def assign_manager():
    return user_controller.assign_manager()
