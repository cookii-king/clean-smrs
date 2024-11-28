from config.config import create_app, db
from flask import render_template, request, jsonify
from classes.observation import Observation, observation_schema, observations_schema
from datetime import datetime
from uuid import UUID


# Create the app (LOOK THE CONFIG.APP TEAM)
app = create_app()

# Create all tables directly within the app context
with app.app_context():
    db.create_all()  # Create the tables in cleansmrs.db when the app starts

# Get all observations
@app.get('/observations/')
def get_all_observations():
    """Endpoint to view all observations records."""
    observations = Observation.query.all()
    return observations_schema.jsonify(observations)

#RETREIVE THE DATA THRO CURL COMMAND
#curl -X GET http://127.0.0.1:5000/observations/OBSERVATION ID HERE
@app.route('/observations/<observation_id>', methods=['GET'])
def get_observation_by_id(observation_id):
    """Endpoint to retrieve a single observation by its UUID."""
    try:
        # Try to convert the observation_id to a valid UUID
        observation_uuid = UUID(observation_id)
    except ValueError:
        return jsonify({"message": "Invalid UUID format."}), 400

    # Now query the database using the UUID
    observation = Observation.query.filter_by(id=observation_uuid).first()

    if observation:
        # If the observation is found, return it as a JSON response
        return observation_schema.jsonify(observation)
    else:
        return jsonify({"message": "Observation not found."}), 404   

# Route to render the add observation form
@app.get('/observations/add')
def get_add_observation_form():
    """Render the form to add a new observation."""
    return render_template('add_observation.html')

# Add a new observation from the form submission
@app.post('/observations/add')
def add_observation():
    """Handle form submission to add a new observation."""
    form_data = request.form.to_dict()  # Get the form data

    # Convert the date string into a proper Python date object
    try:
        date_str = form_data.get('date')  # Get the date from the form data
        if date_str:
            # Convert string 'YYYY-MM-DD' to a datetime.date object
            form_data['date'] = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Create a new observation using the form data
        new_observation = Observation.create(form_data)
        return jsonify({"message": "Observation added successfully!", "observation": observation_schema.dump(new_observation)}), 201
    except Exception as e:
        return jsonify({"message": f"Error creating observation: {str(e)}"}), 500

@app.route('/observations/delete', methods=['GET', 'POST'])
def delete_observation():
    if request.method == 'POST':
        observation_id = request.form.get('observation_id')

        # Find the observation by ID and delete it
        observation = Observation.query.get(observation_id)
        if observation:
            db.session.delete(observation)
            db.session.commit()
            return jsonify({"message": "Observation deleted successfully!"}), 200
        else:
            return jsonify({"message": "Observation not found!"}), 404

    return render_template('delete_observation.html')

@app.route('/observations/check-id', methods=['POST'])
def check_observation_id():
    observation_id = request.form['observation_id']
    observation = Observation.query.get(observation_id)
    
    if observation:
        # If found, pass the observation to the update form
        # http://127.0.0.1:5000/observations/update?observation_id=<ID> write the id u want to update
        return render_template('update_observation.html', observation=observation)
    else:
        # If not found, return a JSON response with an error message
        return jsonify({"message": "Observation ID not found, please try again."}), 404

@app.route('/observations/update', methods=['GET', 'POST'])
def update_observation():
    if request.method == 'GET':
        observation_id = request.args.get('observation_id')  # Get the observation ID from the query string
        observation = Observation.query.get(observation_id)

        if observation:
            # If observation is found, pass it to the template
            return render_template('update_observation.html', observation=observation)
        else:
            return jsonify({"message": "Observation not found."}), 404

    if request.method == 'POST':
        observation_id = request.form['observation_id']
        observation = Observation.query.get(observation_id)

        if observation:
            # Update the observation with the new values
            observation.date = datetime.strptime(request.form['date'], '%Y-%m-%d')
            observation.time = request.form['time']
            observation.coordinates = request.form['coordinates']
            observation.temperature_air = request.form['temperature_air']
            db.session.commit()

            return jsonify({"message": "Observation updated successfully!"}), 200
        else:
            return jsonify({"message": "Observation not found."}), 404
   
if __name__ == "__main__":
    app.run(debug=True)
