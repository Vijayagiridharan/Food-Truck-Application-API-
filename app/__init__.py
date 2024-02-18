from flask import Flask
from dotenv import load_dotenv
from .models import db  # Import db from models module

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize plugins here SQLAlchemy or other
    db.init_app(app)

    # Register Blueprints
    from .module_one import bp as module_one_bp
    app.register_blueprint(module_one_bp)

    # Ensure all database models are created
    with app.app_context():
        db.create_all()

    return app
