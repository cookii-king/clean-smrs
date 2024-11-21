from config.config import app, db
from flask import request, jsonify, abort

@app.get("/about")
def about():
    return "About."