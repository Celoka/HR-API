from flask import request, Blueprint
from app.blueprints.base_blueprint import BaseBlueprint
from app.controllers.user_controller import UserController


url_prefix = '{}/user'.format(BaseBlueprint.base_url_prefix)
user_blueprint = Blueprint('user', __name__, url_prefix=url_prefix)
user_controller = UserController(request)


@user_blueprint.route('/', strict_slashes=False, methods=['POST'])
def create_user():
    return user_controller.create_user()


@user_blueprint.route('/login', strict_slashes=False, methods=['POST'])
def login():
    return user_controller.login()
