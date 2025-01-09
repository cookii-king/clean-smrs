import os
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
ma = Marshmallow()

class Config:
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # Register Blueprints
    from pages.classes.system.view import system_bp
    from pages.classes.observation.view import observation_bp
    app.register_blueprint(system_bp)
    app.register_blueprint(observation_bp)

    # Register Swagger UI
    register_swagger_ui(app)

    return app

def register_swagger_ui(app):
    """Register Swagger UI blueprint."""
    SWAGGER_URL = '/api'
    API_URL = '/static/swagger.yaml'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Test application"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def validate_api_key(func):
    """Decorator to validate API key."""
    def wrapper(*args, **kwargs):
        try:
            DJANGO_URL = os.getenv("DJANGO_URL")
            DJANGO_LOCAL_HOST_URL = os.getenv("DJANGO_LOCAL_HOST_URL")

            # Use local Django URL if DEBUG is enabled
            if Config.DEBUG:
                DJANGO_URL = DJANGO_LOCAL_HOST_URL

            if not DJANGO_URL:
                raise ValueError("DJANGO_URL is not set in the environment variables.")

            print(f"Validating API key with DJANGO_URL: {DJANGO_URL}")

            # Get API key from request headers
            api_key = request.headers.get("X-API-KEY")
            if not api_key:
                return jsonify({"error": "API key is missing"}), 401

            # Payload and headers for Django validation request
            payload = {"api_key": api_key}
            headers = {"Content-Type": "application/json"}

            # Make POST request to Django endpoint
            response = requests.post(
                f"{DJANGO_URL}/api-key/validate/",
                json=payload,
                headers=headers,
                timeout=5
            )
            response.raise_for_status()

            # If validation succeeds, call the original function
            return func(*args, **kwargs)

        except requests.exceptions.RequestException as re:
            error_message = (
                re.response.json() if re.response and re.response.content else str(re)
            )
            return jsonify({"error": f"API key validation failed: {error_message}"}), 403

    return wrapper