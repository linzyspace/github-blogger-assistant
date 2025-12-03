from flask import Blueprint, jsonify
from app.admin.validators import validate_admin_action
from app.assistant import get_predefined_or_blog_response

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/status")
def status():
    return jsonify({"status": "ok"})

@admin_bp.route("/check/<action>")
def check_action(action):
    valid = validate_admin_action(action)
    return jsonify({"action": action, "valid": valid})
