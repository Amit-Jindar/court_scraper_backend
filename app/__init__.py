from flask import Flask
from flask import Flask
from app.api.routes import app  # Import Flask app directly

def create_app():
    return app
