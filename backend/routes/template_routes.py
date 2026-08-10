from flask import Blueprint, jsonify, request

from services.template_service import template_service


template_bp = Blueprint(
    "template",
    __name__
)


# =====================================================
# GET TEMPLATE
# =====================================================

@template_bp.route("/template/<key>", methods=["GET"])
def get_template(key):

    message = template_service.get(key)

    return jsonify({

        "success": True,

        "message": message

    })


# =====================================================
# RENDER TEMPLATE
# =====================================================

@template_bp.route("/template/render", methods=["POST"])
def render_template():

    data = request.get_json()

    if not data:

        return jsonify({

            "success": False,

            "message": "Data tidak ditemukan."

        }), 400


    key = data.get("key", "")

    values = data.get("data", {})


    message = template_service.render(

        key,

        values

    )


    if message is None:

        return jsonify({

            "success": False,

            "message": f"Template dengan KEY '{key}' tidak ditemukan."

        }), 404


    return jsonify({

        "success": True,

        "message": message

    })


# =====================================================
# LIST TEMPLATE
# =====================================================

@template_bp.route("/template/list", methods=["GET"])
def list_template():

    keys = list(

        template_service.templates.keys()

    )


    return jsonify({

        "success": True,

        "total": len(keys),

        "keys": keys

    })


# =====================================================
# RELOAD TEMPLATE
# =====================================================

@template_bp.route("/template/reload", methods=["POST"])
def reload_template():

    template_service.load_templates()


    return jsonify({

        "success": True,

        "message": "Template berhasil di-reload."

    })