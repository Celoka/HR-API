from flask.cli import FlaskGroup
from flask import request

from app.utils.auth import Auth
from app import app, db

# Create a FlaskGroup to manage commands
cli = FlaskGroup(app)


@app.before_request
def check_token():
    decoded_token = Auth.check_token()
    request.user_obj = decoded_token['sub']

@cli.command()
def create_db():
    """Create the database tables."""
    db.create_all()
    print("Database tables created.")


@cli.command()
def drop_db():
    """Drop all database tables."""
    db.drop_all()
    print("All database tables dropped.")


if __name__ == "__main__":
    cli()
