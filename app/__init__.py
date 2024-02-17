from flask import Flask
from dotenv import load_dotenv
from models import db

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Configure the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-uri'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.module_one import bp as module_one_bp
    app.register_blueprint(module_one_bp)
    # Register Blueprints
    
    return app
