from config.config import app, db
from classes.observation import Observation, observations_schema, observation_schema
from flask import request, jsonify, abort

from datetime import datetime, date, time

@app.post("/observation/create")
def create_observation():
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



# @app.post("/observation/<observation_id>/delete")
# def soft_delete_observation(observation_id):
#     observation = Observation.soft_delete(observation_id)
#     if observation:
#         return {
#             "message": f"Observation {observation_id} soft deleted successfully.",
#             "observation": observation_schema.dump(observation)
#         }, 200
#     return {"message": "Observation not found."}, 404


@app.post("/observation/<observation_id>/delete-permanently")
def delete_observation_permanently(observation_id):
    result = Observation.delete(observation_id)
    if "message" in result:
        return result, 200
    return {"message": "Observation not found."}, 404