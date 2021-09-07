from werkzeug.exceptions import abort

from .error_handlers import handler_404, handler_422
from .json_encoder import CustomEncoder
from .routes.dm import dm_blueprint
from .routes.ping import ping_blueprint
from .routes.stats import stats_blueprint
from functions.database import custom_commands
from quart import Quart, jsonify, Response
from quart_cors import cors


# Initialize app
app = Quart(__name__)
# TODO allow_origin=re.compile(r"http://localhost:.*")
#      needs higher Python & Quart version
app = cors(app, allow_origin="*")
app.url_map.strict_slashes = False
app.json_encoder = CustomEncoder

# Register blueprints
app.register_blueprint(dm_blueprint)
app.register_blueprint(ping_blueprint)
app.register_blueprint(stats_blueprint)


@app.route("/custom", methods=["GET"])
async def get_all_custom_commands():
    """
    Return a list of all custom commands in the bot
    """
    commands = custom_commands.get_all()

    return jsonify(commands)


@app.route("/custom/<command_id>")
async def get_custom_command(command_id):
    try:
        command_id = int(command_id)
    except ValueError:
        # Id is not an int
        abort(422, "Parameter id was not a valid integer.")

    command = custom_commands.get_by_id(command_id)

    if command is None:
        abort(404)

    return jsonify(command)


@app.errorhandler(404)
def page_not_found(e):
    return handler_404(e)


@app.errorhandler(422)
def unprocessable_entity(e):
    return handler_422(e)
