from quart import Blueprint

command_stats_blueprint: Blueprint = Blueprint("command_stats", __name__, "/commands")


@command_stats_blueprint.route("/", methods=["GET"])
def get_commands():
    return {}, 200
