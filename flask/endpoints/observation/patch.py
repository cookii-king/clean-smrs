from config.config import app, db
from classes.observation import Observation, observations_schema, observation_schema
from flask import request, jsonify, abort

@app.patch("/observation/<observation_id>/update")
def patch_observation(observation_id):
    data = request.get_json()
    updated_observation = Observation.patch(observation_id, data)
    if updated_observation:
        result = observation_schema.dump(updated_observation)
        return jsonify(result), 200
    else:
        return {"message": "Observation not found."}, 404