from flask import Flask, request, jsonify
from assistant import get_predefined_or_blog_response
from admin.routes import admin_bp
import os

app = Flask(__name__)
app.register_blueprint(admin_bp, url_prefix="/admin")


@app.route("/assistant", methods=["POST"])
def assistant_endpoint():
    payload = request.json or {}
    topic = payload.get("topic", "")
    lang = payload.get("lang", "en")

    if not topic.strip():
        return jsonify({"type": "error", "response": "Missing topic"}), 400

    result = get_predefined_or_blog_response(topic, lang)

    if result:
        return jsonify(result)

    return jsonify({
        "type": "none",
        "response": "No predefined answer or blog post match found."
    })


# -------------------------------
# RUN LOCALLY (dev mode) OR Gunicorn
# -------------------------------
if __name__ == "__main__":
    # Get port from environment (Cloud Run sets PORT)
    port = int(os.environ.get("PORT", 8080))
    # Bind to 0.0.0.0 so Cloud Run can route traffic
    app.run(host="0.0.0.0", port=port)
