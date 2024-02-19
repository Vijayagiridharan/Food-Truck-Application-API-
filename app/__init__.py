from flask import Flask
from dotenv import load_dotenv

from models import db

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')


  

    # Register Blueprints
    from .signup import bp as signup_bp
    app.register_blueprint(signup_bp)


    
    # Configure the database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-uri'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from app.login import bp as login_bp
    app.register_blueprint(login_bp)
    # Register Blueprints
    

    return app

