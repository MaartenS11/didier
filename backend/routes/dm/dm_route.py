from backend.ipc_client import ipc_client
import json
from quart import Blueprint, request, jsonify

dm_blueprint: Blueprint = Blueprint("dm", __name__, url_prefix="/dm")


@dm_blueprint.route("/", methods=["POST"])
async def post_dm():
    """
    Send a DM to the given user
    """
    data = json.loads((await request.body).decode('UTF-8'))

    dm = await ipc_client.request(
        "send_dm",
        user=int(data["userid"]),
        message=data.get("message")
    )

    return jsonify({"response": dm})
