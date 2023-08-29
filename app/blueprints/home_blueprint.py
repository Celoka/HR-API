from flask import Blueprint
from app.blueprints.base_blueprint import BaseBlueprint


url_prefix = '{}/'.format(BaseBlueprint.base_url_prefix)
home_blueprint = Blueprint('home', __name__, url_prefix=url_prefix)


@home_blueprint.route('/', methods=['GET'])
def hello():
    return '''<h1>Welcome to Spotnet Streams</h1> '''
