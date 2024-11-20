from config.config import app, db
import endpoints.endpoints

with app.app_context():
    db.create_all()

@app.get("/")
def root():
    return "Hello World!"

@app.get("/about")
def about():
    return "About."

if __name__ == "__main__":
    app.run(debug=True)
