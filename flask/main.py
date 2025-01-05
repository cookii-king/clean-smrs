from config.config import app, db
from pages import endpoints

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)