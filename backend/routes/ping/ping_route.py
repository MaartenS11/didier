from backend.ipc_client import ipc_client
from quart import Blueprint, jsonify
from time import time

ping_blueprint: Blueprint = Blueprint("ping", __name__, url_prefix="/ping")


@ping_blueprint.route("/", methods=["GET"])
async def get_ping():
    """
    Send a ping request, monitors bot latency and endpoint time
    """
    latency = await ipc_client.request("get_bot_latency")

    return jsonify({"bot_latency": latency, "response_sent": time()})
