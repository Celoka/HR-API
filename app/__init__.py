import os

from flask_api import FlaskAPI
from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy
from app.blueprints.base_blueprint import BaseBlueprint
from flask_migrate import Migrate
from app.utils.helper import get_env


app = FlaskAPI(__name__)
app.config.from_object(get_env("FLASK_ENV"))

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

blueprint = BaseBlueprint(app)
blueprint.register()
