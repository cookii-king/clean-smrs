from flask import Blueprint, request, abort, jsonify
from datetime import datetime
from config.config import validate_api_key
from .model import Observation, observation_schema, observations_schema

# Create a Blueprint for the observation routes
observation_bp = Blueprint('observation', __name__)

@observation_bp.route("/observations", methods=["GET"], endpoint='list_observations')
# @validate_api_key
def list_observations():
    """List all observations."""
    try:
        all_observations = Observation.get_all()
        result = observations_schema.dump(all_observations)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"'GET' Method Failed for observations: {str(e)}"}), 400

@observation_bp.route("/observation/<observation_id>", methods=["GET"], endpoint='get_observation')
@validate_api_key
def get_observation(observation_id):
    """Get a single observation by ID."""
    try:
        observation = Observation.get(observation_id)
        if observation is None:
            abort(404, description="Observation not found")
        result = observation_schema.dump(observation)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"'GET' Method Failed for observation: {str(e)}"}), 400

@observation_bp.route("/observation/create", methods=["POST"], endpoint='create_observation')
# @validate_api_key
def create_observation():
    """Create a new observation."""
    try:
        data = request.get_json()
        
        required_fields = [
            "date", "time", "time_zone_offset", "latitude", "longitude",
            "temperature_water", "temperature_air", "humidity", "wind_speed",
            "wind_direction", "precipitation", "haze", "becquerel", "notes"
        ]

        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            abort(400, description=f"Missing required fields: {', '.join(missing_fields)}")
        
        try:
            data["date"] = datetime.strptime(data["date"], "%Y-%m-%d").date()
            data["time"] = datetime.strptime(data["time"], "%H:%M:%S").time()
        except ValueError as e:
            abort(400, description=f"Invalid date or time format: {e}")

        data["coordinates"] = f"{data['latitude']},{data['longitude']}"

        new_observation = Observation.create(data)
        result = observation_schema.dump(new_observation)

        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": f"'POST' Method Failed for observation: {str(e)}"}), 400