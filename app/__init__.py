from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize plugins here SQLAlchemy or other
    from app.module_one import bp as module_one_bp
    app.register_blueprint(module_one_bp)
    # Register Blueprints
    
    
    return app
