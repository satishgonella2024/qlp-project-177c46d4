from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/version")
def get_version():
    """
    Returns the current version of the microservice.
    """
    return {"version": os.getenv("APP_VERSION", "1.0.0")}