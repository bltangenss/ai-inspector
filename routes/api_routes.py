from flask import Blueprint, jsonify
from models.database import get_history

api_bp = Blueprint("api", __name__)


@api_bp.route("/history", methods=["GET"])
def history():
    rows = get_history(limit=50)
    return jsonify({"success": True, "data": rows})
