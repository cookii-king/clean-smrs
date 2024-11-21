from config.config import app, db
from classes.observation import Observation, observations_schema, observation_schema
from flask import request, jsonify, abort

@app.put("/observation/<observation_id>/update")
def update_observation(observation_id):
    data = request.get_json()
    required_fields = [
        "date", "time", "time_zone_offset", "coordinates", "temperature_water", 
        "temperature_air", "humidity", "wind_speed", "wind_direction", 
        "precipitation", "haze", "becquerel", "notes",
    ]

    if not any(key in data for key in required_fields):
        abort(400, description="Missing required fields for update")

    updated_observation = Observation.update(observation_id, data)
    if updated_observation:
        result = observation_schema.dump(updated_observation)
        return jsonify(result), 200
    else:
        return {"message": "Observation not found."}, 404