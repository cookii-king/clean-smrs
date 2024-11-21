from config.config import app, db
from classes.observation import Observation, observations_schema, observation_schema
from flask import request, jsonify, abort

@app.delete("/observation/<observation_id>/delete")
def delete_observation(observation_id):
    result = Observation.delete(observation_id)
    if "message" in result:
        return result, 200
    return {"message": "Observation not found."}, 404
