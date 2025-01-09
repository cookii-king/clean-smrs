from flask import Blueprint

# Create a Blueprint for the system routes
system_bp = Blueprint('system', __name__)

@system_bp.route("/", methods=["GET"])
def root():
    return "Hello World!"