from flask import request, Blueprint
from app.blueprints.base_blueprint import BaseBlueprint
from app.controllers.stats_controller import StatisticsController



url_prefix = '{}/stats'.format(BaseBlueprint.base_url_prefix)
stats_blueprint = Blueprint('stats', __name__, url_prefix=url_prefix)
stats_controller = StatisticsController(request)


@stats_blueprint.route('/', strict_slashes=False, methods=['GET'])
def stats():
    return stats_controller.get_all_dashboard_stats()
