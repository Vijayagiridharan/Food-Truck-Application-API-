from flask import Flask
from config import Config
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize plugins here SQLAlchemy or other
    
    # Register Blueprints
    
    
    return app
