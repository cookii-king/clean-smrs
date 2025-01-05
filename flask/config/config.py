import os
import requests
from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

DJANGO_URL = os.getenv('DJANGO_URL', 'http://127.0.0.1:8000')  # Use environment variable for flexibility
# # Django server URL
# DJANGO_URL = "http://127.0.0.1:8000"  # Replace with your Django server's URL

def validate_api_key(func):
    def wrapper(*args, **kwargs):
        try:
            # Payload to send to Django
            api_key = request.headers.get('X-API-KEY')
            payload = {
                'api_key': api_key,
            }

            # Headers (if needed, e.g., for authentication)
            headers = {
                'Content-Type': 'application/json',
            }

            # Make POST request to Django endpoint
            response = requests.post(
                f'{DJANGO_URL}/api-key/validate/',
                json=payload,
                headers=headers,
                timeout=5
            )

            # Check the response from Django
            response.raise_for_status()

            # If validation is successful, proceed to the original function
            return func(*args, **kwargs)
        except requests.exceptions.RequestException as re:
            return jsonify({"error": f"API key validation failed: {str(re.response.json())}"}), 403

    return wrapper
# def validate_api_key(func):
#     def inner(*args, **kwargs):
#         try:
#             api_key = request.headers.get('X-API-KEY')
#             response = requests.post(f'{DJANGO_URL}/api-key/validate/', json={'api_key': api_key}, timeout=5)
#             response.raise_for_status()
#         except Exception as e:
#                 # raise f"Error: ${e}"
#                 print(f"Error: ${e}")
#     return inner        
 
# def validate_api_key(func):
#     def wrapper(*args, **kwargs):
#         api_key = request.headers.get('X-API-KEY')
#         if not api_key:
#             return jsonify({'error': 'API key is missing'}), 401

#         try:
#             # Validate the API key with the Django backend
#             response = requests.post(f'{DJANGO_URL}/api-key/validate/', json={'api_key': api_key}, timeout=5)
#             response.raise_for_status()

#             try:
#                 data = response.json()
#                 if not data.get('valid'):
#                     return jsonify({'error': data.get('message', 'Unauthorized')}), 403
#             except ValueError:
#                 return jsonify({'error': 'Invalid response from validation server'}), 500

#         except Exception as e:  # Catch all exceptions instead of RequestException
#             return jsonify({'error': f'Validation server error: {str(e)}'}), 500

#         # Execute the wrapped function
#         try:
#             return func(*args, **kwargs)
#         except Exception as e:
#             return jsonify({'error': f'Error in wrapped function: {str(e)}'}), 500

#     return wrapper
