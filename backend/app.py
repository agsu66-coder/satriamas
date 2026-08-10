from flask import Flask, request, jsonify

# ==============================
# Services
# ==============================

from services.ai_service import ai_service
from services.template_service import template_service
from services.knowledge_engine import knowledge_engine

# ==============================
# Routes
# ==============================

from routes.template_routes import template_bp

# ==============================
# Flask App
# ==============================

app = Flask(__name__)

# ==============================
# Load Engine
# ==============================

template_service.load_templates()

knowledge_engine.load()

# ==============================
# Register Blueprint
# ==============================

app.register_blueprint(template_bp)

# ==============================
# HOME
# ==============================

@app.route("/")
def home():

    return jsonify({

        "status": "online",

        "service": "TERATAI AI Backend",

        "version": "0.2.0"

    })

# ==============================
# HEALTH CHECK
# ==============================

@app.route("/health")
def health():

    return jsonify({

        "success": True,

        "status": "healthy",

        "service": "TERATAI AI",

        "version": "0.2.0"

    })

# ==============================
# ASK AI
# ==============================

@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()

    if not data:

        return jsonify({

            "success": False,

            "answer": "Data tidak ditemukan."

        }), 400

    query = data.get("query", "").strip()

    if query == "":

        return jsonify({

            "success": False,

            "answer": "Silakan masukkan pertanyaan."

        }), 400

    response = ai_service.reply(query)

    return jsonify(

        response.to_dict()

    )

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    print("=" * 50)
    print("TERATAI AI BACKEND")
    print("Version : 0.2.0")
    print("Status  : ONLINE")
    print("=" * 50)

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=False

    )