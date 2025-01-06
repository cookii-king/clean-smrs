import os
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
DEBUG = False

# Load Django URL from environment variables
DJANGO_URL = os.getenv("DJANGO_URL")
DJANGO_LOCAL_HOST_URL = os.getenv("DJANGO_LOCAL_HOST_URL")

# Use local Django URL if DEBUG is enabled
if DEBUG:
    DJANGO_URL = DJANGO_LOCAL_HOST_URL

# Check if DJANGO_URL is properly set
if not DJANGO_URL:
    raise ValueError("DJANGO_URL is not set in the environment variables.")

def validate_api_key(func):
    def wrapper(*args, **kwargs):
        try:
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
