from config.config import app

@app.get("/")
def root():
    return "Hello World!"