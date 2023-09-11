from flask import Flask

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.blueprints.base_blueprint import BaseBlueprint
from app.utils.helper import get_env

app = Flask(__name__)

app.config.from_object(get_env("FLASK_ENV"))
app.config['MAIL_SERVER'] = get_env('MAIL_SERVER')
app.config['MAIL_PORT'] = int(get_env('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = get_env('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = get_env('MAIL_PASSWORD')


bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

# Register CORS middleware with specific options
CORS(app, resources={r"/api/*": {"origins": "*"}})

blueprint = BaseBlueprint(app)
blueprint.register()
