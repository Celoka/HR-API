
class BaseBlueprint:
    base_url_prefix = '/api/v1'

    def __init__(self, app):
        self.app = app

    def register(self):
        """All Blueprints are registered here"""
        from app.blueprints.user_blueprint import user_blueprint
        from app.blueprints.leave_request_blueprint import leave_request_blueprint
        from app.blueprints.home_blueprint import home_blueprint


        self.app.register_blueprint(user_blueprint)
        self.app.register_blueprint(leave_request_blueprint)
        self.app.register_blueprint(home_blueprint)
