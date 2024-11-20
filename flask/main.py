import os
from flask import Flask # type: ignore
app = Flask(__name__)

@app.get("/")
def root():
    return "Hello World!"

@app.get("/about")
def root():
    return "About."