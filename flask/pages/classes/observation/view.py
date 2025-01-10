import requests
import traceback
from config.config import app, validate_api_key
from flask import request, abort, jsonify
from datetime import datetime
from ...classes.observation.model import Observation, observation_schema, observations_schema


# @app.get("/observations", endpoint="get_observations")
# @validate_api_key
# def get_observations():
#     try:
#         all_observations = Observation.get_all()
#         result = observations_schema.dump(all_observations)
#         return jsonify(result), 200
#     except Exception as e:
#         # traceback.print_exc()  # Log full traceback for other exceptions
#         return jsonify({"error": f"'GET' Method Failed for observations: {str(e)}"}), 400

# # observation start
@app.post("/observation/create", endpoint="create_observation")
@validate_api_key
def create_observation():
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


@app.post("/observation/<observation_id>", endpoint="post_observation")
@validate_api_key
def post_observation(observation_id):
    try:
        return jsonify({"message": "POST request received"}), 201
    except Exception as e:
        return jsonify({"error": f"'POST' Method Failed for observation: {str(e)}"}), 400


@app.get("/observation/<observation_id>", endpoint="get_observation")
@validate_api_key
def get_observation(observation_id):
    try:
        observation = Observation.get(observation_id)
        if observation is None:
            abort(404, description="Observation not found")
        result = observation_schema.dump(observation)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"'GET' Method Failed for observation: {str(e)}"}), 400

@app.put("/observation/<observation_id>", endpoint="put_observation")
@validate_api_key
def put_observation(observation_id):
    try:
        return jsonify({"message": "PUT request received"}), 201
    except Exception as e:
        return jsonify({"error": f"'PUT' Method Failed for observation: {str(e)}"}), 400

@app.patch("/observation/<observation_id>", endpoint="patch_observation")
@validate_api_key
def patch_observation(observation_id):
    try:
        return jsonify({"message": "PATCH request received"}), 200
    except Exception as e:
        return jsonify({"error": f"'PATCH' Method Failed for observation: {str(e)}"}), 400

@app.delete("/observation/<observation_id>", endpoint="delete_observation")
@validate_api_key
def delete_observation(observation_id):
    try:
        return jsonify({"message": "DELETE request received"}), 200
    except Exception as e:
        return jsonify({"error": f"'DELETE' Method Failed for observation: {str(e)}"}), 400
# # observation end
# # ========================================================================== #
# # ========================================================================== #


# # observations start
@app.post("/observations", endpoint="post_observations")
@validate_api_key
def post_observations():
    try:
        return jsonify({"message": "POST request received"}), 201
    except Exception as e:
        return jsonify({"error": f"'POST' Method Failed for observations {str(e)}"}), 400


@app.get("/observations", endpoint="get_observations")
@validate_api_key
def get_observations():
    try:
        all_observations = Observation.get_all()
        result = observations_schema.dump(all_observations)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"'GET' Method Failed for observations: {str(e)}"}), 400

@app.put("/observations", endpoint="put_observations")
@validate_api_key
def put_observations():
    try:
        return jsonify({"message": "PUT request received"}), 201
    except Exception as e:
        return jsonify({"error": f"'PUT' Method Failed for observations: {str(e)}"}), 400

@app.patch("/observations", endpoint="patch_observations")
@validate_api_key
def patch_observations():
    try:
        return jsonify({"message": "PATCH request received"}), 200
    except Exception as e:
        return jsonify({"error": f"'PATCH' Method Failed for observations: {str(e)}"}), 400

@app.delete("/observations", endpoint="delete_observations")
@validate_api_key
def delete_observations():
    try:
        return jsonify({"message": "DELETE request received"}), 200
    except Exception as e:
        return jsonify({"error": f"'DELETE' Method Failed for observations: {str(e)}"}), 400
# # observations end
# # ========================================================================== #
# # ========================================================================== #