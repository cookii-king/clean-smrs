from config.config import app, db
from flask import request, jsonify, abort

@app.get("/")
def root():
    return "Hello World!"