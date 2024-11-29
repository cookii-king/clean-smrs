import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint


# Swagger configuration
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        "app_name": "Clean SMRs"
    }
)

def create_app():
    # Create the Flask app
    app = Flask(__name__, template_folder='../templates')
    # Configure your app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cleansmrs.db'  # SQLite database URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking
    app.config['SWAGGER_URL'] = SWAGGER_URL
    app.config['API_URL'] = API_URL

    # Register the Swagger UI blueprint
    app.register_blueprint(swaggerui_blueprint)

    # Initialize the extensions with the app instance
    db.init_app(app)
    ma.init_app(app)

    return app


# Initialize db and marshmallow here as global instances
db = SQLAlchemy()
ma = Marshmallow()
