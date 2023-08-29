import os

from flask import Flask
from flask_bcrypt import Bcrypt

from flask_sqlalchemy import SQLAlchemy
from app.blueprints.base_blueprint import BaseBlueprint
from flask_migrate import Migrate
from config import ProdConfig


app = Flask(__name__)
app.config.from_object(ProdConfig)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

blueprint = BaseBlueprint(app)
blueprint.register()
