from .command_stats import command_stats_blueprint
from quart import Blueprint

stats_blueprint: Blueprint = Blueprint("stats", __name__, url_prefix="/stats")
stats_blueprint.register_blueprint(command_stats_blueprint)


@stats_blueprint.route("/", methods=["GET"])
def get_nested_routes():
    nested_routes = {
        "commands": "/stats/commands"
    }

    return {"nested": nested_routes}, 200
