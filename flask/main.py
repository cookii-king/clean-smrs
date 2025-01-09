from config.config import create_app, db

def setup_database(app):
    """Create database tables."""
    with app.app_context():
        db.create_all()

def main():
    """Run the Flask application."""
    app = create_app()
    setup_database(app)
    app.run(debug=app.config['DEBUG'])

if __name__ == "__main__":
    main()