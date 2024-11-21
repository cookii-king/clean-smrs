from config.config import app, db
from classes.observation import Observation, observations_schema, observation_schema
from flask import request, jsonify, abort

@app.get("/observations")
def get_observations():
    all_observations = Observation.get_all()
    result = observations_schema.dump(all_observations)
    return jsonify(result)


@app.get("/observation/<observation_id>")
def get_observation(observation_id):
    observation = Observation.get(observation_id)
    if observation is None:
        abort(404, description="Observation not found")
    result = observation_schema.dump(observation)
    return jsonify(result)