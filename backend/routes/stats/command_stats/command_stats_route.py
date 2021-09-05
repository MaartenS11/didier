from functions.database.commands import query_command_stats
from quart import Blueprint

command_stats_blueprint: Blueprint = Blueprint("command_stats", __name__, url_prefix="/commands")


@command_stats_blueprint.route("/", methods=["GET"])
def get_commands():
    return {"usage": query_command_stats()}, 200
