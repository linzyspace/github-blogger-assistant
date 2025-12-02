from flask import Blueprint, request, jsonify
import yaml
import os

admin_bp = Blueprint("admin", __name__)

DATA_FOLDER = "app/data/"

@admin_bp.route("/responses", methods=["GET"])
def get_responses():
    with open(DATA_FOLDER + "responses.yaml") as f:
        return jsonify(yaml.safe_load(f))

@admin_bp.route("/responses", methods=["POST"])
def save_responses():
    data = request.json
    with open(DATA_FOLDER + "responses.yaml", "w") as f:
        yaml.safe_dump(data, f)
    return jsonify({"status": "ok"})

