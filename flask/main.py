from config.config import app, db
import endpoints.endpoints

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
