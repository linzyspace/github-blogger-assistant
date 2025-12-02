from flask import Flask, request, jsonify
from assistant import get_predefined_or_blog_response
from admin.routes import admin_bp

app = Flask(__name__)
app.register_blueprint(admin_bp, url_prefix="/admin")

@app.route("/assistant", methods=["POST"])
def assistant_endpoint():
    payload = request.json or {}
    topic = payload.get("topic", "")
    lang = payload.get("lang", "en")

    result = get_predefined_or_blog_response(topic, lang)

    if result:
        return jsonify(result)

    return jsonify({
        "type": "none",
        "response": "No predefined answer or blog post match found."
    })

